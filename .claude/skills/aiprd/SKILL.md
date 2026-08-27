---
name: aiprd
description: >-
  Turn a rough feature idea (a sentence, a Slack message, a ticket) into a structured PRD.
  First checks for genuinely blocking gaps (target user, success metric, scope boundary) and
  asks up to 3 clarifying questions only if real gaps exist, then drafts a 12-section AI-era
  PRD, explicitly flagging every assumption instead of silently inventing scope. Use when the
  user asks to write / draft / generate a PRD, a spec, or a product requirements doc, or says
  "PRD for <feature>".
---

# PRD generation assistant

This skill is the zero-setup version of the `prd-generation-assistant` CLI in this repo. It
encodes the same two-step method — **gap check → (clarify) → draft** — and the same PRD
structure, but *you* (Claude) are the model, so it needs no Ollama, no Python, no API key.

The canonical prompt logic also lives in [`prd_gen/prompts/`](../../../prd_gen/prompts/)
(`gap_check.md`, `behavior_check.md`, `draft.md`). If you change the method here, change it
there too, and vice versa.

---

## Step 1 — Gap check (always run this first, before any drafting)

Only flag a gap as a clarifying question if it is **genuinely blocking** — a reasonable PRD
cannot be drafted without guessing at something load-bearing. Minor details, implementation
specifics, or anything a competent PM could reasonably assume and *state as an explicit
assumption* → do **not** ask; handle it in `## Assumptions I made` later.

Check these three categories. For **each**, write one sentence of reasoning about whether it
is clear from the idea as written, **then** a clear / not-clear verdict. Reasoning before the
verdict is mandatory — do not jump straight to a verdict (a bare verdict is unreliable and
tends to default to "clear").

1. **target_user** — who is this for? Not needed if obvious from context (e.g. "our support team").
2. **success_metric** — how would we know this worked? Not needed if a directional goal is stated.
3. **scope_boundary** — is there an obvious ambiguity about what is in vs. out of scope?

Produce **at most 3 questions total**, at most **one per category**, and only for categories
whose verdict is "not clear". If all three are clear, ask nothing and go straight to Step 3.

> **Why the cap is 3:** three matches the three category checks by construction. More than that
> turns a quick idea-capture flow into an interrogation a real PM would abandon. This is a
> deliberate design decision, not a default — keep it.

## Step 2 — Clarify (only if Step 1 produced questions)

Ask the questions with the `AskUserQuestion` tool (one question per category, concrete
multiple-choice options plus room for a custom answer). Then draft with the answers folded in.

**One-shot escape hatch:** if the user said "just draft it", "don't ask", "auto", or similar,
skip the asking. Every unanswered blocking gap becomes an explicit bullet in
`## Assumptions I made` — state the assumption you made and one line on why that branch, and
what would make it wrong. Never silently fill the gap.

## Step 3 — AI-behavior check (decides whether the PRD gets a Behavior Contract)

Decide whether the feature involves AI/ML or any automated system producing **variable output
on its own judgment**: generating text, classifying, scoring, ranking, recommending,
summarizing, extracting, detecting, predicting — on input that varies. A feature that
"automatically classifies / drafts / suggests" qualifies even if the word "AI" never appears.
A feature that sends a fixed notification, displays stored data, or follows a deterministic
rule ("if 7 days overdue, send this exact email") does **not** qualify.

Write one or two sentences of reasoning that **quote the specific part of the idea** that does
or does not involve this kind of judgment-based behavior, then a true/false verdict.

**Gate (do not skip):** only treat the verdict as **true** if the idea text (or a clarifying
answer) actually contains one of these behavior verbs or a close variant —
*classify, generate, summarize, recommend, rank, score, predict, draft, translate, extract,
cluster, detect, analyze*. If your reasoning says "true" but no such word appears, downgrade to
**false**. This exists because free-text "is it AI?" judgments hallucinate supporting evidence;
a safer false negative beats a fabricated false positive. If a genuine AI feature is described
in unusual language and gets missed, that is the accepted failure mode.

- **True** → write a real `## Behavior Contract` and matching `## Guardrails` (see structure below).
- **False** → `## Behavior Contract` is exactly: *"Not applicable — this feature does not involve
  variable AI or automated behavior that needs an example-based contract."* and `## Guardrails`
  is exactly: *"Not applicable"*.

## Step 4 — Draft the PRD

