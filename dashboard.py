import logging
import streamlit as st
import pandas as pd
from geo_ip_lookup import GeoIPLookup
import folium
import streamlit_folium

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def Dashboard():

    st.title("Cowrie HoneyPot Dashboard")

    df = pd.read_csv("cowrie.csv", names=["timestamp","src_ip", "username", "password"])

    st.subheader("Most Used Passwords")
    df_password_used = df['password'].value_counts().sort_values(ascending=False).head(10)
    st.bar_chart(df_password_used)

    st.subheader("Source IPs with the Most Login Attempts")
    df_src_ip_attempts = df['src_ip'].value_counts().sort_values(ascending=False).head(10)
    st.bar_chart(df_src_ip_attempts)

    st.subheader("Location of Source IPs")
    map = folium.Map(location=[0, 0], zoom_start=2)
    for ip in df['src_ip'].unique():
        location = GeoIPLookup(ip)
        folium.Marker([location['latitude'], location['longitude']], popup=location, icon=folium.Icon(color='red')).add_to(map)

    streamlit_folium.st_folium(map, width=700, height=500)

    st.subheader("Number of attacks per country")
    df_country_count = df['src_ip'].apply(lambda ip: GeoIPLookup(ip)['country']).value_counts().sort_values(ascending=False).head(10)
    st.bar_chart(df_country_count)

    # Timeline for Login Attempts
    st.subheader("Timeline of Login Attempts")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df_resampled = df.resample('D').size()
    st.line_chart(df_resampled)

dashboard = Dashboard()