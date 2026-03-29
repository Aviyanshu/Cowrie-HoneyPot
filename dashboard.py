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

    st.write("""
             Cowrie is a popular honeypot that stimulates a vulnerable SSH and Telnet server to attract and log malicious login attempts. This simple project aims to analyze the data collected from Cowrie honeypot and visualize it using charts. This dashboard provides a basic overview on the most commonly used passwords, source IPs with the most login attempts, geographical locations of source IPs, and the timeline of login attempts. The data was collected from `March 15, 2026` to `March 29,2026` and contains a total of `22030` login attempts. \n
             Tools used:
             1. Cowrie Honeypot: To collect data on login attempts (SSH only)
             2. Python: For data parsing and analysis
             3. Pandas: For data management
             4. GeoLite2 Database: For geolocation of IP addresses
             5. Folium: For creating interactive maps
             6. Streamlit: For creating the interactive dashboard
             7. Streamlit-Folium: For integrating Folium maps into Streamlit
             """)

    df = pd.read_csv("./data/cowrie.csv", names=["timestamp","src_ip", "username", "password","country", "latitude", "longitude"], engine='python', on_bad_lines='skip')

    st.subheader("Most Used Passwords")

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        df_password_used = df['password'].value_counts().sort_values(ascending=False).head(10)
        st.bar_chart(df_password_used, horizontal=True)

    with col2:
        st.write("""
                 This chart shows the most commonly used passwords in the login attempts. It can provide insights into the attacker's behavior and the types of passwords they are trying to use.\n
                 The chart clearly shows that the most commonly used password is the word "password" itself with a value of `43`, followed by "admin" and "123456" both with a value of `41`. This result is in line with common password usage patterns observed in various researches done on most common passwords. In 2025, the most commonly used password was "123456" closely followed by "password". This indicates that attackers rely on commonly used passwords to gain access to systems, which emphasizes the importance of using strong and unique passwords to protect against such malicious activities.
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
                 The map on the left shows the geographical locations of the source IPs that attempted to log in to the honeypot. Each marker represents the exact location of an IP address based on the latitude and logitude data. GeoLite2 database was used to determine the location of the IP addresses. It is important to note that accuracy of the geolocation data can vary, and some IP addresses may not be precisely located. \n
                 The visualization of source IP provides a brief insight into the geographical pattern of attacks and can help identify potential hotspots for malicious activity. "Indonesia" is the country with th most login attempts, with a large value of `21321` attemps, followed by United States with `237` attempts, and The Netherlands with `141`. 
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

    st.write("""
             The line chart above shows the timeline of login attempts. There is a regular pattern of login attempts with peaks at certain times until `March 22` where there is a huge spike in login attempts. On further analysing the data, it was found that the spike was from Indonesia, which is the country with the most login attempts. This spike could be due to a specific attack campaign. Otherwise the overall pattern of login attempts is relatively consistent. 
             """)

dashboard = Dashboard()