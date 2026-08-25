import pandas as pd
import streamlit as st
import sqlite3

st.title('AI_AUTOMATION_TOOL')

Your_file = st.file_uploader(label ='Upload Your Messy File and Just Get It Cleaned CSV.',type=["xlsx"])

if Your_file is not None:

    print("Your File Fetched Successfully")

    df = pd.read_excel(Your_file)
    conn = sqlite3.connect('B_data.db')
    df.to_sql('B_data', conn, index=False, if_exists='replace')
    conn.close()

    st.success("Data successfully saved to SQLite database!")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
    label="Download processed data as CSV",
    data=csv,
    file_name='processed_data.csv',
    mime='text/csv',
)