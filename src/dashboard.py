"""MarketPulse - interactive Dash dashboard (TD11).

Run from the repository root:  python src/dashboard.py
Then open http://127.0.0.1:8050
"""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import plotly.graph_objects as go  # noqa: E402
from dash import Dash, Input, Output, dcc, html  # noqa: E402

from src.main import build_market_snapshot  # noqa: E402


THEMES = {
    "dark": {
        "page_bg": "#0b0f19",
        "container_bg": "#111827",
        "card_bg": "#1e293b",
        "text_primary": "#f8fafc",
        "text_secondary": "#94a3b8",
        "text_muted": "#64748b",
        "border": "#334155",
        "card_border": "1px solid #334155",
        "card_shadow": "0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5)",
        "plot_template": "plotly_dark",
        "chart_bg": "#1e293b",
        "btn_bg": "#1e293b",
        "btn_border": "1px solid #475569",
        "btn_color": "#f8fafc",
        "btn_text": "☀️ Light Mode",
        "badge_bg": "rgba(34, 197, 94, 0.15)",
        "badge_border": "1px solid rgba(34, 197, 94, 0.4)",
        "badge_color": "#4ade80",
    },
    "light": {
        "page_bg": "#f8fafc",
        "container_bg": "#ffffff",
        "card_bg": "#ffffff",
        "text_primary": "#0f172a",
        "text_secondary": "#64748b",
        "text_muted": "#94a3b8",
        "border": "#e2e8f0",
        "card_border": "1px solid #e2e8f0",
        "card_shadow": "0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05)",
        "plot_template": "plotly_white",
        "chart_bg": "#ffffff",
        "btn_bg": "#f1f5f9",
        "btn_border": "1px solid #cbd5e1",
        "btn_color": "#0f172a",
        "btn_text": "🌙 Dark Mode",
        "badge_bg": "rgba(22, 163, 74, 0.1)",
        "badge_border": "1px solid rgba(22, 163, 74, 0.25)",
        "badge_color": "#16a34a",
    },
}




def create_base_100_figure(snapshot, is_dark=True):
    """
    Generate the Base 100 comparative chart for instrument and benchmark.
    
    Args:
        snapshot (dict): Application snapshot from build_market_snapshot().
        is_dark (bool): When True, applies Dark Mode palette.
        
    Returns:
        go.Figure: Interactive Plotly figure.
    """
    inst_series = snapshot["instrument_base_100"]
    bm_series = snapshot["benchmark_base_100"]

    inst_ticker = snapshot["instrument"]["ticker"]
    inst_name = snapshot["instrument"]["name"]
    bm_ticker = snapshot["benchmark"]["ticker"]
    bm_name = snapshot["benchmark"]["name"]

    dates = [row["date"] for row in inst_series]
    inst_values = [row["value"] for row in inst_series]
    bm_values = [row["value"] for row in bm_series]

    fig = go.Figure()

    inst_color = "#38bdf8" if is_dark else "#2563eb"
    bm_color = "#f43f5e" if is_dark else "#dc2626"
    line_ref_color = "#64748b" if is_dark else "#94a3b8"

    # Instrument line
    fig.add_trace(go.Scatter(
        x=dates,
        y=inst_values,
        mode="lines+markers",
        name=f"{inst_ticker} ({inst_name})",
        line=dict(color=inst_color, width=3),
        marker=dict(size=6, color=inst_color),
    ))

    # Benchmark line
    fig.add_trace(go.Scatter(
        x=dates,
        y=bm_values,
        mode="lines+markers",
        name=f"{bm_ticker} ({bm_name})",
        line=dict(color=bm_color, width=2, dash="dash"),
        marker=dict(size=5, color=bm_color),
    ))

    # Base 100 Reference Line
    fig.add_hline(
        y=100.0,
        line_width=1,
        line_dash="dot",
        line_color=line_ref_color,
        annotation_text="Base 100 (Origin)",
        annotation_position="bottom right",
        annotation_font=dict(color=line_ref_color, size=11),
    )

    theme_cfg = THEMES["dark" if is_dark else "light"]
    bg_color = theme_cfg["chart_bg"]
    text_color = theme_cfg["text_primary"]
    grid_color = "#334155" if is_dark else "#f1f5f9"

    fig.update_layout(
        title=dict(
            text="Normalized Relative Performance (Base 100)",
            font=dict(size=18, color=text_color, family="Segoe UI, Inter, -apple-system, sans-serif"),
        ),
        xaxis=dict(
            title="Trading Date",
            gridcolor=grid_color,
            color=text_color,
            showline=True,
            linecolor=grid_color,
        ),
        yaxis=dict(
            title="Base 100 Level",
            gridcolor=grid_color,
            color=text_color,
            showline=True,
            linecolor=grid_color,
        ),
        template=theme_cfg["plot_template"],
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        font=dict(color=text_color, family="Segoe UI, Inter, -apple-system, sans-serif"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=text_color),
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        hovermode="x unified",
    )

    return fig




