import wx
#import serial
import os
from operator import or_
from threading import Timer
import time

import sys
sys.path.append('/home/pi/Desktop/Magneto_simple_v1')
#from fileManagement import fileManagement


def GetIndicadorBitmap(aux):
    return wx.BitmapFromImage(GetIndicadorImage(aux))

def GetIndicadorImage(aux):
    if aux == 3:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/TratamientoCorriendo/Cuadrada.png", wx.BITMAP_TYPE_ANY)
    else:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/TratamientoCorriendo/Triangular.png", wx.BITMAP_TYPE_ANY)    
    return image

class SignalShowFrame(wx.Panel): #(wx.PyPanel): #PyPanel also works
  def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, name="MyPanel"):
  #def __init__(self, parent, id=wx.ID_ANY, pos=(50,50), size=(50,450), style=0, name="MyPanel"):

    super(SignalShowFrame, self).__init__(parent, id, pos, size, style, name)
    self.SetBackgroundColour(wx.Colour(190,190, 190))

    self.Bind(wx.EVT_PAINT, self.OnPaint)

    self.Signal = 0


  def OnPaint(self, event):
    #~ dc = wx.BufferedPaintDC(self) # works, somewhat
     # "Set a red brush to draw a rectangle"
     self.Draw()

  def Draw(self):
    dc = wx.PaintDC(self) # works
#    print(dc)
    bitmap = GetIndicadorBitmap(self.Signal)
    dc.DrawBitmap(bitmap, 0, 0, True)
#    self.Refresh() # recurses here!

  def SetSignal(self, signal):
    self.Signal = signal
