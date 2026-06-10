import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2


# CONNECT TO POSTGRESQL

connection = psycopg2.connect(
    host="localhost",
    database="ai_data_usage",
    user="postgres",
    password="123raju"
)


# LOAD ALL DATA

query = "SELECT * FROM usage_data"

data = pd.read_sql(query, connection)


# SQL ANALYTICS QUERY

analytics_query = """
SELECT
    model,
    SUM(prompts) AS total_prompts,
    SUM(tokens) AS total_tokens,
    SUM(cost) AS total_cost,
    AVG(response_time) AS avg_response_time

FROM usage_data

GROUP BY model

ORDER BY total_prompts DESC
"""

# Most Used Model

most_used_query = """
SELECT model
FROM usage_data
GROUP BY model
ORDER BY SUM(prompts) DESC
LIMIT 1
"""

most_used_model = pd.read_sql(
    most_used_query,
    connection
)


# Highest Cost Model

highest_cost_query = """
SELECT model
FROM usage_data
GROUP BY model
ORDER BY SUM(cost) DESC
LIMIT 1
"""

highest_cost_model = pd.read_sql(
    highest_cost_query,
    connection
)


# Fastest Model

fastest_model_query = """
SELECT model
FROM usage_data
GROUP BY model
ORDER BY AVG(response_time)
LIMIT 1
"""

fastest_model = pd.read_sql(
    fastest_model_query,
    connection
)


analytics_data = pd.read_sql(
    analytics_query,
    connection
)


# Close database connection
connection.close()


# DASHBOARD TITLE

st.title("AI Usage Analytics Dashboard")

st.subheader("Business Insights")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Most Used Model",
    most_used_model.iloc[0]["model"]
)

c2.metric(
    "Highest Cost Model",
    highest_cost_model.iloc[0]["model"]
)

c3.metric(
    "Fastest Model",
    fastest_model.iloc[0]["model"]
)


# SQL ANALYTICS SUMMARY

st.subheader("AI Model Analytics Summary")

st.dataframe(analytics_data)


# SIDEBAR FILTER

st.sidebar.header("Filter Data")

model_list = data["model"].unique()

selected_models = st.sidebar.multiselect(
    "Choose AI Model",
    model_list,
    default=model_list
)


# FILTER DATA

filtered_data = data[
    data["model"].isin(selected_models)
]


# SHOW DATASET

st.subheader("Dataset")

st.dataframe(filtered_data)


# KPI CALCULATIONS

total_prompts = filtered_data["prompts"].sum()

total_tokens = filtered_data["tokens"].sum()

total_cost = filtered_data["cost"].sum()

average_response_time = filtered_data["response_time"].mean()


# KPI CARDS

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Prompts",
    total_prompts
)

col2.metric(
    "Total Tokens",
    total_tokens
)

col3.metric(
    "Total Cost",
    total_cost
)

col4.metric(
    "Average Response Time",
    round(average_response_time, 2)
)


# BAR CHART

st.subheader("Prompts Used By AI Models")

bar_chart = px.bar(
    filtered_data,
    x="model",
    y="prompts",
    color="model"
)

st.plotly_chart(bar_chart)


# PIE CHART

st.subheader("Token Usage Share")

pie_chart = px.pie(
    filtered_data,
    names="model",
    values="tokens"
)

st.plotly_chart(pie_chart)


# LINE CHART

st.subheader("Daily Cost Trend")

line_chart = px.line(
    filtered_data,
    x="date",
    y="cost",
    markers=True
)

st.plotly_chart(line_chart)


# DOWNLOAD REPORT

csv_data = filtered_data.to_csv(
    index=False
)

st.download_button(
    label="Download Report",
    data=csv_data,
    file_name="AI_Report.csv",
    mime="text/csv"
)


# PANDAS ANALYTICS

st.subheader("AI Model Comparison")

comparison_table = filtered_data.groupby(
    "model"
).agg({
    "prompts": "sum",
    "tokens": "sum",
    "cost": "sum",
    "response_time": "mean"
})

st.dataframe(comparison_table)
