import streamlit as st

st.title("📨 WarmUpMailer")
input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-44515?from=job%20search%20funnel")
submit = st.button("Submit Button")

if submit:
    st.code("Hi, here is your warmed up (cold) mail!", language="markdown")