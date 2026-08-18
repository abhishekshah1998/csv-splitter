from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

import pandas as pd


def split_dataframe(
    dataframe: pd.DataFrame, max_rows_per_file: int = 10_000
) -> list[pd.DataFrame]:
    """Split data while reserving one row per output file for the CSV header."""
    if max_rows_per_file < 2:
        raise ValueError("max_rows_per_file must allow one header and one data row.")

    data_rows_per_chunk = max_rows_per_file - 1
    if dataframe.empty:
        return [dataframe.copy()]

    return [
        dataframe.iloc[start : start + data_rows_per_chunk].copy()
        for start in range(0, len(dataframe), data_rows_per_chunk)
    ]


def create_zip(chunks: list[pd.DataFrame], base_name: str) -> bytes:
    """Package CSV chunks into one download to avoid repetitive browser actions."""
    archive_buffer = BytesIO()
    with ZipFile(archive_buffer, "w", ZIP_DEFLATED) as archive:
        for index, chunk in enumerate(chunks, start=1):
            archive.writestr(
                f"{base_name}_part_{index}.csv",
                chunk.to_csv(index=False),
            )
    return archive_buffer.getvalue()
