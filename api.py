from fastapi import FastAPI
from pydantic import BaseModel
from predictor import predict_spam

app = FastAPI(title="Platform Independent Spam Detection API")

class PredictRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(request: PredictRequest):
    result = predict_spam(request.text)
    return {
        "prediction": result,
        "status": "success"
    }

@app.get("/")
def home():
    return {"message": "Spam Detection API is running"}
