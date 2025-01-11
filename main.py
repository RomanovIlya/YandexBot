import asyncio
import sys
import threading
import os

from commands import bot, dp

import sys

from PyQt6 import uic  
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import  QTimer

loop = asyncio.new_event_loop()


def start_bot():
    asyncio.set_event_loop(loop)
    asyncio.run(dp.start_polling(bot))

def stop():
    raise ValueError

class InfMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('source/untitled.ui', self)  
        self.initUI()
        self.bot_thread = None
    
    def initUI(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.get_update)
        self.timer.start(5000)  

        self.get_update()

        self.StartButton.clicked.connect(self.start_bot)
    
    def get_update(self):
        with open("changelog.txt", "r", encoding='utf-8') as f:
            result = ""
            while True:
                line = f.readline()

                if not line:
                    break
                result = result + line.strip() + "\n"
            self.Changelog.setText(result)

    def start_bot(self):
        if self.bot_thread is None or not self.bot_thread.is_alive():
            self.bot_thread = threading.Thread(target=start_bot)
            self.bot_thread.start()

    def closeEvent(self, event):
        stop()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = InfMenu()
    ex.show()
    sys.exit(app.exec())
    