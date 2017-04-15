from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtTest import *
import sys
import time
import random
from Sound import Sound
import threading

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        # tworzenie klas widgetów, czyli naszych ekranów
        self.start_screen = StartScreen()
        self.main_screen = MainScreen()
        #dodanie ekranów do głównego okna
        self.central_widget.addWidget(self.start_screen)
        self.central_widget.addWidget(self.main_screen)
        self.setGeometry(300,100,700,500)

        #ustawienie ekranu start jako domyslnego
        self.central_widget.setCurrentWidget(self.main_screen)
        #Nasłuchiwanie działań z ekranów i przełączanie ich

        self.start_screen.mainClicked.connect(lambda: self.central_widget.setCurrentWidget(self.main_screen))
        self.start_screen.mainClicked.connect(lambda: self.central_widget.setCurrentWidget(self.main_screen.mainTimer.start()))
        self.start_screen.mainClicked.connect(lambda: self.central_widget.setCurrentWidget(self.main_screen.warningTimer.start()))
        self.main_screen.logoutClicked.connect(lambda: self.central_widget.setCurrentWidget(self.start_screen))


#login dialog
class StartScreen(QWidget):
    mainClicked = pyqtSignal()
    def __init__(self):
        super(StartScreen, self).__init__()
        loginButton = QPushButton('Zaloguj', self)
        loginButton.setGeometry(365, 200, 70, 30)
        loginButton.clicked.connect(self.checkCorrectness)
        self.prepareLabels()

        self.textLog = QLineEdit(self)
        self.textLog.move(300, 100)

        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)
        self.textPass.move(300, 150)

    def prepareLabels(self):
        self.font = QFont('times', 13)
        self.font1 = QFont('times', 10)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Foreground, Qt.red)
        self.loginLabel = QLabel('Login', self)
        self.loginLabel.move(240, 100)
        self.loginLabel.setFont(self.font)
        self.passLabel = QLabel('Hasło', self)
        self.passLabel.move(240, 150)
        self.passLabel.setFont(self.font)
        self.incorrectLabel = QLabel('                                                                  ', self)
        self.incorrectLabel.setFont(self.font1)
        self.incorrectLabel.move(240, 50)
        self.incorrectLabel.setPalette(self.palette)

    def checkCorrectness(self):
        if self.textLog.text().strip() == 'user' and self.textPass.text() == 'user':
            self.mainClicked.emit()
            self.incorrectLabel.setText('                                                                  ')
            self.textLog.setText('')
            self.textPass.setText('')
        else:
            self.incorrectLabel.setText('Nieprawidłowy login, lub hasło.')

    def keyPressEvent(self, event):
        #Key_Return bo to jest duży enter, key_enter to ten na numpadzie xDDDD
        if event.key() == Qt.Key_Return:
            self.checkCorrectness()


class MainScreen(QWidget):

    logoutClicked = pyqtSignal()

    def __init__(self):
        super(MainScreen, self).__init__()

        self.progress = 0
        self.amountOfProducts = 0
        self.productLabel = QLabel(self)
        self.productLabel.setText('Wyprodukowano sztuk: {0}   '.format(self.amountOfProducts))

        self.mainTimer = QTimer()
        self.mainTimer.setInterval(15000)
        self.mainTimer.timeout.connect(self.presenceControl)

        self.warningTimer = QTimer()
        self.warningTimer.setInterval(5000)
        self.warningTimer.timeout.connect(self.warningAction)

        self.pBar = QProgressBar(self)
        self.pBar.setGeometry(20, 200, 400, 20)
        self.progressTimer = QTimer()
        self.progressTimer.setInterval(500)
        self.progressTimer.timeout.connect(self.progressAction)

        self.productionSpeedSlider = QSlider(Qt.Horizontal, self)
        self.productionSpeedSlider.setMinimum(1)
        self.productionSpeedSlider.setMaximum(10)
        self.productionSpeedSlider.move(20, 100)
        self.productionSpeedSlider.setValue(5)
        self.productionSpeedSlider.setTickPosition(QSlider.TicksBothSides)
        self.productionSpeedSlider.setTickInterval(1)
        self.productionSpeedSlider.valueChanged.connect(lambda: self.progressTimer.setInterval(100*self.productionSpeedSlider.value()))

        startButton = QPushButton('Start', self)
        startButton.setGeometry(20, 250, 70, 30)
        startButton.clicked.connect(self.progressTimer.start)

        stopButton = QPushButton('Stop', self)
        stopButton.setGeometry(310, 250, 70, 30)
        stopButton.clicked.connect(self.progressTimer.stop)

        logoutButton = QPushButton('Wyloguj!', self)
        logoutButton.setGeometry(610, 10, 70, 30)
        logoutButton.clicked.connect(self.logoutClicked.emit)
        logoutButton.clicked.connect(self.stopMainTime)
        logoutButton.clicked.connect(self.progressTimer.stop)

    def progressAction(self):
        self.progress += 1
        if self.progress > 100:
            self.progress = 0
            self.amountOfProducts += 1
            self.productLabel.setText('Wyprodukowano sztuk: {0}   '.format(self.amountOfProducts))
        self.pBar.setValue(self.progress)

    def stopMainTime(self):
        self.mainTime = 0
        self.mainTimer.stop()

    def presenceControl(self):
        self.callControlBox()
        self.mainTime = 0
        self.mainTimer.stop()

    def callControlBox(self):
        self.controlBox = QMessageBox(self)
        self.timeToWait = 10
        self.controlBox.setText('Kontrola obecności. Zareaguj w ciągu {0} sekund!'.format(self.timeToWait))
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.controlBox.setStandardButtons(QMessageBox.Ok)
        self.controlBox.open()
        self.timer.timeout.connect(self.changeContent)
        self.timer.start()

    def warningAction(self):
        if random.randrange(0, 5) == 1:
            warningBox = QMessageBox(self)
            warningBox.setText('Silnik uległ awarii!!! Wstrzymano produkcję!!!')
            self.progressTimer.stop()
            threading.Thread(target=Sound).start()
            warningBox.open()

    def changeContent(self):
        self.timeToWait -= 1
        self.controlBox.setText('Kontrola obecności. Zareaguj w ciągu {0} sekund!'.format(self.timeToWait))
        if self.controlBox.clickedButton():
            self.timer.stop()
            self.timeToWait = 10
            self.mainTimer.start()
        if self.timeToWait <= 0:
            self.logoutClicked.emit()
            threading.Thread(target=Sound).start()
            self.controlBox.close()
            self.timeToWait = 10
            self.timer.stop()
            self.warningTimer.stop()
            self.progressTimer.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MainWindow(None)
    myWindow.show()
    app.exec_()