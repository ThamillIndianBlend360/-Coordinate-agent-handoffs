# Trust boundaries

The local checker is a reference for deterministic decisions over trusted snapshots. Its identity JSON is an input supplied by the receiver. Production authentication must resolve the principal from the host identity system. Protect the project policy, evidence catalog and ledger from sender edits. A sender who can rewrite those inputs can defeat the local checks.

Apply authorization again at the service that executes an action. Scope it to the project, intended recipient, operation and delegated requester. Retrieve evidence from the authoritative CI service and bind it to the immutable artifact, suite and environment. Revalidate at execution time if permissions or artifacts may have changed. Serialize state transitions or use a transactional compare-and-set. The SQLite implementation demonstrates atomic local recording only. External deployments require an outbox or equivalent retry-safe action design.

Free-text notes do not affect the reference checker's control flow. This establishes a narrow data-path property. It does not establish that an LLM resists prompt injection. Exercise prompt-injection scenarios with the actual agent and tool environment, and record the outcomes separately.

Keep secrets in the host credential store. Avoid passing credentials in handoff content. Limit memory and evidence retrieval to the project and audience. Record security decisions without copying sensitive data into public reports.

Supporting guidance
- https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html
- https://a2a-protocol.org/
