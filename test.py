# Retry: Create an HTML with two line charts next to each other (2-column layout)
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.io import to_html

# ============================
# THEMES
# ============================
LIGHT = {
    "page_bg": "#f5f5f5",
    "text": "#111827",
    "grid": "#E5E7EB",
    "plot_bg": "#ffffff",
    "paper_bg": "#ffffff",
}

DARK = {
    "page_bg": "#0B1220",
    "text": "#E5E7EB",
    "grid": "#2A3441",
    "plot_bg": "#0E1117",
    "paper_bg": "#0E1117",
}

# ============================
# SAMPLE DATA
# ============================
np.random.seed(1)

countries = ["Poland", "Germany"]
scenarios = ["a", "b", "c"]
dates = pd.date_range("2024-01-01", periods=60, freq="D")

rows = []
for country in countries:
    base = np.linspace(10, 25, len(dates)) + np.random.normal(0, 1.0, len(dates))
    for scen in scenarios:
        shift = {"a": 0, "b": 3, "c": -2}[scen]
        for d, v in zip(dates, base + shift):
            rows.append({
                "country": country,
                "date": d,
                "scenario": scen,
                "value": float(v)
            })

df = pd.DataFrame(rows)

# ============================
# APPLY THEME TO FIGURE
# ============================
def apply_theme(fig, theme):
    fig.update_layout(
        plot_bgcolor=theme["plot_bg"],
        paper_bgcolor=theme["paper_bg"],
        font=dict(color=theme["text"]),
        xaxis=dict(
            type="date",
            rangeslider=dict(visible=True),
            showgrid=True,
            gridcolor=theme["grid"],
            showline=False,
            ticks="",
            zeroline=False,
        ),
        yaxis=dict(
            title="Value",
            showgrid=True,
            gridcolor=theme["grid"],
            showline=False,
            ticks="",
            zeroline=False,
            fixedrange=False
        ),
        legend=dict(
            title="Scenario",
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=theme["text"]),
        ),
        margin=dict(l=30, r=20, t=60, b=40),
    )
    return fig

# ============================
# BUILD FIGURES (LIGHT + DARK)
# ============================
light_divs, dark_divs = [], []
include_js = True

for country, dff in df.groupby("country"):
    base_fig = px.line(
        dff,
        x="date",
        y="value",
        color="scenario",
        title=f"{country} — Scenarios a / b / c"
    )

    fig_light = apply_theme(base_fig, LIGHT)

    fig_dark_base = px.line(
        dff,
        x="date",
        y="value",
        color="scenario",
        title=f"{country} — Scenarios a / b / c"
    )
    fig_dark = apply_theme(fig_dark_base, DARK)

    light_divs.append(to_html(
        fig_light,
        full_html=False,
        include_plotlyjs="cdn" if include_js else False
    ))
    include_js = False

    dark_divs.append(to_html(
        fig_dark,
        full_html=False,
        include_plotlyjs=False
    ))

# ============================
# FINAL HTML (NO FRAMES)
# ============================
html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Country Scenario Charts</title>

<style>
  :root {{
    --page-bg: {LIGHT["page_bg"]};
    --text: {LIGHT["text"]};
  }}

  body {{
    margin: 0;
    padding: 20px;
    font-family: Arial, sans-serif;
    background: var(--page-bg);
    color: var(--text);
    transition: background 0.2s ease, color 0.2s ease;
  }}

  h1 {{
    text-align: center;
    margin-bottom: 20px;
  }}

  .grid {{
    max-width: 1400px;
    margin: auto;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
  }}

  @media (max-width: 1100px) {{
    .grid {{
      grid-template-columns: 1fr;
    }}
  }}

  /* NO FRAMES */
  .plot-wrapper {{
    padding: 0;
    margin: 0;
  }}

  .theme-light .plot-dark {{ display: none; }}
  .theme-dark .plot-light {{ display: none; }}

  /* VISIBLE TOGGLE BUTTON */
  .theme-toggle {{
    position: fixed;
    top: 18px;
    right: 22px;
    z-index: 9999;
    padding: 10px 16px;
    border-radius: 999px;
    border: 2px solid rgba(0,0,0,0.3);
    font-weight: 600;
    cursor: pointer;
    background: #ffffff;
    color: #111827;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  }}

  .theme-dark .theme-toggle {{
    background: #111827;
    color: #f9fafb;
    border-color: rgba(255,255,255,0.35);
  }}
</style>
</head>

<body class="theme-light" id="page">

<button class="theme-toggle" id="toggleBtn">🌙 Dark Mode</button>

<h1>Country Scenario Line Charts</h1>

<div class="grid">
  <div class="plot-wrapper">
    <div class="plot-light">{light_divs[0]}</div>
    <div class="plot-dark">{dark_divs[0]}</div>
  </div>

  <div class="plot-wrapper">
    <div class="plot-light">{light_divs[1]}</div>
    <div class="plot-dark">{dark_divs[1]}</div>
  </div>
</div>

<script>
  const page = document.getElementById("page");
  const btn = document.getElementById("toggleBtn");

  const LIGHT = {{
    bg: "{LIGHT["page_bg"]}",
    text: "{LIGHT["text"]}"
  }};

  const DARK = {{
    bg: "{DARK["page_bg"]}",
    text: "{DARK["text"]}"
  }};

  function applyTheme(mode) {{
    const t = mode === "dark" ? DARK : LIGHT;
    document.documentElement.style.setProperty("--page-bg", t.bg);
    document.documentElement.style.setProperty("--text", t.text);
    btn.innerHTML = mode === "dark" ? "☀️ Light Mode" : "🌙 Dark Mode";
  }}

  applyTheme("light");

  btn.onclick = () => {{
    if (page.classList.contains("theme-light")) {{
      page.classList.remove("theme-light");
      page.classList.add("theme-dark");
      applyTheme("dark");
    }} else {{
      page.classList.remove("theme-dark");
      page.classList.add("theme-light");
      applyTheme("light");
    }}
  }};
</script>

</body>
</html>
"""

# ============================
# SAVE FILE
# ============================
output_path = "final_borderless_light_dark_dashboard.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved:", output_path)
