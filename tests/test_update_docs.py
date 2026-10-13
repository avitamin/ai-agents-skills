"""Tests for scripts/update_docs.py."""

import sys
import textwrap
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from update_docs import (  # noqa: E402
    DocGenError,
    Skill,
    collect_skills,
    first_sentence,
    main,
    parse_frontmatter,
    render,
    render_table,
)


def write_skill(skills_dir: Path, name: str, frontmatter: str, body: str = "Body.\n") -> Path:
    skill_dir = skills_dir / name
    skill_dir.mkdir(parents=True)
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(textwrap.dedent(frontmatter) + "\n" + body, encoding="utf-8")
    return skill_file


def make_skills(tmp_path: Path) -> Path:
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    return skills_dir


class TestFirstSentence:
    def test_stops_at_first_period(self):
        assert first_sentence("One sentence. Second one.") == "One sentence."

    def test_without_terminator_returns_all(self):
        assert first_sentence("no terminator here") == "no terminator here"

    def test_collapses_folded_whitespace(self):
        assert first_sentence("Folded\n   text.  Rest.") == "Folded text."

    def test_question_and_exclamation_marks(self):
        assert first_sentence("Is it? Yes.") == "Is it?"
        assert first_sentence("Stop! Go on.") == "Stop!"

    def test_terminator_run_kept_intact(self):
        assert first_sentence("What?. Next.") == "What?."


class TestParseFrontmatter:
    def test_plain_and_quoted_values(self, tmp_path):
        path = tmp_path / "SKILL.md"
        path.write_text(
            '---\nname: example\ndescription: "Quoted \\"value\\"."\n---\nBody.\n',
            encoding="utf-8",
        )
        data = parse_frontmatter(path.read_text(encoding="utf-8"), path)
        assert data == {"name": "example", "description": 'Quoted "value".'}

    def test_folded_block_scalar(self, tmp_path):
        path = tmp_path / "SKILL.md"
        path.write_text(
            "---\nname: x\ndescription: >-\n  First line\n  second line.\n---\nBody.\n",
            encoding="utf-8",
        )
        data = parse_frontmatter(path.read_text(encoding="utf-8"), path)
        assert data["description"] == "First line second line."

    def test_missing_frontmatter(self, tmp_path):
        path = tmp_path / "SKILL.md"
        path.write_text("# No frontmatter\n", encoding="utf-8")
        with pytest.raises(DocGenError, match="no YAML frontmatter"):
            parse_frontmatter(path.read_text(encoding="utf-8"), path)

    def test_unclosed_frontmatter(self, tmp_path):
        path = tmp_path / "SKILL.md"
        path.write_text("---\nname: x\n", encoding="utf-8")
        with pytest.raises(DocGenError, match="not closed"):
            parse_frontmatter(path.read_text(encoding="utf-8"), path)

    def test_non_mapping_frontmatter(self, tmp_path):
        path = tmp_path / "SKILL.md"
        path.write_text("---\njust a string\n---\nBody.\n", encoding="utf-8")
        with pytest.raises(DocGenError, match="mapping"):
            parse_frontmatter(path.read_text(encoding="utf-8"), path)

    def test_invalid_yaml(self, tmp_path):
        path = tmp_path / "SKILL.md"
        path.write_text("---\nname: [unclosed\n---\nBody.\n", encoding="utf-8")
        with pytest.raises(DocGenError, match="invalid YAML"):
            parse_frontmatter(path.read_text(encoding="utf-8"), path)


