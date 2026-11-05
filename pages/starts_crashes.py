from pathlib import Path

import pandas as pd
import plotly.express as px
import dash
from dash import Input, Output, State, callback, dcc, html

dash.register_page(
    __name__,
    path="/starts-crashes",
    name="Starts & Crashes",
)

data_path = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "integrated_housing_sirta_borough_month.csv"
)
df = pd.read_csv(data_path)

font_family = "Avenir Next, Arial, sans-serif"

card_style = {
    "backgroundColor": "#ffffff",
    "padding": "22px",
    "border": "1px solid #dce5ef",
    "borderRadius": "14px",
    "marginBottom": "20px",
    "boxShadow": "0 4px 16px rgba(20, 45, 78, 0.06)",
}

layout = html.Div(
    [
        html.H2(
            "Housing Starts & Street Crashes",
            style={
                "color": "#142d4e",
                "fontFamily": font_family,
                "fontSize": "30px",
                "marginTop": "0",
                "marginBottom": "8px",
            },
        ),
        html.P(
            "Explore how monthly affordable housing activity and SIRTA crash records vary across boroughs.",
            style={
                "color": "#53657b",
                "fontFamily": font_family,
                "fontSize": "16px",
                "lineHeight": "1.6",
                "marginTop": "0",
                "marginBottom": "24px",
            },
        ),

        html.Section(
            [
                html.H3(
                    "RQ1 · Housing starts and crash records",
                    style={"color": "#142d4e", "fontFamily": font_family},
                ),
                html.P(
                    "Are borough-months with more housing projects started associated with more recorded crashes? Each point represents one borough-month.",
                    style={"color": "#53657b", "fontFamily": font_family},
                ),
                dcc.Graph(
                    id="rq1-scatter",
                    config={"displaylogo": False, "scrollZoom": True},
                ),
            ],
            style=card_style,
        ),

        html.Section(
            [
                html.H3(
                    "RQ2 · Crash records by housing activity",
                    style={"color": "#142d4e", "fontFamily": font_family},
                ),
                html.P(
                    "Compare average crash records in months with starts only, completions only, both, or neither.",
                    style={"color": "#53657b", "fontFamily": font_family},
                ),
                dcc.Graph(
                    id="rq2-bar",
                    config={"displaylogo": False, "scrollZoom": True},
                ),
            ],
            style=card_style,
        ),
    ],
    style={"fontFamily": font_family},
)


@callback(
    Output("rq1-scatter", "figure"),
    Output("rq2-bar", "figure"),
    Input("generate-report", "n_clicks"),
    State("borough-filter", "value"),
    State("year-filter", "value"),
)
def update_starts_crashes(_clicks, selected_borough, selected_year):
    filtered = df.copy()

    if selected_borough:
        filtered = filtered[filtered["borough_key"] == selected_borough]

    if selected_year:
        filtered = filtered[filtered["year"] == selected_year]

    figure1 = px.scatter(
        filtered,
        x="housing_projects_started",
        y="crash_records",
        color="borough_key",
        hover_data=["year", "month"],
        color_discrete_sequence=px.colors.qualitative.Safe,
        labels={
            "housing_projects_started": "Housing projects started",
            "crash_records": "SIRTA crash records",
            "borough_key": "Borough",
        },
        title="Housing Starts and Crash Records by Borough-Month",
    )
    figure1.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font={"family": font_family, "color": "#25364d"},
        margin={"l": 55, "r": 25, "t": 65, "b": 50},
        legend_title_text="Borough",
    )

    q2_data = filtered.copy()
    started = q2_data["housing_projects_started"] > 0
    completed = q2_data["housing_projects_completed"] > 0

    q2_data["housing_activity"] = "Neither"
    q2_data.loc[started & ~completed, "housing_activity"] = "Starts only"
    q2_data.loc[~started & completed, "housing_activity"] = "Completions only"
    q2_data.loc[started & completed, "housing_activity"] = "Both"

    q2_summary = (
        q2_data.groupby(
            ["borough_key", "housing_activity"], as_index=False
        )["crash_records"]
        .mean()
    )

    figure2 = px.bar(
        q2_summary,
        x="borough_key",
        y="crash_records",
        color="housing_activity",
        barmode="group",
        category_orders={
            "housing_activity": [
                "Neither",
                "Starts only",
                "Completions only",
                "Both",
            ]
        },
        color_discrete_map={
            "Neither": "#9aa9ba",
            "Starts only": "#2b6cb0",
            "Completions only": "#d69e2e",
            "Both": "#142d4e",
        },
        labels={
            "borough_key": "Borough",
            "crash_records": "Average crash records per month",
            "housing_activity": "Housing activity",
        },
        title="Average Crash Records by Monthly Housing Activity",
    )
    figure2.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font={"family": font_family, "color": "#25364d"},
        margin={"l": 55, "r": 25, "t": 65, "b": 50},
        legend_title_text="Housing activity",
    )

    return figure1, figure2