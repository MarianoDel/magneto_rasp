import wx
#import serial
import os
from operator import or_
from threading import Timer
import time

import sys
sys.path.append('/home/pi/Desktop/Magneto_simple_v1')
#from fileManagement import fileManagement


def GetIndicadorBitmap():
    return wx.BitmapFromImage(GetIndicadorImage())

def GetIndicadorImage():
    image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/TratamientoCorriendo/PowerIndicator.png", wx.BITMAP_TYPE_ANY)
    return image

class PowerShowFrame(wx.Panel): #(wx.PyPanel): #PyPanel also works
  def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, name="MyPanel"):
  #def __init__(self, parent, id=wx.ID_ANY, pos=(50,50), size=(50,450), style=0, name="MyPanel"):

    super(PowerShowFrame, self).__init__(parent, id, pos, size, style, name)
    self.SetBackgroundColour(wx.Colour(190,190, 190))

    self.Bind(wx.EVT_PAINT, self.OnPaint)

    #self.text2 = wx.StaticText(self, -1, "10", (90, 100))
    #self.text2 = wx.StaticText(self, -1, '100', (60, 100))
    self.text2 = wx.StaticText(self, -1, '', (120, 100))
    font = wx.Font(60, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    self.text2.SetFont(font)

  def OnPaint(self, event):
    #~ dc = wx.BufferedPaintDC(self) # works, somewhat
     # "Set a red brush to draw a rectangle"
     self.Draw()

  def Draw(self):
    dc = wx.PaintDC(self) # works
#    print(dc)
    bitmap = GetIndicadorBitmap()
    dc.DrawBitmap(bitmap, 5, 5, True)
#    self.Refresh() # recurses here!

  
  def SetPower (self, power):
    if power < 10:
      self.text2.SetPosition((120, 100))
    elif power < 100:
      self.text2.SetPosition((90, 100))
    else:
      self.text2.SetPosition((60, 100))


    self.text2.SetLabel("%d" % power)
