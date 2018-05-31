import wx
import serial
import os
from operator import or_
import socket
import threading
#import string
from threading import Timer
import time
import math

import sys

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.OUT)
GPIO.output(21, False)

#Tiempos de Buzzer
# T = N x 100ms
tiempo_inicio = 5 
tiempo_fin_ok = 3
repeticiones_fin_ok = 3
tiempo_fin_error = 20

tiempo_OverCurrent = 2
repeticiones_OverCurrent = 5


#importar clases
sys.path.append('/home/pi/Desktop/Magneto_simple_v1')
#from fileManagement import fileManagement
#from slider import MyPanel
from upFrame import UpFrame
from startButton import StBtnFrame
from SelectParameter import SlParamFrame
from RemainingTime import RemainingFrame
from PowerSelected import PowerShowFrame
from SignalShow import SignalShowFrame
from FreqShow import FreqShowFrame
from pauseButton import PsBtnFrame
from stopButton import StpBtnFrame
from LoadTime import LoadFrame

treatment_duration = 15
treatment_power = 70

#from downFrame import DownFrame
#from keyboardPanel import *
#from serialCom import *

# tested on wxPython 2.8.11.0, Python 2.7.1+, Ubuntu 11.04
# http://stackoverflow.com/questions/2053268/side-effects-of-handling-evt-paint-event-in-wxpython
# http://stackoverflow.com/questions/25756896/drawing-to-panel-inside-of-frame-in-wxpython
# http://www.infinity77.net/pycon/tutorial/pyar/wxpython.html
# also, see: wx-2.8-gtk2-unicode/wx/lib/agw/buttonpanel.py
class MyFrame3(wx.Frame):
  def __init__(self, parent):
    wx.Frame.__init__(self, parent, -1, "GSTKv1")
    self.SetSize((1024, 768))

    self.Layout()

    self.SetBackgroundColour(wx.Colour(190,190, 190))

    #FullScreen
    #FullScreenTestPanel(self)
    top = self.GetTopLevelParent()
    top.OnFullScreen(1)

    self.padre = parent


#    self.Bind(wx.EVT_PAINT, self.OnPaint)

    #paneles
    self.LoadTimePanel = LoadFrame(self, pos=(212,80), size=(600,600), name="Rem")

    #Carga de parametros
    self.RemainingTime = self.padre.GetTime()
    self.power = self.padre.GetPower()
    self.Signal = self.padre.GetSignal()
    self.Freq = self.padre.GetFrequency()


    self.hour = math.floor(self.RemainingTime / 60)
    self.minute = self.RemainingTime - (60 * self.hour)

    self.timer2 = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.timeout, self.timer2)
    self.timer2.Start(700)

    #UART
    #possible timeout values:
    #    1. None: wait forever, block call
    #    2. 0: non-blocking mode, return immediately
    #    3. x, x is bigger than 0, float allowed, timeout block call

    self.ser = serial.Serial()
    #self.ser.port = "/dev/ttyUSB0"
    self.ser.port = "/dev/serial0"
    #self.ser.port = "/dev/ttyS2"
    self.ser.baudrate = 9600
    self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    self.ser.parity = serial.PARITY_NONE #set parity check: no parity
    self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    #self.ser.timeout = None          #block read
    self.ser.timeout = 0            #non-block read
    #self.ser.timeout = 2              #timeout block read
    self.ser.xonxoff = False     #disable software flow control
    self.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    self.ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
    self.ser.writeTimeout = 2     #timeout for write
 
    try:
      self.ser.open()
    except Exception, e:
      print "error open serial port: " + str(e)

