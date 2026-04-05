"""
Smart insight generation.
Compares a player's per-90 stats to position-group averages from the CSV
and returns ranked natural-language insight strings.
"""

from core.normalizer import per_90

# Human-readable labels for each per-90 stat key
STAT_LABELS: dict[str, str] = {
    "goals_p90":               "goals",
    "assists_p90":             "assists",
    "shots_on_p90":            "shots on target",
    "xg_p90":                  "expected goals",
    "xag_p90":                 "expected assists",
    "key_passes_p90":          "key passes",
    "progressive_passes_p90":  "progressive passes",
    "tackles_p90":             "tackles",
    "interceptions_p90":       "interceptions",
    "clearances_p90":          "clearances",
    "dribbles_p90":            "dribbles",
    "progressive_carries_p90": "progressive carries",
    "fouls_drawn_p90":         "fouls drawn",
}

# Position-group labels for insight strings
_POS_LABELS: dict[str, str] = {
    "attacker":   "attacker",
    "midfielder": "midfielder",
    "defender":   "defender",
    "goalkeeper": "goalkeeper",
}

# Stats to generate insights for (subset of per-90 keys)
INSIGHT_STATS: list[str] = list(STAT_LABELS.keys())

# CSV column → raw cumulative stat name mapping (for per-90 computation)
_CSV_COL_MAP: dict[str, tuple[str, str]] = {
    # insight_stat_key: (csv_column, raw_key_for_per_90)
    "goals_p90":               ("Gls",    "goals"),
    "assists_p90":             ("Ast",    "assists"),
    "shots_on_p90":            ("SoT",    "shots_on"),
    "xg_p90":                  ("xG",     "xg"),
    "xag_p90":                 ("xAG",    "xag"),
    "key_passes_p90":          ("KP",     "passes_key"),
    "progressive_passes_p90":  ("PrgP",   "progressive_passes"),
    "tackles_p90":             ("Tkl",    "tackles"),
    "interceptions_p90":       ("Int",    "interceptions"),
    "clearances_p90":          ("Clr",    "clearances"),
    "dribbles_p90":            ("Succ",   "dribbles_success"),
    "progressive_carries_p90": ("PrgC",   "progressive_carries"),
    "fouls_drawn_p90":         ("Fld",    "fouls_drawn"),
}


def _pos_group(pos_str: str) -> str:
    """Map a position string to one of four canonical groups."""
    low = (pos_str or "").lower().strip()
    if low == "fw" or "," in low and low.split(",")[0].strip() == "fw":
        return "attacker"
    if low == "mf" or "," in low and low.split(",")[0].strip() == "mf":
        return "midfielder"
    if low == "df" or "," in low and low.split(",")[0].strip() == "df":
        return "defender"
    if low == "gk":
        return "goalkeeper"
    if any(k in low for k in ("attack", "forward", "winger", "striker")):
        return "attacker"
    if "midfield" in low:
        return "midfielder"
    if any(k in low for k in ("defend", "back")):
        return "defender"
    if any(k in low for k in ("goal", "keeper")):
        return "goalkeeper"
    return "attacker"


def _compute_group_averages(df, pos_group: str, season: str) -> dict[str, float]:
    """
    Filter df to pos_group + season rows with Min >= 450.
    Compute per-90 average for each stat in INSIGHT_STATS.
    Returns {} if fewer than 5 qualifying players.
    """
    import pandas as pd

    try:
        mask = df["season"] == season
        subset = df[mask].copy()

        # Filter by position group
        def _matches_group(pos_str):
            return _pos_group(str(pos_str)) == pos_group

        subset = subset[subset["Pos"].apply(_matches_group)]

        # Require minimum minutes
        def _safe_float(v):
            try:
                f = float(v)
                return f if not pd.isna(f) else 0.0
            except (TypeError, ValueError):
                return 0.0

        subset = subset[subset["Min"].apply(_safe_float) >= 450]

        if len(subset) < 5:
            return {}

        averages: dict[str, float] = {}
        for stat_key, (csv_col, _) in _CSV_COL_MAP.items():
            if csv_col not in subset.columns:
                continue
            vals = []
            for _, row in subset.iterrows():
                raw_val = _safe_float(row.get(csv_col, 0))
                mins    = _safe_float(row.get("Min", 0))
                p90_val = per_90(raw_val, int(mins)) if mins >= 1 else 0.0
                if p90_val > 0:
                    vals.append(p90_val)
            if vals:
                averages[stat_key] = round(sum(vals) / len(vals), 4)

        return averages
    except Exception:
        return {}


def generate_insights(norm: dict, league: str, season: str, position: str,
                      top_n: int = 3) -> list[str]:
    """
    Compare norm's per-90 stats to position-group averages.
    Returns up to top_n insight strings ranked by abs % diff.
    Returns [] on insufficient sample or any error.
    """
    try:
        from core.fetcher import _get_df
        df = _get_df()

        pos_group = _pos_group(position)
        pos_label = _POS_LABELS.get(pos_group, "player")

        # Normalize season format
        if "-" not in str(season):
            season = f"{season}-{str(int(season) + 1)[2:]}"

        averages = _compute_group_averages(df, pos_group, season)
        if not averages:
            return []

        candidates: list[tuple[float, str]] = []  # (abs_pct_diff, insight_string)

        for stat_key in INSIGHT_STATS:
            avg = averages.get(stat_key)
            if not avg or avg <= 0:
                continue
            player_val = float(norm.get(stat_key, 0) or 0)
            stat_label = STAT_LABELS[stat_key]

            pct_diff = (player_val - avg) / avg  # signed
            abs_diff = abs(pct_diff)

            if abs_diff <= 0.10:
                continue  # threshold: must differ by more than 10%

            if pct_diff > 0:
                ratio = player_val / avg
                if ratio >= 1.5:
                    insight = f"Scores {ratio:.1f}x the {stat_label} of an average {pos_label}"
                else:
                    insight = f"Creates {round(pct_diff * 100):.0f}% more {stat_label} than the average {pos_label}"
            else:
                insight = f"Below average in {stat_label} for a {pos_label}"

            candidates.append((abs_diff, insight))

        # Sort descending by absolute percentage difference
        candidates.sort(key=lambda x: x[0], reverse=True)
        return [ins for _, ins in candidates[:top_n]]

    except Exception:
        return []
