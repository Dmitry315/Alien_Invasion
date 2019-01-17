from main import *
from tutorial import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from sys import argv, exit


class Window(QMainWindow):
    is_settings = 0
    widget = None

    def __init__(self):
        Window.widget = self
        super().__init__()
        uic.loadUi('launcher.ui', self)
        self.play.clicked.connect(self.btn_pressed)
        self.tutorial.clicked.connect(self.btn_pressed)
        self.settings.clicked.connect(self.btn_pressed)
        self.leader_board.clicked.connect(self.btn_pressed)
        self.exit_game.clicked.connect(exit)
        self.pixmap = QPixmap('images/main_menu.png')
        self.img.setPixmap(self.pixmap)
        self.img.resize(self.img.sizeHint())

    def btn_pressed(self):
        x = self.sender().text()
        if x == 'Играть':
            self.hide()
            main()
            sleep(0.5)
            self.show()
        elif x == 'Обучение':
            self.hide()
            tutorial()
            sleep(0.5)
            self.show()
        elif x == 'Настройки' and not Window.is_settings:
            Settings.show_widget()
            Window.is_settings = 0
        elif x == 'Таблица рекордов':
            try:
                LeaderBoard.show_widget()
            except Exception as err:
                print(err)


class Settings(QDialog):
    widget = None

    def __init__(self):
        Settings.widget = self
        super().__init__()
        uic.loadUi('settings.ui', self)
        self.apply.clicked.connect(self.apply_settings)
        self.cancel.clicked.connect(self.cancel_settings)

    def apply_settings(self):
        fps1 = self.fps.value()
        diff = self.difficulty.currentIndex()
        with open('game_settings.txt', encoding='utf-8', mode='w') as f:
            f.write('game_speed: ' + str(fps1) + '\n')
            f.write('difficulty: ' + str(diff))
        self.hide()

    def cancel_settings(self):
        self.hide()

    @classmethod
    def show_widget(cls):
        cls.widget.show()


class LeaderBoard(QDialog):
    widget = None

    def __init__(self):
        LeaderBoard.widget = self
        super().__init__()
        uic.loadUi('leader_board.ui', self)

    def update_board(self):
        with open('score.txt', mode='r', encoding='utf-8') as f:
            lines = f.readlines()
        self.easy.setText(lines[0][:-1])
        self.medium.setText(lines[1][:-1])
        self.hard.setText(lines[2][:-1])

    @classmethod
    def show_widget(cls):
        cls.widget.update_board()
        cls.widget.show()


if __name__ == '__main__':
    app = QApplication(argv)
    win = Window()
    settings = Settings()
    leader_board = LeaderBoard()
    win.show()
    exit(app.exec())
