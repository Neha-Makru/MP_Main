import streamlit as st

def display_learning_path():
    if 'step' not in st.session_state:
        st.session_state.step = 1
    
    if st.session_state.step == 1:
        st.title("Learning Path for Data Analysis")
        st.header("Step 1: Data Ingestion")
        st.write("The first step in any data analysis process is to import the data. We will work with CSV or Excel files, using Pandas to load them into a DataFrame.Data ingestion is the process of collecting and moving data from multiple sources to a central location for storage, processing, and analysis. It's a critical step in any data pipeline and is essential for many data-based operations, including analytics, visualization, and integration.")
        st.image("data_ingestion.png", caption="Data Ingestion Process", use_column_width=True)
        if st.button("Next"):
            st.session_state.step += 1

    elif st.session_state.step == 2:
        st.header("Step 2: Data Cleaning")
        st.write("Once the data is loaded, it often contains missing values, duplicates, or other inconsistencies. Cleaning the data ensures that your analysis will be accurate and meaningful.Data cleaning is the process of fixing or removing errors in data to make it more accurate and reliable for analysis. It's also known as data cleansing or scrubbing. Data cleaning is important because incorrect data can lead to unreliable results, which can negatively impact business activities.")
        st.image("data_cleaning.png", caption="Data Cleaning Techniques", use_column_width=True)
        if st.button("Next"):
            st.session_state.step += 1

    elif st.session_state.step == 3:
        st.header("Step 3: Exploratory Data Analysis (EDA)")
        st.write("Exploratory Data Analysis (EDA) is the process of visually and statistically examining your dataset to discover patterns, outliers, and relationships. EDA is an iterative process that involves visualizing, summarizing, and editing data. It often uses data visualization methods like scatterplots, correlation coefficients, and mapping.")
        st.image("eda.png", caption="Exploratory Data Analysis", use_column_width=True)
        if st.button("Next"):
            st.session_state.step += 1

    elif st.session_state.step == 4:
        st.header("Step 4: Data Visualization")
        st.write("Data visualization is the final step where we transform data into meaningful plots, charts, and graphs. This helps to communicate insights and trends effectively. Data visualization is the practice of translating information into a visual context, such as a map or graph, to make data easier for the human brain to understand and pull insights from. The main goal of data visualization is to make it easier to identify patterns, trends and outliers in large data sets.")
        st.image("data_visualization.png", caption="Data Visualization Techniques", use_column_width=True)
        if st.button("Next"):
            st.session_state.step += 1

    elif st.session_state.step == 5:
        st.header("Step 5: Grouping and Aggregation")
        st.write("Grouping and aggregation allow you to summarize data by specific groups. For instance, you can find the average salary by department or total sales by region. Grouping and aggregation is a data science technique that involves splitting data into groups, applying a function to each group, and combining the results into a data structure. It's a powerful way to summarize, analyze, and transform data.")
        st.image("grouping_aggregation.png", caption="Grouping & Aggregation", use_column_width=True)
        if st.button("Finish"):
            st.session_state.step += 1

    elif st.session_state.step == 6:
        st.balloons()
        st.write("Congratulations! You've completed the learning path.")
