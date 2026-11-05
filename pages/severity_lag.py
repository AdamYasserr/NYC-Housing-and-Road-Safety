from pathlib import Path

import pandas as pd
import plotly.express as px
import dash
from dash import Input, Output, State, callback, dcc, html

dash.register_page(
    __name__,
    path="/severity-lag",
    name="Severity & Next Month",
)

data_path = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "integrated_housing_sirta_borough_month.csv"
)
df = pd.read_csv(data_path)

# Compare each borough-month with that borough's median project starts.
borough_medians = df.groupby("borough_key")["housing_projects_started"].transform("median")
df["activity_group"] = "At/below borough median"
df.loc[
    df["housing_projects_started"] > borough_medians,
    "activity_group",
] = "Above borough median"

# Compare this month's starts to next month's crashes in the same borough.
df = df.sort_values(["borough_key", "year", "month"]).copy()
df["next_month_crashes"] = (
    df.groupby("borough_key")["crash_records"].shift(-1)
)

# Severe injuries per 100 crash records.
df["severe_injuries_per_100_crashes"] = (
    100 * df["severe_injuries"] / df["crash_records"]
).where(df["crash_records"] > 0)

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
            "Severity & Next-Month Patterns",
            style={
                "color": "#142d4e",
                "fontFamily": font_family,
                "fontSize": "30px",
                "marginTop": "0",
                "marginBottom": "8px",
            },
        ),
        html.P(
            "Compare injury severity during high- and lower-start months, "
            "and explore whether crash counts are higher in the month after more housing starts.",
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
                    "RQ7 · Injury severity and housing-start activity",
                    style={"color": "#142d4e", "fontFamily": font_family},
                ),
                html.P(
                    "High-start months are above that borough's median. Bars compare mean severe injuries per 100 crash records.",
                    style={"color": "#53657b", "fontFamily": font_family},
                ),
                dcc.Graph(
                    id="rq7-severity",
                    config={"displaylogo": False, "scrollZoom": True},
                ),
            ],
            style=card_style,
        ),

        html.Section(
            [
                html.H3(
                    "RQ8 · Housing starts and following-month crashes",
                    style={"color": "#142d4e", "fontFamily": font_family},
                ),
                html.P(
                    "Each point compares a borough-month's project starts with crash records in the following month in the same borough.",
                    style={"color": "#53657b", "fontFamily": font_family},
                ),
                dcc.Graph(
                    id="rq8-lag",
                    config={"displaylogo": False, "scrollZoom": True},
                ),
            ],
            style=card_style,
        ),
    ],
    style={"fontFamily": font_family},
)


@callback(
    Output("rq7-severity", "figure"),
    Output("rq8-lag", "figure"),
    Input("generate-report", "n_clicks"),
    State("borough-filter", "value"),
    State("year-filter", "value"),
)
def update_severity_lag(_clicks, selected_borough, selected_year):
    filtered = df.copy()

    if selected_borough:
        filtered = filtered[filtered["borough_key"] == selected_borough]

    if selected_year:
        filtered = filtered[filtered["year"] == selected_year]

    # RQ7: average severe injuries per 100 crash records.
    severity_summary = (
        filtered.groupby(
            ["borough_key", "activity_group"], as_index=False
        )["severe_injuries_per_100_crashes"]
        .mean()
    )

    figure7 = px.bar(
        severity_summary,
        x="borough_key",
        y="severe_injuries_per_100_crashes",
        color="activity_group",
        barmode="group",
        category_orders={
            "activity_group": [
                "At/below borough median",
                "Above borough median",
            ]
        },
        color_discrete_map={
            "At/below borough median": "#9aa9ba",
            "Above borough median": "#2878a5",
        },
        labels={
            "borough_key": "Borough",
            "severe_injuries_per_100_crashes": "Mean severe injuries per 100 crash records",
            "activity_group": "Housing-start activity",
        },
        title="Injury Severity by Housing-Start Activity",
    )
    figure7.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font={"family": font_family, "color": "#25364d"},
        margin={"l": 65, "r": 30, "t": 75, "b": 50},
        legend_title_text="Housing-start activity",
    )

    # RQ8: this month's project starts versus following-month crash records.
    lag_data = filtered.dropna(subset=["next_month_crashes"])

    figure8 = px.scatter(
        lag_data,
        x="housing_projects_started",
        y="next_month_crashes",
        color="borough_key",
        hover_data=["year", "month"],
        color_discrete_sequence=px.colors.qualitative.Safe,
        labels={
            "housing_projects_started": "Housing projects started this month",
            "next_month_crashes": "Crash records next month",
            "borough_key": "Borough",
        },
        title="Housing Starts and Following-Month Crash Records",
    )
    figure8.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font={"family": font_family, "color": "#25364d"},
        margin={"l": 65, "r": 30, "t": 75, "b": 50},
        legend_title_text="Borough",
    )

    return figure7, figure8