#    self.ser.write("Hola!")

    self.step = 0

  def timeout (self, event):

    if self.step == 0:
      self.ser.write("duration,%02d,%02d,00,1\n" % (self.hour, self.minute))
      self.LoadTimePanel.StepLoad()
    elif self.step == 1:
      if (self.Signal + self.Freq) == 0: #T10Hz
        self.ser.write("signal,%03d,%03d,0000,0049,0001,0001,0049,0000,0000,1\n" % (self.power, self.power))      
      elif (self.Signal + self.Freq) == 1: #T30Hz
        self.ser.write("signal,%03d,%03d,0000,0016,0001,0001,0015,0000,0000,1\n" % (self.power, self.power))
      elif (self.Signal + self.Freq) == 2: #T60Hz
        self.ser.write("signal,%03d,%03d,0000,0007,0001,0001,0007,0000,0000,1\n" % (self.power, self.power))
      elif (self.Signal + self.Freq) == 3: #C10Hz
        self.ser.write("signal,%03d,%03d,0000,0001,0049,0001,0049,0000,0000,1\n" % (self.power, self.power))
      elif (self.Signal + self.Freq) == 4: #C30Hz
        self.ser.write("signal,%03d,%03d,0000,0001,0016,0001,0015,0000,0000,1\n" % (self.power, self.power))
      elif (self.Signal + self.Freq) == 5: #C60Hz
        self.ser.write("signal,%03d,%03d,0000,0001,0007,0001,0007,0000,0000,1\n" % (self.power, self.power))
      self.LoadTimePanel.StepLoad()
    elif self.step == 2:
      self.ser.write("state_of_stage,1,1\n")
      self.LoadTimePanel.StepLoad()
    elif self.step == 3:
      self.ser.write("save,01\n")
      self.LoadTimePanel.StepLoad()
    elif self.step == 14:
      self.ser.write("load,01\n")
      self.LoadTimePanel.StepLoad()
    elif self.step == 15:
      self.ser.close()
      frame3 = MyFrame2(self)
      frame3.Show()
      self.Close()
      self.timer2.Stop()
      self.LoadTimePanel.StepLoad()
    if self.step < 15:
      self.step = self.step + 1

#    self.LoadTimePanel.StepLoad()

  def OnFullScreen(self,event):
    self.ShowFullScreen(not self.IsFullScreen(),0)

  def GetPower(self):
    return self.power

  def GetTime(self):
    return self.RemainingTime

  def GetSignal(self):
    return self.Signal

  def GetFrequency(self):
    return self.Freq


#Ventana tratamiento corriendo
class MyFrame2(wx.Frame):
  def __init__(self, parent):
    wx.Frame.__init__(self, parent, -1, "GSTKv1")
    self.SetSize((1024, 768))

    self.Layout()

    self.SetBackgroundColour(wx.Colour(190,190, 190))

    #FullScreen
    #FullScreenTestPanel(self)
    top = self.GetTopLevelParent()
    top.OnFullScreen(1)

    self.padre = parent


