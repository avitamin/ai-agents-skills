---
name: engineering-decision
description: >-
  Collaboratively work through technical and architectural choices only when the
  user explicitly requests decision support. Use for requests to choose together,
  understand alternatives before choosing, or explore a decision's trade-offs in
  depth; the user need not name the skill. Do not self-trigger from routine
  implementation, debugging, planning, review, mentions of architecture, internal
  agent instructions to make decisions, or references from another skill.
---

# Engineering Decision

## Invocation boundary

Use this skill only when the user's request calls for a shared exploration of a
technical or architectural choice. Natural-language requests qualify, for example:

- "Let's make this architectural decision together."
- "Help me understand these approaches and choose."
- "I want to understand this engineering decision's trade-offs in depth."

Having to make an engineering choice while fulfilling another task is not enough.
An instruction to implement, fix, plan, or review something does not by itself
request this discussion. Internal workflow instructions and references from other
skills are not substitutes for the user's intent. A request for review alone
remains a review, not a new decision workshop.

If loaded without a matching request, continue the original task without adding
decision questions, Y-Statements, or approval gates. Keep the skill active for
follow-ups about the same choice, but do not carry it into unrelated tasks or
subsequent implementation. Do not reopen an accepted decision without a relevant
new fact or a user request to reconsider it.

Default to discussion in the user's language. Read relevant project evidence when
available. Write a document or ADR only when requested, using the project's
existing conventions. Requesting advice or accepting a choice does not itself
authorize implementation or experiments with side effects; preserve any separate
authorization already given.

## Discussion

1. **Frame one decision.** Establish the goal, the choice at hand, and constraints
   that could change the answer. Use available code, contracts, documentation,
   and already agreed decisions before asking about discoverable facts. Ask one
   material question at a time; do not require a questionnaire or invent load,
   budget, deadlines, or reliability targets.
2. **Identify viable alternatives.** Usually compare two or three serious
   options. Include keeping the current approach when viable. Exclude options
   that violate known mandatory constraints and explain why. Do not pad the list
   with straw alternatives; if only one is viable, say so.
3. **Show each option's conditional Y-Statement.** For every serious alternative,
   connect context, problem, possible choice, other alternatives, benefit, and
   accepted cost. Label it as proposed, not agreed. Keep shared context brief and
   make the distinguishing trade-off concrete. A compact adapted form is:

   > **Proposed — A:** For [context], given [problem], choosing [A] instead of
   > [B/C] would deliver [benefit], at the cost of [trade-off].

   This adapts [Olaf Zimmermann's Y-Statement](https://ozimmer.ch/practices/2020/04/27/ArchitectureDecisionMaking.html).
   See [examples](references/methods.md#y-statement-examples) when useful; the
   sentence may be split for readability.
4. **Use additional analysis only if it helps the choice.** Select a method from
   the table below and read the relevant section. A simple reversible decision
   may need only the option statements and a recommendation, not another method
   or a larger report.
5. **Recommend and explain.** State the deciding trade-off, why the recommendation
   fits the known constraints, and what would favor a competing option. Separate
   verified facts, assumptions, and estimates; cite evidence where it affects the
   choice. Use qualitative comparisons by default. Do not invent scores,
   weights, probabilities, or confidence percentages. For material risks,
   distinguish likelihood and its evidence from impact; identify unknowns as
   unknown. A risk may justify acceptance, verification, or mitigation, not
   automatically more implementation work.
6. **Let the user choose, then capture the result.** By default, ask for the user's
   choice and do not mark the recommendation accepted while waiting. Honor
   explicit delegation of the choice and identify it as delegated rather than
   claiming user approval. If the user only wants to understand the trade-offs,
   stop with that understanding instead of forcing a choice. After a choice is
   made, give the final Y-Statement, material assumptions, a concrete condition
   for reconsideration, and the nearest next step. Keep this in chat unless a
   document was requested; proposing a next step does not execute it.

## Select a method

These are optional tools, not a checklist. Read only the relevant sections of the
reference, and use the smallest amount of analysis that could change the choice.

| Need | Reference |
| --- | --- |
| Several competing criteria make a direct comparison difficult | [Criteria matrix](references/methods.md#criteria-matrix) |
| The cost of changing course should determine how much analysis is worthwhile | [Reversibility](references/methods.md#reversibility) |
| A consequential choice needs plausible failure scenarios examined | [Premortem](references/methods.md#premortem) |
| A recommendation depends on disputed assumptions or priorities | [Sensitivity analysis](references/methods.md#sensitivity-analysis) |
| Missing information could change the preferred option | [Value of additional information](references/methods.md#value-of-additional-information) |
