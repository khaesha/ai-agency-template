"""Record and recover file baselines for AI Agency installations."""

import argparse
import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys
import tempfile


MANIFEST = "agency/INSTALLATION.json"


def file_path(root, relative):
    path = PurePosixPath(relative)
    if path.is_absolute() or ".." in path.parts or not path.parts or str(path) != relative:
        raise ValueError(f"Expected a normalized relative file path: {relative}")
    resolved = (root / path).resolve()
    resolved.relative_to(root)
    return resolved


def read_manifest(path):
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"version": 1, "files": {}}
    if (
        not isinstance(manifest, dict)
        or manifest.get("version") != 1
        or not isinstance(manifest.get("files"), dict)
    ):
        raise ValueError(f"Unsupported installation manifest: {path}")
    return manifest


def sha256(content):
    return hashlib.sha256(content).hexdigest()


def record(args, path, manifest):
    source_root = args.source_root.resolve()
    project_root = args.project.resolve()
    files = manifest["files"].copy()
    for source, destination in args.file:
        if not file_path(project_root, destination).is_file():
            raise ValueError(f"Installed file is missing: {destination}")
        content = file_path(source_root, source).read_bytes()
        files[destination] = {
            "source_path": source,
            "source_reference": args.reference,
            "source_sha256": sha256(content),
            "source_content_base64": base64.b64encode(content).decode("ascii"),
        }
    updated = {**manifest, "files": files}
    if updated == manifest:
        return

    # Keep the previous manifest readable if the write is interrupted.
    with tempfile.TemporaryDirectory(dir=path.parent) as directory:
        temporary = Path(directory) / path.name
        temporary.write_text(json.dumps(updated, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        temporary.replace(path)


def baseline(destination, manifest):
    entry = manifest["files"].get(destination)
    if entry is None:
        raise ValueError(f"No recorded baseline for {destination}")
    content = base64.b64decode(entry["source_content_base64"], validate=True)
    if sha256(content) != entry["source_sha256"]:
        raise ValueError(f"Baseline hash does not match for {destination}")
    sys.stdout.buffer.write(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="Destination project root")
    commands = parser.add_subparsers(dest="command", required=True)
    record_command = commands.add_parser("record", help="Record source bytes for selected installed files")
    record_command.add_argument("source_root", type=Path)
    record_command.add_argument("reference", help="Source commit, archive reference, or checkout label")
    record_command.add_argument("--file", nargs=2, action="append", required=True, metavar=("SOURCE", "DESTINATION"))
    baseline_command = commands.add_parser("baseline", help="Write a recorded baseline to standard output")
    baseline_command.add_argument("destination", help="Project-relative installed file path")
    args = parser.parse_args()

    try:
        path = file_path(args.project.resolve(), MANIFEST)
        manifest = read_manifest(path)
        if args.command == "record":
            record(args, path, manifest)
        else:
            baseline(args.destination, manifest)
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
