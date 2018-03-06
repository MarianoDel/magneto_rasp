import wx
#import serial
import os
from operator import or_


import sys
sys.path.append('/home/pi/Desktop/Magneto_simple_v1')
#from fileManagement import fileManagement


def GetSTBBitmap(state):
    return wx.BitmapFromImage(GetSTBImage(state))

def GetSTBImage(state):
    if state == 0:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/TratamientoCorriendo/Parar1.png", wx.BITMAP_TYPE_ANY)
    else:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/TratamientoCorriendo/Parar2.png", wx.BITMAP_TYPE_ANY)
    return image



class StpBtnFrame(wx.Panel): #(wx.PyPanel): #PyPanel also works
  def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, name="MyPanel"):
  #def __init__(self, parent, id=wx.ID_ANY, pos=(50,50), size=(50,450), style=0, name="MyPanel"):

    super(StpBtnFrame, self).__init__(parent, id, pos, size, style, name)
    self.SetBackgroundColour(wx.Colour(190,190, 190))

    #self.Bind(wx.EVT_SIZE, self.OnSize)
    self.Bind(wx.EVT_PAINT, self.OnPaint)
    self.Bind(wx.EVT_LEFT_DOWN, self.OnClickDwn)
    self.Bind(wx.EVT_LEFT_UP, self.OnClickUp)

    self.button = 0
    self.buttonFlag = 0

  def OnClickDwn(self, event):
     self.button = 1
#    self.refresh()

  def OnClickUp(self, event):
     self.button = 0
     self.buttonFlag = 1

  def OnPaint(self, event):
    #~ dc = wx.BufferedPaintDC(self) # works, somewhat
     # "Set a red brush to draw a rectangle"
     self.Draw()

  def Draw(self):
    dc = wx.PaintDC(self) # works
#    print(dc)

    bitmap = GetSTBBitmap(self.button)
    dc.DrawBitmap(bitmap, 0, 0, True)

    self.Refresh() # recurses here!

  def GetButtonFlag (self):
    return self.buttonFlag

  def SetButtonFlag (self, flag):
    self.buttonFlag = flag

