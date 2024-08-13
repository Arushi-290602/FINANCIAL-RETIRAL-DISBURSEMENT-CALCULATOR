import streamlit as st
import pandas as pd


def disp_results(file_name):
    df = pd.read_csv(file_name)

    # Create a new DataFrame without the index
    df_no_index = df.reset_index(drop=True)

    # Apply CSS styling
    css = """
        <style>
            table {
                border-collapse: collapse;
                width: 100%;
            }
            th, td {
                text-align: left;
                padding: 8px;
                background-color: #f9f9f9;  /* Apply the same background color to header and data cells */
            }
            th {
                color: black;  /* Set text color for headers */
            }
            tr {
                background-color: #f9f9f9;
            }
        </style>
        """

    # Display CSS styling
    st.markdown(css, unsafe_allow_html=True)

    # Convert DataFrame to HTML with no index and display it
    st.write(df_no_index.to_html(index=False, escape=False), unsafe_allow_html=True)
#disp_results("financial_instruments_data.csv")
