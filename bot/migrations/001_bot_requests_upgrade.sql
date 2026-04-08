ALTER TABLE bot_managers
ADD COLUMN IF NOT EXISTS role text NOT NULL DEFAULT 'manager',
ADD COLUMN IF NOT EXISTS is_active boolean NOT NULL DEFAULT true;

ALTER TABLE bot_requests
ADD COLUMN IF NOT EXISTS taken_at timestamp NULL,
ADD COLUMN IF NOT EXISTS closed_at timestamp NULL,
ADD COLUMN IF NOT EXISTS result_comment text NULL;

CREATE TABLE IF NOT EXISTS bot_request_events (
    id bigserial PRIMARY KEY,
    request_id bigint NOT NULL REFERENCES bot_requests(id) ON DELETE CASCADE,
    actor_telegram_id bigint NOT NULL,
    event_type text NOT NULL,
    old_status text NULL,
    new_status text NULL,
    comment text NULL,
    created_at timestamp NOT NULL DEFAULT now()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_bot_managers_telegram_id ON bot_managers(telegram_id);
CREATE INDEX IF NOT EXISTS idx_bot_requests_status ON bot_requests(status);
CREATE INDEX IF NOT EXISTS idx_bot_requests_manager_telegram_id ON bot_requests(manager_telegram_id);
CREATE INDEX IF NOT EXISTS idx_bot_request_events_request_id ON bot_request_events(request_id);