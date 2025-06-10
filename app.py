import streamlit as st
import pandas as pd
import math
import os
from io import BytesIO

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
    chunk_size = 99999
    num_chunks = math.ceil(total_rows / chunk_size)

    st.success(f"✅ Successfully loaded `{file_name}` with **{total_rows} rows**.")
    st.info(f"Splitting into **{num_chunks} files** with up to **10,000 rows each** (including header).")

    chunks = []
    for i in range(num_chunks):
        start_row = i * chunk_size
        end_row = start_row + chunk_size
        chunk_df = df.iloc[start_row:end_row]

        buffer = BytesIO()
        chunk_df.to_csv(buffer, index=False)
        buffer.seek(0)

        chunk_filename = f"{base_name}_part_{i+1}.csv"
        chunks.append((chunk_filename, buffer))

    with st.expander("📂 Download Your Chunks"):
        for chunk_filename, buffer in chunks:
            st.download_button(
                label=f"⬇️ Download {chunk_filename}",
                data=buffer,
                file_name=chunk_filename,
                mime="text/csv"
            )

    st.success("🎉 All chunks are ready! Download them above.")

