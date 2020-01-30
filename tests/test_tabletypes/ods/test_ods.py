from pathlib import Path

from tabler import ODS, Table

from ...test_tools import TablerTestTools, TableTypeTestTools


class TestODS:
    tabletype = ODS()

    BASIC_FILE_PATH = Path(__file__).parent / "testfile.ods"
    WITH_NULLS_PATH = Path(__file__).parent / "testfile_empties.ods"
    WITH_INCOMPLETE_ROW = Path(__file__).parent / "testfile_incomplete_rows.ods"
    WITH_LONG_ROW = Path(__file__).parent / "testfile_long_rows.ods"
    TEST_FORMATTING = Path(__file__).parent / "test_format.ods"
    expected_formatting = [0, 0, "None", 893275023572039]

    def test_open(self):
        table = Table(self.BASIC_FILE_PATH, table_type=ODS())
        TablerTestTools.table_valid(table)

    def test_write(self, tmpdir):
        TableTypeTestTools.write_with_table_type(ODS(), tmpdir)

    def test_read_null_values(self):
        TableTypeTestTools.read_null_values_with_tabletype(ODS(), self.WITH_NULLS_PATH)

    def test_formatting(self):
        TableTypeTestTools.format_with_table_type(
            ODS(), self.TEST_FORMATTING, self.expected_formatting
        )

    def test_write_null_values(self, tmpdir):
        table = Table(
            header=["Col1", "Col2", "Col3"],
            data=[["Red", "", "Blue"], ["Orange", "Yellow", "Magenta"]],
        )
        path = Path(str(tmpdir.join("empty_test.csv")))
        expected = "Col1,Col2,Col3\nRed,,Blue\nOrange,Yellow,Magenta\n"
        table.write(filepath=str(path))
        with open(str(path), "r") as f:
            assert f.read() == expected

    def test_read_incomplete_rows(self):
        TableTypeTestTools.read_incomplete_rows_with_table_type(
            ODS(), self.WITH_INCOMPLETE_ROW
        )

    def test_write_incomplete_rows(self, tmpdir):
        TableTypeTestTools.write_incomplete_rows_with_table_type(ODS(), tmpdir)

    def test_read_long_rows(self):
        TableTypeTestTools.read_long_rows_with_table_type(ODS(), self.WITH_LONG_ROW)

    def test_open_file_without_table_type(self):
        TablerTestTools.table_valid(Table(str(Path(__file__).parent / "testfile.ods")))

    def test_write_long_rows_with(self, tmpdir):
        TableTypeTestTools.write_long_rows_with_table_type(ODS(), tmpdir)

    def test_save_file_without_extension(self, tmpdir):
        table = TablerTestTools.basic_table()
        filename = "testfile"
        path = str(tmpdir.join(filename))
        table.write(filepath=path, table_type=ODS())
        assert Path(path + ".ods").exists()

    def test_save_file_without_table_type(self, tmpdir):
        table = TablerTestTools.basic_table()
        filename = "testfile.csv"
        path = Path(str(tmpdir)) / filename
        table.write(filepath=str(path))
        assert path.exists()
