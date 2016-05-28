from tkinter import *

class TextArea(Text):
    def __init__(self, parent):
        Text.__init__(self, parent, wrap=WORD, yscrollcommand=self.scrollYUpdate,
            padx=5, pady=5, undo=True, maxundo=-1, selectforeground='black',selectbackground="#ccccff")
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root
        
        self.init()

    def init(self):
        #self.bind('<<Modified>>', self.changed) # works only once
        self.bind('<KeyRelease>', self.on_key_release)
        self.bind('<Motion>', self.on_motion)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Return>', self.on_return)
        self.bind('<Tab>', self.on_tab)
        self.bind('<Shift-Tab>', self.on_shift_tab)
        self.bind('<ButtonRelease-1>', self.after_click)
        self.bind('<Double-Button-1>', self.on_dclick)
        
    def scrollY(self, action, position, type=None):
        self.yview_moveto(position)
        self.mainframe.LineTools.yview_moveto(position)

    def scrollYUpdate(self, first, last, type=None):
        # http://stackoverflow.com/a/37087317
        self.yview_moveto(first)
        self.mainframe.LineTools.yview_moveto(first)
        self.mainframe.scrollbarY.set(first, last)
        self.mainframe.HighLight.tokens('scrollYUpdate')

    def on_key_release(self, event=None):
        #print(repr(event.char))
        #if event and event.char == '\r': # example to detect keypress return during anykepress
        self.mainframe.LineTools.update_linenumbers(event)
        self.mainframe.HighLight.tokens(event)
        self.mainframe.HighLight.brackets(event)
        self.mainframe.HighLight.same(event)

    def on_motion(self, event=None):
        self.mainframe.HighLight.brackets(event)
        self.mainframe.HighLight.same(event)

    def on_leave(self, event=None):
        # hilight whitespace
        self.mainframe.HighLight.whitespace(event)

    def on_enter(self, event=None):
        # unhilight whitespace
        self.mainframe.HighLight.clear_whitespace()

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

        # find nearest above line with lesser indentation
        for i in range(line.n - 1, 1, -1):
            line2 = self.mainframe.texthelper.Line(self, i)
            if len(line.indent) < len(line2.indent):
                self.delete(line.start, line.start + '+ %dc' % len(line.indent))
                self.insert(line.start, line2.indent)
                #print( repr(line2.indent) )
                return "break"

    def on_shift_tab(self, event=None):
        "Remove indentation (same as above line with lesser)"
        line = self.mainframe.texthelper.Line(self)
        if line.indent:
            # find nearest above line with lesser indentation
            for i in range(line.n, 1, -1):
                line2 = self.mainframe.texthelper.Line(self, i)
                if len(line.indent) > len(line2.indent):
                    self.delete(line.start, line.start + '+ %dc' % len(line.indent))
                    self.insert(line.start, line2.indent)
                    #print( repr(line2.indent) )
                    break
        return "break"

    def after_click(self, event=None):
        self.mainframe.HighLight.same(event)

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
        self.mainframe.HighLight.clear_brackets()

        self.mainframe.HighLight.same(event)
        return "break"
        
