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

        self.bind('<ButtonRelease-1>', self.after_click)

    def new_editor(self, fpathname=''):
        ed = editor.Editor(self, fpathname)
        self.editors.append(ed)
        self.add(ed)
        # switch to newly opened tab
        index = self.editors.index(ed)
        self.select(index)
        self.after_click()

    def current_editor(self):
        index = self.index( self.select() )
        return self.editors[index]

    def after_click(self, event=None):
        current = self.current_editor()
        for ed in self.editors:
            i = self.editors.index(ed)
            if current == ed:
                # fpathname exists only on saved files
                self.tab(i, text=ed.fpathname or ed.fname)
            else:
                self.tab(i, text=ed.fname)
