import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression

# Load data
df = pd.read_csv("housing_v2.csv")

# Target
y = df["price"]

# Features
numeric_features = ["size", "rooms", "year_built"]
categorical_features = ["location", "condition"]

X = df[numeric_features + categorical_features]

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
    ]
)

# Pipeline
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("regressor", LinearRegression())
    ]
)

# Split
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

# Train
model.fit(X_train, y_train)

# Evaluate
score = model.score(X_val, y_val)
print("Validation score:", score)

# Save
joblib.dump(model, "model.pkl")

print("Model saved as model.pkl")