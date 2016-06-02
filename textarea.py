try:
    from tkinter import *
except:
    from Tkinter import *

class TextArea(Text):
    def __init__(self, parent):
        Text.__init__(self, parent, wrap=WORD, yscrollcommand=self.scrollYUpdate,
            padx=5, pady=5, undo=True, maxundo=-1, selectforeground='black',selectbackground="#ccccff")
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root
        self.scrollbarY = parent.scrollbarY
        self.texthelper = self.mainframe.texthelper
        
        self.bind('<<Modified>>', self.mainframe.notebook.after_click) # works only once, when .edit_modified() becomes True
        self.bind('<KeyRelease>', self.on_key_release)
        self.bind('<Motion>', self.on_motion)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Return>', self.on_return)
        self.bind('<Tab>', self.on_tab)
        self.bind('<Shift-Tab>', self.on_shift_tab)
        self.bind('<ButtonRelease-1>', self.after_click)
        self.bind('<Double-Button-1>', self.on_dclick)
        # bind triple click because otherwise dclick "break" returnage seems to untrigger default behaviour
        self.bind('<Triple-Button-1>', lambda event: True)
        self.bind('<Control-o>', self.mainframe.filemenu.load)
        self.bind('<Home>', self.on_home)

    def scrollY(self, action, position, type=None):
        self.yview_moveto(position)

    def scrollYUpdate(self, first, last, type=None):
        # http://stackoverflow.com/a/37087317
        self.yview_moveto(first)
        self.scrollbarY.set(first, last)
        self.highlight.tokens('scrollYUpdate')
        self.after(0, self.linenumbers.draw) # self.after makes this work on scroll (although delayed)

    def on_key_release(self, event=None):
        #if event:
        #    print(repr(event.char))
        #if event and event.char == '\r': # example to detect keypress return during anykepress
        self.highlight.tokens(event)
        self.highlight.brackets(event)
        self.highlight.same(event)
        self.after(0, self.linenumbers.draw) # self.after makes this work on program start

    def on_motion(self, event=None):
        self.highlight.brackets(event)
        self.highlight.same(event)

    def on_leave(self, event=None):
        # hilight whitespace
        self.highlight.whitespace(event)

    def on_enter(self, event=None):
        # unhilight whitespace
        self.highlight.clear_whitespace()

    def on_return(self, event=None):
        "Create indentation for new lines (same as above line)"
        line = self.mainframe.texthelper.Line(self)
        self.insert(INSERT, '\n' + line.indent)
        return "break"

    def on_tab(self, event=None):
        "Add indentation (same as nearest above line with more)"
        line = self.mainframe.texthelper.Line(self)
        if self.get(line.start, INSERT).lstrip():
            # normal tab if cursor not in leading indentation
            return
        self.insert(INSERT, '    ')
        return "break"

    def on_shift_tab(self, event=None):
        "Remove indentation (same as above line with lesser)"
        line = self.mainframe.texthelper.Line(self)
        if line.indent:
            self.delete(line.start, line.start + '+ 4c')
        return "break"

    def on_home(self, event=None):
        line = self.texthelper.Line(self)
        if line.column == len(line.indent):
            # INSERT is at end of indent, so do default move to beginning of line
            return
        # move to end of indent
        self.mark_set("insert", "%d.%d" % (line.n, len(line.indent)))
        return "break"

    def after_click(self, event=None):
        self.highlight.same(event)

    def on_dclick(self, event=None):
        char = self.get(INSERT, 'insert + 1c')
        if not char.strip():
            # handle double clicking whitespace normally
            return

        line = self.mainframe.texthelper.Line(self)
        n, start = self.index(INSERT).split('.')
        start = end = int(start)
        while line.text[start-1].isalnum() or line.text[start-1] == '_':
            start -= 1
        while len(line.text) > end and (line.text[end].isalnum() or line.text[end] == '_'):
            end += 1
        #print( end, repr(text[end]))

        self.tag_add(SEL, "%d.%d" % (line.n,start), "%d.%d" % (line.n,end))
        # hide hilighted brackets when dclick selecting text
        self.highlight.clear_brackets()

        self.highlight.same(event)
        return "break"
        
