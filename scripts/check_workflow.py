"""Initialize or check a single-cell study index. Python 3 standard library."""
import argparse
import csv
from pathlib import Path, PureWindowsPath
import shutil
import sys

TEMPLATE = Path(__file__).resolve().parents[1] / "assets" / "analysis_index_template.csv"
NEW_RESULTS = {"Completed", "Completed without significant findings"}
WITH_FILES = NEW_RESULTS | {"Reused", "Descriptive only"}
LIMITED = {"Insufficient input or design", "Not applicable"}
OPEN = {"Failed", "Pending"}
FRESH_COUNT_STAGES = {"qc", "normalization", "graph", "clustering", "annotation"}
SCRIPT_SUFFIXES = {".r", ".py", ".sh", ".ps1", ".bat", ".cmd", ".sbatch"}


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames or [], list(reader)


def check_file(value, root):
    path = Path(value)
    if path.is_absolute() or PureWindowsPath(value).drive:
        return f"use a project-relative path: {value}"
    target = (root / path).resolve()
    if not target.is_relative_to(root):
        return f"path leaves project: {value}"
    if not target.is_file() or not target.stat().st_size:
        return f"missing or empty file: {value}"
    return None


def inspect_index(root, path, full, require_run):
    expected, inventory = read_csv(TEMPLATE)
    fields, rows = read_csv(path)
    missing = set(expected).difference(fields)
    if missing:
        return ["missing index columns: " + ", ".join(sorted(missing)) +
                ". Preserve the old index and migrate to the documented schema in a copy."]
    if not rows:
        return ["empty index"]
    errors = []
    seen = set()
    stages = set()
    for number, raw in enumerate(rows, 2):
        if None in raw or any(raw[name] is None for name in expected):
            errors.append(f"row {number}: wrong number of fields")
            continue
        row = {name: raw[name].strip() for name in expected}
        key = tuple(row[name] for name in ("stage_id", "branch", "contrast", "cell_type"))
        stage, branch = key[:2]
        status = row["status"]
        problems = []
        if key in seen:
            problems.append("duplicate stage/branch/contrast/cell type")
        seen.add(key)
        stages.add(stage)
        for name in ("stage_id", "branch", "required_inputs", "evidence"):
            if not row[name]:
                problems.append("missing " + name)
        if status in OPEN:
            problems.append(status + " (work remains)")
        elif status not in WITH_FILES | LIMITED:
            problems.append("unrecognized status: " + status)
        files = [s.strip() for s in row["output_paths"].split(";") if s.strip()]
        if status in WITH_FILES and not files:
            problems.append("missing output paths")
        if stage in require_run and files and all(Path(f).suffix.lower() in SCRIPT_SUFFIXES for f in files):
            problems.append("only scripts are listed; link an executed result")
        if full and stage in {"design", "input", "report"} and status not in WITH_FILES:
            problems.append("full delivery needs evidence-backed design, input review and report")
        if stage in require_run and status not in NEW_RESULTS:
            problems.append("new execution was requested for this stage")
        for value in files:
            problem = check_file(value, root)
            if problem:
                problems.append(problem)
        errors.extend(f"row {number} [{stage} / {branch}]: {p}" for p in problems)
    required = set(require_run)
    if full:
        required.update(row["stage_id"] for row in inventory)
    if required - stages:
        errors.append("missing stages: " + ", ".join(sorted(required - stages)))
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="create a full-run inventory without replacing an existing index")
    check = commands.add_parser("check", help="validate entries and referenced files")
    for command in (init, check):
        command.add_argument("project", type=Path)
    check.add_argument("--index", type=Path, help="alternate project-relative index path for review")
    check.add_argument("--full", action="store_true", help="require a decision for every inventory stage")
    check.add_argument("--fresh-counts", action="store_true",
                       help="full inventory plus newly executed QC, normalization, graph, clustering and annotation")
    check.add_argument("--require-run", nargs="+", default=[], metavar="STAGE",
                       help="require new execution for every listed entry of these stages")
    args = parser.parse_args()
    root = args.project.resolve()
    path = root / "results" / "analysis_index.csv"
    try:
        if args.command == "init":
            path.parent.mkdir(parents=True, exist_ok=True)
            try:
                with TEMPLATE.open("rb") as source, path.open("xb") as target:
                    shutil.copyfileobj(source, target)
            except FileExistsError:
                print(f"Existing index preserved: {path}")
            else:
                print(f"Created {path}")
            return 0
        if args.index:
            path = (root / args.index).resolve()
            if not path.is_relative_to(root):
                parser.error("--index must resolve within the study directory")
        required = set(args.require_run)
        if args.fresh_counts:
            required.update(FRESH_COUNT_STAGES)
        errors = inspect_index(root, path, args.full or args.fresh_counts, required)
    except (OSError, UnicodeError, csv.Error) as error:
        print(error, file=sys.stderr)
        return 1
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("Index coverage and declared files verified. Review scientific contents separately.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
