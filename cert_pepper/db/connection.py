"""SQLAlchemy async engine and session factory."""

from pathlib import Path
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy import text

from cert_pepper.config import get_settings

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is None:
        settings = get_settings()
        _engine = create_async_engine(
            settings.db_url,
            echo=False,
            connect_args={"check_same_thread": False},
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            get_engine(),
            expire_on_commit=False,
            class_=AsyncSession,
        )
    return _session_factory


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


def _strip_sql_comments(sql: str) -> str:
    """Remove single-line SQL comments (-- ...) to avoid semicolon-in-comment bugs."""
    lines = []
    for line in sql.split("\n"):
        # Remove inline and full-line comments
        comment_idx = line.find("--")
        if comment_idx >= 0:
            line = line[:comment_idx]
        lines.append(line)
    return "\n".join(lines)


async def init_db() -> None:
    """Create all tables from schema.sql."""
    schema_path = Path(__file__).parent / "schema.sql"
    schema_sql = schema_path.read_text()

    # Strip comments before splitting on ; to avoid semicolons inside comments
    schema_sql = _strip_sql_comments(schema_sql)

    engine = get_engine()
    async with engine.begin() as conn:
        # Execute each statement separately
        statements = [s.strip() for s in schema_sql.split(";") if s.strip()]
        for stmt in statements:
            if not stmt:
                continue
            try:
                await conn.execute(text(stmt))
            except Exception as e:
                # Skip if already exists
                if "already exists" not in str(e).lower():
                    raise

    # Run migrations for existing DBs (idempotent — swallows duplicate column errors)
    await _run_migrations()

    # Seed the default certification and user
    await _seed_defaults()


async def _run_migrations() -> None:
    """Add new columns to existing tables. Idempotent: swallows duplicate column errors."""
    migrations = [
        "ALTER TABLE flashcards ADD COLUMN certification_id INTEGER REFERENCES certifications(id)",
        "ALTER TABLE acronyms ADD COLUMN certification_id INTEGER REFERENCES certifications(id)",
        "ALTER TABLE study_sessions ADD COLUMN certification_id INTEGER REFERENCES certifications(id)",
        "ALTER TABLE predicted_scores ADD COLUMN certification_id INTEGER REFERENCES certifications(id)",
    ]
    engine = get_engine()
    async with engine.begin() as conn:
        for stmt in migrations:
            try:
                await conn.execute(text(stmt))
            except Exception as e:
                if "duplicate column name" not in str(e).lower():
                    raise


async def _seed_defaults() -> None:
    """Insert default certification, domains, and user if not present."""
    async with get_session() as session:
        # Check if already seeded
        result = await session.execute(text("SELECT COUNT(*) FROM certifications"))
        count = result.scalar()
        if count and count > 0:
            return

        # Insert certification
        await session.execute(
            text(
                "INSERT OR IGNORE INTO certifications (code, name, vendor) "
                "VALUES ('SY0-701', 'CompTIA Security+', 'CompTIA')"
            )
        )

        # Get cert id
        result = await session.execute(
            text("SELECT id FROM certifications WHERE code='SY0-701'")
        )
        cert_id = result.scalar()

        # Insert domains
        domains = [
            (1, "General Security Concepts", 12.0),
            (2, "Threats, Vulnerabilities, and Mitigations", 22.0),
            (3, "Security Architecture", 18.0),
            (4, "Security Operations", 28.0),
            (5, "Program Management and Oversight", 20.0),
        ]
        for number, name, weight in domains:
            await session.execute(
                text(
                    "INSERT OR IGNORE INTO domains (certification_id, number, name, weight_pct) "
                    "VALUES (:cert_id, :number, :name, :weight)"
                ),
                {"cert_id": cert_id, "number": number, "name": name, "weight": weight},
            )

        # Insert default user
        await session.execute(
            text("INSERT OR IGNORE INTO users (username) VALUES ('default')")
        )
