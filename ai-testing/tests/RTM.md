# Requirements Traceability Matrix (RTM)

REQ-001: Chatbot must verify user identity via KYC data

- Tests: test_kyc_schema_and_basic_validation

REQ-002: System must detect high-value transactions (>100k)

- Tests: test_aml_schema_and_suspicious_flagging

REQ-003: System must detect rapid transaction bursts per customer

- Tests: test_aml_transaction_aggregation_rule

REQ-004: Data generation and ingestion must produce valid schema & unique IDs

- Tests: test_kyc_schema_and_basic_validation, test_aml_schema_and_suspicious_flagging
