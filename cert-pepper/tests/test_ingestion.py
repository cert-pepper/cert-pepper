"""Tests for markdown ingestion pipeline."""

from __future__ import annotations

from pathlib import Path
import textwrap

import pytest

from cert_pepper.ingestion.questions import parse_questions_file, parse_all_questions
from cert_pepper.ingestion.flashcards import parse_flashcards
from cert_pepper.ingestion.acronyms import parse_acronyms


# ===========================================================
# Fixtures: synthetic markdown content
# ===========================================================

@pytest.fixture
def questions_file(tmp_path: Path) -> Path:
    content = textwrap.dedent("""\
        # Domain 1 Practice Questions

        ---

        **Q1.** What does CIA stand for?

        A) Confidentiality, Integrity, Availability
        B) Control, Integrity, Access
        C) Confidentiality, Information, Access
        D) Control, Information, Availability

        <details><summary>Answer</summary>

        **A) Confidentiality, Integrity, Availability**

        The CIA triad is the foundation of security: keeping data secret (C), unaltered (I), and accessible (A).

        </details>

        ---

        **Q2.** Which protocol provides real-time certificate revocation status?

        A) CRL
        B) OCSP
        C) CSR
        D) CA

        <details><summary>Answer</summary>

        **B) OCSP**

        OCSP provides real-time status. CRL is a periodically updated list.

        </details>

        ---
    """)
    path = tmp_path / "domain1-practice.md"
    path.write_text(content)
    return path


@pytest.fixture
def flashcards_file(tmp_path: Path) -> Path:
    content = textwrap.dedent("""\
        # Security+ Flashcards

        ## CIA Triad
        **Confidentiality** → Only authorized users can access data | C = Can't see
        **Integrity** → Data hasn't been altered | I = Intact
        **Availability** → Systems accessible when needed | A = Always up

        ## Attack Types
        **Phishing** → Mass email impersonating trusted source
        **Spear phishing** → Targeted phishing (specific individual)
    """)
    path = tmp_path / "key-concepts.md"
    path.write_text(content)
    return path


@pytest.fixture
def acronyms_file(tmp_path: Path) -> Path:
    content = textwrap.dedent("""\
        # Security+ Master Acronym List

        ## Authentication & Access
        | Acronym | Full Term |
        |---------|-----------|
        | AAA | Authentication, Authorization, Accounting |
        | ACL | Access Control List |
        | MFA | Multi-Factor Authentication |

        ## Cryptography & PKI
        | Acronym | Full Term |
        |---------|-----------|
        | AES | Advanced Encryption Standard |
        | RSA | Rivest-Shamir-Adleman |
        | TLS | Transport Layer Security |
    """)
    path = tmp_path / "acronyms.md"
    path.write_text(content)
    return path


# ===========================================================
# Question tests
# ===========================================================

class TestQuestionsParser:
    def test_parses_correct_count(self, questions_file: Path):
        questions = parse_questions_file(questions_file)
        assert len(questions) == 2

    def test_correct_domain_number(self, questions_file: Path):
        questions = parse_questions_file(questions_file)
        assert all(q.domain_number == 1 for q in questions)

    def test_correct_question_numbers(self, questions_file: Path):
        questions = parse_questions_file(questions_file)
        assert [q.number for q in questions] == [1, 2]

    def test_stem_parsed(self, questions_file: Path):
        questions = parse_questions_file(questions_file)
        assert "CIA" in questions[0].stem

    def test_options_parsed(self, questions_file: Path):
        questions = parse_questions_file(questions_file)
        q = questions[0]
        assert q.option_a != ""
        assert q.option_b != ""
        assert q.option_c != ""
        assert q.option_d != ""

    def test_correct_answer(self, questions_file: Path):
        questions = parse_questions_file(questions_file)
        assert questions[0].correct_answer == "A"
        assert questions[1].correct_answer == "B"

    def test_explanation_parsed(self, questions_file: Path):
        questions = parse_questions_file(questions_file)
        assert "CIA triad" in questions[0].explanation

    def test_source_file(self, questions_file: Path):
        questions = parse_questions_file(questions_file)
        assert questions[0].source_file == "domain1-practice.md"

    def test_bad_domain_filename_raises(self, tmp_path: Path):
        bad = tmp_path / "practice.md"
        bad.write_text("# Practice\n---\n**Q1.** Stem\nA) a\nB) b\nC) c\nD) d\n")
        with pytest.raises(ValueError, match="Cannot determine domain number"):
            parse_questions_file(bad)

    def test_parse_all_multiple_files(self, tmp_path: Path):
        for domain in [1, 2, 3]:
            content = textwrap.dedent(f"""\
                # Domain {domain}
                ---
                **Q1.** Question for domain {domain}?
                A) Option A
                B) Option B
                C) Option C
                D) Option D
                <details><summary>Answer</summary>
                **A) Option A**
                Explanation here.
                </details>
                ---
            """)
            (tmp_path / f"domain{domain}-practice.md").write_text(content)

        all_q = parse_all_questions(tmp_path)
        assert len(all_q) == 3
        domain_nums = {q.domain_number for q in all_q}
        assert domain_nums == {1, 2, 3}


