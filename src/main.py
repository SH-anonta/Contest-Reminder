import time, sys, threading

from PyQt5.QtWidgets import QApplication

import time

# modules of this project
from src.gui import MainWindow
from src.DataFetcher import ContestDataCollector


class TableUpdater:
    def __init__(self, update_interval, data_source, target_gui):
        """
        :param update_interval: interval between updates in seconds
        :param data_source: the ContestDataCollector from which data will be retrieved
        :param target_gui: the widget needs to be updated
        """
        self._update_interval = update_interval
        self._target = target_gui
        self._data_fetcher= data_source

        self._update_timer= threading.Timer(update_interval, self.selfUpdatingTimer)

    def selfUpdatingTimer(self):
        """
        executes the timers function and sets the timer to go off again
        :return: None
        """
        self._update_timer.cancel()
        self.updateNow()
        self._update_timer= threading.Timer(self._update_interval, self.selfUpdatingTimer)
        self._update_timer.setDaemon(True)
        self._update_timer.start()

    def updateNow(self):
        """
        updates the target without delay
        :return:
        """
        # print(time.time())
        self._target.updateTable(self._data_fetcher.getFutureContests())

    def setUpdateInterval(self, interval):
        """
        :param interval: interbetween updates
        :return: None
        This will reset the current waiting time to 0
        """
        self._update_interval = interval
        self.selfUpdatingTimer()

    def startUpdateTimer(self):
        self.selfUpdatingTimer()


def main():
    default_update_interval = 60 # in seconds
    data_provider = ContestDataCollector()
    qapp = QApplication(sys.argv)
    window= MainWindow()

    updater = TableUpdater(default_update_interval, data_provider, window)

    #This .1 second delay in updating the table gives widgets some time to setup
    # without the delay the gui seems to hang for a few second during launch
    threading.Timer(.1, updater.startUpdateTimer).start()

    exit(qapp.exec_())





if __name__ == '__main__':
    main()
