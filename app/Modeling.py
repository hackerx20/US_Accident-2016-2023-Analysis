import streamlit as st
# import numpy as np
# import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
# import plotly.express as px
# import folium
# from folium.plugins import HeatMap
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
# from mlxtend.plotting import plot_decision_regions
import warnings
warnings.simplefilter('ignore')
elec_type_colors = ['green', 'gold']
cmap = 'RdYlBu_r'

def app():
    st.title("Data Preprocessing :")
    
    # Initial Data Preprocessing!
    df = st.session_state.data
    df.dropna(inplace=True)
    df["Start_Time"] = pd.to_datetime(df['Start_Time'], errors='coerce')
    df.dropna(subset=["Start_Time"], inplace=True)
    df['Year'] = df['Start_Time'].dt.year
    
    df_data_handling = df[["Distance(mi)","Temperature(F)","Humidity(%)", "Pressure(in)", "Visibility(mi)","Wind_Direction", "Wind_Speed(mph)","Weather_Condition","Precipitation(in)", "Severity"]]
    df_data_handling.duplicated()
    df_data_handling = df_data_handling.drop_duplicates()
    
    st.subheader("Dataset used for modeling:")
    st.write(df_data_handling.head(3))
    
    # Encoding Wind_Directions and Whether_Conditions Column
    la = LabelEncoder()
    la.fit(df_data_handling["Wind_Direction"])
    df_data_handling["Wind_Direction"] = la.transform(df_data_handling["Wind_Direction"])
    la.fit(df_data_handling["Weather_Condition"])
    df_data_handling["Weather_Condition"] = la.transform(df_data_handling["Weather_Condition"])
    st.subheader("Dataset After Encoding:")
    st.write(df_data_handling.head(3))
    
    st.subheader("Basic Statistics of Dataset:")
    st.write(df_data_handling.describe())
    
    st.subheader("Correlation of Dataset:")
    st.write(df_data_handling.corr())
    q1 = df_data_handling["Temperature(F)"].quantile(0.25)
    q3 = df_data_handling["Temperature(F)"].quantile(0.75)
    iqr = q3 - q1
    min_value = q1 - 1.5 * iqr
    max_value = q3 + 1.5 * iqr
    new_df = df_data_handling[df_data_handling["Temperature(F)"]<=max_value]
    df_data_handling = new_df[new_df["Temperature(F)"]>=min_value]
    sns.boxplot(x="Temperature(F)", data = df_data_handling)
    plt.show()
    
    q1 = df_data_handling["Pressure(in)"].quantile(0.25)
    q3 = df_data_handling["Pressure(in)"].quantile(0.75)
    iqr = q3 - q1
    min_value = q1 - 1.5 * iqr
    max_value = q3 + 1.5 * iqr
    new_df = df_data_handling[df_data_handling["Pressure(in)"]<=max_value]
    df_data_handling = new_df[new_df["Pressure(in)"]>=min_value]
    sns.boxplot(x="Pressure(in)", data = df_data_handling)
    plt.show()
    
    q1 = df_data_handling["Visibility(mi)"].quantile(0.25)
    q3 = df_data_handling["Visibility(mi)"].quantile(0.75)
    iqr = q3 - q1
    min_value = q1 - 1.5 * iqr
    max_value = q3 + 1.5 * iqr
    new_df = df_data_handling[df_data_handling["Visibility(mi)"]<=max_value]
    df_data_handling = new_df[new_df["Visibility(mi)"]>=min_value]
    sns.boxplot(x="Visibility(mi)", data = df_data_handling)
    plt.show()
    q1 = df_data_handling["Wind_Speed(mph)"].quantile(0.25)
    q3 = df_data_handling["Wind_Speed(mph)"].quantile(0.75)
    iqr = q3 - q1
    min_value = q1 - 1.5 * iqr
    max_value = q3 + 1.5 * iqr
    new_df = df_data_handling[df_data_handling["Wind_Speed(mph)"]<=max_value]
    df_data_handling = new_df[new_df["Wind_Speed(mph)"]>=min_value]
    sns.boxplot(x="Wind_Speed(mph)", data = df_data_handling)
    plt.show()
    q1 = df_data_handling["Precipitation(in)"].quantile(0.25)
    q3 = df_data_handling["Precipitation(in)"].quantile(0.75)
    iqr = q3 - q1
    min_value = q1 - 1.5 * iqr
    max_value = q3 + 1.5 * iqr
    new_df = df_data_handling[df_data_handling["Precipitation(in)"]<=max_value]
    df_data_handling = new_df[new_df["Precipitation(in)"]>=min_value]
    sns.boxplot(x="Precipitation(in)", data = df_data_handling)
    plt.show()
    # outliers removal done!
    # Sample Dataset Selection!
    sampled_df = df_data_handling.sample(n=100000, random_state=42)
    x = sampled_df.drop(columns="Severity")
    y = sampled_df["Severity"]
    st.subheader("Dataset After Removing Outliers:")
    st.write(df_data_handling.head(3))
    
    ss = StandardScaler()
    ss.fit(x)
    x = pd.DataFrame(ss.transform(x), columns=x.columns)
    x.head(3)
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2, random_state=42)
    lr = LogisticRegression(multi_class="multinomial")
    lr.fit(x_train,y_train)
    lr.score(x_test,y_test)*100