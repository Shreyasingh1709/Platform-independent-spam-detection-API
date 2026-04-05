import mysql.connector

# ---------- Create Connection ----------
def create_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="sh170903@",
        database="spam_db"
    )
    # Ensure table exists
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT,
            prediction VARCHAR(10),
            confidence FLOAT,
            label VARCHAR(10),
            uid VARCHAR(255) UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Try to add uid column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE messages ADD COLUMN uid VARCHAR(255) UNIQUE")
    except Exception as e:
        # Ignore error if column already exists
        if 'Duplicate column name' not in str(e):
            print(f"[DB] Warning: {e}")
    # Try to add created_at column if it doesn't exist
    try:
        cursor.execute("ALTER TABLE messages ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    except Exception as e:
        if 'Duplicate column name' not in str(e):
            print(f"[DB] Warning: {e}")
    conn.commit()
    return conn


# ---------- Insert Data ----------
def insert_data(uid, message, prediction, confidence):
    conn = create_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO messages (uid, message, prediction, confidence, label)
    VALUES (%s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        message=VALUES(message),
        prediction=VALUES(prediction),
        confidence=VALUES(confidence)
    """
    # Default label to None for now
    values = (uid, message, prediction, confidence, None)
    cursor.execute(query, values)
    conn.commit()
    conn.close()

# Check if UID exists
def uid_exists(uid):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM messages WHERE uid=%s LIMIT 1", (uid,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


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