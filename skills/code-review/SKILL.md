---
name: code-review
description: "Two-axis review of changes since a fixed point (commit, branch, tag, or merge-base): Standards (documented repo standards plus a fixed baseline of code smells, unjustified complexity, repository-convention breaks, and architectural risks) and Spec (does the code faithfully implement the originating issue, spec, or documentation?). Runs both axes as parallel sub-agents and reports them side by side with inline code comments; also runs criteria-only to augment a host's native /review. Use when the user wants to review a branch, a PR, a diff, work-in-progress changes, work done by another agent, or asks to \"review since X\" — even a bare \"review this\"."
---

# Code Review

Two-axis review of the diff between `HEAD` and a fixed point the user
supplies:

- **Standards**: does the code conform to this repo's documented coding
  standards and to the review baseline below — code smells, unjustified
  complexity, repository-convention breaks, architectural risks?
- **Spec**: does the code faithfully implement the originating issue,
  spec, or documentation?

Both axes run as **parallel sub-agents** — two sub-agent tool calls in a
single message — so they don't pollute each other's context. This skill
then aggregates their findings and attaches the line-anchored ones inline
as code comments.

## Invocation modes

- **Full workflow** (default): the skill is invoked directly — a branch,
  a PR, a diff, "review since X". Run the process below end to end.
- **Criteria-only**: a host client's native review (for example `/review`
  in OpenCode or Codex) loads this skill for extra criteria. Apply the
  criteria from steps 2–3 to whatever the host review selected; inherit
  its scope, report format, and priority scale. Do not launch sub-agents,
  do not extend the host's report schema with extra fields or sections,
  and do not let non-blocking style or documentation findings change an
  overall verdict. An open question is not a finding.

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
4. User-facing documentation the change touches (`README`, `docs/`, CLI
   help) — it is a contract too; see the docs-contract check below.
5. If nothing is found, ask the user where the spec is. If they say there
   isn't one, the **Spec** sub-agent is skipped and the final report says
   "no spec available".

**Docs-contract check.** Wherever the diff touches documented behaviour,
compare both directions: inputs, defaults, outputs, errors, side effects,
examples, migrations, operational constraints. Code and tests show actual
behaviour but can jointly violate a documented requirement — don't
declare the documentation stale by default; tie both sides together and
show whom the divergence misleads. Where documentation is missing, name
the knowledge a consumer or maintainer actually needs and the project's
usual place for it; don't demand describing obvious internal details or
a standard set of files.

### 3. Identify the standards sources

Anything in the repo that documents how code should be written, such as
`CODING_STANDARDS.md`, `CONTRIBUTING.md`, lint configs, or the coding
conventions in `AGENTS.md` / `CLAUDE.md`.

On top of whatever the repo documents, the Standards axis always carries
the **review baseline** below: it applies even when a repo documents
nothing. Three rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it
  endorses something the baseline would flag, suppress the finding.
- **A smell or risk is a prompt, not a verdict.** Baseline findings are
  judgement calls ("possible Feature Envy"), never hard violations. Name
  the concrete structural consequence — a rule multiplied across places,
  a hidden obligation, an extra dependency, several reasons to change one
  module. A failing test is not required, and the label alone is not a
  justification.
- **Skip what tooling enforces.** Lint, typecheck, and test output
  already cover it; don't restate those violations.

