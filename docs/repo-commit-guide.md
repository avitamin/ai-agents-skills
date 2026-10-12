# Repo Commit Guide

Repository: `avitamin/ai-agents-skills` — a collection of agent skills
(`skills/<name>/SKILL.md`) bundled into one plugin for skills.sh, ZCode,
Claude Code, and Codex.

## Source Priority

1. The user's explicit instructions for the current commit.
2. This guide.
3. Repository docs (`README.md`, skill conventions in
   `skills/example/SKILL.md`).
4. The current branch and recent commit history.
5. The actual diff being committed.

When sources conflict, follow the higher-priority source and mention the
conflict to the user when it changes the outcome.

## Commit Message Format

Fact: history uses single-line imperative subjects with no issue key and
no trailing period; both Russian and English subjects exist.

Use:

```text
Глагол в императиве + конкретный предмет изменения
```

Examples:

```text
Добавить навык code-review (двухосевой ревью стандартов/спецификаций) и зарегистрировать его в README/манифестах
Добавить repo commit guide (формат коммитов, ветки, staging)
Влить критерии review-style в навык code-review и поднять версию плагина до 0.3.0
```

Conservative default: prefer Russian for the subject, matching the
latest commit; keep one line, under ~72 characters where practical; name
the affected skill when the change touches one.

## Issue Key Rules

Fact: no commit in history carries an issue key; no repository document
requires one.

Do not add an issue key unless the user explicitly provides one.

## Branch Policy

Fact: all commits live on `main` and are pushed to `origin/main`
(github.com/avitamin/ai-agents-skills); no feature branches exist.

Conservative default: commit directly to `main` for routine skill and
docs changes. Create a task-named branch only when the user asks for one.

## Staging Policy

Conservative default: review the diff first, then stage only the files
that belong to the task. Leave unrelated working-tree edits (for example
a user's local `.gitignore` tweak) unstaged. Never stage ignored paths
such as `.local/`.

## Validation Policy

Fact: `README.md` documents the skill-change checklist — verify discovery
with `npx skills add <repo> --list` (or against a local clone), bump
`version` in `.zcode-plugin/plugin.json`, `.claude-plugin/plugin.json`,
and `.codex-plugin/plugin.json` together, and update the skill table in
`README.md`.

Conservative default: before committing changes that touch `skills/`,
plugin manifests, or `README.md`, check that:

- each `SKILL.md` frontmatter parses and its `name` equals the folder
  name;
- the three plugin manifests are valid JSON and share the same version;
- files referenced from a skill (for example
  `skills/code-review/references/calibration.md`) exist.

No CI, tests, or lint are configured for this repository.

## Missing Facts And Defaults

- Fact: no `AGENTS.md`, `CONTRIBUTING.md`, or contribution guide exists
  in the repository; this guide is the only commit-policy document.
- Fact: no `.agents/git-commit-gate.json` is configured, so the
  deterministic git commit gate has nothing to enforce; if a gate config
  appears later, follow it.
- Conservative default: no AI attribution in commit messages
  (`Co-authored-by` for AI, `Generated with/by`, model or agent names) —
  per the user's global instructions.
- Question: none currently blocking commit preparation.
