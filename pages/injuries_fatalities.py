from pathlib import Path

import pandas as pd
import plotly.express as px
import dash
from dash import Input, Output, State, callback, dcc, html
from filter_utils import apply_filters

dash.register_page(
    __name__,
    path="/units-fatalities",
    name="Injuries & Fatalities",
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
            "Injuries & Fatalities",
            style={
                "color": "#142d4e",
                "fontFamily": font_family,
                "fontSize": "30px",
                "marginTop": "0",
                "marginBottom": "8px",
            },
        ),
        html.P(
            "Explore how completed affordable housing units, severe injuries, and recorded fatalities vary across boroughs.",
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
                    "RQ5 · Completed units and severe injuries",
                    style={"color": "#142d4e", "fontFamily": font_family},
                ),
                html.P(
                    "Each bubble represents one borough-month. Bubble size represents crash records.",
                    style={"color": "#53657b", "fontFamily": font_family},
                ),
                dcc.Graph(
                    id="rq5-bubble",
                    config={"displaylogo": False, "scrollZoom": True},
                ),
            ],
            style=card_style,
        ),

        html.Section(
            [
                html.H3(
                    "RQ6 · Are boroughs with higher affordable housing development activity also experiencing higher numbers of severe road injuries?",
                    style={"color": "#142d4e", "fontFamily": font_family},
                ),
                html.P(
                    "Each point represents one borough, using total completed affordable housing units and severe road injuries from 2022–2025.",
                    style={"color": "#53657b", "fontFamily": font_family},
                ),
                dcc.Graph(
                    id="rq6-boroughs",
                    config={"displaylogo": False, "scrollZoom": True},
                ),
            ],
            style=card_style,
        ),
    ],
    style={"fontFamily": font_family},
)


@callback(
    Output("rq5-bubble", "figure"),
    Output("rq6-boroughs", "figure"),
    Input("generate-report", "n_clicks"),
    State("borough-filter", "value"),
    State("year-filter", "value"),
    State("housing-filter", "value"),
    State("transportation-filter", "value"),
    State("search-input", "value"),
)
def update_units_fatalities(
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

    # RQ5: one bubble for each borough-month.
    figure5 = px.scatter(
        filtered,
        x="counted_units_in_projects_completed",
        y="severe_injuries",
        size="crash_records",
        color="borough_key",
        hover_data=["year", "month"],
        size_max=28,
        color_discrete_sequence=px.colors.qualitative.Safe,
        labels={
            "counted_units_in_projects_completed": "Counted completed units",
            "severe_injuries": "Severe injuries",
            "crash_records": "Crash records",
            "borough_key": "Borough",
        },
        title="Completed Units and Severe Injuries by Borough-Month",
    )
    figure5.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font={"family": font_family, "color": "#25364d"},
        margin={"l": 60, "r": 30, "t": 75, "b": 50},
        legend_title_text="Borough",
    )

    # RQ6: total completed units and severe injuries by borough for 2022–2025.
    rq6_filtered = filtered[filtered["year"].between(2022, 2025)]
    borough_totals = (
        rq6_filtered.groupby("borough_key", as_index=False)[
            ["counted_units_in_projects_completed", "severe_injuries"]
        ]
        .sum()
    )

    figure6 = px.scatter(
        borough_totals,
        x="counted_units_in_projects_completed",
        y="severe_injuries",
        color="borough_key",
        hover_name="borough_key",
        hover_data={
            "borough_key": False,
            "counted_units_in_projects_completed": ":,",
            "severe_injuries": ":,",
        },
        color_discrete_sequence=px.colors.qualitative.Safe,
        labels={
            "borough_key": "Borough",
            "counted_units_in_projects_completed": "Total completed affordable housing units",
            "severe_injuries": "Total severe road injuries",
        },
        title="Affordable Housing Completions and Severe Road Injuries by Borough (2022–2025)",
    )
    figure6.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font={"family": font_family, "color": "#25364d"},
        margin={"l": 60, "r": 30, "t": 75, "b": 50},
        legend_title_text="Borough",
    )
    figure6.update_traces(marker={"size": 12, "line": {"width": 1, "color": "#ffffff"}})
    figure6.update_xaxes(title_text="Total completed affordable housing units")
    figure6.update_yaxes(title_text="Total severe road injuries")

    return figure5, figure6