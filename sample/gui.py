from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtWidgets import  QTableWidget,QTableWidgetItem
from PyQt5.QtWidgets import QLabel

from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from PyQt5.QtWidgets import QAbstractItemView

import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    # Construction helpers

    def setupUI(self):
        "setup the gui for this window"
        self.main_panel= MainPanel()

        self.setCentralWidget(self.main_panel)
        self.setGeometry(800, 100, 700, 400)
        # self.statusBar().setSizeGripEnabled(False)
        self.setFixedSize(700, 400)
        self.show()

    def updateTable(self, contests):
        self.main_panel.updateTable(contests)
    # setters and getters

class MainPanel(QWidget):

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.contests_table = self.setupTable()
        grid = QGridLayout()

        grid.addWidget(self.contests_table, 0,0, 1, 1)
        # grid.addWidget(QLabel('This is a text'))

        self.setLayout(grid)
        self.show()

    def setupTable(self):
        table = QTableWidget(0, 5)
        table.setHorizontalHeaderLabels(['Title', 'Judge','Status', 'Start Time', 'Duration'])
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setColumnWidth(0, 300)
        table.setColumnWidth(1, 80)
        table.setColumnWidth(2, 80)
        table.setColumnWidth(3, 120)
        table.setColumnWidth(4, 80)
        return table


    def updateTable(self, contests):
        self.contests_table.setRowCount(0)

        self.time_format= '%d %b at %I:%M %p'

        for row, contest in enumerate(contests):
            self.contests_table.insertRow(row)
            self.contests_table.setItem(row, 0, QTableWidgetItem(contest.title))
            self.contests_table.setItem(row, 1, QTableWidgetItem(contest.judge))
            self.contests_table.setItem(row, 2, QTableWidgetItem(contest.status))
            self.contests_table.setItem(row, 3, QTableWidgetItem(time.strftime(self.time_format, time.localtime(contest.time))))

            self.contests_table.setItem(row, 4, QTableWidgetItem(time.strftime('%d:%H:%M', time.gmtime(contest.duration))))
