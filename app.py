from pathlib import Path

import pandas as pd
import dash
from dash import Dash, dcc, html

data_path = (
    Path(__file__).parent
    / "data"
    / "integrated_housing_sirta_borough_month.csv"
)
df = pd.read_csv(data_path)

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
server = app.server

link_style = {
    "display": "inline-block",
    "padding": "10px 14px",
    "margin": "4px",
    "borderRadius": "8px",
    "backgroundColor": "#eef3f8",
    "color": "#142d4e",
    "textDecoration": "none",
    "fontFamily": "Avenir Next, Arial, sans-serif",
    "fontWeight": "600",
    "fontSize": "14px",
}

label_style = {
    "display": "block",
    "marginBottom": "7px",
    "color": "#253b59",
    "fontFamily": "Avenir Next, Arial, sans-serif",
    "fontWeight": "600",
    "fontSize": "14px",
}

app.layout = html.Div(
    [
        html.Header(
            [
                html.P(
                    "NYC DATA STORY  |  2022–2025",
                    style={
                        "margin": "0 0 8px",
                        "color": "#c5d5e8",
                        "fontSize": "12px",
                        "fontWeight": "700",
                        "letterSpacing": "1.5px",
                    },
                ),
                html.H1(
                    "Affordable Housing and Street Safety",
                    style={
                        "margin": "0",
                        "color": "#ffffff",
                        "fontSize": "clamp(28px, 4vw, 40px)",
                        "fontWeight": "700",
                    },
                ),
                html.P(
                    "Explore borough-level patterns in affordable housing, crashes, injuries, and fatalities.",
                    style={
                        "margin": "10px 0 0",
                        "color": "#e1eaf3",
                        "fontSize": "16px",
                        "lineHeight": "1.5",
                    },
                ),
            ],
            style={
                "backgroundColor": "#142d4e",
                "padding": "30px 34px",
                "borderRadius": "16px",
                "marginBottom": "18px",
                "fontFamily": "Avenir Next, Arial, sans-serif",
                "boxShadow": "0 8px 24px rgba(20, 45, 78, 0.14)",
            },
        ),

        html.Nav(
            [
                dcc.Link("Our Story", href="/our-story", style=link_style),
                dcc.Link("Data & Filters", href="/", style=link_style),
                dcc.Link("Starts & Crashes", href="/starts-crashes", style=link_style),
                dcc.Link("Trends & Seasons", href="/trends-seasons", style=link_style),
                dcc.Link("Injuries & Fatalities", href="/units-fatalities", style=link_style),
                dcc.Link("Severity & Next Month", href="/severity-lag", style=link_style),
            ],
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "gap": "6px",
                "backgroundColor": "#ffffff",
                "padding": "10px",
                "borderRadius": "12px",
                "marginBottom": "18px",
                "boxShadow": "0 3px 12px rgba(20, 45, 78, 0.06)",
            },
        ),

        html.Section(
            [
                html.Div(
                    [
                        html.Label("Borough", style=label_style),
                        dcc.Dropdown(
                            id="borough-filter",
                            options=[
                                {"label": "All boroughs", "value": ""},
                                *[
                                    {"label": borough, "value": borough}
                                    for borough in sorted(df["borough_key"].unique())
                                ],
                            ],
                            value="",
                            clearable=False,
                        ),
                    ]
                ),

                html.Div(
                    [
                        html.Label("Year", style=label_style),
                        dcc.Dropdown(
                            id="year-filter",
                            options=[
                                {"label": "All years", "value": ""},
                                *[
                                    {"label": str(year), "value": int(year)}
                                    for year in sorted(df["year"].unique())
                                ],
                            ],
                            value="",
                            clearable=False,
                        ),
                    ]
                ),

                html.Button(
                    "Generate Report",
                    id="generate-report",
                    n_clicks=0,
                    style={
                        "backgroundColor": "#142d4e",
                        "color": "#ffffff",
                        "border": "none",
                        "borderRadius": "8px",
                        "padding": "12px 20px",
                        "fontSize": "15px",
                        "fontWeight": "700",
                        "cursor": "pointer",
                        "fontFamily": "Avenir Next, Arial, sans-serif",
                    },
                ),
            ],
            style={
                "display": "grid",
                "gridTemplateColumns": "minmax(220px, 1fr) minmax(180px, 0.7fr) auto",
                "gap": "18px",
                "alignItems": "end",
                "backgroundColor": "#ffffff",
                "padding": "20px",
                "border": "1px solid #dce5ef",
                "borderRadius": "14px",
                "marginBottom": "22px",
                "boxShadow": "0 4px 16px rgba(20, 45, 78, 0.06)",
            },
        ),

        html.Main(dash.page_container),
    ],
    style={
        "maxWidth": "1500px",
        "minHeight": "100vh",
        "margin": "0 auto",
        "padding": "28px",
        "backgroundColor": "#f3f6fa",
        "fontFamily": "Avenir Next, Arial, sans-serif",
        "color": "#25364d",
    },
)

if __name__ == "__main__":
    app.run(debug=True)