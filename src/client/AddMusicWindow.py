"""Sub window for adding new music to server db."""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QVBoxLayout
from . import _
import os


class AddMusicWindow(QWidget):
    """Sub window for adding new music to server db.

    Window contains:
            2 QLineEdit feilds for music path and music title,
            1 QLabel for status,
            1 QPushButton to do action
    """

    def __init__(self, parentWindow):
        """Initialize window.

        Args:
            parenwWindow: window wich contains this window
        """
        super().__init__()

        self.parentWindow = parentWindow

        self.setWindowTitle(_("Add Music"))
        self.setFixedSize(300, 200)

        self.input_path = QLineEdit()
        self.input_path.setPlaceholderText(_("print path to music file"))

        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText(_("print music title"))

        self.output_lbl = QLabel()

        self.add_btn = QPushButton(_("Add"))
        self.add_btn.clicked.connect(self.add_music)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.input_path)
        main_layout.addWidget(self.input_title)
        main_layout.addWidget(self.output_lbl)
        main_layout.addWidget(self.add_btn)

        self.setLayout(main_layout)

    def add_music(self):
        """Fun send from user input to server."""
        if not os.path.exists(self.input_path.text()):
            self.output_lbl.setText(_("File not exist"))
        else:
            self.parentWindow.add_music(self.input_path.text(), self.input_title.text())
            self.output_lbl.setText(_("File send to server"))
