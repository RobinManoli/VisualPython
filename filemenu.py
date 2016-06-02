try:
    from tkinter import *
    from tkinter.filedialog import askopenfilename, asksaveasfilename
    from tkinter.messagebox import askyesnocancel, askokcancel, showinfo
except:
    from Tkinter import *
    from tkFileDialog import askopenfilename, asksaveasfilename
    from tkMessageBox import askyesnocancel, askokcancel, showinfo

class FileMenu(Menu):
    """
    """
    def __init__(self, parent):
        Menu.__init__(self, parent, background="white")
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root
        
        self.add_command(label="New", command=self.new, accelerator="Ctrl+N")
        self.add_command(label="Open...", command=self.load, accelerator="Ctrl+O")
        self.add_command(label="Save", command=self.write, accelerator="Ctrl+S")
        self.add_command(label="Exit", command=self.root.quit)
        self.mainframe.menu.add_cascade(label="File", menu=self)

        self.root.bind_all('<Control-n>', self.new)
        self.root.bind_all('<Control-o>', self.load)
        self.root.bind_all('<Control-s>', self.write)

    def new(self, event=None):
        self.notebook.new_editor()

    def open(self, fname):
        return open(fname, 'r+')

    def write(self, event=None, editor=None):
        # http://stackoverflow.com/questions/2424000/read-and-overwrite-a-file-in-python
        if not editor:
            editor = self.notebook.current_editor()

        content = editor.textarea.get(1.0, 'end - 1c')
        editor.f.seek(0)
        editor.f.write(content)
        editor.f.truncate()
        #editor.f.close()
        editor.textarea.edit_modified(False)
        self.notebook.after_click(event)
        return "break"

    def load(self, event=None):
        fname = askopenfilename(filetypes=(
            ("All files", "*.*"),
            ("Python", "*.py"),
            ("HTML files", "*.html;*.htm"),
        ))
        if fname:
            self.notebook.new_editor(fname)
        return "break"


    def save(self, editor):
        if not editor.f:
            fpathname = asksaveasfilename()
            if not fpathname:
                # file not saved
                return False
            editor.open(fpathname)
        self.write(editor=editor)
        # file saved
        return True

    def prompt_save(self, editor):
        fname = editor.fpathname or editor.fname
        msg = "Save '%s' before closing?" % fname
        ans = askyesnocancel(message=msg)
        if ans:
            # return cancel if selected save and then not saved
            return True if self.save(editor) else None
        return ans
        

    def before_exit(self):
        for editor in self.notebook.editors:
            if editor.textarea.edit_modified():
                self.notebook.select( editor )
                if self.prompt_save(editor) is None:
                    # cancel pressed - close editor manually to discard changes
                    return
                # No returns False
        self.root.destroy()