"""Tests for ai/prompts.py and the pure helpers in ai/client.py.

Covers:
  - prompts.py: get_explainer_system (domain lookup, fallback, suffix inclusion)
  - prompts.py: get_hint_system (constant content)
  - client.py: make_prompt_hash (deterministic, unique, 16-char hex)

No API calls are made — all tested functions are pure.
"""

from __future__ import annotations

import pytest

from cert_pepper.ai.prompts import (
    DOMAIN_CONTEXT,
    EXPLAINER_SUFFIX,
    HINT_SYSTEM,
    get_explainer_system,
    get_hint_system,
)
from cert_pepper.ai.client import make_prompt_hash


# ---------------------------------------------------------------------------
# get_explainer_system
# ---------------------------------------------------------------------------

class TestGetExplainerSystem:
    def test_returns_string(self):
        result = get_explainer_system(1)
        assert isinstance(result, str)

    def test_contains_domain_context_for_domain_1(self):
        result = get_explainer_system(1)
        assert DOMAIN_CONTEXT[1] in result

    def test_contains_domain_context_for_domain_4(self):
        result = get_explainer_system(4)
        assert DOMAIN_CONTEXT[4] in result

    def test_contains_explainer_suffix(self):
        for domain in range(1, 6):
            result = get_explainer_system(domain)
            assert EXPLAINER_SUFFIX in result, f"EXPLAINER_SUFFIX missing for domain {domain}"

    def test_unknown_domain_falls_back_to_domain_1(self):
        result = get_explainer_system(99)
        assert DOMAIN_CONTEXT[1] in result

    def test_all_five_domains_have_distinct_context(self):
        prompts = [get_explainer_system(i) for i in range(1, 6)]
        # Each prompt should be unique because the domain contexts differ
        assert len(set(prompts)) == 5

    def test_domain_2_mentions_threats(self):
        result = get_explainer_system(2)
        assert "threat" in result.lower() or "malware" in result.lower()

    def test_domain_4_mentions_highest_weight(self):
        result = get_explainer_system(4)
        assert "28%" in result or "highest weight" in result.lower()

    def test_suffix_appended_after_context(self):
        result = get_explainer_system(1)
        context_end = result.index(EXPLAINER_SUFFIX)
        domain_end = result.index(DOMAIN_CONTEXT[1]) + len(DOMAIN_CONTEXT[1])
        assert context_end > domain_end


# ---------------------------------------------------------------------------
# get_hint_system
# ---------------------------------------------------------------------------

class TestGetHintSystem:
    def test_returns_string(self):
        assert isinstance(get_hint_system(), str)

    def test_returns_hint_system_constant(self):
        assert get_hint_system() == HINT_SYSTEM

    def test_result_is_non_empty(self):
        assert len(get_hint_system()) > 0

    def test_idempotent(self):
        assert get_hint_system() == get_hint_system()


# ---------------------------------------------------------------------------
# make_prompt_hash
# ---------------------------------------------------------------------------

class TestMakePromptHash:
    def test_returns_string(self):
        result = make_prompt_hash("system", "user")
        assert isinstance(result, str)

    def test_length_is_16(self):
        result = make_prompt_hash("system text", "user text")
        assert len(result) == 16

    def test_only_hex_characters(self):
        result = make_prompt_hash("system text", "user text")
        assert all(c in "0123456789abcdef" for c in result)

    def test_deterministic(self):
        h1 = make_prompt_hash("same system", "same user")
        h2 = make_prompt_hash("same system", "same user")
        assert h1 == h2

    def test_different_system_gives_different_hash(self):
        h1 = make_prompt_hash("system A", "user")
        h2 = make_prompt_hash("system B", "user")
        assert h1 != h2

    def test_different_user_gives_different_hash(self):
        h1 = make_prompt_hash("system", "user A")
        h2 = make_prompt_hash("system", "user B")
        assert h1 != h2

    def test_swapping_system_and_user_gives_different_hash(self):
        # json.dumps with sort_keys ensures positional labels matter
        h1 = make_prompt_hash("text A", "text B")
        h2 = make_prompt_hash("text B", "text A")
        assert h1 != h2

    def test_empty_strings_produce_valid_hash(self):
        result = make_prompt_hash("", "")
        assert len(result) == 16

    def test_real_domain_prompt_produces_consistent_hash(self):
        system = get_explainer_system(4)
        user = "Q: Which protocol handles key exchange?\nSelected: A) TLS\nCorrect: B) IKE"
        h1 = make_prompt_hash(system, user)
        h2 = make_prompt_hash(system, user)
        assert h1 == h2
        assert len(h1) == 16