#### Smell baseline

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: functions, variables, or classes whose names don't reveal their intent → rename to say what it does, or delete if it's redundant.
- **Long Function**: a function packs steps that change for different reasons or mixes abstraction levels → extract functions along the seams; split by responsibility, not a line limit.
- **Large Class**: a class accumulates fields and methods serving unrelated responsibilities → split it so each part changes for one reason.
- **Duplicated Code**: identical or near-identical logic in multiple places → extract a shared function/module; prefer a bit of duplication *now* over a wrong abstraction (rule of three).
- **Shotgun Surgery**: one conceptual change requires edits scattered across many files → move fields & functions so one change stays in one place.
- **Divergent Change**: one module changes for many unrelated reasons → split it (mixins, delegation, separate modules).
- **Feature Envy**: a method that uses another object's data more than its own → move the method to the object it envies.
- **Inappropriate Intimacy**: a class reaches into another's internals, computing its invariants for it → move the behaviour or expose a narrower interface.
- **Message Chains**: `a.b().c().d()` — the caller knows the whole navigation path → hide the chain behind a method (`a.lastD()`).
- **Middle Man**: a class whose methods just forward to another class → remove it and let callers use the delegate directly.
- **Lazy Element**: a function, class, or constant too small to justify its own existence → inline it — unless the name carries meaning a call site can't.
- **Data Clumps**: the same group of fields/params (e.g. `city, street, zip`) passed around together → bundle them into an object.
- **Primitive Obsession**: domain concepts (money, coordinates, email) modelled as bare primitives → introduce a value object.
- **Long Parameter List**: a long run of parameters callers must keep synchronized and in order → bundle the values that travel together.
- **Repeated Switches**: the same conditional dispatch repeated in multiple places → replace with polymorphism.
- **Parallel Inheritance Hierarchies**: adding one variant forces synchronized subclass additions in two hierarchies → connect or merge them so one change stays in one place.
- **Speculative Generality**: abstractions/hooks with only one real caller ("we might need it") → inline them; add the abstraction when the second case arrives.
- **Mutable Data**: state whose owner and required write order are hidden → narrow the mutation surface and make ownership explicit.
- **Global Data**: state anyone can write and everyone must guess about → give it an owner and route writes through it.
- **Refused Bequest**: a subclass that ignores/overrides most of its parent's behaviour → replace inheritance with composition or a sibling.

Counterweights — don't flag these: a single implementation doesn't prove
an abstraction redundant (a boundary may isolate a dependency or
translate its errors); a separate type isn't needed for every bare string
or number; syntactically similar code serving independent rules doesn't
need merging.

#### Unjustified complexity

Judge the artifact, not the presumed author — style alone cannot show
whether code was machine-written, and every finding must name a concrete
defect. Look for:

- redirection chains with no responsibility of their own, unused options,
  extension points added "for the future", and homemade analogues of
  mechanisms the language or framework already provides;
- defensive checks inside a guaranteed contract that mask its violation —
  distinct from justified validation of external input at a boundary;
- broad catches, fake success, and fallbacks that lose the error, the
  data, or observability;
- assumed APIs and parameters, stubs and unfinished paths standing in for
  declared behaviour — check them against the available contracts;
- comments that restate the operations, boilerplate descriptions, and
  reliability promises with no mechanism behind them;
- tests that assert their own mock or only the happy path instead of the
  declared invariant or failure handling.

Allow justified adapters, compatibility shims, and generated or vendored
code; if the generator is in scope, look there for the cause. Don't
demand refactoring for brevity alone.

#### Repository conventions

Distinguish an explicit rule or an established module pattern from a
single old example. Account for local differences, migrations, and
explained exceptions. Don't propose copying a bug for the sake of
consistency, and don't pass a personal preference off as a standard.

Give special attention to: a second error-handling mechanism, a bypass of
a shared contract, duplicated infrastructure, and an unusual dependency
direction.

#### Architectural risks and justification gaps

Look for new long-term obligations: a dependency, a module boundary, a
public contract, a data owner, a source of truth, storage, a cache,
asynchrony, global state. Check for cycles, leaking internals, several
owners of one invariant, partial execution, compatibility breaks, and
hidden ordering. A risk needs a concrete mechanism — abstract
"scalability" without conditions is not enough.

Separately check the explanation of significant choices: constraint,
motive, trade-off, and boundary of application — wherever the project
keeps such records (design note, ADR, change description, comment).
Don't invent the author's motive. A missing ADR is not a defect by
itself. A justification gap matters only when, without that specific
knowledge, the next maintainer could break the contract or change the
mechanism wrongly — then name the missing knowledge and the minimal
fitting place to record it. An explained choice closes the motive
question but doesn't cancel a proven technical risk.

