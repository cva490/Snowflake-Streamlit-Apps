

import streamlit as st
import pandas as pd

# Streamlit app title
st.title("Streamlit Filters Example")

# Sample data
data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"],
    "Age": [25, 30, 35, 40, 28, 32],
    "Country": ["USA", "UK", "Canada", "Australia", "USA", "Canada"],
    "Sales": [1000, 1500, 2000, 2500, 1200, 1800]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Sidebar filters
st.sidebar.header("Filters")

# Filter by country
selected_country = st.sidebar.multiselect(
    "Select Country",
    options=df["Country"].unique(),
    default=df["Country"].unique()
)

# Filter by age range
min_age, max_age = st.sidebar.slider(
    "Select Age Range",
    min_value=int(df["Age"].min()),
    max_value=int(df["Age"].max()),
    value=(int(df["Age"].min()), int(df["Age"].max()))
)

# Apply filters
filtered_df = df[
    (df["Country"].isin(selected_country)) &
    (df["Age"] >= min_age) &
    (df["Age"] <= max_age)
]

# Display filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_df)

# Optional: show total sales for filtered data
st.metric(label="Total Sales", value=filtered_df["Sales"].sum())
