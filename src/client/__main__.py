from PyQt6.QtWidgets import QApplication
from .MainWindow import MainWindow
from .SockedWrapper import SockedWrapper

    
if __name__ == "__main__":
    app = QApplication([])
    socket = SockedWrapper(host='0.0.0.0', port=1337)
    w = MainWindow(socket)
    w.show()
    app.exec()
