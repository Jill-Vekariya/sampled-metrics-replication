"""Recalculate checksums for the amended release, preserving the submission baseline.

Run from the repository root:
    python publication/update_amendment_records.py

The frozen scientific summary, scientific source and protocol are never edited.
"""
from pathlib import Path
import hashlib
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
PUB = ROOT / "publication"
PLAN = PUB / "release_plan.json"
MANIFEST = ROOT / "RELEASE_MANIFEST.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save_json(path, data):
    path.write_bytes((json.dumps(data, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))


def main():
    baseline_plan = PUB / "ORIGINAL_SUBMISSION_RELEASE_PLAN.json"
    baseline_manifest = PUB / "ORIGINAL_SUBMISSION_MANIFEST.json"
    if not baseline_plan.exists():
        shutil.copy2(PLAN, baseline_plan)
    if not baseline_manifest.exists():
        shutil.copy2(MANIFEST, baseline_manifest)

    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    for name in plan["file_hashes"]:
        plan["file_hashes"][name] = sha(ROOT / name)
    plan["last_amendment"] = "2026-11-14"
    plan["original_submission_release_plan"] = "publication/ORIGINAL_SUBMISSION_RELEASE_PLAN.json"
    plan["amendment_document"] = "AMENDMENTS.md"
    save_json(PLAN, plan)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest.update({name: {} for name in [
        "AMENDMENTS.md",
        "tests/test_figure3.py",
        "publication/ORIGINAL_SUBMISSION_RELEASE_PLAN.json",
        "publication/ORIGINAL_SUBMISSION_MANIFEST.json",
        "publication/update_amendment_records.py",
    ]})
    new_manifest = {}
    for name in sorted(manifest):
        path = ROOT / name
        if not path.is_file():
            raise FileNotFoundError(name)
        new_manifest[name] = {"bytes": path.stat().st_size, "sha256": sha(path)}
    save_json(MANIFEST, new_manifest)
    print("Updated amended checksums for", len(new_manifest), "files.")


if __name__ == "__main__":
    main()
