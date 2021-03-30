from json.decoder import JSONDecodeError
from PySide2 import QtWidgets, QtCore, QtGui

from Dictionnary import Dictionnary
import keyboard, time, json


class Mainwindow(QtWidgets.QWidget):

    def __init__(self, ctx):
        super(Mainwindow, self).__init__()
        self.ctx = ctx
        self.setWindowTitle('SpeedTextingApp')

        self.minuter = 60

        self.setupUi()        

        self.i = 0
        self.nb_mot = 0             
        self.liste_check = []
        self.check = ""
        self.timer_left_in = self.minuter
        self.timer = None
        
        
        
    def setupUi(self):
        self.createWidget()       
        self.modifyWidgets()
        self.createLayout()
        self.addWidgetToLayout()
        self.setupConnection()
        self.displayText()
        

    def createWidget(self):
        self.label_CPM = QtWidgets.QLabel('Corrected CPM')
        self.le_CPM = QtWidgets.QLineEdit('?')
        self.label_WPM = QtWidgets.QLabel('WPM')
        self.le_WPM = QtWidgets.QLineEdit('?')
        self.label_time = QtWidgets.QLabel('Time Left')
        self.le_time = QtWidgets.QLineEdit()
        self.btn_restart = QtWidgets.QPushButton('Restart')

        self.pte_string = QtWidgets.QListWidget()
        self.le_string = QtWidgets.QLineEdit('')

    def modifyWidgets(self):
        self.le_CPM.setEnabled(False)
        self.le_WPM.setEnabled(False)
        self.le_time.setEnabled(False)

        styleSheet = """
                        QListWidget {font:time; font-size:40px;}                                             
                        QLabel {font:time; font-size:20px}
                        QPlainTextEdit {font:time; font-size:40px; text-align:justify; letter-spacing:2px; word-spacing:20px;}
                        QLineEdit {font:time; font-size:20px; text-align:center;}
                        QPushButton {font:time; font-size: 20px; border: none; color:red; font-weight:bold}
                    """

        self.setStyleSheet(styleSheet)        

        self.pte_string.setAutoScroll(True)
        self.pte_string.setProperty("showDropIndicator", True)
        self.pte_string.setFlow(QtWidgets.QListView.LeftToRight)
        self.pte_string.setProperty("isWrapping", True)
        self.pte_string.setObjectName("pte_string")
        self.pte_string.setSpacing(10)
        self.le_string.setPlaceholderText('Type the text here')
        self.le_string.setStyleSheet('font:40px')
        self.le_time.setText(str(self.minuter))
               

    def createLayout(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)      
        self.label_layout = QtWidgets.QHBoxLayout()
        self.user_layout = QtWidgets.QHBoxLayout()

    def addWidgetToLayout(self):
        self.label_layout.addWidget(self.label_CPM)
        self.label_layout.addWidget(self.le_CPM)
        self.label_layout.addWidget(self.label_WPM)
        self.label_layout.addWidget(self.le_WPM)
        self.label_layout.addWidget(self.label_time)
        self.label_layout.addWidget(self.le_time)
        self.label_layout.addWidget(self.btn_restart)

        self.main_layout.addLayout(self.user_layout)
        self.main_layout.addLayout(self.label_layout)
        self.main_layout.addWidget(self.pte_string)
        self.main_layout.addWidget(self.le_string)

    def setupConnection(self):
        self.btn_restart.clicked.connect(self.restart)
        self.le_string.textChanged.connect(self.checking)
        self.le_string.textChanged.connect(self.start_timer)       

        self.le_string.setFocus()

        
    ##### Window Methods #############

    def displayText(self):
        self.i = 0        
        self.nb_mot = 0
        self.dictionnary = Dictionnary(200).random_list_word()
        self.pte_string.clear()
        for word in self.dictionnary:
            item = QtWidgets.QListWidgetItem(word)
            self.pte_string.addItem(item)          
        self.pte_string.setCurrentRow(self.nb_mot)    
        return self.dictionnary

    def update_label(self):
        self.timer_left_in -= 1
        self.le_time.setText(str(self.timer_left_in))        
        if self.timer_left_in == 0 :
            self.timer.stop()            
            self.le_time.setEnabled(False)
            self.check_results()

    def start_timer(self):
        if self.timer == None :       
            self.le_time.setEnabled(True)  
            self.timer = QtCore.QTimer()
            self.timer.timeout.connect(self.update_label)   
            self.timer.start(1000)                   

    def checking(self):
        self.pte_string.setCurrentRow(self.nb_mot)
        if keyboard.is_pressed('backspace'):
            if self.i == 0 :
                pass
            else:
                self.i -= 1

        if keyboard.is_pressed('space'):            
            #print(f"Keyboard Space : self.i = {self.i} len(dict) {len(self.dictionnary[self.nb_mot])} self.nb_mot = {self.nb_mot}")
            if self.i >= len(self.dictionnary[self.nb_mot]):
                
                self.liste_check.append(self.le_string.text()[-self.i - 1:-1]) 
                if self.nb_mot == len(self.dictionnary):
                    self.le_string.setEnabled(False)
                    self.check_results() 
                else:
                    self.nb_mot += 1
                    self.i = -1
                    self.pte_string.setCurrentRow(self.nb_mot)
                    self.le_string.clear()                   
                    #print(self.liste_check)
            else:
                self.i -= 1                
        self.i += 1     
  
    def check_results(self):        
        self.le_string.setEnabled(False)
        wpm = 0
        liste = []
        for i in range(0, len(self.dictionnary)):
            try:
                if  self.liste_check[i] == self.dictionnary[i]:            
                    wpm += 1
                    liste.append(self.liste_check[i])
            except IndexError:
                pass
        cpm = len(''.join(liste))
        self.le_CPM.setText(str(cpm))
        self.le_WPM.setText(str(wpm))
        #print("CPM WPM", cpm, wpm)
    
    def restart(self):        
        self.liste_check = []
        self.le_time.setText(str(self.minuter))
        self.le_time.setEnabled(True)
        self.le_CPM.setText('?')
        self.le_WPM.setText('?')
        self.le_string.clear()
        self.le_string.setPlaceholderText('Type the text here')
        self.le_string.setEnabled(True)
        self.le_string.setFocus()
        self.timer_left_in = self.minuter
        self.timer = None
        self.displayText()


      
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = Mainwindow(ctx=app)
    window.resize(800, 600)
    window.show()    
    app.exec_()


