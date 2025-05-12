CREATE TABLE IF NOT EXISTS rate_codes (
  code SMALLINT PRIMARY KEY,
  description TEXT NOT NULL
);

INSERT INTO rate_codes (code, description) VALUES
  (1, 'Standard rate'),
  (2, 'JFK'),
  (3, 'Newark'),
  (4, 'Nassau or Westchester'),
  (5, 'Negotiated fare'),
  (6, 'Group ride'),
  (99, 'Null/unknown')
ON CONFLICT (code) DO NOTHING;
