# CSV Splitter

A small self-serve utility for splitting a large CSV into files that comply with row-count limits while preserving the header in every output.

## Product brief

**User:** Operations and data teams moving records between systems with file-size or row-count constraints.

**Problem:** Manually splitting files is repetitive and error-prone. A technically valid split can still fail when a receiving system counts the header toward its row limit.

**Approach:** Let the user select the destination limit, reserve one row for the header, preview the output plan, and package all parts into a single ZIP download.

## Product decisions

- The row limit is configurable because different destination systems impose different constraints.
- Every output includes the original header.
- A single ZIP replaces a long sequence of individual downloads.
- Processing happens within the Streamlit session; the application does not intentionally persist uploaded data.
- Splitting and archive creation live outside the UI so the core behavior can be tested independently.

## Run locally

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

Run tests:

```bash
python -m pip install -r requirements-dev.txt
pytest
```

## Success metrics for a production version

- successful processing rate by file size and encoding;
- time from upload to completed download;
- percentage of generated files accepted by the target system;
- repeat usage; and
- support requests caused by row-count or formatting issues.

## Limitations and next steps

Very large files currently load into memory through pandas. A production version should add streamed parsing, encoding and delimiter controls, file-size guidance, and schema validation for common destination systems.
