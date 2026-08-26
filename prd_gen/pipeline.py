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


def draft_prd(idea: str, qa_pairs: list[tuple[str, str]], model: str = MODEL) -> str:
    if qa_pairs:
        qa_text = "\n".join(f"- Q: {q}\n  A: {a}" for q, a in qa_pairs)
    else:
        qa_text = "(none — the idea as given had no genuinely blocking gaps)"

    prompt = _load_prompt("draft").replace("{{IDEA}}", idea).replace("{{QA}}", qa_text)
    return chat(model, prompt, temperature=0.4)
