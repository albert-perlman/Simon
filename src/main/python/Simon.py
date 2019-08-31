from PyQt5.QtCore import *

import random

# Simon Says back-end thread: handles game logic and emits signals to update GUI
#______________________________________________________________________________________________
class SimonSays(QThread):

  # signals slotted to main thread
  flash         = pyqtSignal(int, int, QSemaphore)  # flash button ( button , time(ms), semaphore )
  delay         = pyqtSignal(int, QSemaphore)       # run delay timer ( time(ms), semaphore )
  sound         = pyqtSignal(int)                   # play sound
  revert        = pyqtSignal(int)                   # revert game button style to normal
  setStatus     = pyqtSignal(str)                   # update status bar message
  setMsgBar     = pyqtSignal(str)                   # update MsgBar text
  setWinTitle   = pyqtSignal(str)                   # update main window title
  btnEnable     = pyqtSignal(bool)                  # enable / disable game buttons

  def __init__(self, difficulty, parent=None):
    super(SimonSays, self).__init__(parent)

    self.sem        = QSemaphore() # semaphore used for blocking thread during GUI updates in main thread
    self.difficulty = difficulty
    self.roundNum   = 0            # round number
    self.pattern    = []           # Simon's pattern
    self.usrInput   = []           # user's input pattern
    self.valid      = True         # user's input pattern valid
      
  def run(self):

    self.setMsgBar.emit("Starting new game . . .")
    self.runStartupFlash()

    while (self.valid):

      self.roundNum += 1

      ### Simon's turn ########################################################
      self.btnEnable.emit(False)
      self.setMsgBar.emit("Round " + str(self.roundNum) + ": Simon's turn")
      self.setWinTitle.emit(" - Round " + str(self.roundNum))

      # delay
      self.delay.emit(1500, self.sem)
      self.sem.acquire()

      # generate Simon's pattern for the round and flash it onto GUI
      self.patternGen()
      self.patternFlash()
      #########################################################################

      ### user's turn #########################################################
      self.usrInput.clear()
      self.btnEnable.emit(True)
      self.setMsgBar.emit("Round " + str(self.roundNum) + ": Your turn")

      # wait for user to input a pattern
      while (len(self.usrInput) < self.roundNum):
        if (not self.valid): break
        self.delay.emit(1, self.sem)
        self.sem.acquire()
      #########################################################################

      # Round CLEARED
      if (self.valid):
        self.setMsgBar.emit("Round " + str(self.roundNum) + ": CLEARED")
        self.delay.emit(1500, self.sem)
        self.sem.acquire()      

    # GAME OVER
    self.pattern.clear()
    self.setMsgBar.emit("Round " + str(self.roundNum) + ": GAME OVER")
    self.runStartupFlash()
    self.quit()

  # generate Simon's pattern for the round
  def patternGen(self):
    if self.difficulty == "easy":
      self.pattern.append(random.randint(1,4))
    
    elif self.difficulty == "hard":
      self.pattern.clear()
      for i in range(self.roundNum):
        self.pattern.append(random.randint(1,4))

  # flash Simon's pattern for the round
  def patternFlash(self):
    for i in range(len(self.pattern)):
      self.flash.emit(self.pattern[i], 500, self.sem)
      self.sem.acquire()
      self.delay.emit(500, self.sem)
      self.revert.emit(0)
      self.sem.acquire()

  # run new game startup flash sequence
  def runStartupFlash(self, ms=75):

    for i in range(3):
      self.flash.emit(1, ms, self.sem)
      self.sem.acquire()
      self.flash.emit(2, ms, self.sem)
      self.sem.acquire()
      self.flash.emit(4, ms, self.sem)
      self.sem.acquire()
      self.flash.emit(3, ms, self.sem)
      self.sem.acquire()
      self.revert.emit(0)

  #_________________________________
  # SLOTs for game buttons' signals
  #_________________________________
  def SLOT_btn1Clicked(self):

    self.usrInput.append(1)
    try:

      if (self.usrInput[-1] == self.pattern[len(self.usrInput)-1]):
        self.valid = True
      else:
        self.valid = False

    except Exception as e:
      pass

  def SLOT_btn2Clicked(self):

    self.usrInput.append(2)
    try:

      if (self.usrInput[-1] == self.pattern[len(self.usrInput)-1]):
        self.valid = True
      else:
        self.valid = False

    except Exception as e:
      pass

  def SLOT_btn3Clicked(self):

    self.usrInput.append(3)
    try:

      if (self.usrInput[-1] == self.pattern[len(self.usrInput)-1]):
        self.valid = True
      else:
        self.valid = False

    except Exception as e:
      pass

  def SLOT_btn4Clicked(self):

    self.usrInput.append(4)
    try:

      if (self.usrInput[-1] == self.pattern[len(self.usrInput)-1]):
        self.valid = True
      else:
        self.valid = False

    except Exception as e:
      pass                
  #_________________________________
