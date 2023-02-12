import numpy as np
import plotly.express as px
import pandas as pd
import os
import json
import json
import mysql.connector
import streamlit as st
import plotly.express as px
import csv
import pandas
import geojson
import plotly.graph_objects as go
import plotly.graph_objs as go


root_folder = r"C:\Users\Vishaal Grizzly\PycharmProjects\PhonePeproject\cloned_repository\data"

# list to store the extracted data from the json files
data = []

data = []
data = []
for subdir, dirs, files in os.walk(root_folder):
    for file in files:
        if file.endswith(".json"):
            file_path = os.path.join(subdir, file)
            parent_dir = os.path.basename(os.path.dirname(file_path))
            state = os.path.basename(os.path.dirname(os.path.dirname(file_path)))  # Extract the state information from the parent folder of the file
            with open(file_path) as f:
                # load the json file into a dictionary
                json_data = json.load(f)
                districts = json_data.get("data", {}).get("districts", [])
                quarter = int(file.split(".")[0])  # Extract the quarter information from the file name
                for district in districts:
                    district_name = district.get("name", None)
                    registered_users = district.get("registeredUsers", None)
                    data.append([district_name, state, parent_dir, quarter, registered_users])  # Update the columns list

# create a pandas dataframe from the extracted data
df = pd.DataFrame(data, columns=["District Name", "State", "Year", "Quarter", "Registered Users"])

df["Registered Users"].fillna(0, inplace=True)

#Checking the shape of the dataframe
print (df.head())
print (df.shape)

#Checking for zero values in the district and registered users column to drop
df.dropna(subset=["District Name"], inplace=True)
df = df.loc[df["Registered Users"] != 0.0]

print ("Here is the dataframe after cleaning null values")
print (df.head())
#Checking the shape of the dataframe after dropping irrelevant rows
print (df.shape)

# Converting the dataframe into a CSV file
df.to_csv("data.csv", index=False)

file = pandas.read_csv('data.csv')
print (type(file))
print (file)


#Moving on to connecting with the local mysql database

# Connect to the MySQL server
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="PhonePe_project"
)

cursor = cnx.cursor()

#In this part we will be creating a table to write the data we extracted

# Read the data from the data.csv file
df = pd.read_csv("data.csv")

# Get the column names and data types from the data.csv file
columns = []
for col in df.columns:
    if df[col].dtype == int:
        columns.append(f"`{col}` INT")
    elif df[col].dtype == float:
        columns.append(f"`{col}` FLOAT")
    else:
        columns.append(f"`{col}` VARCHAR(255)")

# Create the table with the column names and data types from the data.csv file
table_create_query = "CREATE TABLE IF NOT EXISTS table_name ({})".format(", ".join(columns))
cursor.execute(table_create_query)

# Prepare the query to insert the data into the table
insert_query = "INSERT INTO table_name ({}) VALUES ({})".format(
    ", ".join(["`{}`".format(col) for col in df.columns]),
    ", ".join(["%s"] * len(df.columns))
)

# Insert the data into the table
for i, row in df.iterrows():
    cursor.execute(insert_query, tuple(row.values))

#Connect to the MySQL server
cnx = mysql.connector.connect(
host="localhost",
user="root",
password="12345",
database = "PhonePe_project"
)

cursor = cnx.cursor()

#Select all the data from the table
select_query = "SELECT * FROM table_name"
cursor.execute(select_query)

#Fetch all the data from the result set
result = cursor.fetchall()

#Print the result
for row in result:
    print(row)

#Commit the changes
cnx.commit()


# Load the data from the database
query = "SELECT * FROM table_name"
df = pd.read_sql(query, cnx)

# Create a dropdown menu to select the year
selected_year = st.selectbox("Select Year", df["Year"].unique())

# Create a dropdown menu to select the state
selected_state = st.selectbox("Select State", df["State"].unique())

# Filter the data based on the selected year and state
filtered_data = df[(df["Year"] == selected_year) & (df["State"] == selected_state)]

# Create a dropdown menu to select the quarter
selected_quarter = st.selectbox("Select Quarter", filtered_data["Quarter"].unique())

# Filter the data based on the selected quarter
filtered_data = filtered_data[filtered_data["Quarter"] == selected_quarter]

# Create a dropdown menu to select the district name
selected_district = st.selectbox("Select District", filtered_data["District Name"].unique())

# Filter the data based on the selected district name
filtered_data = filtered_data[filtered_data["District Name"] == selected_district]

# Load the India map data
india_map_data = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'

# Create a choropleth map
fig = go.Figure(go.Choroplethmapbox(
    geojson=india_map_data,
    locations=filtered_data["District Name"],
    z=filtered_data["Registered Users"],
    colorscale="Viridis",
    colorbar_title="Number of Registered Users",
    marker_line_width=0.5,
    marker_line_color='white',
    zmin=0,
    zmax=filtered_data["Registered Users"].max(),
))

fig.update_layout(
    title=f"Registered Users in {selected_district}, {selected_state} ({selected_year}), Quarter: {selected_quarter}",
    mapbox_style="carto-positron",
    mapbox_zoom=4,
    mapbox_center={"lat": 20.5937, "lon": 78.9629},
)

st.title("PhonePe Pulse Visualization based on 4 years transactions data")
st.plotly_chart(fig)

# Close the cursor and connection
cursor.close()
cnx.close()






