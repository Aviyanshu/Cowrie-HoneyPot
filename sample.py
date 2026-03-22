import streamlit as st
import pandas as pd
import numpy as np

# Sample data
df = pd.DataFrame(
    np.random.randn(1000, 2) / 50 + [37.76, -122.4],
    columns=['lat', 'lon']
)

st.map(df)