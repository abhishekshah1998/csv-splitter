import os

import pandas as pd
import streamlit as st

from csv_splitter import split_dataframe


st.set_page_config(page_title="CSV Splitter", layout="centered")
st.title("📄 CSV Splitter (10,000 rows per file)")

st.markdown("""
Upload a CSV file, and we'll split it into multiple CSV files, 
each with **up to 10,000 rows (header + 9,999 records)**.
""")

uploaded_file = st.file_uploader("🔼 Upload your CSV file", type="csv")

if uploaded_file:
    file_name = uploaded_file.name
    base_name, _ = os.path.splitext(file_name)

    with st.spinner("Reading your CSV file..."):
        df = pd.read_csv(uploaded_file)

    total_rows = len(df)
    chunks = split_dataframe(df)
    num_chunks = len(chunks)

    st.success(f"✅ Successfully loaded `{file_name}` with **{total_rows} rows**.")
    st.info(f"Splitting into **{num_chunks} files** with up to **10,000 rows each** (including header).")

    with st.expander("📂 Download Your Chunks"):
        for index, buffer in enumerate(chunks, start=1):
            chunk_filename = f"{base_name}_part_{index}.csv"
            st.download_button(
                label=f"⬇️ Download {chunk_filename}",
                data=buffer,
                file_name=chunk_filename,
                mime="text/csv"
            )

    st.success("🎉 All chunks are ready! Download them above.")
