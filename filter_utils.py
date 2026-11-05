import re

import pandas as pd


BOROUGHS = ("Bronx", "Brooklyn", "Manhattan", "Queens", "Staten Island")
HOUSING_ACTIVITIES = ("Starts", "Completions", "Both")
TRANSPORTATION_OUTCOMES = (
    "Crashes",
    "Injuries",
    "Severe injuries",
    "Fatalities",
)


def parse_search_query(query):
    """Return recognized filters and the terms that could not be interpreted."""
    text = (query or "").strip()
    lowered = text.lower()
    borough = next((value for value in BOROUGHS if value.lower() in lowered), None)
    year_match = re.search(r"\b(20\d{2})\b", text)
    year = int(year_match.group(1)) if year_match else None

    housing = None
    if re.search(r"\b(new buildings?|building records?|starts?|started)\b", lowered):
        housing = "Starts"
    elif re.search(r"\b(completions?|completed)\b", lowered):
        housing = "Completions"
    elif re.search(r"\bboth\b", lowered):
        housing = "Both"

    transportation = None
    if re.search(r"\bfatalit(?:y|ies)\b", lowered):
        transportation = "Fatalities"
    elif re.search(r"\bsevere injuries?\b", lowered):
        transportation = "Severe injuries"
    elif re.search(r"\binjuries?\b", lowered):
        transportation = "Injuries"
    elif re.search(r"\bcrashes?\b|\bcrash records?\b|\btraffic\b", lowered):
        transportation = "Crashes"

    recognized_terms = set()
    if borough:
        recognized_terms.add(borough.lower())
    if year:
        recognized_terms.add(str(year))
    if housing:
        recognized_terms.update(
            {
                "Starts": ("start", "starts", "started", "new", "buildings", "building"),
                "Completions": ("completion", "completions", "completed"),
                "Both": ("both",),
            }[housing]
        )
    if transportation:
        recognized_terms.update(transportation.lower().split())
        if transportation == "Crashes":
            recognized_terms.update(("crash", "crashes", "traffic"))
    unrecognized = [
        term
        for term in re.findall(r"[a-z0-9]+", lowered)
        if term not in recognized_terms
    ]
    return {
        "borough": borough,
        "year": year,
        "housing_activity": housing,
        "transportation_outcome": transportation,
        "unrecognized_terms": sorted(set(unrecognized)),
    }


def apply_filters(
    data,
    selected_borough=None,
    selected_year=None,
    housing_activity=None,
    transportation_outcome=None,
    search_query=None,
):
    parsed = parse_search_query(search_query)
    borough = selected_borough or parsed["borough"]
    year = selected_year or parsed["year"]
    housing = housing_activity or parsed["housing_activity"]
    transportation = transportation_outcome or parsed["transportation_outcome"]

    filtered = data.copy()
    if borough:
        filtered = filtered[filtered["borough_key"] == borough]
    if year:
        filtered = filtered[filtered["year"] == int(year)]
    if housing == "Starts":
        filtered = filtered[filtered["housing_projects_started"] > 0]
    elif housing == "Completions":
        filtered = filtered[filtered["housing_projects_completed"] > 0]
    elif housing == "Both":
        filtered = filtered[
            (filtered["housing_projects_started"] > 0)
            & (filtered["housing_projects_completed"] > 0)
        ]
    if transportation == "Crashes":
        filtered = filtered[filtered["crash_records"] > 0]
    elif transportation == "Injuries":
        filtered = filtered[
            (filtered["non_severe_injuries"] + filtered["severe_injuries"]) > 0
        ]
    elif transportation == "Severe injuries":
        filtered = filtered[filtered["severe_injuries"] > 0]
    elif transportation == "Fatalities":
        filtered = filtered[filtered["fatalities"] > 0]
    return filtered, parsed


def format_filter_summary(
    selected_borough,
    selected_year,
    housing_activity,
    transportation_outcome,
    search_query,
):
    parsed = parse_search_query(search_query)
    borough = selected_borough or parsed["borough"]
    year = selected_year or parsed["year"]
    housing = housing_activity or parsed["housing_activity"]
    transportation = transportation_outcome or parsed["transportation_outcome"]
    criteria = []
    if borough:
        criteria.append(f"borough: {borough}")
    if year:
        criteria.append(f"year: {year}")
    if housing:
        criteria.append(f"housing: {housing}")
    if transportation:
        criteria.append(f"transportation: {transportation}")
    return ", ".join(criteria) if criteria else "all records"
