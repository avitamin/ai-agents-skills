# Calibrating findings

The examples are hypothetical; their paths and facts do not refer to the
project under review. Use the reasoning pattern, not the findings
themselves — don't carry these findings into a real report.

## Duplicating one rule

Material: preview and apply independently compute whether one operation is
allowed. Apply gained a rejection for `locked`, while preview still offers
the action.

Useful finding: "`preview` keeps the old check, so for `locked` it offers
an action that `apply` rejects. Update both paths; the permissibility rule
belongs in a shared source so they can't diverge again."

Not enough: "This is Duplicated Code, a DRY violation."

Counterexample: two identical transformations serve independent contracts
of different formats. Their future changes differ; a shared helper could
tighten the coupling.

## An extra abstraction with no behaviour bug

Material: for a closed set of one operation, a registry, a factory, and a
strategy were added; calls run sequentially through all three, with no
choice of implementation. The project provides no plugin API, no extra
lifecycle management, and no external consumers; no extensibility
rationale exists.

A maintenance risk is fitting: understanding a single call requires
walking three redirections with no responsibility of their own. Suggest a
direct call, or keeping only the boundary that is really needed. Don't
call it a runtime bug.

Counterexample: an interface isolates an external dependency, and an
adapter translates its errors into the module's contract. A single
implementation doesn't make them redundant.

## A fallback that hides a failure

Material: a loader catches every failure and returns an empty collection.
The consumer treats it as the full current set and deletes absent local
records.

A useful finding links the catch to the consumer: source unavailability
becomes an empty authoritative result and triggers deletion. Need a
separate error result, or last-known-state retention, per the contract.

Counterexample: the contract for optional hints allows an empty response,
and the failure is logged and doesn't affect the main data. The catch
itself is not a problem.

## A check at the boundary and inside a contract

Material: a parser already returns a valid non-empty identifier or an
error. A new internal consumer substitutes an impossible empty identifier
with `default`, hiding a contract violation.

The finding describes the meaning substitution and the lost diagnostics;
it doesn't claim that all null-guarding is harmful. Validating unchecked
external input remains justified.

## Documentation vs implementation

Material: the manual promises a dry-run with no writes. A new branch saves
the result before checking the dry-run flag; the manual's example now
mutates data.

The finding references both sides and shows the side effect. First
establish whether the dry-run requirement still stands. Updating the
documentation does not fix a violation of a live contract.

Counterexample: an internal variable was renamed; external behaviour is
unchanged. There is no ground to demand a README change.

## Local style

Material: the guide requires a typed error at the module boundary;
neighbouring implementations comply. A new path returns a string the
shared handler doesn't recognise.

The finding names the rule, the new path, and the consequence for the
handler. If one root cause produces both a behaviour bug and a style
violation, one finding is enough.

Counterexample: the reviewer prefers guard clauses while the module
consistently uses short if/else with no complexity. That is a preference,
not a finding.

## An unexplained architectural decision

Material: a second persisted source of the same state appeared. Nothing
indicates the authoritative owner, synchronisation, or conflict
resolution.

If a divergence path is visible, report the technical risk along that
path. If the code is consistent but the long-term commitment is
unexplained, call out the gap separately: a future maintainer doesn't know
which source may change the state. Name the owner, the reason for the
second representation, and its boundary — a formal ADR is not required.

Counterexample: a design note already explains that the second
representation is a fully rebuildable cache with a named owner. The
absence of an `ADR-001.md` file proves nothing.

Explained decision with a defect: a design note justifies a second store
for offline reads, but the update path commits to the primary store before
writing to the second. If the second write fails, offline readers retain
the old state with no retry or reconciliation mechanism. Keep the finding
about this concrete divergence path; omit the claim that the second store
has no rationale. An explanation does not resolve the defect.

## Incomplete context

Material: a wrapper's signature is visible, but the external contract that
might require the transformation is not.

Don't declare the wrapper unnecessary. Check the consumers available to
you. If the contract remains unknown and the question matters, name
exactly the missing guarantee. Continue reviewing the rest of the changes
without requesting access to the whole environment.
