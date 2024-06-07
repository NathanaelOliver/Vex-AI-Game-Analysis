import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Game Window")
        self.setGeometry(200, 200, 400, 300)
        self.label = QLabel("Game Window", self)
        self.setCentralWidget(self.label)

class StatsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stats Window")
        self.setGeometry(300, 300, 400, 300)
        self.label = QLabel("Stats Window", self)
        self.setCentralWidget(self.label)

class AIWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Visualization Window")
        self.setGeometry(400, 400, 400, 300)
        self.label = QLabel("AI Visualization Window", self)
        self.setCentralWidget(self.label)

class SuccessWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Success Rate Window")
        self.setGeometry(500, 500, 400, 300)
        self.label = QLabel("Success Rate Window", self)
        self.setCentralWidget(self.label)


class MainApplication:
    def __init__(self):
        self.game_window = GameWindow()
        self.stats_window = StatsWindow()
        self.ai_window = AIWindow()
        self.success_window = SuccessWindow()

    def run(self):
        self.game_window.show()
        self.stats_window.show()
        self.ai_window.show()
        self.success_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApplication()
    r = input()
    main_app.run()
    sys.exit(app.exec_())

