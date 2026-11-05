from pathlib import Path

import pandas as pd
import dash
from dash import Dash, Input, Output, State, dcc, html, no_update

from filter_utils import (
    HOUSING_ACTIVITIES,
    TRANSPORTATION_OUTCOMES,
    apply_filters,
    format_filter_summary,
    parse_search_query,
)

data_path = (
    Path(__file__).parent
    / "data"
    / "integrated_housing_sirta_borough_month.csv"
)
df = pd.read_csv(data_path)

app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
server = app.server
application = server

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

                html.Div(
                    [
                        html.Label("Search", style=label_style),
                        dcc.Input(
                            id="search-input",
                            type="search",
                            placeholder="e.g. Brooklyn 2022 new buildings",
                            debounce=True,
                            style={"width": "100%", "padding": "10px", "boxSizing": "border-box"},
                        ),
                        html.Small(id="search-status", style={"color": "#53657b"}),
                    ]
                ),

                html.Div(
                    [
                        html.Label("Housing activity", style=label_style),
                        dcc.Dropdown(
                            id="housing-filter",
                            options=[{"label": "All housing activity", "value": ""}]
                            + [{"label": value, "value": value} for value in HOUSING_ACTIVITIES],
                            value="",
                            clearable=False,
                        ),
                    ]
                ),

                html.Div(
                    [
                        html.Label("Transportation outcome", style=label_style),
                        dcc.Dropdown(
                            id="transportation-filter",
                            options=[{"label": "All transportation outcomes", "value": ""}]
                            + [{"label": value, "value": value} for value in TRANSPORTATION_OUTCOMES],
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
                "gridTemplateColumns": "repeat(auto-fit, minmax(min(220px, 100%), 1fr))",
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
        html.Div(id="report-summary"),
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

@app.callback(
    Output("borough-filter", "value"),
    Output("year-filter", "value"),
    Output("housing-filter", "value"),
    Output("transportation-filter", "value"),
    Output("search-status", "children"),
    Input("search-input", "value"),
)
def apply_search_query(query):
    parsed = parse_search_query(query)
    if not (query or "").strip():
        return no_update, no_update, no_update, no_update, ""
    recognized = [
        value
        for value in (
            parsed["borough"],
            parsed["year"],
            parsed["housing_activity"],
            parsed["transportation_outcome"],
        )
        if value is not None
    ]
    status = f"Recognized: {', '.join(map(str, recognized))}."
    if parsed["unrecognized_terms"]:
        status += " Unrecognized terms ignored: " + ", ".join(
            parsed["unrecognized_terms"]
        ) + "."
    if not recognized:
        status = "No supported borough, year, housing, or transportation terms recognized."
    return (
        parsed["borough"] or no_update,
        parsed["year"] or no_update,
        parsed["housing_activity"] or no_update,
        parsed["transportation_outcome"] or no_update,
        status,
    )


@app.callback(
    Output("report-summary", "children"),
    Input("generate-report", "n_clicks"),
    State("borough-filter", "value"),
    State("year-filter", "value"),
    State("housing-filter", "value"),
    State("transportation-filter", "value"),
    State("search-input", "value"),
)
def generate_report(_clicks, borough, year, housing, transportation, query):
    filtered, _ = apply_filters(
        df, borough, year, housing, transportation, query
    )
    criteria = format_filter_summary(
        borough, year, housing, transportation, query
    )
    if filtered.empty:
        message = "No matching borough-month records were found for " + criteria + "."
        return html.Div(message, style={"color": "#8a3b3b", "fontWeight": "600"})

    total_crashes = int(filtered["crash_records"].sum())
    total_injuries = int(
        (filtered["non_severe_injuries"] + filtered["severe_injuries"]).sum()
    )
    total_severe = int(filtered["severe_injuries"].sum())
    total_fatalities = int(filtered["fatalities"].sum())
    return html.Div(
        [
            html.H3("Results summary", style={"color": "#142d4e", "marginBottom": "8px"}),
            html.P(f"Applied filters: {criteria}."),
            html.P(f"{len(filtered)} borough-month records matched."),
            html.P(
                f"Housing: {int(filtered['housing_projects_started'].sum()):,} projects "
                f"started and {int(filtered['housing_projects_completed'].sum()):,} completed."
            ),
            html.P(
                f"Transportation: {total_crashes:,} crashes, {total_injuries:,} injuries "
                f"({total_severe:,} severe), and {total_fatalities:,} fatalities."
            ),
        ],
        style={
            "backgroundColor": "#ffffff",
            "border": "1px solid #dce5ef",
            "borderRadius": "14px",
            "padding": "18px 20px",
            "marginBottom": "22px",
            "color": "#53657b",
        },
    )


if __name__ == "__main__":
    app.run(debug=True)