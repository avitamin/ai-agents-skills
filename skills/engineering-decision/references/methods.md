# Decision methods

Use the section that addresses the current decision. These methods support
judgment; completing them all is not a condition for choosing.

## Criteria matrix

Use when alternatives win on different requirements and a short comparison needs
more structure.

1. Separate mandatory constraints from preferences. Exclude a confirmed violation
   of a mandatory constraint before ranking; a high score elsewhere cannot
   compensate for it. Mark an unverified constraint as unknown, not satisfied.
2. Choose criteria that could distinguish the options, such as delivery effort,
   operational cost, compatibility, or a stated reliability requirement. Establish
   disputed priorities with the user rather than silently assigning weights.
3. Compare the alternatives with evidence and concrete descriptions. Use a small
   table when it helps. Record missing evidence instead of filling every cell with
   invented ratings.
4. If quantified comparison is useful and supported, define scales and explain
   the origin of weights and estimates. Check sensitivity before treating a small
   difference in totals as decisive.

Output the deciding criteria and trade-off, not just a winning total. A matrix
cannot establish requirements or preferences on the user's behalf.

Basis: [NASA Systems Engineering Handbook, Decision Analysis, sections
6.8.1.2.1–6.8.1.2.5](https://www.nasa.gov/reference/6-8-decision-analysis/).

## Reversibility

Use to match the depth of analysis to the cost of changing direction.

- Identify what would have to change: local code, public contracts, stored data,
  infrastructure, external commitments, or users' behavior.
- Distinguish reverting code from recovering consequences. A redeployable service
  can still have emitted irreversible events or transformed data.
- Describe the known effort, disruption, and dependencies of changing course;
  avoid an unsupported numeric estimate or a bare "reversible" label.
- For an inexpensive change, prefer a bounded choice and a relevant revisit
  condition. For a costly change, examine the material assumptions before committing.

Output the practical cost of changing course and how it affects today's analysis.
Do not require a prototype or a formal rollback plan for every decision.

Basis: the distinction between reversible and irreversible decisions in
[Amazon's 2016 shareholder letter](https://www.aboutamazon.com/news/company-news/2016-letter-to-shareholders).
The software examples above are adaptations.

## Premortem

Use when a consequential option warrants examining plausible failure scenarios.

Imagine that the proposed choice has failed. Describe a few credible causes in
this project's context, each as a condition, failure mechanism, and consequence.
Separate evidence for likelihood from severity; leave likelihood unknown when the
available evidence does not establish it.

For each material scenario, explain what it changes about the choice. The user
may accept the risk, obtain evidence, narrow the choice, or mitigate it. Include
the cost of mitigation; do not turn every imagined failure into required work or
present a hypothetical outcome as an observed defect.

Output only the scenarios that materially affect the choice and their implications.
Use plausible project conditions, not an exhaustive disaster catalogue.

Basis: Gary Klein, [Performing a Project Premortem](https://hbr.org/2007/09/performing-a-project-premortem).
The evidence and action guidance above adapts the technique for engineering choices.

## Sensitivity analysis

Use when a recommendation may depend on an uncertain fact, estimate, or priority.

- Identify the assumption most likely to change the recommendation.
- Compare plausible alternatives to that assumption, grounded in supplied
  constraints or explicitly labelled scenarios. Do not invent a range and call it
  measured data.
- State whether the preferred option changes. Explain the boundary if known;
  otherwise identify what evidence would locate it.
- If small plausible changes reverse the ranking, present the choice as fragile
  and show what information or user preference would resolve it.

For example, a delivery-first recommendation may change if independent releases
become a mandatory requirement. Without workload data, do not invent a throughput
threshold at which an architectural style supposedly becomes necessary.

Basis: [NASA Decision Analysis, uncertainty and robustness of rankings, sections
6.8.1.2.4–6.8.1.2.5](https://www.nasa.gov/reference/6-8-decision-analysis/).

## Value of additional information

Use when a missing fact could change which option is preferable.

1. Name the unknown and explain how different answers would affect the choice.
2. Inspect existing evidence first: a contract, relevant source, documentation,
   or available measurements may answer it without new experimentation.
3. If a new check is needed, propose the smallest one that separates the options.
   State its expected cost or time only when grounded; otherwise ask for a useful
   limit. Define what result would support each option and when to stop checking.
4. Compare the likely usefulness of the information with the cost of obtaining it
   and delaying the decision. A qualitative judgment is sufficient when
   probabilities and costs cannot be defended.

If the information would not change the choice, do not require the check as a
prerequisite. If uncertainty remains decisive, say so and offer a conditional
recommendation or a deferred choice. Do not claim a proposed check was run, and
do not execute side-effectful experiments without authorization for that work.

Basis: [NASA Decision Analysis, section 6.8.1.2.4](https://www.nasa.gov/reference/6-8-decision-analysis/).

## Y-Statement examples

These are fictional, conditional examples, not general recommendations. They
adapt the six elements of [Y-Statements by Olaf
Zimmermann](https://ozimmer.ch/practices/2020/04/27/ArchitectureDecisionMaking.html):
context, concern, chosen option, alternatives, benefit, and accepted downside.

**Given:** A team is adding report generation to its existing application. The
user has stated that delayed completion is acceptable, users can retrieve reports
later, and their current queue workers are available. Operational independence is
a preference, not a mandatory requirement.

**Proposed — A:** For report generation in the existing application, given that
work may finish after the request, choosing its existing queue workers instead
of a separate reporting service would reuse the team's operating model, at the
cost of sharing deployment and worker capacity with the application.

**Proposed — B:** For the same report workflow, choosing a separate reporting
service instead of the application's workers would allow independent releases
and capacity management, at the cost of another deployment and a service contract
to operate and maintain.

Neither option is accepted yet. A recommendation can favor A under the stated
priorities while explaining when B would become preferable.

**Only after the user selects A:** For report generation in the existing
application, given that work may finish after the request, we chose existing
queue workers over a separate reporting service to reuse the operating model,
accepting shared deployment and worker capacity.

- **Choice source:** the user selected A. If the choice was delegated, say that
  instead; do not fabricate this confirmation.
- **Material assumption:** delayed completion remains acceptable and the existing
  worker infrastructure can support the workflow; available workers alone do not
  prove sufficient capacity.
- **Revisit when:** independent releases become a requirement, or observed resource
  contention cannot be addressed within the agreed operating constraints.
- **Next step:** verify the report workload against available worker capacity.
  This is a proposed check, not a reported result or permission to implement.
