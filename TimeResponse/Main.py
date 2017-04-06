from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtTest import *
import sys
import time
import random

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        # tworzenie klas widgetów, czyli naszych ekranów
        self.start_screen = Start()
        self.demo_screen = Demo()
        self.test_screen = Test()
        self.score_screen = Score()
        #dodanie ekranów do głównego okna
        self.central_widget.addWidget(self.start_screen)
        self.central_widget.addWidget(self.demo_screen)
        self.central_widget.addWidget(self.test_screen)
        self.central_widget.addWidget(self.score_screen)
        self.setGeometry(300,100,300,300)
        #ustawienie ekranu start jako domyslnego
        self.central_widget.setCurrentWidget(self.start_screen)
        #Nasłuchiwanie działań z ekranów i przełączanie ich
        self.start_screen.demoClicked.connect(lambda: self.central_widget.setCurrentWidget(self.demo_screen))
        self.start_screen.testClicked.connect(lambda: self.central_widget.setCurrentWidget(self.test_screen))

        self.demo_screen.startClicked.connect(lambda: self.central_widget.setCurrentWidget(self.start_screen))

        self.test_screen.startClicked.connect(lambda: self.central_widget.setCurrentWidget(self.start_screen))
        self.test_screen.scoreClicked.connect(lambda: self.central_widget.setCurrentWidget(self.score_screen))
        self.test_screen.scoreClicked.connect(lambda: self.central_widget.setCurrentWidget(self.score_screen.printScore(self.test_screen.testScore[-5:])))

        self.score_screen.startClicked.connect(lambda: self.central_widget.setCurrentWidget(self.start_screen))

class Start(QWidget):

    demoClicked = pyqtSignal()
    testClicked = pyqtSignal()
    def __init__(self):
        super(Start, self).__init__()
        l1 = QLabel("Witamy w teście na sprawność", self)
        l2 = QLabel('psychomotoryczną!',self)
        l3 = QLabel('Wciśnij Demo, aby potrenować.', self)
        l4 = QLabel('Wciśnij Test, aby przejść do testu!', self)
        l1.move(20, 50)
        l2.move(70, 80)
        l3.move(20, 150)
        l4.move(10, 190)
        font = QFont('times', 14)
        l1.setFont(font)
        l2.setFont(font)
        l3.setFont(font)
        l4.setFont(font)
        demoButton = QPushButton('Demo', self)
        testButton = QPushButton('Test', self)
        demoButton.setGeometry(45, 240, 100,50)
        testButton.setGeometry(155, 240, 100, 50)
        demoButton.clicked.connect(self.demoClicked.emit)
        testButton.clicked.connect(self.testClicked.emit)


class Demo(QWidget):

    startClicked = pyqtSignal()

    def __init__(self):
        super(Demo, self).__init__()
        self.tryNumber = 0
        self.color = 1  #3 kolory: 1 - czarny, 2 - czerwony, 3 - zielony
        startButton = QPushButton('Back to Start!', self)
        self.drawRect()
        startButton.clicked.connect(self.startClicked.emit)

        #obsługa etykiet, komunikatów
        font = QFont('times', 11)
        font2 = QFont('times', 10)
        self.l1 = QLabel(self)
        self.l1.setFont(font)
        self.l1.setText('Próba ' + str(self.tryNumber) + '/5')
        self.l1.move(90, 30)
        self.l2 = QLabel(self)
        self.l2.setText('Kliknij prostokąt, aby zacząć sprawdzian.')
        self.l2.move(20, 230)
        self.l2.setFont(font2)
        self.l3 = QLabel(self)
        self.l3.setFont(font)
        self.l3.move(90, 160)
        self.l3.setText('Wynik:                        ')

    def mousePressEvent(self, event):
        if event and self.color == 1:
            self.color = 2
            self.col.setRed(255)
            self.square.setStyleSheet("QFrame { background-color: %s }" %
                                    self.col.name())
            self.tryNumber += 1
            self.l1.setText('Próba ' + str(self.tryNumber) + '/5')
            self.l2.setText('Kliknij                        ')
        elif event and self.color == 2:
            self.l2.setText('Kliknij jak będzie zielony')
            self.delay()
            self.col.setRed(0)
            self.col.setGreen(255)
            self.square.setStyleSheet("QFrame { background-color: %s }" %
                                    self.col.name())
            self.t1 = time.clock()
            self.color = 3

        elif event and self.color == 3:
            self.t2 = time.clock()
            reactTime = (self.t2 - self.t1)*1000
            print(reactTime, ' ms')
            self.l3.setText('Wynik: '+str(reactTime)[:5]+' ms')
            self.col.setGreen(0)
            self.col.setRed(255)
            self.tryNumber += 1
            if self.tryNumber > 5:
                self.tryNumber = 0
                self.startClicked.emit()
                self.l3.setText('Wynik:                  ')
            self.l1.setText('Próba ' + str(self.tryNumber) + '/5')
            self.square.setStyleSheet("QFrame { background-color: %s }" %
                                      self.col.name())
            self.color = 2
            self.l2.setText('Kliknij')

    def drawRect(self):
        self.col = QColor(0,0,0)
        self.square = QFrame(self)
        self.square.setGeometry(90,50,120,100)
        self.square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())

    def delay(self):
        mSecs = random.randrange(1000, 3000, 10)
        QTest.qWait(mSecs)

