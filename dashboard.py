import streamlit as st
import requests
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

st.title("📊 Spam Detection Dashboard")

# -------- INPUT ----------
user_input = st.text_area("Enter message")

if st.button("Predict"):
    
    data = {
        "message": user_input,
        "source": "dashboard"
    }

    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=data)
        result = response.json()

        st.success("Prediction completed")

        st.write("### Result")
        st.write("Prediction:", result["prediction"])
        st.write("Confidence:", result["confidence"])
        st.write("Keywords:", result["reason"])

    except:
        st.error("API not running")

# -------- DATABASE GRAPH ----------
st.write("### Prediction History")

conn = sqlite3.connect("spam.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS messages (message TEXT, prediction TEXT, confidence REAL)")
conn.commit()

df = pd.read_sql_query("SELECT * FROM messages", conn)

if not df.empty:

    spam_count = len(df[df["prediction"]=="spam"])
    ham_count = len(df[df["prediction"]=="ham"])

    fig, ax = plt.subplots()

    ax.bar(["Spam","Ham"], [spam_count, ham_count])
    ax.set_title("Spam vs Ham")

    st.pyplot(fig)

    st.dataframe(df)

else:
    st.write("No data yet")