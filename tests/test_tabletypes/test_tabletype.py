from pathlib import Path

from tabler import Table

from ..test_tabler import TableTest


class TableTypeTest(TableTest):
    tabletype = None
    BASIC_FILE_PATH = None
    WITH_NULLS_PATH = None
    WITH_INCOMPLETE_ROW = None
    WITH_LONG_ROW = None

    def test_open(self):
        path = str(self.BASIC_FILE_PATH)
        table = Table(path, table_type=self.tabletype)
        self.is_valid_table(table)

    def test_write(self, tmpdir):
        out_table = self.get_basic_table()
        filepath = Path(str(tmpdir)) / "testfile{}".format(self.tabletype.extension)
        out_table.write(filepath, table_type=self.tabletype)
        in_table = Table(filepath, table_type=self.tabletype)
        assert [list(_) for _ in in_table] == [list(_) for _ in out_table]

    def test_read_null_values(self):
        table = Table(str(self.WITH_NULLS_PATH), table_type=self.tabletype)
        assert list(table[0]) == ["Red", self.tabletype.empty_value, "Blue"]

    def test_write_null_values(self, tmpdir):
        table = Table(
            header=["Col1", "Col2", "Col3"],
            data=[
                ["Red", self.tabletype.empty_value, "Blue"],
                ["Orange", "Yellow", "Magenta"],
            ],
        )
        path = Path(str(tmpdir.join("empty_test")))
        table.write(filepath=str(path), table_type=self.tabletype)

    def test_read_incomplete_rows(self):
        table = Table(str(self.WITH_INCOMPLETE_ROW), self.tabletype)
        assert list(table[0]) == ["Red", "Green", self.tabletype.empty_value]

    def test_write_incomplete_rows(self, tmpdir):
        table = Table(
            header=["Col1", "Col2", "Col3"],
            data=[["Red"], ["Orange", "Yellow", "Magenta"]],
        )
        path = Path(str(tmpdir.join("empty_test")))
        table.write(filepath=str(path), table_type=self.tabletype)

    def test_read_long_rows(self):
        table = Table(str(self.WITH_LONG_ROW), self.tabletype)
        assert table.header == ("Col1", "Col2", "Col3", table._EMPTY_HEADER.format(1))
        assert list(table[0]) == ["Red", "Green", "Blue", "Purple"]

    def test_write_long_rows(self, tmpdir):
        table = Table(
            header=["Col1", "Col2", "Col3"],
            data=[["Red", "Green", "Blue", "Purple"], ["Orange", "Yellow", "Magenta"]],
        )
        path = Path(str(tmpdir.join("empty_test")))
        table.write(filepath=str(path), table_type=self.tabletype)