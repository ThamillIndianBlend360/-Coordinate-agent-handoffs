# Evaluation protocol

Prepare independently reviewed expected outcomes before running cases. Use valid delivery, stale evidence, missing evidence, contract failure, unavailable recipient, permission denial, identity mismatch, duplicate delivery and out-of-order delivery. Include valid work to measure unnecessary blocking. Save the inputs, output verdict, check trace and implementation fingerprint.

Run deterministic regression checks after changes to the checker. Run application unit, contract and integration checks after relevant code changes. Run the same representative tasks with the actual agent configuration after model, prompt, skill or tool changes. Use a fresh reviewer context and record observed disagreements. An LLM judge may help with qualitative completeness, but permissions and executable outcomes require direct evidence.

Measure delivery time and reviewer effort against comparable tasks with the same acceptance conditions. Report sample size and task mix. Record untested integrations and limits. Avoid extrapolating fixture pass rates to production safety or team productivity.

## Repeatable agent exercises

Run each exercise in a fresh agent context with the skill and the minimum raw inputs. Retain exact request text, model identity when available, source fingerprints, tool calls, output artifacts, review findings, and any errors. Use disposable ledgers and the fixture clock for examples.

| Exercise | Observable completion condition |
| --- | --- |
| Prepare from approved project data | Request uses observed values, identifies recipient, records unresolved items, and reports actual delivery status |
| Verify current evidence | Decision follows all applicable checks and cites the correct revision and run |
| Verify stale evidence | Report identifies required and observed revisions, responsible owner, and retry condition |
| Missing evidence access | Agent records the access blocker and identifies the required source |
| Retry unchanged accepted request | Agent recognizes recorded acceptance and avoids repeated side effects |
| Corrected evidence | Agent uses a new request ID when the evidence reference changes and verifies the new run |

Compare actual outcomes with independently reviewed expected behavior. A single walkthrough provides limited behavioral evidence. Report run counts and retain failed attempts. Publish only claims supported by recorded execution.

