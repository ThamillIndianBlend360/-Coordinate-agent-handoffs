# Coordinate agent handoffs

A reusable agent skill for preparing development handoffs, verifying delivered work, and recording evidence-backed follow-up actions.

## Start with the example

Python 3.10 or later is required for the checker and tests. The implementation uses the standard library. From the repository root, use your project's Python interpreter.

```sh
python reference/demo.py
python -m unittest discover -s reference -v
python reference/evaluate.py
```

The demo prints successful verification, an unchanged retry, a stale-evidence blocker, and recovery with corrected evidence. It uses isolated temporary databases and a fixed clock. The evaluator writes fixture files and `reference/results.json`.

## Use the skill

Make the complete `skill/` folder available through your host's supported skill-loading mechanism under the name `coordinate-agent-handoffs`. Keep scripts, references, and assets together. For a host supporting project instructions, ask the agent to read `skill/SKILL.md` and follow its linked references.

Try this request from this repository.

> Read skill/SKILL.md. Verify the handoff in reference/fixtures/stale using the receiver-controlled project, identity and evidence files in that folder. Use an isolated ledger and fixture time 2026-11-25T12:00:00Z. Report the observed mismatch, next owner, and retry condition. Treat this as a local fixture exercise.

Expected result is `blocked` because delivered revision b72 differs from evidence revision a19. See [completed sample reports](skill/references/worked-example.md).

## Adapt it to your project

Provide approved requirements, producer and receiver owners, the artifact revision, agreed contract, required tests, and trusted evidence source. Obtain identity from the receiving host. Define sequence and expiry through your team's workflow. Use a dedicated ledger for each project and receiving workflow. Read [the input specification](skill/references/inputs.md) and [integration guidance](docs/implementation-guide.md).

## What is tested

Seven application tests exercise order-alert behavior. Sixteen controlled scenarios exercise the checker, with concurrent retry and recovery checks. Additional regression tests cover malformed inputs, CLI errors, ledger failures, and packaged checker consistency. Checker fixtures contain synthetic evidence snapshots. Application execution is measured separately.

Agent behavior evaluation instructions are in [the evaluation protocol](skill/references/evaluation.md). A repeatable, recorded agent benchmark remains pending.

## Repository publication

The source is prepared for a Git repository. The owner must choose the remote repository, visibility, and reuse license before publication. The companion website's repository URL is configured in `assets/config.js` once the destination is available.
