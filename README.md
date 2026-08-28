# AI Agent Skills

A collection of reusable [agent skills](https://github.com/vercel-labs/skills) — portable `SKILL.md` instruction packages that extend what AI coding agents can do.

One repository, three consumption paths: the [skills.sh](https://skills.sh) package manager, the **ZCode** plugin marketplace, and the **Codex** plugin marketplace (Claude Code works too).

## Skills

| Name | Description |
| --- | --- |
| [`example`](skills/example/SKILL.md) | Template and conventions for skills in this repository. |

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
4. Add the skill to the table above.
