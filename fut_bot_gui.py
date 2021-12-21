import sys

# 1. Import `QApplication` and all the required widgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget


app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle('Fifa Ultimate Team')
window.setGeometry(300, 300, 1000, 1000)
window.setStyleSheet(
    "background: qlineargradient(spread: pad, x1: 0.01, y1: 0.126, x2: 0.75, y2: 0.227, stop: 0.0738636 rgba(8, 10, 23, 255), stop: 0.840909 rgba(14, 17, 38, 255))")

#
#   background-size:100% 20px;
#   background-position:0 100%;


# 4. Show your application's GUI
window.show()

# 5. Run your application's event loop (or main loop)
sys.exit(app.exec_())
