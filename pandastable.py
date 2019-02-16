import pandas as pd

from PyQt5.QtCore import QAbstractTableModel, QTimer, QVariant
from PyQt5.QtCore import Qt


class PandasTable(QAbstractTableModel):
    # TODO: update table when data changes
    def __init__(self, df=pd.DataFrame(), parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.df = df

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.updateTable)
        # self.timer.start(500)

    def rowCount(self, parent=None):
        return self.df.shape[0]

    def columnCount(self, parent=None):
        return self.df.shape[1]

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:
            return self.df.columns[section]
        elif orientation == Qt.Vertical:
            return self.df.index.values[section]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self.df.to_numpy()[index.row()][index.column()])
        return QVariant()

    @pyqtSlot("updateTable")
    def updateTable(self):
        nrows, ncols = self.df.shape
        for i in range(nrows):
            for j in range(ncols):
                self.dataChanged.emit(i, j)

    # def setData(self, index: QModelIndex, value: typing.Any, role: int = ...):
    #     return

if __name__ == "__main__":
    columns = ["Drawpile", "Hand", "In play", "Discardpile", "Gesamt"]
    emptydf = pandas.DataFrame(columns=columns)
    print(emptydf.columns, type(emptydf.columns))

