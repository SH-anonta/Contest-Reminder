import time, sys, threading

from PyQt5.QtWidgets import QApplication

# modules of this project
from sample.gui import MainWindow
from sample.DataFetcher import ContestDataCollector

def main():
    qapp = QApplication(sys.argv)

    window= MainWindow()

    def updater():
        print('Updating...')
        window.updateTable(data_provider.getFutureContests())
        timer = threading.Timer(5, updater)
        timer.setDaemon(True)
        timer.start()


    data_provider = ContestDataCollector()
    updater()
    exit(qapp.exec_())





if __name__ == '__main__':
    main()






