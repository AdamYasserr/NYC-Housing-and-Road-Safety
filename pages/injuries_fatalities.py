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
                    "RQ6 · Which boroughs recorded the most SIRTA fatalities?",
                    style={"color": "#142d4e", "fontFamily": font_family},
                ),
                html.P(
                    "Bars show total recorded fatalities for the selected boroughs and years.",
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

    # RQ6: total recorded fatalities by borough.
    borough_fatalities = (
        filtered.groupby("borough_key", as_index=False)["fatalities"]
        .sum()
        .sort_values("fatalities", ascending=False)
    )

    figure6 = px.bar(
        borough_fatalities,
        x="borough_key",
        y="fatalities",
        color="borough_key",
        text="fatalities",
        color_discrete_sequence=px.colors.qualitative.Safe,
        labels={
            "borough_key": "Borough",
            "fatalities": "Recorded fatalities",
        },
        title="Recorded SIRTA Fatalities by Borough",
    )
    figure6.update_layout(
        template="plotly_white",
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font={"family": font_family, "color": "#25364d"},
        margin={"l": 60, "r": 30, "t": 75, "b": 50},
        showlegend=False,
    )
    figure6.update_traces(textposition="outside")
    figure6.update_yaxes(title_text="Recorded fatalities")

    return figure5, figure6