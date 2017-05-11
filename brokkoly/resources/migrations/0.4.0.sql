BEGIN;

INSERT INTO migrations (version) VALUES ('0.4.0');
ALTER TABLE message_logs ADD COLUMN completed_at TIMESTAMP;

COMMIT;
