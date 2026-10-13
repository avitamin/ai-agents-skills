#!/usr/bin/env python3
"""Keep generated documentation in sync with skill frontmatter.

Walks ``skills/*/SKILL.md``, validates the YAML frontmatter, renders the
skills table and regenerates ``README.md`` from ``templates/README.md``.

Usage:
    python scripts/update_docs.py           # regenerate README.md
    python scripts/update_docs.py --check   # verify only; exit 1 if README.md is stale

Exit codes:
    0  README.md is up to date (or was regenerated)
    1  --check found README.md stale
    2  a skill or template failed validation
"""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
TEMPLATE_PATH = REPO_ROOT / "templates" / "README.md"
TARGET_PATH = REPO_ROOT / "README.md"

TABLE_PLACEHOLDER = "skills_table"

PLACEHOLDER_RE = re.compile(r"\{\{\s*(\w+)\s*\}\}")
SENTENCE_END_RE = re.compile(r"[.!?]+(?=\s|$)")


class DocGenError(Exception):
    """A skill file or template failed validation."""


@dataclass(frozen=True)
class Skill:
    """Public metadata of a skill, taken from its SKILL.md frontmatter."""

    name: str
    description: str


def parse_frontmatter(text: str, path: Path) -> dict:
    """Return the YAML frontmatter mapping of a SKILL.md file."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise DocGenError(f"{path}: no YAML frontmatter — the file must start with a '---' line")
    for idx in range(1, len(lines)):
        if lines[idx].strip() != "---":
            continue
        try:
            data = yaml.safe_load("\n".join(lines[1:idx]))
        except yaml.YAMLError as exc:
            raise DocGenError(f"{path}: invalid YAML frontmatter: {exc}") from exc
        if not isinstance(data, dict):
            raise DocGenError(
                f"{path}: frontmatter must be a YAML mapping, got {type(data).__name__}"
            )
        return data
    raise DocGenError(f"{path}: frontmatter is not closed — missing closing '---'")


def collect_skills(skills_dir: Path) -> list[Skill]:
    """Collect public skills from ``skills_dir``, sorted by name.

    Skills with ``metadata.internal: true`` are skipped (work in progress,
    hidden from listings, same semantics as skills.sh). Raises DocGenError
    on any SKILL.md that violates the frontmatter rules.
    """
    if not skills_dir.is_dir():
        raise DocGenError(f"{skills_dir}: skills directory not found")
    skills: list[Skill] = []
    for entry in sorted(skills_dir.iterdir()):
        if not entry.is_dir():
            continue
        skill_file = entry / "SKILL.md"
        if not skill_file.is_file():
            continue
        data = parse_frontmatter(skill_file.read_text(encoding="utf-8"), skill_file)
        name = data.get("name")
        description = data.get("description")
        if not isinstance(name, str) or not name.strip():
            raise DocGenError(f"{skill_file}: 'name' is required and must be a non-empty string")
        if not isinstance(description, str) or not description.strip():
            raise DocGenError(
                f"{skill_file}: 'description' is required and must be a non-empty string"
            )
        if name != entry.name:
            raise DocGenError(
                f"{skill_file}: 'name' ({name!r}) must match the folder name ({entry.name!r})"
            )
        metadata = data.get("metadata") or {}
        if not isinstance(metadata, dict):
            raise DocGenError(f"{skill_file}: 'metadata' must be a mapping")
        if metadata.get("internal") is True:
            continue
        skills.append(Skill(name=name, description=description.strip()))
    if not skills:
        raise DocGenError(
            f"{skills_dir}: no public skills found "
            "(every skills/<name>/SKILL.md is missing, internal, or invalid)"
        )
    return skills


def first_sentence(text: str) -> str:
    """Return the first sentence of ``text`` with whitespace collapsed."""
    text = " ".join(text.split())
    match = SENTENCE_END_RE.search(text)
    return text[: match.end()] if match else text


def render_table(skills: list[Skill]) -> str:
    """Render the skills markdown table (Name links + first-sentence descriptions)."""
    lines = ["| Name | Description |", "| --- | --- |"]
    for skill in skills:
        description = first_sentence(skill.description).replace("|", "\\|")
        lines.append(f"| [`{skill.name}`](skills/{skill.name}/SKILL.md) | {description} |")
    return "\n".join(lines)


def render(template: str, replacements: dict[str, str], template_path: Path) -> str:
    """Substitute ``{{ key }}`` placeholders in ``template``.

    Fails on placeholders that are unknown or declared but missing from the
    template, so a typo cannot silently drop generated content.
    """
    used: set[str] = set()

    def substitute(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in replacements:
            known = ", ".join(sorted(replacements)) or "none"
            raise DocGenError(f"{template_path}: unknown placeholder '{{{key}}}' (known: {known})")
        used.add(key)
        return replacements[key]

    rendered = PLACEHOLDER_RE.sub(substitute, template)
    missing = set(replacements) - used
    if missing:
        keys = ", ".join("{{" + key + "}}" for key in sorted(missing))
        raise DocGenError(f"{template_path}: placeholder {keys} not found in template")
    return rendered


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="update_docs",
        description="Regenerate README.md from templates/README.md and skills frontmatter.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="do not write anything; exit 1 if README.md is stale",
    )
    args = parser.parse_args(argv)

    try:
        skills = collect_skills(SKILLS_DIR)
        table = render_table(skills)
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
        rendered = render(template, {TABLE_PLACEHOLDER: table}, TEMPLATE_PATH)
    except DocGenError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    rendered = rendered.rstrip("\n") + "\n"

    rel_target = TARGET_PATH.relative_to(REPO_ROOT)
    current = TARGET_PATH.read_text(encoding="utf-8") if TARGET_PATH.is_file() else ""
    if current == rendered:
        print(f"{rel_target}: up to date ({len(skills)} skills)")
        return 0

    if args.check:
        diff = difflib.unified_diff(
            current.splitlines(keepends=True),
            rendered.splitlines(keepends=True),
            fromfile=str(rel_target),
            tofile="generated",
        )
        sys.stdout.writelines(diff)
        print(f"{rel_target}: stale — run 'python scripts/update_docs.py' ({len(skills)} skills)")
        return 1

    TARGET_PATH.write_text(rendered, encoding="utf-8")
    print(f"{rel_target}: updated ({len(skills)} skills)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
