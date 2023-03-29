import streamlit as st
import pandas as pd
import mysql.connector as msql
from mysql.connector import Error
import plotly.express as px
import geopandas as gpd
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests


# ----------------------------------MySQl server connection--------------------------------------------

try:
    conn = msql.connect(host='localhost',
                        database='phonepe_pulse',
                        user='root',
                        password='root')
    if conn.is_connected():
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM AggregatedData")
        records1 = cursor.fetchall()
        AggregatedData = pd.DataFrame(records1,
                           columns=[i[0] for i  in cursor.description])

        cursor.execute("SELECT * FROM brandsused")
        records2 = cursor.fetchall()
        brandsused = pd.DataFrame(records2,
                         columns=[i[0] for i in cursor.description])

        cursor.execute("SELECT * FROM transbydistrictmap")
        records3 = cursor.fetchall()
        transbydistrictmap = pd.DataFrame(records3,
                             columns=[i[0] for i in cursor.description])

        cursor.execute("SELECT * FROM usersbydistmap")
        records4 = cursor.fetchall()
        usersbydistmap = pd.DataFrame(records4, columns=[i[0] for i in cursor.description])
        conn.commit()
        cursor.close()
        conn.close()
except Error as e:
    pass
# ------------------------------------ MySQl server connection End------------------------------------------------------


# ------------------------------------Side Bar--------------------------------------------------------------------------
with st.sidebar:
    menu = option_menu(
                       menu_title='Pick the action to perform',
                       options=['About the project',
                                'APP Registered',
                                'Geo Map',
                                'User Mobile Brand',
                                'Brand percentage'],
                       icons=['house', 'app', 'geo-alt', 'phone', 'pie-chart'], default_index=0)

if menu == 'About the project':
    # Header or Title of the page
    st.markdown("<h1 style='text-align:center; color:red;'"
                ">Phonepe Pulse Data Visualization and Exploration</h1>",
                unsafe_allow_html=True)

    # ----------------------------------------Lottie Animation----------------------------------------------------------
    def load_lottieURl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_dashboard = load_lottieURl("https://assets3.lottiefiles.com/packages/lf20_odoe8cta.json")
    st_lottie(lottie_dashboard, height=300, width=700, key='Transaction')

    # ------------------------------------Lottie Animation----------------------------------------------------------
    st.write(" This project aims to extract and process data from Phonepe pulse Github repository to create,"
             " an interactive and visually appealing geo visualization dashboard using Streamlit and Plotly in Python,"
             " The solution will include steps like data extraction, transformation, and storage in a MySQL database."
             " The dashboard will fetch data from the database and provide at least 10 dropdown options for users,"
             " to select different facts and figures. The solution must be secure, efficient, and user-friendly,"
             " providing valuable insights, and information about the data in the Phonepe pulse Github repository.")
# ---------------------------------------Inputs-------------------------------------------------------------------------
yearTuple = ('2018', '2019', '2020', '2021', '2022')
quarterTuple = ('Q1', 'Q2', 'Q3', 'Q4')
stateTuple= ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh',
                 'assam', 'bihar', 'chandigarh', 'chhattisgarh',
                 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa', 'gujarat',
                 'haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand',
                 'karnataka', 'kerala', 'ladakh', 'lakshadweep', 'madhya-pradesh',
                 'maharashtra', 'manipur', 'meghalaya', 'mizoram', 'nagaland',
                 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                 'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh',
                 'uttarakhand', 'west-bengal')

# ---------------------------------------Inputs--------------------------------------------------------------------------

# -----------------------------------App Registered User by District----------------------------------------------------
if menu == 'APP Registered':
    st.markdown("<h1 style='text-align:center; color:red;'"
                ">App Registered User By District</h1>",
                unsafe_allow_html=True)

    barYear = st.selectbox('Select the Year:', yearTuple)
    st.write(' ')

    state = st.selectbox('Select the State:', stateTuple, index=30)

    usersbydistmap_filter = usersbydistmap[(usersbydistmap['State'] == state)
                                     & (usersbydistmap['Year'] == int(barYear))]

    dist_reg = usersbydistmap_filter.groupby(['District']).sum(numeric_only=True)[['Registered_user','App_opening']]
    dist_reg = dist_reg.reset_index()

    fig1 = px.bar(dist_reg,
                  x="District",
                  y=["Registered_user"],
                  color='District',
                  title=f"District wise registered user in {state}:")
    fig1.update_traces(width=1)
    st.plotly_chart(fig1)

# -----------------------------------App Registered User by District----------------------------------------------------


# ----------------------------------Geo map visualization---------------------------------------------------------------

import requests

state_lat_lon = pd.read_csv('state_lat_lon.csv')

