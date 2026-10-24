CREATE TABLE IF NOT EXISTS tasks(id TEXT PRIMARY KEY, session TEXT, state TEXT, prompt TEXT);
CREATE TABLE IF NOT EXISTS commands(id TEXT PRIMARY KEY, task TEXT, cwd TEXT, exit_code INT, log_dir TEXT);
CREATE TABLE IF NOT EXISTS approvals(id TEXT PRIMARY KEY, task TEXT, binding_hash TEXT, decision TEXT);
