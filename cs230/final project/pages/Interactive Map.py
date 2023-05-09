
import streamlit as st
import pydeck as pdk
import pandas as pd


path = "/Users/janhavi/Library/CloudStorage/OneDrive-BentleyUniversity/cs230/final project"

df_shipwreck = pd.read_csv(path + "/Shipwreck_Database.csv")

#df_shipwreck.set_index("SHIP'S NAME", inplace =True)

df_shipwreck.rename(columns={"LATITUDE":"lat", "LONGITUDE": "lon"}, inplace= True)

#Add a title
st.markdown("<span style= 'font-size: 45px'>**:green[Interactive Map]**</span>", unsafe_allow_html=True)

#slice dataframe
df_shipwreck = df_shipwreck[['lat', 'lon', 'YEAR', "SHIP'S NAME", 'VESSEL TYPE', 'LOCATION LOST']]

#convert values to numbers, eliminate blank spaces - https://www.geeksforgeeks.org/python-pandas-to_numeric-method/
df_shipwreck['lat'] = pd.to_numeric(df_shipwreck['lat'], errors = 'coerce')
df_shipwreck['lon'] = pd.to_numeric(df_shipwreck['lon'], errors = 'coerce')

df_shipwreck.dropna(inplace=True)


# SIDEBAR

#select type of map
selected_map = st.sidebar.radio("Please select the type of map", ["Simple", "Scatter"])


#select year of loss - slider

#show shipwrecks from given year or display message
selected_year = st.sidebar.slider("Please select year", 1738, 2020)
if selected_year > 1738:
    df_shipwreck = df_shipwreck[df_shipwreck['YEAR'] == selected_year]


#select vessel type - selectbox
selected_vessel = st.sidebar.selectbox("Please select vessel type", [" ", "Bark", "Brig","Schooner","Scow", "Steamship", "Yacht"])
if selected_vessel != " ":
    df_shipwreck = df_shipwreck[df_shipwreck['VESSEL TYPE'] == selected_vessel]


# MAP

#insert simple map
if selected_map == "Simple":
    st.header("Simple Map - Shipwrecks")
    st.map(df_shipwreck)

#insert scatter map
elif selected_map == "Scatter":
    st.header("Scatter Map - Shipwrecks")
    view_ship = pdk.ViewState(
            latitude=df_shipwreck["lat"].mean(), # The latitude of the view center
            longitude=df_shipwreck["lon"].mean(), # The longitude of the view center
            zoom=8, # View zoom level
            pitch=0) # Tilt level

    layer1 = pdk.Layer(type = 'ScatterplotLayer', # layer type
                          data=df_shipwreck, # data source
                          get_position='[lon, lat]', # coordinates
                          get_radius=800, # scatter radius
                          get_color=[0, 65, 95],   # scatter color
                          pickable=True # work with tooltip
                          )


    tool_tip = {"html": "Name: <b> {SHIP'S NAME} </b> <br/> Year Lost: <b>{YEAR}</b> <br/> Vessel Type: <b>{VESSEL TYPE}</b> <br/> Location Lost: <b>{LOCATION LOST}</b>",
                "style": {"backgroundColor": "salmon",
                          "color": "white"}
                }

    map = pdk.Deck(
        map_style='mapbox://styles/mapbox/outdoors-v11',
        # Go to https://docs.mapbox.com/api/maps/styles/ for more map styles
        initial_view_state=view_ship,
        layers=[layer1], # The following layer would be on top of the previous layers
        tooltip= tool_tip
    )

    #show map or display error - https://www.geeksforgeeks.org/python-pandas-dataframe-empty/
    if df_shipwreck.empty:
        st.success("No data matches your search. Please try again.")
    else:
        st.pydeck_chart(map)
