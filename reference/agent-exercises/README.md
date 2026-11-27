# Agent exercises

These exercises test whether an agent follows the skill. The checker and application have their own tests. This folder covers the part that is instructions, not code.

## Files

- `setup.py` builds one isolated folder per exercise: a copy of the skill (without `references/evaluation.md`), neutral input files, an empty `work/` folder, and the exact prompt.
- `rubric.md` lists the pass criteria. It was written before any agent ran.
- `results.json` records the first run: prompts, criteria, the agents' reports, limits, and the fingerprint of every skill file used.

## Run them

```sh
python reference/agent-exercises/setup.py OUT_DIR
```

Give each agent the `prompt.txt` in its folder, in a fresh context, one exercise per agent. Then grade each result against `rubric.md` using the saved files, the ledger state and the unchanged inputs, not the agent's own summary.

## First recorded run (2026-11-27)

Seven exercises, one run each. All seven met their criteria: prepare a handoff, verify current evidence, stale evidence, missing evidence, retry an accepted request, corrected evidence, and an unrelated billing project.

This shows the skill can be followed. It does not show how reliably. Limits:

- One run per exercise, on one model.
- The agents wrote their own traces, and several are condensed. Tool calls are not independently verified.
- The same model family produced the agents' work and the grading.
- Exercises 2 and 3 resemble the skill's worked example. The other five do not.
- No live CI, authentication or delivery was involved.

Repeat the run after any change to the skill, the prompts, or the model, and keep every attempt, including failures.
