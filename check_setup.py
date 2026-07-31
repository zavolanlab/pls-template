"""Pre-flight check. Run this before the Week 2 session:  python check_setup.py

It does not fix anything. It tells you what is missing, so that the session is not spent
on installation.

`ruff` is reported as a warning rather than a failure: it is in `environment.yml` and you will
need it from Week 5, so a warning here means your environment was not built from that file.
"""
import shutil
import subprocess
import sys

# Importable packages. The command-line tools (git, conda, jupyter, ruff) are checked below.
REQUIRED = ["numpy", "scipy", "pandas", "matplotlib", "sklearn", "yaml", "pytest"]


def version_of(cmd):
    exe = shutil.which(cmd)
    if exe is None:
        return None
    try:
        out = subprocess.run([cmd, "--version"], capture_output=True, text=True, timeout=15)
        return (out.stdout or out.stderr).strip().splitlines()[0]
    except Exception:
        return "found, but would not report a version"


def main():
    problems = []

    py = sys.version_info
    ok = (py.major, py.minor) >= (3, 11)
    print(f"[{'PASS' if ok else 'FAIL'}] Python {py.major}.{py.minor}.{py.micro} (need 3.11+)")
    if not ok:
        problems.append("Python is older than 3.11")

    for cmd, needed in (("git", True), ("conda", True), ("jupyter", True), ("ruff", False)):
        v = version_of(cmd)
        if v:
            print(f"[PASS] {cmd}: {v}")
        else:
            print(f"[{'FAIL' if needed else 'WARN'}] {cmd} not found on PATH")
            if needed:
                problems.append(f"{cmd} is not installed or not on PATH")

    for mod in REQUIRED:
        try:
            __import__(mod)
            print(f"[PASS] import {mod}")
        except ImportError:
            print(f"[FAIL] cannot import {mod}")
            problems.append(f"package missing: {mod}")

    print()
    if problems:
        print("NOT READY. Fix these before the session:")
        for p in problems:
            print(f"  - {p}")
        print("\nMost of them are fixed by:  conda env create -f environment.yml")
        sys.exit(1)
    print("READY. Bring your laptop and your questions.")


if __name__ == "__main__":
    main()
