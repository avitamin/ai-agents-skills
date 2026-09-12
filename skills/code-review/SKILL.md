---
name: code-review
description: "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards and a fixed code-smell baseline?) and Spec (does the code faithfully implement the originating issue or spec?). Runs both reviews as parallel sub-agents, reports them side by side, and attaches findings inline as code comments. Use when the user wants to review a branch, a PR, a diff, work-in-progress changes, work done by another agent, or asks to \"review since X\" — even a bare \"review this\"."
---

# Code Review

Two-axis review of the diff between `HEAD` and a fixed point the user
supplies:

- **Standards**: does the code conform to this repo's documented coding
  standards?
- **Spec**: does the code faithfully implement the originating issue / spec?

Both axes run as **parallel sub-agents** — two `Agent` tool calls in a
single message — so they don't pollute each other's context. This skill
then aggregates their findings and attaches the line-anchored ones inline
as code comments.

## Process

### 1. Pin the fixed point

Whatever the user said is the fixed point (a commit SHA, branch name, tag,
`main`, `HEAD~5`, etc.). If they didn't specify one, ask for it.

Capture the diff command once: `git diff <fixed-point>...HEAD` (three-dot,
so the comparison is against the merge-base). Also note the list of
commits via `git log <fixed-point>..HEAD --oneline`.

Before going further, confirm the fixed point resolves
(`git rev-parse --verify <fixed-point>^{Commit}`) and the diff is
non-empty. A bad ref or an empty diff should fail here, not inside two
parallel sub-agents: report the problem and ask for the correct fixed
point.

### 2. Identify the spec source

Look for the originating spec, in this order:

1. Issue references in the commit messages (`#123`, `Closes #45`, GitLab
   `!67`, etc.). If the repo has a GitHub remote, fetch the text with
   `gh issue view <number>` (or `gh pr view <number>`). Without a GitHub
   remote or a working `gh`, treat the reference as a lead and keep going
   down the list.
2. A path the user passed as an argument.
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch
   name or feature.
4. If nothing is found, ask the user where the spec is. If they say there
   isn't one, the **Spec** sub-agent is skipped and the final report says
   "no spec available".

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as
`CODING_STANDARDS.md`, `CONTRIBUTING.md`, lint configs, or the coding
conventions in `AGENTS.md` / `CLAUDE.md`.

On top of whatever the repo documents, the Standards axis always carries
the **smell baseline** below: a fixed set of Fowler code smells
(_Refactoring_, ch. 3) that applies even when a repo documents nothing.
Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it
  endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic
  ("possible Feature Envy"), never a hard violation. As with any standard
  here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: functions, variables, or classes whose names don't reveal their intent → rename to say what it does, or delete if it's redundant.
- **Duplicated Code**: identical or near-identical logic in multiple places → extract a shared function/module; prefer a bit of duplication *now* over a wrong abstraction (rule of three).
- **Feature Envy**: a method that uses another object's data more than its own → move the method to the object it envies.
- **Data Clumps**: the same group of fields/params (e.g. `city, street, zip`) passed around together → bundle them into an object.
- **Primitive Obsession**: domain concepts (money, coordinates, email) modelled as bare primitives → introduce a value object.
- **Repeated Switches**: the same conditional dispatch repeated in multiple places → replace with polymorphism.
- **Shotgun Surgery**: one conceptual change requires edits scattered across many files → move fields & functions so one change stays in one place.
- **Divergent Change**: one module changes for many unrelated reasons → split it (mixins, delegation, separate modules).
- **Speculative Generality**: abstractions/hooks with only one real caller ("we might need it") → inline them; add the abstraction when the second case arrives.
- **Message Chains**: `a.b().c().d()` — the caller knows the whole navigation path → hide the chain behind a method (`a.lastD()`).
- **Middle Man**: a class whose methods just forward to another class → remove it and let callers use the delegate directly.
- **Refused Bequest**: a subclass that ignores/overrides most of its parent's behaviour → replace inheritance with composition or a sibling.

### 4. Launch both sub-agents in parallel

ZCode sub-agents start with a fresh context — nothing from this
conversation is visible to them — so every prompt must be fully
self-contained. Send **two `Agent` tool calls (`general-purpose`) in a
single message** so they run concurrently. Shape each prompt along the
task-input structure Z.ai recommends for coding agents — Goal / Context /
Constraints / Done when — for example:

```text
Goal: review the diff in <absolute working dir> along ONE axis only: <axis>.
Context: run `git diff <fixed-point>...HEAD` yourself; commits:
  <oneline list>; sources: <standards files / smell baseline / spec text>.
Constraints: cite file:line for every finding; <axis-specific rules>.
Done when: a report under 400 words covering (a) ..., (b) ..., (c) ...
```

**Standards sub-agent prompt** should include:

- The working directory, the full diff command, and the commit list.
- The standards-source files found in step 3 (their paths, or contents if
  short), **plus the smell baseline from step 3 pasted in full** — the
  sub-agent has no other access to it.
- The brief: "Report, per file/hunk where relevant, (a) every place the
  diff violates a documented standard: cite the standard (file + the
  rule); and (b) any baseline smell you spot: name it and quote the hunk.
  Distinguish hard violations from judgement calls: documented-standard
  breaches can be hard, but baseline smells are always judgement calls,
  and a documented repo standard overrides the baseline. Skip anything
  tooling enforces. Cite `file:line` for every finding. Under 400 words."

**Spec sub-agent prompt** should include:

- The working directory, the diff command, and the commit list.
- The path or fetched contents of the spec.
- The brief: "Report: (a) requirements the spec asked for that are missing
  or partial; (b) behaviour in the diff that wasn't asked for (scope
  creep); (c) requirements that look implemented but where the
  implementation looks wrong. Quote the spec line and cite `file:line`
  for each finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the
final report.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings,
verbatim or lightly cleaned. Do **not** merge or rerank findings, because
the two axes are deliberately separate (see _Why two axes_).

Then attach every finding that has a `file:line` anchor inline with one
`::code-comment` directive per finding, so the review shows up at the
code itself, like a PR review:

```text
::code-comment{title="[Standards][P2] Feature Envy" body="getTotal() uses Cart's data more than its own; move it onto Cart." file="C:/repo/src/order.ts" start=42 end=48 priority=2}
```

Tag the axis in the title (`[Standards]` / `[Spec]`) and map severity to
priority: 0 critical (broken build, spec requirement outright violated),
1 major, 2 minor, 3 nit. Findings without a concrete anchor stay in the
report only.

End with a one-line summary: total findings per axis, and the worst issue
*within each axis* (if any). Don't pick a single winner across axes —
that is the reranking the separation exists to prevent.

## Why two axes

A change can pass one axis and fail the other:

- Code that follows every standard but implements the wrong thing →
  **Standards pass, Spec fail.**
- Code that does exactly what the issue asked but breaks the project's
  conventions → **Spec pass, Standards fail.**

Reporting them separately stops one axis from masking the other.

---

Adapted for ZCode from Matt Pocock's
[code-review skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/code-review);
the smell baseline and both sub-agent briefs are kept from the original.
