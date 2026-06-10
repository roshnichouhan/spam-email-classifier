from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
import joblib

app = FastAPI(
    title="Spam Email Detection API",
    description="Machine Learning API for detecting spam emails using a trained classification model.",
    version="1.0.0"
)

# ==================================================
# LOAD MODEL
# ==================================================

MODEL_PATH = Path("models/model.pkl")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    raise RuntimeError(f"Failed to load model: {e}")


# ==================================================
# REQUEST SCHEMA
# ==================================================

class EmailRequest(BaseModel):
    email_text: str = Field(
        ...,
        min_length=5,
        description="Email content to classify as Spam or Not Spam"
    )


# ==================================================
# ROUTES
# ==================================================

@app.get("/")
def home():
    return {
        "project": "Spam Email Classifier",
        "status": "Running",
        "model_version": "1.0",
        "api": "FastAPI"
    }


@app.get("/health")
def health_check():
    return {
        "status": "Healthy",
        "service": "Spam Detection API"
    }


@app.post("/predict")
def predict(email: EmailRequest):

    try:
        prediction = model.predict([email.email_text])[0]

        result = "Spam" if prediction == 1 else "Not Spam"

        return {
            "email_text": email.email_text,
            "prediction": result,
            "status": "Success"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
