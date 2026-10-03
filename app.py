import streamlit as st
import requests
import joblib
from streamlit_geolocation import streamlit_geolocation


# -----------------------------------
# LOAD ML MODEL
# -----------------------------------

model = joblib.load("model.pkl")


# -----------------------------------
# PAGE
# -----------------------------------

st.set_page_config(
    page_title="Smart Crop Recommendation",
    page_icon="🌾"
)

st.title("🌾 Smart Crop Recommendation System")

st.write(
    "Get weather automatically from your location "
    "and predict the most suitable crop."
)


# -----------------------------------
# LOCATION
# -----------------------------------

st.subheader("📍 Farm Location")

location = streamlit_geolocation()


if location:

    latitude = location["latitude"]
    longitude = location["longitude"]

    st.success("✓ Location detected")


    # -----------------------------------
    # WEATHER API
    # -----------------------------------

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,rain",
        "timezone": "auto"
    }

    response = requests.get(url, params=params)


    if response.status_code == 200:

        data = response.json()

        current = data["current"]


        # -----------------------------------
        # WEATHER VALUES
        # -----------------------------------

        temperature = current["temperature_2m"]

        humidity = current["relative_humidity_2m"]

        rainfall = current["rain"]


        # -----------------------------------
        # DISPLAY WEATHER
        # -----------------------------------

        st.subheader("🌦 Automatically Retrieved Weather")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Temperature",
            f"{temperature} °C"
        )

        col2.metric(
            "Humidity",
            f"{humidity} %"
        )

        col3.metric(
            "Rainfall",
            f"{rainfall} mm"
        )


        # -----------------------------------
        # SOIL INPUT
        # -----------------------------------

        st.subheader("🌱 Soil Information")

        N = st.number_input(
            "Nitrogen (N)",
            min_value=0.0
        )

        P = st.number_input(
            "Phosphorus (P)",
            min_value=0.0
        )

        K = st.number_input(
            "Potassium (K)",
            min_value=0.0
        )

        ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5
        )


        # -----------------------------------
        # PREDICTION
        # -----------------------------------

        if st.button("🌾 Predict Crop"):

            input_data = [[
                N,
                P,
                K,
                temperature,
                humidity,
                ph,
                rainfall
            ]]

            prediction = model.predict(input_data)

            st.success(
                f"🌾 Recommended Crop: {prediction[0]}"
            )


    else:

        st.error(
            "Weather service could not be reached."
        )