"""Two-step PRD generation: gap check -> (optional clarification) -> draft.

Prompt templates live in prompts/*.md as separate, readable files rather than inline strings —
the PRD structure and the gap-check judgment are the actual product decisions this tool encodes,
so they need to be auditable and editable without touching Python code.
"""
from pathlib import Path

from prd_gen.llm import chat, chat_json

PROMPTS_DIR = Path(__file__).parent / "prompts"
MODEL = "llama3.2"
MAX_QUESTIONS = 3  # enforced in code, not just requested in the prompt — see README Tradeoffs


def _load_prompt(name: str) -> str:
    return (PROMPTS_DIR / f"{name}.md").read_text()


def check_gaps(idea: str, model: str = MODEL) -> dict:
    """Ask the model to reason per-category before verdicting, then derive sufficiency in code
    from the three *_clear booleans rather than trusting a bare top-level verdict.

    A bare "respond with just {sufficient, questions}" schema turned out to make this small
    local model default to sufficient=true for every input regardless of content, with no
    apparent reasoning happening — see README Tradeoffs. Forcing reasoning-before-verdict per
    category fixed it; this function still doesn't trust the model to only ever populate the
    top-level "questions" list, since in testing it occasionally invented a differently-named
    list (e.g. "scope_boundary_questions") instead — so it collects from any list-valued key
    whose name ends in "questions", not just the exact key asked for.
    """
    prompt = _load_prompt("gap_check").replace("{{IDEA}}", idea)
    result = chat_json(model, prompt, temperature=0)

    clear_flags = [v for k, v in result.items() if k.endswith("_clear")]
    sufficient = bool(clear_flags) and all(clear_flags)

    questions = []
    for key, value in result.items():
        if key.endswith("questions") and isinstance(value, list):
            questions.extend(str(q) for q in value)
    questions = list(dict.fromkeys(questions))[:MAX_QUESTIONS]  # dedupe, preserve order, hard cap

    if questions:
        sufficient = False

    return {"sufficient": sufficient, "questions": questions}


NOT_APPLICABLE_TEXT = (
    "Not applicable — this feature does not involve variable AI or automated behavior that "
    "needs an example-based contract."
)

BEHAVIOR_CONTRACT_YES = (
    "This feature DOES involve AI/automated variable-output behavior (confirmed separately). "
    "Provide:\n"
    "- 3 to 5 GOOD examples: realistic input paired with the output this feature should "
    "produce, each with a one-line note on why it's good.\n"
    "- 2 to 3 BAD examples: realistic input paired with a plausible-but-wrong output this "
    "feature should avoid, each with a one-line note on why it's bad.\n"
    "- 1 to 2 REJECT examples: an input this feature should refuse or escalate instead of "
    "answering, with a one-line note on why.\n"
    "A real launch-ready spec would have 15 to 25 examples; this is a smaller illustrative set "
    "appropriate for an early draft, not a launch-ready contract."
)

GUARDRAILS_YES = (
    "This feature DOES involve AI/automated variable-output behavior (confirmed separately). "
    "List 2 to 4 concrete constraints or limitations on that behavior (what it must never do, "
    "what it must always check before acting)."
)


# Requiring the idea text to actually contain one of these before trusting a "true" verdict —
# see check_ai_behavior docstring for why this second gate exists.
AI_BEHAVIOR_KEYWORDS = [
    "classif", "generat", "summar", "recommend", "rank", "scor", "predict",
    "draft", "translat", "extract", "cluster", "detect", "analy",
]


def check_ai_behavior(idea: str, qa_text: str, model: str = MODEL) -> dict:
    """Dedicated JSON-mode classification call, kept separate from drafting on purpose.

    The first version of this check was embedded inline in the draft prompt as a
    "first decide, then write" instruction. In testing it failed even on an unambiguous case
    (a feature literally described as "automatically classifies... based on ticket text" was
    still marked "Not applicable") — free-form reasoning-then-verdict inside a single large
    12-section generation call isn't reliable, unlike the same pattern in a dedicated JSON-mode
    call (see check_gaps). Moving it out to its own call fixed that false negative.

    But it introduced a false positive: on a plain "send a notification when an invoice is 7
    days overdue" idea (a fixed rule, not a judgment call), the model said "true" and justified
    it with a quote it fabricated — "automatically suggests" — that doesn't appear anywhere in
    the idea text. So this function adds a second gate in code: a "true" verdict is only trusted
    if the idea text itself contains one of a defined set of AI-behavior verb stems. This won't
    catch every real AI feature described in unusual language, and that's a real, disclosed
    limitation (see README Tradeoffs) — but it's a meaningfully safer default than trusting a
    small model's free-text justification, which in testing was shown to hallucinate evidence
    for its own verdict.
    """
    prompt = _load_prompt("behavior_check").replace("{{IDEA}}", idea).replace("{{QA}}", qa_text)
    result = chat_json(model, prompt, temperature=0)
    model_says_yes = bool(result.get("involves_ai_behavior", False))
    keyword_present = any(kw in idea.lower() for kw in AI_BEHAVIOR_KEYWORDS)
    return {
        "involves_ai_behavior": model_says_yes and keyword_present,
        "reasoning": result.get("reasoning", ""),
        "model_verdict": model_says_yes,
        "keyword_present": keyword_present,
    }


def draft_prd(idea: str, qa_pairs: list[tuple[str, str]], model: str = MODEL) -> str:
    if qa_pairs:
        qa_text = "\n".join(f"- Q: {q}\n  A: {a}" for q, a in qa_pairs)
    else:
        qa_text = "(none — the idea as given had no genuinely blocking gaps)"

    behavior_check = check_ai_behavior(idea, qa_text, model)
    if behavior_check["involves_ai_behavior"]:
        behavior_instruction = BEHAVIOR_CONTRACT_YES
        guardrails_instruction = GUARDRAILS_YES
    else:
        behavior_instruction = f'Write exactly: "{NOT_APPLICABLE_TEXT}"'
        guardrails_instruction = 'Write exactly: "Not applicable"'

    prompt = (
        _load_prompt("draft")
        .replace("{{IDEA}}", idea)
        .replace("{{QA}}", qa_text)
        .replace("{{BEHAVIOR_CONTRACT_INSTRUCTION}}", behavior_instruction)
        .replace("{{GUARDRAILS_INSTRUCTION}}", guardrails_instruction)
    )
    return chat(model, prompt, temperature=0.4)
