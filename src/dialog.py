"""The window where the student checks the decks that take part in the final review."""

from __future__ import annotations

from collections.abc import Sequence

from aqt.qt import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    Qt,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from .deck_choice import chosen_names, locked_names


class DeckWindow(QDialog):
    """A deck tree with a checkbox on each deck; a checked deck locks its subdecks.

    Attributes:
        chosen: The decks to save; set from the checkboxes when OK is pressed.
    """

    def __init__(self, parent: QWidget, names: Sequence[str], chosen: Sequence[str]) -> None:
        """Build the tree with the `chosen` decks checked.

        Args:
            parent: The window this one sits over.
            names: Every normal deck's full name.
            chosen: The decks in the settings; names not in `names` are ignored.
        """
        super().__init__(parent)
        self.setWindowTitle("Final Review decks")
        self.chosen: list[str] = list(chosen)
        self._names = list(names)
        self._checked = set(chosen) & set(self._names)
        self._items: dict[str, QTreeWidgetItem] = {}
        self._tree = QTreeWidget()
        self._tree.setHeaderHidden(True)
        for name in sorted(self._names):
            parent_name, _, leaf = name.rpartition("::")
            parent_item = self._items.get(parent_name)
            if parent_item is None:
                item = QTreeWidgetItem(self._tree)
            else:
                item = QTreeWidgetItem(parent_item)
            item.setText(0, leaf)
            item.setData(0, Qt.ItemDataRole.UserRole, name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            self._items[name] = item
        self._tree.expandAll()
        self._refresh()
        self._tree.itemChanged.connect(self._on_item_changed)
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("A checked deck brings its subdecks with it."))
        layout.addWidget(self._tree)
        layout.addWidget(buttons)
        self.resize(400, 500)

    def _refresh(self) -> None:
        """Show each deck checked or not, and lock the subdecks of a checked deck."""
        locked = locked_names(self._names, self._checked)
        self._tree.blockSignals(True)
        for name, item in self._items.items():
            on = name in self._checked or name in locked
            item.setCheckState(0, Qt.CheckState.Checked if on else Qt.CheckState.Unchecked)
            item.setDisabled(name in locked)
        self._tree.blockSignals(False)

    def _on_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        """Record the student's click on a checkbox and redraw the locks."""
        name = item.data(0, Qt.ItemDataRole.UserRole)
        if item.checkState(0) == Qt.CheckState.Checked:
            self._checked.add(name)
        else:
            self._checked.discard(name)
        self._refresh()

    def _save(self) -> None:
        """Keep the decks to save and close the window as accepted."""
        self.chosen = chosen_names(self._names, self._checked)
        self.accept()
