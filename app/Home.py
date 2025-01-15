import streamlit as st
import pandas as pd

def app():
    st.title("Traffic Accident Analysis")
    st.write("Welcome to the Traffic Accident Analysis App.")
    
    on = st.toggle("Show Dataset!")

    if on:    
        df = st.session_state.data
        df.dropna(inplace=True)
        df["Start_Time"] = pd.to_datetime(df['Start_Time'], errors='coerce')
        df.dropna(subset=["Start_Time"], inplace=True)
        df['Year'] = df['Start_Time'].dt.year
        
        # Title and Description
        
        # Display Dataset Overview
        st.header("Raw Data")
        st.write(df.head(3))
        
    st.write("Use the sidebar to navigate through different sections of the app.")