from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSpacerItem
from PyQt6.QtWidgets import QHBoxLayout


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Misuc player")
        self.setFixedSize(1000, 800)

        self.input_music = QLineEdit()
        self.input_music.setPlaceholderText("print music title")

        self.search_btn =QPushButton("Search")
        self.search_btn.clicked.connect(self.search_music)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_music)
        input_layout.addWidget(self.search_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addStretch()

        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)


    def search_music(self):
        print(self.input_music.text())