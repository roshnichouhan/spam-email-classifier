from fastapi import FastAPI
from pydantic import BaseModel
import pickle
from src.predict import predict_message

app = FastAPI(title="Spam Classifier API")

# load model
model = pickle.load(open("models/model.pkl", "rb"))

class Request(BaseModel):
    message: str


@app.get("/")
def home():
    return {"message": "API Running Successfully 🚀"}


@app.post("/predict")
def predict(req: Request):
    result = predict_message(model, req.message)

    return {
        "prediction": "Spam" if result == 1 else "Not Spam"
    }