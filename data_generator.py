"""
Synthetic data generator for the IT Helpdesk / Field Support Ticket Simulator.

Simulates an internal IT helpdesk supporting staff across multiple field
offices and roles — ticket intake, categorization, priority, SLA tracking,
and resolution. All data is randomly generated for demonstration purposes.
"""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

random.seed(7)
np.random.seed(7)

SITES = [
    "Frankfort HQ", "Lexington East", "Lexington West", "Covington",
    "Louisville Downtown", "Louisville South", "Bowling Green", "Owensboro",
    "Paducah", "Elizabethtown", "Somerset", "London", "Pikeville",
    "Ashland", "Winchester",
]

ROLES = ["Field Technician", "Office Clerk", "Supervisor", "Regional Admin"]

CATEGORIES = {
    "Hardware": ["Scanner", "Printer", "Workstation", "Card Reader", "Barcode Scanner"],
    "Software / Access": ["Login Failure", "Permission Denied", "App Crash", "Password Reset"],
    "Network": ["Connectivity Drop", "VPN Issue", "Slow Network", "Wi-Fi Outage"],
    "Data": ["Sync Error", "Record Mismatch", "Report Discrepancy", "Duplicate Entry"],
    "Training / How-To": ["Workflow Question", "New Feature Question", "Process Clarification"],
}

PRIORITY_SLA_HOURS = {"Critical": 4, "High": 24, "Medium": 72, "Low": 168}
PRIORITY_WEIGHTS = {"Critical": 0.05, "High": 0.2, "Medium": 0.45, "Low": 0.3}

AGENTS = [
    "Helpdesk - Agent A", "Helpdesk - Agent B", "Helpdesk - Agent C",
    "Helpdesk - Agent D", "Field Support - Agent E",
]

WINDOW_START = datetime(2026, 6, 1)
WINDOW_END = datetime(2026, 8, 27, 17, 0)


def _random_datetime(start, end):
    delta = end - start
    seconds = random.randint(0, int(delta.total_seconds()))
    dt = start + timedelta(seconds=seconds)
    # bias toward business hours, Mon-Fri
    while dt.weekday() >= 5 or not (7 <= dt.hour <= 18):
        dt = start + timedelta(seconds=random.randint(0, int(delta.total_seconds())))
    return dt


def generate_tickets(n_tickets=850):
    rows = []
    for i in range(1, n_tickets + 1):
        site = random.choice(SITES)
        role = random.choices(ROLES, weights=[0.4, 0.35, 0.15, 0.1])[0]
        category = random.choices(
            list(CATEGORIES.keys()), weights=[0.32, 0.28, 0.18, 0.14, 0.08]
        )[0]
        subcategory = random.choice(CATEGORIES[category])
        priority = random.choices(
            list(PRIORITY_SLA_HOURS.keys()),
            weights=list(PRIORITY_WEIGHTS.values()),
        )[0]

        opened = _random_datetime(WINDOW_START, WINDOW_END)
        sla_hours = PRIORITY_SLA_HOURS[priority]

        # resolution time: usually within SLA, occasionally breaches it
        breach_roll = random.random()
        if breach_roll < 0.12:  # ~12% SLA breach rate
            resolve_hours = sla_hours * random.uniform(1.1, 3.0)
        else:
            resolve_hours = sla_hours * random.uniform(0.05, 0.95)

        resolved_at = opened + timedelta(hours=resolve_hours)
        is_resolved = resolved_at <= WINDOW_END
        agent = random.choice(AGENTS)

        rows.append({
            "ticket_id": f"HD-{i:05d}",
            "site": site,
            "requester_role": role,
            "category": category,
            "subcategory": subcategory,
            "priority": priority,
            "agent": agent,
            "date_opened": opened,
            "sla_hours": sla_hours,
            "date_resolved": resolved_at if is_resolved else pd.NaT,
            "status": "Resolved" if is_resolved else "Open",
            "resolution_hours": round(resolve_hours, 1) if is_resolved else None,
            "sla_breached": (resolve_hours > sla_hours) if is_resolved else (
                (WINDOW_END - opened).total_seconds() / 3600 > sla_hours
            ),
        })

    df = pd.DataFrame(rows)
    return df.sort_values("date_opened").reset_index(drop=True)


def load_data():
    return generate_tickets()
