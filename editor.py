try:
    from tkinter import *
except:
    from Tkinter import *
import textarea
import linenumbers
import highlight

class Editor(Frame):
    def __init__(self, parent, fpathname):
        Frame.__init__(self, parent)
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root

        self.open(fpathname)
        from os import path
        self.fname = path.basename(fpathname) if fpathname else 'new'
        self.scrollbarY = Scrollbar(self)
        self.textarea = textarea.TextArea(self)
        self.linenumbers = linenumbers.LineNumbers(self, self.textarea)
        self.highlight = highlight.HighLight(self, self.textarea)

        self.linenumbers.pack(side=LEFT, fill=Y)
        self.textarea.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbarY.pack(side=RIGHT, fill=Y)
        self.scrollbarY.config(command=self.textarea.scrollY)

        #self.bind('<Button-3>', self.on_rclick)

        #print( self.mainframe.f )
        #self.textarea.delete(1.0, END)
        if self.f:
            self.textarea.insert(1.0, self.f.read())
            # set textarea to not modified after original insertion
            self.textarea.edit_modified(False)
            # clear the undo stack not to be able to undo to empty textarea
            self.textarea.edit_reset()
            self.textarea.on_key_release()

    def open(self, fpathname):
        self.f = self.mainframe.filemenu.open( fpathname ) if fpathname else None
        self.fpathname = fpathname
