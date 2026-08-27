# IT Helpdesk / Field Support Ticket Simulator

A Streamlit dashboard simulating an internal IT helpdesk supporting staff
across multiple field and regional offices — ticket volume, category
breakdown, SLA performance, and agent workload.

**Why this exists:** when a new system goes live across many field offices,
support tickets become the earliest signal of where the rollout is
struggling — which sites, which issue types, and whether the team is
meeting response-time commitments. This project simulates that support
operations view.

## What it shows

- **KPI strip** — total tickets, currently open, average resolution time,
  SLA breach rate
- **Ticket volume over time** — daily trend line
- **Priority mix** — donut chart of Critical / High / Medium / Low
- **Tickets by site** — which field offices are generating the most
  support load
- **Tickets by category** — Hardware, Software/Access, Network, Data,
  Training/How-To, each with subcategories (e.g. scanner issues, login
  failures, sync errors)
- **SLA breach rate by priority** — measured against realistic SLA targets
  (Critical: 4h, High: 24h, Medium: 72h, Low: 168h)
- **Agent workload** — ticket count and average resolution time per agent
- **Full ticket log** — filterable, sortable table of every ticket

All filters (date range, site, priority) update every chart and table.

## Data

All data is synthetically generated in `data_generator.py` — no real
agency, staff, or ticket data is used. The generator models ~850 tickets
across 15 sites, 4 requester roles, 5 categories with realistic
subcategories, weighted priority distribution, and an ~12% SLA breach rate
to keep the numbers realistic rather than uniformly clean.

Swap in real data by replacing `data_generator.load_data()` with a loader
that returns a DataFrame with the same columns used throughout `app.py`.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Tech

Python, Streamlit, Pandas, Plotly.
