-- cert-pepper database schema
-- SQLite-compatible; PostgreSQL migration path via SQLAlchemy

PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

-- ============================================================
-- CONTENT TABLES
-- ============================================================

CREATE TABLE IF NOT EXISTS certifications (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    code        TEXT NOT NULL UNIQUE,       -- e.g. "SY0-701"
    name        TEXT NOT NULL,              -- e.g. "CompTIA Security+"
    vendor      TEXT NOT NULL DEFAULT '',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS domains (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    certification_id INTEGER NOT NULL REFERENCES certifications(id),
    number          INTEGER NOT NULL,       -- 1-5
    name            TEXT NOT NULL,
    weight_pct      REAL NOT NULL,          -- e.g. 28.0
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(certification_id, number)
);

CREATE TABLE IF NOT EXISTS topics (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id   INTEGER NOT NULL REFERENCES domains(id),
    name        TEXT NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS questions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id       INTEGER NOT NULL REFERENCES domains(id),
    topic_id        INTEGER REFERENCES topics(id),
    number          INTEGER NOT NULL,       -- Q1, Q2, etc. within file
    stem            TEXT NOT NULL,
    option_a        TEXT NOT NULL,
    option_b        TEXT NOT NULL,
    option_c        TEXT NOT NULL,
    option_d        TEXT NOT NULL,
    correct_answer  TEXT NOT NULL CHECK(correct_answer IN ('A','B','C','D')),
    explanation     TEXT NOT NULL DEFAULT '',
    difficulty      REAL NOT NULL DEFAULT 0.3,  -- 0.0 easy → 1.0 hard
    source_file     TEXT NOT NULL DEFAULT '',
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(domain_id, number)
);

CREATE TABLE IF NOT EXISTS flashcards (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    domain_id        INTEGER REFERENCES domains(id),
    category         TEXT NOT NULL DEFAULT '',
    front            TEXT NOT NULL,
    back             TEXT NOT NULL,
    tip              TEXT NOT NULL DEFAULT '',
    certification_id INTEGER REFERENCES certifications(id),
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS acronyms (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    acronym          TEXT NOT NULL UNIQUE,
    full_term        TEXT NOT NULL,
    category         TEXT NOT NULL DEFAULT '',
    certification_id INTEGER REFERENCES certifications(id),
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- AI CACHE
-- ============================================================

CREATE TABLE IF NOT EXISTS ai_explanations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    content_type    TEXT NOT NULL,          -- 'question', 'flashcard', 'acronym'
    content_id      INTEGER NOT NULL,
    explanation_type TEXT NOT NULL,         -- 'full', 'hint', 'wrong_answer'
    selected_answer TEXT,                   -- for wrong_answer explanations
    model_used      TEXT NOT NULL,
    prompt_hash     TEXT NOT NULL,
    content         TEXT NOT NULL,
    tokens_used     INTEGER NOT NULL DEFAULT 0,
    cached          INTEGER NOT NULL DEFAULT 0,  -- 1 if Anthropic cache hit
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(content_type, content_id, explanation_type, selected_answer)
);

-- ============================================================
-- USERS & SESSIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT NOT NULL UNIQUE DEFAULT 'default',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS study_sessions (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER NOT NULL REFERENCES users(id),
    session_type     TEXT NOT NULL,
    domain_filter    INTEGER,
    started_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    ended_at         DATETIME,
    questions_seen   INTEGER NOT NULL DEFAULT 0,
    questions_correct INTEGER NOT NULL DEFAULT 0,
    total_time_seconds INTEGER NOT NULL DEFAULT 0,
    certification_id INTEGER REFERENCES certifications(id)
);

-- ============================================================
-- ATTEMPTS
-- ============================================================

CREATE TABLE IF NOT EXISTS question_attempts (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id          INTEGER NOT NULL REFERENCES study_sessions(id),
    user_id             INTEGER NOT NULL REFERENCES users(id),
    question_id         INTEGER NOT NULL REFERENCES questions(id),
    selected_answer     TEXT NOT NULL,
    is_correct          INTEGER NOT NULL,   -- 0/1
    time_taken_seconds  REAL NOT NULL DEFAULT 0.0,
    confidence_rating   INTEGER,            -- 1-5 scale, NULL if not asked
    hint_used           INTEGER NOT NULL DEFAULT 0,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS flashcard_attempts (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      INTEGER NOT NULL REFERENCES study_sessions(id),
    user_id         INTEGER NOT NULL REFERENCES users(id),
    flashcard_id    INTEGER NOT NULL REFERENCES flashcards(id),
    rating          INTEGER NOT NULL,       -- 1=Again, 2=Hard, 3=Good, 4=Easy
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- FSRS (Free Spaced Repetition Scheduler)
-- ============================================================

CREATE TABLE IF NOT EXISTS fsrs_cards (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL REFERENCES users(id),
    content_type    TEXT NOT NULL,          -- 'question', 'flashcard'
    content_id      INTEGER NOT NULL,
    stability       REAL NOT NULL DEFAULT 1.0,
    difficulty      REAL NOT NULL DEFAULT 0.3,
    retrievability  REAL NOT NULL DEFAULT 1.0,
    due_date        DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_review     DATETIME,
    state           TEXT NOT NULL DEFAULT 'new',  -- new/learning/review/relearning
    step            INTEGER NOT NULL DEFAULT 0,   -- learning step index
    reps            INTEGER NOT NULL DEFAULT 0,
    lapses          INTEGER NOT NULL DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, content_type, content_id)
);

CREATE TABLE IF NOT EXISTS fsrs_reviews (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    card_id     INTEGER NOT NULL REFERENCES fsrs_cards(id),
    rating      INTEGER NOT NULL,           -- 1=Again, 2=Hard, 3=Good, 4=Easy
    stability   REAL NOT NULL,
    difficulty  REAL NOT NULL,
    retrievability REAL NOT NULL,
    interval_days REAL NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- BKT (Bayesian Knowledge Tracing)
-- ============================================================

CREATE TABLE IF NOT EXISTS bkt_skill_states (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id),
    skill_id    INTEGER NOT NULL,           -- domain_id or topic_id
    skill_type  TEXT NOT NULL,              -- 'domain' or 'topic'
    p_mastery   REAL NOT NULL DEFAULT 0.1,  -- P(mastered)
    p_learn     REAL NOT NULL DEFAULT 0.3,  -- P(learn per attempt)
    p_guess     REAL NOT NULL DEFAULT 0.2,  -- P(correct | not mastered)
    p_slip      REAL NOT NULL DEFAULT 0.1,  -- P(incorrect | mastered)
    attempts    INTEGER NOT NULL DEFAULT 0,
    correct     INTEGER NOT NULL DEFAULT 0,
    theta       REAL NOT NULL DEFAULT 0.0,  -- IRT ability estimate
    accuracy_pct REAL NOT NULL DEFAULT 0.0,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, skill_id, skill_type)
);

-- ============================================================
-- ANALYTICS
-- ============================================================

CREATE TABLE IF NOT EXISTS daily_progress (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL REFERENCES users(id),
    date            TEXT NOT NULL,          -- YYYY-MM-DD
    questions_seen  INTEGER NOT NULL DEFAULT 0,
    questions_correct INTEGER NOT NULL DEFAULT 0,
    study_minutes   INTEGER NOT NULL DEFAULT 0,
    domains_studied TEXT NOT NULL DEFAULT '', -- JSON array
    UNIQUE(user_id, date)
);

CREATE TABLE IF NOT EXISTS predicted_scores (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER NOT NULL REFERENCES users(id),
    d1_accuracy      REAL NOT NULL DEFAULT 0.0,
    d2_accuracy      REAL NOT NULL DEFAULT 0.0,
    d3_accuracy      REAL NOT NULL DEFAULT 0.0,
    d4_accuracy      REAL NOT NULL DEFAULT 0.0,
    d5_accuracy      REAL NOT NULL DEFAULT 0.0,
    predicted_score  INTEGER NOT NULL DEFAULT 0,
    pass_probability REAL NOT NULL DEFAULT 0.0,
    certification_id INTEGER REFERENCES certifications(id),
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- GOALS
-- ============================================================

CREATE TABLE IF NOT EXISTS user_goals (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id             INTEGER NOT NULL REFERENCES users(id),
    certification_id    INTEGER NOT NULL REFERENCES certifications(id),
    exam_date           DATE NOT NULL,          -- YYYY-MM-DD
    target_hours        INTEGER NOT NULL DEFAULT 40,
    created_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at          DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, certification_id)
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_questions_domain ON questions(domain_id);
CREATE INDEX IF NOT EXISTS idx_fsrs_cards_user_due ON fsrs_cards(user_id, due_date);
CREATE INDEX IF NOT EXISTS idx_fsrs_cards_state ON fsrs_cards(user_id, state);
CREATE INDEX IF NOT EXISTS idx_attempts_user ON question_attempts(user_id);
CREATE INDEX IF NOT EXISTS idx_attempts_question ON question_attempts(question_id);
CREATE INDEX IF NOT EXISTS idx_bkt_user_skill ON bkt_skill_states(user_id, skill_type);
CREATE INDEX IF NOT EXISTS idx_ai_cache ON ai_explanations(content_type, content_id, explanation_type);
