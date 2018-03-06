import wx
import serial
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
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/Loading/loading1.png", wx.BITMAP_TYPE_ANY)
    elif image == 1:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/Loading/loading2.png", wx.BITMAP_TYPE_ANY)
    elif image == 2:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/Loading/loading3.png", wx.BITMAP_TYPE_ANY)
    elif image == 3:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/Loading/loading4.png", wx.BITMAP_TYPE_ANY)
    elif image == 4:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/Loading/loading5.png", wx.BITMAP_TYPE_ANY)
    elif image == 5:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/Loading/loading6.png", wx.BITMAP_TYPE_ANY)
    return image

class LoadFrame(wx.Panel): #(wx.PyPanel): #PyPanel also works
  def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, name="MyPanel"):
  #def __init__(self, parent, id=wx.ID_ANY, pos=(50,50), size=(50,450), style=0, name="MyPanel"):

    super(LoadFrame, self).__init__(parent, id, pos, size, style, name)
    self.SetBackgroundColour(wx.Colour(190,190, 190))

    #self.Bind(wx.EVT_SIZE, self.OnSize)
    self.Bind(wx.EVT_PAINT, self.OnPaint)
#    self.Bind(wx.EVT_LEFT_DOWN, self.OnClickDwn)
#    self.Bind(wx.EVT_LEFT_UP, self.OnClickUp)

    self.text = wx.StaticText(self, -1, "0%", (200, 210))
    font = wx.Font(60, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    font.SetPixelSize((150,150))
    self.text.SetFont(font)

    self.step = 0

  def OnPaint(self, event):
    #~ dc = wx.BufferedPaintDC(self) # works, somewhat
     # "Set a red brush to draw a rectangle"
     self.Draw()

  def Draw(self):
    dc = wx.PaintDC(self) # works
#    print(dc)
    bitmap = GetIndicadorBitmap(self.step)
    dc.DrawBitmap(bitmap, 5, 5, True)
    self.Refresh() # recurses here!

  def WriteLoadPercent (self, value):
    if value < 10:
      self.text.SetPosition((200, 210))
    elif value < 100:
      self.text.SetPosition((160, 210))
    else:
      self.text.SetPosition((120, 210))

    self.text.SetLabel("%d%%" % value)

  def StepLoad (self):
    if self.step == 0:
     self.WriteLoadPercent(8)
    elif self.step == 1:
      self.WriteLoadPercent(21)
    elif self.step == 2:
      self.WriteLoadPercent(53)
    elif self.step == 3:
      self.WriteLoadPercent(87)
    elif self.step == 4:
      self.WriteLoadPercent(100)

    if self.step < 5:
      self.step = self.step + 1


  
