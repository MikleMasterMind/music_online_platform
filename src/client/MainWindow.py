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


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

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
        file_path = "./test_music/" + "music.mp3"
        self.musics = {"music.mp3" : QUrl.fromLocalFile(file_path)}
        self.music_list.clear()
        self.music_list.addItems(self.musics)

    def play_music(self):
        if self.selected_music:
            self.player.setSource(self.musics[self.selected_music])
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
