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
        self.mainframe.filemenu.notebook = self

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
        #print(self.select())
        try:
            index = self.index( self.select() )
            return self.editors[index]
        except TclError:
            # this might occur if notebook/editor is not initiated yet
            # perhaps since after_click happens on many occations
            pass

    def after_click(self, event=None):
        current = self.current_editor()
        for ed in self.editors:
            i = self.editors.index(ed)
            modified = ' *' if ed.textarea.edit_modified() else ''
            if current == ed:
                text = ed.fpathname or ed.fname
                # fpathname exists only on saved files
                self.tab(i, text=text + modified)
            else:
                self.tab(i, text=ed.fname + modified)
                
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
        # todo: trigger close on clicked tab, not active tab
        # todo: confirm close unsaved
        current_editor = self.NoteBook.current_editor()
        index = self.NoteBook.editors.index(current_editor)
        current_editor.destroy()
        self.NoteBook.editors.pop(index)
        