if menu == 'Geo Map':
    st.markdown("<h1 style='text-align:center; color:red;'"
                ">Transaction by State</h1>",
                unsafe_allow_html=True)

    Year = st.radio('Please select the Year', yearTuple, horizontal=True)
    st.write(' ')
    Quarter = st.radio('Please select the Quarter', quarterTuple, horizontal=True)
    st.write(' ')
    
    print("Selected Year:", Year)
    print("Selected Quarter:", Quarter)
    print("Unique Years in AggregatedData:", AggregatedData['Year'].unique())
    print("Unique Quarters in AggregatedData:", AggregatedData['Quarter'].unique())

    # filter AggregatedData for selected year and quarter
    AggregatedData_filter = AggregatedData[
        (AggregatedData['Year'] == Year) & (AggregatedData['Quarter'] == Quarter)]
    #AggregatedData['State'] = AggregatedData['State'].str.replace('-', ' ')
    print("Selected Year:", Year)
    print("Selected Quarter:", Quarter)
    print("Unique Years in AggregatedData:", AggregatedData['Year'].unique())
    print("Unique Quarters in AggregatedData:", AggregatedData['Quarter'].unique())

    # check if any data exists for selected year and quarter
    if AggregatedData_filter.empty:
        st.warning("No data available for the selected year and quarter.")
    else:
        # group by state and calculate sum of Transaction_no and Transaction_tot
        AggregatedData_filter = AggregatedData_filter.groupby(['State']).sum(numeric_only=True)[
            ['Transaction_no', 'Transaction_tot']]
        AggregatedData_filter = AggregatedData_filter.reset_index()

        lat_lon_df = pd.merge(state_lat_lon, AggregatedData_filter, left_on='State.Name', right_on='State')
        lat_lon_df = lat_lon_df.rename(columns={'State.Name': 'State'})

        # getting some geojson for India.  Reduce complexity of geometry to make it more efficient
        url = "https://raw.githubusercontent.com/Subhash9325/GeoJson-Data-of-Indian-States/master/Indian_States"
        gdf = gpd.read_file(url)
        gdf["geometry"] = gdf.to_crs(gdf.estimate_utm_crs()).simplify(1000).to_crs(gdf.crs)
        india_states = gdf.rename(columns={"NAME_1": "ST_NM"}).__geo_interface__

        # create the scatter geo plot
        fig1 = None
        if not lat_lon_df.empty:
            fig1 = px.scatter_geo(lat_lon_df,
                                  lat="lat",
                                  lon="lon",
                                  color="Transaction_tot",
                                  size=lat_lon_df["Transaction_no"],
                                  hover_name="State",
                                  hover_data=["State",
                                              'Transaction_tot',
                                              'Transaction_no'],
                                  title='State',
                                  size_max=10, )

            fig1.update_traces(marker={'color': "#CC0044", 'line_width': 1})
        else:
            st.warning("No data available for the selected year and quarter.")

        fig = px.choropleth(
            pd.json_normalize(india_states["features"])["properties.ST_NM"],
            locations="properties.ST_NM",
            geojson=india_states,
            featureidkey="properties.ST_NM",
            color_discrete_sequence=["red"], )

        fig.update_geos(fitbounds="locations", visible=False)

        if not lat_lon_df.empty:
            fig.add_trace(fig1.data[0])

        fig.update_layout(height=1000, width=700)

        # remove white background
        fig.update_geos(bgcolor='#F8F8F8', showland=True)

        st.plotly_chart(fig)
# ------------------------------------User Mobile Brand analysis--------------------------------------------------------
if menu == 'User Mobile Brand':

    st.markdown("<h1 style='text-align:center; color:red;'"
                ">Mobile Brand Analysis by State</h1>",
                unsafe_allow_html=True)

    StateBar = st.selectbox('Please select State', stateTuple, index=30)
    yearBar = st.radio('Please select the Year:', yearTuple, horizontal=True)
    quarterBar = st.radio('Please select the Quarter:', quarterTuple, horizontal=True)

    UserByBrand_filter = brandsused[(brandsused['State'] == StateBar)
                                        & (brandsused['Year'] == int(yearBar))
                                        & (brandsused['Quarter'] == quarterBar)]

    userBrand = px.bar(UserByBrand_filter,
                       x='Brand',
                       y='Brand_count',
                       color='Brand',
                       title='User Mobile Brand Analysis ',
                       color_continuous_scale='magma', )

    st.plotly_chart(userBrand)
# ------------------------------------User Mobile Brand Percentage Analysis---------------------------------------------
if menu == 'Brand percentage':
    st.markdown("<h1 style='text-align:center; color:red;'"
                ">Mobile Brand Percentage Analysis</h1>",
                unsafe_allow_html=True)

    StatePie = st.selectbox('Please Choose State', stateTuple, index=30)
    yearPie = st.radio('Please Choose the Year:', yearTuple, horizontal=True)
    quarterPie = st.radio('Please choose the Quarter:', quarterTuple, horizontal=True)

    UserByBrand_filterPie = brandsused[(brandsused['State'] == StatePie)
                                        & (brandsused['Year'] == int(yearPie))
                                        & (brandsused['Quarter'] == quarterPie)]

    BrandPercent = px.pie(UserByBrand_filterPie,
                       names='Brand',
                       values='Brand_percentage',
                       color='Brand',
                       template='plotly_dark',
                       title='User Mobile Brand in percentage ',
                       width=800,
                       height=600)

    BrandPercent.update_traces(textposition='inside',
                               textinfo='percent+label',
                               textfont_size=15,
                               insidetextorientation='radial',
                               pull=[0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                               marker=dict(line=dict(color='#000000', width=2)))

    BrandPercent.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')

    st.plotly_chart(BrandPercent)
# ------------------------------------User Mobile Brand Percentage Analysis End ----------------------------------------