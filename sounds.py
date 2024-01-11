from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import json
class Sounds:
    def __init__(self):
        self.media_player = QMediaPlayer()

        self.url1 = QUrl.fromLocalFile("sounds/dice_rolling.mp3")
        self.url2 = QUrl.fromLocalFile("sounds/winner.mp3")
        self.url3 = QUrl.fromLocalFile("sounds/click_button.mp3")

        with open("JSON/settings.json", "r") as file:
            loaded_settings = json.load(file)
        volume = loaded_settings.get("sound_volume", 1)
        self.media_player.setVolume(volume)
    def dice_rolling(self):
        content = QMediaContent(self.url1)
        self.media_player.setMedia(content)
        self.media_player.play()
    def winner(self):
        content = QMediaContent(self.url2)
        self.media_player.setMedia(content)
        self.media_player.play()
    def click_button(self):
        content = QMediaContent(self.url3)
        self.media_player.setMedia(content)
        self.media_player.play()



