import wx
#import serial
import os
from operator import or_


import sys
sys.path.append('/home/pi/Desktop/Magneto_simple_v1')
#from fileManagement import fileManagement

treatment_signal = 0
treatment_freq = 0

def GetUpFrameBitmap(signal):
    return wx.BitmapFromImage(GetUpFrameImage(signal))

def GetUpFrameImage(signal):

    if signal == 0:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/UpFrameImagenes/Triangular10Hz.png", wx.BITMAP_TYPE_ANY)
    elif signal == 1:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/UpFrameImagenes/Triangular30Hz.png", wx.BITMAP_TYPE_ANY)    
    elif signal == 2:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/UpFrameImagenes/Triangular60Hz.png", wx.BITMAP_TYPE_ANY)
    elif signal == 3:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/UpFrameImagenes/Cuadrada10Hz.png", wx.BITMAP_TYPE_ANY)
    elif signal == 4:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/UpFrameImagenes/Cuadrada30Hz.png", wx.BITMAP_TYPE_ANY)
    elif signal == 5:
        image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/UpFrameImagenes/Cuadrada60Hz.png", wx.BITMAP_TYPE_ANY)


    return image


class UpFrame(wx.Panel): #(wx.PyPanel): #PyPanel also works
  def __init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, name="MyPanel"):
  #def __init__(self, parent, id=wx.ID_ANY, pos=(50,50), size=(50,450), style=0, name="MyPanel"):

    super(UpFrame, self).__init__(parent, id, pos, size, style, name)
    self.SetBackgroundColour(wx.Colour(190,190, 190))

    #self.Bind(wx.EVT_SIZE, self.OnSize)
    self.Bind(wx.EVT_PAINT, self.OnPaint)
    self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)

    self.signal = treatment_signal
    self.frequency = treatment_freq

  def OnClick(self, event):
    pos = event.GetPosition()

#    print pos.y
#    print pos.x

    if pos.y > 20 and pos.y < 145:
        if pos.x > 20 and pos.x < 240:
            self.signal = 0

        if pos.x > 250 and pos.x < 470:
            self.signal = 3

        if pos.x > 635 and pos.x < 730:
            self.frequency = 0

        if pos.x > 760 and pos.x < 875:
            self.frequency = 1

        if pos.x > 890 and pos.x < 1000:
            self.frequency = 2

#    self.refresh()

  def OnPaint(self, event):
    #~ dc = wx.BufferedPaintDC(self) # works, somewhat
     # "Set a red brush to draw a rectangle"
     self.Draw()

  def Draw(self):
    dc = wx.PaintDC(self) # works
#    print(dc)

    bitmap = GetUpFrameBitmap(self.signal+self.frequency)
    dc.DrawBitmap(bitmap, 12, 20, True)

    self.Refresh() # recurses here!

  def Get_TreatmentSignal (self):
    
    global treatment_signal
    treatment_signal = self.signal

    global treatment_freq
    treatment_freq = self.frequency
	
    return self.signal+self.frequency

  def GetSignal (self):

    global treatment_signal
    treatment_signal = self.signal

    return self.signal

  def GetFrequency(self):

    global treatment_freq
    treatment_freq = self.frequency

    return self.frequency

