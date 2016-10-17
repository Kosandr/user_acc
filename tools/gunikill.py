#!/usr/bin/python3

import pexpect, curses

scr = None

def init_curses():
   global scr
   scr = curses.initscr()
   curses.curs_set(0)
   curses.cbreak()
   scr.keypad(True)
   curses.start_color()

def shutdown(end_win=True):
   global scr
   curses.nocbreak()
   scr.keypad(False)
   curses.echo()
   if end_win:
      curses.endwin()

def curses_try(f, *args, **kwargs):
   try:
      f(*args, **kwargs)
   except Exception as e:
      shutdown(False)
      scr.addstr(0, 0, "Error occured:" + str(e))
      scr.getch()
      shutdown()


SERVER_LST_HEIGHT = 55
SERVER_LST_WIDTH = 30

def main():
   curses_try(init_curses)
   #scr.border(1)
   #fdsf uncomment to test error recovery

   pad_top = curses.newpad(3, 80)
   pad_top.border(0)
   pad_top.refresh(0, 0, 1, 1, 3, 90)

   #vertical
   pad1 = curses.newpad(SERVER_LST_HEIGHT, SERVER_LST_WIDTH)
   pad1.border(0)

   #horizontal
   pad2 = curses.newpad(20, 50)
   pad2.border(0)

   def draw_server_list(pad, lst):
      i = 1
      for serv_name in lst:
         empty_left = SERVER_LST_WIDTH - len(serv_name)
         extra_str = ''
         for x in range(2, empty_left):
            extra_str += ' '
         serv_name += extra_str

         pad.addstr(i, 1, serv_name, curses.A_STANDOUT)
         i += 1
      pad.refresh(0, 0, 1, 1, 65, 35)

   draw_server_list(pad1, ['hello          ', 'world          '])

   x = pad_top.getkey()
   if x == 'x':
      scr.refresh()
      pad2.refresh(0, 0, 1, 1, 30, 30)

   pad_top.getkey()

   #init_curses()
   shutdown()

   #pexpect.run('ls -l')
   #p = pexpect.spawn('ls -l')

   #p.expect('kkostya')
   #print(p.before)
   #p.expect(pexpect.EOF)
   #print(p.before)


if __name__ == "__main__":
   curses_try(main)

