# CSV Splitter

A small Streamlit utility that splits a CSV into upload-ready chunks while preserving the header in every output file.

## The problem

Some operational systems limit CSV imports to 10,000 total rows per file. Manually dividing a larger export is repetitive and easy to get wrong—especially when the header must be counted in that limit.

CSV Splitter turns that constraint into a simple self-serve workflow:

1. Upload a CSV.
2. The app reads the file and reports its record count.
3. Records are divided into chunks of at most 9,999 rows.
4. Each downloaded file includes the original header, keeping the total at or below 10,000 rows.

## Current capabilities

- Browser-based CSV upload
- Deterministic 9,999-record chunking
- Header preservation in every output
- Predictable filenames such as `orders_part_1.csv`
- Individual downloads generated in memory

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Then open the local address printed by Streamlit.

## Implementation

The app uses Streamlit for the interface and pandas for parsing, slicing, and exporting CSV data. Uploaded data and generated chunks are held in memory; the current implementation does not write them to local disk.

## Current limitations

- The full input and all generated chunks must fit in memory.
- Parsing uses pandas defaults; unusual delimiters or encodings are not configurable yet.
- Downloads are provided one file at a time rather than as a ZIP archive.
- This is a focused utility, not a hosted service with persistence, authentication, or compliance controls.

## Product direction

Useful next steps would include streaming large inputs, delimiter and encoding controls, ZIP export, configurable row limits, and automated validation of each output file.
