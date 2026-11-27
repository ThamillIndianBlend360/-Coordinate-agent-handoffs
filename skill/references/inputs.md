# Checker inputs

Use UTF-8 JSON and Python 3.10 or later. Supply each input through its CLI flag. Paths may be absolute or relative to the process working directory.

| Input | Required shape | Source |
| --- | --- | --- |
| Message | Non-empty strings `request_id`, `task`, `project`, `sender`, `recipient`, `action`, `revision`, `contract`, `evidence_id`, `expires_at`; positive integer `sequence`; string array `acceptance` | Sender's request |
| Project | Strings `id`, `revision`, `contract`, `suite`, `environment`; non-empty string arrays `required_acceptance`, `required_tests`; string array `available_agents`; object `grants` | Receiver-approved project record |
| Identity | String `principal`; string array `projects` | Receiving service's authenticated session |
| Evidence | Object keyed by evidence ID. Each run contains `project`, `revision`, `contract`, `suite`, `environment`, and a `tests` object keyed by required test name | Independently retrieved CI run or receiver-executed checks |

`grants` maps principal names to objects containing string arrays `actions` and `recipients`. Required test outcomes must be JSON `true`. Missing or false outcomes require correction. Missing evidence blocks verification.

`expires_at` is an ISO timestamp including timezone. Sequence orders accepted handoffs for a task. Revision identifies the delivered artifact. Obtain sequence and expiry policy from the team's workflow.

The optional message `context` object carries `artifact_locations`, `unresolved_issues`, `next_owner`, and `retry_condition`. These fields support the agent's report and are included in the payload fingerprint. The checker does not fetch their locations.

Use a durable SQLite ledger dedicated to one project and receiving workflow. It records accepted IDs, fingerprints, task sequences, and results. Replays undergo current identity, scope, expiry, acceptance, and revision checks before duplicate lookup. Rechecking changed requirements requires a fresh request and advancing sequence.

The CLI prints a JSON verdict. File-reading or JSON-decoding errors exit with status 2. Verification decisions, including blocked and changes_required, exit with status 0 for compatibility. Automation must inspect `verdict`. Save operational reports outside the acceptance ledger.

The repository's `reference/fixtures/valid/` contains a complete four-file example. It uses an illustrative revision and a fixed clock. Actual work uses trusted current time and actual artifact identities. The `expires_at` in `skill/assets/handoff.json` is an illustrative date that has already passed. Set a future expiry from team policy, or pass `--now` when reproducing fixtures.