def render_header(snapshot, is_dark):
    t = THEMES["dark" if is_dark else "light"]
    return html.Div(
        style={
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "borderBottom": f"2px solid {t['border']}",
            "paddingBottom": "20px",
            "marginBottom": "28px",
            "flexWrap": "wrap",
            "gap": "16px",
        },
        children=[
            html.Div(
                children=[
                    html.Div(
                        style={"display": "flex", "alignItems": "center", "gap": "12px", "marginBottom": "8px"},
                        children=[
                            html.H1(
                                "MarketPulse Dashboard",
                                style={"margin": "0", "color": t["text_primary"], "fontSize": "28px", "fontWeight": "800"},
                            ),
                            html.Span(
                                "CONNECTED",
                                style={
                                    "backgroundColor": t["badge_bg"],
                                    "border": t["badge_border"],
                                    "color": t["badge_color"],
                                    "fontSize": "11px",
                                    "fontWeight": "700",
                                    "padding": "3px 8px",
                                    "borderRadius": "12px",
                                    "letterSpacing": "0.5px",
                                },
                            ),
                        ],
                    ),
                    html.Div(
                        style={"display": "flex", "gap": "20px", "color": t["text_secondary"], "fontSize": "14px", "flexWrap": "wrap"},
                        children=[
                            html.Span(f"Provider: {snapshot['provider']}"),
                            html.Span(f"Lookback: {snapshot['lookback']}"),
                            html.Span(f"Interval: {snapshot['interval']}"),
                        ],
                    ),
                ]
            ),
            html.Button(
                t["btn_text"],
                id="theme-toggle-btn",
                n_clicks=1,
                style={
                    "backgroundColor": t["btn_bg"],
                    "color": t["btn_color"],
                    "border": t["btn_border"],
                    "padding": "10px 18px",
                    "borderRadius": "8px",
                    "cursor": "pointer",
                    "fontWeight": "600",
                    "fontSize": "14px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "transition": "all 0.2s ease-in-out",
                },
            ),
        ],
    )


def render_kpis(snapshot, is_dark):
    t = THEMES["dark" if is_dark else "light"]
    inst_return = snapshot["instrument_return"]
    bm_return = snapshot["benchmark_return"]
    rel_perf = snapshot["relative_performance"]

    inst_color = "#38bdf8" if is_dark else "#2563eb"
    bm_color = "#f43f5e" if is_dark else "#dc2626"
    rel_color = "#4ade80" if rel_perf >= 0 else "#f87171"

    card_common = {
        "backgroundColor": t["card_bg"],
        "padding": "22px",
        "borderRadius": "10px",
        "boxShadow": t["card_shadow"],
        "border": t["card_border"],
        "transition": "all 0.3s ease",
    }

    return html.Div(
        style={
            "display": "grid",
            "gridTemplateColumns": "repeat(auto-fit, minmax(280px, 1fr))",
            "gap": "22px",
            "marginBottom": "32px",
        },
        children=[
            # KPI Instrument
            html.Div(
                style={**card_common, "borderLeft": f"5px solid {inst_color}"},
                children=[
                    html.Div("SELECTED INSTRUMENT", style={"fontSize": "12px", "color": t["text_secondary"], "fontWeight": "700", "letterSpacing": "0.5px"}),
                    html.H3(f"{snapshot['instrument']['ticker']} - {snapshot['instrument']['name']}", style={"margin": "8px 0 14px 0", "color": t["text_primary"], "fontSize": "18px"}),
                    html.Div(
                        f"{inst_return:+.2f}%",
                        style={"fontSize": "32px", "fontWeight": "800", "color": inst_color},
                    ),
                    html.Div("Period return", style={"fontSize": "12px", "color": t["text_muted"], "marginTop": "4px"}),
                ],
            ),

            # KPI Benchmark
            html.Div(
                style={**card_common, "borderLeft": f"5px solid {bm_color}"},
                children=[
                    html.Div("BENCHMARK INDEX", style={"fontSize": "12px", "color": t["text_secondary"], "fontWeight": "700", "letterSpacing": "0.5px"}),
                    html.H3(f"{snapshot['benchmark']['ticker']} - {snapshot['benchmark']['name']}", style={"margin": "8px 0 14px 0", "color": t["text_primary"], "fontSize": "18px"}),
                    html.Div(
                        f"{bm_return:+.2f}%",
                        style={"fontSize": "32px", "fontWeight": "800", "color": bm_color},
                    ),
                    html.Div("Period return", style={"fontSize": "12px", "color": t["text_muted"], "marginTop": "4px"}),
                ],
            ),

            # KPI Relative Performance
            html.Div(
                style={**card_common, "borderLeft": f"5px solid {rel_color}"},
                children=[
                    html.Div("RELATIVE PERFORMANCE", style={"fontSize": "12px", "color": t["text_secondary"], "fontWeight": "700", "letterSpacing": "0.5px"}),
                    html.H3(f"{snapshot['instrument']['ticker']} vs {snapshot['benchmark']['ticker']}", style={"margin": "8px 0 14px 0", "color": t["text_primary"], "fontSize": "18px"}),
                    html.Div(
                        f"{rel_perf:+.2f} pts",
                        style={"fontSize": "32px", "fontWeight": "800", "color": rel_color},
                    ),
                    html.Div("Arithmetic difference (percentage points)", style={"fontSize": "12px", "color": t["text_muted"], "marginTop": "4px"}),
                ],
            ),
        ],
    )



