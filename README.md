#Geo Visualization and Exploration with PhonePe Pulse

To begin with, I extracted the data from the Phonepe Pulse Github repository through scripting and cloned it. The data was stored in a suitable format such as CSV or JSON. I used Python and Pandas library to manipulate and pre-process the data, which included cleaning the data, handling missing values, and transforming the data into a format suitable for analysis and visualization.

Next, I inserted the transformed data into a MySQL database for efficient storage and retrieval using the "mysql-connector-python" library in Python.

I created a live geo-visualization dashboard using Streamlit and Plotly in Python to display the data in an interactive and visually appealing manner. I used Plotly's built-in geo map functions to display the data on a map and Streamlit to create a user-friendly interface with multiple dropdown options for users to select different facts and figures to display.

To fetch the data from the MySQL database to display in the dashboard, I used the "mysql-connector-python" library to connect to the MySQL database and fetch the data into a Pandas dataframe. I used the data in the dataframe to update the dashboard dynamically.

I thoroughly tested the solution and deployed the dashboard publicly (I am still working on the map option), making it accessible to users. I added multiple dropdown options for users to select different facts and figures to display on the dashboard. 
