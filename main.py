import asyncio
import sys
import time
import threading

from commands import bot, dp

import sys

from PyQt6 import uic  
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QThread, QTimer


class BotThread(QThread):
    def __init__(self):
        super().__init__()
        self.running = False 

    def run(self):
        self.thread = threading.Thread(target=self.start_bot)
        self.thread.start()
    
    def start_bot(self):
        asyncio.run(dp.start_polling(bot))

class InfMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('source/untitled.ui', self)  
        self.isrun = False
        self.initUI()
        self.Bot = BotThread()
    
    def initUI(self):
        self.StartButton.clicked.connect(self.run)
        QTimer.singleShot(10, self.get_update())
    
    def run(self):
        if not self.isrun:
            self.Bot.run()
            self.isrun = True
    
    def get_update(self):
        with open("changelog.txt", "r", encoding='utf-8') as f:
            result = ""
            while True:
                line = f.readline()

                if not line:
                    break
                result = result + line.strip() + "\n"
            self.Changelog.setText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InfMenu()
    ex.show()
    sys.exit(app.exec())
