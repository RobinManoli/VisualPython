try:
    from tkinter import *
    from tkinter.filedialog import askopenfilename, asksaveasfilename
except:
    from Tkinter import *
    from tkFileDialog import askopenfilename, asksaveasfilename

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
        return open(fname, 'r+')

    def write(self, event=None):
        # http://stackoverflow.com/questions/2424000/read-and-overwrite-a-file-in-python
        editor = self.mainframe.notebook.current_editor()

        content = editor.textarea.get(1.0, 'end - 1c')
        editor.f.seek(0)
        editor.f.write(content)
        editor.f.truncate()
        #editor.f.close()
        editor.textarea.edit_modified(False)
        self.mainframe.notebook.after_click(event)
        return "break"

    def load(self, event=None):
        fname = askopenfilename(filetypes=(
            ("All files", "*.*"),
            ("Python", "*.py"),
            ("HTML files", "*.html;*.htm"),
        ))
        if fname:
            self.mainframe.notebook.new_editor(fname)
        return "break"


    def save(self):
        pass