#    self.Bind(wx.EVT_PAINT, self.OnPaint)

    #paneles
    self.RemainingTimePanel = RemainingFrame(self, pos=(90,60), size=(520,520), name="Rem")
    self.PowerShowPanel = PowerShowFrame(self, pos=(670,290), size=(280,280), name="Pow")
    self.SignalPanel = SignalShowFrame(self, pos=(660,5), size=(230,135), name="Sig")
    self.FreqPanel = FreqShowFrame(self, pos=(880,5), size=(135,135), name="Sig")
    self.PausePanel = PsBtnFrame(self, pos=(120,620), size=(382,113), name="Pause")
    self.StopPanel = StpBtnFrame(self, pos=(540,620), size=(382,113), name="Pause")

    self.timer5 = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.timeout2, self.timer5)
    self.timer5.Start(10)

    self.timer2 = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.timeout, self.timer2)
    self.timer2.Start(500)

    self.timer3 = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.timeout3, self.timer3)
    self.timer3.Start(100)

    #Timer Led
    self.timerLED = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.timeoutLED, self.timerLED)
    self.timerLED.Start(100) #ms

    self.timeLED_opt = 1 #LED Inicio
    self.timeLED_aux1 = 0 #Variable para efectos
    self.timeLED_aux2 = 0 #Variable para efectos

    #Carga de parametros
    self.RemainingTimePanel.SetTimer(self.padre.GetTime(),0)
    self.PowerShowPanel.SetPower(self.padre.GetPower())
    self.SignalPanel.SetSignal(self.padre.GetSignal())
    self.FreqPanel.SetFrequency(self.padre.GetFrequency())
    print self.padre.GetFrequency()

    #UART
    self.ser = serial.Serial()
    #self.ser.port = "/dev/ttyUSB0"
    self.ser.port = "/dev/serial0"
    #self.ser.port = "/dev/ttyS2"
    self.ser.baudrate = 9600
    self.ser.bytesize = serial.EIGHTBITS #number of bits per bytes
    self.ser.parity = serial.PARITY_NONE #set parity check: no parity
    self.ser.stopbits = serial.STOPBITS_ONE #number of stop bits
    #self.ser.timeout = None          #block read
    self.ser.timeout = 0            #non-block read
    #self.ser.timeout = 2              #timeout block read
    self.ser.xonxoff = False     #disable software flow control
    self.ser.rtscts = False     #disable hardware (RTS/CTS) flow control
    self.ser.dsrdtr = False       #disable hardware (DSR/DTR) flow control
    self.ser.writeTimeout = 2     #timeout for write

    try:
      self.ser.open()
    except Exception, e:
      print "error open serial port: " + str(e)

    self.ser.write("start,\n")

  def timeout2 (self, event):
    strUARTrx = ""
    while self.ser.inWaiting() > 0:
      sample_string = self.ser.read(1)
      # Add the line to the log text box
      if sample_string != '\r' and sample_string != '\n':
        #self.Log1text.AppendText(sample_string)
        strUARTrx = strUARTrx + sample_string
      elif sample_string == '\r':
	pass
      else:
        #if sample_string != '\n':
          #self.Log1text.AppendText(strUARTrx + '\n')
          #--- Analisis de lo recibido por UART ---#
        #self.ser.write(strUARTrx)

          #--- Fin ---#
        print strUARTrx
        if strUARTrx[0:4] == "STOP":
          self.RemainingTimePanel.SetStoppedByError()
          self.timeLED_opt = 3 #LED Error

        if strUARTrx[0:9] == "ERROR(0x5":
          self.RemainingTimePanel.SetStoppedByError()
          self.timeLED_opt = 5 #LED Error Over current
	  #Dialog message box
          dlg = wx.MessageDialog(None, "Over current error in channel "+ strUARTrx[9], "ERROR", wx.CENTRE | wx.OK | wx.ICON_EXCLAMATION)
          result = dlg.ShowModal()
          dlg.Destroy()
          #self.timeLED_opt = 5 #LED Error Over current
	
	strUARTrx = ""
    

  def timeout (self, event):
#    print self.Ind1Panel.getValue()
    self.RemainingTimePanel.RefreshRemainingTime()

  def timeoutLED (self, event):
    #GPIO.output(21, not GPIO.input(21))
    #0: Sin acciones.
    #1: Inicio de tratamiento
    #2: Tratamiento fin Ok
    #3: Tratamiento fin ERROR
    #4: Prueba intervalo timer
    #5: Over Current

    #tiempo_inicio = 5
    #tiempo_fin_ok = 3
    #repeticiones_fin_ok = 3
    #tiempo_fin_error = 20

    if self.timeLED_opt == 1:

      if self.timeLED_aux2 == 0:
        self.timeLED_aux2 = 1
        self.timeLED_aux1 = tiempo_inicio + 1

      if self.timeLED_aux1 > 0:
        self.timeLED_aux1 = self.timeLED_aux1 - 1
        GPIO.output(21, True)
      else:
        GPIO.output(21, False)
        self.timeLED_aux2 = 0
        self.timeLED_opt = 0

    elif self.timeLED_opt == 2:

      if self.timeLED_aux2 == 0:
        self.timeLED_aux2 = repeticiones_fin_ok
        self.timeLED_aux1 = (tiempo_fin_ok + 1) * 2

      if self.timeLED_aux1 > 5:
        self.timeLED_aux1 = self.timeLED_aux1 - 1
        GPIO.output(21, True)
      elif self.timeLED_aux1 > 0:
        self.timeLED_aux1 = self.timeLED_aux1 - 1
        GPIO.output(21, False)
      else:
	if self.timeLED_aux2 > 1:
  	  self.timeLED_aux2 = self.timeLED_aux2 - 1
          self.timeLED_aux1 = (tiempo_fin_ok + 1) * 2
	elif self.timeLED_aux2 == 1:
          GPIO.output(21, False)
          self.timeLED_aux2 = 0
          self.timeLED_opt = 0

    elif self.timeLED_opt == 3:
      if self.timeLED_aux2 == 0:
        self.timeLED_aux2 = 1
        self.timeLED_aux1 = tiempo_fin_error + 1 
      if self.timeLED_aux1 > 0:
        self.timeLED_aux1 = self.timeLED_aux1 - 1
        GPIO.output(21, True)
      else:
        GPIO.output(21, False)
        self.timeLED_aux2 = 0
        self.timeLED_opt = 0

    elif self.timeLED_opt == 4:
      GPIO.output(21, not GPIO.input(21))

    elif self.timeLED_opt == 5:

      #print "Over current\n"
      if self.timeLED_aux2 == 0:
        self.timeLED_aux2 = repeticiones_OverCurrent
        self.timeLED_aux1 = (tiempo_OverCurrent + 1) * 2

      if self.timeLED_aux1 > 5:
        self.timeLED_aux1 = self.timeLED_aux1 - 1
        GPIO.output(21, True)
      elif self.timeLED_aux1 > 0:
        self.timeLED_aux1 = self.timeLED_aux1 - 1
        GPIO.output(21, False)
      else:
        if self.timeLED_aux2 > 1:
          self.timeLED_aux2 = self.timeLED_aux2 - 1
          self.timeLED_aux1 = (tiempo_OverCurrent + 1) * 2
        elif self.timeLED_aux2 == 1:
          GPIO.output(21, False)
          self.timeLED_aux2 = 0
