import streamlit as st
import pandas as pd
import plotly.express as px
from fetch_data import *

url = "https://www.aqhi.gov.hk/epd/ddata/html/out/24pc_Eng.xml"
data = requests_url(url)

_ = transform_data(data)
# -- Edit this path to your CSV file
CSV_PATH = "cleaned_data.csv"

st.title("ETL side project")

try:
    # Read CSV from path
    df = pd.read_csv(CSV_PATH)
    
    st.subheader("Preview of Data")
    # st.write(df)

    # Select columns for visualization
    numeric_cols = df.select_dtypes(include=['float', 'int']).columns.tolist()
    # st.write(numeric_cols)
    if len(numeric_cols) < 1:
        st.warning("No numeric columns available for plotting.")
    else:
        selected_station = st.selectbox("Select district", df.Station.unique())
        pollution_element = st.selectbox("Select pollutant", numeric_cols)
        filterd_df = df[df.Station == selected_station]

        # Interactive Plot
        fig = px.line(filterd_df, x="DateTime", y=filterd_df[pollution_element], title=f"{pollution_element} vs {selected_station}")
        fig.update_yaxes(title_text=f"{pollution_element}")
        st.plotly_chart(fig, use_container_width=True)
except FileNotFoundError:
    st.error(f"Could not find CSV file at path: {CSV_PATH}")
except Exception as e:
    st.error(f"An error occurred: {e}")