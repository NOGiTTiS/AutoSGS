"""
Unit tests for autosgs.core.clipboard_parser
"""

import pytest
from autosgs.core.clipboard_parser import parse_tsv, ScoreMatrix


def test_parse_empty():
    assert parse_tsv("").is_empty
    assert parse_tsv(None).is_empty
    assert parse_tsv("   \n\r\n  ").is_empty


def test_parse_single_column():
    raw = "10\n15\n20\n\n"
    matrix = parse_tsv(raw)
    assert matrix.total_rows == 3
    assert matrix.total_columns == 1
    assert matrix.total_cells == 3
    assert matrix.empty_cells_count == 0
    assert matrix.rows == [["10"], ["15"], ["20"]]


def test_parse_multi_column_tsv():
    raw = "10\t18\t20\r\n15\t\t19\r\n12\t14\t16\r\n"
    matrix = parse_tsv(raw)
    assert matrix.total_rows == 3
    assert matrix.total_columns == 3
    assert matrix.total_cells == 9
    assert matrix.empty_cells_count == 1  # 1 empty cell in row 2 col 2
    assert matrix.rows[0] == ["10", "18", "20"]
    assert matrix.rows[1] == ["15", "", "19"]
    assert matrix.rows[2] == ["12", "14", "16"]


def test_parse_irregular_columns_padded():
    raw = "10\t20\n30\n40\t50\t60"
    matrix = parse_tsv(raw)
    assert matrix.total_rows == 3
    assert matrix.total_columns == 3
    assert matrix.rows[0] == ["10", "20", ""]
    assert matrix.rows[1] == ["30", "", ""]
    assert matrix.rows[2] == ["40", "50", "60"]
    assert matrix.empty_cells_count == 3


def test_parse_thai_and_decimals():
    raw = "15.5\tข\n18.0\t20"
    matrix = parse_tsv(raw)
    assert matrix.total_rows == 2
    assert matrix.total_columns == 2
    assert matrix.rows[0] == ["15.5", "ข"]
    assert matrix.rows[1] == ["18.0", "20"]
    assert matrix.empty_cells_count == 0


def test_parse_multi_column_with_trailing_empty_tabs():
    # 5 students with 2 columns, but only students 1 and 2 have scores; students 3-5 are empty tabs
    raw = "10\t15\n18\t20\n\t\n\t\n\t"
    matrix = parse_tsv(raw)
    assert matrix.total_rows == 5
    assert matrix.total_columns == 2
    assert matrix.rows[0] == ["10", "15"]
    assert matrix.rows[1] == ["18", "20"]
    assert matrix.rows[2] == ["", ""]
    assert matrix.rows[3] == ["", ""]
    assert matrix.rows[4] == ["", ""]
    assert matrix.empty_cells_count == 6


def test_parse_comments_ignored_from_cells():
    # Any comment starting with '#' is safely ignored
    raw = "# Some comment\n10\t15\n20\t25"
    matrix = parse_tsv(raw)
    assert matrix.total_rows == 2
    assert matrix.total_columns == 2
    assert matrix.rows[0] == ["10", "15"]
    assert matrix.rows[1] == ["20", "25"]


