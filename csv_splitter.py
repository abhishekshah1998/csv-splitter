from __future__ import annotations

from io import BytesIO
import math

import pandas as pd


DEFAULT_TOTAL_ROW_LIMIT = 10_000


def split_dataframe(
    dataframe: pd.DataFrame,
    total_row_limit: int = DEFAULT_TOTAL_ROW_LIMIT,
) -> list[BytesIO]:
    """Return CSV buffers whose row count includes one header row.

    An empty input still produces one valid header-only CSV so that the result
    can be imported or inspected consistently.
    """
    if total_row_limit < 2:
        raise ValueError("total_row_limit must leave room for a header and one record")

    records_per_chunk = total_row_limit - 1
    chunk_count = max(1, math.ceil(len(dataframe) / records_per_chunk))
    buffers: list[BytesIO] = []

    for index in range(chunk_count):
        start = index * records_per_chunk
        stop = start + records_per_chunk
        buffer = BytesIO()
        dataframe.iloc[start:stop].to_csv(buffer, index=False)
        buffer.seek(0)
        buffers.append(buffer)

    return buffers
