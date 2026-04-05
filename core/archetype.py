"""
Playstyle archetype classification.
Maps the five get_archetype_scores bucket values to one of seven named archetypes.
Rules are applied in priority order — first match wins.
"""

VALID_ARCHETYPES = {
    "🎯 Finisher",
    "🧠 Playmaker",
    "🚀 Ball Carrier",
    "🛡️ Defensive Midfielder",
    "🏰 Defender",
    "🦅 Complete Forward",
    "⚙️ Box-to-Box",
}


def classify(scores: dict) -> str:
    """
    Accept five archetype bucket scores (Attack, Creation, Progression, Technical, Defense)
    each in [0, 1] and return exactly one archetype label string.

    Rules applied in priority order (first match wins):
      1. 🎯 Finisher          — Attack == max AND Creation < 0.40
      2. 🧠 Playmaker         — Creation == max AND Progression > 0.45 AND Attack < 0.40
      3. 🚀 Ball Carrier      — Progression == max AND 0.25 <= Attack <= 0.65
      4. 🛡️ Defensive MF     — Defense == max AND Technical > 0.40 AND Attack < 0.35
      5. 🏰 Defender          — Defense == max AND Attack < 0.25 AND Creation < 0.25
      6. 🦅 Complete Forward  — Attack > 0.55 AND Creation > 0.45
      7. ⚙️ Box-to-Box        — fallback
    """
    attack      = float(scores.get("Attack",      0) or 0)
    creation    = float(scores.get("Creation",    0) or 0)
    progression = float(scores.get("Progression", 0) or 0)
    technical   = float(scores.get("Technical",   0) or 0)
    defense     = float(scores.get("Defense",     0) or 0)

    max_score = max(attack, creation, progression, technical, defense)

    # Rule 1 — Finisher
    if attack == max_score and creation < 0.40:
        return "🎯 Finisher"

    # Rule 2 — Playmaker
    if creation == max_score and progression > 0.45 and attack < 0.40:
        return "🧠 Playmaker"

    # Rule 3 — Ball Carrier
    if progression == max_score and 0.25 <= attack <= 0.65:
        return "🚀 Ball Carrier"

    # Rule 4 — Defensive Midfielder
    if defense == max_score and technical > 0.40 and attack < 0.35:
        return "🛡️ Defensive Midfielder"

    # Rule 5 — Defender
    if defense == max_score and attack < 0.25 and creation < 0.25:
        return "🏰 Defender"

    # Rule 6 — Complete Forward
    if attack > 0.55 and creation > 0.45:
        return "🦅 Complete Forward"

    # Rule 7 — Box-to-Box (fallback)
    return "⚙️ Box-to-Box"
