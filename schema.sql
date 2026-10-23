CREATE TABLE IF NOT EXISTS usage_data (
    date DATE NOT NULL,
    model TEXT NOT NULL,
    prompts BIGINT NOT NULL DEFAULT 0,
    tokens BIGINT NOT NULL DEFAULT 0,
    cost NUMERIC(14, 4) NOT NULL DEFAULT 0,
    response_time NUMERIC(14, 4) NOT NULL DEFAULT 0,
    PRIMARY KEY (date, model)
);
