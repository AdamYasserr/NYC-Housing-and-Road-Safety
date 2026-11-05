import dash
from dash import html

dash.register_page(__name__, path="/our-story", name="Our Story")

navy = "#17345b"
muted = "#5d6f86"
card_style = {
    "backgroundColor": "white",
    "border": "1px solid #dbe4ef",
    "borderRadius": "16px",
    "padding": "26px",
    "marginBottom": "20px",
    "boxShadow": "0 4px 16px rgba(23, 52, 91, 0.06)",
}

layout = html.Div(
    [
        html.H1(
            "Our Story",
            style={"color": navy, "fontSize": "38px", "marginBottom": "8px"},
        ),
        html.P(
            "Affordable housing activity and serious road-safety outcomes across "
            "New York City's five boroughs, 2022–2025.",
            style={
                "color": muted,
                "fontSize": "18px",
                "lineHeight": "1.6",
                "marginTop": "0",
                "marginBottom": "28px",
            },
        ),

        html.Section(
            [
                html.H2("The question", style={"color": navy}),
                html.P(
                    "How did monthly affordable housing starts and completions "
                    "coincide with SIRTA crash records, severe injuries, and "
                    "fatalities across NYC boroughs?",
                    style={"color": muted, "fontSize": "17px", "lineHeight": "1.7"},
                ),
            ],
            style=card_style,
        ),

        html.Section(
            [
                html.H2("What the data shows", style={"color": navy}),
                html.P(
                    "Across the 240 borough-month records, the dataset includes "
                    "2,408 housing projects started, 2,267 completed, and 102,141 "
                    "counted units in completed projects. It also records 11,922 "
                    "SIRTA crashes, 12,011 severe injuries, and 970 fatalities.",
                    style={
                        "color": muted,
                        "fontSize": "16px",
                        "lineHeight": "1.7",
                        "overflowWrap": "anywhere",
                    },
                ),
                html.Ul(
                    [
                        html.Li(
                            "Queens recorded the most fatalities (286), followed "
                            "closely by Brooklyn (283). Staten Island recorded the "
                            "fewest (53)."
                        ),
                        html.Li(
                            "During high housing-start months, average crash "
                            "records were higher in summer than winter in the Bronx, "
                            "Brooklyn, Manhattan, and Queens. Staten Island showed "
                            "the reverse pattern."
                        ),
                        html.Li(
                            "Severe injuries per 100 crash records were generally "
                            "close to 100, with differences varying by borough and "
                            "housing-start activity."
                        ),
                        html.Li(
                            "The charts show that housing activity and crash "
                            "records vary across boroughs and months. They do not "
                            "show that housing activity causes crashes."
                        ),
                    ],
                    style={
                        "color": muted,
                        "fontSize": "16px",
                        "lineHeight": "1.9",
                        "paddingLeft": "24px",
                    },
                ),
            ],
            style=card_style,
        ),

        html.Section(
            [
                html.H2("Why this matters to NYC", style={"color": navy}),
                html.P(
                    "This dashboard gives residents and decision-makers a borough "
                    "and month-level view of affordable housing activity alongside "
                    "serious crash outcomes. It can help identify patterns that "
                    "deserve closer investigation and support conversations about "
                    "coordinating housing growth with street-safety planning.",
                    style={
                        "color": muted,
                        "fontSize": "16px",
                        "lineHeight": "1.7",
                        "overflowWrap": "anywhere",
                    },
                ),
            ],
            style=card_style,
        ),

        html.Section(
            [
                html.H2("Data and integration", style={"color": navy}),
                html.P(
                    "The dashboard integrates New York City Department of Housing "
                    "Preservation and Development's Affordable Housing Production by "
                    "Building dataset with the NYC Department of Transportation's Serious "
                    "Injury Response Tracking Analysis Program (SIRTA) dataset. The "
                    "supplied integrated CSV covers NYC's five boroughs at the monthly "
                    "level from 2022 through 2025. Housing fields include project and "
                    "building-record starts, completions, and counted units; transportation "
                    "fields include crash, injury, and fatality counts.",
                    style={
                        "color": muted,
                        "fontSize": "16px",
                        "lineHeight": "1.7",
                        "overflowWrap": "anywhere",
                    },
                ),
                html.P(
                    "Official sources: "
                    "Affordable Housing Production by Building "
                    "(NYC HPD), "
                    "https://data.cityofnewyork.us/Housing-Development/"
                    "Affordable-Housing-Production-by-Building/hg8x-zxpr; and "
                    "Serious-Injury-Response-Tracking-Analysis-Program (SIRTA) "
                    "(NYC DOT), "
                    "https://data.cityofnewyork.us/Transportation/"
                    "Serious-Injury-Response-Tracking-Analysis-Program-/xeqp-qz8h. "
                    "The integration is an aggregate join by borough and year-month; "
                    "missing values are retained as represented in the supplied CSV. "
                    "This aggregation cannot identify individual projects or crashes, "
                    "and it does not provide population-, traffic-volume-, or "
                    "exposure-adjusted rates.",
                    style={
                        "color": muted,
                        "fontSize": "16px",
                        "lineHeight": "1.7",
                        "overflowWrap": "anywhere",
                    },
                ),
            ],
            style=card_style,
        ),

        html.Section(
            [
                html.H2("Limitations", style={"color": navy}),
                html.Ul(
                    [
                        html.Li(
                            "The data is aggregated by borough and month. It cannot "
                            "connect an individual crash to a specific housing "
                            "project or construction site."
                        ),
                        html.Li(
                            "These are raw counts, not rates adjusted for "
                            "population, traffic volume, or road-user exposure. "
                            "Borough totals may differ partly because boroughs "
                            "differ in size and activity."
                        ),
                        html.Li(
                            "The analysis describes patterns and associations; it "
                            "cannot establish cause and effect."
                        ),
                        html.Li(
                            "Findings cover the period represented in the supplied "
                            "dataset and may not describe conditions outside it."
                        ),
                    ],
                    style={
                        "color": muted,
                        "fontSize": "16px",
                        "lineHeight": "1.9",
                        "paddingLeft": "24px",
                    },
                ),
            ],
            style=card_style,
        ),
    ],
    style={
        "backgroundColor": "#f3f6fb",
        "minHeight": "100vh",
        "padding": "36px 5%",
        "fontFamily": "'Avenir Next', Arial, sans-serif",
    },
)