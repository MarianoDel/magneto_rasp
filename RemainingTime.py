import wx
#import serial
import os
from operator import or_
from threading import Timer
import time
import math

import sys
sys.path.append('/home/pi/Desktop/Magneto_simple_v1')
#from fileManagement import fileManagement


def GetIndicadorBitmap(image):
    return wx.BitmapFromImage(GetIndicadorImage(image))

def GetIndicadorImage(image):
    if image == 0:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/TratamientoCorriendo/Remaining_time.png", wx.BITMAP_TYPE_ANY)
    elif image == 1:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/TratamientoCorriendo/Remaining_time2.png", wx.BITMAP_TYPE_ANY)
    elif image == 2:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/TratamientoCorriendo/Remaining_time3.png", wx.BITMAP_TYPE_ANY)
    elif image == 3:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/TratamientoCorriendo/Remaining_time4.png", wx.BITMAP_TYPE_ANY)
    return image

class RemainingFrame(wx.Panel): #(wx.PyPanel): #PyPanel also works
  def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, name="MyPanel"):
  #def __init__(self, parent, id=wx.ID_ANY, pos=(50,50), size=(50,450), style=0, name="MyPanel"):

    super(RemainingFrame, self).__init__(parent, id, pos, size, style, name)
    self.SetBackgroundColour(wx.Colour(190,190, 190))

    #self.Bind(wx.EVT_SIZE, self.OnSize)
    self.Bind(wx.EVT_PAINT, self.OnPaint)
    self.Bind(wx.EVT_LEFT_DOWN, self.OnClickDwn)
    self.Bind(wx.EVT_LEFT_UP, self.OnClickUp)

    self.UpButton = 0
    self.DownButton = 0
    self.minutes = 0
    self.nameInd = ' '

#    text = wx.StaticText(self, -1, self.nameInd, (20, 5))
#    font = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
#    text.SetFont(font)

    self.valor = 0
    self.timer = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.timeout, self.timer)

    self.seconds = 0
    self.minutes = 0

    self.RemainingImage = 0
    self.ToggleImage = 0
    self.Image = 1


    self.textMin = wx.StaticText(self, -1, "", (130, 130))
    font = wx.Font(60, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
#    font.SetPixelSize((140,140))
    font.SetPixelSize((250,250))
    self.textMin.SetFont(font)

    self.remainingTime = 0
    self.finalSeconds = 0

    self.stoppedFlag = 0

  def OnClickDwn(self, event):
     pos = event.GetPosition()

  def up(self):
    if self.UpButton == 1:
      if (self.valor+self.step) < self.max:
        self.valor = self.valor + self.step
      else:
        self.valor = self.max

  def down(self):
    if self.DownButton == 1:
      if (self.valor-self.step) > self.min:
        self.valor = self.valor - self.step
      else:
        self.valor = self.min


  def timeout (self, event):
    self.up();
    self.down();
 
  def OnClickUp(self, event):
     self.DownButton = 0
     self.UpButton = 0
     self.timer.Stop()

  def OnPaint(self, event):
    #~ dc = wx.BufferedPaintDC(self) # works, somewhat
     # "Set a red brush to draw a rectangle"
     self.Draw()

  def Draw(self):
    dc = wx.PaintDC(self) # works
#    print(dc)
    bitmap = GetIndicadorBitmap(self.RemainingImage)
    dc.DrawBitmap(bitmap, 5, 5, True)
    self.Refresh() # recurses here!

  def RefreshRemainingTime(self):
    if self.RemainingImage < 2:
        if self.seconds + self.minutes > 0:
            if self.ToggleImage == 0:
                self.ToggleImage = 1
                self.RemainingImage = self.Image
            else:
                self.ToggleImage = 0
                self.RemainingImage = 0
        else:
            self.RemainingImage = 2
            self.stoppedFlag = 1
#	    print "paso1"
    
        self.Refresh()

#        if self.seconds > 0:
#            self.seconds = self.seconds - 1
#        else:
#            if self.minutes > 0:
#                self.minutes = self.minutes - 1
#                self.seconds = 59
 

        #print time.time() - self.remainingTime
        self.remainingTime = self.finalSeconds - time.time()
#        self.remainingTime = time.time()

#        print self.remainingTime
#        print self.finalSeconds
#        print " "
       

        if self.remainingTime > 0:   
            self.minutes = self.remainingTime/60
            self.seconds = self.remainingTime - math.floor(self.remainingTime/60) * 60
            self.RefreshTimer()    
        else:
	    self.minutes = 0
            self.seconds = 0
    elif self.RemainingImage == 3:
      #print self.finalSeconds
      #print self.remainingTime
      self.finalSeconds = time.time() + self.remainingTime

  def SetTimer (self, min, sec):
    self.finalSeconds = time.time() + (min * 60 + sec)
    print time.time()
    print self.finalSeconds
    self.minutes = min
    self.seconds = sec
    self.RefreshTimer()


  def RefreshTimer (self):
 
    if self.minutes < 1:
        self.textMin.SetPosition((130,130))
    elif self.minutes < 10:
        self.textMin.SetPosition((130,180))
    elif self.minutes < 100:
        self.textMin.SetPosition((90,180))
    else:
        self.textMin.SetPosition((50,180))

    if self.minutes < 1:
        font = wx.Font(60, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        font.SetPixelSize((250,250))
        self.textMin.SetFont(font)
        self.textMin.SetLabel("%02d" % (self.seconds))
    else:
        font = wx.Font(60, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        font.SetPixelSize((140,140))
        self.textMin.SetFont(font)
        self.textMin.SetLabel("%d:%02d" % (self.minutes, self.seconds))

  def SetPause (self, pause):
    if self.seconds + self.minutes > 0 and self.RemainingImage != 2:
        if pause == 1:
            self.RemainingImage = 3
        else:
            #self.finalSeconds = time.time() + self.remainingTime
            if self.ToggleImage == 0:
                self.RemainingImage = 0
            else:
                self.RemainingImage = self.Image

  def SetStoppedByError (self):
     self.RemainingImage = 2
     self.stoppedFlag = 2

  def GetStoppedFlag (self):  
#    print "paso2"
    return self.stoppedFlag
  
  def ClearStoppedFlag (self):
#    print "paso3"
    self.stoppedFlag = 0

