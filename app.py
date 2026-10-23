import os
from contextlib import closing

import pandas as pd
import plotly.express as px
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Usage Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "ai_data_usage"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
    "port": int(os.getenv("DB_PORT", "5432")),
}

if not DB_CONFIG["password"]:
    st.error(
        "Database password is not configured. Create a local .env file "
        "based on .env.example and set DB_PASSWORD."
    )
    st.stop()


@st.cache_data(ttl=60)
def load_dashboard_data():
    """Load data from PostgreSQL and close the connection reliably."""
    with closing(psycopg2.connect(**DB_CONFIG)) as connection:
        data = pd.read_sql_query(
            """
            SELECT date, model, prompts, tokens, cost, response_time
            FROM usage_data
            """,
            connection,
        )
        analytics = pd.read_sql_query(
            """
            SELECT
                model,
                SUM(prompts) AS total_prompts,
                SUM(tokens) AS total_tokens,
                SUM(cost) AS total_cost,
                AVG(response_time) AS avg_response_time
            FROM usage_data
            GROUP BY model
            ORDER BY total_prompts DESC
            """,
            connection,
        )
    return data, analytics


try:
    data, analytics_data = load_dashboard_data()
except (psycopg2.Error, pd.errors.DatabaseError) as exc:
    st.error(
        "Could not load dashboard data. Check that PostgreSQL is running, "
        "the database credentials are correct, and the usage_data table exists."
    )
    st.caption(f"Database error type: {type(exc).__name__}")
    st.stop()

if data.empty:
    st.warning("The usage_data table is empty. Load sample records to explore the dashboard.")
    st.stop()

st.title("AI Usage Analytics Dashboard")
st.caption("Explore model usage, token volume, estimated cost, and response-time patterns.")

st.subheader("Model overview")
if analytics_data.empty:
    st.info("No model-level analytics are available yet.")
else:
    c1, c2, c3 = st.columns(3)
    c1.metric("Most Used Model", str(analytics_data.iloc[0]["model"]))
    highest_cost = analytics_data.loc[analytics_data["total_cost"].idxmax()]
    fastest = analytics_data.loc[analytics_data["avg_response_time"].idxmin()]
    c2.metric("Highest Cost Model", str(highest_cost["model"]))
    c3.metric("Fastest Average Response", str(fastest["model"]))

st.subheader("Filter data")
models = sorted(data["model"].dropna().unique().tolist())
selected_models = st.sidebar.multiselect("AI models", models, default=models)
filtered_data = data[data["model"].isin(selected_models)]

if filtered_data.empty:
    st.info("Choose at least one model to display metrics.")
    st.stop()

total_prompts = filtered_data["prompts"].sum()
total_tokens = filtered_data["tokens"].sum()
total_cost = filtered_data["cost"].sum()
average_response_time = filtered_data["response_time"].mean()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Prompts", f"{total_prompts:,.0f}")
c2.metric("Total Tokens", f"{total_tokens:,.0f}")
c3.metric("Total Cost", f"{total_cost:,.2f}")
c4.metric(
    "Avg. Response Time",
    f"{average_response_time:,.2f}" if pd.notna(average_response_time) else "N/A",
)

left, right = st.columns(2)
with left:
    st.subheader("Prompts by model")
    prompts_by_model = filtered_data.groupby("model", as_index=False)["prompts"].sum()
    st.plotly_chart(
        px.bar(prompts_by_model, x="model", y="prompts", color="model"),
        use_container_width=True,
    )
with right:
    st.subheader("Token usage share")
    tokens_by_model = filtered_data.groupby("model", as_index=False)["tokens"].sum()
    if tokens_by_model["tokens"].sum() > 0:
        st.plotly_chart(
            px.pie(tokens_by_model, names="model", values="tokens", hole=0.35),
            use_container_width=True,
        )
    else:
        st.info("No token usage recorded for the selected models.")

st.subheader("Cost trend")
cost_by_date = filtered_data.copy()
cost_by_date["date"] = pd.to_datetime(cost_by_date["date"], errors="coerce")
cost_by_date = cost_by_date.dropna(subset=["date"]).groupby(
    "date", as_index=False
)["cost"].sum()
if not cost_by_date.empty:
    st.plotly_chart(
        px.line(cost_by_date, x="date", y="cost", markers=True),
        use_container_width=True,
    )
else:
    st.info("No valid dates are available for the cost trend.")

st.subheader("Model analytics")
st.dataframe(
    filtered_data.groupby("model", as_index=False).agg(
        total_prompts=("prompts", "sum"),
        total_tokens=("tokens", "sum"),
        total_cost=("cost", "sum"),
        avg_response_time=("response_time", "mean"),
    ),
    use_container_width=True,
)

st.subheader("Filtered records")
st.dataframe(filtered_data, use_container_width=True)

st.download_button(
    label="Download filtered CSV",
    data=filtered_data.to_csv(index=False),
    file_name="ai_usage_report.csv",
    mime="text/csv",
)
