# Housing Safety Website

## Project overview and objectives

An interactive Plotly Dash data story comparing affordable housing activity with
street-safety outcomes across New York City's boroughs.

The project objective is to make borough- and month-level patterns easier to
explore while clearly separating descriptive association from causation.

## Research question

How did monthly affordable housing starts and completions coincide with SIRTA
crash records, severe injuries, and fatalities across NYC boroughs?

## Dataset sources and integration

- **Affordable Housing Production by Building** — New York City Department of
  Housing Preservation and Development (HPD):  
  https://data.cityofnewyork.us/Housing-Development/Affordable-Housing-Production-by-Building/hg8x-zxpr
- **Serious Injury Response Tracking Analysis Program (SIRTA)** — New York City
  Department of Transportation (DOT):  
  https://data.cityofnewyork.us/Transportation/Serious-Injury-Response-Tracking-Analysis-Program-/xeqp-qz8h

The checked-in integrated file contains NYC's five boroughs and monthly records
from 2022 through 2025. Housing measures are aggregated into project/building
starts, completions, and counted units. Transportation measures are aggregated
into crash records, non-severe injuries, severe injuries, and fatalities. The
integration key is borough plus `year_month`. Missing-value handling follows
the supplied integrated CSV; no project-level crash linkage is inferred.

## Technologies

Python, Plotly Dash, Pandas, Plotly, and Gunicorn.

## Project structure

```text
app.py                 Shared layout, navigation, filters, search, and report
filter_utils.py        Search parsing and combined filtering
pages/                 Six registered dashboard pages
data/                  Integrated CSV dataset
requirements.txt       Python dependencies
```

## Data cleaning and limitations

The application loads the supplied CSV with Pandas using a path relative to
the project root. Date values are represented by `year_month`, and the pages
derive month dates, seasons, activity groups, and the next month's crash
comparison from the integrated rows. The data is an aggregate borough-month
view: it does not support causal claims, individual project-to-crash matching,
or rates adjusted for population, traffic volume, or road-user exposure.

## Installation and virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate`.

## Run locally

```bash
python app.py
```

Open the local URL printed by Dash. Use the borough/year dropdowns, the
category filters, or a search such as `Brooklyn 2022 new buildings`, then
select **Generate Report**.

## Environment variables

No environment variables, credentials, or external API keys are required.

## Deployment

From the project root, serve the WSGI object with:

```bash
gunicorn app
```

Live deployment URL: **[PLACEHOLDER - add deployed website URL]**

## Dashboard pages

1. **Our Story** — research question, findings, data notes, and limitations.
2. **Data & Filters** — filtered integrated borough-month records.
3. **Starts & Crashes** — housing starts and crash-record comparisons.
4. **Trends & Seasons** — monthly trends and seasonal high-start comparisons.
5. **Injuries & Fatalities** — severe injuries, completed units, and fatalities.
6. **Severity & Next Month** — injury severity and following-month crash patterns.

## Team

## Team members and contributions

Each member contributed to two research questions and their corresponding
visualizations and analysis. Each member therefore contributed to two
visualizations:

| Team member | Student ID | Assigned research questions and contribution |
|---|---:|---|
| Adam Yasser | 16001052 | Q1 and Q6, including the corresponding visualizations and analysis |
| Gizelle Mohamed | 16002790 | Q3 and Q4, including the corresponding visualizations and analysis |
| Masa Bassem | 16007640 | Q2 and Q5, including the corresponding visualizations and analysis |
| Hania Baher | 16007635 | Q7 and Q8, including the corresponding visualizations and analysis |
