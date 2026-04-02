from fastapi import FastAPI
from pydantic import BaseModel
from predictor import predict_spam, get_confidence
from explain import get_shap_explanation, initialize_explainer
import pickle

app = FastAPI(title="Platform Independent Spam Detection API")

# Load model and vectorizer for explainer
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
initialize_explainer(model, vectorizer)

class PredictRequest(BaseModel):
    message: str
    source: str = "unknown"

@app.post("/predict")
def predict(request: PredictRequest):
    result = predict_spam(request.message)
    confidence = get_confidence(request.message)
    reason = get_shap_explanation(request.message)
    
    # Store in database
    conn = sqlite3.connect("spam.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS messages (message TEXT, prediction TEXT, confidence REAL)")
    cursor.execute("INSERT INTO messages (message, prediction, confidence) VALUES (?, ?, ?)", (request.message, result, confidence))
    conn.commit()
    conn.close()
    
    return {
        "prediction": result,
        "confidence": confidence,
        "reason": reason
    }

@app.get("/")
def home():
    return {"message": "Spam Detection API is running"}
