#!/usr/bin/python3

import curses

#https://docs.python.org/3/howto/curses.html

#Terminals usually return special keys, such as the cursor keys or navigation keys such as Page Up and Home, as a multibyte escape sequence. While you could write your application to expect such sequences and process them accordingly, curses can do it for you, returning a special value such as curses.KEY_LEFT. To get curses to do the job, you’ll have to enable keypad mode.

#stdscr.keypad(True) #for special keys convert multi-byte sequence to string
#curses.noech() #turn off echo for getch and getstr()
#curses.cbreak() #react without waiting for enter


#when terminating:
   #curses.nocbreak()
   #scr.keypad(False)
   #curses.echo()
   #curses.endwin()

#scr = curses.initscr()
#scr.border(0/1)
#input = scr.getstr(y, x, max_str_len)

#curses.start_color()
#set color pair 1 to RED and WHITE
#curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
#scr.addstr(y, x, str_to_print, curses.color_pair(1))
#scr.addstr(y, x, str_to_print, curses.A_REVERSE)
#A_REVERSE, A_BLINK, A_BOLD, A_DIM, A_STANDOUT, A_UNDERLINE

#scr.refresh()
#scr.getkey() #converts to strings, special chars return stuff like KEY_UP
#scr.getch() #returns numeric


#(0, 0) upper-left corner of pad to display
#(5, 5) upper-left corner of window are to put pad
#(20, 70) lower-right corner of window area to be filled with pad
#pad.refresh(0, 0,  5, 5,   20, 70)

#curses.curs_set(0)

scr = curses.initscr()
curses.cbreak()
scr.keypad(True)

scr.border(1)
scr.addstr(5, 5, "HEllo", curses.A_STANDOUT)
scr.refresh()

x = scr.getch()
#curses.start_color()

#curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)
scr.addstr(0, 0, "RED ALERT!") #, curses.color_pair(1))
#curses.cbreak()

win = curses.newwin(10, 15, 0, 0)
win.addstr(0, 10, "HAHA")
win.refresh()
win.border(1)

pad = curses.newpad(100, 100)
#for y in range(0, 99):
#    for x in range(0, 99):
#        pad.addch(y,x, ord('a') + (x*x+y*y) % 26)
pad.border(2)

pad.addstr(10, 7, "Hello my name is cool")
pad.addstr(2, 2, "Hi")
pad.refresh(3, 3, 5, 5, 30, 30)

#x = win.getch()
#x = pad.getch()

#x = scr.getkey()
#scr.addstr(10, 10, x, )
#scr.getch()

def update_scr(serv_list):
   #myscr.addstr(12, 25, "Python curses in action!")
   i = 1
   for serv_name in serv_list:
      scr.addstr(i, 1, serv_name)
      i = i+1
   x = scr.getstr(5, 10, 15)
   scr.refresh()
   scr.getch()

lst = ['serv1', 'serv2']
#update_scr(lst)
#lst = ['blah', 'ha']
#update_scr(lst)

#x = scr.getstr(0, 1, 15)

curses.nocbreak()
scr.keypad(False)
curses.echo()
curses.endwin()

