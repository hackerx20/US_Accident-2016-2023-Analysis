import streamlit as st
import pandas as pd

def app():
    st.title("Exploratory Data Analysis")
    st.title("US Accident Data Analysis (2016-2023)")
    st.markdown("""This is a countrywide car accident dataset that covers 49 states of the USA. The accident data were collected from February 2016 to March 2023, using multiple APIs that provide streaming traffic incident (or event) data. These APIs broadcast traffic data captured by various entities, including the US and state departments of transportation, law enforcement agencies, traffic cameras, and traffic sensors within the road networks.""")
    
    df = st.session_state.data
    df.dropna(inplace=True)
    df["Start_Time"] = pd.to_datetime(df['Start_Time'], errors='coerce')
    df.dropna(subset=["Start_Time"], inplace=True)
    df['Year'] = df['Start_Time'].dt.year
    
    
    # Total Number of Accidents!
    st.write(f"Total No. of Accident from 2016 to 2023 : {df.shape[0]}")
    df_eda = df[["Severity", "State", "Start_Lat", "Start_Lng", "Year", "Amenity", "Bump", "Crossing", "Give_Way", "Junction", "No_Exit",  "Railway", "Roundabout", "Station", "Stop", "Traffic_Calming", "Traffic_Signal", "Turning_Loop"]]
    
    # Severity Distribution
    st.header("Dataset used for Below Analysis:")
    st.write(df_eda.head(3))
    st.write("\n")
    # st.subheader("Severity Distributions")
    
    left, middle, right = st.columns(3)
    if left.button("Accidents based on Severity", use_container_width=True):
        st.header("Accidents from 2016 -2023:")
        year_count = df_eda['Year'].value_counts()
        # st.write(year_count)
        st.bar_chart(year_count)
        st.write("Most no. of Accidents took place in the year 2021 and 2022. And Least no. of Accident took place in the year 2016 and 2023.")

        st.header("Total No. of Accident from 2016 - 2023 according to Severity:")
        severity_count = df_eda['Severity'].value_counts()
        st.bar_chart(severity_count)
        st.write("Most Accidents that occured in US between 2016-2023 are of severity 2.")
        # Default severity 
        # Assuming df_eda is already loaded
        
        # <<<<-------------------Severity vs Year ---------------------------->>>>
        st.write("\n")
        st.write("\n")
        
        st.header("Total No. of Accidents from 2016 to 2023 of a particular Severity:")
        
        severity = st.selectbox("Select Severity", options=df_eda['Severity'].unique(), index=1)
        df_severity = df_eda[df_eda['Severity'] == severity]
        Severity_accidents = df_severity.groupby('Year').size().reset_index(name='Accident_Count')
        Severity_accidents.set_index('Year', inplace=True)
        # st.write(Severity_accidents.head(3))
        st.bar_chart(Severity_accidents['Accident_Count'])

        # <<<<-----------------Severity vs State--------------------------->>>>
        st.header("Total no. of Accidents in each State with a Particular Severity:")
        severity1 = st.selectbox("Select Severity", options=df_eda['Severity'].unique(), index=2)
        df_severity1 = df_eda[df_eda['Severity'] == severity1]

        # Aggregate accident counts by state
        Severity_accidents1 = df_severity1.groupby('State').size().reset_index(name='Accident_Count')

        # Set the 'State' column as the index for plotting
        Severity_accidents1.set_index('State', inplace=True)

        # st.write(Severity_accidents1.head(3))
        # Display the bar chart using Streamlit's built-in method
        st.bar_chart(Severity_accidents1['Accident_Count'])

    if middle.button("Accidents in Different States", use_container_width=True):

        # <<<<---------------------------- State vs NO. of Accidents ---------------------------->>>>

        st.header("Accidents in Different States from 2016 to 2023 :")
        state_count = df_eda['State'].value_counts()
        st.bar_chart(state_count)

        # <<<<---------------------------- State vs NO. of Accidents ---------------------------->>>>

        st.header(f"Total no. of Accidents in each State in a Particular year:")
        year = st.selectbox("Select Year", options=df_eda['Year'].unique(), index=5)
        df_year = df_eda[df_eda['Year'] == year]

        # Aggregate accident counts by state
        state_accidents = df_year.groupby('State').size().reset_index(name='Accident_Count')

        # Set the 'State' column as the index for plotting
        state_accidents.set_index('State', inplace=True)
        # st.write(state_accidents.head(3))
        # Display the bar chart using Streamlit's built-in method
        st.bar_chart(state_accidents['Accident_Count'])

    if right.button("Accidents at Different Location", use_container_width=True):
        bool_columns = [
            "Amenity",
            "Bump",
            "Crossing",
            "Give_Way",
            "Junction",
            "No_Exit",
            "Railway",
            "Roundabout",
            "Station",
            "Stop",
            "Traffic_Calming",
            "Traffic_Signal",
            "Turning_Loop",
        ]
        
        # Select the state and year
        state = st.selectbox("Select State", options=df_eda['State'].unique())
        year = st.selectbox("Select Year", options=df_eda['Year'].unique())

        # Filter data for the selected state and year
        df_selected_state_year = df_eda[(df_eda["State"] == state) & (df_eda["Year"] == year)]

        # Calculate the mean of boolean columns grouped by severity
        severity_bool_analysis1 = df_selected_state_year.groupby("Severity")[bool_columns].mean()
        # st.write(severity_bool_analysis1.head(3))
        # Display the bar chart for the selected state and year
        st.bar_chart(severity_bool_analysis1.T)
        st.subheader(f"Accidents prone Locations:")
        severity3 = st.selectbox("Select Severity", options=df_eda['Severity'].unique(), index=3)
        # Group by severity and calculate mean for boolean columns
        severity_bool_analysis = df_eda.groupby("Severity")[bool_columns].mean()

        # Filter the data based on the selected severity
        severity_data = severity_bool_analysis.loc[severity3]
        
        # st.write(severity_data.head(3))
        # Display the bar chart using Streamlit's built-in method
        st.bar_chart(severity_data)






        # Correlation Heatmap
        # st.subheader("Correlation Heatmap")
        # fig, ax = plt.subplots(figsize=(10, 8))
        # sns.heatmap(data= data.corr(), annot=True, cmap='coolwarm', ax=ax)
        # st.pyplot(fig)


        # Assuming df_eda contains the columns 'Start_Lat', 'Start_Lng', and 'Severity'
        # Example for illustration, replace it with your actual dataframe
        # df_eda = pd.read_csv("your_data.csv")  # Example: loading data from a CSV

        # Select the severity


        #<<<<---------------Pydeck Chart Starts ------------------>>>>
        # Prepare chart data for pydeck
        # df_location = df_eda[['Start_Lng', 'Start_Lat','Severity']]
        # df_location.drop_duplicates()
        # # Adjust hexagon height and colors based on severity
        # elevation_scale = {1: 1, 2: 2, 3: 3, 4: 4}  # Example scale
        # elevation_range = {1: [0, 500], 2: [0, 1000], 3: [0, 1500], 4: [0, 2000]}
        # color_map = {
        #     1: [200, 30, 0, 160],   # Red
        #     2: [0, 200, 0, 160],    # Green
        #     3: [0, 0, 200, 160],    # Blue
        #     4: [200, 200, 0, 160],  # Yellow
        # }

        # # Create the pydeck chart
        # deck = pdk.Deck(
        #     map_style="light",
        #     initial_view_state=pdk.ViewState(
        #         latitude=df_location['Start_Lat'].mean(),
        #         longitude=df_location['Start_Lng'].mean(),
        #         zoom=11,
        #         pitch=50,
        #     ),
        #     layers=[
        #         pdk.Layer(
        #             "HexagonLayer",
        #             data=df_location,
        #             get_position="[Start_Lng, Start_Lat]",
        #             radius=200,
        #             elevation_scale=elevation_scale[severity],
        #             elevation_range=elevation_range[severity],
        #             pickable=True,
        #             extruded=True,
        #             get_fill_color=color_map[severity],  # Adjust hexagon color based on severity
        #         ),
        #         pdk.Layer(
        #             "ScatterplotLayer",
        #             data=df_location,
        #             get_position="[Start_Lng, Start_Lat]",
        #             get_color=color_map[severity],
        #             get_radius=200,
        #         ),
        #     ],
        # )

        # # Display the chart
        # st.pydeck_chart(deck)


        # Example DataFrame `df_eda`, replace with your actual data
        # df_eda = pd.read_csv("your_data.csv")  # Load your data

        # Define a color map with valid hex codes for each severity
        # color_map = {
        #     1: [255, 0, 0],  # Red
        #     2: [0, 255, 0],  # Green
        #     3: [0, 0, 255],  # Blue
        #     4: [255, 255, 0],  # Yellow
        # }

        # # Add a color column based on severity
        # df_eda['color'] = df_eda['Severity'].map(color_map)

        # # Optional: Add size column for scaling
        # df_eda['size'] = df_eda['Severity'] * 100  # Adjust the size scaling factor as needed

        # # Define the Pydeck visualization
        # layer = pdk.Layer(
        #     "ScatterplotLayer",
        #     data=df_eda,
        #     get_position=["Start_Lng", "Start_Lat"],  # Longitude first, Latitude second
        #     get_color="color",  # Use the color column
        #     get_radius="size",  # Use the size column
        #     pickable=True,
        # )

        # view_state = pdk.ViewState(
        #     latitude=df_eda["Start_Lat"].mean(),
        #     longitude=df_eda["Start_Lng"].mean(),
        #     zoom=5,
        #     pitch=0,
        # )

        # # Render the map
        # st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))


        #<<<<---------------Pydeck Chart ends ------------------>>>>

        #<<<<---------------map Chart Starts ------------------>>>>

        # Create a selectbox for choosing the severity
        st.subheader("Accidents prone Locations:")
        severity = st.selectbox("Select Severity", options=df_eda["Severity"].unique())
        # Filter the DataFrame based on the selected severity
        filtered_data = df_eda[df_eda["Severity"] == severity]

        # Display the map with the filtered data
        st.map(filtered_data, latitude="Start_Lat", longitude="Start_Lng")
    