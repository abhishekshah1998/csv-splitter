import streamlit as st
import pandas as pd
import math
from io import BytesIO

st.title("CSV Splitter (10,000 rows per file)")

uploaded_file = st.file_uploader("Upload your CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    total_rows = len(df)
    chunk_size = 9999  # because header + 9999 records = 10,000
    num_chunks = math.ceil(total_rows / chunk_size)

    st.write(f"Total rows: {total_rows}")
    st.write(f"Splitting into {num_chunks} chunks of up to 10,000 rows (header + 9999 records).")

    for i in range(num_chunks):
        start_row = i * chunk_size
        end_row = start_row + chunk_size
        chunk_df = df.iloc[start_row:end_row]

        buffer = BytesIO()
        chunk_df.to_csv(buffer, index=False)
        buffer.seek(0)

        st.download_button(
            label=f"Download chunk {i+1}",
            data=buffer,
            file_name=f"chunk_{i+1}.csv",
            mime="text/csv"
        )
