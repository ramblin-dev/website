"""Validate indexing files at a given base (directory or URL).

Checks:
  - sitemap.xml parses as XML and contains at least one <loc>
  - robots.txt has a Sitemap: directive pointing somewhere
  - llms.txt is non-empty and starts with an H1
  - IndexNow key file's contents equal its filename (the verification rule)

Exits 1 on the first failure. Used in two places:
  - Netlify build (uv-shim.sh), against `output/` before deploy
  - GitHub Actions daily cron, against `https://ramblin.dev`

Run via `uv run scripts/check_indexing.py [base]`.
"""

from __future__ import annotations

import argparse
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import NoReturn

KEY = "b6746e9d951fd5f64f1059f04b919e7e94b15f34f85d8d903c73a6eb75c5f0d3"


def fail(msg: str) -> NoReturn:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def ok(msg: str) -> None:
    print(f"  ok: {msg}")


def fetch(base: str, path: str) -> str:
    if base.startswith(("http://", "https://")):
        url = f"{base.rstrip('/')}/{path}"
        with urllib.request.urlopen(url, timeout=10) as resp:
            if resp.status != 200:
                raise RuntimeError(f"HTTP {resp.status}")
            return resp.read().decode("utf-8")
    return (Path(base) / path).read_text(encoding="utf-8")


def check(base: str) -> None:
    print(f"Checking {base}")

    print("* sitemap.xml")
    try:
        sitemap = fetch(base, "sitemap.xml")
    except Exception as e:
        fail(f"sitemap.xml not reachable: {e}")
    try:
        root = ET.fromstring(sitemap)
    except ET.ParseError as e:
        fail(f"sitemap.xml is not valid XML: {e}")
    locs = [el for el in root.iter() if el.tag.rsplit("}", 1)[-1] == "loc"]
    if not locs:
        fail("sitemap.xml contains no <loc> entries")
    ok(f"valid XML with {len(locs)} URL(s)")

    print("* robots.txt")
    try:
        robots = fetch(base, "robots.txt")
    except Exception as e:
        fail(f"robots.txt not reachable: {e}")
    has_sitemap = any(
        line.lower().lstrip().startswith("sitemap:") and "http" in line
        for line in robots.splitlines()
    )
    if not has_sitemap:
        fail("robots.txt missing Sitemap: directive")
    ok("has Sitemap: directive")

    print("* llms.txt")
    try:
        llms = fetch(base, "llms.txt")
    except Exception as e:
        fail(f"llms.txt not reachable: {e}")
    if not llms.strip():
        fail("llms.txt is empty")
    if not llms.startswith("# "):
        fail("llms.txt must start with an H1 (# ...)")
    ok("non-empty, starts with H1")

    filename = f"{KEY}.txt"
    print(f"* IndexNow key ({filename})")
    try:
        keyfile = fetch(base, filename)
    except Exception as e:
        fail(f"IndexNow key file not reachable: {e}")
    if keyfile.strip() != KEY:
        fail("IndexNow key file content does not equal filename")
    ok("content matches filename")

    print("All checks passed.")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "base",
        nargs="?",
        default="output",
        help="Directory or URL to check (default: output)",
    )
    args = p.parse_args()
    check(args.base)


if __name__ == "__main__":
    main()
