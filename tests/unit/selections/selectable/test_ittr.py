import pytest

from datachef.models.source.cell import Cell
from datachef.selection.selectable import Selectable
from tests.fixtures import fixture_simple_one_tab


@pytest.fixture
def selectable_simple1():
    return fixture_simple_one_tab()


def test_conform_selection_iteration(selectable_simple1: Selectable):
    """
    Confirm that selection iterations works as expected
    """

    for cell in selectable_simple1:
        assert isinstance(cell, Cell)
