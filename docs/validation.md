# Revision validation

## Executed local checks

The updated Python evaluator passed all 16 handoff scenarios, seven application tests, eight operational regression tests, concurrent retries, recipient recovery, and corrected-evidence recovery. The runnable demonstration produced verified, duplicate, blocked, and verified in order. Full traces and Python version are in reference/results.json.

JavaScript was syntax-checked with Node. A lightweight DOM stub exercised nine current/legacy routes, all 16 scenario reveal interactions, three example stages, and repository URL validation. This checks rendering logic and event handling. Actual browser layout and accessibility review remain pending.

Direct structural checks passed for the skill's name and description, linked references, matching packaged checker, consistent published evidence, and removal of ZIP links from the active interface. The bundled quick_validate.py could not run because its PyYAML dependency is unavailable.

## Agent exercises

On 2026-11-27 I ran seven exercises, each once, with a fresh agent that saw only the skill folder and neutral input files: prepare a handoff, verify current evidence, stale evidence, missing evidence, retry an accepted request, corrected evidence, and an unrelated billing project. All seven met criteria written before the run. The criteria, prompts, reports and limits are in reference/agent-exercises/.

The limits are one run each, one model, condensed self-written traces, and my own grading. Rebuild the exercises with `python reference/agent-exercises/setup.py OUT_DIR`.

## Publication decisions

The repository URL and tested release reference are set in assets/config.js. Until an HTTPS URL is supplied, the interface shows the repository link as pending.

The ledger continues to use its existing schema. Documented usage is one project and receiving workflow per ledger, with request IDs unique within that file. This release preserves existing accepted records and CLI verdict exit-code behavior.
