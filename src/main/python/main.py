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

    self.appctxt    = ApplicationContext()
    self.sounds     = self.initSounds()
    self.difficulty = "easy"

    # fonts #
    QFontDatabase.addApplicationFont(self.appctxt.get_resource('fonts/LLPIXEL3.ttf'))
    QFontDatabase.addApplicationFont(self.appctxt.get_resource('fonts/batmfo__.ttf'))
    QFontDatabase.addApplicationFont(self.appctxt.get_resource('fonts/batmfa__.ttf'))

    ###################
    ### Main Window ###
    ###################
    msgBarHeight = 10
    startBtnHeight = 75
    difficultyBtnHeight = 15
    windowWidth = 500
    windowHeight = windowWidth + msgBarHeight + difficultyBtnHeight
    self.setFixedSize(windowWidth, windowHeight)
    self.setStyleSheet("QMainWindow { color:rgb(255,255,255);"                    
                                      "background-color:#606060;"
                                      "font-family: BatmanForeverOutline; }"
                       "QPushButton { font-size: 26pt; color: black; font-family: BatmanForeverAlternate;"
                                     "border: 5px solid black;"
                                     "border-radius: 15px;"
                                     "background: transparent; }"
                       "QPushButton:hover { color: white; border: 5px solid white; }" 
                       "QPushButton:pressed { color: rgb(150,255,150); border: 5px solid rgb(150,255,150); }" )

    MainVBoxLayout = QVBoxLayout()

    MainWidgetContainer = QWidget()
    MainWidgetContainer.setLayout(MainVBoxLayout)
    self.setCentralWidget(MainWidgetContainer)
        
    # status bar #
    self.status = QStatusBar()
    self.status.setStyleSheet("color:rgb(255,255,255);")    
    self.setStatusBar(self.status)

    #####################
    #  Message Display  #
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
    # MainVBoxLayout.addWidget(self.startBtn)



    ################
    # EASY  button #
    ################
    self.easyBtn = QPushButton("EASY")
    self.easyBtn.setStyleSheet("QPushButton { font-size: 22pt; font-family: BatmanForeverAlternate;  color: black;"
                                              "padding: 5px;"
                                              "border: 5px solid black;"
                                              "border-radius: 15px;"
                                              "background: transparent; }"
                              "QPushButton:hover { color: white; border: 5px solid white; }" 
                              "QPushButton:checked { color: rgb(0,255,0); border: 5px solid rgb(0,255,0); }" )

    self.easyBtn.setCheckable(True)
    self.easyBtn.setChecked(True)
    self.easyBtn.setStatusTip("Classic ~ Simon adds on to the previous pattern every round")
    self.easyBtn.clicked.connect(self.SLOT_easyBtn)

    ################
    # HARD  button #
    ################
    self.hardBtn = QPushButton("HARD")
    self.hardBtn.setStyleSheet("QPushButton { font-size: 22pt;  font-family: BatmanForeverAlternate; color: black;"
                                              "padding: 5px;"
                                              "border: 5px solid black;"
                                              "border-radius: 15px;"
                                              "background: transparent; }"
                              "QPushButton:hover { color: white; border: 5px solid white; }" 
                              "QPushButton:checked { color: rgb(255,0,0); border: 5px solid rgb(255,0,0); }" )

    self.hardBtn.setCheckable(True)
    self.hardBtn.setChecked(False)
    self.hardBtn.setStatusTip("Challenger ~ Simon plays a new random pattern every round")
    self.hardBtn.clicked.connect(self.SLOT_hardBtn)

    # EASY-HARD button sizing
    difficultyBtnWidth = 175
    self.easyBtn.setMinimumWidth(difficultyBtnWidth)
    self.easyBtn.setMinimumHeight(difficultyBtnHeight)
    self.hardBtn.setMinimumWidth(difficultyBtnWidth)
    self.hardBtn.setMinimumHeight(difficultyBtnHeight)

    # spacers #
    spacerEasy = QWidget()
    spacerEasyHard = QWidget()
    spacerHard = QWidget()
    spacerEasy.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    spacerEasyHard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
    spacerHard.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

    # EASY-HARD button row
    difficultyLayout = QHBoxLayout()
    MainVBoxLayout.addLayout(difficultyLayout)

    difficultyLayout.addWidget(spacerEasy)   
    difficultyLayout.addWidget(self.easyBtn)
    difficultyLayout.addWidget(spacerEasyHard)
    difficultyLayout.addWidget(self.hardBtn)
    difficultyLayout.addWidget(spacerHard)

    ################
    # GAME BUTTONS #
    ################
  
    # Layout #
    btnLayout   = QVBoxLayout()
    row1Layout  = QHBoxLayout()
    row2Layout  = QHBoxLayout()

    btnLayout.addLayout(row1Layout)
    btnLayout.addLayout(row2Layout)
    MainVBoxLayout.addLayout(btnLayout)

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

    # START #
    self.startBtn = QPushButton(MainWidgetContainer)
    self.startBtn.setText("START")
    self.startBtn.setStatusTip("Start a new game")
    startBtnWidth = 200
    startBtnHeight = startBtnWidth
    self.startBtn.resize(startBtnWidth,startBtnHeight)
    pos = QPoint(windowWidth/2 - startBtnWidth/2, windowHeight/2 - startBtnHeight/2)
    self.startBtn.move(pos)

    self.startBtn.clicked.connect(self.SLOT_start)

    # style game buttons
    self.styleBtn(0)
    self.styleBtn(1)
    self.styleBtn(2)
    self.styleBtn(3)
    self.styleBtn(4)

    # connect game button press to synth sounds
    self.btn1.pressed.connect(self.sounds[1].play)
    self.btn2.pressed.connect(self.sounds[2].play)
    self.btn3.pressed.connect(self.sounds[3].play)
    self.btn4.pressed.connect(self.sounds[4].play)

    # connect game button press / release to style center START button
    self.btn1.pressed.connect(lambda: self.flashStart(1))
    self.btn2.pressed.connect(lambda: self.flashStart(2))
    self.btn3.pressed.connect(lambda: self.flashStart(3))
    self.btn4.pressed.connect(lambda: self.flashStart(4))
    self.btn1.released.connect(self.styleBtn)
    self.btn2.released.connect(self.styleBtn)
    self.btn3.released.connect(self.styleBtn)
    self.btn4.released.connect(self.styleBtn)

    # add MsgBar at bottom
    MainVBoxLayout.addWidget(self.msgBar)

    self.updateTitle()
    self.show()

  # start Simon Says
  def SLOT_start(self):

    # disable difficulty selection
    self.enableDifficultyButtons(False)

    # create Simon Says back-end thread
    self.simonThread = Simon.SimonSays(self.difficulty)

    # connect Simon Says thread signals to main thread methods
    self.simonThread.flash.connect(self.flashBtn)
    self.simonThread.delay.connect(self.runDelayTimer)
    self.simonThread.sound.connect(self.playSound)
    self.simonThread.revert.connect(self.styleBtn)
    self.simonThread.setStatus.connect(self.status.showMessage)
    self.simonThread.setMsgBar.connect(self.msgBar.setText)
    self.simonThread.setWinTitle.connect(self.updateTitle)
    self.simonThread.btnEnable.connect(self.enableButtons)
    self.simonThread.finished.connect(self.enableDifficultyButtons)

    # connect GUI button signals to Simon Says thread SLOTs
    self.btn1.clicked.connect(self.simonThread.SLOT_btn1Clicked)
    self.btn2.clicked.connect(self.simonThread.SLOT_btn2Clicked)
    self.btn3.clicked.connect(self.simonThread.SLOT_btn3Clicked)
    self.btn4.clicked.connect(self.simonThread.SLOT_btn4Clicked)

    # run Simon Says thread
    self.simonThread.start()

  # set button stylesheet to normal
  def styleBtn(self, btn=0, sem=None):

    if (btn == 0):
      self.startBtn.setStyleSheet("QPushButton { font-size: 26pt; font-family: BatmanForeverAlternate; color: black;"
                                                "border: 5px solid black;"
                                                "border-radius: 100px;"
                                                "background: gray; }"
                            "QPushButton:hover { color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #FF0000, stop: 0.4 #FFFF00, stop: 0.45 #00FF00, stop: 1.0 #0000FF);"
                                                "border-bottom-color: rgb(0,255,0);"
                                                "border-left-color: rgb(255,0,0);"
                                                "border-top-color: rgb(0,0,255);"
                                                "border-right-color: rgb(255,255,0); }" 
                            "QPushButton:pressed { color: rgb(0,255,0); border: 5px solid rgb(0,255,0); }" )

    if (btn == 1):
      self.btn1.setStyleSheet("QPushButton{ background-color: rgb(175,255,175);"
                                           "border: 5px solid black;"                                            
                                           "border-radius: 15px;"                                           
                                           "border-top-left-radius: 75px; }"
                            "QPushButton:hover{ border-color: rgb(0,255,0); }"
                            "QPushButton:pressed{ border-width: 7px; border-color: rgb(0,100,0); background-color: rgb(0,255,0); }")

    elif (btn == 2):
      self.btn2.setStyleSheet("QPushButton{ background-color: rgb(255,175,175);"
                                           "border: 5px solid black;"         
                                           "border-radius: 15px;"
                                           "border-top-right-radius: 75px; }"
                            "QPushButton:hover{ border-color: rgb(255,0,0); }"
                            "QPushButton:pressed{ border-width: 7px; border-color: rgb(100,0,0); background-color: rgb(255,0,0); }")

    elif (btn == 3):
      self.btn3.setStyleSheet("QPushButton{ background-color: rgb(255,255,175);"
                                           "border: 5px solid black;"         
                                           "border-radius: 15px;"
                                           "border-bottom-left-radius: 75px; }"
                            "QPushButton:hover{ border-color: rgb(255,255,0); }"
                            "QPushButton:pressed{ border-width: 7px; border-color: rgb(75,75,0); background-color: rgb(255,255,0); }")
        
    elif (btn == 4):
      self.btn4.setStyleSheet("QPushButton{ background-color: rgb(175,175,255);"
                                           "border: 5px solid black;"      
                                           "border-radius: 15px;"
                                           "border-bottom-right-radius: 75px; }"
                            "QPushButton:hover{ border-color: rgb(0,0,255); }"
                            "QPushButton:pressed{ border-width: 7px; border-color: rgb(0,0,100); background-color: rgb(0,0,255); }")

    if (sem):
      sem.release()

  # flash START button
  def flashStart(self, btn):

    if (btn == 1):
      self.startBtn.setStyleSheet("QPushButton { font-size: 26pt; font-family: BatmanForeverAlternate; color: rgb(0,255,0);"
                                              "border: 5px solid black;"                                              
                                              "border-radius: 100px;"
                                              "background: gray; }" )

    elif (btn == 2):
      self.startBtn.setStyleSheet("QPushButton { font-size: 26pt; font-family: BatmanForeverAlternate; color: rgb(255,0,0);"
                                              "border: 5px solid black;"                                              
                                              "border-radius: 100px;"
                                              "background: gray; }" )

    elif (btn == 3):
      self.startBtn.setStyleSheet("QPushButton { font-size: 26pt; font-family: BatmanForeverAlternate; color: rgb(255,255,0);"
                                              "border: 5px solid black;"                                              
                                              "border-radius: 100px;"
                                              "background: gray; }" )

    elif (btn == 4):
      self.startBtn.setStyleSheet("QPushButton { font-size: 26pt; font-family: BatmanForeverAlternate; color: rgb(0,0,255);"
                                              "border: 5px solid black;"                                              
                                              "border-radius: 100px;"
                                              "background: gray; }" )

  # flash button
  def flashBtn(self, btn, ms, sem):

    if (btn == 1):
      self.flashStart(1)
      self.btn1.setStyleSheet("QPushButton{ background-color: rgb(0,255,0);"
                                           "border: 5px ridge black;"                                            
                                           "border-radius: 15px;"                                           
                                           "border-top-left-radius: 75px; }")

    elif (btn == 2):
      self.flashStart(2)
      self.btn2.setStyleSheet("QPushButton{ background-color: rgb(255,0,0);"
                                           "border: 5px ridge black;"         
                                           "border-radius: 15px; "
                                           "border-top-right-radius: 75px; }")

    elif (btn == 3):
      self.flashStart(3)
      self.btn3.setStyleSheet("QPushButton{ background-color: rgb(255,255,0);"
                                           "border: 5px ridge black;"         
                                           "border-radius: 15px;"
                                           "border-bottom-left-radius: 75px; }")
            
    elif (btn == 4):
      self.flashStart(4)
      self.btn4.setStyleSheet("QPushButton{ background-color: rgb(0,0,255);"
                                           "border: 5px ridge black;"      
                                           "border-radius: 15px;"
                                           "border-bottom-right-radius: 75px; }") 

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

  # enable / disable game buttons
  def enableButtons(self, en):
    self.btn1.setEnabled(en)
    self.btn2.setEnabled(en)
    self.btn3.setEnabled(en)
    self.btn4.setEnabled(en)

  # enable / disable difficulty selection buttons
  def enableDifficultyButtons(self, en=True):
    self.easyBtn.setEnabled(en)
    self.hardBtn.setEnabled(en)
    self.startBtn.setEnabled(en)

  # init synth sounds from sounds/*.wav files
  def initSounds(self):
    soundsPath = "../sounds/"
    sounds = {
      
      # START-UP #
      # 0: QSound(self.appctxt.get_resource('/home/mojo/devel/git/Simon/src/main/resources/base/sounds/Cymatics - Mothership Dubstep Sample Pack/Synths - Loops/Cymatics - Mothership Drop Loop 1 - 150 BPM F.wav')),
      0: QSound(self.appctxt.get_resource('/home/mojo/devel/git/Simon/src/main/resources/base/sounds/Cymatics - Mothership Dubstep Sample Pack/Synths - Loops/Cymatics - Mothership Drop Loop 2 - 150 BPM F.wav')),
      # 0: QSound(self.appctxt.get_resource('/home/mojo/devel/git/Simon/src/main/resources/base/sounds/Cymatics - Mothership Dubstep Sample Pack/Synths - Loops/Cymatics - Mothership Drop Loop 3 - 150 BPM F.wav')),
      # 0: QSound(self.appctxt.get_resource('/home/mojo/devel/git/Simon/src/main/resources/base/sounds/Cymatics - Mothership Dubstep Sample Pack/Synths - Loops/Cymatics - Mothership Drop Loop 4 - 150 BPM F.wav'))

      # WUB-SYNTH #
      1: QSound(self.appctxt.get_resource('sounds/Cymatics - Mothership Dubstep Sample Pack/Synths - One Shots/Cymatics - Mothership Bass One Shot 10 - F.wav')),
      2: QSound(self.appctxt.get_resource('sounds/Cymatics - Mothership Dubstep Sample Pack/Synths - One Shots/Cymatics - Mothership Bass One Shot 9 - F.wav')), # w/ snare
      3: QSound(self.appctxt.get_resource('sounds/Cymatics - Mothership Dubstep Sample Pack/Synths - One Shots/Cymatics - Mothership Bass One Shot 1 - E.wav')),
      4: QSound(self.appctxt.get_resource('sounds/Cymatics - Mothership Dubstep Sample Pack/Synths - One Shots/Cymatics - Mothership Bass One Shot 3 - E.wav'))

      # # SNARE #
      # 1: QSound(self.appctxt.get_resource('sounds/Drums - One Shots/Snares/Cymatics - Terror Heavy Snare 014.wav')),
      # 2: QSound(self.appctxt.get_resource('sounds/Drums - One Shots/Snares/Cymatics - Terror Heavy Snare 038.wav')),
      # 3: QSound(self.appctxt.get_resource('sounds/Drums - One Shots/Snares/Cymatics - Ultimate Snare 20 - D#.wav')),
      # 4: QSound(self.appctxt.get_resource('sounds/Drums - One Shots/Snares/Cymatics - Ultimate Snare 36 - G#.wav'))
    }

    return sounds

  # play sound effect
  def playSound(self, i):
    self.sounds[i].play()

  # EASY button pressed
  def SLOT_easyBtn(self):
    self.difficulty = "easy"
    self.easyBtn.setChecked(True)
    self.hardBtn.setChecked(False)

  # HARD button pressed
  def SLOT_hardBtn(self):
    self.difficulty = "hard"
    self.hardBtn.setChecked(True)
    self.easyBtn.setChecked(False)

  # critical dialog pop-up
  def SLOT_dialogCritical(self, s):
    dlg = QMessageBox(self)
    dlg.setText(s)
    dlg.setIcon(QMessageBox.Critical)
    dlg.show()

  # update main window title
  def updateTitle(self, str=""):
    self.setWindowTitle("SiMoN sAyS "+ str)

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    Window = MainWindow()
    exit_code = appctxt.app.exec_()      # 2. Invoke appctxt.app.exec_()
    sys.exit(exit_code)
