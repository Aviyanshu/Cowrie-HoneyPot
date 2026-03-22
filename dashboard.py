import logging
import streamlit as st
import pandas as pd
from geo_ip_lookup import GeoIPLookup
import folium
import streamlit_folium

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

st.set_page_config(layout="wide")

def Dashboard():

    st.title("Cowrie HoneyPot Dashboard")

    df = pd.read_csv("data/cowrie.csv", names=["timestamp","src_ip", "username", "password","country", "latitude", "longitude"])

    st.subheader("Most Used Passwords")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        df_password_used = df['password'].value_counts().sort_values(ascending=False).head(10)
        st.bar_chart(df_password_used, horizontal=True)

    with col2:
        st.write("""
                 Some text here about the most used passwords and their significance.
                 """)

    st.subheader("Source IPs with the Most Login Attempts")
    df_src_ip_attempts = df['src_ip'].value_counts().sort_values(ascending=False).head(10)
    st.bar_chart(df_src_ip_attempts)

    st.subheader("Location of Source IPs")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        map = folium.Map(location=[0, 0], zoom_start=2)
        for ip in df['src_ip'].unique():
            df_location = df[df['src_ip'] == ip].iloc[0]
            folium.Marker([df_location['latitude'], df_location['longitude']], popup=f"IP: {ip}", icon=folium.Icon(color='red')).add_to(map)

        streamlit_folium.st_folium(map, width=700, height=500)

    with col2:
        st.write("""
                 Some text here about the geographical distribution of the source IPs and any insights that can be drawn from it.
                 """)

    st.subheader("Number of attacks per country")
    df_country_count = df['country'].value_counts().sort_values(ascending=False).head(10)
    st.bar_chart(df_country_count)

    # Timeline for Login Attempts
    st.subheader("Timeline of Login Attempts")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df_resampled = df.resample('h').size()
    st.line_chart(df_resampled)

dashboard = Dashboard()