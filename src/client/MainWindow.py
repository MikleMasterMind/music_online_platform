"""Main window for app."""
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtMultimedia import QMediaPlayer
from PyQt6.QtMultimedia import QAudioOutput
from PyQt6.QtCore import QUrl
from PyQt6.QtCore import QBuffer
from PyQt6.QtCore import QIODevice
from .SockedWrapper import SockedWrapper
from .AddMusicWindow import AddMusicWindow
from . import _
import threading
import time
import os


class MainWindow(QMainWindow):
    """Main window for listening music.

    Window contains:
        Search layout:
            QLineEdit for music to search
            QLabel for status
            QPushButton to send search
        List layout:
            QListWidget to show found musics
        Player Layout:
            QLabel to show current music and pause mode
            QPushButton to start play music from begin
            QPushButton to pause and contine music
        Add Music Layout:
            QPushButton to open sudwindow for adding new music
    """

    def __init__(self, socket: SockedWrapper):
        """Initialiaze window.

        Args:
            socket: connected to server socket
        """
        super(MainWindow, self).__init__()

        self.socket = socket

        self.setWindowTitle(_("Misuc player"))
        self.setFixedSize(600, 300)

        self.input_music = QLineEdit()
        self.input_music.setPlaceholderText(_("print music title"))

        self.status_output = QLabel("")

        self.search_btn = QPushButton(_("Search"))
        self.search_btn.clicked.connect(self.search_music)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_music)
        input_layout.addWidget(self.status_output)
        input_layout.addWidget(self.search_btn)

        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        self.musics = []
        self.music_list = QListWidget()
        self.music_list.addItems(self.musics)
        self.music_list.itemClicked.connect(self.set_selected)

        self.music_buffer = QBuffer()
        self.music_buffer.open(QIODevice.OpenModeFlag.ReadWrite)

        list_layout = QHBoxLayout()
        list_layout.addWidget(self.music_list)

        self.play_btn = QPushButton(_("Play"))
        self.play_btn.clicked.connect(self.play_music)

        self.pause_btn = QPushButton(_("Pause"))
        self.pause_btn.clicked.connect(self.pause_music)

        self.music_paused = False

        self.selected_music = None
        self.selected_music_title = QLabel("")

        player_layout = QHBoxLayout()
        player_layout.addWidget(self.selected_music_title)
        player_layout.addWidget(self.play_btn)
        player_layout.addWidget(self.pause_btn)

        self.add_music_btn = QPushButton(_("Add music"))
        self.add_music_btn.clicked.connect(self.show_add_music_window)

        add_music_layout = QHBoxLayout()
        add_music_layout.addWidget(self.add_music_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(list_layout)
        main_layout.addLayout(player_layout)
        main_layout.addLayout(add_music_layout)
        main_layout.addStretch()

        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)

    def search_music(self):
        """Fun to send searc-query to server."""
        music_title = self.input_music.text()
        self.socket.sendall(f"FIND FILE {music_title}\n")
        response = self.socket.readline()
        if response == "FOUND FILE":
            self.music_list.addItem(music_title)
            self.status_output.setText(_("success"))
        else:
            self.status_output.setText(_("not success"))

    def play_music(self):
        """Fun to get music from server and start plaing."""
        if self.selected_music and not self.socket.busy():
            self.socket.sendall(f"GET FILE {self.selected_music}\n")
            response = self.socket.readline()
            if response == "FILE TRANSMIT":
                threading.Thread(target=self.receive_stream).start()
                time.sleep(0.1)
                self.player.setSourceDevice(self.music_buffer, QUrl("audio/mp3"))
                self.player.play()

    def pause_music(self):
        """Fun to pause music."""
        if not self.music_paused:
            self.music_paused = True
            self.selected_music_title.setText(f"{self.selected_music}\t{_('paused')}")
            self.player.pause()
        else:
            self.music_paused = False
            self.selected_music_title.setText(self.selected_music)
            self.player.play()

    def set_selected(self, item):
        """Fun to select music from list."""
        self.selected_music = item.text()
        self.selected_music_title.setText(self.selected_music)

    def receive_stream(self):
        """Fun read stream data from socket and write it to buffer."""
        size = int(self.socket.readline())
        chunk_size = 4096
        while size >= 0:
            chunk = self.socket.recv(chunk_size)
            self.music_buffer.write(chunk)
            chunk_size = min(chunk_size, size)
            size -= chunk_size

    def show_add_music_window(self):
        """Fun to show subwindow to add music."""
        self.add_music_window = AddMusicWindow(self)
        self.add_music_window.show()

    def add_music(self, path_to_file, title, chunk_size = 4096):
        """Fun write music from file to socket."""
        self.socket.send(f"ADD FILE {title}\n")
        with open(path_to_file, 'rb') as f:
            filesize = os.path.getsize(path_to_file)
            self.socket.send(f'{str(filesize)}\n')
            while chunk := f.read(chunk_size):
                self.socket.sendraw(chunk)
