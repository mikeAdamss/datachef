"""
These tests are whoely concerned with testsing the dunder methods
controlling Input upon Input operators.
"""

import pytest

from pivoter.exceptions import UnalignedTableOperation
from pivoter.selection import datafuncs as dfc
from pivoter.selection.spreadsheet.xls import XlsInputSelectable
from tests.fixtures.preconfigured import fixture_simple_one_tab


@pytest.fixture
def table_simple_as_xls1():
    return fixture_simple_one_tab()


@pytest.fixture
def table_simple_as_xls2():
    return fixture_simple_one_tab()


def test_sub_operator(table_simple_as_xls1: XlsInputSelectable):
    """
    Test we can make a substraction of cells from a table selection,
    using another selection taken from said table.
    """

    two_rows = table_simple_as_xls1.excel_ref("A1:Z2")
    assert dfc.xycells_to_excel_ref(two_rows.cells) == "A1:Z2"
    assert len(two_rows.cells) == 52

    bottom_row = two_rows.excel_ref("A2:Z2")
    assert dfc.xycells_to_excel_ref(bottom_row.cells) == "A2:Z2"
    assert len(bottom_row.cells) == 26

    top_row = two_rows.excel_ref("A1:Z1")
    assert dfc.xycells_to_excel_ref(top_row.cells) == "A1:Z1"
    assert len(top_row.cells) == 26

    sub1 = two_rows - top_row
    assert len(sub1.cells) == 26

    sub2 = two_rows - bottom_row
    assert len(sub2.cells) == 26


def test_subtract_operator_raises_for_unaligned_tables(
    table_simple_as_xls1: XlsInputSelectable, table_simple_as_xls2: XlsInputSelectable
):
    """
    Test that a a suitable error is raised if we try and make a substraction of
    cells using selections taken from different tables.
    """

    with pytest.raises(UnalignedTableOperation):
        table_simple_as_xls1 - table_simple_as_xls2


def test_union_operator(table_simple_as_xls1: XlsInputSelectable):
    """
    Test we can create a union of cells from a table selection
    with another selection taken from the same table.
    """

    two_rows = table_simple_as_xls1.excel_ref("A1:Z2")
    assert dfc.xycells_to_excel_ref(two_rows.cells) == "A1:Z2"
    assert len(two_rows.cells) == 52

    bottom_row = two_rows.excel_ref("A2:Z2")
    assert dfc.xycells_to_excel_ref(bottom_row.cells) == "A2:Z2"
    assert len(bottom_row.cells) == 26

    top_row = two_rows.excel_ref("A1:Z1")
    assert dfc.xycells_to_excel_ref(top_row.cells) == "A1:Z1"
    assert len(top_row.cells) == 26

    recombined = bottom_row | top_row
    assert len(recombined.cells) == 52
    assert dfc.xycells_to_excel_ref(recombined.cells) == "A1:Z2"


def test_union_operator_raises_for_unaligned_tables(
    table_simple_as_xls1: XlsInputSelectable, table_simple_as_xls2: XlsInputSelectable
):
    """
    Test that a a suitable error is raised if we try and make a substraction of
    cells using selections taken from different tables.
    """

    with pytest.raises(UnalignedTableOperation):
        table_simple_as_xls1 | table_simple_as_xls2
