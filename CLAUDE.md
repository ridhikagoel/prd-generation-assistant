# PRD Generation Assistant

**Category:** AI Agents · **Source #5** · **Skill it proves:** Product thinking

## Why this matters for senior/principal AI PM
Anyone can ask an LLM to "write a PRD." The senior-level version proves you know what makes a
PRD actually good — the right structure, the right level of ambiguity resolved vs. left open,
the right questions asked back — and that you encoded that judgment into a tool, not just a
prompt.

## What to build (MVP scope)
A CLI or small web app that takes a rough feature idea (a paragraph, a Slack message, a ticket)
and produces a structured PRD draft, asking clarifying questions when critical info is missing
rather than hallucinating requirements.

- Input: freeform text description of a feature/problem.
- Step 1 — gap check: LLM identifies missing critical info (target user, success metric,
  constraints) and asks up to 3 clarifying questions before drafting, if genuinely ambiguous.
- Step 2 — draft: generates PRD with sections — Problem, Goals/Non-goals, Users, Requirements,
  Success metrics, Open questions, Risks.
- Explicitly flags assumptions it made (don't let it silently invent scope).
- Output as markdown, ready to paste into Notion/Confluence/Google Docs.

## Suggested stack
Python or TypeScript CLI, LLM API with a multi-turn flow (clarify → draft), simple prompt
templates kept in version-controlled files (not buried inline) so the PRD structure is
auditable and editable.

## Core requirements
- Clarifying-question step must be able to produce zero questions when the input is already
  complete — don't force questions for the sake of it.
- Every generated PRD has an explicit "Assumptions I made" section.
- Prompt templates are separate, readable files — this is a PM tool, the PRD structure itself
  is the product decision.

## Definition of done
- [ ] Runs end-to-end on 3 different sample inputs (vague, medium, detailed) with outputs in README
- [ ] README explains the PRD structure choices (why these sections, why this order)
- [ ] Shows one example where the clarifying-question step correctly caught missing info
- [ ] `.env.example`; no secrets committed

## Portfolio pitch
"Built a PRD assistant that asks the right clarifying questions before drafting — encoding PM
judgment about what makes a PRD complete, not just a prompt wrapper."
