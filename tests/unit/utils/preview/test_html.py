import os
import shutil
import uuid
from pathlib import Path
from typing import Optional

import pytest

from datachef.models.source.cell import Cell
from datachef.models.source.table import LiveTable, Table
from datachef.selection.selectable import Selectable
from datachef.utils.preview.previewer import label, preview
from datachef.utils.preview.previewers.html import HtmlPreview
from tests.fixtures import path_to_fixture
from tests.fixtures.preconfigured import fixture_simple_small_one_tab


@pytest.fixture
def selectable_simple_small1():
    return fixture_simple_small_one_tab()


def _assert_compare_html(
    fixture: Path, *selections, end: Optional[str] = None, start: Optional[str] = None
):
    """
    Helper to compare html as output but datachef with
    a html fixture
    """

    # This type cast is usually handled by the preview() wrapper
    selections = list(selections)

    with open(fixture) as f:
        html = HtmlPreview()._make_preview_as_html_str(selections, start=start, end=end)
        preview = f.read()
        if preview != html:

            uid = str(uuid.uuid4())
            with open(f"{uid}.html", "w") as f:
                f.write(html)

            raise AssertionError(
                "Test preview does not match expected.\n"
                f"Fixture of expected output: {fixture}"
                f"Output generated by test is {uid}.html"
            )


def test_standard_small_preview_two_selections(selectable_simple_small1: Selectable):
    """
    Test that we can generate the expected preview for a preview of
    two selections.
    -------------
    from datachef import acquire, preview

    table = acquire('./tests/fixtures/csv/simple-small.csv')
    s1 = table.excel_ref('A4:C10')
    s2 = table.excel_ref('F8:G12')
    preview(s1, s2, path="./tests/fixtures/preview/simple-selections1.html")
    """
    s1 = selectable_simple_small1.excel_ref("A4:C10")
    s2 = selectable_simple_small1.excel_ref("F8:G12")
    fixture = path_to_fixture("preview", "simple-selections1.html").resolve()
    _assert_compare_html(fixture, s1, s2)


def test_standard_small_preview_two_selections_start_and_end(
    selectable_simple_small1: Selectable,
):
    """
    Test that we can generate the expected preview for a preview of
    two selections using a specified start and end point.
    -------------
    from datachef import acquire, preview

    table = acquire('./tests/fixtures/csv/simple-small.csv')
    s1 = table.excel_ref('B4:C10')
    s2 = table.excel_ref('E6:G8')
    preview(s1, s2, start='B3', end='H12', path="./tests/fixtures/preview/simple-small-start-and-end.html")
    """
    s1 = selectable_simple_small1.excel_ref("B4:C10")
    s2 = selectable_simple_small1.excel_ref("E6:G8")
    fixture = path_to_fixture("preview", "simple-small-start-and-end.html").resolve()
    _assert_compare_html(fixture, s1, s2, start="B3", end="H12")


def test_standard_small_preview_named_selections(selectable_simple_small1: Selectable):
    """
    Test that we can generate the expected preview for a preview of
    three selections and using custom selection labels.
    -------------
    from datachef import acquire, preview, label

    table = acquire('./tests/fixtures/csv/simple-small.csv')
    s1 = table.excel_ref('B10:F20')
    s2 = table.excel_ref('C3:H4')
    s3 = table.excel_ref('K6:K9')
    preview(label(s1, "Block near the bottom"), label(s2, "Some near the top"), label(s3, 'Down the side'), path="./tests/fixtures/preview/simple-small-named-selections.html")
    """
    s1 = selectable_simple_small1.excel_ref("B10:F20")
    s2 = selectable_simple_small1.excel_ref("C3:H4")
    s3 = selectable_simple_small1.excel_ref("K6:K9")
    fixture = path_to_fixture("preview", "simple-small-named-selections.html").resolve()
    _assert_compare_html(
        fixture,
        label(s1, "Block near the bottom"),
        label(s2, "Some near the top"),
        label(s3, "Down the side"),
    )


def test_standard_small_preview_overlap_warnings(selectable_simple_small1: Selectable):
    """
    Test that we can generate the expected preview for a preview of
    two selections where the cell selections overlap.
    -------------
    from datachef import acquire, preview

    table = acquire('./tests/fixtures/csv/simple-small.csv')
    s1 = table.excel_ref('B4:C6')
    s2 = table.excel_ref('C5:E7')
    preview(s1, s2, start='B3', end='G8', path="./tests/fixtures/preview/simple-small-overlap-warning.html")
    """
    s1 = selectable_simple_small1.excel_ref("B4:C6")
    s2 = selectable_simple_small1.excel_ref("C5:E7")
    fixture = path_to_fixture("preview", "simple-small-overlap-warning.html").resolve()
    _assert_compare_html(fixture, s1, s2, start="B3", end="G8")


def test_boundary_to_selection(selectable_simple_small1: Selectable):
    """
    Test that we can generate the expected preview where we want the
    boundary of the preview to be dictated by the selected cells.
    -------------
    from datachef import acquire, preview

    table = acquire('./tests/fixtures/csv/simple-small.csv')
    s1 = table.excel_ref('B7:G10')
    s2 = table.excel_ref('F14')
    preview(s1, s2, start='selection', end='selection', path="./tests/fixtures/preview/boundary-to-selection.html")
    """
    s1 = selectable_simple_small1.excel_ref("B7:G10")
    s2 = selectable_simple_small1.excel_ref("F14")
    fixture = path_to_fixture("preview", "boundary-to-selection.html").resolve()
    _assert_compare_html(fixture, s1, s2, start="selection", end="selection")


def test_preview_with_a_table_name():
    """
    Test that we can generate a named table such that its name is
    included in the preview.
    """
    from datachef.models.source.cell import Cell
    from datachef.models.source.table import LiveTable, Table
    from datachef.selection.selectable import Selectable

    t = Table([Cell(0, 0, value="A1"), Cell(0, 1, value="B1")])
    s = Selectable(t, t, _name="Example Table")

    fixture = path_to_fixture("preview", "tiny-with-table-name.html")
    _assert_compare_html(fixture, s)


def test_html_to_path(selectable_simple_small1: Selectable):
    """
    Confirm that we can write previews to a specified path
    """
    this_dir = Path(__file__).parent
    tmp_file_path = Path(this_dir / f"{str(uuid.uuid4())}.html")
    preview(selectable_simple_small1, path=tmp_file_path)
    assert tmp_file_path.exists()
    os.remove(tmp_file_path)
