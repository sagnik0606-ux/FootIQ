"""
League difficulty adjustment.
Multiplies per-90 stats by a league coefficient to enable fair cross-league comparisons.
Ratio/percentage keys are left unchanged.
"""

COEFFICIENTS: dict[str, float] = {
    "Premier League": 1.00,
    "La Liga":        0.96,
    "Bundesliga":     0.93,
    "Serie A":        0.91,
    "Ligue 1":        0.85,
}

# Keys that are ratios/percentages — must NOT be scaled
_RATIO_KEYS = {"pass_accuracy", "aerial_win_pct", "tkl_pct", "sca90", "gca90"}


def get_coefficient(league: str) -> float:
    """Return the difficulty coefficient for a league; 1.00 for unknown leagues."""
    return COEFFICIENTS.get(league, 1.00)


def adjust_stat(value: float, league: str) -> float:
    """Return value * coefficient, rounded to 3 decimal places."""
    try:
        return round(float(value) * get_coefficient(league), 3)
    except (TypeError, ValueError):
        return 0.0


def adjust_norm(norm: dict, league: str) -> dict:
    """
    Return a copy of norm with all _p90 keys multiplied by the league coefficient.
    Ratio/percentage keys and non-numeric values are left unchanged.
    """
    coeff = get_coefficient(league)
    result = dict(norm)
    for key, val in norm.items():
        if key in _RATIO_KEYS:
            continue
        if key.endswith("_p90"):
            try:
                result[key] = round(float(val) * coeff, 3)
            except (TypeError, ValueError):
                result[key] = 0.0
    return result