#          dlg = wx.MessageDialog(None, "Over current error in channel ", "ERROR", wx.CENTRE | wx.OK | wx.ICON_EXCLAMATION)
#          result = dlg.ShowModal()
#          dlg.Destroy()
          self.timeLED_opt = 0


    elif self.timeLED_opt == 0:
      GPIO.output(21, False)
    
  def timeout3 (self, event):
    self.RemainingTimePanel.SetPause(self.PausePanel.GetButtonFlag())


    #Stop treatment
    #0: Running
    #1: Treatment finished OK
    #2: Stop by ERROR
    if self.RemainingTimePanel.GetStoppedFlag() > 0:
       #self.RemainingTimePanel.ClearStoppedFlag()
       #modificacion MED 6-3-18 manda terminado ok por serie
       #self.ser.write("stop,\n")
       print "END TYPE"
       print self.RemainingTimePanel.GetStoppedFlag()
       if self.RemainingTimePanel.GetStoppedFlag() == 1:
           self.timeLED_opt = 2 #LED Fin OK
           self.ser.write("finish_ok,\n")
       if self.RemainingTimePanel.GetStoppedFlag() == 2:
           self.timeLED_opt = 3 #LED Fin by ERROR
           self.ser.write("stop,\n")
       self.RemainingTimePanel.ClearStoppedFlag()

    #Boton Pausa
    if self.PausePanel.GetPauseFlag() == 1:
       self.PausePanel.ClearPauseFlag()
       print  self.PausePanel.GetButtonFlag()
       if self.PausePanel.GetButtonFlag() == 1:
         self.ser.write("pause,1\n")
       else:
         self.ser.write("pause,0\n")


    #Boton Stop
    if self.StopPanel.GetButtonFlag() == 1:
        self.StopPanel.SetButtonFlag(0)
#        self.RemainingTimePanel.SetStoppedByError()
        self.timer2.Stop()
        self.timer3.Stop()
        self.timer5.Stop()
	self.timerLED.Stop()
        self.ser.write("stop,\n")
        self.ser.close()
        frame3 = MyFrame(None)
        frame3.Show()
        self.Close()     

  def OnFullScreen(self,event):
    self.ShowFullScreen(not self.IsFullScreen(),0)

#Ventana principal
def GetUpButtonBitmap(width, height):
    return wx.BitmapFromImage(GetUpButtonImage(width,height))

def GetUpButtonImage(width, height):
    image = wx.Image("/home/pi/Desktop/Magneto_simple_v1/Imagenes/Magneto.png", wx.BITMAP_TYPE_ANY)
    #return image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    return image

