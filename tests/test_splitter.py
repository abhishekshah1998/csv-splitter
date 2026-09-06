from __future__ import annotations

from io import BytesIO
import unittest

import pandas as pd

from csv_splitter import split_dataframe


class SplitDataframeTests(unittest.TestCase):
    def read(self, buffer: BytesIO) -> pd.DataFrame:
        buffer.seek(0)
        return pd.read_csv(buffer)

    def test_preserves_every_record_and_header(self) -> None:
        source = pd.DataFrame({"id": range(20_005), "label": ["item"] * 20_005})

        chunks = split_dataframe(source)

        self.assertEqual([len(self.read(chunk)) for chunk in chunks], [9_999, 9_999, 7])
        combined = pd.concat([self.read(chunk) for chunk in chunks], ignore_index=True)
        pd.testing.assert_frame_equal(combined, source)

    def test_exact_boundary_needs_one_chunk(self) -> None:
        source = pd.DataFrame({"id": range(9_999)})

        chunks = split_dataframe(source)

        self.assertEqual(len(chunks), 1)
        self.assertEqual(len(self.read(chunks[0])), 9_999)

    def test_empty_input_returns_header_only_csv(self) -> None:
        source = pd.DataFrame(columns=["id", "label"])

        [chunk] = split_dataframe(source)

        self.assertEqual(chunk.getvalue().decode("utf-8"), "id,label\n")

    def test_rejects_limit_without_record_capacity(self) -> None:
        with self.assertRaises(ValueError):
            split_dataframe(pd.DataFrame({"id": [1]}), total_row_limit=1)


if __name__ == "__main__":
    unittest.main()
