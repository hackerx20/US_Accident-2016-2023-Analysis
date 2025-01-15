import streamlit as st
import pandas as pd
# import streamlit as st
# import pandas as pd

# Load dataset once and store it in session_state
if "data" not in st.session_state:
    st.session_state.data = pd.read_csv("./data/US_Accidents_March23.csv")
st.set_page_config(page_title="Traffic Accident Analysis", layout="wide")

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "EDA", "Modeling"])

if page == "Home":
    from app.Home import app
    app()
elif page == "EDA":
    from app.EDA import app
    app()
elif page == "Modeling":
    from app.Modeling import app
    app()

