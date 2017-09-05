import unittest, sys, time, threading, requests

from PyQt5.QtWidgets import QApplication

# Modules of this project
import sample.DataFetcher
import sample.gui
import sample.main


class MyTestCase(unittest.TestCase):

    def setUp(self):
        pass
    def tearDown(self):
        pass


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

    @unittest.skip
    def testTimers(self):
        t= threading.Timer(.5, lambda :print('xxx'))
        t.cancel()
        t.start()

    def testUpdater(self):
        qapp = QApplication(sys.argv)

        window = sample.gui.MainWindow()
        collector = sample.DataFetcher.ContestDataCollector()

        updater = sample.main.TableUpdater(10, collector, window)

        #this one milli second delay is nneded to give qwidget time to set up
        threading.Timer(.1, updater.updateNow).start()
        updater.startUpdateTimer()
        threading.Timer(1, self.helperChangeInterval, [updater]).start()
        qapp.exec_()

    def helperChangeInterval(self, updater):
        print('updated')
        updater.setUpdateInterval(3)