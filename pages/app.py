import streamlit as st 
import numpy as np 
import pandas as pd 
import plotly.figure_factory as ff

@st.cache_data
def load_data():
    df = pd.read_csv("aircrashesFullData.csv")
    # save month names
    df['Month Name'] = df['Month']
    month_mapping = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    # Map month names to numeric values
    df['Month'] = df['Month'].map(month_mapping)
    # Combine 'Year', 'Month', and 'Day' columns into a single 'Date' column
    df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
    return df 

df = load_data()
st.title("Air crashes App")

# dispaly metrics 
# total numbers 
try:
    total_aboard = df["Aboard"].sum()
    total_ground = df["Ground"].sum()
    total_fatalities = df["Fatalities (air)"].sum()

    st.subheader("Totals")
    cols1, cols2, cols3 = st.columns(3)
    cols1.metric("Total Aboard", total_aboard)
    cols2.metric("Total Fatalities", total_fatalities)
    cols3.metric("Total Ground", total_ground)

    percent_fatalities = (total_fatalities ) / (total_aboard) * 100
    cols1.metric("Fatalities Ratio", f'{np.round(percent_fatalities,2)}%')

    # filters 
    st.sidebar.title("Select Filters")
    # year 
    year = df['Year'].unique()
    selected_year = st.sidebar.multiselect('Year', year, [year[0],year[-1]])
    filtered_year = df[df["Year"].isin(selected_year)]

    # manufacturers
    manu = df['Aircraft Manufacturer'].unique()
    selected_manu = st.sidebar.multiselect('Manufacturers', manu, manu[3])
    filtered_manu = df[df["Aircraft Manufacturer"].isin(selected_manu)]
    # country
    cntry = df['Country/Region'].unique()
    selected_cntry = st.sidebar.multiselect('Country/Region', cntry, cntry[2])
    filtered_cntry = df[df["Country/Region"].isin(selected_cntry)]

    # location
    loca = df['Location'].unique()
    selected_loca = st.sidebar.multiselect('Location', loca, loca[2])
    filtered_loca = df[df["Location"].isin(selected_loca)]

    # aircraft
    craft = df['Aircraft'].unique()
    selected_craft = st.sidebar.multiselect('Aircraft', craft, craft[2])
    filtered_craft = df[df["Aircraft"].isin(selected_craft)]

    # operator
    ops = df['Operator'].unique()
    selected_ops = st.sidebar.multiselect('Operator', ops, ops[2])
    filtered_ops = df[df["Operator"].isin(selected_ops)]

    # display filtered result
    st.subheader("display filtered results table")
    if not selected_manu:
        st.write('Please select a company') 
    else:
        st.dataframe(filtered_manu)

    st.divider()

    # # 1. Trend Analysis
    yearly_incidents = df.groupby('Year').size()
    quarterly_incidents = df.groupby(['Year', 'Quarter']).size()
    monthly_incidents = df.groupby(['Year', 'Month']).size()

    col4, col5, col6 = st.columns(3)
    col4.subheader("Yearly Incidents:\n",)
    col4.dataframe(yearly_incidents)
    col5.subheader("\nQuarterly Incidents:\n")
    col5.dataframe( quarterly_incidents)
    col6.subheader("\nMonthly Incidents:\n",)
    col6.dataframe( monthly_incidents)

    st.divider()
    # 2. Geographical Analysis
    st.subheader('Geographical Analysis')
    top_countries = df['Country/Region'].value_counts().head(10)
    location_incidents = df['Location'].value_counts()

    col4.subheader('Top Countries')
    col4.dataframe(top_countries)

    col6.subheader('Locations')
    col6.dataframe(location_incidents)

    st.divider()
    # 3. Aircraft Analysis
    st.subheader('Aircraft Analysis')
    aircraft_manufacturer_incidents = df['Aircraft Manufacturer'].value_counts()
    aircraft_type_incidents = df['Aircraft'].value_counts()

    if aircraft_type_incidents not in st.session_state:
        st.session_state.aircraft_type_incidents = df['Aircraft'].value_counts()

    

except:
    st.error("Wait")
