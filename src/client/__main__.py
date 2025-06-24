from PyQt6.QtWidgets import QApplication
from .MainWindow import MainWindow

    
if __name__ == "__main__":
    app = QApplication([])
    w = MainWindow()
    w.show()
    app.exec()
