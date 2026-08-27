# Field Support Ticket Simulator

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://field-support-simulator.streamlit.app/)

A Streamlit dashboard built to monitor simulated IT helpdesk operations across multi-site field offices. Tracks ticket spikes, resolution times, SLA compliance, and recurring failure categories during phased software rollouts.

---

### Key Features

* **Operational Overview:** Live summary of total tickets, open issues, average resolution time, and SLA breach rate.
* **Volume Tracking:** Daily ticket volume trends over time.
* **Severity Breakdown:** Distribution across Critical, High, Medium, and Low priorities.
* **Site & Category Analytics:** Ticket distribution by field office and issue category (Hardware, Software/Access, Network, Data, Training) with subcategory drill-downs.
* **SLA Performance:** Breach tracking evaluated against priority-based SLA targets (Critical: 4h, High: 24h, Medium: 72h, Low: 168h).
* **Agent Workload:** Ticket volume and mean resolution time per support engineer.
* **Interactive Ticket Log:** Filterable and sortable records by site, priority, and date range.

---

### Tech Stack

* **Language:** Python
* **Framework:** Streamlit
* **Data Processing:** Pandas
* **Visualizations:** Plotly

---

### Getting Started

1. **Clone the repository**
   ```bash
   git clone [https://github.com/Jonikpatel/field-support-simulator.git](https://github.com/Jonikpatel/field-     support-simulator.git)
   cd field-support-simulator
   
2.**Set up a virtual environment**

    ```Bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3.**Install dependencies**

    ```Bash
    pip install -r requirements.txt
  
4.**Run the dashboard**

    ```Bash
    streamlit run app.py

---

### Data & Customization

The app runs on synthetic data generated via data_generator.py (~850 simulated tickets across 15 sites with a ~12% SLA breach rate).

To use your own data, replace data_generator.load_data() with a function returning a DataFrame matching the schema in app.py (ticket_id, site, category, subcategory, priority, created_at, resolved_at, and assigned_agent).
