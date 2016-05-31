"Helpers for tkinter's Text widget."

try:
    from tkinter import *
except:
    from Tkinter import *

def indent(text):
    "Finds and returns the indentation of the beginning of text."
    indent = ''
    if text != text.lstrip():
        for c in text:
            if c.strip():
                break
            indent += c
    return indent


def linenumber(widget, index=INSERT):
    index = widget.index(index)
    nline = int( index.split('.')[0] )
    return nline

def column(widget, index=INSERT):
    index = widget.index(index)
    col = int( index.split('.')[1] )
    return col    

def visible(widget, index):
    return bool( widget.bbox(index) )

def top_visible(widget):
    return widget.index('@0,0')

def bottom_visible(widget):
    height = widget.winfo_height()
    return widget.index( '@0,%d' % height )

class Line():
    def __init__(self, widget, index=INSERT):
        "Get text data of index. Index may be a tk text widget index or a line number."
        integer = 1
        if type(index) == type(integer):
            self.n = index
            self.column = 0
        else:
            self.n = linenumber(widget, index)
            self.column = column(widget, index)
        # todo: self.column
        self.start = "%d.0" % self.n
        self.end = "%d.end" % self.n
        self.text = widget.get(self.start, self.end)
        self.indent = indent(self.text)

def get_selection(widget):
    try:
        return widget.get(SEL_FIRST, SEL_LAST)
    except TclError:
        # there is no selection
        return ''
