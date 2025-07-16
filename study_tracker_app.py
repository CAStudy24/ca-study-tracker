import streamlit as st
import pandas as pd
from datetime import date
import json

st.set_page_config(page_title="CA Final Study Tracker", layout="centered")

# Load motivational quotes
with open("365_quotes.txt", "r") as f:
    quotes = f.readlines()

today_index = (date.today() - date(date.today().year, 1, 1)).days % 365

# Title
user_name = st.text_input("Enter your name to begin:")
if user_name:
    st.markdown(f"### {user_name}, you will succeed and clear CA Final with Rank 🎯")
    st.markdown(f"💬 **Motivation of the Day:** _{quotes[today_index].strip()}_")

    st.markdown("---")
    st.markdown("### Study Entry")
    uploaded = st.file_uploader("Upload your previous Excel (optional)", type="xlsx")
    data = pd.DataFrame(columns=["Date", "Subject", "Minutes"])
    if uploaded:
        data = pd.read_excel(uploaded)

    date_input = st.date_input("Study Date", date.today())
    subject = st.selectbox("Subject", ["FR", "SFM", "Audit", "Law", "DT", "IDT", "Elective"])
    minutes = st.number_input("Minutes Studied", min_value=0)

    if st.button("Add Entry"):
        new_entry = pd.DataFrame([[date_input, subject, minutes]], columns=["Date", "Subject", "Minutes"])
        data = pd.concat([data, new_entry], ignore_index=True)
        st.success("Entry added.")

    st.markdown("### Study Data")
    st.dataframe(data)

    if st.download_button("Download Tracker Excel", data.to_excel(index=False), file_name="Study_Tracker.xlsx"):
        st.success("Download started.")
