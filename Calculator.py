import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import Qt
from math import sqrt
from PyQt4.QtGui import *
from time import strftime

num = 0.0
newNum = 0.0
sumAll = 0.0
operator = ""

opVar = False
sumIt = 0

class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def setBlue(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.darkBlue)
        self.setPalette(palette)

    def setWhite(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.white)
        self.setPalette(palette)

    def setGreen(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.darkGreen)
        self.setPalette(palette)

    def setRed(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.darkRed)
        self.setPalette(palette)

    def setGray(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.darkGray)
        self.setPalette(palette)

    def Time(self):
        self.lcd.display(strftime("%H" + ":" + "%M"))

    def digitClock(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Time)
        self.timer.start(1000)

        self.lcd = QtGui.QLCDNumber(self)
        self.lcd.move(50, 240)

    def initUI(self):

        self.digitClock()

        self.line = QtGui.QLineEdit(self)
        self.line.move(5, 30)
        self.line.setReadOnly(True)
        self.line.setAlignment(Qt.AlignRight)
        self.line.resize(200, 25)

        #Menu Bar
        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu('File')
        skinMenu = mainMenu.addMenu('Skins')

        # Add exit button
        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # Change skin
        blueButton = QAction('Blue', self)
        blueButton.setStatusTip('Blue')
        blueButton.triggered.connect(self.setBlue)

        whiteButton = QAction('White', self)
        whiteButton.setStatusTip('White')
        whiteButton.triggered.connect(self.setWhite)

        greenButton = QAction('Green', self)
        greenButton.setStatusTip('Green')
        greenButton.triggered.connect(self.setGreen)

        redButton = QAction('Red', self)
        redButton.setStatusTip('Red')
        redButton.triggered.connect(self.setRed)

        grayButton = QAction('Gray', self)
        grayButton.setStatusTip('Gray')
        grayButton.triggered.connect(self.setGray)

        skinMenu.addAction(blueButton)
        skinMenu.addAction(whiteButton)
        skinMenu.addAction(greenButton)
        skinMenu.addAction(redButton)
        skinMenu.addAction(grayButton)

        zero = QtGui.QPushButton("0", self)
        zero.move(50, 205)
        zero.resize(35, 30)

        one = QtGui.QPushButton("1", self)
        one.move(10, 170)
        one.resize(35, 30)

        two = QtGui.QPushButton("2", self)
        two.move(50, 170)
        two.resize(35, 30)

        three = QtGui.QPushButton("3", self)
        three.move(90, 170)
        three.resize(35, 30)

        four = QtGui.QPushButton("4", self)
        four.move(10, 135)
        four.resize(35, 30)

        five = QtGui.QPushButton("5", self)
        five.move(50, 135)
        five.resize(35, 30)

        six = QtGui.QPushButton("6", self)
        six.move(90, 135)
        six.resize(35, 30)

        seven = QtGui.QPushButton("7", self)
        seven.move(10, 100)
        seven.resize(35, 30)

        eight = QtGui.QPushButton("8", self)
        eight.move(50, 100)
        eight.resize(35, 30)

        nine = QtGui.QPushButton("9", self)
        nine.move(90, 100)
        nine.resize(35, 30)

        point = QtGui.QPushButton(".", self)
        point.move(90, 205)
        point.resize(35, 30)
        point.clicked.connect(self.pointClicked)

        div = QtGui.QPushButton("/", self)
        div.move(130, 100)
        div.resize(35, 30)

        mult = QtGui.QPushButton("*", self)
        mult.move(130, 135)
        mult.resize(35, 30)

        minus = QtGui.QPushButton("-", self)
        minus.move(130, 170)
        minus.resize(35, 30)

        plus = QtGui.QPushButton("+", self)
        plus.move(130, 205)
        plus.resize(35, 30)

        sqrt = QtGui.QPushButton("sqrt", self)
        sqrt.move(170, 100)
        sqrt.resize(35, 30)
        sqrt.clicked.connect(self.Sqrt)

        squared = QtGui.QPushButton("^2", self)
        squared.move(170, 135)
        squared.resize(35, 30)
        squared.clicked.connect(self.Squared)

        equal = QtGui.QPushButton("=", self)
        equal.move(170, 170)
        equal.resize(35, 65)
        equal.clicked.connect(self.Equal)

        c = QtGui.QPushButton("C", self)
        c.move(145, 60)
        c.resize(60, 30)
        c.clicked.connect(self.C)

        ce = QtGui.QPushButton("CE", self)
        ce.move(77, 60)
        ce.resize(60, 30)
        ce.clicked.connect(self.CE)

        back = QtGui.QPushButton("Back", self)
        back.move(10, 60)
        back.resize(60, 30)
        back.clicked.connect(self.Back)

        nums = [zero, one, two, three, four, five, six, seven, eight, nine]

        ops = [back, c, ce, div, mult, minus, plus, equal, sqrt, squared]

        rest = [squared, sqrt, point]

        for i in nums:
            i.setStyleSheet("color:blue;")
            i.clicked.connect(self.Nums)

        for i in ops:
            i.setStyleSheet("color:red;")

        for i in ops[3:7]:
            i.clicked.connect(self.Operator)

        # ---------Window settings --------------------------------
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.white)
        self.setPalette(palette)
        self.setGeometry(300, 300, 210, 220)
        self.setFixedSize(210, 280)
        self.setWindowTitle("Calculator")
        self.setWindowIcon(QtGui.QIcon(""))
        self.show()

    def keyPressEvent(self, event):
        global num
        global newNum
        global opVar
        global operator
        global sumIt
        global sumAll

        char = event.text()
        if char == '0' or char == '1' or char == '2' or char == '3' or char == '4' or char == '5' \
                or char == '6' or  char =='7' or char == '8' or char == '9':
            newNum = int(char)
            setNum = str(newNum)

            if opVar == False:
                self.line.setText(self.line.text() + setNum)
            else:
                self.line.setText(setNum)
                opVar = False

        if char == '+' or char == '-' or char == '*' or char == '/':
            sumIt += 1
            if sumIt > 1:
                self.Equal()
            num = self.line.text()
            operator = char
            opVar = True

        if char == '=':
            self.Equal()

        if char == '.':
            self.pointClicked()

        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def Nums(self):
        global num
        global newNum
        global opVar

        sender = self.sender()

        newNum = int(sender.text())
        setNum = str(newNum)

        if opVar == False:
            self.line.setText(self.line.text() + setNum)


        else:
            self.line.setText(setNum)
            opVar = False

    def pointClicked(self):
        global opVar

        if "." not in self.line.text():
            self.line.setText(self.line.text() + ".")

    def Operator(self):
        global num
        global opVar
        global operator
        global sumIt

        sumIt += 1

        if sumIt > 1:
            self.Equal()

        num = self.line.text()

        sender = self.sender()

        operator = sender.text()

        opVar = True

    def Equal(self):
        global num
        global newNum
        global sumAll
        global operator
        global opVar
        global sumIt

        sumIt = 0

        newNum = self.line.text()

        print(num)
        print(newNum)
        print(operator)

        if operator == "+":
            sumAll = float(num) + float(newNum)

        elif operator == "-":
            sumAll = float(num) - float(newNum)

        elif operator == "/":
            sumAll = float(num) / float(newNum)

        elif operator == "*":
            sumAll = float(num) * float(newNum)

        print(sumAll)
        self.line.setText(str(sumAll))
        opVar = True

    def Back(self):
        self.line.backspace()

    def C(self):
        global newNum
        global sumAll
        global operator
        global num

        self.line.clear()

        num = 0.0
        newNum = 0.0
        sumAll = 0.0
        operator = ""

    def CE(self):
        self.line.clear()

    def Sqrt(self):
        global num

        num = float(self.line.text())
        n = sqrt(num)
        num = n

        self.line.setText(str(num))

    def Squared(self):
        global num

        num = float(self.line.text())

        n = num ** 2

        num = n

        self.line.setText(str(n))


def main():
    app = QtGui.QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
