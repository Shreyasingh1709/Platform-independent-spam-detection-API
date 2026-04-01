import matplotlib.pyplot as plt
from database import get_spam_count, get_ham_count
import mysql.connector


# ---------- Graph 1: Spam vs Ham ----------
def plot_spam_vs_ham():
    spam = get_spam_count()
    ham = get_ham_count()

    labels = ['Spam', 'Ham']
    values = [spam, ham]

    plt.figure()
    plt.bar(labels, values)

    plt.title("Spam vs Ham Messages")
    plt.xlabel("Type")
    plt.ylabel("Count")

    plt.show()


# ---------- Graph 2: Daily Trend ----------
def plot_daily_trend():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="spam_db"
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT DATE(timestamp), COUNT(*) 
    FROM messages 
    GROUP BY DATE(timestamp)
    """)

    data = cursor.fetchall()

    dates = [str(row[0]) for row in data]
    counts = [row[1] for row in data]

    plt.figure()
    plt.plot(dates, counts, marker='o')

    plt.title("Daily Message Trend")
    plt.xlabel("Date")
    plt.ylabel("Messages")

    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.show()

    conn.close()


# ---------- MAIN ----------
if __name__ == "__main__":
    plot_spam_vs_ham()
    plot_daily_trend()