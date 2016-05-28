from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

class FileMenu(Menu):
    """
    """
    def __init__(self, parent):
        Menu.__init__(self, parent, background="white")
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root
        
        self.init()


    def init(self):
        self.add_command(label="Open...", command=self.load, accelerator="Ctrl+O")
        self.add_command(label="Save", command=self.write, accelerator="Ctrl+S")
        self.add_command(label="Exit", command=self.root.quit)
        self.mainframe.menu.add_cascade(label="File", menu=self)

        self.root.bind_all('<Control-o>', self.load)
        self.root.bind_all('<Control-s>', self.write)

    def open(self, fname):
        self.mainframe.f = open(fname, 'r+')
        #print( self.mainframe.f )
        self.mainframe.TextArea.delete(1.0, END)
        self.mainframe.TextArea.insert(1.0, self.mainframe.f.read())
        self.mainframe.TextArea.on_key_release()
        

    def write(self):
        # http://stackoverflow.com/questions/2424000/read-and-overwrite-a-file-in-python
        content = self.mainframe.TextArea.get(1.0, 'end - 1c')
        self.mainframe.f.seek(0)
        self.mainframe.f.write(content)
        self.mainframe.f.truncate()
        #self.mainframe.f.close()

    def load(self, event=None):
        fname = askopenfilename(filetypes=(
            ("All files", "*.*"),
            ("Python", "*.py"),
            ("HTML files", "*.html;*.htm"),
        ))
        if fname:
            self.open(fname)


    def save(self):
        pass