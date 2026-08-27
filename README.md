# PRD Generation Assistant

A two step CLI that turns a rough feature idea into a structured PRD: first checks for genuinely
blocking gaps (target user, success metric, scope boundary) and asks up to 3 clarifying
questions only if real gaps exist, then drafts the PRD, explicitly flagging every assumption it
had to make instead of silently inventing scope.

Runs entirely on a local [Ollama](https://ollama.com) model (`llama3.2`). No API key, no
billing. See the parent [CLAUDE.md](../CLAUDE.md) for the broader portfolio initiative.

## Overview

This project turns "just ask an AI to write a PRD" into something closer to what a PM actually
needs: a tool that knows what a PRD requires to be complete, and says so before it starts
drafting.

**The problem it solves.** Anyone can prompt an LLM into producing a confident looking PRD. The
failure mode is that it fills gaps silently, so the output reads as complete even when it is
built on invented assumptions about the user, the success metric, or the scope. The actual PM
skill is knowing what a PRD cannot be missing, and building that judgment into the tool rather
than trusting the model to know.

**How it works, step by step.**

1. We wrote the prompt templates as separate files (`prd_gen/prompts/gap_check.md`,
   `draft.md`), not inline strings, since the PRD structure and the gap check judgment are the
   actual product decisions here, not implementation detail.
2. We built a gap check step that runs before any drafting: it checks the idea against three
   things a PRD cannot function without (who it is for, how we would know it worked, what is in
   versus out of scope) and only asks a question when a gap is genuinely blocking, capped at 3.
3. We found a real bug while testing this: the first version asked the model for a bare
   `{sufficient, questions}` verdict, and it turned out the model said "sufficient" for every
   input we tried, including a deliberately vague one line idea. It was not reasoning about the
   gaps at all, just defaulting to the easy answer.
4. We fixed it by forcing the model to write one sentence of reasoning per category before
   committing to a verdict, and confirmed the fix actually worked by rerunning the same vague
   input and watching it correctly ask three real questions instead of zero.
5. We built the draft step with a PRD structure we designed on purpose rather than copying a
   generic template, later expanded with a published field framework. See the next two points.
6. We read a published AI PRD framework and used it to expand the structure well past a basic
   Problem/Goals/Requirements shape: Opportunity Framing
   (Problem, Working Hypothesis, Strategy Fit as three separate one line answers, not one vague
   paragraph), a Behavior Contract with GOOD/BAD/REJECT examples for features that involve real
   AI or automated judgment, Success Measurement split into an Offline Golden Set, Human Review,
   and Online Metrics with a stated minimum detectable effect, a real Rollout Plan (Exposure,
   Duration, Ramp Gates), Risk Management with Detection and a Fallback/Kill Switch instead of a
   generic risk list, and Ownership & Action naming who is accountable and when the PRD gets
   revisited. The Success Measurement addition has a nice property: the "Offline Golden Set" this
   PRD template asks a PM to describe is literally what `llm-output-quality-scorer`, the sibling
   project in this same portfolio, actually builds.
7. Adding the Behavior Contract section surfaced a second real bug, worse than the first: asking
   the model to decide inline, mid draft, whether a feature needed a Behavior Contract failed
   even on an unambiguous case, a feature literally described as "automatically classifies
   tickets" was marked "not applicable." Moving that judgment into its own dedicated JSON call
   (the same fix pattern as point 4) fixed the false negative, but flipped it into a false
   positive on an unrelated idea, with the model fabricating a quote from the idea text to
   justify its own wrong verdict. The fix that actually held: require the idea text to contain
   one of a fixed set of AI behavior verbs before trusting a "true" verdict at all, a code level
   check the model can't talk its way around. See Tradeoffs for the full story.
8. We tested all three difficulty tiers a real idea could arrive in (vague, medium, fully
   specified) plus a fourth idea that genuinely involves AI behavior, specifically to prove the
   new Behavior Contract section fires correctly in both directions, not just the direction that
   was easy to get right.
9. We kept every example that did not go well in the README instead of swapping in a cleaner
   run: a timing detail gets inverted often enough across regenerations that it is clearly a
   real, recurring limitation, not a one off, and disclosing that consistently is worth more than
   a tidier looking example.

## Setup

```
ollama pull llama3.2
pip install -r requirements.txt
```

## Usage

```
python3 -m prd_gen.cli generate --idea "your feature idea here"
python3 -m prd_gen.cli generate --idea-file idea.txt --output prd.md
python3 -m prd_gen.cli generate --idea "..." --auto     # skip interactive Q&A, unanswered
                                                          # questions become explicit assumptions
```

Interactive mode (the default) prompts for each clarifying question at the terminal before
drafting. `--auto` is for scripted or demo runs; see the three examples below, all generated
with it.

## PRD structure

`## Problem` (Core Problem, Working Hypothesis, Strategy Fit) then `## Goals & Non-Goals` then
`## Target users` then `## Requirements` then `## Behavior Contract` (GOOD/BAD/REJECT examples,
or "Not applicable" for non AI features) then `## Guardrails` then `## Assumptions I made` then
`## Open questions` then `## Success metrics` (Offline Golden Set, Human Review, Online Metrics)
then `## Rollout Plan` (Exposure, Duration, Ramp Gates) then `## Risk Management` (Detection,
Fallback & Kill Switch, Owner) then `## Ownership & Action` (Primary Owner, Decision Points).

See Tradeoffs below for why this differs from a generic PRD template, and for where this
structure came from.

## Sample runs (all three required by CLAUDE.md's definition of done, plus a fourth)

Full outputs: [examples/vague.md](examples/vague.md), [examples/medium.md](examples/medium.md),
[examples/detailed.md](examples/detailed.md), [examples/ai_feature.md](examples/ai_feature.md).

**Vague:** `"We should add some kind of notifications feature."`
Three clarifying questions correctly fired (target user, success metric, scope), all three left
unanswered (`--auto`), all three correctly routed into `## Assumptions I made` in the final PRD.
`## Behavior Contract` correctly says "Not applicable."

**Medium:** `"Notify customers by email when their invoice is 7 days overdue, so they pay
faster and support gets fewer where is my invoice tickets."`
Three clarifying questions fired, mostly about scope edge cases; PRD drafted with those flagged
as assumptions. `## Behavior Contract` correctly says "Not applicable."

**Detailed:** a fully specified version of the same idea (named target user role, explicit
numeric success metrics with a stated baseline, an explicit list of what is out of scope).
Zero clarifying questions, drafted directly. `## Open questions` in the output correctly asks a
real follow up rather than forcing a fake one. This is the core requirement proof that the gap
check does not force questions when the input is already complete. `## Behavior Contract`
correctly says "Not applicable" here too.

**AI feature (new):** `"Add an AI feature that automatically classifies each new support ticket
as Urgent, Normal, or Low priority based on the ticket text..."` (full idea in the file).
Zero clarifying questions (the idea was written to be fully specified). `## Behavior Contract`
correctly fires this time, with 3 real GOOD examples, 2 real BAD examples, and 1 real REJECT
example specific to ticket classification, plus a matched `## Guardrails` section. This example
exists specifically to prove the Behavior Contract logic works in the "yes" direction, not just
the easy "not applicable" direction; see Tradeoffs for why that took two attempts.

## Tradeoffs

Required per [CLAUDE.md](./CLAUDE.md):

1. **PRD structure deliberately differs from a generic template in three ways.** (a) Goals and
   Non Goals are one section, not two; a non goal only makes sense in contrast to a goal, and
   splitting them into separate sections most people do not cross reference loses that contrast.
   (b) No Timeline or Stakeholders sections; those are project tracking metadata that belongs in
   a tracking tool, not the PRD. A timeline embedded in a PRD document is stale within a sprint,
   and rather than solve doc staleness this tool just does not put a staleness prone field in a
   place things go to become authoritative. (c) `Assumptions I made` sits right after
   Requirements, not at the end; scope assumptions need to be seen exactly where scope is
   defined, not buried after a reviewer's attention has already moved to metrics and risk.
2. **Clarifying question threshold: only "blocking" gaps (target user, success metric, scope
   boundary) trigger a question, capped at 3, one per category.** Anything else gets silently
   turned into a stated assumption instead. The cap is enforced twice, in the prompt and in code
   (`pipeline.py: MAX_QUESTIONS`, hard sliced), because a cap that only lives in the prompt is
   not reliable with a small local model (see the next tradeoff). Three matches the three
   category checks by construction; going beyond that turns a quick idea capture flow into an
   interrogation a real PM would just abandon.
3. **The gap check prompt forces per category reasoning before each true or false verdict,
   instead of asking directly for `{sufficient, questions}`.** This was a real bug we hit and
   fixed, not a preference: the bare verdict version of this prompt made `llama3.2` return
   `sufficient: true` for every single input we tried, including "We should add some kind of
   notifications feature." It was not reasoning about the gaps at all, just defaulting to the
   positive answer. Forcing a one sentence reasoning field per category before the verdict fixed
   it completely (see `pipeline.py` and `prompts/gap_check.md` for the exact before and after).
   This is a real, disclosed limitation of small local models for this kind of judgment task:
   without an explicit reasoning step, it does not reliably do the judgment at all.
4. **Whether a feature needs a Behavior Contract is decided by its own dedicated model call, not
   inline during drafting, and that call's "true" verdict is not trusted on its own.** This took
   three attempts, and each one taught something different. Attempt one asked the draft model to
   decide inline, mid document, whether a feature needed a Behavior Contract. It failed even on
   an unambiguous case: a feature literally described as "automatically classifies tickets" was
   still marked "not applicable," the same skipped reasoning failure as point 3, just inside a
   bigger, busier prompt. Attempt two moved the check into its own dedicated JSON call, the same
   fix pattern that worked for the gap check. That fixed the false negative, but on the very next
   test, an unrelated notification idea with no AI behavior at all, the model said "true" and
   justified it by quoting the phrase "automatically suggests" as evidence, a phrase that does
   not appear anywhere in that idea. It did not just guess wrong, it fabricated supporting
   evidence for its own wrong guess. Attempt three, the one that shipped, adds a code level gate:
   a "true" verdict is only accepted if the idea text itself contains one of a fixed list of AI
   behavior verb stems (classify, generate, summarize, recommend, and similar). That is a real,
   disclosed ceiling on this feature: a genuine AI feature described in unusual language could
   still be missed, and we chose a safer false negative over a fabricated false positive.
5. **The PRD structure is intentionally heavier than a minimal one, sourced from a published
   framework rather than invented from scratch.** That framework argues the difference between a
   mediocre PRD and a good one is not length, it is decision making, and gives concrete examples
   of specs that read well but decide
   nothing ("improve engagement" is a hope, not a threshold). We adopted its structure (Behavior
   Contract, Rollout Plan, Risk Management, Ownership) over inventing our own, because it is a
   tested field framework citing a real, successful example (OpenAI's model spec) rather than a
   guess at what a good AI PRD should contain. The real tradeoff: this makes the tool's output
   longer and slower to generate than the original eight section version, a deliberate choice
   that a real launch track feature needs Rollout and Risk Management sections and a fast Slack
   idea does not always need all twelve, worth revisiting if this tool is ever used for something
   closer to a one line internal note than a real PRD.
6. **This tool still hands the LLM the first full draft, in tension with the source framework's
   own advice ("do not use an LLM for your first draft, use it to finesse, as copilot not ghost
   writer").** We are not changing that, and we are naming the tension instead of hiding it: the
   framework's own vocabulary calls an early, rough draft a "speclet," meant to be thrown away or
   heavily revised, not a finished PRD. That is exactly how this tool is positioned, an idea in,
   a reviewable first pass out, with every gap explicitly flagged rather than silently filled, not
   a replacement for a PM's own strategic thinking on the sections that matter most (Strategy Fit,
   the actual behavior contract for a real launch, real rollout risk tolerance). Read that way,
   the tool is closer to the framework's advice than it first looks, but it is worth being
   explicit that a generated speclet still needs a human pass before anyone should trust it as
   final.

## Known limitation (disclosed, not fixed)

The draft step misreads a directional detail often enough across regenerations that it is a
real, recurring pattern, not a one off worth quietly rerunning away. In the current
`examples/detailed.md`, the model wrote "Notifications are sent exactly 7 days **before** an
invoice is due" (twice, once in Requirements and once in the Offline Golden Set description),
inverting the actual ask, which was 7 days **after** the invoice becomes overdue. An earlier
regeneration put the same inverted timing in the medium example instead. This is a drafting
quality limitation of the small local model, not a bug in the gap check, the behavior check, or
the pipeline logic; a stronger model would very likely not make this error, or would make it far
less often. We are leaving the current real output in place rather than swapping in a cleaner
looking regeneration, since quietly picking a better run would be exactly the kind of glossing
over this project's own Tradeoffs discipline exists to prevent, and the fact that this recurs
across different examples is itself a more honest signal than a single instance would be.
