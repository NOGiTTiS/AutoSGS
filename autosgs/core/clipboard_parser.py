"""
Clipboard Parser module for AutoSGS.
Parses Tab-Separated Values (TSV) from Excel or Google Sheets into structured ScoreMatrix.
"""

from dataclasses import dataclass, field
from typing import List, Optional
import pyperclip


@dataclass
class ScoreMatrix:
    """Represents a 2D matrix of scores parsed from clipboard."""
    total_rows: int = 0
    total_columns: int = 0
    total_cells: int = 0
    empty_cells_count: int = 0
    rows: List[List[str]] = field(default_factory=list)
    raw_text: str = ""

    @property
    def is_empty(self) -> bool:
        """Returns True if there is no data in matrix."""
        return self.total_rows == 0 or self.total_columns == 0

    def get_cell(self, row: int, col: int) -> str:
        """Gets cell value safely, returns empty string if out of bounds."""
        if 0 <= row < self.total_rows and 0 <= col < self.total_columns:
            return self.rows[row][col]
        return ""

    def summary(self) -> str:
        """Human-readable summary of the matrix."""
        if self.is_empty:
            return "ไม่พบข้อมูลในคลิปบอร์ด"
        return f"{self.total_rows} แถว × {self.total_columns} คอลัมน์ (รวม {self.total_cells} ช่อง, ว่าง {self.empty_cells_count} ช่อง)"


def get_clipboard_text() -> str:
    """
    Safely retrieves text content from the system clipboard.
    Returns empty string if clipboard is empty or does not contain text.
    """
    try:
        content = pyperclip.paste()
        return content if content is not None else ""
    except Exception:
        return ""


def parse_tsv(text: Optional[str]) -> ScoreMatrix:
    """
    Parses TSV (Tab-Separated Values) text into a ScoreMatrix.
    Handles:
    - Trailing newlines from Excel/Sheets copy
    - Variable column counts per line by normalizing to max columns
    - Stripping whitespace around individual cell values
    - Empty cell detection
    """
    if not text or not text.strip():
        return ScoreMatrix(raw_text=text or "")

    # Split lines, handling CRLF and LF
    lines = [line for line in text.splitlines()]

    # Filter out empty trailing lines often appended by Excel
    while lines and not lines[-1].strip():
        lines.pop()

    if not lines:
        return ScoreMatrix(raw_text=text)

    # Split each line by tab
    raw_rows: List[List[str]] = []
    max_cols = 0

    for line in lines:
        # If line has no tabs, it might still be a single column cell or row
        cells = [c.strip() for c in line.split("\t")]
        if len(cells) > max_cols:
            max_cols = len(cells)
        raw_rows.append(cells)

    if max_cols == 0:
        return ScoreMatrix(raw_text=text)

    # Normalize all rows to max_cols so matrix is rectangular
    normalized_rows: List[List[str]] = []
    empty_cells = 0

    for row in raw_rows:
        if len(row) < max_cols:
            row.extend([""] * (max_cols - len(row)))
        normalized_rows.append(row)
        for cell in row:
            if cell == "":
                empty_cells += 1

    total_rows = len(normalized_rows)
    total_cells = total_rows * max_cols

    return ScoreMatrix(
        total_rows=total_rows,
        total_columns=max_cols,
        total_cells=total_cells,
        empty_cells_count=empty_cells,
        rows=normalized_rows,
        raw_text=text,
    )


def load_matrix_from_clipboard() -> ScoreMatrix:
    """Convenience function to fetch clipboard and parse into ScoreMatrix."""
    text = get_clipboard_text()
    return parse_tsv(text)
