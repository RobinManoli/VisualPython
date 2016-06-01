try:
    from tkinter import *
    from tkinter.ttk import Notebook
except:
    from Tkinter import *
    from ttk import Notebook
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
        self.bind('<Button-3>', self.on_rclick)
        
        self.menu = NoteBookMenu(self)

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
                
    def on_rclick(self, event=None):
        self.menu.post(event.x_root, event.y_root)

class NoteBookMenu(Menu):
    def __init__(self, NoteBook):
        self.NoteBook = NoteBook
        self.mainframe = NoteBook.mainframe
        self.root = NoteBook.root
        Menu.__init__(self, self.root, tearoff=0)

        self.add_command(label="Close", command=self.close, accelerator="Ctrl+F4")
        self.root.bind_all('<Control-F4>', self.close)
    
    def close(self, event=None):
        # todo: destroy Editor instance too (not just Frame)?
        # todo: confirm close unsaved
        self.NoteBook.current_editor().destroy()


