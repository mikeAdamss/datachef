from os import linesep
import pytest

from pivoter.exceptions import UnnamedTableError
from pivoter.models.source.cell import Cell
from pivoter.models.source.table import LiveTable
from pivoter.selection.base import Selectable
from helpers import single_table_test_input


@pytest.fixture
def two_cell_table_A1A2():
    return single_table_test_input(
        [Cell(x=0, y=0, value="foo"), Cell(x=0, y=0, value="bar")]
    )


def test_simple_xy_str(two_cell_table_A1A2: Selectable):
    """
    Test the cells that make up a table can be displayed as
    simple string of the x,y and value attributes.
    """

    expected_str_lines = ["x:0, y:0, value = foo", "x:0, y:0, value = bar"]
    expected_len = len(expected_str_lines)

    got_str_lines = two_cell_table_A1A2.selected_table.filtered._as_xy_str().split(
        linesep
    )
    got_len = len(got_str_lines)

    assert (
        got_len == expected_len
    ), f"Expected {expected_len} line for outputs, got {got_len}"

    for got_line in got_str_lines:
        assert (
            got_line in expected_str_lines
        ), f"""
            Expected line {got_line} not found in:
            {(linesep).join(expected_str_lines)}
            """


def test_livetable_name_setter_and_getter(two_cell_table_A1A2: Selectable):
    """
    Test we can both set and retreive the name property as defined
    on the LiveTable class
    """

    ltable: LiveTable = two_cell_table_A1A2.selected_table
    ltable.name = "foo"
    assert ltable.name == "foo"


def test_livetable_name_getter_unnamed_table_err(two_cell_table_A1A2: Selectable):
    """
    Test the expected error is raised at the LiveTable class level if
    we try and access an unset name property.
    """

    ltable: LiveTable = two_cell_table_A1A2.selected_table
    with pytest.raises(UnnamedTableError):
        ltable.name

if __name__ == "__main__":
    pytest()