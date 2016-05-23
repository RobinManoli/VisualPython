from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

class FileMenu():
    """
    """
    def __init__(self, parent):
        self.parent = parent
        self.mainframe = parent
        self.root = parent.root
        
        self.init()


    def init(self):
        menubar = Menu(self.mainframe)
        self.root.config(menu=menubar)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open...", command=self.load)
        fileMenu.add_command(label="Save", command=self.write)
        fileMenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=fileMenu)

        self.root.bind_all('<Control-o>', self.load)

    def open(self, fname):
        self.mainframe.f = open(fname, 'r+')
        #print( self.mainframe.f )
        self.mainframe.textarea.delete(1.0, END)
        self.mainframe.textarea.insert(1.0, self.mainframe.f.read())
        self.mainframe.TextArea.changed()
        

    def write(self):
        # http://stackoverflow.com/questions/2424000/read-and-overwrite-a-file-in-python
        content = self.mainframe.textarea.get(1.0, 'end - 1c')
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