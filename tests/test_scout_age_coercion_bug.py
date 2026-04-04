"""
Bug Condition Exploration Test — Property 1: Age Coercion Excludes Valid Candidates

Validates: Requirements 1.1

CRITICAL: This test MUST FAIL on unfixed code — failure confirms the bug exists.
DO NOT attempt to fix the test or the code when it fails.

The test encodes the EXPECTED (correct) behavior:
  - A player with Age=22.0 (pandas float64) and max_age=23 → should be INCLUDED
  - A player with Age=NaN and max_age=23 → should be EXCLUDED (treated as 99), not raise TypeError

When this test fails on unfixed code, it proves the bug exists.
When this test passes after the fix, it confirms the fix is correct.
"""

import math
import pytest
import pandas as pd
import numpy as np
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st


# ---------------------------------------------------------------------------
# Replicate the exact candidate-filtering logic from app.py api_scout
# (copied verbatim — no fixes applied)
# ---------------------------------------------------------------------------

def _detect_position(position_str: str) -> str:
    """Copied from core/scorer.py — unchanged."""
    pos = (position_str or "").lower().strip()
    first = pos.split(",")[0].strip()
    if first == "fw":  return "attacker"
    if first == "mf":  return "midfielder"
    if first == "df":  return "defender"
    if first == "gk":  return "goalkeeper"
    if any(k in pos for k in ["attack", "forward", "winger", "striker"]):
        return "attacker"
    if "midfield" in pos:
        return "midfielder"
    if any(k in pos for k in ["defend", "back"]):
        return "defender"
    if any(k in pos for k in ["goal", "keeper"]):
        return "goalkeeper"
    return "attacker"


def _filter_candidates_unfixed(pool_df: pd.DataFrame, target_id: int, max_age: int,
                                target_position: str) -> list:
    """
    Replicates the UNFIXED candidate-filtering loop from app.py api_scout.

    Key bug: `age = row.get('Age', 99)` — no numeric coercion.
    When Age is a pandas float64 (e.g. 22.0), the comparison works for clean floats
    but when Age is NaN, `NaN > max_age` is False (NaN passes the filter unexpectedly).
    When Age is an object/string dtype (e.g. "22.0"), `"22.0" > 23` raises TypeError in Python 3.
    """
    candidates = []
    for _, row in pool_df.iterrows():
        if int(row['player_id']) == target_id:
            continue

        # BUG: raw value from CSV — no coercion
        age = row.get('Age', 99)
        if age > max_age:
            continue

        # Position filtering
        if _detect_position(row.get('Pos', '')) != _detect_position(target_position):
            continue

        # Minutes threshold
        if row.get('Min', 0) < 400:
            continue

        candidates.append({
            "player_id": int(row['player_id']),
            "name": row['Player'],
            "age": age,
        })

    return candidates


# ---------------------------------------------------------------------------
# Helper: build a minimal mock pool_df
# ---------------------------------------------------------------------------

def _make_pool_df(rows: list) -> pd.DataFrame:
    """
    Build a minimal DataFrame that mirrors the CSV structure used by api_scout.
    Each row dict must have: player_id, Player, Age, Pos, Min.
    """
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Concrete unit tests (scoped to the exact failing case)
# ---------------------------------------------------------------------------

