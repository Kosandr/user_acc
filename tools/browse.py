#!/usr/bin/python3

import curses, requests
#from HTMLParser import HTMLParser
from html.parser import HTMLParser

url = 'https://forty7.guru/tmp/mybrowsertest.html' #'https://google.com'

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

def cclean(function, *args, **kwargs):
   def wrapper(*args, **kwargs):
      try:
         return function(*args, **kwargs)
      except Exception as e:
         shutdown(False)
         scr.addstr(0, 0, "Error occured:" + str(e))
         scr.getch()
         shutdown()


class Lex(object):
   O = 0
   C = 1
   B = 2
   def __init__(self, tag_type, attrs=None):
      self.tag_type = tag_type
      self.attrs = attrs


class Lexer(HTMLParser):
   def __init__(self):
      super(MyHTMLParser, self).__init__()
      self.tags = []

   def handle_starttag(self, tag, attrs):
      self.tags.append(Lex(Lex.O, attrs))
   def handle_endtag(self, tag):
      self.tags.append(Lex(Lex.C, attrs))
   def handle_data(self, data):
      self.tags.append(Lex(Lex.B, attrs))

class OldHTMLParser(HTMLParser):
   def handle_starttag(self, tag, attrs):
      print("<%s %s>" % (tag, attrs))
   def handle_endtag(self, tag):
      print("</%s>" % tag)
   def handle_data(self, data):
      print(data)

''' //for every new tag it encounters, adds it to dictionary with count. when count reaches 0, adds new one to tree
self.tags = {
   'h1': [(body, attrs), (body, attrs), (body, attrs)], //3
   'h2':[], //0
   'div': [(body, attrs), (body, attrs)], //2
}
'''
class Parser(HTMLParser):
   def __init__(self):
      super(MyHTMLParser, self).__init__()
      self.tags = {}

   def handle_starttag(self, tag, attrs):
      if tag not in self.tags:
         #tlen = len(self.tags[tag])
         self.tags[tag] = 1
      else:
         self.tags[tag] += 1

   def handle_endtag(self, tag):
      if tag in self.tags:
         t = self.tags[tag]
         if len(t) == 0:
            return self.tags #assuming we recursive but not so
      else:
         print("error: tag isn't in subtags")

   def handle_data(self, data):
      self.tags.append(Lex(Lex.B, attrs))


def parse_html(html):
   #html = MyHTMLParser()
   lexer = Lexer()
   lexer.feed(code)

   lex = lexer.tags


r = requests.get(url)
code = r.text
parse_html(code)


