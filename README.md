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
   generic template: Problem, then Goals and Non Goals together (not split into two sections),
   then Target users, Requirements, an Assumptions section placed right after Requirements
   instead of at the end, then Success metrics, Open questions, and Risks.
6. We tested all three difficulty tiers a real idea could arrive in: vague, medium, and fully
   specified, and proved both directions work, a vague idea correctly triggers real questions,
   and a fully specified idea correctly triggers zero.
7. We kept one example that did not go well and put it in the README instead of swapping it for
   a cleaner run: the medium example's draft inverted a timing detail, writing "before" when the
   input clearly said "after."

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

`## Problem` then `## Goals & Non-Goals` then `## Target users` then `## Requirements` then
`## Assumptions I made` then `## Success metrics` then `## Open questions` then `## Risks`.

See Tradeoffs below for why this differs from a generic PRD template.

## Sample runs (all three required by CLAUDE.md's definition of done)

Full outputs: [examples/vague.md](examples/vague.md), [examples/medium.md](examples/medium.md),
[examples/detailed.md](examples/detailed.md).

**Vague:** `"We should add some kind of notifications feature."`
Three clarifying questions correctly fired (target user, success metric, scope), all three left
unanswered (`--auto`), all three correctly routed into `## Assumptions I made` in the final PRD.

**Medium:** `"Notify customers by email when their invoice is 7 days overdue, so they pay
faster and support gets fewer where is my invoice tickets."`
Three clarifying questions fired, mostly about scope edge cases; PRD drafted with those flagged
as assumptions.

**Detailed:** a fully specified version of the same idea (named target user role, explicit
numeric success metrics with a stated baseline, an explicit list of what is out of scope).
Zero clarifying questions, drafted directly. `Open questions` in the output correctly reads
"None, all scope decisions were directly stated...". This is the core requirement proof that
the gap check does not force questions when the input is already complete.

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

## Known limitation (disclosed, not fixed)

The draft step occasionally misreads a directional detail even when it is stated plainly: in
`examples/medium.md`, the model wrote "Send a notification email to customers 7 days **before**
their invoice is due," inverting the actual ask, which was 7 days **after** the invoice becomes
overdue. This is a drafting quality limitation of the small local model, not a bug in the gap
check or the pipeline logic; a stronger model would very likely not make this error. We are
flagging it here rather than swapping in a cleaner looking example, since quietly picking a
better run would be exactly the kind of glossing over this project's own Tradeoffs discipline
exists to prevent.
