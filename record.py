import traceback
import string
import time
import curses

class log:
   def __init__(self):
      self.stdscr = curses.initscr()
      self.log = ''
      with open('log', 'r') as self.logfile:
         self.log = logfile.read()
      with open('dat', 'r') as self.dat:
         self.event_list = dat.read().split('\n')
      self.dat = open('dat', 'w')
      self.logfile = open('log', 'ap')
      print 'Welcome\n'
      self.user = raw_input('User: ')
      self.password = raw_input('Password: ')
      print 'Begining Console'
      while 1:
         ch = self.main() 
         if(ch == 'quit'):
            break
         elif(ch in ['r', 'record']): curses.endwin()
      curses.endwin()
      if(raw_input('Write Out Entries? y/n') == 'y'): self.logfile.write(self.log)
   def main(self):
      ch = raw_input('>')
      if(ch in ['r', 'record']): self.record()
      elif(ch in ['quit', 'q']): return 'quit'
      elif(ch in ['a', 'add_event', 'add']): self.add_event()
      elif(ch in ['d', 'del', 'delete', 'del_event']): self.del_event()
      elif(ch in ['e', 'encrypt']): self.encrypt()
      elif(ch == 'decrypt'): self.decrypt()
      return ch 
   def record(self):
      self.stdscr.clear()
      entry = '<{0}/{1}/{2}/{3}/{4}/{5}>:   '.format(str(time.localtime().tm_year), str(time.localtime().tm_mon), str(time.localtime().tm_mday), str(time.localtime().tm_hour), str(time.localtime().tm_min), str(time.localtime().tm_sec))+self.user+ '\nGeneral:\n'
      self.stdscr.addstr(1,1,entry)
      self.stdscr.refresh()
      self.log += (entry + self.stdscr.getstr(3,3,100000).replace('<', '(').replace('>', ')')+ '\n')
      x = 0 
      for event in self.event_list:
         x += 1
         stdscr.addstr(3+x, 3, event+ ':') 
         self.log += event + ': ' + stdscr.getstr(4+x, 6, 10000).replace('<', '(').replace('>', ')') + '\n'
      self.log += '\x04'		#end of transmission character
   def encrypt(self):
      pass
   def decrypt(self):
      pass
   def add_event(self):
      self.event_list.append(raw_input('Add Event: '))
   def del_event(self):
      name = raw_input('Del Event')
      if( name in self.event_list ): 
         del self.event_list[self.event_list.index(name)]
   def read_entries(self):
      name = raw_input('Time of Entry, y/m/d/h/m/s :')
      switch = 0
      text = ''
      timestamp = ''
      matches = ['']
      self.stdscr.clear()
      self.stdscr.refresh()
      
      for ch in self.log:		#parse for matching timestamps
         if(ch == '<'):
            switch = 1
            timestamp = ''
         elif(ch == '>'): 
            switch = 2
         if(switch == 2):
            if(ch == '\x04'):
               if(name in timestamp):
                  matches.append((timestamp, text))
               switch = 0
               text = ''
            else:
               text += ch
         elif(switch ==  1): timestamp += ch
      
      for x in range(0, len(matches)):
         self.stdscr.addstr(x+1, 1, str(x) + ' : ' + matches[x][0])
      self.stdscr.addstr(x+3, 1, 'Entry Number : ')
      which = self.stdscr.getstr(100000)
      try: int(which)
      except: return 0
      stdscr.clear()
      x = 0
      line = ''
      counter = 0
      scroll = 0
      decrement = 0
      display = ''
      msg_length = len(matches[which][1].split('\n'))-1 
      while 1:
         decrement = scroll
         counter = 0
         self.stdscr.clear()
         self.stdscr.addstr(1,1, matches[which+x][0])
         for z in matches[which+x][1]:
            line += z
            if(z == '\n') and (counter < 24) and (decrement == 0):
               display += line
               counter += 1
            elif(z == '\n') and (counter < 24) and (decrement != 0):
               decrement -= 1
            
         self.stdscr.addstr(3, 0, display)
         self.stdscr.refresh()
         ch = self.stdscr.getch()
         if((ch == 'a') and ((x+2)<len(matches))): x += 1
         elif((ch == 'd') and ((x-1)> 0)): x -= 1
         elif((ch == 's') and (scroll < msg_length)): scroll += 1
         elif((ch == 'w') and (scroll > 1)): scroll -= 1
         elif(ch == 'q'): return 0 
try:
   log = log()
except:
   curses.endwin()
   print traceback.format_exc()
