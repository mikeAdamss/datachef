"""
.. include:: ./README.md
"""
from .common import (
    assert_quadrilaterals,
    cell_is_not_within,
    cell_is_within,
    cells_not_in,
    cells_on_x_index,
    cells_on_y_index,
    ensure_human_read_order,
    exactly_matched_xy_cells,
    exactly_matching_xy_cell,
    get_outlier_indicies,
    matching_xy_cells,
    maximum_x_offset,
    maximum_y_offset,
    minimum_x_offset,
    minimum_y_offset,
    specific_cell_from_xy,
)
from .excel import (
    any_excel_ref_as_wanted_basecells,
    assert_excel_ref_within_cells,
    multi_excel_ref_to_basecells,
    single_excel_ref_to_basecell,
    xycell_to_excel_ref,
    xycells_to_excel_ref,
)