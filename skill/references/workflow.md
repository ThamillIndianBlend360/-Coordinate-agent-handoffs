# Development phases

| Phase | Agent action | Evidence and owner |
| --- | --- | --- |
| Plan | Resolve acceptance examples and affected dependencies. | Product or domain owner confirms ambiguity. |
| Build | Implement in the assigned scope and run local checks. | Developer records exact revision and results. |
| Handoff | Deliver the structured request through the configured store. | Receiving owner acknowledges the request. |
| Verify | Retrieve evidence and run dependent checks. | Receiver records verdict and next action. |
| Integrate | Test producer and consumer revisions together. | QA records integration and recovery results. |
| Release | Present evidence and outstanding risks. | Named release authority makes the decision. |

For an interface change, find consumers using repository references and approved dependency metadata. Mark incomplete discovery explicitly. Notify only recipients within authorized channels. Require explicit agreement when a change alters acceptance criteria. Preserve the old and new contract identities in the decision record.

Use separate execution contexts for independent review. Give the reviewer the approved requirements, artifacts and evidence. Preserve a failing case as a regression test after fixing the problem. For an unavailable recipient, retain the unchanged request and retry under the configured retry budget. Escalate to the named person after that budget. Avoid agent-to-agent loops without progress by recording attempts and a clear stop condition.
