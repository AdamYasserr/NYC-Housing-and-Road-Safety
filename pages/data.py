from pathlib import Path

import pandas as pd
import dash
from dash import Input, Output, State, callback, dash_table, html

dash.register_page(__name__, path="/", name="Data & Filters")

data_path = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "integrated_housing_sirta_borough_month.csv"
)
df = pd.read_csv(data_path)

layout = html.Div(
    [
        html.H2(
            "Explore the Integrated Dataset",
            style={
                "color": "#142d4e",
                "fontFamily": "Avenir Next, Arial, sans-serif",
                "fontSize": "30px",
                "fontWeight": "700",
                "marginBottom": "10px",
            },
        ),

        html.P(
            "Examine monthly affordable housing production and SIRTA crash "
            "outcomes across New York City by borough and year.",
            style={
                "color": "#53657b",
                "fontFamily": "Avenir Next, Arial, sans-serif",
                "fontSize": "16px",
                "lineHeight": "1.6",
                "marginTop": "0",
                "marginBottom": "24px",
                "maxWidth": "850px",
            },
        ),

        html.P(
            id="row-count",
            children="Choose a borough or year, then select Generate Report to view the matching records.",
            style={
                "color": "#53657b",
                "fontFamily": "Avenir Next, Arial, sans-serif",
                "fontSize": "14px",
                "marginBottom": "12px",
            },
        ),

        dash_table.DataTable(
            id="data-table",
            columns=[{"name": column, "id": column} for column in df.columns],
            data=df.to_dict("records"),
            page_size=10,
            style_table={
                "overflowX": "auto",
                "border": "1px solid #d8e1ed",
                "borderRadius": "10px",
            },
            style_cell={
                "textAlign": "left",
                "padding": "12px",
                "fontFamily": "Avenir Next, Arial, sans-serif",
                "fontSize": "13px",
                "color": "#25364d",
                "backgroundColor": "#ffffff",
                "minWidth": "120px",
                "maxWidth": "280px",
                "whiteSpace": "normal",
                "height": "auto",
            },
            style_header={
                "backgroundColor": "#142d4e",
                "color": "#ffffff",
                "fontWeight": "700",
                "border": "1px solid #142d4e",
                "whiteSpace": "normal",
                "height": "auto",
            },
            style_data_conditional=[
                {
                    "if": {"row_index": "odd"},
                    "backgroundColor": "#f4f7fb",
                }
            ],
        ),
    ],
    style={
        "backgroundColor": "#ffffff",
        "padding": "30px",
        "borderRadius": "16px",
        "fontFamily": "Avenir Next, Arial, sans-serif",
        "boxShadow": "0 6px 24px rgba(20, 45, 78, 0.08)",
    },
)


@callback(
    Output("data-table", "data"),
    Output("row-count", "children"),
    Input("generate-report", "n_clicks"),
    State("borough-filter", "value"),
    State("year-filter", "value"),
)
def filter_table(_clicks, selected_borough, selected_year):
    filtered = df.copy()

    if selected_borough:
        filtered = filtered[filtered["borough_key"] == selected_borough]

    if selected_year:
        filtered = filtered[filtered["year"] == selected_year]

    return (
        filtered.to_dict("records"),
        f"Showing {len(filtered)} borough-month records.",
    )