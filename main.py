import streamlit as st 
import os 
base_dir = os.getcwd()
file_1 = os.path.join(base_dir, "pages", "app.py")
file_2 = os.path.join(base_dir, "pages", "charts.py")

st.title("Welcome to Air crashes Analysis App")
st.subheader("Please select a page")

st.page_link(file_1, label="App page", icon="📌")

st.page_link(file_2, label="Charts", icon="😎")