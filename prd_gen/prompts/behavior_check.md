You are checking whether a feature idea involves AI, ML, or any automated system producing
variable output on its own judgment: generating text, classifying, scoring, ranking,
recommending, or summarizing based on input that varies. A feature that "automatically
classifies," "automatically drafts," "automatically suggests," or similarly makes a judgment
call on variable input DOES qualify, even if the word "AI" is never used. A feature that just
sends a fixed notification, displays stored data, or follows a deterministic rule (like "if 7
days overdue, send this exact email") does NOT qualify.

First write one to two sentences of reasoning, quoting the specific part of the idea that does
or does not involve this kind of variable, judgment-based behavior. Then give a true or false
verdict.

--- Feature idea ---
{{IDEA}}

--- Clarifying questions and answers (if any) ---
{{QA}}

Respond with ONLY valid JSON in exactly this shape:
{
  "reasoning": "...",
  "involves_ai_behavior": true
}
