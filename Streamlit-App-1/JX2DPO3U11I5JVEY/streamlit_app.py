# Import python packages
import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import numpy as np
from snowflake.snowpark.context import get_active_session

# Write directly to the app
st.markdown("""
    <style>
div.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 12em;
    font-weight: bold;
}
div.stButton > button:hover {
    background-color: #45a049;
}

/* Style metrics */
[data-testid="stMetricValue"] {
    color: #FF5733;
    font-weight: 700;
    font-size: 22px;
}
[data-testid="stMetricLabel"] {
    color: #555;
    font-size: 16px;
}
</style>

    """, unsafe_allow_html=True)
st.write(
  """
    Goal is to understand:\n 
    ✅ Streamlit capabilities\n
    ✅ Challenges to build dashboard using Streamlit
  """
)

# Get the current credentials
session = get_active_session()


# Create sample data
np.random.seed(42)
df = pd.DataFrame({
    "City": np.random.choice(["New York", "London", "Tokyo", "Sydney"], 100),
    "Year": np.random.choice([2023, 2024, 2025], 100),
    "Sales": np.random.randint(100, 1000, 100),
    "Profit": np.random.uniform(10, 100, 100)
})

results_data = {
    'RUN_ID':[1080,1043,1077],
    'CHECK_ID':[31,36,31],
    'PROCESS_START_TIME':['2025-11-07 18:30:20.167000000','2025-11-07 11:56:15.023000000','2025-11-07 18:29:00.776000000'],
    'PROCESS_END_TIME':['2025-11-07 18:30:20.706000000','2025-11-07 11:56:16.106000000','2025-11-07 18:29:01.663000000'],
    'REPORT_DATE':['2025-11-07','2025-11-07','2025-11-06'],
    'OUTCOME':['Fail','Success','Fail'],
    'FAILED_COUNT':[0,0,0],
    'REASON':['hard_bus_na_tst_2_0Positive failed for date 2025-11-07','','hard_bus_na_tst_2_0Positive failed for date 2025-11-06'],
    'RUN_TYPE':['AUTO','AUTO','AUTO'],
    'RUN_QUERY':['select * from DEV_USERS.TEAM_CDW_QA.SDU_TEST','SELECT COUNT(*),LIST_ID,USER_NAME FROM DEV_USERS.TEAM_CDW_QA.SDU_TEST GROUP BY LIST_ID,USER_NAME HAVING COUNT(*)>1','select * from DEV_USERS.TEAM_CDW_QA.SDU_TEST where report_date = 2025-11-06'],
    'SNOWFLAKE_SESSION_ID':['42780910106820523','42780910106616923','42780910106820523'],
    'RUN_BY_USER':['RALUCA.MOISE@LSEG.COM','SIMONA.DUTA@LSEG.COM','RALUCA.MOISE@LSEG.COM'],
    'DYNAMIC_FILTER_VALUES':['','',''],
    'MATILLION_RUN_HISTORY_ID':[99,100,101]
}
df_results = pd.DataFrame(results_data)

st.subheader("Results Data")
st.dataframe(df_results)
#st.subheader("Raw Data")
#st.dataframe(df)

# --- FILTERS ---
st.sidebar.header("🧭 Filters")

# Dropdown filter
selected_city = st.sidebar.multiselect("Select City", options=df["City"].unique(), default=df["City"].unique())

# Slider filter
selected_year = st.sidebar.selectbox("Select Year", options=sorted(df["Year"].unique()))

st.markdown("### 📊 Key Performance Metrics")

with st.container(border=True,horizontal=True, horizontal_alignment="left"):
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("💵 Revenue", "$12,000", "+5%",border=True, width="content")
    with col2:
        st.metric("💰 Net Profit", "$7,500", "+8%", border=True, width="content")
    with col3:
        st.metric("💸 Expenses", "$4,500", "-2%", border=True, width="content")
    with col4:        
        st.metric("📊 EBITDA", "$35K", "+7%", border=True, width="content")
    with col5:        
        st.metric("📦 Orders Processed", "1,245", "+12%", border=True, width="content")



df = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Revenue": [12000, 15000, 14000, 17000, 18000, 21000]
})

st.dataframe(df);

tabs = st.tabs(["Monthly Revenue Growth","Revenue vs Expenses","Revenue Over the Months"])



fig = px.bar(
    df,
    x="Month",
    y="Revenue",
    text_auto=True,
    color="Revenue",
    color_continuous_scale="Blues",
    title="📊 Monthly Revenue Growth"
)

fig.update_traces(marker_line_color='black', marker_line_width=1.2)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(size=14),
    title_x=0.5
)

with tabs[0]:
    st.plotly_chart(fig, use_container_width=True)


data = pd.DataFrame({
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"] * 2,
    "Value": [12000, 15000, 14000, 17000, 18000, 21000,
              8000, 9000, 9500, 10000, 11000, 12000],
    "Type": ["Revenue"] * 6 + ["Expenses"] * 6
})

chart = (
    alt.Chart(data)
    .mark_bar()
    .encode(
        x="Month:N",
        y="Value:Q",
        color="Type:N",
        tooltip=["Month", "Type", "Value"]
    )
    .properties(width="container", height=350, title="Revenue vs Expenses")
)

with tabs[1]:
    st.altair_chart(chart, use_container_width=True)

dates = pd.date_range(start="2025-01-01", periods=30, freq="D")

# Generate some example data (Y-axis)
sales = np.random.randint(100, 500, size=30)

# Create DataFrame
df = pd.DataFrame({
    "Date": dates,
    "Sales": sales
})

# Set Date as index (common for line charts)
df = df.set_index("Date")

with tabs[2]:
    st.line_chart(df)

#st.header('test')
data = np.random.rand(10, 10)
df = pd.DataFrame(data, columns=[f"C{i}" for i in range(10)])

# Plotly heatmap
fig = px.imshow(df, text_auto=True, color_continuous_scale="Viridis")
st.plotly_chart(fig, use_container_width=True)