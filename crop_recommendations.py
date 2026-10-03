import React, { useState } from 'react';

interface WeatherData {
  temperature: number;
  humidity: number;
  rainfall: number;
}

interface PredictionResponse {
  status: string;
  recommended_crop: string;
  confidence: number;
  weather_data: WeatherData;
}

export default function CropPrediction() {
  const [formData, setFormData] = useState({
    lat: 22.5726,
    lon: 88.3639,
    N: 90,
    P: 42,
    K: 43,
    ph: 6.5,
  });

  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: parseFloat(e.target.value) || 0,
    });
  };

  const handlePredictCrop = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.statusText}`);
      }

      const data: PredictionResponse = await response.json();
      console.log("Prediction Result:", data);
      
      // Update state with response data
      setResult(data);
    } catch (err) {
      console.error("Error connecting to Python backend:", err);
      setError("Failed to connect to backend server. Ensure Uvicorn is running on port 8000.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto my-10 p-6 bg-white rounded-xl shadow-md border border-gray-100">
      <h2 className="text-2xl font-bold text-[#1D2916] mb-6 text-center">
        🌾 Crop Recommendation Engine
      </h2>

      <form onSubmit={handlePredictCrop} className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Latitude</label>
            <input
              type="number"
              step="any"
              name="lat"
              value={formData.lat}
              onChange={handleChange}
              required
              className="mt-1 w-full p-2 border border-gray-300 rounded-md focus:ring-[#18310E] focus:border-[#18310E]"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Longitude</label>
            <input
              type="number"
              step="any"
              name="lon"
              value={formData.lon}
              onChange={handleChange}
              required
              className="mt-1 w-full p-2 border border-gray-300 rounded-md focus:ring-[#18310E] focus:border-[#18310E]"
            />
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Nitrogen (N)</label>
            <input
              type="number"
              name="N"
              value={formData.N}
              onChange={handleChange}
              required
              className="mt-1 w-full p-2 border border-gray-300 rounded-md focus:ring-[#18310E] focus:border-[#18310E]"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Phosphorus (P)</label>
            <input
              type="number"
              name="P"
              value={formData.P}
              onChange={handleChange}
              required
              className="mt-1 w-full p-2 border border-gray-300 rounded-md focus:ring-[#18310E] focus:border-[#18310E]"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Potassium (K)</label>
            <input
              type="number"
              name="K"
              value={formData.K}
              onChange={handleChange}
              required
              className="mt-1 w-full p-2 border border-gray-300 rounded-md focus:ring-[#18310E] focus:border-[#18310E]"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">Soil pH</label>
          <input
            type="number"
            step="0.1"
            name="ph"
            value={formData.ph}
            onChange={handleChange}
            required
            className="mt-1 w-full p-2 border border-gray-300 rounded-md focus:ring-[#18310E] focus:border-[#18310E]"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3 bg-[#18310E] text-white font-semibold rounded-md hover:bg-[#2c521b] transition duration-200 disabled:opacity-50"
        >
          {loading ? "Fetching Weather & Predicting..." : "Get Crop Recommendation"}
        </button>
      </form>

      {/* Error Banner */}
      {error && (
        <div className="mt-6 p-4 bg-red-50 border border-red-200 text-red-700 rounded-md text-sm">
          {error}
        </div>
      )}

      {/* Results Display */}
      {result && (
        <div className="mt-6 p-5 bg-[#FBF9F4] border border-[#E2EED9] rounded-lg space-y-3">
          <div className="flex justify-between items-center">
            <span className="text-sm font-medium text-gray-600">Recommended Crop</span>
            <span className="px-3 py-1 bg-green-100 text-green-800 font-bold uppercase rounded-full text-sm">
              {result.recommended_crop}
            </span>
          </div>

          <div className="flex justify-between items-center text-sm">
            <span className="text-gray-600">Confidence Score</span>
            <span className="font-semibold text-gray-800">{result.confidence}%</span>
          </div>

          <hr className="border-gray-200 my-2" />

          <h4 className="text-sm font-semibold text-gray-700">Live Satellite Weather Data</h4>
          <div className="grid grid-cols-3 gap-2 text-xs text-center">
            <div className="p-2 bg-white rounded border">
              <p className="text-gray-500">Temp</p>
              <p className="font-semibold">{result.weather_data.temperature}°C</p>
            </div>
            <div className="p-2 bg-white rounded border">
              <p className="text-gray-500">Humidity</p>
              <p className="font-semibold">{result.weather_data.humidity}%</p>
            </div>
            <div className="p-2 bg-white rounded border">
              <p className="text-gray-500">Rainfall</p>
              <p className="font-semibold">{result.weather_data.rainfall} mm</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}