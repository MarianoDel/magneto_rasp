import wx
#import serial
import os
from operator import or_
from threading import Timer
import time

import sys
sys.path.append('/home/pi/Desktop/Magneto_simple_v1')
#from fileManagement import fileManagement


def GetUBBitmap(state):
    return wx.BitmapFromImage(GetUBImage(state))

def GetUBImage(state):
    if state == 0:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/SelectTreatmentImagenes/UpButton.png", wx.BITMAP_TYPE_ANY)
    else:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/SelectTreatmentImagenes/UpButton_pressed.png", wx.BITMAP_TYPE_ANY)
    return image

def GetDBBitmap(state):
    return wx.BitmapFromImage(GetDBImage(state))

def GetDBImage(state):
    if state == 0:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/SelectTreatmentImagenes/DownButton.png", wx.BITMAP_TYPE_ANY)
    else:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/SelectTreatmentImagenes/DownButton_pressed.png", wx.BITMAP_TYPE_ANY)
    return image

def GetIndicadorBitmap():
    return wx.BitmapFromImage(GetIndicadorImage())

def GetIndicadorImage():
    image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/SelectTreatmentImagenes/Indicador.png", wx.BITMAP_TYPE_ANY)
    return image

class SlParamFrame(wx.Panel): #(wx.PyPanel): #PyPanel also works
  def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, name="MyPanel"):
  #def __init__(self, parent, id=wx.ID_ANY, pos=(50,50), size=(50,450), style=0, name="MyPanel"):

    super(SlParamFrame, self).__init__(parent, id, pos, size, style, name)
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

    self.TurboCounter = 0

  def OnClickDwn(self, event):
     pos = event.GetPosition()

     if pos.y > 220 and pos.y < 380 and pos.x > 0 and pos.x < 130:
         self.UpButton = 1
         self.up()
	 self.timer.Start(60)

     elif pos.y > 220 and pos.y < 380 and pos.x > 270 and pos.x < 400:
         self.DownButton = 1
	 self.down()
         self.timer.Start(60)
     #pass     

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
    if self.TurboCounter > 5:
        self.up();
        self.down();
    else:
        self.TurboCounter = self.TurboCounter + 1

 
  def OnClickUp(self, event):
     self.DownButton = 0
     self.UpButton = 0
     self.timer.Stop()
     self.TurboCounter=0

  def OnPaint(self, event):
    #~ dc = wx.BufferedPaintDC(self) # works, somewhat
     # "Set a red brush to draw a rectangle"
     self.Draw()

  def Draw(self):
    dc = wx.PaintDC(self) # works
#    print(dc)

    bitmap = GetIndicadorBitmap()
    dc.DrawBitmap(bitmap, 60, 10, True)
    bitmap = GetUBBitmap(self.UpButton)
    dc.DrawBitmap(bitmap, 10, 230, True)
    bitmap = GetDBBitmap(self.DownButton)
    dc.DrawBitmap(bitmap, 270, 230, True)

#    text = wx.StaticText(self, -1, self.nameInd, (20, 5))
#    font = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
#    text.SetFont(font)

    self.Refresh() # recurses here!

  def Get_TreatmentSignal (self):
    return self.signal+self.frequency

  def setName (self, nameInd):
    self.nameInd = nameInd 
  
  def setLimit (self, min, max, step, inicial):
    self.min = min
    self.max = max
    self.step = step
    self.valor = inicial

  def getValue (self):
    return self.valor
