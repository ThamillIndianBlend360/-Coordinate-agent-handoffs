# Revision validation

## Executed local checks

The updated Python evaluator passed all 16 handoff scenarios, seven application tests, eight operational regression tests, concurrent retries, recipient recovery, and corrected-evidence recovery. The runnable demonstration produced verified, duplicate, blocked, and verified in order. Full traces and Python version are in reference/results.json.

JavaScript was syntax-checked with Node. A lightweight DOM stub exercised nine current/legacy routes, all 16 scenario reveal interactions, three example stages, and repository URL validation. This checks rendering logic and event handling. Actual browser layout and accessibility review remain pending.

Direct structural checks passed for the skill's name and description, linked references, matching packaged checker, consistent published evidence, and removal of ZIP links from the active interface. The bundled quick_validate.py could not run because its PyYAML dependency is unavailable.

## Independent agent exercise

An independent agent was assigned preparation, stale-evidence verification, and accepted-request retry using the revised skill and raw fixtures. It stopped before reading any input. The Windows restricted-token sandbox could not enforce the writable-root configuration, and the elevated file-read request was rejected by the user. Outcomes remain unverified.

Reproduce these exercises using skill/references/evaluation.md once the evaluator can access the files. Retain exact prompts, inputs, tool traces, outputs, and reviewer findings before publishing agent-behavior claims.

## Publication decisions

The remote repository URL, visibility, reuse license, and tested release reference remain owner decisions. The interface explicitly shows the repository link as pending until assets/config.js supplies an HTTPS URL.

The ledger continues to use its existing schema. Documented usage is one project and receiving workflow per ledger, with request IDs unique within that file. This release preserves existing accepted records and CLI verdict exit-code behavior.
