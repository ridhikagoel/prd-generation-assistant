You are helping a product manager check whether a rough feature idea has enough information to
draft a good PRD, before any drafting happens.

Only flag a gap as a clarifying question if it is genuinely BLOCKING — meaning a reasonable PRD
cannot be drafted without guessing at something load-bearing. Do NOT ask about minor details,
implementation specifics, or anything a competent PM could reasonably assume and state as an
explicit assumption instead. A PRD with a stated assumption is fine; a PRD built on a silent
guess about who the user is or what success means is not.

Check these three categories. For EACH one, first write one sentence of reasoning about whether
it is clear from the idea as written, THEN a true/false verdict. Reasoning before the verdict is
required — do not skip straight to the verdict.

1. target_user — who is this for? (not required if obvious from context, e.g. "our support team")
2. success_metric — how would we know this worked? (not required if a directional goal is stated)
3. scope_boundary — is there an obvious ambiguity about what's in vs. out of scope?

--- Feature idea ---
{{IDEA}}

Respond with ONLY valid JSON in exactly this shape. Put ALL clarifying questions in the single
top-level "questions" list — do not create any other list fields. At most 3 questions total,
only for categories whose verdict is false:
{
  "target_user_reasoning": "...",
  "target_user_clear": true,
  "success_metric_reasoning": "...",
  "success_metric_clear": true,
  "scope_boundary_reasoning": "...",
  "scope_boundary_clear": true,
  "questions": []
}