def create_app():
    """Initialize Dash application with interactive dynamic Dark Mode."""
    snapshot = build_market_snapshot()

    app = Dash(__name__, title="MarketPulse Dashboard")

    app.layout = html.Div(
        id="page-wrapper",
        style={
            "fontFamily": "Segoe UI, Inter, -apple-system, sans-serif",
            "backgroundColor": THEMES["dark"]["page_bg"],
            "minHeight": "100vh",
            "padding": "36px 20px",
            "transition": "background-color 0.3s ease",
        },
        children=[
            html.Div(
                style={"maxWidth": "1200px", "margin": "0 auto"},
                children=[
                    html.Div(id="header-container", children=render_header(snapshot, is_dark=True)),
                    html.Div(id="kpis-container", children=render_kpis(snapshot, is_dark=True)),
                    html.Div(
                        id="chart-card",
                        style={
                            "backgroundColor": THEMES["dark"]["card_bg"],
                            "padding": "24px",
                            "borderRadius": "10px",
                            "boxShadow": THEMES["dark"]["card_shadow"],
                            "border": THEMES["dark"]["card_border"],
                            "transition": "all 0.3s ease",
                        },
                        children=[
                            dcc.Graph(
                                id="base-100-comparison-chart",
                                figure=create_base_100_figure(snapshot, is_dark=True),
                                config={"displayModeBar": False},
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )

    @app.callback(
        Output("page-wrapper", "style"),
        Output("header-container", "children"),
        Output("kpis-container", "children"),
        Output("chart-card", "style"),
        Output("base-100-comparison-chart", "figure"),
        Input("theme-toggle-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_theme(n_clicks):
        is_dark = (n_clicks % 2 == 1)
        t = THEMES["dark" if is_dark else "light"]

        page_style = {
            "fontFamily": "Segoe UI, Inter, -apple-system, sans-serif",
            "backgroundColor": t["page_bg"],
            "minHeight": "100vh",
            "padding": "36px 20px",
            "transition": "background-color 0.3s ease",
        }

        header_ui = render_header(snapshot, is_dark)
        kpis_ui = render_kpis(snapshot, is_dark)

        chart_card_style = {
            "backgroundColor": t["card_bg"],
            "padding": "24px",
            "borderRadius": "10px",
            "boxShadow": t["card_shadow"],
            "border": t["card_border"],
            "transition": "all 0.3s ease",
        }

        fig = create_base_100_figure(snapshot, is_dark=is_dark)

        return page_style, header_ui, kpis_ui, chart_card_style, fig

    return app


def main():
    app = create_app()
    print("MarketPulse Dashboard ready on http://127.0.0.1:8050")
    app.run(debug=False, host="127.0.0.1", port=8050)


if __name__ == "__main__":
    main()
