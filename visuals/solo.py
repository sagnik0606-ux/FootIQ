"""
Solo player visualizations:
  generate_solo_radar  — filled radar vs benchmark max
  generate_solo_lollipop — horizontal lollipop showing each stat vs benchmark
Returns base64 PNG strings.
"""
import io, base64
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from core.scorer import get_position_config

BG_DARK  = "#0a0e1a"
BG_PANEL = "#111827"
GRID_COL = "#1f2937"


def _fig_to_b64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight",
                facecolor=fig.get_facecolor(), dpi=140)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)
    return encoded


def _pct_color(pct: float) -> str:
    stops = [
        (0.00, (239, 68,  68)),
        (0.25, (249, 115, 22)),
        (0.50, (234, 179,  8)),
        (0.75, ( 34, 197, 94)),
        (1.00, ( 59, 130,246)),
    ]
    pct = max(0.0, min(1.0, pct))
    for i in range(len(stops) - 1):
        t0, c0 = stops[i];  t1, c1 = stops[i + 1]
        if t0 <= pct <= t1:
            a = (pct - t0) / (t1 - t0)
            r = int(c0[0] + a*(c1[0]-c0[0]))
            g = int(c0[1] + a*(c1[1]-c0[1]))
            b = int(c0[2] + a*(c1[2]-c0[2]))
            return f"#{r:02x}{g:02x}{b:02x}"
    return "#3b82f6"


def generate_solo_radar(norm: dict, name: str, color_override: str = None) -> str:
    config   = get_position_config(norm.get("position", "Attacker"))
    labels   = config["labels"]
    metrics  = config["metrics"]
    max_vals = config["max_vals"]

    vals   = [min((norm.get(m, 0) or 0) / mv, 1.0) if mv > 0 else 0.0
              for m, mv in zip(metrics, max_vals)]
    N      = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    v_plot = vals + [vals[0]]
    a_plot = angles + [angles[0]]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"polar": True}, facecolor=BG_DARK)
    ax.set_facecolor(BG_PANEL)

    # Benchmark (max) ring
    ax.fill(a_plot, [1.0] * (N + 1), color="#1e2535", alpha=1.0, zorder=1)
    # Player area
    main_col = color_override if color_override else "#3b82f6"
    ax.fill(a_plot, v_plot, color=main_col, alpha=0.25, zorder=3)
    ax.plot(a_plot, v_plot, color=main_col, linewidth=2.5, zorder=4)
    ax.scatter(angles, vals, color=main_col, s=70, zorder=5)

    ax.set_xticks(angles)
    ax.set_xticklabels(labels, color="#e2e8f0", fontsize=9.5, fontweight="bold")
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["25%", "50%", "75%", "Elite"], color="#4b5563", fontsize=7)
    ax.grid(color=GRID_COL, linewidth=0.8)
    ax.spines["polar"].set_color(GRID_COL)

    fig.suptitle(f"{name} — Performance Radar", color="white",
                 fontsize=13, fontweight="bold", y=1.02)
    return _fig_to_b64(fig)


def generate_archetype_radar(norm: dict, name: str, color_override: str = None) -> str:
    from core.scorer import get_archetype_scores
    scores_dict = get_archetype_scores(norm)
    
    labels  = list(scores_dict.keys())
    values  = list(scores_dict.values())
    N       = len(labels)
    
    angles  = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    v_plot  = values + [values[0]]
    a_plot  = angles + [angles[0]]
    
    # BRAND THEME
    MAIN_COL = color_override if color_override else "#f59e0b" # Amber-500 or custom hex
    
    # Increase figsize and use polar
    # Uniform 8x8 figure for professional scaling
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"polar": True}, facecolor=BG_DARK)
    ax.set_facecolor(BG_PANEL)
    
    # Background rings
    ax.fill(a_plot, [1.0] * (N + 1), color="#1e2535", alpha=1.0, zorder=1)
    
    # Player Area
    ax.fill(a_plot, v_plot, color=MAIN_COL, alpha=0.35, zorder=3)
    ax.plot(a_plot, v_plot, color=MAIN_COL, linewidth=3.5, zorder=4)
    ax.scatter(angles, values, color=MAIN_COL, s=100, zorder=5, 
               edgecolors="white", linewidths=1.2)
    
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, color="#fde68a", fontsize=12, fontweight="bold")
    
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["", "", "", ""], color="#4b5563")
    
    ax.grid(color=GRID_COL, linewidth=1.2)
    ax.spines["polar"].set_color(GRID_COL)
    
    # Unified scout report headings with absolute centering
    fig.suptitle(f"{name}", color="white", fontsize=22, fontweight="bold", y=0.98)
    fig.text(0.5, 0.89, "Tactical Profile Archetype", color="#94a3b8", fontsize=11, 
             ha="center", fontweight="bold")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    return _fig_to_b64(fig)
