"""Integration tests: two exams coexist in same DB without bleeding into each other."""

from __future__ import annotations

import pytest
from sqlalchemy import text

from cert_pepper.db.connection import get_session
from cert_pepper.db.exams import resolve_cert_id
from cert_pepper.engine.selector import select_question, select_exam_questions
from cert_pepper.engine.scorer import get_domain_accuracies, get_weak_areas, predict_score

from tests.conftest import (
    get_cert_id,
    get_user_id,
    seed_attempt,
    seed_certification,
    seed_domains_for_cert,
    seed_question,
    seed_session,
)


# ---------------------------------------------------------------------------
# Setup helpers
# ---------------------------------------------------------------------------

async def setup_two_exams(session):
    """
    Seed two certifications (SY0-701 already exists) + a second one.
    Returns (cert_a_id, cert_b_id).
    """
    cert_a_id = await get_cert_id(session, "SY0-701")

    cert_b_id = await seed_certification(session, "MULTI-B", "Multi Exam B", "Vendor B")
    await seed_domains_for_cert(
        session,
        cert_b_id,
        [
            (1, "B Domain One", 50.0),
            (2, "B Domain Two", 50.0),
        ],
    )
    return cert_a_id, cert_b_id


# ---------------------------------------------------------------------------
# DB isolation
# ---------------------------------------------------------------------------

class TestMultiExamDbIsolation:
    async def test_two_certs_have_separate_domains(self, db):
        """Each certification has its own set of domains."""
        async with get_session() as session:
            cert_a_id, cert_b_id = await setup_two_exams(session)
            await session.commit()

        async with get_session() as session:
            result = await session.execute(
                text("SELECT COUNT(*) FROM domains WHERE certification_id = :cid"),
                {"cid": cert_a_id},
            )
            a_count = result.scalar()

            result = await session.execute(
                text("SELECT COUNT(*) FROM domains WHERE certification_id = :cid"),
                {"cid": cert_b_id},
            )
            b_count = result.scalar()

        assert a_count == 5  # SY0-701 has 5 domains
        assert b_count == 2

    async def test_resolve_cert_id_with_two_certs_requires_code(self, db):
        """With 2 certs in DB, resolve_cert_id(None) raises an error."""
        async with get_session() as session:
            cert_a_id, cert_b_id = await setup_two_exams(session)
            await session.commit()

        async with get_session() as session:
            with pytest.raises(ValueError, match="Multiple exams"):
                await resolve_cert_id(session)

    async def test_resolve_cert_id_by_code_works_with_two_certs(self, db):
        """With 2 certs in DB, resolve_cert_id('MULTI-B') returns the correct id."""
        async with get_session() as session:
            cert_a_id, cert_b_id = await setup_two_exams(session)
            await session.commit()

        async with get_session() as session:
            result = await resolve_cert_id(session, "MULTI-B")
        assert result == cert_b_id


# ---------------------------------------------------------------------------
# Question isolation
# ---------------------------------------------------------------------------

class TestQuestionIsolation:
    async def test_select_question_only_returns_own_cert(self, db):
        """Selecting from cert A never returns cert B questions."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_a_id, cert_b_id = await setup_two_exams(session)

            # 3 questions in cert A domain 4
            a_ids = set()
            for n in range(1, 4):
                a_ids.add(await seed_question(session, domain_number=4, number=n, cert_id=cert_a_id))

            # 3 questions in cert B domain 1
            b_ids = set()
            for n in range(1, 4):
                b_ids.add(await seed_question(session, domain_number=1, number=n, cert_id=cert_b_id))

            await session.commit()

        # Repeatedly select from cert A — must always get cert A questions
        for _ in range(10):
            async with get_session() as session:
                user_id = await get_user_id(session)
                q_id = await select_question(session, user_id, cert_id=cert_a_id)
            assert q_id in a_ids, f"Expected cert A question, got {q_id}"

    async def test_select_exam_questions_scoped_to_cert(self, db):
        """select_exam_questions returns only questions from the specified cert."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_a_id, cert_b_id = await setup_two_exams(session)

            # 5 questions in cert B (domains 1 and 2)
            b_ids = set()
            for n in range(1, 4):
                b_ids.add(await seed_question(session, domain_number=1, number=n, cert_id=cert_b_id))
            for n in range(4, 7):
                b_ids.add(await seed_question(session, domain_number=2, number=n, cert_id=cert_b_id))

            # 5 questions in cert A domain 4
            a_ids = set()
            for n in range(1, 6):
                a_ids.add(await seed_question(session, domain_number=4, number=n, cert_id=cert_a_id))

            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            b_exam_qs = await select_exam_questions(session, user_id, total=10, cert_id=cert_b_id)

        assert len(b_exam_qs) > 0
        for q_id in b_exam_qs:
            assert q_id in b_ids, f"Cert B exam returned cert A question {q_id}"


