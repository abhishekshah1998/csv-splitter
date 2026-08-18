from pathlib import Path

import pandas as pd
import streamlit as st

from csv_splitter import create_zip, split_dataframe


st.set_page_config(page_title="CSV Splitter", page_icon="✂️")
st.title("CSV Splitter")
st.write(
    "Split a large CSV into upload-ready files while preserving the header in every part."
)

max_rows_per_file = st.number_input(
    "Maximum rows per output file, including the header",
    min_value=2,
    max_value=1_000_000,
    value=10_000,
    step=1_000,
)
uploaded_file = st.file_uploader("Upload CSV", type="csv")

if uploaded_file:
    try:
        with st.spinner("Reading and splitting the file..."):
            dataframe = pd.read_csv(uploaded_file)
            base_name = Path(uploaded_file.name).stem
            chunks = split_dataframe(dataframe, int(max_rows_per_file))
            archive = create_zip(chunks, base_name)

        st.success(
            f"Prepared {len(chunks)} file{'s' if len(chunks) != 1 else ''} "
            f"from {len(dataframe):,} data rows."
        )
        st.download_button(
            "Download all parts as ZIP",
            data=archive,
            file_name=f"{base_name}_parts.zip",
            mime="application/zip",
        )

        with st.expander("Preview output plan"):
            for index, chunk in enumerate(chunks, start=1):
                st.write(f"Part {index}: {len(chunk):,} data rows")
    except (pd.errors.ParserError, UnicodeDecodeError, ValueError) as error:
        st.error(f"This file could not be processed: {error}")
