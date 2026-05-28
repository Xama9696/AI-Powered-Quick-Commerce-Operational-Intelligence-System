import streamlit as st

import pandas as pd
import numpy as np

import plotly.express as px

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(

    page_title="OperaIQ",

    layout="wide"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv("../data/operaiq_dataset.csv")

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title(
    "OperaIQ — Operational Intelligence Dashboard"
)

st.markdown("""
Integrated Quick Commerce Operating Intelligence System
""")

# ---------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------

st.sidebar.title("OperaIQ Controls")

zone_filter = st.sidebar.multiselect(

    "Select City Zone",

    df["city_zone"].unique(),

    default=df["city_zone"].unique()
)

peak_filter = st.sidebar.selectbox(

    "Peak Hour",

    ["All", 0, 1]
)

# ---------------------------------------------------
# FILTER DATAFRAME
# ---------------------------------------------------

filtered_df = df[
    df["city_zone"].isin(zone_filter)
]

if peak_filter != "All":

    filtered_df = filtered_df[
        filtered_df["peak_hour"] == peak_filter
    ]

# ---------------------------------------------------
# KPI CARDS
# ---------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(

    "Orders",

    len(filtered_df)
)

col2.metric(

    "Avg Delivery Time",

    round(
        filtered_df["delivery_time"].mean(),
        2
    )
)

col3.metric(

    "SLA Breach %",

    round(
        filtered_df["sla_breach"].mean()*100,
        2
    )
)

col4.metric(

    "Avg Order Cost",

    round(
        filtered_df["order_cost"].mean(),
        2
    )
)

col5.metric(

    "Avg Pick Time",

    round(
        filtered_df["pick_time"].mean(),
        2
    )
)

# ---------------------------------------------------
# TABS
# ---------------------------------------------------

tab1, tab2, tab3 = st.tabs([

    "Operations",

    "Cost Intelligence",

    "SLA Analytics"
])

# ---------------------------------------------------
# TAB 1 — OPERATIONS
# ---------------------------------------------------

with tab1:

    st.subheader(
        "Pick Time vs Delivery Time"
    )

    fig1 = px.scatter(

        filtered_df,

        x="pick_time",

        y="delivery_time",

        color="sla_breach",

        title="Pick Time vs Delivery Time"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    st.subheader(
        "Operational Congestion Heatmap"
    )

    pivot = pd.pivot_table(

        filtered_df,

        values="delivery_time",

        index="city_zone",

        columns="peak_hour",

        aggfunc=np.mean
    )

    fig2 = px.imshow(

        pivot,

        text_auto=True,

        color_continuous_scale="Blues",

        title="Operational Congestion Heatmap"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ---------------------------------------------------
# TAB 2 — COST INTELLIGENCE
# ---------------------------------------------------

with tab2:

    st.subheader(
        "Operational Cost Ledger"
    )

    costs = pd.DataFrame({

        "Type":[

            "Pick",

            "Staging",

            "Last Mile"
        ],

        "Cost":[

            filtered_df["pick_cost"].mean(),

            filtered_df["staging_cost"].mean(),

            filtered_df["last_mile_cost"].mean()
        ]
    })

    fig3 = px.pie(

        costs,

        names="Type",

        values="Cost",

        title="Operational Cost Distribution"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.subheader(
        "Cost Distribution Histogram"
    )

    fig4 = px.histogram(

        filtered_df,

        x="order_cost",

        nbins=30,

        title="Order Cost Distribution"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# ---------------------------------------------------
# TAB 3 — SLA ANALYTICS
# ---------------------------------------------------

with tab3:

    st.subheader(
        "SLA Breach Distribution"
    )

    fig5 = px.histogram(

        filtered_df,

        x="delivery_time",

        color="sla_breach",

        title="SLA Breach Distribution"
    )

    st.plotly_chart(

        fig5,

        use_container_width=True
    )

    st.subheader(
        "SLA Breach by City Zone"
    )

    sla_zone = filtered_df.groupby(
        "city_zone"
    )["sla_breach"].mean().reset_index()

    sla_zone["sla_breach"] = (
        sla_zone["sla_breach"] * 100
    )

    fig6 = px.bar(

        sla_zone,

        x="city_zone",

        y="sla_breach",

        title="SLA Breach % by City Zone"
    )

    st.plotly_chart(

        fig6,

        use_container_width=True
    )

# ---------------------------------------------------
# AI OPERATIONAL RECOMMENDATIONS
# ---------------------------------------------------

st.subheader(
    "AI Operational Recommendations"
)

if filtered_df["sla_breach"].mean() > 0.7:

    st.warning(

        "High SLA breach risk detected. Increase rider allocation during peak operational windows."
    )

if filtered_df["pick_time"].mean() > 25:

    st.warning(

        "Warehouse pick latency elevated. Dynamic SKU slotting optimization recommended."
    )

if filtered_df["warehouse_wait_time"].mean() > 10:

    st.warning(

        "Dispatch staging delays detected. Improve batching workflows."
    )

# ---------------------------------------------------
# BUSINESS INSIGHTS
# ---------------------------------------------------

st.subheader(
    "Operational Insights"
)

st.markdown("""

- Peak-hour congestion significantly increases SLA breach probability.

- Last-mile operations contribute the largest share of operational cost.

- Warehouse pick latency strongly correlates with delivery delays.

- Dispatch staging inefficiencies create downstream operational bottlenecks.

- Certain city zones exhibit persistent fulfillment inefficiencies.

- Integrated operational optimization improves both SLA adherence and unit economics.

""")
