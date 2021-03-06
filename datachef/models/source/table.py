"""
Classes representing a single cell of data.
"""

from __future__ import annotations

import copy
import uuid
from pathlib import Path
from typing import List, Optional, Union

from datachef.exceptions import (
    InvalidTableSignatures,
    UnalignedTableOperation,
    UnnamedTableError,
)
from datachef.models.source.cell import BaseCell, Cell
from datachef.selection import datafuncs as dfc
from datachef.utils.decorators import dontmutate


class Table:
    """
    Represents a table of data in the form of a list of cells.
    """

    def __init__(self, cells: Optional[List[Cell]] = None):
        self.cells = cells
        self._signature = str(uuid.uuid4())

    def add_cell(self, cell: Cell):
        if not self.cells:
            self.cells = []
        self.cells.append(cell)


class LiveTable:
    """
    A "live" table represents two things:

    1.) "pristine" - The pristine table as pulled from the source.
    2.) "filtered" - The current subset of cells (up to all) as selected from the pristine table.

    Keeping track of the pristine cell selection (the initial table) allows us to
    extend a Table of cells (.filtered) via comparing it with the pristine Table
    (.pristine). This enables the extension of a cell selection as well as the
    filtering down of one.
    """

    def __init__(
        self, pristine: Table, filtered: Table, _name: str = None, source: str = None
    ):
        self.pristine: Table = pristine
        self.filtered: Table = filtered
        self._name: Optional[str] = _name
        self.source: Union[Path, str] = source

        # An optional label used when working with previews
        self._label: Optional[str] = None

        self.validate()

    @property
    def name(self):
        """
        Return a name if we have a name, else raises
        """
        if self._name:
            return self._name
        else:
            raise UnnamedTableError()

    @property
    def cells(self) -> List[Cell]:
        """
        Accessor for currently selected cells from the
        currently selected table
        """
        return self.filtered.cells

    @cells.setter
    def cells(self, cells: List[Cell]):
        """
        Setter for the cells property
        """
        self.filtered.cells = cells

    @property
    def pcells(self) -> List[BaseCell]:
        """
        Accessor for the pristine cells from the
        currently selected table
        """
        return self.pristine.cells

    def selections_made(self) -> bool:
        """
        Have any selections been made
        """
        return len(self.pristine.cells) != len(self.filtered.cells)

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def title(self) -> str:
        """
        Alternate call to name for databaker backwards compatibility
        """
        return self.name

    def validate(self):
        """
        Confirm class is validly constructed.
        """
        if self.pristine._signature != self.filtered._signature:
            raise InvalidTableSignatures()

    @staticmethod
    def from_table(
        table: Table, source: Union[Path, str], name: str = None
    ) -> LiveTable:
        """
        Given a table and optional it's name, create a livetable.
        """
        return LiveTable(
            table,
            copy.deepcopy(table),
            _name=name,
            source=source,
        )

    @property
    def signature(self):
        """
        A uuid that uniquely identifies a parsed input source table
        """
        return self.filtered._signature

    @dontmutate
    def __sub__(self, other_input: LiveTable):
        """
        Implements "-" operator, subtraction

        Allows subtraction of one selection from the same distinct
        and currently selected table from another. Provided they
        are derrived from the same initial BaseInput.
        """

        if self.signature != other_input.signature:
            raise UnalignedTableOperation()

        self.cells = dfc.cells_not_in(self.cells, other_input.cells)
        return self

    @dontmutate
    def __or__(self, other_input: LiveTable):
        """
        Implements "|" operator, union.

        Allows the union of one selection from the same distinct
        and currently selected table with another. Provided they
        are derrived from the same initial BaseInput.
        """
        if self.signature != other_input.signature:
            raise UnalignedTableOperation()

        new_cells = dfc.cells_not_in(other_input.cells, self.cells)
        self.cells = self.cells + new_cells
        return self

    def __iter__(self):
        """
        We're not really iterating table objects, we're just moving the
        pointer to the selected table then returning the updated self
        """
        for cell in self.cells:
            yield cell