### 4. Launch both sub-agents in parallel

Sub-agents start with a fresh context — nothing from this conversation is
visible to them — so every prompt must be fully self-contained. Send
**two sub-agent tool calls (`general-purpose`) in a single message** —
`Agent` in ZCode, `Task` in Claude Code, `subagent` in OpenCode — so they
run concurrently. Shape each prompt along the task-input structure coding
agents follow best — Goal / Context / Constraints / Done when — for
example:

```text
Goal: review the diff in <absolute working dir> along ONE axis only: <axis>.
Context: run `git diff <fixed-point>...HEAD` yourself; commits:
  <oneline list>; sources: <standards files / review baseline / spec text>.
Constraints: cite file:line for every finding; <axis-specific rules>.
Done when: a report under 400 words covering (a) ..., (b) ..., (c) ...
```

**Standards sub-agent prompt** should include:

- The working directory, the full diff command, and the commit list.
- The standards-source files found in step 3 (their paths, or contents if
  short), **plus the smell baseline, the counterweights, and the three
  criteria checklists (unjustified complexity, repository conventions,
  architectural risks) from step 3 pasted in full** — the sub-agent has no
  other access to them.
- The brief: "Report, per file/hunk where relevant: (a) every place the
  diff violates a documented standard: cite the standard (file + the
  rule); (b) any baseline smell you spot: name it and quote the hunk;
  (c) unjustified complexity, convention breaks, and architectural risks
  per the checklists. Distinguish hard violations from judgement calls:
  documented-standard breaches can be hard, but baseline findings are
  always judgement calls, and a documented repo standard overrides the
  baseline. Every finding needs a concrete mechanism or structural
  consequence, not just a label. Skip anything tooling enforces. Cite
  `file:line` for every finding. Under 400 words."

**Spec sub-agent prompt** should include:

- The working directory, the diff command, and the commit list.
- The path or fetched contents of the spec, plus the docs-contract check
  from step 2 and the relevant documentation contents.
- The brief: "Report: (a) requirements the spec asked for that are missing
  or partial; (b) behaviour in the diff that wasn't asked for (scope
  creep); (c) requirements that look implemented but where the
  implementation looks wrong; (d) divergences between documentation and
  implementation, in both directions. Quote the spec line and cite
  `file:line` for each finding. Under 400 words."

If the spec is missing, skip the Spec sub-agent and note this in the
final report.

### 5. Aggregate

Present the two reports under `## Standards` and `## Spec` headings,
verbatim or lightly cleaned. Do **not** merge or rerank findings, because
the two axes are deliberately separate (see _Why two axes_).

Before publishing, filter findings against the counterexamples in
[`references/calibration.md`](references/calibration.md): a justified
adapter, an explained decision, or mere similarity must not survive as a
finding.

Then attach every finding that has a `file:line` anchor inline with the
client's inline-review mechanism, one comment per finding, so the review
shows up at the code itself, like a PR review. In ZCode that is a
`::code-comment` directive:

```text
::code-comment{title="[Standards][P2] Feature Envy" body="getTotal() uses Cart's data more than its own; move it onto Cart." file="C:/repo/src/order.ts" start=42 end=48 priority=2}
```

Tag the axis in the title (`[Standards]` / `[Spec]`) and map severity to
priority: 0 critical (broken build, spec requirement outright violated),
1 major, 2 minor, 3 nit. Maintainability, documentation, and
justification-gap findings default to priority 2–3 and don't block.
Findings without a concrete anchor stay in the report only. An open
question is not a finding — surface real uncertainty only where the
format allows it.

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

Adapted from Matt Pocock's
[code-review skill](https://github.com/mattpocock/skills/tree/main/skills/engineering/code-review);
the smell baseline and both sub-agent briefs are kept from the original.
The complexity, conventions, architecture, and docs-contract criteria are
merged in from the `review-style` skill.
