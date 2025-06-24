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
import socket
from .SockedWrapper import SockedWrapper
import threading


class MainWindow(QMainWindow):
    def __init__(self, socket: SockedWrapper):
        super(MainWindow, self).__init__()

        self.socket = socket

        self.setWindowTitle("Misuc player")
        self.setFixedSize(600, 300)

        self.input_music = QLineEdit()
        self.input_music.setPlaceholderText("print music title")

        self.search_btn =QPushButton("Search")
        self.search_btn.clicked.connect(self.search_music)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_music)
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

        self.play_btn = QPushButton("Play")
        self.play_btn.clicked.connect(self.play_music)

        self.pause_btn = QPushButton("Pause")
        self.pause_btn.clicked.connect(self.pause_music)

        self.music_paused = False

        self.selected_music = None
        self.selected_music_title = QLabel("")

        player_layout = QHBoxLayout()
        player_layout.addWidget(self.selected_music_title)
        player_layout.addWidget(self.play_btn)
        player_layout.addWidget(self.pause_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addLayout(list_layout)
        main_layout.addLayout(player_layout)
        main_layout.addStretch()

        widget = QWidget()
        widget.setLayout(main_layout)

        self.setCentralWidget(widget)

    def search_music(self):
        music_title = self.input_music.text()
        self.socket.sendall(f"GET MUSIC {music_title}\n")
        response = self.socket.readline()
        if response == "FILE TRANSMIT":
            self.music_list.addItem(music_title)
            threading.Thread(target=self.receive_stream).start()
            self.selected_music = music_title
            
    def play_music(self):
        if self.selected_music:
            print(self.music_buffer.buffer())
            self.player.setSourceDevice(self.music_buffer, QUrl("audio/mp3"))
            self.player.play()

    def pause_music(self):
        if not self.music_paused:
            self.music_paused = True
            self.selected_music_title.setText(f"{self.selected_music}\tpaused")
            self.player.pause()
        else:
            self.music_paused = False
            self.selected_music_title.setText(self.selected_music)
            self.player.play()

    def set_selected(self, item):
        self.selected_music = item.text()
        self.selected_music_title.setText(self.selected_music)

    def receive_stream(self):
        size = int(self.socket.readline())
        chunk_size = 4096
        while size > 0:
            chunk = self.socket.recv(chunk_size)
            self.music_buffer.write(chunk)
            chunk_size = min(chunk_size, size)
            size -= chunk_size
    