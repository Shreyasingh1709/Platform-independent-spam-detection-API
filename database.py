import mysql.connector

# ---------- Create Connection ----------
def create_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="spam_db"
    )
    return conn


# ---------- Insert Data ----------
def insert_data(message, prediction, confidence):
    conn = create_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO messages (message, prediction, confidence)
    VALUES (%s, %s, %s)
    """

    values = (message, prediction, confidence)

    cursor.execute(query, values)
    conn.commit()
    conn.close()


# ---------- Analytics Functions ----------

def get_spam_count():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM messages WHERE prediction='spam'")
    result = cursor.fetchone()[0]

    conn.close()
    return result


def get_ham_count():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM messages WHERE prediction='ham'")
    result = cursor.fetchone()[0]

    conn.close()
    return result