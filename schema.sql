CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    doc_number TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    logged_in INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL DEFAULT (DATE('now')),
    updated_at TEXT NOT NULL DEFAULT (DATE('now'))
);
CREATE TABLE IF NOT EXISTS tokens (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT (DATE('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);