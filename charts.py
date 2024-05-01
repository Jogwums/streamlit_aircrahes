import streamlit as st 
import numpy as np 
import pandas as pd 
import plotly.figure_factory as ff
import plotly.express as px
# from app import aircraft_manufacturer_incidents, aircraft_type_incidents


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
st.title("Visuals")
df.columns
# dispaly metrics 
# total numbers 
try:
    month_names = df['Month Name'].unique()

    # bar 1
    data_monthly = px.histogram(df, x='Month Name',y='Aboard',text_auto='.2s',
                          title="Monthly Passenger Incidents")
    st.plotly_chart(data_monthly)

    # line 1 
    line1 = px.line(df, x='Year', y='Fatalities (air)',
                    title='Yearly Fatalities')
    st.plotly_chart(line1)

    # scatter plot
    plot2 = px.scatter(df,x='Ground', y='Fatalities (air)',
                       title='Ground Casualties vs. Fatalities'
                       )
    st.plotly_chart(plot2)

    st.sidebar.button("Refresh")

    selected_months = st.sidebar.multiselect("Months",month_names,month_names[0])

    filtered_months = df[df['Month Name'].isin(selected_months)]

    # px.histogram
    # bar 2 from filtered data
    data_monthly = px.histogram(filtered_months, x='Month Name',y='Aboard',
                          color="Quarter",
                          title="Monthly Passenger Incidents")
    st.plotly_chart(data_monthly)

    # view aircraft dets
    aircaft__ = st.session_state.aircraft_type_incidents
    aircaft__table = aircaft__.reset_index()[:10]
    st.dataframe(aircaft__table)
    bar3 = px.histogram(aircaft__table, x='Aircraft', y='count',
                        color='Aircraft', 
                        title='top 10 problematic aircrafts',
                        labels={'y':'nos'})
    st.plotly_chart(bar3)


except:
    st.error('This is an error', icon="🚨")
