"Helpers for tkinter's Text widget."

from tkinter import *

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
        else:
            self.n = linenumber(widget, index)
        # todo: self.column
        self.start = "%d.0" % self.n
        self.end = "%d.end" % self.n
        self.text = widget.get(self.start, self.end)
        self.indent = indent(self.text)
