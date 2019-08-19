from fbs_runtime.application_context.PyQt5 import ApplicationContext

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtMultimedia  import *

# from PySide.QtGui import *
# from PySide.QtWidgets import *
# from PySide.QtCore import *

import os
import sys

import Simon

class MainWindow(QMainWindow):

  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)

    self.sounds = self.initSounds()

    ###################
    ### Main Window ###
    ###################
    msgBarHeight = 10
    startBtnHeight = 75
    windowWidth = 500
    windowHeight = windowWidth + msgBarHeight + startBtnHeight
    self.resize(windowWidth, windowHeight)
    self.setStyleSheet("QMainWindow { color:rgb(255,255,255);"                    
                                      "background-color:#454545; }"
                       "QPushButton { font-size: 26pt;  font-family: Consolas; color: black;"
                                     "border: 5px solid black;"
                                     "border-radius: 15px;"
                                     "background: transparent; }"
                       "QPushButton:hover { color: white; border: 5px solid white; }" 
                       "QPushButton:pressed { color: rgb(0,255,0); border: 5px solid rgb(0,255,0); }" )

    MainVBoxLayout = QVBoxLayout()

    MainWidgetContainer = QWidget()
    MainWidgetContainer.setLayout(MainVBoxLayout)
    self.setCentralWidget(MainWidgetContainer)
        
    # status bar #
    self.status = QStatusBar()
    self.status.setStyleSheet("color:rgb(255,255,255);")    
    self.setStatusBar(self.status)

    #####################
    # Round No. display #
    #####################
    self.msgBar = QLineEdit("press START to begin new game")
    font = QFont("Serif", 9) 
    self.msgBar.setFont(font)
    self.msgBar.setStyleSheet("font-size: 16pt;  font-family: Consolas;"
                   "color:rgb(255,255,255);"
                   "border: 2px ridge #707070;"
                   "border-radius: 10px;"
                   "padding: 5px;"
                   "background-color:qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #393939, stop: 1 #343434);")
    self.msgBar.setReadOnly(True)
    self.msgBar.setAlignment(Qt.AlignCenter)

    msgBarWidth = 200
    self.msgBar.resize(msgBarWidth, msgBarHeight)

    policy = self.msgBar.sizePolicy()
    policy.setHorizontalPolicy(QSizePolicy.Expanding)
    self.msgBar.setSizePolicy(policy)

    ################
    # START button #
    ################
    self.startBtn = QPushButton("S T A R T")
    self.startBtn.setMinimumHeight(startBtnHeight)
    self.startBtn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    MainVBoxLayout.addWidget(self.startBtn)

    self.startBtn.setStatusTip("Start a new game")
    self.startBtn.clicked.connect(self.SLOT_start)

    ###########
    # BUTTONS #
    ###########
  
    # row 1 Layout #
    row1Layout = QHBoxLayout()
    MainVBoxLayout.addLayout(row1Layout)

    # row 2 Layout #
    row2Layout = QHBoxLayout()
    MainVBoxLayout.addLayout(row2Layout)

    # button 1 #
    self.btn1 = QPushButton()
    self.btn1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    row1Layout.addWidget(self.btn1)

    # button 2 #
    self.btn2 = QPushButton()
    self.btn2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    row1Layout.addWidget(self.btn2)

    # button 3 #
    self.btn3 = QPushButton()
    self.btn3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    row2Layout.addWidget(self.btn3)

    # button 4 #
    self.btn4 = QPushButton()   
    self.btn4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    row2Layout.addWidget(self.btn4)

    # style game buttons
    self.styleBtn(1)
    self.styleBtn(2)
    self.styleBtn(3)
    self.styleBtn(4)

    # connect game button clicks to synth sounds
    self.btn1.clicked.connect(self.sounds[1].play)
    self.btn2.clicked.connect(self.sounds[2].play)
    self.btn3.clicked.connect(self.sounds[3].play)
    self.btn4.clicked.connect(self.sounds[4].play)

    # add MsgBar at bottom
    MainVBoxLayout.addWidget(self.msgBar)

    self.updateTitle()
    self.show()

  # start Simon Says
  def SLOT_start(self):

    # create Simon Says back-end thread
    self.simonThread = Simon.SimonSays()

    # connect Simon Says thread signals to main thread methods
    self.simonThread.flash.connect(self.flashBtn)
    self.simonThread.sound.connect(self.playSound)
    self.simonThread.delay.connect(self.runDelayTimer)
    self.simonThread.setStatus.connect(self.status.showMessage)
    self.simonThread.setMsgBar.connect(self.msgBar.setText)
    self.simonThread.setWinTitle.connect(self.updateTitle)
    self.simonThread.btnEnable.connect(self.enableButtons)

    # connect GUI button signals to Simon Says thread SLOTs
    self.btn1.clicked.connect(self.simonThread.SLOT_btn1Clicked)
    self.btn2.clicked.connect(self.simonThread.SLOT_btn2Clicked)
    self.btn3.clicked.connect(self.simonThread.SLOT_btn3Clicked)
    self.btn4.clicked.connect(self.simonThread.SLOT_btn4Clicked)

    # run Simon Says thread
    self.simonThread.start()

  # flash button
  def flashBtn(self, btn, ms, sem):

    if (btn == 1):
      self.sounds[1].play()
      self.btn1.setStyleSheet("QPushButton{ background-color: rgb(255,0,0);"
                                            "border: transparent;"            
                                            "border-radius: 15px; }")

    elif (btn == 2):
      self.sounds[2].play()
      self.btn2.setStyleSheet("QPushButton{ background-color: rgb(0,255,0);"
                                            "border: transparent;"            
                                            "border-radius: 15px; }")

    elif (btn == 3):
      self.sounds[3].play()
      self.btn3.setStyleSheet("QPushButton{ background-color: rgb(0,0,255);"
                                            "border: transparent;"            
                                            "border-radius: 15px; }")
            
    elif (btn == 4):
      self.sounds[4].play()
      self.btn4.setStyleSheet("QPushButton{ background-color: rgb(255,255,0);"
                                            "border: transparent;"            
                                            "border-radius: 15px; }") 

    self.runFlashTimer(btn, ms, sem)

  # flash button timer
  def runFlashTimer(self, btn, ms, sem):
    self.timer = QTimer()
    self.timer.timeout.connect( lambda: self.styleBtn(btn, sem) )
    self.timer.start(ms)    

  # delay timer used in between pattern flashes
  def runDelayTimer(self, ms, sem):
    self.timer = QTimer()
    self.timer.timeout.connect(sem.release)
    self.timer.start(ms)                      

  # set button stylesheet to normal
  def styleBtn(self, btn, sem=None):

    if (btn == 1):
      self.btn1.setStyleSheet("QPushButton{ background-color: rgb(255,175,175);"
                                           "border: transparent;"           
                                           "border-radius: 15px; }"
                            "QPushButton:hover{ background-color: rgb(255,0,0); }"
                            "QPushButton:pressed{ border: 5px ridge white; border-radius: 35px; }")

    elif (btn == 2):
      self.btn2.setStyleSheet("QPushButton{ background-color: rgb(175,255,175);"
                                           "border: transparent;"           
                                           "border-radius: 15px; }"
                            "QPushButton:hover{ background-color: rgb(0,255,0); }"
                            "QPushButton:pressed{ border: 5px ridge white; border-radius: 35px; }")

    elif (btn == 3):
      self.btn3.setStyleSheet("QPushButton{ background-color: rgb(175,175,255);"
                                           "border: transparent;"           
                                           "border-radius: 15px; }"
                            "QPushButton:hover{ background-color: rgb(0,0,255); }"
                            "QPushButton:pressed{ border: 5px ridge white; border-radius: 35px; }")
        
    elif (btn == 4):
      self.btn4.setStyleSheet("QPushButton{ background-color: rgb(255,255,175);"
                                           "border: transparent;"           
                                           "border-radius: 15px; }"
                            "QPushButton:hover{ background-color: rgb(255,255,0); }"
                            "QPushButton:pressed{ border: 5px ridge white; border-radius: 35px; }")

    if (sem):
      sem.release()

  # enable / disable game buttons
  def enableButtons(self, en):
    self.btn1.setEnabled(en)
    self.btn2.setEnabled(en)
    self.btn3.setEnabled(en)
    self.btn4.setEnabled(en)

  # init synth sounds from sounds/*.wav files
  def initSounds(self):
    soundsPath = "../sounds/"
    sounds = {
      # 2: QSound(self.resource_path('sounds/nice-work.wav')),
      # 3: QSound(self.resource_path('sounds/nice-work.wav')),
      # 4: QSound(self.resource_path('sounds/nice-work.wav')),
      # 1: QSound(self.resource_path('sounds/nice-work.wav')),

      # 2: QSound(self.resource_path('sounds/808s/Cymatics x San Holo - 808 2 - C.wav')),
      # 3: QSound(self.resource_path('sounds/808s/Cymatics x San Holo - 808 3 - D#.wav')),
      # 4: QSound(self.resource_path('sounds/808s/Cymatics x San Holo - 808 4 - E.wav')),
      # 1: QSound(self.resource_path('sounds/808s/Cymatics x San Holo - 808 1 - C.wav'))

      # 2: QSound(self.resource_path('sounds/simon 2 saec1.wav')),
      # 3: QSound(self.resource_path('sounds/simon 2 sec2.wav')),
      # 4: QSound(self.resource_path('sounds/simon 2 sec3.wav'))

      1: QSound(soundsPath+"nice-work.wav"),
      2: QSound(soundsPath+"nice-work.wav"),
      3: QSound(soundsPath+"nice-work.wav"),
      4: QSound(soundsPath+"nice-work.wav")
    }

    return sounds

  # play sound effect
  def playSound(self, i):
    self.sounds[i].play()

  # critical dialog pop-up
  def SLOT_dialogCritical(self, s):
    dlg = QMessageBox(self)
    dlg.setText(s)
    dlg.setIcon(QMessageBox.Critical)
    dlg.show()

  # update main window title
  def updateTitle(self, str=""):
    self.setWindowTitle("SiMoN sAyS "+ str)

  # Get absolute path to resource, works for dev and for PyInstaller  -   used to set icon paths
  # https://stackoverflow.com/questions/33144448/icons-in-pyqt-app-created-by-pyinstaller-wont-work-on-other-computers
  #______________________________________________________________________________________________
  def resource_path(self,relative_path):
    try:
      # PyInstaller creates a temp folder and stores path in _MEIPASS
      base_path = sys._MEIPASS
    except Exception:
      base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#______________________________________________________________________________________________

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    Window = MainWindow()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)