# PRD Generation Assistant

A two-step CLI that turns a rough feature idea into a structured PRD: first checks for genuinely
blocking gaps (target user, success metric, scope boundary) and asks up to 3 clarifying
questions only if real gaps exist, then drafts the PRD — explicitly flagging every assumption it
had to make instead of silently inventing scope.

Runs entirely on a local [Ollama](https://ollama.com) model (`llama3.2`) — no API key, no
billing. See the parent [CLAUDE.md](../CLAUDE.md) for the broader portfolio initiative.

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
drafting. `--auto` is for scripted/demo runs — see the three examples below, all generated with it.

## PRD structure

`## Problem` → `## Goals & Non-Goals` → `## Target users` → `## Requirements` →
`## Assumptions I made` → `## Success metrics` → `## Open questions` → `## Risks`

See Tradeoffs below for why this differs from a generic PRD template.

## Sample runs (all three required by CLAUDE.md's definition of done)

Full outputs: [examples/vague.md](examples/vague.md), [examples/medium.md](examples/medium.md),
[examples/detailed.md](examples/detailed.md).

**Vague** — `"We should add some kind of notifications feature."`
→ 3 clarifying questions correctly fired (target user, success metric, scope), all three
unanswered (`--auto`), all three correctly routed into `## Assumptions I made` in the final PRD.

**Medium** — `"Notify customers by email when their invoice is 7 days overdue, so they pay
faster and support gets fewer where-is-my-invoice tickets."`
→ 3 clarifying questions fired (mostly about scope edge cases); PRD drafted with those flagged
as assumptions.

**Detailed** — a fully-specified version of the same idea (named target user role, explicit
numeric success metrics with a stated baseline, explicit out-of-scope list)
→ **zero clarifying questions**, drafted directly. `Open questions` in the output correctly
reads "None — all scope decisions were directly stated...". This is the core-requirement proof
that the gap check doesn't force questions when the input is already complete.

## Tradeoffs

Required per [CLAUDE.md](./CLAUDE.md):

1. **PRD structure deliberately differs from a generic template in three ways.** (a) Goals and
   Non-Goals are one section, not two — a non-goal only makes sense in contrast to a goal, and
   splitting them into separate sections most people don't cross-reference loses that contrast.
   (b) No Timeline or Stakeholders sections — those are project-tracking metadata that belongs
   in a tracking tool, not the PRD; a timeline embedded in a PRD document is stale within a
   sprint, and rather than solve doc-staleness this tool just doesn't put a staleness-prone field
   in a place things go to become authoritative. (c) `Assumptions I made` sits right after
   Requirements, not at the end — scope assumptions need to be seen exactly where scope is
   defined, not buried after a reviewer's attention has already moved to metrics and risk.
2. **Clarifying-question threshold: only "blocking" gaps (target user, success metric, scope
   boundary) trigger a question, capped at 3, one per category.** Anything else gets silently
   turned into a stated assumption instead. The cap is enforced twice — in the prompt AND in
   code (`pipeline.py: MAX_QUESTIONS`, hard-sliced) — because a prompt-only cap isn't reliable
   with a small local model (see the next tradeoff). Three matches the three category checks by
   construction; going beyond that turns a quick idea-capture flow into an interrogation a real
   PM would just abandon.
3. **The gap-check prompt forces per-category reasoning before each true/false verdict, instead
   of asking directly for `{sufficient, questions}`.** This was a real bug I hit and fixed, not
   a preference: the bare-verdict version of this prompt made `llama3.2` return
   `sufficient: true` for every single input I tried, including "We should add some kind of
   notifications feature." — it wasn't reasoning about the gaps at all, just defaulting to the
   positive answer. Forcing a one-sentence reasoning field per category before the verdict fixed
   it completely (see `pipeline.py` and `prompts/gap_check.md` for the exact before/after). This
   is a real, disclosed limitation of small local models for this kind of judgment task: without
   an explicit reasoning step, it doesn't reliably do the judgment at all.

## Known limitation (disclosed, not fixed)

The draft step occasionally misreads a directional detail even when it's stated plainly: in
`examples/medium.md`, the model wrote "Send a notification email to customers 7 days **before**
their invoice is due" — inverting the actual ask, which was 7 days **after** the invoice becomes
overdue. This is a drafting-quality limitation of the small local model, not a bug in the gap
check or the pipeline logic; a stronger model would very likely not make this error. Flagging it
here rather than hand-picking a cleaner example, since silently swapping in a better-looking run
would be exactly the kind of glossing-over this project's own Tradeoffs discipline exists to
prevent.