# ===========================================================
# Flashcard tests
# ===========================================================

class TestFlashcardsParser:
    def test_parses_correct_count(self, flashcards_file: Path):
        cards = parse_flashcards(flashcards_file)
        assert len(cards) == 5

    def test_category_assigned(self, flashcards_file: Path):
        cards = parse_flashcards(flashcards_file)
        cia_cards = [c for c in cards if c.category == "CIA Triad"]
        assert len(cia_cards) == 3

    def test_front_back_parsed(self, flashcards_file: Path):
        cards = parse_flashcards(flashcards_file)
        confidentiality = next(c for c in cards if c.front == "Confidentiality")
        assert "authorized users" in confidentiality.back

    def test_tip_parsed(self, flashcards_file: Path):
        cards = parse_flashcards(flashcards_file)
        confidentiality = next(c for c in cards if c.front == "Confidentiality")
        assert confidentiality.tip == "C = Can't see"

    def test_no_tip_empty_string(self, flashcards_file: Path):
        cards = parse_flashcards(flashcards_file)
        phishing = next(c for c in cards if c.front == "Phishing")
        assert phishing.tip == ""


# ===========================================================
# Acronym tests
# ===========================================================

class TestAcronymsParser:
    def test_parses_correct_count(self, acronyms_file: Path):
        acronyms = parse_acronyms(acronyms_file)
        assert len(acronyms) == 6

    def test_acronym_parsed(self, acronyms_file: Path):
        acronyms = parse_acronyms(acronyms_file)
        aaa = next(a for a in acronyms if a.acronym == "AAA")
        assert "Authentication" in aaa.full_term

    def test_category_assigned(self, acronyms_file: Path):
        acronyms = parse_acronyms(acronyms_file)
        aes = next(a for a in acronyms if a.acronym == "AES")
        assert aes.category == "Cryptography & PKI"

    def test_no_header_rows(self, acronyms_file: Path):
        acronyms = parse_acronyms(acronyms_file)
        assert all(a.acronym.lower() not in ("acronym", "term") for a in acronyms)


# ===========================================================
# Real files integration tests (skipped if not found)
# ===========================================================

REPO_ROOT = Path(__file__).parent.parent.parent  # security-plus/


@pytest.mark.skipif(
    not (REPO_ROOT / "practice-questions" / "domain1-practice.md").exists(),
    reason="Real practice questions not found",
)
def test_real_questions_parse():
    q = parse_all_questions(REPO_ROOT / "practice-questions")
    assert len(q) >= 30, f"Expected at least 30 questions, got {len(q)}"
    assert all(q_.correct_answer in "ABCD" for q_ in q)


@pytest.mark.skipif(
    not (REPO_ROOT / "acronyms.md").exists(),
    reason="Real acronyms.md not found",
)
def test_real_acronyms_parse():
    acronyms = parse_acronyms(REPO_ROOT / "acronyms.md")
    assert len(acronyms) >= 50, f"Expected at least 50 acronyms, got {len(acronyms)}"


@pytest.mark.skipif(
    not (REPO_ROOT / "flashcards" / "key-concepts.md").exists(),
    reason="Real flashcards not found",
)
def test_real_flashcards_parse():
    cards = parse_flashcards(REPO_ROOT / "flashcards" / "key-concepts.md")
    assert len(cards) >= 20, f"Expected at least 20 flashcards, got {len(cards)}"
