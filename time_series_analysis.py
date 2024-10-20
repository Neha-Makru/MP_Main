import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def time_series_analysis(df):
    """Function to perform Time Series Analysis and display results in the app."""
    if df is not None:
        st.subheader("Time Series Data Preview")
        st.dataframe(df.head())  

        date_column = st.selectbox("Select Date Column", df.columns)
        value_column = st.selectbox("Select Value Column", df.columns)

        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        df.set_index(date_column, inplace=True)

        df.dropna(subset=[value_column], inplace=True)

        st.subheader(f"Time Series Plot of {value_column}")
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=df, x=df.index, y=value_column)
        plt.xticks(rotation=45)
        st.pyplot(plt)
    else:
        st.warning("No data available for time series analysis.")
