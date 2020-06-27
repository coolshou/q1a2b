#!/usr/bin/env python3

# 1A2B猜數字遊戲
# 可選擇一到九位數來進行猜數字，數字可重複
import sys
import os
from random import randint, shuffle
# Import the Gtts module for text to speech conversion 
# from gtts import gTTS 
try:
    import pyttsx3
except ImportError:
    print("pip install pyttsx3")
    raise SystemExit
try:
    from PyQt5.QtCore import (pyqtSlot, pyqtSignal)
    from PyQt5.QtGui import (QIcon)
    from PyQt5.QtWidgets import ( QMainWindow, QMessageBox, QTableWidgetItem,
                                 QApplication)
    # from PyQt5.QtNetwork import (QHostAddress)
    from PyQt5.uic import loadUi
except ImportError:
    print("pip install PyQt5")
    raise SystemExit

items = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
notice = {
    0: "加油",
    1: "再加油",
    2: "不錯喔",
    3: "很接近了"
    }


class Q1A2B(QMainWindow):
    '''  1A2B class    '''
    signal_debug = pyqtSignal(str, str)
    sig_prj_status = pyqtSignal(str)  # have new/open/close project

    # close any dialog
    sig_close_dlg =  pyqtSignal(int)

    def __init__(self, tray=True):
        super(Q1A2B, self).__init__()
        if getattr(sys, 'frozen', False):
            # we are running in a |PyInstaller| bundle
            self._basedir = sys._MEIPASS
        else:
            # we are running in a normal Python environment
            self._basedir = os.path.dirname(__file__)
        loadUi(os.path.join(self._basedir, 'q1a2b.ui'), self)
        
        self.answer = ""
        self.playerGuess = ""
        self.nOfDigits = self.sbGuessLen.value()
    
        self.pbNew.clicked.connect(self.newGame)
        self.pbGuess.clicked.connect(self.checkUserGuess)
        self.actionAnswer.triggered.connect(self.showAnswer)
        self.newGame()
        self.setWindowIcon(QIcon(os.path.join(self._basedir, 
                                              "images", "q1a2b.png")))
        self._speech = pyttsx3.init()
        
    @pyqtSlot()
    def showAnswer(self):
        QMessageBox.information(self, "答案", "答案為:%s" % str(self.answer))
        
    def nDigitNumber(self, n):
        if self.cbRepeate.isChecked():
            # 產生n位數的數字，例如 n = 3 會輸出 100 ~ 999 三位數的數值。
            start = 10**(n-1)
            end = (10**n)-1
            return str( randint(start, end) )
        else:
            # 產生不重複的n數字
            answer=''
            shuffle(items)
            for i in range(4):
                answer+=str(items[i])
            return answer
            
    @pyqtSlot()
    def newGame(self):
        self.nOfDigits = self.sbGuessLen.value()
        self.answer = self.nDigitNumber(self.nOfDigits)
        self.twResult.clearContents()
        self.twResult.setRowCount(0)
        self.leGuess.setText("")

    @pyqtSlot()    
    def checkUserGuess(self):
        self.playerGuess = self.leGuess.text()
        if len(self.playerGuess) == self.nOfDigits:
            a = self.calA(self.playerGuess)
            b = self.calB(self.playerGuess)
            self.showResult(self.playerGuess, a, b)
        else:
            msg =  "位數要為:%s" % (self.nOfDigits)
            QMessageBox.information(self, "提醒", msg)
            self.speek(msg)
            self.leGuess.setFocus()
    
    def calA(self, guess):
        a = 0
        for i in range( len(self.answer) ):
            if guess[i] == self.answer[i]:
                a = a + 1
        return a
    
    def calB(self, guess):
        b = 0
        k = len(self.answer)
        for i in range(k):
            for j in range(k):
                if(i != j):
                    if guess[i] == self.answer[j]:
                        b = b + 1
        return b

    def showResult(self, guess, a, b):
        if a == self.nOfDigits:
            result = "You Win"
            self.speek(result)
            QMessageBox.information(self, "提醒", "<b>%s</b>" % result)
        else:
            result = str(a) + "A" + str(b) + "B"
            self.addResult(guess, result)
            self.speek(result)
            if a > 2:
                self.speek(notice.get(3))
            elif a > 1:
                self.speek(notice.get(2))
            elif b > 2:
                self.speek(notice.get(1))
            else:
                self.speek(notice.get(0))

    def addResult(self, guess, result):
        num = self.twResult.rowCount()
        idx = num + 1
        self.twResult.setRowCount(idx)
        self.twResult.setItem(num, 0, QTableWidgetItem(guess))
        self.twResult.setItem(num, 1, QTableWidgetItem(result))

    def speek(self, text):
        # TODO: put in thread todo the tts convert!!
        self._speech.say(text)
        self._speech.runAndWait()
        '''
        gtts
        # Language we want to use 
        language = 'en'
        myobj = gTTS(text, lang=language, slow=False) 
        myobj.save("output.mp3") 
          
        # Play the converted file 
        # os.system("start output.mp3")
        '''
        
# main
if __name__ == '__main__':
    APP = QApplication(sys.argv)
    MAINWIN = Q1A2B()
    MAINWIN.show()

    sys.exit(APP.exec_())
