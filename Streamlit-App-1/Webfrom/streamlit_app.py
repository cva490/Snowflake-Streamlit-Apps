import streamlit as st
import pandas as pd
import numpy as np

# --- PAGE SETUP ---
st.set_page_config(page_title="Advanced Editable Table", layout="wide")
st.title("💼 Employee Management Dashboard")

# --- SAMPLE DATA ---
@st.cache_data
def load_data():
    np.random.seed(42)
    return pd.DataFrame({
        "ID": range(1, 11),
        "Name": ["Alice", "Bob", "Charlie", "Diana", "Ethan", "Fiona", "George", "Hannah", "Ian", "Julia"],
        "Department": np.random.choice(["HR", "Finance", "IT", "Marketing", "Sales"], 10),
        "Age": np.random.randint(25, 60, 10),
        "Salary": np.random.randint(40000, 120000, 10),
        "Performance": np.random.choice(["Excellent", "Good", "Average", "Poor"], 10)
    })

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("🧭 Filters")

selected_dept = st.sidebar.multiselect(
    "Select Department(s):", options=df["Department"].unique(), default=df["Department"].unique()
)

age_range = st.sidebar.slider(
    "Select Age Range:", int(df["Age"].min()), int(df["Age"].max()), (25, 60)
)

search_name = st.sidebar.text_input("🔍 Search by Name:")

# --- APPLY FILTERS ---
filtered_df = df[
    (df["Department"].isin(selected_dept)) &
    (df["Age"].between(age_range[0], age_range[1]))
]

if search_name:
    filtered_df = filtered_df[filtered_df["Name"].str.contains(search_name, case=False)]

st.subheader("📋 Editable Employee Table")

# --- EDITABLE TABLE ---
edited_df = st.data_editor(
    filtered_df,
    num_rows="dynamic",
    use_container_width=True,
    key="editable_table",
    column_config={
        "Salary": st.column_config.NumberColumn("Salary ($)", min_value=30000, max_value=200000, step=1000),
        "Performance": st.column_config.SelectboxColumn(
            "Performance Rating", options=["Excellent", "Good", "Average", "Poor"]
        )
    }
)

# --- SAVE / EXPORT SECTION ---
col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    if st.button("💾 Save Changes"):
        st.session_state["saved_data"] = edited_df
        st.success("✅ Changes saved in session!")

with col2:
    csv = edited_df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download CSV", data=csv, file_name="edited_data.csv", mime="text/csv")

# --- SHOW SAVED DATA (FROM SESSION) ---
if "saved_data" in st.session_state:
    st.markdown("### 🗂️ Previously Saved Data")
    st.dataframe(st.session_state["saved_data"], use_container_width=True)

# --- ANALYTICS / CHARTS ---
st.markdown("---")
st.subheader("📊 Analytics")

tab1, tab2 = st.tabs(["📈 Salary Distribution", "🏆 Performance Breakdown"])

with tab1:
    st.bar_chart(edited_df.groupby("Department")["Salary"].mean(), use_container_width=True)

with tab2:
    perf_counts = edited_df["Performance"].value_counts()
    st.bar_chart(perf_counts, use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.markdown(
    "<center>Built with ❤️ using Streamlit | Demo Dashboard © 2025</center>",
    unsafe_allow_html=True
)
