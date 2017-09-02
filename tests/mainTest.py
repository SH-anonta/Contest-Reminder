import unittest, sys, time, threading, requests

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QTableView
from PyQt5.QtWidgets import QGridLayout, QVBoxLayout
from PyQt5.QtWidgets import QAbstractItemView

# Modules of this project
import sample.DataFetcher
import sample.gui

class TableTest(QWidget):
    """
    Working prototype for table vi
    """
    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupTable(self):
        table = QTableWidget(5, 3)
        table.setHorizontalHeaderLabels(['Title','Time','Duration'])

        # disable table editing
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)


        table.setItem(0,0, QTableWidgetItem('a'))
        table.setItem(0,1, QTableWidgetItem('x'))

        table.setItem(1,0, QTableWidgetItem('b'))
        table.setItem(1,1, QTableWidgetItem('y'))

        table.setItem(2,0, QTableWidgetItem('c'))
        table.setItem(2,1, QTableWidgetItem('z'))

        table.setSortingEnabled(True)
        return table

    def setupUI(self):
        self.setGeometry(500,500,500,500)
        self.show()

        vlayout= QVBoxLayout(self)

        vlayout.addWidget(self.setupTable() , 1)

        self.setLayout(vlayout)



class MyTestCase(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    @unittest.skip
    def testQTableWidget(self):
        qapp = QApplication(sys.argv)

        window = TableTest()
        qapp.exec_()

    @unittest.skip
    def testMainGUI(self):
        cf = sample.DataFetcher.CodeForcesDataFetcher()
        cont = cf.getFutureContests()

        qapp = QApplication(sys.argv)

        window = sample.gui.MainWindow()
        window.show()


        def updateTable():
            st= time.time()
            window.updateTable(cont)
            print(time.time() - st)


            timer = threading.Timer(5, function=updateTable)
            timer.setDaemon(True)
            timer.start()

        updateTable()

        qapp.exec_()

class ModleTesters(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass

    @unittest.skip
    def testFetchers(self):
        cf = sample.DataFetcher.CodeForcesDataFetcher()
        cont = cf.getFutureContests()

        for x in cont:
            print(x)

    def testTopCoderFetcher(self):
        with requests.session() as s:
            s.get('http://api.topcoder.com/v2/validation/sso')
            print(s.cookies)
            m = 'http://api.topcoder.com/v2/data/srm/contests'

            # headers = {'user-agent': 'Mozilla/5.0'}

            resp= s.get(m)
            self.assertEqual(resp.status_code, requests.codes['ok'])
            print('code: ', resp.status_code)
            j= resp.json()
            print(j)

