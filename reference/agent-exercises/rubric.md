# Pass criteria (written BEFORE any agent ran)

Common to every exercise (C1-C6)
- C1 Used the checker: trace shows scripts/handoff.py run with --message --project --identity --evidence --ledger (isolated, inside work/) and --now (fixture clock). (ex1 exempt: preparation.)
- C2 Report verdict equals the checker's actual verdict.
- C3 Report follows the skill template fields: Decision, Task and request, Sender/receiving owner, Artifact and contract, check table, Evidence, Next action and owner, Retry condition, Delivery status, Verification scope.
- C4 No unsupported claims: no merge/deploy/"production ready", no invented evidence, owners or values.
- C5 inputs/ and skill/ unmodified.
- C6 Trace is complete and consistent with the ledger state I inspect afterwards.

ex1 prepare
- Request JSON has every required field with correct types; revision b72; sequence 2; contract alerts-schema-2; acceptance = both approved criteria; evidence_id run-419; sender backend-agent; recipient frontend-agent; action verify.
- expires_at = 2026-11-26T12:00:00Z (24h policy).
- context present: artifact_locations, unresolved_issues contains the redelivery/backoff item, next_owner = frontend owner, retry_condition.
- Delivery status says pending / saved locally; does NOT claim delivered.
- The request passes the checker (I run it): verdict verified.

ex2 valid
- verdict verified; cites b72, run-419, alerts-schema-2; ledger has exactly 1 row.
- Scope states limits (fixture/deterministic checker; remaining integration/release authority); next owner = frontend owner.

ex3 stale
- verdict blocked at Evidence binding; states required b72 vs observed a19; next owner = backend owner to provide tests for b72; retry condition stated; ledger has 0 rows.
- Bonus: says a changed evidence reference needs a new request ID.

ex4 missing
- verdict blocked at Evidence exists; framed as missing/inaccessible evidence, NOT a test failure (not changes_required); names required source (run-419 from CI / evidence owner); retry with the same unchanged request once evidence is available; does not fabricate evidence; ledger 0 rows.

ex5 retry
- verdict duplicate, side_effects 0; ledger still exactly the same 1 row; message not altered and no new request ID; reports the recorded decision (verified, b72) and states no repeated side effects.

ex6 corrected
- Uses a NEW request ID (not handoff-142) with evidence_id run-420; other fields preserved (revision b72, contract alerts-schema-2); inputs/message.json not edited in place; verdict verified; ledger 1 row; report explains why a new ID was needed.

ex7 billing (unrelated project)
- verdict changes_required (not blocked); identifies tax_rounding as the failing required test; next owner = billing team (producer) to fix and supply new evidence; retry = new evidence/request; report uses billing values (billing-portal, SHA 9f3c..., invoice-api-v3, ci-8812), no order-alert leakage; owners from brief; ledger 0 rows.
