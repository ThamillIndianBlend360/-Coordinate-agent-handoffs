# Worked verification reports

These order-alert examples use illustrative revisions and controlled evidence.

## Blocked handoff

**Decision:** blocked

The available test run covers an earlier revision.

| Item | Required | Observed |
| --- | --- | --- |
| Project | order-alerts | order-alerts |
| Evidence revision | b72 | a19 |

**Request:** handoff-142 for ORD-142, backend-agent to frontend-agent.

**Evidence:** receiver fixture catalog, run-419. Verification stopped at Evidence binding.

**Next action and owner:** backend owner provides required test results for b72.

**Retry condition:** receiver can retrieve applicable evidence with the approved contract, suite, environment, and passing required tests.

If the evidence reference changes, prepare a new request ID. Preserve the original blocked report in the task history.

## Verified handoff

**Decision:** verified for b72 under alerts-schema-2.

The receiver matched project, revision, suite, environment and contract. Required duplicate-delivery and consumer-contract outcomes were true. One local acceptance record was written.

**Next owner:** receiving frontend owner coordinates the next integration step under the project's release workflow.

**Scope:** deterministic fixture verification. Live CI retrieval and authenticated delivery require host integration.
