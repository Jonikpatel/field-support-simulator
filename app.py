"""
IT Helpdesk / Field Support Ticket Simulator
---------------------------------------------
A dashboard for an internal IT helpdesk supporting staff across multiple
field/regional offices — ticket volume, category breakdown, SLA
performance, and agent workload. Built to mirror the kind of support
operations view needed when a new system is deployed across many sites and
field staff need a fast path to help.

All data in this demo is synthetically generated (see data_generator.py).
Run locally with:  streamlit run app.py
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from data_generator import load_data, PRIORITY_SLA_HOURS, WINDOW_END

st.set_page_config(
    page_title="Field Support Ticket Simulator",
    page_icon="\U0001F6E0\uFE0F",
    layout="wide",
)

PRIORITY_ORDER = ["Critical", "High", "Medium", "Low"]
PRIORITY_COLORS = {
    "Critical": "#EA4335", "High": "#F4B400",
    "Medium": "#4285F4", "Low": "#8AB4F8",
}


@st.cache_data
def get_data():
    return load_data()


tickets = get_data()

# ---------------------------------------------------------------- sidebar --
st.sidebar.title("Filters")

date_min = tickets["date_opened"].min().date()
date_max = tickets["date_opened"].max().date()
date_range = st.sidebar.date_input(
    "Date range", (date_min, date_max), min_value=date_min, max_value=date_max
)

sites = sorted(tickets["site"].unique())
selected_sites = st.sidebar.multiselect("Site", sites, default=sites)

priorities = st.sidebar.multiselect(
    "Priority", PRIORITY_ORDER, default=PRIORITY_ORDER
)

if len(date_range) == 2:
    start, end = date_range
else:
    start, end = date_min, date_max

mask = (
    (tickets["date_opened"].dt.date >= start)
    & (tickets["date_opened"].dt.date <= end)
    & (tickets["site"].isin(selected_sites))
    & (tickets["priority"].isin(priorities))
)
f = tickets[mask]

st.sidebar.markdown("---")
st.sidebar.caption(
    f"As of **{WINDOW_END.strftime('%B %d, %Y')}**\n\n"
    "All data is synthetic, generated for demonstration purposes."
)

# ------------------------------------------------------------------ title --
st.title("\U0001F6E0\uFE0F Field Support Ticket Simulator")
st.caption(
    "Helpdesk ticket volume, categories, and SLA performance across field "
    "and regional office staff."
)

# -------------------------------------------------------------------- KPIs --
total = len(f)
open_count = len(f[f["status"] == "Open"])
resolved = f[f["status"] == "Resolved"]
breach_rate = f["sla_breached"].mean() * 100 if total else 0
avg_resolution = resolved["resolution_hours"].mean() if not resolved.empty else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total tickets", total)
k2.metric("Open now", open_count)
k3.metric("Avg. resolution time", f"{avg_resolution:.1f} hrs")
k4.metric("SLA breach rate", f"{breach_rate:.1f}%", delta_color="inverse")

st.markdown("---")

# ------------------------------------------------------------- top row -----
c1, c2 = st.columns([1.5, 1])

with c1:
    st.subheader("Ticket Volume Over Time")
    if not f.empty:
        daily = (
            f.assign(day=f["date_opened"].dt.date)
            .groupby("day")
            .size()
            .reset_index(name="tickets")
        )
        fig = px.line(daily, x="day", y="tickets", markers=True,
                       labels={"day": "Date", "tickets": "Tickets Opened"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No tickets match the current filters.")

with c2:
    st.subheader("By Priority")
    if not f.empty:
        pc = f["priority"].value_counts().reindex(PRIORITY_ORDER).fillna(0)
        fig2 = px.pie(
            values=pc.values, names=pc.index, hole=0.5,
            color=pc.index, color_discrete_map=PRIORITY_COLORS,
        )
        fig2.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320)
        st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------ site & cat ---
c3, c4 = st.columns(2)

with c3:
    st.subheader("Tickets by Site")
    if not f.empty:
        by_site = f["site"].value_counts().reset_index()
        by_site.columns = ["site", "count"]
        fig3 = px.bar(
            by_site.sort_values("count"), x="count", y="site", orientation="h",
            labels={"count": "Tickets", "site": ""}, height=450,
        )
        st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("Tickets by Category")
    if not f.empty:
        by_cat = f["category"].value_counts().reset_index()
        by_cat.columns = ["category", "count"]
        fig4 = px.bar(
            by_cat.sort_values("count"), x="count", y="category", orientation="h",
            labels={"count": "Tickets", "category": ""}, height=450,
            color="category",
        )
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# --------------------------------------------------------- SLA & agents ----
c5, c6 = st.columns(2)

with c5:
    st.subheader("SLA Breach Rate by Priority")
    if not f.empty:
        sla = (
            f.groupby("priority")["sla_breached"]
            .mean()
            .reindex(PRIORITY_ORDER)
            .fillna(0)
            .mul(100)
            .reset_index(name="breach_pct")
        )
        fig5 = px.bar(
            sla, x="priority", y="breach_pct", color="priority",
            color_discrete_map=PRIORITY_COLORS,
            labels={"breach_pct": "SLA Breach %", "priority": "Priority"},
            category_orders={"priority": PRIORITY_ORDER},
        )
        fig5.update_layout(showlegend=False)
        st.plotly_chart(fig5, use_container_width=True)
        st.caption(
            "SLA targets: Critical = "
            f"{PRIORITY_SLA_HOURS['Critical']}h, High = {PRIORITY_SLA_HOURS['High']}h, "
            f"Medium = {PRIORITY_SLA_HOURS['Medium']}h, Low = {PRIORITY_SLA_HOURS['Low']}h"
        )

with c6:
    st.subheader("Agent Workload")
    if not f.empty:
        by_agent = f.groupby("agent").agg(
            tickets=("ticket_id", "count"),
            avg_resolution_hrs=("resolution_hours", "mean"),
        ).reset_index().sort_values("tickets", ascending=False)
        by_agent["avg_resolution_hrs"] = by_agent["avg_resolution_hrs"].round(1)
        st.dataframe(by_agent, use_container_width=True, hide_index=True)

# ------------------------------------------------------------ ticket table -
st.subheader("Ticket Log")
log = f[[
    "ticket_id", "date_opened", "site", "requester_role", "category",
    "subcategory", "priority", "agent", "status", "resolution_hours", "sla_breached",
]].rename(columns={
    "ticket_id": "Ticket", "date_opened": "Opened", "site": "Site",
    "requester_role": "Requester Role", "category": "Category",
    "subcategory": "Subcategory", "priority": "Priority", "agent": "Agent",
    "status": "Status", "resolution_hours": "Resolution (hrs)",
    "sla_breached": "SLA Breached",
})
st.dataframe(
    log.sort_values("Opened", ascending=False),
    use_container_width=True, hide_index=True, height=400,
)
