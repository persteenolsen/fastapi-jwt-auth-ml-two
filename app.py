import datetime
import os

import uvicorn
import jwt
import joblib
import pandas as pd

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Literal

# -----------------------------
# INIT APP
# -----------------------------
app = FastAPI(
    title="FastAPI + JWT + ML (v2)",
    description="18-04-2026 - House Price Prediction API with ML pipeline + JWT auth.",
    version="2.0.2",
    contact={
        "name": "Per Olsen",
        "url": "https://persteenolsen.netlify.app",
    },
)

# -----------------------------
# ENV
# -----------------------------
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
FAKE_USERNAME = os.getenv("FAKE_USERNAME")
FAKE_PASSWORD = os.getenv("FAKE_PASSWORD")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is missing in environment variables")

# -----------------------------
# AUTH
# -----------------------------
bearer = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    try:
        decoded = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=["HS256"]
        )
        return decoded["username"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

# -----------------------------
# MODEL (LAZY LOADING)
# -----------------------------
model = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

def get_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise RuntimeError("model.pkl not found. Run train.py first.")
        model = joblib.load(MODEL_PATH)
    return model

# -----------------------------
# REQUEST MODELS
# -----------------------------
class LoginRequest(BaseModel):
    username: str
    password: str


class PredictionRequest(BaseModel):
    size: float
    rooms: int
    year_built: int
    location: Literal["city", "suburb", "rural"]
    condition: Literal["poor", "fair", "good", "excellent"]

# -----------------------------
# ROUTES
# -----------------------------
@app.post("/login")
def login(req: LoginRequest):
    if req.username == FAKE_USERNAME and req.password == FAKE_PASSWORD:
        payload = {
            "username": req.username,
            "exp": datetime.datetime.now(datetime.UTC)
                   + datetime.timedelta(hours=1),
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return {"token": token}

    raise HTTPException(status_code=401, detail="Bad credentials")


@app.get("/")
def root():
    return {"message": "FastAPI + JWT + ML v2 is running"}


@app.post("/predict")
def predict(
    data: PredictionRequest,
    username: str = Depends(verify_token)
):
    model = get_model()

    try:
        input_data = data.model_dump()
        df_input = pd.DataFrame([input_data])

        prediction = model.predict(df_input)[0]

        return {
            "user": username,
            "input": input_data,
            "predicted_price": round(float(prediction), 2)
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)