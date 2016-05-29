from tkinter import *
import textarea
import linetools

class Editor(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root
        
        self.textarea = textarea.TextArea(self)
        self.linetools = linetools.LineTools(self, self.textarea)

        self.linetools.pack(side=LEFT, fill=Y)
        self.textarea.pack(side=LEFT, fill=BOTH, expand=True)
        
        self.mainframe.TextArea = self.textarea

        
