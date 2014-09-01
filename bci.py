#signal strength, attention, meditation, delta, theta, low alpha, high alpha, low beta, high beta, low gamma, high gamma
import pyqtgraph
import serial
import os
import string
import fluidsynth
piano = fluidsynth.Synth()
piano.start(driver='alsa')
pianoid = piano.sfload('/home/Justin/SF2/AJH_Piano.sf2')
piano.program_select(0, pianoid, 0, 0)
from time import sleep
data = (os.listdir('/dev'))
if(('ttyACM0' in data)): port = '/dev/ttyACM0'
elif(('ttyACM1' in data)): port = '/dev/ttyACM1'
elif(('ttyACM2' in data)): port = '/dev/ttyACM2'
atmega = serial.Serial(port, 9600)
plot = pyqtgraph.plot()
list = []
old_list = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
rx = ''
data = ''
y = 0
while 1:
   if(atmega.inWaiting()>0):
      rx = atmega.read(1)
      if(rx == '<'):
         y += 1
         while 1:
            rx = atmega.read(1)
            if(rx == '>'): break
            data += rx
         list = data.split(',')
         print list
         if(len(list) == 11):
            piano.noteon(0, list[1], 127)
            for x in range(3,11):
               plot.plot((y-1,y), (int(old_list[x]), int(list[x])), pen = x)
            pyqtgraph.QtGui.QApplication.processEvents()
            old_list = list
         data = ''
