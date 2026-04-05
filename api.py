

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Define FastAPI app instance
app = FastAPI()


from predictor import predict_spam, get_confidence
from database import insert_data



# SHAP Explainability Request Model
class ShapExplainRequest(BaseModel):
    message: str
    source: str = "unknown"

# Predict Request Model

# Predict Request Model
class PredictRequest(BaseModel):
    message: str
    uid: str | None = None


@app.post("/predict")
def predict(request: PredictRequest):
    label = predict_spam(request.message)
    confidence = get_confidence(request.message)
    uid = request.uid if request.uid else str(abs(hash(request.message)))
    insert_data(uid, request.message, label, confidence)
    return {
        "prediction": label,
        "confidence": confidence
    }
