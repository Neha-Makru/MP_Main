import streamlit as st
from Learning_path import display_learning_path
from time_series_analysis import time_series_analysis
from statistical_tests import statistical_tests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from openpyxl import *
import plotly.express as px

st.set_page_config(page_title='DataViz Hub', page_icon='📊', layout='wide')
st.title('Your Data, Your Way')

def load_data(file):
    """Load a CSV or Excel file into a DataFrame."""
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file, engine='openpyxl')
        else:
            st.warning("Unsupported file type")
            return None
        return df
    except Exception as e:
        st.warning(f"Warning: {e}")
        return None

def convert_df(df):
    """Convert DataFrame to CSV format for download."""
    return df.to_csv(index=False).encode('utf-8')

option = st.sidebar.radio("Select a feature",
                         ('Data Analysis 📈',
                          'Time Series Analysis ⏳',
                          'Statistical Tests & Hypothesis Testing 📊',
                          'Learning Path 📚'), index=0)

if option == 'Data Analysis 📈':
    uploaded_file = st.file_uploader("Upload your Excel or CSV file here", type=['csv', 'xlsx'], key="data_analysis_file")

    if uploaded_file is not None:
        df = load_data(uploaded_file)
        if df is not None:
            st.subheader("Data Preview")
            st.dataframe(df)

            st.subheader("Summary Statistics")
            st.write(df.describe())

            st.subheader("Correlation Heatmap")
            if st.button('Show Correlation Heatmap'):
                numeric_df = df.select_dtypes(include=[np.number])
                if numeric_df.empty:
                    st.warning("No numeric columns to compute correlation.")
                else:
                    corr = numeric_df.corr()
                    plt.figure(figsize=(10, 6))
                    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
                    st.pyplot(plt)

            csv = convert_df(df)
            st.download_button(
                label="Download filtered data as CSV",
                data=csv,
                file_name='Processed_data.csv',
                mime='text/csv')

            st.subheader("Filter Data")
            for col in df.select_dtypes(include=['object']).columns:
                unique_vals = df[col].unique()
                selected_vals = st.multiselect(f"Filter {col}", unique_vals)
                if selected_vals:
                    df = df[df[col].isin(selected_vals)]

            st.write('Filtered Data', df)

            st.subheader('Select columns for visualization')
            columns = df.columns.tolist()
            selected_columns = st.multiselect('Select Columns: ', columns)

            if selected_columns and len(selected_columns) >= 2:
                st.subheader('Visualization Options')
                plot_type = st.selectbox('Select type of plot', ['Bar Chart', 'Line Chart', 'Scatter Plot', 'Box Plot', 'Pie Chart'])

                st.subheader(f"{plot_type} of selected columns")
                x_col = st.selectbox('Select X-axis', selected_columns)
                y_col = st.multiselect('Select Y-axis', selected_columns)

                if x_col and y_col:
                    plt.figure(figsize=(10, 6))

                    if plot_type == "Bar Chart":
                        sns.barplot(x=x_col, y=y_col[0], data=df)
                    elif plot_type == "Line Chart":
                        for y in y_col:
                            sns.lineplot(x=x_col, y=y, data=df, label=y)
                    elif plot_type == "Scatter Plot":
                        sns.scatterplot(x=x_col, y=y_col[0], data=df)
                    elif plot_type == "Box Plot":
                        sns.boxplot(x=x_col, y=y_col[0], data=df)
                    elif plot_type == "Pie Chart":
                        if df[y_col[0]].dtype == 'object':
                            pie_data = df[y_col[0]].value_counts()
                            plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
                        else:
                            plt.pie(df[y_col[0]], labels=df[x_col], autopct='%1.1f%%')
                        plt.axis('equal')
                    st.pyplot(plt)

                st.subheader("Interactive Plot")
                if st.button("Show Interactive Plot"):
                    fig = px.scatter(df, x=x_col, y=y_col[0])
                    st.plotly_chart(fig)

            else:
                st.warning("Please select at least two columns for visualization.")

            if df.isnull().values.any():
                st.warning("Dataset contains missing values")
                missing_option = st.selectbox("How would you like to handle the missing values?",
                                              ('Drop Rows', 'Fill With Mean', 'Fill With Median'))

                if missing_option == 'Drop Rows':
                    df = df.dropna()
                elif missing_option == 'Fill With Mean':
                    df = df.fillna(df.mean())
                elif missing_option == 'Fill With Median':
                    df = df.fillna(df.median())

                st.write('Data after handling the missing values: ', df)

            st.subheader('Group Data And Aggregate')
            group_by_col = st.selectbox('Select column to group by', columns)
            agg_col = st.selectbox('Select column to aggregate', df.select_dtypes(include=np.number).columns)
            agg_func = st.selectbox('Select aggregation function', ['sum', 'mean', 'max', 'min'])

            if group_by_col and agg_col and agg_func:
                grouped_df = df.groupby(group_by_col).agg({agg_col: agg_func})
                st.write(grouped_df)

    else:
        st.write('Upload a CSV or Excel file to proceed.')

elif option == 'Time Series Analysis ⏳':
    st.subheader("Time Series Analysis")
    st.write("""
    Time series analysis involves analyzing data points collected or recorded at specific time intervals. 
    It helps in identifying trends, patterns, and seasonal variations in data over time.
    Common applications include stock price prediction, weather forecasting, and sales analysis.
    """)

    uploaded_file = st.file_uploader("Upload your Excel or CSV file for Time Series Analysis", type=['csv', 'xlsx'], key="time_series_file")

    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None:
            st.subheader("Time Series Data Preview")
            st.dataframe(df)

            date_column = st.selectbox("Select Date Column", df.columns)
            if date_column:
                try:
                    df[date_column] = pd.to_datetime(df[date_column])
                    value_column = st.selectbox("Select Value Column", df.columns)
                    
                    if value_column:
                        df.set_index(date_column, inplace=True)

                        st.subheader(f"Time Series Plot of {value_column}")
                        plt.figure(figsize=(10, 6))
                        sns.lineplot(data=df, x=df.index, y=value_column)
                        st.pyplot(plt)

                except KeyError as e:
                    st.error(f"Error: {e}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.warning("No data available for analysis.")
    else:
        st.write("Upload a CSV or Excel file to proceed with Time Series Analysis.")

elif option == 'Statistical Tests & Hypothesis Testing 📊':
    st.subheader("Statistical Tests & Hypothesis Testing")
    st.write("""
    Hypothesis testing helps determine whether the results from your data sample are statistically significant.
    The t-score and p-value are two key metrics used in hypothesis testing. 
    The t-score indicates how many standard deviations an element is from the mean, while the p-value helps assess 
    the strength of the results in relation to the null hypothesis.
    """)

    uploaded_file = st.file_uploader("Upload your Excel or CSV file for Statistical Tests", type=['csv', 'xlsx'], key="statistical_tests_file")

    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None:
            statistical_tests(df)
        else:
            st.warning("No data available for statistical testing.")
    else:
        st.write("Upload a CSV or Excel file to proceed with Statistical Tests.")
elif option == 'Learning Path 📚':
    display_learning_path()