# ---------------------------------------------------------------------------
# Analytics isolation
# ---------------------------------------------------------------------------

class TestAnalyticsIsolation:
    async def test_accuracies_do_not_bleed_across_certs(self, db):
        """Attempts on cert B questions don't show up in cert A analytics."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_a_id, cert_b_id = await setup_two_exams(session)

            sess_id = await seed_session(session, user_id)

            # Perfect score in cert B domain 1
            for n in range(1, 4):
                b_q = await seed_question(session, domain_number=1, number=n, cert_id=cert_b_id)
                await seed_attempt(session, user_id, b_q, sess_id, is_correct=True)

            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_a_id = await get_cert_id(session, "SY0-701")
            a_accs = await get_domain_accuracies(session, user_id, cert_id=cert_a_id)

        # Cert A should show zero attempts
        assert a_accs == {}

    async def test_weak_areas_per_cert_are_independent(self, db):
        """get_weak_areas for cert A shows cert A domains; cert B domains are independent."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_a_id, cert_b_id = await setup_two_exams(session)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_b_weak = await get_weak_areas(session, user_id, cert_id=cert_b_id)

        # Cert B has 2 domains, both unattempted
        assert len(cert_b_weak) == 2
        assert all(d.domain_number in {1, 2} for d in cert_b_weak)

    async def test_predict_score_uses_correct_cert_weights(self, db):
        """predict_score for cert B uses cert B's domain weights, not cert A's."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_a_id, cert_b_id = await setup_two_exams(session)

            sess_id = await seed_session(session, user_id)
            b_q = await seed_question(session, domain_number=1, cert_id=cert_b_id, number=1)
            await seed_attempt(session, user_id, b_q, sess_id, is_correct=True)
            await session.commit()

        async with get_session() as session:
            user_id = await get_user_id(session)
            score = await predict_score(session, user_id, cert_id=cert_b_id)

        # Cert B has 2 domains (weights 0.5, 0.5); domain 1 at 100%, domain 2 at 0%
        # weighted = 1.0 * 0.5 + 0.0 * 0.5 = 0.5 → predicted_score = 450
        assert score.predicted_score == 450
        assert set(score.domain_weights.keys()) == {1, 2}


# ---------------------------------------------------------------------------
# Session scoping
# ---------------------------------------------------------------------------

class TestSessionScoping:
    async def test_study_session_stores_certification_id(self, db):
        """INSERT into study_sessions with certification_id persists correctly."""
        async with get_session() as session:
            user_id = await get_user_id(session)
            cert_a_id = await get_cert_id(session, "SY0-701")

            await session.execute(
                text(
                    "INSERT INTO study_sessions (user_id, session_type, certification_id) "
                    "VALUES (:uid, 'study', :cid)"
                ),
                {"uid": user_id, "cid": cert_a_id},
            )
            result = await session.execute(text("SELECT last_insert_rowid()"))
            sess_id = result.scalar()
            await session.commit()

        async with get_session() as session:
            from cert_pepper.db.exams import get_cert_id_for_session
            stored = await get_cert_id_for_session(session, sess_id)

        assert stored == cert_a_id
