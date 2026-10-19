<!-- GENERATED FILE — README.md is rendered from templates/README.md by scripts/update_docs.py. Edit the template, not README.md, then regenerate. -->

# AI Agent Skills

A collection of reusable [agent skills](https://github.com/vercel-labs/skills) — portable `SKILL.md` instruction packages that extend what AI coding agents can do.

One repository, three consumption paths: the [skills.sh](https://skills.sh) package manager, the **ZCode** plugin marketplace, and the **Codex** plugin marketplace (Claude Code works too).

## Skills

| Name | Description |
| --- | --- |
| [`ai-docs-review`](skills/ai-docs-review/SKILL.md) | Review AI-generated project documentation, PRDs, specifications, architecture and implementation plans through four independent review planes coordinated into one verified report. |
| [`code-review`](skills/code-review/SKILL.md) | Two-axis review of changes since a fixed point (commit, branch, tag, or merge-base): Standards (documented repo standards plus a fixed baseline of code smells, unjustified complexity, repository-convention breaks, and architectural risks) and Spec (does the code faithfully implement the originating issue, spec, or documentation?). |
| [`example`](skills/example/SKILL.md) | Template and conventions for skills in this repository. |
| [`plan-handoff`](skills/plan-handoff/SKILL.md) | Подготовь и сохрани подробный план реализации для новой сессии или другой модели, которой недоступна история переписки. |

## Install

### skills.sh (`npx skills`)

```bash
# interactive picker for this repo
npx skills add avitamin/ai-agents-skills

# one specific skill
npx skills add avitamin/ai-agents-skills --skill example

# install into a specific agent (codex, claude-code, cursor, opencode, ...)
npx skills add avitamin/ai-agents-skills -a codex

# user-global install instead of project-local
npx skills add avitamin/ai-agents-skills -g
```

### ZCode

1. Open **Settings → Plugin Management → Discover**.
2. Click **`+`** and add the GitHub repository `avitamin/ai-agents-skills`.
3. Find the **ai-agents-skills** plugin card and click **Get**.

Skills are then available as `ai-agents-skills:<name>` (for example `ai-agents-skills:example`).

### Codex

```bash
codex plugin marketplace add avitamin/ai-agents-skills
```

Then install the `ai-agents-skills` plugin from the marketplace in the Codex UI.

### Claude Code

```bash
claude plugin marketplace add avitamin/ai-agents-skills
claude plugin install ai-agents-skills@ai-agents-skills
```

## Repository layout

```
ai-agents-skills/
├── skills/<name>/SKILL.md             # the skills themselves — single source of truth
├── scripts/
│   └── update_docs.py                 # regenerates README.md from the template + skill frontmatter
├── templates/
│   └── README.md                      # README template — the editable source of README.md
├── .claude-plugin/
│   ├── marketplace.json               # marketplace catalog: ZCode + Claude Code (+ Codex legacy path)
│   └── plugin.json                    # plugin manifest: ZCode + Claude Code
├── .zcode-plugin/
│   └── plugin.json                    # plugin manifest: ZCode (preferred probe path)
├── .codex-plugin/
│   └── plugin.json                    # plugin manifest: Codex
└── .agents/
    └── plugins/marketplace.json       # marketplace catalog: Codex (native path)
```

The whole `skills/` folder is bundled into a single plugin (`ai-agents-skills`) whose root is the repository root, so no per-skill registration is needed anywhere: drop a folder with a `SKILL.md` under `skills/` and every consumer picks it up.

## Adding a skill

1. Create `skills/<skill-name>/SKILL.md`. See the [`example`](skills/example/SKILL.md) skill for required frontmatter and conventions (`name` must match the folder name).
2. Verify discovery: `npx skills add avitamin/ai-agents-skills --list` (or run it against a local clone).
3. Bump `version` in the three plugin manifests (`.zcode-plugin/plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`) so plugin managers detect the update.
4. Regenerate the skills table: `python scripts/update_docs.py`. `README.md` is a generated file — edit `templates/README.md` instead of `README.md`.