class TestCollectSkills:
    def test_collects_and_sorts(self, tmp_path):
        skills_dir = make_skills(tmp_path)
        write_skill(skills_dir, "zeta", "---\nname: zeta\ndescription: Zeta skill.\n---\n")
        write_skill(skills_dir, "alpha", "---\nname: alpha\ndescription: Alpha skill.\n---\n")
        assert [s.name for s in collect_skills(skills_dir)] == ["alpha", "zeta"]

    def test_internal_skill_skipped(self, tmp_path):
        skills_dir = make_skills(tmp_path)
        write_skill(skills_dir, "public", "---\nname: public\ndescription: Visible.\n---\n")
        write_skill(
            skills_dir,
            "wip",
            "---\nname: wip\ndescription: Hidden.\nmetadata:\n  internal: true\n---\n",
        )
        assert [s.name for s in collect_skills(skills_dir)] == ["public"]

    def test_folder_without_skill_md_ignored(self, tmp_path):
        skills_dir = make_skills(tmp_path)
        write_skill(skills_dir, "public", "---\nname: public\ndescription: Visible.\n---\n")
        (skills_dir / "scratch").mkdir()
        assert [s.name for s in collect_skills(skills_dir)] == ["public"]

    def test_name_folder_mismatch_rejected(self, tmp_path):
        skills_dir = make_skills(tmp_path)
        write_skill(skills_dir, "folder", "---\nname: other\ndescription: Mismatch.\n---\n")
        with pytest.raises(DocGenError, match="must match the folder name"):
            collect_skills(skills_dir)

    def test_missing_description_rejected(self, tmp_path):
        skills_dir = make_skills(tmp_path)
        write_skill(skills_dir, "broken", "---\nname: broken\n---\n")
        with pytest.raises(DocGenError, match="'description' is required"):
            collect_skills(skills_dir)

    def test_missing_skills_dir_rejected(self, tmp_path):
        with pytest.raises(DocGenError, match="skills directory not found"):
            collect_skills(tmp_path / "nowhere")


class TestRenderTable:
    def test_rows_link_and_describe(self):
        table = render_table([Skill(name="example", description="Does things. And more.")])
        lines = table.splitlines()
        assert lines[0] == "| Name | Description |"
        assert lines[1] == "| --- | --- |"
        assert lines[2] == "| [`example`](skills/example/SKILL.md) | Does things. |"

    def test_escapes_pipe(self):
        table = render_table([Skill(name="a", description="has | pipe. rest")])
        assert "has \\| pipe." in table


class TestRender:
    def test_substitutes_placeholder(self, tmp_path):
        result = render("A {{ skills_table }} B", {"skills_table": "X"}, tmp_path / "t.md")
        assert result == "A X B"

    def test_unknown_placeholder_rejected(self, tmp_path):
        with pytest.raises(DocGenError, match=r"unknown placeholder '\{other\}'"):
            render("{{ other }}", {"skills_table": "X"}, tmp_path / "t.md")

    def test_missing_required_placeholder_rejected(self, tmp_path):
        with pytest.raises(DocGenError, match="not found in template"):
            render("no placeholders here", {"skills_table": "X"}, tmp_path / "t.md")


class TestMain:
    def test_end_to_end_check_and_update(self, tmp_path, monkeypatch, capsys):
        skills_dir = make_skills(tmp_path)
        write_skill(skills_dir, "example", "---\nname: example\ndescription: Demo skill.\n---\n")
        template = tmp_path / "README.md"
        template.write_text("# Title\n\n{{ skills_table }}\n", encoding="utf-8")
        target = tmp_path / "out.md"

        monkeypatch.setattr("update_docs.SKILLS_DIR", skills_dir)
        monkeypatch.setattr("update_docs.TEMPLATE_PATH", template)
        monkeypatch.setattr("update_docs.TARGET_PATH", target)
        monkeypatch.setattr("update_docs.REPO_ROOT", tmp_path)

        assert main([]) == 0
        assert "updated" in capsys.readouterr().out
        assert "| [`example`](skills/example/SKILL.md) | Demo skill. |" in target.read_text(
            encoding="utf-8"
        )

        assert main([]) == 0
        assert "up to date" in capsys.readouterr().out

        target.write_text("hand-edited\n", encoding="utf-8")
        assert main(["--check"]) == 1
        assert "stale" in capsys.readouterr().out
        assert target.read_text(encoding="utf-8") == "hand-edited\n"

    def test_invalid_skill_exits_2(self, tmp_path, monkeypatch, capsys):
        skills_dir = make_skills(tmp_path)
        write_skill(skills_dir, "broken", "---\nname: broken\n---\n")
        template = tmp_path / "README.md"
        template.write_text("{{ skills_table }}\n", encoding="utf-8")
        target = tmp_path / "out.md"

        monkeypatch.setattr("update_docs.SKILLS_DIR", skills_dir)
        monkeypatch.setattr("update_docs.TEMPLATE_PATH", template)
        monkeypatch.setattr("update_docs.TARGET_PATH", target)
        monkeypatch.setattr("update_docs.REPO_ROOT", tmp_path)

        assert main([]) == 2
        assert "'description' is required" in capsys.readouterr().err
        assert not target.exists()
