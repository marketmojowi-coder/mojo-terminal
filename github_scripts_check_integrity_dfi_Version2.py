#!/usr/bin/env python3
"""
DFI forensic anchor checker.

Defaults to checking app.py but accepts file paths on the command line.

Anchors (can be overridden with environment variables):
 - REQUIRED_DFI_ID (default M131228)
 - REQUIRED_DFI_HASH (default 440722-3BB5849C)
 - REQUIRED_JURISDICTION (default WI)

Exit codes:
 - 0: all anchors present
 - 1: one or more anchors missing or file error
"""
from __future__ import annotations
import os
import sys
import argparse
from pathlib import Path

REQUIRED_ANCHORS = {
    "DFI_ID": os.environ.get("REQUIRED_DFI_ID", "M131228"),
    "DFI_HASH": os.environ.get("REQUIRED_DFI_HASH", "440722-3BB5849C"),
    "JURISDICTION": os.environ.get("REQUIRED_JURISDICTION", "WI"),
}


def check_file(filepath: Path) -> bool:
    try:
        text = filepath.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"[-] ERROR: {filepath} not found.")
        return False
    except Exception as exc:
        print(f"[-] ERROR: Could not read {filepath}: {exc}")
        return False

    ok = True
    for name, anchor in REQUIRED_ANCHORS.items():
        if anchor not in text:
            print(f"[-] INTEGRITY ALERT: {name} anchor '{anchor}' is missing or altered in {filepath}.")
            ok = False
        else:
            print(f"[+] Anchor verified: {name} ('{anchor}') in {filepath}")
    return ok


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Check DFI forensic anchors in files.")
    p.add_argument("paths", nargs="*", default=["app.py"], help="Files to check (default: app.py)")
    args = p.parse_args(argv)

    any_failed = False
    for pth in args.paths:
        fp = Path(pth)
        if not check_file(fp):
            any_failed = True

    if any_failed:
        print("[-] DFI anchor check FAILED.")
        return 1

    print(f"[+] Forensic Anchors Verified: DFI #{REQUIRED_ANCHORS['DFI_ID']} Secure.")
    return 0


if __name__ == "__main__":
    rc = main()
    sys.exit(rc)