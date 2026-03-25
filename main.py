from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
from datetime import datetime
import sqlite3

# Import preprocessing (Member 3)
from preprocess import preprocess_text

# Import explanation (Member 3)
from explain import get_keywords

app = FastAPI(title="Platform Independent Spam Detection API")

# ----------- Load Model (Member 2) -----------
try:
    model = pickle.load(open("model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
except:
    model = None
    vectorizer = None

# ----------- Request Schema -----------
class MessageRequest(BaseModel):
    message: str
    source: str = "unknown"   # gmail / sms / chat

# ----------- Database Connection (Member 4) -----------
def store_result(message, prediction):
    conn = sqlite3.connect("spam.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT,
        prediction TEXT,
        timestamp TEXT
    )
    """)

    cursor.execute(
        "INSERT INTO messages (message, prediction, timestamp) VALUES (?, ?, ?)",
        (message, prediction, str(datetime.now()))
    )

    conn.commit()
    conn.close()

# ----------- API Endpoint -----------
@app.post("/predict")
def predict_spam(data: MessageRequest):

    if model is None or vectorizer is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # Step 1: Preprocess
    cleaned = preprocess_text(data.message)

    # Step 2: Vectorize
    vector = vectorizer.transform([cleaned])

    # Step 3: Predict
    prediction = model.predict(vector)[0]
    confidence = max(model.predict_proba(vector)[0])

    result = "spam" if prediction == 1 else "ham"

    # Step 4: Explanation
    keywords = get_keywords(cleaned)

    # Step 5: Store in DB
    store_result(data.message, result)

    return {
        "source": data.source,
        "prediction": result,
        "confidence": round(float(confidence), 2),
        "reason": keywords
    }

# ----------- Health Check -----------
@app.get("/")
def home():
    return {"message": "Spam Detection API is running"}