class MyFrame(wx.Frame):
  def __init__(self, parent):
    wx.Frame.__init__(self, parent, -1, "Custom dmx demo")
    self.SetSize((1024, 768))

    self.Layout()

    self.SetBackgroundColour(wx.Colour(190,190, 190))

    #Up Frame
    self.upPanel = UpFrame(self, pos=(0,0), size=(1024,150), name="Up")
    self.StartPanel = StBtnFrame(self, pos=(0,560), size=(1024,180), name="Up")
    self.Ind1Panel = SlParamFrame(self, pos=(80,200), size=(400,380), name="Up")
    text = wx.StaticText(self, -1, 'Duration (Minutes)', (150, 170))
    font = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    text.SetFont(font)
    self.Ind1Panel.setLimit(1,120,1,treatment_duration)
    self.Ind2Panel = SlParamFrame(self, pos=(540,200), size=(400, 380), name="Up")
    text = wx.StaticText(self, -1, 'Power (%)', (675, 170))
    font = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    text.SetFont(font)
    self.Ind2Panel.setLimit(10,100,10,treatment_power)    
    #FullScreen
    #FullScreenTestPanel(self)
    top = self.GetTopLevelParent()
    top.OnFullScreen(1)

    self.Bind(wx.EVT_PAINT, self.OnPaint)

    #self.text2 = wx.StaticText(self.Ind2Panel, -1, "10", (150, 100))
    self.text2 = wx.StaticText(self.Ind2Panel, -1, '', (120, 100))
    #self.text2 = wx.StaticText(self.Ind2Panel, -1, '1', (170, 100))
    font = wx.Font(60, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    self.text2.SetFont(font)

    #self.text1 = wx.StaticText(self.In1Panel, -1, '90', (150, 100))
    self.text1 = wx.StaticText(self.Ind1Panel, -1, '', (120,100))
    #self.text1 = wx.StaticText(self.Ind1Panel, -1, "0", (170, 100))
    font = wx.Font(60, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
    self.text1.SetFont(font)

    self.timer2 = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, self.timeout, self.timer2)
    self.timer2.Start(100)

  def timeout (self, event):
#    print self.Ind1Panel.getValue()

    #Actualizar indicadores
    if self.Ind1Panel.getValue() < 10:
        self.text1.SetPosition((170,100))
    elif self.Ind1Panel.getValue() < 100:
        self.text1.SetPosition((150,100))
    else:
	self.text1.SetPosition((120,100))

    if self.Ind2Panel.getValue() < 10:
        self.text2.SetPosition((170,100))
    elif self.Ind2Panel.getValue() < 100:
        self.text2.SetPosition((150,100))
    else:
        self.text2.SetPosition((120,100))

    self.text1.SetLabel("%d" %  self.Ind1Panel.getValue())
    #cambio color a rojo
    if (self.Ind2Panel.getValue() >= 70):
      self.text2.SetForegroundColour((255,0,0))
    else:
      self.text2.SetForegroundColour((0,0,0))
    self.text2.SetLabel("%d" %  self.Ind2Panel.getValue())

    #Start button
    if self.StartPanel.GetButtonFlag() == 1:
        self.StartPanel.SetButtonFlag(0)

	#Dialog message box
	#dlg = wx.MessageDialog(None, "Over current error in channel x", "ERROR", wx.CENTRE | wx.OK | wx.ICON_EXCLAMATION)
    	#result = dlg.ShowModal()
    	#dlg.Destroy()
    
        #self.param.SetAll(self.Ind2Panel.getValue(), self.Ind1Panel.getValue(), self.upPanel.GetSignal(), self.upPanel.GetFrequency())
       
	global treatment_duration	
	treatment_duration = self.Ind1Panel.getValue()

	global treatment_power 
	treatment_power = self.Ind2Panel.getValue()

#	print "ButtonStart"
        frame2 = MyFrame3(self)
        frame2.Show()
        self.Close()

  def GetPower(self):
    return self.Ind2Panel.getValue()
  
  def GetTime(self): 
    return self.Ind1Panel.getValue()

  def GetSignal(self):
    return self.upPanel.GetSignal()

  def GetFrequency(self):
    return self.upPanel.GetFrequency()

  def OnClick(self, event):
    print "Hola button"

  def OnPaint(self, event):
    #~ dc = wx.BufferedPaintDC(self) # works, somewhat
     # "Set a red brush to draw a rectangle"    
    # self.Draw()
     pass
  
  def Draw(self):
    dc = wx.PaintDC(self) # works
    print(dc)
    bitmap = GetUpButtonBitmap(60,60)
    dc.DrawBitmap(bitmap, 0, 0, True)

  def OnFullScreen(self,event):
    self.ShowFullScreen(not self.IsFullScreen(),0)


app = wx.App(0)
frame = MyFrame(None)
app.SetTopWindow(frame)
frame.Show()
app.MainLoop()
 