class Test(QWidget):

    startClicked = pyqtSignal()
    scoreClicked = pyqtSignal()
    testScore = []

    def __init__(self):
        super(Test, self).__init__()
        self.tryNumber = 0
        self.testScore = []
        self.color = 1  #3 kolory: 1 - czarny, 2 - czerwony, 3 - zielony
        startButton = QPushButton('Back to Start!', self)
        self.drawRect()
        startButton.clicked.connect(self.startClicked.emit)

        #obsługa etykiet, komunikatów
        font = QFont('times', 11)
        font2 = QFont('times', 10)
        self.l1 = QLabel(self)
        self.l1.setFont(font)
        self.l1.setText('Próba ' + str(self.tryNumber) + '/5')
        self.l1.move(90, 30)
        self.l2 = QLabel(self)
        self.l2.setText('Kliknij prostokąt, aby zacząć sprawdzian.')
        self.l2.move(20, 230)
        self.l2.setFont(font2)
        self.l3 = QLabel(self)
        self.l3.setFont(font)
        self.l3.move(90, 160)
        self.l3.setText('Wynik:                        ')
    def mousePressEvent(self, event):
        if event and self.color == 1:
            self.color = 2
            self.col.setRed(255)
            self.square.setStyleSheet("QFrame { background-color: %s }" %
                                    self.col.name())
            self.tryNumber += 1
            self.l1.setText('Próba ' + str(self.tryNumber) + '/5')
            self.l2.setText('Kliknij                        ')
        elif event and self.color == 2:
            self.l2.setText('Kliknij jak będzie zielony')
            self.delay()
            self.col.setRed(0)
            self.col.setGreen(255)
            self.square.setStyleSheet("QFrame { background-color: %s }" %
                                    self.col.name())
            self.t1 = time.clock()
            self.color = 3

        elif event and self.color == 3:
            self.t2 = time.clock()
            reactTime = (self.t2 - self.t1)*1000
            self.l3.setText('Wynik: '+str(reactTime)[:5]+' ms')
            self.testScore.append(reactTime)
            self.col.setGreen(0)
            self.col.setRed(255)
            self.tryNumber += 1
            if self.tryNumber > 5:
                self.tryNumber = 0
                self.scoreClicked.emit()
                self.l3.setText('Wynik:                  ')
            self.l1.setText('Próba ' + str(self.tryNumber) + '/5')
            self.square.setStyleSheet("QFrame { background-color: %s }" %
                                      self.col.name())
            self.color = 2
            self.l2.setText('Kliknij')

    def drawRect(self):
        self.col = QColor(0,0,0)
        self.square = QFrame(self)
        self.square.setGeometry(90,50,120,100)
        self.square.setStyleSheet("QWidget { background-color: %s }" % self.col.name())

    def delay(self):
        mSecs = random.randrange(1000, 3000, 10)
        QTest.qWait(mSecs)


class Score(QWidget):

    startClicked = pyqtSignal()

    def __init__(self):
        super(Score, self).__init__()
        startButton = QPushButton('Back to Start!', self)
        startButton.clicked.connect(self.startClicked.emit)
        self.font = QFont('times', 22)
        self.font1 = QFont('times', 14)
        self.palette = QPalette()
        self.palette.setColor(QPalette.Foreground, Qt.red)
        self.l1 = QLabel('Wyniki!', self)
        self.l1.setFont(self.font)
        self.l1.move(105, 30)
        self.l2 = QLabel('                                    ',self)
        self.l2.setFont(self.font1)
        self.l2.move(30, 90)
        self.l3 = QLabel('                                    ',self)
        self.l3.setFont(self.font1)
        self.l3.move(30, 120)
        self.l4 = QLabel('                                    ',self)
        self.l4.setFont(self.font1)
        self.l4.move(30, 150)
        self.l5 = QLabel('                                    ',self)
        self.l5.setFont(self.font1)
        self.l5.move(30, 180)
        self.l6 = QLabel('                                    ',self)
        self.l6.setFont(self.font1)
        self.l6.move(30, 210)
        self.l7 = QLabel('                                    ',self)
        self.l7.setFont(self.font1)
        self.l7.move(30, 250)
        self.l7.setPalette(self.palette)

    def printScore(self, testScore):
        self.l2.setText('Próba I: ' + str(testScore[0])[:5] + ' ms')
        self.l3.setText('Próba II: ' + str(testScore[1])[:5] + ' ms')
        self.l4.setText('Próba III: ' + str(testScore[2])[:5] + ' ms')
        self.l5.setText('Próba IV: ' + str(testScore[3])[:5] + ' ms')
        self.l6.setText('Próba V: ' + str(testScore[4])[:5] + ' ms')
        avrg = sum(testScore)/len(testScore)
        self.l7.setText('Średnio: ' + str(avrg)[:5] + ' ms')

app = QApplication(sys.argv)
myWindow = MainWindow(None)
myWindow.show()
app.exec_()