# 🏠 v2 - House Price Prediction API (FastAPI + JWT + ML)

Last updated:

- 18-04-2026

A simple but production-style Machine Learning API built with FastAPI, JWT authentication, and a scikit-learn pipeline model.

This project demonstrates how to move from a basic ML script to a full backend service.

---

## 🚀 Features

- JWT authentication
- Machine Learning model (scikit-learn pipeline)
- Lazy-loaded model for performance
- Pydantic v2 request validation
- FastAPI REST API
- Synthetic housing dataset generator

---

## 📁 Project Structure

app.py → FastAPI backend (auth + prediction API)  
train.py → Model training script  
generate_data.py → Dataset generator (optional)  
housing_v2.csv → Generated dataset  
model.pkl → Trained ML model  
requirements.txt → Dependencies  
.env → Environment variables  

---

## ⚙️ Installation

### 1. Clone project

git clone <your-repo-url>  
cd <your-project-folder>  

---

### 2. Create virtual environment

python -m venv venv  

Activate virtual environment:

Windows:
venv\Scripts\activate  

Mac/Linux:
source venv/bin/activate  

---

### 3. Install dependencies

pip install -r requirements.txt  

---

## 🔐 Environment Variables (.env)

Create a file named `.env`:

SECRET_KEY=your_secret_key_here  
FAKE_USERNAME=admin  
FAKE_PASSWORD=1234  

---

## 🧠 Train the Model

(Optional) Generate dataset:

python generate_data.py  

Train model:

python train.py  

This creates:

model.pkl  

---

## 🚀 Run the API

python app.py  

API runs at:

http://127.0.0.1:8000  

---

## 📡 API Endpoints

### 🔐 Login

POST /login  

Request:
{
  "username": "admin",
  "password": "1234"
}

Response:
{
  "token": "your_jwt_token"
}

---

### 🏠 Predict House Price

POST /predict  

Header:
Authorization: Bearer <token>  

Request:
{
  "size": 140,
  "rooms": 4,
  "year_built": 2005,
  "location": "suburb",
  "condition": "good"
}

Response:
{
  "user": "admin",
  "input": {
    "size": 140,
    "rooms": 4,
    "year_built": 2005,
    "location": "suburb",
    "condition": "good"
  },
  "predicted_price": 312450.55
}

---

## 🧠 Tech Stack

- FastAPI
- scikit-learn
- pandas
- PyJWT
- Uvicorn
- Pydantic v2

---

## 📈 What this project demonstrates

- ML pipelines (not just scripts)
- REST API design for ML systems
- JWT authentication
- Model deployment basics
- Data preprocessing with ColumnTransformer

---

## 🚀 Next improvements

- Add PostgreSQL for storing predictions
- Real user authentication system
- Model versioning
- Docker deployment
- Logging + monitoring

---

## 👨‍💻 Author

Built as a learning project for combining Machine Learning with backend engineering