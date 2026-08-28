---
name: example
description: Template and conventions for skills in this repository. Use when creating a new skill, checking skill structure rules, or deciding how a skill is picked up by skills.sh, ZCode, and Codex.
---

# Example Skill

This skill is a living template. Copy its folder to create a new skill, then edit
the frontmatter and body.

## Anatomy of a skill

A skill is a folder under `skills/` containing a `SKILL.md` file:

```
skills/<skill-name>/
├── SKILL.md        # required: YAML frontmatter + instructions
└── ...             # optional: scripts, references, templates
```

## Frontmatter rules

Required fields:

```yaml
---
name: example               # lowercase, hyphens allowed; MUST equal the folder name
description: One or two sentences telling the agent what this skill does and when to use it.
---
```

Optional fields:

```yaml
argument-hint: "[topic]"            # hint shown for slash-command style invocation
disable-model-invocation: true      # hide from automatic triggering; manual /invoke only
metadata:
  internal: true                    # hide from skills.sh listings (work-in-progress skills)
```

The `description` is the most important field: agents use it to decide when to load
the skill. Say what the skill does **and** when to use it; include trigger keywords.

## Writing the body

- Lead with the goal, then the steps. Keep instructions imperative and concrete.
- Prefer checklists and short examples over long prose.
- Reference bundled files by relative path (`scripts/run.py`, `references/api.md`)
  so the skill works from any install location.
- Cover edge cases and failure modes at the end — what to check when something
  doesn't work.

## How skills in this repo are consumed

The same `skills/` folder is served three ways (no per-skill registration needed):

- **skills.sh**: `npx skills add avitamin/ai-agents-skills` discovers every
  `skills/<name>/SKILL.md`.
- **ZCode**: the plugin marketplace entry in `.claude-plugin/marketplace.json`
  bundles the whole `skills/` folder into one plugin; skills appear as
  `ai-agents-skills:<name>`.
- **Codex**: the marketplace in `.agents/plugins/marketplace.json` exposes the
  same plugin via `codex plugin marketplace add avitamin/ai-agents-skills`.

## Adding a new skill

1. Create `skills/<skill-name>/SKILL.md` (copy this folder as a starting point).
2. Fill in `name` (must match the folder name) and a trigger-rich `description`.
3. Test locally: `npx skills add /path/to/ai-agents-skills --list` should show it.
4. Bump `version` in `.zcode-plugin/plugin.json`, `.claude-plugin/plugin.json`,
   and `.codex-plugin/plugin.json` so plugin managers detect the update.
5. Add the skill to the table in the repository `README.md`.
