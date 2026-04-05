
# --- All imports at the top ---
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import database
import email_client
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv



# --- Hardcoded SQL password (URL-encoded @ as %40) ---
sql_password = "sh170903%40"

# --- Streamlit App Title ---
st.title("📧 Email Spam Detection Dashboard")

# Fetch and categorize recent emails
if st.button("Fetch and Categorize Recent Emails"):
    with st.spinner("Fetching and categorizing emails..."):
        email_client.fetch_and_detect()
    st.success("Fetched and categorized recent emails!")

# -------- DATABASE ANALYTICS ----------
st.write("### Email Prediction Analytics")

try:    
    # Connect to MySQL database
    # Connect to MySQL database using SQLAlchemy
    engine = create_engine(f"mysql+mysqlconnector://root:{sql_password}@localhost:3306/spam_db")
    # Fetch recent emails
    df = pd.read_sql("SELECT * FROM messages ORDER BY id DESC LIMIT 20", engine)
    # Remove label column if present
    if 'label' in df.columns:
        df = df.drop(columns=['label'])
    spam_count = database.get_spam_count()
    ham_count = database.get_ham_count()

    # Spam vs Ham bar chart
    fig, ax = plt.subplots()
    ax.bar(["Spam", "Ham"], [spam_count, ham_count], color=["red", "green"])
    ax.set_title("Spam vs Ham (All Emails)")
    st.pyplot(fig)

    # Daily trend graph for spam and ham
    st.write("### Daily Trend: Spam vs Ham")
    try:
        trend_query = """
            SELECT created_at, prediction FROM messages
        """
        trend_df = pd.read_sql(trend_query, engine)
        # Parse dates and drop rows with missing/invalid dates
        trend_df['created_at'] = pd.to_datetime(trend_df['created_at'], errors='coerce')
        trend_df = trend_df.dropna(subset=['created_at'])
        # Group by week
        trend_df['week'] = trend_df['created_at'].dt.to_period('W').apply(lambda r: r.start_time)
        # Group by week and prediction
        trend_grouped = trend_df.groupby(['week', 'prediction']).size().reset_index(name='count')
        # Pivot for plotting
        trend_pivot = trend_grouped.pivot(index='week', columns='prediction', values='count').fillna(0)
        # Show only the last 8 weeks
        last_n = 8
        trend_pivot_recent = trend_pivot.tail(last_n)
        week_labels = [d.strftime('%Y-%m-%d') for d in trend_pivot_recent.index]
        x = range(len(week_labels))
        spam_counts = trend_pivot_recent['spam'] if 'spam' in trend_pivot_recent else [0]*len(week_labels)
        ham_counts = trend_pivot_recent['ham'] if 'ham' in trend_pivot_recent else [0]*len(week_labels)
        # Rolling average (window=4)
        spam_smooth = pd.Series(spam_counts).rolling(window=4, min_periods=1).mean()
        ham_smooth = pd.Series(ham_counts).rolling(window=4, min_periods=1).mean()
        fig2, ax2 = plt.subplots(figsize=(14, 6))
        ax2.plot(x, spam_smooth, label='Spam (4-week avg)', color='red', marker='o')
        ax2.plot(x, ham_smooth, label='Ham (4-week avg)', color='green', marker='o')
        ax2.set_title('Weekly Trend of Spam and Ham Emails (Last 8 Weeks, 4-week Rolling Avg)')
        ax2.set_xlabel('Week')
        ax2.set_ylabel('Count')
        ax2.set_xticks(x)
        ax2.set_xticklabels(week_labels, rotation=45, ha='right', fontsize=10)
        ax2.legend()
        fig2.tight_layout()
        st.pyplot(fig2)
    except Exception as e:
        st.warning(f"Could not plot daily trend graph: {e}")

    st.write("### Recent Emails (last 20)")
    # Show confidence as percentage if present
    if 'confidence' in df.columns:
        df['confidence'] = pd.to_numeric(df['confidence'], errors='coerce')
        df['confidence'] = df['confidence'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "")
    st.dataframe(df)

    # --- Single Message Prediction Section ---
    st.write("### Predict Email with Naive Bayes")
    try:
        from predictor import predict_spam
        user_input = st.text_area("Enter email text to predict:")
        if st.button("Predict Spam/Ham"):
            if user_input.strip():
                pred = predict_spam(user_input)
                st.write(f"Prediction: **{pred}**")
            else:
                st.warning("Please enter some text.")
    except Exception as e:
        st.error(f"Prediction error: {e}")
    # No need to close SQLAlchemy engine
except Exception as e:
    st.error(f"Error loading analytics: {e}")