Write the PRD in **exactly these 12 sections, in this order, with these exact headings**. Use
only information given or directly implied — do not invent metrics, segments, or product
decisions. Anything you had to fill goes in `## Assumptions I made`.

```
## Problem
- Core Problem: one sentence — what's wrong and for whom.
- Working Hypothesis: one sentence — our proposed answer.
- Strategy Fit: one sentence — which broader bet this unlocks. If not stated or implied, say so
  plainly rather than inventing a strategic narrative.

## Goals & Non-Goals
A side-by-side table: what this IS trying to achieve, and explicitly what it is NOT (scope
boundaries), so the contrast is visible. Keep non-goals to ~3, concrete.

## Target users
Who specifically this is for. If not fully specified, state your best-supported inference and
flag it as an assumption (also list it under Assumptions).

## Requirements
Bulleted, concrete, testable behavior a reviewer could check off. Not implementation detail.

## Behavior Contract
Per Step 3. If applicable: 3–5 GOOD examples (realistic input → the output this should
produce, one-line why-good), 2–3 BAD examples (input → plausible-but-wrong output to avoid,
one-line why-bad), 1–2 REJECT examples (input this should refuse or escalate, one-line why).
Note this is a small illustrative set; a launch-ready spec would have 15–25.

## Guardrails
Per Step 3. If applicable: 2–4 concrete constraints on the behavior (what it must never do,
what it must always check before acting).

## Assumptions I made
Every place above where you filled a gap instead of using a stated fact or a clarifying
answer, one bullet each — the assumption, why that branch, what would make it wrong. If truly
none: "None — all scope decisions were directly stated or resolved by the clarifying answers."

## Open questions
Genuinely unresolved things a reviewer should weigh in on — distinct from Assumptions (these
are flagged for discussion, not silently decided).

## Success metrics
- Offline Golden Set: what a pre-launch validation dataset looks like, or "Not applicable" if
  the feature is simple/deterministic enough not to need one.
- Human Review: what a person manually checks before or shortly after launch.
- Online Metrics: 1–3 concrete KPIs with numeric thresholds, plus one sentence on the minimum
  detectable effect (how big a change counts as signal, not noise).

## Rollout Plan
- Exposure: what % of users/traffic this launches to initially.
- Duration: how long the initial rollout runs before a go/no-go.
- Segments & Ramp Gates: criteria that must be met before exposure expands.

## Risk Management
- Detection: how we'd notice this failing in production, concretely.
- Fallback & Kill Switch: what happens if it's turned off, and how fast.
- Owner: who gets paged (a role is fine).

## Ownership & Action
- Primary Owner: the accountable person or team (a role is fine).
- Decision Points: when this PRD/feature should be revisited (e.g. after first rollout data,
  after N days).
```

Write all 12 sections even if some are short. Output the markdown PRD with no preamble before
`## Problem`.

## Step 5 — Deliver

Save the PRD to `<slug>-prd.md` in the working directory (slug from the feature name), then
tell the user the path and give a 3–4 line summary: how many clarifying questions fired,
whether the Behavior Contract applied, and which assumptions the draft is resting on.

---

## Structure rationale (why this differs from a generic PRD template)

The 12-section shape is adapted from Aakash Gupta's published "AI PRD" framework (Opportunity
Framing → Boundaries → Success Measurement → Rollout → Risk Management → Ownership, plus the
AI-specific Behavior Contract + Guardrails). Deliberate deviations, each a real call:

- **Goals and Non-Goals are one section, not two.** A non-goal only means something next to a
  goal; splitting them loses the contrast most reviewers never cross-reference.
- **No Timeline or Stakeholders sections.** That's project-tracking metadata that goes stale in
  a sprint and belongs in a tracking tool, not the authoritative doc.
- **`Assumptions I made` sits right after Requirements**, not at the end — scope assumptions
  need to be seen where scope is defined, before the reviewer's attention moves to metrics.
- **Reasoning-before-verdict** in Steps 1 and 3, and the **hard cap of 3** questions, and the
  **behavior-verb gate** in Step 3 — all carried over from bugs the CLI actually hit. Keep them.

## Not a finished PRD

What this produces is a *speclet* — a reviewable first pass with every gap flagged, not a
replacement for the PM's own thinking on Strategy Fit, the real behavior contract for a launch,
and real rollout risk tolerance. Hand it back to a human before anyone treats it as final.
