"""Regenerate the README chart. Encodes the outcomes of the four checked-in example runs
(examples/*.md) — the clarifying-question count and the Behavior-Contract gate result per input.
These are `--auto` runs documented in the README; this script just draws them.

    python3 scripts/make_charts.py  ->  outputs/gate_behavior.png
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "outputs"

# (input tier, clarifying questions fired, behavior-contract fired?, gate verdict correct?)
RUNS = [
    ("vague\n'add some kind of\nnotifications feature'", 3, False, True),
    ("medium\n'email when invoice\n7 days overdue'", 3, False, True),
    ("detailed\nfully-specified\nsame idea", 0, False, True),
    ("AI feature\n'auto-classify each\nticket by urgency'", 0, True, True),
]


def main() -> None:
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4.4))
    labels = [r[0] for r in RUNS]
    qs = [max(r[1], 0.07) for r in RUNS]   # stub so a 0-question bar is still visible
    colors = ["#6baed6" if not r[2] else "#e6550d" for r in RUNS]
    ax.bar(range(len(RUNS)), qs, color=colors, width=0.55)

    for i, r in enumerate(RUNS):
        ax.text(i, r[1] + 0.12, f"{r[1]} question{'s' if r[1] != 1 else ''}", ha="center",
                va="bottom", fontsize=8, weight="bold")
        bc = "Behavior Contract: FIRED\n(correct)" if r[2] else "Behavior Contract:\n“not applicable” (correct)"
        ax.text(i, r[1] + 0.55, bc, ha="center", va="bottom", fontsize=8,
                color=("#e6550d" if r[2] else "#555"))

    ax.set_xticks(range(len(RUNS)))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("clarifying questions the gap check asked")
    ax.set_ylim(0, 4.6)
    ax.set_yticks([0, 1, 2, 3])
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("The gates fire on the input, not on every input\n"
                 "questions scale with vagueness and hit 0 on a complete spec; "
                 "the AI-behavior gate fires once, correctly", fontsize=10)
    fig.tight_layout()
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / "gate_behavior.png", dpi=130)
    plt.close(fig)
    print(f"wrote {OUT/'gate_behavior.png'}")


if __name__ == "__main__":
    main()
