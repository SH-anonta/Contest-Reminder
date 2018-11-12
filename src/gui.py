from PyQt5.QtWidgets import QWidget, QMainWindow
from PyQt5.QtWidgets import  QTableWidget,QTableWidgetItem
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtGui import QIcon

import time

class GUIResources:

    @classmethod
    def getTitleBarIcon(self):
        return '../resources/titlebar_icon.png'

    @classmethod
    def getTitleBarText(self):
        return 'Contest reminder'


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()

    # Construction helpers

    def setupUI(self):
        "setup the gui for this window"
        self.main_panel= MainPanel()

        self.setCentralWidget(self.main_panel)
        self.setWindowTitle(GUIResources.getTitleBarText())
        self.setFixedSize(700, 400)
        self.move(750, 100)

        window_icon= QIcon(GUIResources.getTitleBarIcon())
        self.setWindowIcon(window_icon)

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
        table.setHorizontalHeaderLabels(['Title', 'Judge','Status', 'Start Time', 'End Time'])
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setColumnWidth(0, 220)
        table.setColumnWidth(1, 80)
        table.setColumnWidth(2, 70)
        table.setColumnWidth(3, 140)
        table.setColumnWidth(4, 140)
        return table


    TIME_FORMAT= '%d %b %Y at %I:%M %p'

    def updateTable(self, contests):
        self.contests_table.setRowCount(0)


        for row, contest in enumerate(contests):
            self.contests_table.insertRow(row)
            self.contests_table.setItem(row, 0, QTableWidgetItem(contest.title))
            self.contests_table.setItem(row, 1, QTableWidgetItem(contest.judge))
            self.contests_table.setItem(row, 2, QTableWidgetItem(contest.status))
            self.contests_table.setItem(row, 3, QTableWidgetItem(self.secondsToStringTime(contest.start_time)))
            self.contests_table.setItem(row, 4, QTableWidgetItem(self.secondsToStringTime(contest.end_time)))


    # helper methods
    def secondsToStringTime(self, time_seconds):
        return time.strftime(self.TIME_FORMAT, time.localtime(time_seconds))
