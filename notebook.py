from tkinter import *
from tkinter.ttk import Notebook
import editor

class NoteBook(Notebook):
    """
    http://www.tkdocs.com/tutorial/complex.html
    """
    def __init__(self, parent):
        Notebook.__init__(self, parent)
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root

        self.editors = []

    def new_tab(self, fpathname=''):
        if fpathname:
            fname = fpathname
            f = self.mainframe.filemenu.open( fpathname )
            
        else:
            fname = 'new'
            f = None
        ed = editor.Editor(self, fname, f)
        self.editors.append(ed)
        self.add(ed, text=fname)
        # switch to newly opened tab
        index = self.editors.index(ed)
        self.select(index)

    def current_editor(self):
        index = self.index( self.select() )
        return self.editors[index]
