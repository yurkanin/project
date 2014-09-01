import fluidsynth
import serial
import string
import sys
import os
import time
import curses
class keytar:
   def __init__(self,s):
      self.s = s
      self.name = 'keytar'
      self.event = ''
      self.VOLUME = 0
      self.note = 0
      self.REGISTER = 57 
      self.blend = 0
      self.piano = fluidsynth.Synth()
      self.piano.start(driver='alsa')
      s.stdscr.addstr(12,3,str(os.listdir('/home/Justin/SF2'))+'\nChoose Instrument: ')
      self.font = s.stdscr.getstr(14,19,40)
      pianoid = self.piano.sfload('/home/Justin/SF2/'+self.font)
      self.piano.program_select(0, pianoid, 0, 0)
 
      data = (os.listdir('/dev')) 
      if(('ttyACM0' in data)): port = '/dev/ttyACM0'
      elif(('ttyACM1' in data)): port = '/dev/ttyACM1'
      elif(('ttyACM2' in data)): port = '/dev/ttyACM2'
      #else: port = '/dev/tty6'
      self.ATMEGA = serial.Serial(port, baudrate=9600)	#initalizes serial port
      if not(self.ATMEGA.isOpen()): return None
   def change(self):
      self.s.stdscr.timeout(1000000)
      self.font = self.s.stdscr.getstr(13,30,40)
      self.s.stdscr.timeout(1)
      self.piano.program_select(0, self.piano.sfload('/home/Justin/SF2/'+self.font),0, 0)
   def main(self):
      ATMEGA = self.ATMEGA
      freq = [87, 93, 98, 104, 110, 117, 123, 131, 139, 147, 156, 165, 175, 185, 196, 208, 220, 233, 247, 262, 277, 294, 311, 330, 349, 370, 392, 415, 440, 466, 494, 523, 554, 587, 622, 659, 698, 740, 784, 831, 880, 932, 988, 1047]
      note_states = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      OLDDATA = ''
      while 1: 
         DATA = ''
         REGISTER = self.REGISTER
         VOLUME = self.VOLUME
         while 1: 
            if ATMEGA.inWaiting()>0: break
            if(self.blend > 0)and(self.s.ch != 'e'): self.blend -= 1
            elif(self.blend < 0)and(self.s.ch != 'c'): self.blend += 1
            if(self.blend != 0): self.piano.pitch_bend(0, self.blend)
            time.sleep(.0001)            
         while 1:
            DATA += ATMEGA.read(1)
            if '\n' in DATA: break
         DATA = DATA.split('.')
         del DATA[-1]
         self.DATA = DATA
         self.OLDDATA = OLDDATA
         for x in DATA:
            if not(x in OLDDATA):
               self.note = freq.index(int(x))+REGISTER
               if(note_states[self.note] != 1):
                  self.event = 'noteon'+str(self.note)
                  self.piano.noteon(0, self.note, VOLUME)
                  note_states[self.note] = 1
               else:
                  self.event = ''
         for x in OLDDATA:
            if not(x in DATA):
               y = freq.index(int(x))+REGISTER
               if(note_states[y] != 0):
                  self.event = 'noteoff'+str(self.note)
                  note_states[y] = 0
                  self.piano.noteoff(0,freq.index(int(x))+REGISTER)  
               else:
                  self.event = ''
         OLDDATA = DATA

class mididevice:
   def __init__(self, name):
      from time import sleep
      from pygame import midi
      self.instrument = midi(name)
      self.name = 'midi'
   def main(self):
      while 1:
         sleep(.001)
         if(self.instrument.poll() == True):
            rx =  self.instrument.read()
            print rx

