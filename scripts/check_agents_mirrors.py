#!/usr/bin/env python3
"""Fail if full-text AGENTS.md mirrors drift from the canonical file."""

from __future__ import annotations

import argparse
import difflib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL = ROOT / "AGENTS.md"
MIRRORS = [
    ROOT / ".github/copilot-instructions.md",
    ROOT / ".trae/rules/follow-agents.md",
    ROOT / "CODEBUDDY.md",
    ROOT / ".lingma/rules/follow-agents.md",
    ROOT / ".comate/rules/follow-agents.mdr",
]


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def split_adapter_prefix(text: str) -> tuple[str, str]:
    """Split a tool adapter into (allowed prefix, policy body).

    Allowed prefix is optional YAML frontmatter plus leading HTML comments.
    The remaining body must match AGENTS.md exactly.
    """
    text = normalize(text)
    i = 0
    if text.startswith("---\n"):
        close = text.find("\n---\n", 4)
        if close == -1:
            raise ValueError("unclosed YAML frontmatter")
        i = close + len("\n---\n")

    while True:
        while i < len(text) and text[i] == "\n":
            i += 1
        if text.startswith("<!--", i):
            end = text.find("-->", i)
            if end == -1:
                raise ValueError("unclosed HTML comment")
            i = end + 3
            continue
        break

    while i < len(text) and text[i] == "\n":
        i += 1
    return text[:i], text[i:]


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="rewrite mirrors from AGENTS.md, preserving each file's prefix",
    )
    args = parser.parse_args()

    canonical = normalize(CANONICAL.read_text(encoding="utf-8"))
    failures: list[str] = []

    for path in MIRRORS:
        if not path.is_file():
            failures.append(f"missing mirror: {rel(path)}")
            continue
        try:
            prefix, body = split_adapter_prefix(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            failures.append(f"{rel(path)}: {exc}")
            continue

        if args.write:
            path.write_text(prefix + canonical, encoding="utf-8")
            print(f"updated {rel(path)}")
            continue

        if body == canonical:
            print(f"ok {rel(path)}")
            continue

        diff = "".join(
            difflib.unified_diff(
                canonical.splitlines(keepends=True),
                body.splitlines(keepends=True),
                fromfile=f"AGENTS.md (canonical)",
                tofile=rel(path),
            )
        )
        failures.append(
            f"{rel(path)} does not match AGENTS.md after stripping "
            f"frontmatter/notices.\n{diff}"
        )

    if args.write:
        return 0
    if failures:
        print("AGENTS.md full-text mirrors are out of sync:\n", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        print(
            "\nUpdate AGENTS.md, then refresh mirrors with:\n"
            "  python3 scripts/check_agents_mirrors.py --write",
            file=sys.stderr,
        )
        return 1
    print("all AGENTS.md full-text mirrors match")
    return 0


if __name__ == "__main__":
    sys.exit(main())