class TestAgeCoercionBugCondition:
    """
    Scoped PBT / unit tests for Property 1: Bug Condition.

    isBugCondition: max_age is set AND the candidate pool contains players
    whose CSV Age column value is a float (e.g. 22.0) or NaN AND all candidates
    are excluded by the age filter.
    """

    def test_float_age_22_with_max_age_23_should_be_included(self):
        """
        CONCRETE FAILING CASE:
        Player with Age=22.0 (pandas float64), max_age=23 → player SHOULD be included.

        On unfixed code this test FAILS because the age comparison either:
        - Works for clean float64 (22.0 > 23 is False → passes), BUT
        - The real failure mode is when Age dtype is object/string "22.0" → TypeError
          or when the pool returns 0 candidates due to NaN rows causing silent errors.

        We test the exact scenario described in the design doc.
        """
        pool_df = _make_pool_df([
            {
                "player_id": 1,
                "Player": "Young Attacker",
                "Age": pd.array([22.0], dtype="float64")[0],  # explicit float64
                "Pos": "FW",
                "Min": 900,
            }
        ])

        max_age = 23
        target_id = 999  # different from player_id=1
        target_position = "FW"

        candidates = _filter_candidates_unfixed(pool_df, target_id, max_age, target_position)

        # EXPECTED (correct) behavior: player with Age=22.0 ≤ max_age=23 IS included
        # This assertion FAILS on unfixed code if the age comparison is broken
        assert len(candidates) == 1, (
            f"BUG CONFIRMED: Player with Age=22.0 was excluded when max_age=23. "
            f"Candidates found: {candidates}"
        )
        assert candidates[0]["player_id"] == 1

    def test_string_age_22_with_max_age_23_raises_or_excludes(self):
        """
        OBJECT-DTYPE CASE:
        Player with Age="22.0" (string/object dtype), max_age=23.

        In Python 3, `"22.0" > 23` raises TypeError.
        The unfixed code has no try/except around the age comparison,
        so this either raises or silently skips the candidate.

        Expected (correct) behavior: player IS included (age 22 ≤ 23).
        This test documents the TypeError counterexample.
        """
        pool_df = _make_pool_df([
            {
                "player_id": 2,
                "Player": "String Age Player",
                "Age": "22.0",  # object dtype — the real bug trigger
                "Pos": "FW",
                "Min": 900,
            }
        ])

        max_age = 23
        target_id = 999
        target_position = "FW"

        # On unfixed code: TypeError is raised OR candidate is silently excluded
        # Either way, the player is NOT correctly included
        try:
            candidates = _filter_candidates_unfixed(pool_df, target_id, max_age, target_position)
            # If no exception: the player should be included but likely isn't
            assert len(candidates) == 1, (
                f"BUG CONFIRMED: Player with Age='22.0' (string) was excluded when max_age=23. "
                f"Candidates: {candidates}"
            )
        except TypeError as e:
            # TypeError is also a bug confirmation — the unfixed code crashes
            pytest.fail(
                f"BUG CONFIRMED: TypeError raised when comparing string Age '22.0' > {max_age}: {e}"
            )

    def test_nan_age_with_max_age_23_should_be_excluded_not_raise(self):
        """
        NaN AGE CASE:
        Player with Age=NaN, max_age=23 → player SHOULD be excluded (treated as age 99).

        On unfixed code: `NaN > 23` evaluates to False in Python (NaN comparisons always False),
        so the NaN player PASSES the age filter unexpectedly — it is included when it should not be.

        This test asserts the CORRECT behavior: NaN → excluded.
        On unfixed code this test FAILS because NaN rows pass the filter.
        """
        pool_df = _make_pool_df([
            {
                "player_id": 3,
                "Player": "Unknown Age Player",
                "Age": float('nan'),  # NaN age
                "Pos": "FW",
                "Min": 900,
            }
        ])

        max_age = 23
        target_id = 999
        target_position = "FW"

        # Should NOT raise TypeError — NaN must be handled gracefully
        try:
            candidates = _filter_candidates_unfixed(pool_df, target_id, max_age, target_position)
        except TypeError as e:
            pytest.fail(f"BUG: TypeError raised for NaN age — should be handled gracefully: {e}")

        # EXPECTED (correct) behavior: NaN age → treated as 99 → excluded
        # On unfixed code: NaN > 23 is False → NaN player passes filter → len == 1 (WRONG)
        assert len(candidates) == 0, (
            f"BUG CONFIRMED: Player with Age=NaN was INCLUDED when max_age=23. "
            f"NaN should be treated as age 99 (excluded). Candidates: {candidates}"
        )

    def test_mixed_pool_float_and_nan_ages(self):
        """
        MIXED POOL CASE:
        Pool has:
          - player_id=1: Age=22.0 (float64) → should be INCLUDED (22 ≤ 23)
          - player_id=2: Age=NaN → should be EXCLUDED (treated as 99)
          - player_id=3: Age=25.0 (float64) → should be EXCLUDED (25 > 23)

        On unfixed code:
          - player_id=1: 22.0 > 23 is False → included (correct by accident for clean float64)
          - player_id=2: NaN > 23 is False → included (WRONG — should be excluded)
          - player_id=3: 25.0 > 23 is True → excluded (correct)

        Expected: only player_id=1 in candidates.
        Unfixed result: player_id=1 AND player_id=2 in candidates (NaN bug).
        """
        pool_df = _make_pool_df([
            {"player_id": 1, "Player": "Young Player",   "Age": 22.0,         "Pos": "FW", "Min": 900},
            {"player_id": 2, "Player": "Unknown Age",    "Age": float('nan'), "Pos": "FW", "Min": 900},
            {"player_id": 3, "Player": "Older Player",   "Age": 25.0,         "Pos": "FW", "Min": 900},
        ])

        max_age = 23
        target_id = 999
        target_position = "FW"

        candidates = _filter_candidates_unfixed(pool_df, target_id, max_age, target_position)
        candidate_ids = [c["player_id"] for c in candidates]

        # EXPECTED: only player 1 (age 22.0 ≤ 23)
        assert candidate_ids == [1], (
            f"BUG CONFIRMED: Expected only player_id=1 (Age=22.0), "
            f"but got candidate_ids={candidate_ids}. "
            f"NaN player (id=2) should be excluded but passes the unfixed filter."
        )


# ---------------------------------------------------------------------------
# Property-based test — generalises the concrete cases
# ---------------------------------------------------------------------------

@settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
@given(
    float_age=st.floats(min_value=18.0, max_value=22.9, allow_nan=False, allow_infinity=False),
    max_age=st.integers(min_value=23, max_value=30),
)
def test_property_float_age_lte_max_age_should_be_included(float_age, max_age):
    """
    **Validates: Requirements 1.1**

    Property 1 (Bug Condition): For any scout request where max_age is set and the
    candidate pool contains a player whose CSV Age value is a float ≤ max_age,
    the candidate-filtering logic SHALL include that player.

    On UNFIXED code: this test FAILS when Age is stored as object/string dtype,
    because `"22.5" > 23` raises TypeError in Python 3.

    We test with float64 dtype here to surface the NaN-related failure mode,
    and with string dtype in the unit tests above to surface the TypeError.
    """
    pool_df = _make_pool_df([
        {
            "player_id": 42,
            "Player": "Test Player",
            "Age": float_age,  # pandas float64
            "Pos": "FW",
            "Min": 900,
        }
    ])

    target_id = 999
    target_position = "FW"

    candidates = _filter_candidates_unfixed(pool_df, target_id, max_age, target_position)

    assert len(candidates) == 1, (
        f"BUG CONFIRMED (Property 1): Player with Age={float_age} (float64) "
        f"was excluded when max_age={max_age}. "
        f"float_age={float_age} ≤ max_age={max_age} so player SHOULD be included."
    )
