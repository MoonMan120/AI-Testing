# Prompt Templates for Requirement Elicitation

## Chatbot functionality / behavior prompt

You are an expert product analyst. Produce a complete list of functional requirements for a customer-facing AML/KYC assistant chatbot used by bank compliance teams. Include:

- user stories,
- supported channels (web, API, Slack),
- required intents, dialog flows (onboarding, identity verification, suspicious activity reporting, escalation),
- allowed actions (fetch customer profile, initiate verification email/SMS, flag account),
- security & auth requirements (RBAC, audit logs),
- privacy requirements (data retention, masking),
- acceptance criteria and example interactions.

## NLP capabilities prompt

You are an NLP engineer. Provide a detailed list of NLP requirements for the chatbot:

- language support, entity types (names, IDs, dates, amounts, locations),
- intent detection accuracy targets (e.g., >90% top intent on test set),
- NER performance expectations,
- required contextual memory, multi-turn slot-filling behavior,
- confidence thresholding and fallback strategies,
- explainability & provenance for decisions,
- model refresh cadence and evaluation metrics.

## Integration & non-functional prompt

You are a systems architect. Enumerate integration and non-functional requirements:

- APIs to integrate (CRM, case management, transaction store),
- expected throughput (transactions/day), latency SLAs (99th pct < 300ms),
- scalability (horizontal, containerized), testing (load, chaos),
- monitoring and observability needs (traces, metrics, alerting),
- data retention and compliance (GDPR, PCI if applicable).

## Prompts to generate test cases and scenarios

You are a testing lead. Produce test case suites that cover:

- functional flows (KYC onboarding, documents upload, verification),
- edge cases (missing ID, name mismatch, DOB out of range),
- AML scenarios (structuring, rapid deposit spikes, high value TXNs),
- performance/load tests,
- security tests (auth bypass attempts).
  For each test case include preconditions, steps, expected results, and severity.
