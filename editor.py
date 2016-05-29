from tkinter import *
import textarea
import linetools
import highlight

class Editor(Frame):
    def __init__(self, parent, fname, f):
        Frame.__init__(self, parent)
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root
        
        self.fname = fname
        self.f = f
        
        self.scrollbarY = Scrollbar(self)
        self.textarea = textarea.TextArea(self)
        self.linetools = linetools.LineTools(self, self.textarea)
        self.highlight = highlight.HighLight(self, self.textarea)

        self.linetools.pack(side=LEFT, fill=Y)
        self.textarea.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbarY.pack(side=RIGHT, fill=Y)
        self.scrollbarY.config(command=self.textarea.scrollY)

        #print( self.mainframe.f )
        #self.textarea.delete(1.0, END)
        if self.f:
            self.textarea.insert(1.0, f.read())
            self.textarea.on_key_release()
