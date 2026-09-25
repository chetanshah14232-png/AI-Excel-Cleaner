import pandas as pd
import streamlit as st
import sqlite3
import io
import zipfile

st.title('AI_AUTOMATION_TOOL')

uploaded_files = st.file_uploader(
    label='Upload Your Messy Files and Get Cleaned CSVs.',
    type=["xlsx"],
    accept_multiple_files=True
)

if uploaded_files:
    st.info(f"Total {len(uploaded_files)} file(s) uploaded. Processing started...")

    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        conn = sqlite3.connect('B_data.db')

        for file in uploaded_files:
            try:
                df = pd.read_excel(file)

                table_name = file.name.split('.')[0].replace(" ", "_").lower()

                df.to_sql(table_name, conn, index=False, if_exists='replace')

                csv_data = df.to_csv(index=False).encode('utf-8')

                csv_filename = f"{table_name}_cleaned.csv"
                zip_file.writestr(csv_filename, csv_data)

            except Exception as e:
                st.error(f"Error processing {file.name}: {e}")

        conn.close()

    st.success("All files successfully processed, saved to SQLite, and packed!")

    zip_buffer.seek(0)

    st.download_button(
        label="Download All Cleaned CSVs (ZIP)",
        data=zip_buffer,
        file_name="cleaned_files_batch.zip",
        mime="application/zip",
    )
