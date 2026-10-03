import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import requests
import joblib

app = FastAPI(title="AgriAI Crop Recommendation API")

# Allow frontend requests (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Robust model path resolution
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'crop_recommendation_model.pkl')
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.join(BASE_DIR, 'model.pkl')

model = joblib.load(MODEL_PATH)

class PredictionInput(BaseModel):
    lat: float
    lon: float
    N: float
    P: float
    K: float
    ph: float

def get_satellite_weather_data(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,rain&timezone=auto"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json().get('current', {})
        temp = data.get('temperature_2m', 25.0)
        humidity = data.get('relative_humidity_2m', 65.0)
        rainfall = data.get('rain', 0.0) * 10.0
        return temp, humidity, rainfall
    else:
        # Fallback default weather
        return 26.0, 65.0, 50.0

@app.get("/")
@app.get("/health")
def health_check():
    return {"status": "online", "model_loaded": True, "engine": "AgriAI FastAPI Engine"}

@app.post("/predict")
def predict_crop(data: PredictionInput):
    temperature, humidity, rainfall = get_satellite_weather_data(data.lat, data.lon)
    
    input_df = pd.DataFrame([{
        'N': data.N,
        'P': data.P,
        'K': data.K,
        'temperature': temperature,
        'humidity': humidity,
        'ph': data.ph,
        'rainfall': rainfall
    }])
    
    predicted_crop = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    confidence = round(float(max(probabilities)) * 100, 2)
    
    return {
        "status": "success",
        "recommended_crop": str(predicted_crop),
        "confidence": confidence,
        "weather_data": {
            "temperature": temperature,
            "humidity": humidity,
            "rainfall": rainfall
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)