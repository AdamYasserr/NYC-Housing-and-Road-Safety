from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Input, Output, State, callback, dcc, html
from filter_utils import apply_filters
from plotly.subplots import make_subplots

dash.register_page(
    __name__,
    path="/trends-seasons",
    name="Trends & Seasons",
)

data_path = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "integrated_housing_sirta_borough_month.csv"
)
df = pd.read_csv(data_path)

df["date"] = pd.to_datetime(df["year_month"], format="%Y-%m")

# Define high-start months relative to each borough's median across all years.
borough_medians = df.groupby("borough_key")["housing_projects_started"].transform("median")
df["high_start_activity"] = df["housing_projects_started"] > borough_medians

df["season"] = df["month"].map(
    {
        12: "Winter",
        1: "Winter",
        2: "Winter",
        6: "Summer",
        7: "Summer",
        8: "Summer",
    }
)

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
            "Trends & Seasons",
            style={
                "color": "#142d4e",
                "fontFamily": font_family,
                "fontSize": "30px",
                "marginTop": "0",
                "marginBottom": "8px",
            },
        ),
        html.P(
            "Explore monthly changes in housing completions and crash records, "
            "then compare summer and winter crash patterns during high-start months.",
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
                    "RQ3 · Monthly housing completions and crash records",
                    style={"color": "#142d4e", "fontFamily": font_family},
                ),
                html.P(
                    "Separate panels use separate scales for completed units and crash records.",
                    style={"color": "#53657b", "fontFamily": font_family},
                ),
                dcc.Graph(
                    id="rq3-trends",
                    config={"displaylogo": False, "scrollZoom": True},
                ),
            ],
            style=card_style,
        ),

        html.Section(
            [
                html.H3(
                    "RQ4 · Summer and winter during high-start months",
                    style={"color": "#142d4e", "fontFamily": font_family},
                ),
                html.P(
                    "A high-start month has project starts above that borough's median across the full dataset.",
                    style={"color": "#53657b", "fontFamily": font_family},
                ),
                dcc.Graph(
                    id="rq4-seasons",
                    config={"displaylogo": False, "scrollZoom": True},
                ),
            ],
            style=card_style,
        ),
    ],
    style={"fontFamily": font_family},
)


@callback(
    Output("rq3-trends", "figure"),
    Output("rq4-seasons", "figure"),
    Input("generate-report", "n_clicks"),
    State("borough-filter", "value"),
    State("year-filter", "value"),
    State("housing-filter", "value"),
    State("transportation-filter", "value"),
    State("search-input", "value"),
)
def update_trends_seasons(
    _clicks,
    selected_borough,
    selected_year,
    housing_activity,
    transportation_outcome,
    search_query,
):
    filtered, _ = apply_filters(
        df,
        selected_borough,
        selected_year,
        housing_activity,
        transportation_outcome,
        search_query,
    )

    monthly = (
        filtered.groupby("date", as_index=False)
        .agg(
            completed_units=("counted_units_in_projects_completed", "sum"),
            completed_projects=("housing_projects_completed", "sum"),
            crash_records=("crash_records", "sum"),
            severe_injuries=("severe_injuries", "sum"),
            non_severe_injuries=("non_severe_injuries", "sum"),
            fatalities=("fatalities", "sum"),
        )
        .sort_values("date")
    )

    figure3 = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.14,
        subplot_titles=(
            "Counted units in completed housing projects",
            "SIRTA crash records",
        ),
    )

    figure3.add_trace(
        go.Scatter(
            x=monthly["date"],
            y=monthly["completed_units"],
            mode="lines",
            fill="tozeroy",
            name="Completed units",
            line={"color": "#2878a5", "width": 3},
            customdata=monthly[["completed_projects"]].to_numpy(),
            hovertemplate=(
                "%{x|%B %Y}<br>"
                "Affordable housing units completed: %{y:,}<br>"
                "Housing projects completed: %{customdata[0]:,}"
                "<extra></extra>"
            ),
        ),
        row=1,
        col=1,
    )

    figure3.add_trace(
        go.Scatter(
            x=monthly["date"],
            y=monthly["crash_records"],
            mode="lines",
            fill="tozeroy",
            name="Crash records",
            line={"color": "#d66a4a", "width": 3},
            customdata=monthly[
                [
                    "severe_injuries",
                    "non_severe_injuries",
                    "fatalities",
                ]
            ].to_numpy(),
            hovertemplate=(
                "%{x|%B %Y}<br>"
                "Total crash records: %{y:,}<br>"
                "Severe injuries: %{customdata[0]:,}<br>"
                "Non-severe injuries: %{customdata[1]:,}<br>"
                "Fatalities: %{customdata[2]:,}"
                "<extra></extra>"
            ),
        ),
        row=2,
        col=1,
    )

    figure3.update_layout(
        title="Monthly Housing Completions and Crash Records",
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font={"family": font_family, "color": "#25364d"},
        height=600,
        showlegend=False,
        margin={"l": 60, "r": 30, "t": 75, "b": 50},
    )
    figure3.update_yaxes(title_text="Completed units", row=1, col=1)
    figure3.update_yaxes(title_text="Crash records", row=2, col=1)

    seasonal = filtered[
        filtered["high_start_activity"]
        & filtered["season"].isin(["Summer", "Winter"])
    ]

    seasonal_summary = (
        seasonal.groupby(["borough_key", "season"], as_index=False)["crash_records"]
        .mean()
    )

    figure4 = px.bar(
        seasonal_summary,
        x="borough_key",
        y="crash_records",
        color="season",
        barmode="group",
        category_orders={"season": ["Summer", "Winter"]},
        color_discrete_map={
            "Summer": "#d69e2e",
            "Winter": "#2878a5",
        },
        labels={
            "borough_key": "Borough",
            "crash_records": "Average crash records per month",
            "season": "Season",
        },
        title="Summer vs Winter During High-Start Months",
    )
    figure4.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font={"family": font_family, "color": "#25364d"},
        margin={"l": 60, "r": 30, "t": 75, "b": 50},
        legend_title_text="Season",
    )

    return figure3, figure4