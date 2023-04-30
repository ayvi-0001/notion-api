# MIT License

# Copyright (c) 2023 ayvi-0001

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import annotations

from typing import Any, Collection, MutableMapping, Optional, Sequence

from notion.api.blockmixin import _TokenBlockMixin
from notion.api.client import _NLOG
from notion.properties.blocktypes import BlockChildren, TableRowBlockType
from notion.properties.richtext import RichText

__all__: Sequence[str] = ("TableBlock", "CELLS_ARRAY")


CELLS_ARRAY = Sequence[list[dict[str, Collection[str]]]]
""" An array of cell contents in horizontal display order. Each cell is an array of rich text objects. """


class TableBlock(_TokenBlockMixin):
    """
    Note that the number of columns in a table can only be set when the table is first created.
    Calls to the Update block endpoint to update table_width fail.
    See examples in repo `examples/block_extensions.md` for more details.

    Table:      https://developers.notion.com/reference/block#table
    Table Rows: https://developers.notion.com/reference/block#table-rows
    """

    def __init__(
        self,
        id: str,
        /,
        *,
        token: Optional[str] = None,
    ) -> None:
        super().__init__(id, token=token)
        self.logger = _NLOG.getChild(self.__repr__())

        if self.type != "table":
            raise TypeError(
                f"Block type must be 'table', not '{self.type}' for TableBlock."
            )

        self.table_width = int(self._block["table"]["table_width"])
        self.rows = self.retrieve_children().get("results", [])

    def get_row(self, row_index: int) -> list[str]:
        """:returns: A list of cell contents in horizontal display order."""
        table_row = self.rows[row_index]["table_row"]

        row: list[str] = []
        for cell in table_row["cells"]:
            try:
                row.append(cell[0]["text"]["content"])
            except IndexError:
                row.append("")
        return row

    def get_cell(self, row_index: int, column_index: int) -> str:
        """:returns: The cell content at the given row and cell index."""
        return self.get_row(row_index)[column_index]

    def get_table(self) -> list[Sequence[str]]:
        """:returns: A list of rows in the table."""
        table: list[Sequence[str]] = []
        for index, row in enumerate(self.rows):
            table.append(self.get_row(index))
        return table

    def edit_cell(self, row_index: int, column_index: int, *, value: str) -> None:
        """Edits the cell content at the given row and cell index."""
        table_row = self.rows[row_index]
        table_row_id = table_row["id"]
        table_row["table_row"]["cells"][column_index] = [RichText(value)]

        self._patch(self._block_endpoint(table_row_id), payload=table_row)

    def append_row(self, values_array: Optional[list[str]] = None) -> None:
        """:raises: NotionValidationError
        if the length of values_array is not equal to the number of cells in table row.
        """
        if not values_array:
            cells: CELLS_ARRAY = [[] for _ in range(self.table_width)]
            row = [TableRowBlockType(cells)]
            self._patch(
                self._block_endpoint(self.id, children=True),
                payload=BlockChildren(row),
            )

        else:
            cells: CELLS_ARRAY = [[RichText(value)] for value in values_array]
            row = [TableRowBlockType(cells)]
            self._patch(
                self._block_endpoint(self.id, children=True),
                payload=BlockChildren(row),
            )

    def overwrite_row(self, row_index: int, values_array: list[str]) -> None:
        table_row = self.rows[row_index]
        table_row_id = table_row["id"]
        table_row["table_row"]["cells"] = [[RichText(value)] for value in values_array]

        self._patch(self._block_endpoint(table_row_id), payload=table_row)

    def delete_row(self, row_index: int) -> None:
        table_row = self.rows[row_index]
        table_row_id = table_row["id"]
        self._delete(self._block_endpoint(table_row_id))

    def has_column_header(self, value: bool) -> None:
        table = self._block
        table["table"]["has_column_header"] = value
        table["table"].pop("table_width")
        self._patch(self._block_endpoint(self.id), payload=table)

    def has_row_header(self, value: bool) -> None:
        table = self._block
        table["table"]["has_row_header"] = value
        table["table"].pop("table_width")
        self._patch(self._block_endpoint(self.id), payload=table)

    def retrieve_children(self) -> MutableMapping[str, Any]:
        return self._get(self._block_endpoint(self.id, children=True))
