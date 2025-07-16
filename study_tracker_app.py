
import streamlit as st
import pandas as pd
import io
import json
from datetime import date, datetime
import plotly.express as px

st.set_page_config(page_title="CA Final Study Tracker", layout="centered")

# Load quotes
def load_quotes():
    try:
        with open("365_quotes.txt", "r") as f:
            return [line.strip().split(":", 1)[1].strip() for line in f.readlines()]
    except:
        return ["Stay consistent. You are getting closer every day."] * 365

# Load badges (dummy loader for now)
def load_badges():
    try:
        with open("badges.json", "r") as f:
            return json.load(f)["badges"]
    except:
        return []

# Initialize session state
if "data" not in st.session_state:
    st.session_state["data"] = pd.DataFrame(columns=["Date", "Subject", "Minutes"])

# Light/Dark Mode Toggle
theme = st.radio("Choose Theme", ["🌞 Light Mode", "🌙 Dark Mode"], horizontal=True)
if theme == "🌙 Dark Mode":
    st.markdown('<style>body { background-color: #0e1117; color: white; }</style>', unsafe_allow_html=True)

# App starts here
st.title("📘 CA Final Study Tracker")

name = st.text_input("Enter your name to begin:")
if name:
    st.success(f"{name}, you will succeed and clear CA Final with Rank 💪")

    # Motivation
    quotes = load_quotes()
    today_index = (date.today() - date(date.today().year, 1, 1)).days % 365
    st.markdown(f"💬 **Motivation of the Day:** _{quotes[today_index]}_")

    st.divider()

    # Import section
    with st.expander("📂 Import Previous Tracker (.xlsx)"):
        uploaded = st.file_uploader("Upload Excel file to continue from previous sessions", type=["xlsx"])
        if uploaded:
            df = pd.read_excel(uploaded)
            st.session_state["data"] = pd.concat([st.session_state["data"], df], ignore_index=True)
            st.success("Previous data imported successfully!")

    st.header("📥 Add Study Entry")
    col1, col2, col3 = st.columns(3)
    with col1:
        study_date = st.date_input("Date", value=date.today())
    with col2:
        subject = st.selectbox("Subject", ["FR", "SFM", "Audit", "Law", "DT", "IDT", "Elective"])
    with col3:
        minutes = st.number_input("Minutes Studied", min_value=0, step=1)

    if st.button("Add Entry"):
        new_row = pd.DataFrame([[study_date, subject, minutes]], columns=["Date", "Subject", "Minutes"])
        st.session_state["data"] = pd.concat([st.session_state["data"], new_row], ignore_index=True)
        st.success("Entry added successfully!")

    st.divider()
    st.header("📊 Study Log This Session")

    if not st.session_state["data"].empty:
        df = st.session_state["data"]
        st.dataframe(df, use_container_width=True)

        # Excel export
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        st.download_button(
            label="📤 Download Tracker Excel",
            data=output,
            file_name="Study_Tracker.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # Weekly Summary Graph
        df["Week"] = pd.to_datetime(df["Date"]).dt.to_period("W").astype(str)
        week_summary = df.groupby(["Week", "Subject"])["Minutes"].sum().reset_index()
        chart = px.bar(week_summary, x="Week", y="Minutes", color="Subject", barmode="group",
                       title="📅 Weekly Study Summary")
        st.plotly_chart(chart, use_container_width=True)

    else:
        st.info("No data entered yet.")
