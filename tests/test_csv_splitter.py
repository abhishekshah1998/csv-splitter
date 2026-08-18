from io import BytesIO
from zipfile import ZipFile

import pandas as pd

from csv_splitter import create_zip, split_dataframe


def test_split_reserves_one_row_for_header():
    dataframe = pd.DataFrame({"id": range(20_001)})

    chunks = split_dataframe(dataframe, max_rows_per_file=10_000)

    assert [len(chunk) for chunk in chunks] == [9_999, 9_999, 3]


def test_empty_dataframe_still_produces_header_only_file():
    dataframe = pd.DataFrame(columns=["id", "name"])

    chunks = split_dataframe(dataframe)
    archive = create_zip(chunks, "empty")

    with ZipFile(BytesIO(archive)) as zip_file:
        assert zip_file.namelist() == ["empty_part_1.csv"]
        assert zip_file.read("empty_part_1.csv").decode() == "id,name\n"


def test_rejects_limit_without_room_for_data():
    dataframe = pd.DataFrame({"id": [1]})

    try:
        split_dataframe(dataframe, max_rows_per_file=1)
    except ValueError as error:
        assert "header" in str(error)
    else:
        raise AssertionError("Expected a ValueError")
