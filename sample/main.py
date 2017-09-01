import time, sys, requests
from PyQt5.QtWidgets import QApplication

# modules of this project
from sample.gui import MainWindow


def main():
    qapp = QApplication(sys.argv)

    window= MainWindow()
    exit(qapp.exec_())

if __name__ == '__main__':
    main()






