import streamlit as st
import pandas as pd
import numpy as np
import pickle

def app():
    
    # Load the trained model
    @st.cache_resource
    def load_model():
        # Replace 'model.pkl' with your actual model file
        with open('model.pkl', 'rb') as file:
            model = pickle.load(file)
        return model

    model = load_model()

    # Input Form
    st.title("Accident Severity Prediction")
    st.markdown("""
    Input the following details about the accident and weather conditions, and the application will predict the severity of the accident.
    """)

    with st.form("severity_form"):
        distance = st.number_input("Distance(mi)", min_value=-50.0, max_value=150.0, value=70.0, step=0.1)
        temperature = st.number_input("Temperature(F)", min_value=-50.0, max_value=150.0, value=70.0, step=0.1)
        humidity = st.number_input("Humidity(%)", min_value=0.0, max_value=100.0, value=50.0, step=0.1)
        wind_direction = st.selectbox("Wind_Direction", options=['NNW', 'S', 'CALM', 'SSW', 'E', 'SW', 'ENE', 'ESE', 'WSW', 'NW','SSE', 'WNW', 'NE', 'W', 'N', 'SE', 'VAR', 'NNE', 'Variable', 'North', 'West', 'East', 'South'])
        pressure = st.number_input("Pressure(in)", min_value=20.0, max_value=35.0, value=29.92, step=0.01)
        visibility = st.number_input("Visibility(mi)", min_value=0.0, max_value=100.0, value=10.0, step=0.1)
        wind_speed = st.number_input("Wind_Speed(mph)", min_value=0.0, max_value=200.0, value=10.0, step=0.1)
        precipitation = st.number_input("Precipitation(in)", min_value=0.0, max_value=10.0, value=0.0, step=0.01)
        weather_condition = st.selectbox("Weather_Condition", options=['Cloudy', 'Fair', 'Partly Cloudy', 'Light Rain', 'Mostly Cloudy',
            'Fair / Windy', 'Fog', 'Haze', 'Rain', 'Light Rain with Thunder',
            'Heavy Rain', 'Light Snow', 'Cloudy / Windy', 'Smoke', 'Snow',
            'Thunder in the Vicinity', 'Overcast', 'Light Rain / Windy',
            'T-Storm', 'Mostly Cloudy / Windy', 'Light Freezing Drizzle',
            'Partly Cloudy / Windy', 'Light Drizzle', 'Light Snow / Windy',
            'Thunder', 'Heavy Rain / Windy', 'Scattered Clouds',
            'Thunder / Windy', 'Wintry Mix', 'Heavy Snow', 'Drizzle', 'Mist',
            'Small Hail', 'Patches of Fog', 'Heavy T-Storm',
            'Light Snow and Sleet / Windy', 'Freezing Rain',
            'Light Snow and Sleet', 'Showers in the Vicinity', 'Shallow Fog',
            'Light Freezing Rain', 'Snow / Windy',
            'Light Thunderstorms and Rain', 'Haze / Windy', 'Blowing Snow',
            'Heavy Snow / Windy', 'Sand / Dust Whirlwinds', 'T-Storm / Windy',
            'Heavy T-Storm / Windy', 'Light Drizzle / Windy',
            'N/A Precipitation', 'Rain / Windy', 'Drizzle and Fog',
            'Light Snow Shower', 'Clear', 'Snow and Sleet', 'Fog / Windy',
            'Blowing Dust', 'Blowing Snow / Windy', 'Sleet',
            'Wintry Mix / Windy', 'Heavy Drizzle', 'Thunder and Hail / Windy',
            'Light Freezing Rain / Windy', 'Light Rain Shower',
            'Thunderstorms and Rain', 'Heavy Thunderstorms and Rain', 'Hail'])

        submitted = st.form_submit_button("Predict")

    if submitted:
        # Map wind direction to numeric values (if necessary for your model)
        wind_dir_map = {'NNW':8, 'S':11, 'CALM':0, 'SSW':14, 'E':1, 'SW':15, 'ENE':2, 'ESE':3, 'WSW':21, 'NW':9,'SSE':13, 'WNW':20, 'NE':6, 'W':19, 'N':5, 'SE':12, 'VAR':17, 'NNE':7, 'Variable':18, 'North':10, 'West':22, 'East':4, 'South':16}
        wind_direction_numeric = wind_dir_map[wind_direction]

        weather_condition_map = {
            'Cloudy': 4,
            'Fair': 8,
            'Partly Cloudy': 44,
            'Light Rain': 29,
            'Mostly Cloudy': 40,
            'Fair / Windy': 9,
            'Fog': 10,
            'Haze': 14,
            'Rain': 47,
            'Light Rain with Thunder': 32,
            'Heavy Rain': 17,
            'Light Snow': 33,
            'Cloudy / Windy': 5,
            'Smoke': 55,
            'Snow': 56,
            'Thunder in the Vicinity': 64,
            'Overcast': 43,
            'Light Rain / Windy': 30,
            'T-Storm': 59,
            'Mostly Cloudy / Windy': 41,
            'Light Freezing Drizzle': 26,
            'Partly Cloudy / Windy': 45,
            'Light Drizzle': 24,
            'Light Snow / Windy': 34,
            'Thunder': 61,
            'Heavy Rain / Windy': 18,
            'Scattered Clouds': 50,
            'Thunder / Windy': 62,
            'Wintry Mix': 66,
            'Heavy Snow': 19,
            'Drizzle': 6,
            'Mist': 39,
            'Small Hail': 54,
            'Patches of Fog': 46,
            'Heavy T-Storm': 21,
            'Light Snow and Sleet / Windy': 37,
            'Freezing Rain': 12,
            'Light Snow and Sleet': 36,
            'Showers in the Vicinity': 52,
            'Shallow Fog': 51,
            'Light Freezing Rain': 27,
            'Snow / Windy': 57,
            'Light Thunderstorms and Rain': 38,
            'Haze / Windy': 15,
            'Blowing Snow': 1,
            'Heavy Snow / Windy': 20,
            'Sand / Dust Whirlwinds': 49,
            'T-Storm / Windy': 60,
            'Heavy T-Storm / Windy': 22,
            'Light Drizzle / Windy': 25,
            'N/A Precipitation': 42,
            'Rain / Windy': 48,
            'Drizzle and Fog': 7,
            'Light Snow Shower': 35,
            'Clear': 3,
            'Snow and Sleet': 58,
            'Fog / Windy': 11,
            'Blowing Dust': 0,
            'Blowing Snow / Windy': 2,
            'Sleet': 53,
            'Wintry Mix / Windy': 67,
            'Heavy Drizzle': 16,
            'Thunder and Hail / Windy': 63,
            'Light Freezing Rain / Windy': 28,
            'Light Rain Shower': 31,
            'Thunderstorms and Rain': 65,
            'Heavy Thunderstorms and Rain': 23,
            'Hail': 13
        }
        weather_condition_numeric = weather_condition_map[weather_condition]
        
        # Prepare input data for the model
        input_data = np.array([[
            distance,temperature, humidity, pressure, visibility,
            wind_direction_numeric, wind_speed, precipitation, weather_condition_numeric
        ]])

        # Simulate prediction if model requires encoding for weather condition
        # Replace this with actual preprocessing steps if needed
        severity_prediction = model.predict(input_data)[0]

        # Display the result
        st.subheader("Predicted Severity")
        st.write(f"The predicted accident severity is: {severity_prediction}")