class Synthesizer:
   def __init__(self):
      #curses are already imported
      from threading import Thread
      self.time = time
      self.songpath = os.getcwd()+'/'+raw_input('Name of Your Song : ')
      os.mkdir(self.songpath)
      os.chdir(self.songpath)
      self.tracklist = []
      self.ch = ''
      self.songlist = []
      self.filename = ''
      self.track_number = 0
      self.is_recording = False
      self.soundfonts = str(os.listdir('/home/Justin/SF2')).replace(',', '\n      ')
      self.song = []			#self.song = [track1, track2, track3]
      self.stdscr = curses.initscr()
      self.stdscr.addstr(str(os.listdir('/dev')))
      self.stdscr.addstr(10,10, 'Which Device Will We Be Reading From?\n  : /dev/')
      name = '/dev/'+self.stdscr.getstr(11,9, 20)
      self.stdscr.addstr(12,9,name)
      #try:
      if('tty' in name): self.device = keytar(self)
      elif('midi' in name): self.device = mididevice(name)
      else: print 'Device Not Found; Check Your Typing You Illiterate Fuck.'
      #except:
      #return None
      self.screen()
      if(self.device.name == 'keytar'):
         th = Thread(target = self.device.main)
         th.daemon = True
         th.start()
      elif(self.device.name == 'midi'):
         th = Thread(target = self.device.main)
         th.daemon = True
         th.start()
      else: print 'what did you do??? This exception shoud have been caught already!!! ... uh? uh... *sweats nervously*'
      self.stdscr.clear()
      self.stdscr.timeout(1)
      self.stdscr.refresh()
      while 1:
         self.main()
   def screen(self):
      size = self.stdscr.getmaxyx()
      #self.stdscr.clear()
      self.stdscr.addstr(1,1, '='*(size[1]-2))
      self.stdscr.addstr(2,1, (' '*((size[1]/2)-10)) + 'Super Swaggy Software Synthesizer')
      self.stdscr.addstr(3,1, '='*(size[1]-2))
      self.stdscr.addstr(4,3, 'FluidSynth Variables {')
      self.stdscr.addstr(5,6, 'Sound Font : '+str(self.device.font))
      self.stdscr.addstr(5,32, '//<, >')
      self.stdscr.addstr(6,6, 'Velocity : '+str(self.device.VOLUME))
      self.stdscr.addstr(6,32, '//Q++, Z--')
      self.stdscr.addstr(7,6, 'Octave : '+str(self.device.REGISTER/12))
      self.stdscr.addstr(7,32, '//W++, X--')
      self.stdscr.addstr(8,6, 'Pitch_Blend : '+str(self.device.blend)+((5-len(str(self.device.blend)))*'0'))
      self.stdscr.addstr(8,32, '//E++, C--')
      self.stdscr.addstr(9,6, 'Last_Note : '+str(self.device.note))
      self.stdscr.addstr(10,6, 'Recording : ' + str(self.is_recording))
      self.stdscr.addstr(10,32,'R To Start/Stop')
      self.stdscr.addstr(11,6, 'Tracks : ' + str(self.tracklist))
      self.stdscr.addstr(11,32,'A Adds, D Deletes')
      self.stdscr.addstr(12,6,'SongList : ' + str(self.songlist))
      self.stdscr.addstr(13,6, 'Getch : ' + str(self.ch))
      self.stdscr.addstr(14,6, self.soundfonts)
   def main(self):
      ch = self.stdscr.getch()
      if(ch in range(0,256)): self.ch = ch = chr(ch)
      else: ch = ' '
      if(ch == '<'): self.device.change()
      elif(ch == '>'): self.device.change()
      elif(ch == 'q') and (self.device.VOLUME < 127): self.device.VOLUME += 1
      elif(ch == 'z') and (self.device.VOLUME > 1): self.device.VOLUME -= 1
      elif(ch == 'w') and (self.device.REGISTER < 73): self.device.REGISTER += 12
      elif(ch == 'x') and (self.device.REGISTER > 13): self.device.REGISTER -= 12
      elif(ch == 'e') and (self.device.blend < 4000): 
         self.device.blend += 256
         self.device.piano.pitch_bend(0, self.device.blend)
      elif(ch == 'c') and (self.device.blend > -4000): 
         self.device.blend -= 256
         self.device.piano.pitch_bend(0, self.device.blend)
      elif(ch == 'r') and not(self.is_recording): self.record_track()
      elif(ch == 'r') and (self.is_recording): self.is_recording = not(self.is_recording)
      elif(ch == 'p'): self.playback()
      elif(ch == 'a'): self.add_track()		#add track to song from recorded track
      elif(ch == 'd'): self.delete_track()
      self.screen()
      if(ch in '<>qzwxrpad'):
         self.stdscr.refresh()
         self.stdscr.clear()
   def record_track (self):
      from threading import Thread
      self.stdscr.refresh()
      self.stdscr.timeout(10000000)
      self.stdscr.addstr(29, 10, 'Track:')
      self.stdscr.refresh()
      name = self.stdscr.getstr(30)   #track name
      self.track_number = name
      if(self.track_number in self.tracklist): del self.tracklist[self.tracklist.index(name)]
      self.stdscr.timeout(1)
      self.tracklist.append(self.track_number)
      self.filename = 'track' + str(self.track_number)
      thread_record = Thread(target = self.recording_thread)
      thread_record.daemon = True
      thread_record.start()
   def recording_thread(self):
      file = open(self.filename+'.py', 'w')
      file.write('''def track(synth):\n   import time
''')
      from time import time
      start_time = time()
      now_time = time()
      self.is_recording = not(self.is_recording)
      self.stdscr.clear()
      self.screen()
      while (now_time - start_time) < 5:
         now_time = time()
         self.stdscr.addstr(9,30, 'Will Record In: ' + str(int(5-(now_time-start_time))))
         self.stdscr.refresh()
      self.stdscr.clear()
      self.stdscr.refresh()
      timer = time()
      oldevent = ''
      event = ''
      while 1:		 	#main recording loop
         event = self.device.event
         if('noteon' in event) and (oldevent != event):
            now_time = time()
            file.write('   time.sleep('+str(now_time-timer)+')\n')
            timer = now_time
            file.write('   synth.noteon(0,'+str(self.device.note)+','+str(self.device.VOLUME)+')\n')
         elif('noteoff' in event) and (oldevent != event):
            now_time = time()
            file.write('   time.sleep('+str(now_time-timer)+')\n')
            timer = now_time
            file.write('   synth.noteoff(0,'+str(self.device.note)+')\n')
         if(self.is_recording == 0): break
         oldevent = event
      file.write('   return 0')
      file.close()
      return None
   def playback(self):
      #start each track in a new thread with piano object as argument 
      #so as to have a new instance in each thread each with different soundfonts and stuff
      import importlib #this is for dynamic importing later
      from threading import Thread
      os.chdir(self.songpath)
      for filename in self.songlist:
         exec(open('track'+filename+'.py', 'r').read())
         x = Thread(target=track,  args=(self.device.piano,))
         x.daemon = True
         x.start()
      """list = [a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
      for thread in threadlist:
         list[threadlist.index(thread)] = Thread(target=thread, args=(self.device.piano,))   #import lib returns the track module. which is passed to the Thread method which returns thread which becomes a list item 
      for th in list:
         if(th != 0): 
            th.daemon = True
            th.start()"""            
   def add_track(self):
      self.stdscr.timeout(10000)
      self.stdscr.addstr(12,30, 'Add Track To Song: ')
      self.stdscr.refresh()
      track = self.stdscr.getstr(20)
      self.stdscr.timeout(1)
      if(track in self.tracklist): self.songlist.append(track)
   def delete_track(self):
      self.stdscr.addstr(12,30, 'Rm Track From Song: ')
      self.stdscr.timeout(100000)
      name  = self.stdscr.getstr(20)
      if(name in self.songlist):
         try: del self.songlist[self.songlist.index(name)]
         except: pass
      self.stdscr.timeout(1)
#try:
#s = Synthesizer()
#except File Exists:
   
try:
   s = Synthesizer()
except:
   try:
      mididevice.instrument.close()
   except: pass
   try:
      keytar.ATMEGA.close()
      keytar.piano.stop()
   except: pass
   curses.endwin()

