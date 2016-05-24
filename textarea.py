from tkinter import *

class TextArea(Text):
    def __init__(self, parent):
        Text.__init__(self, parent, wrap=WORD, yscrollcommand=self.scrollYUpdate, padx=5, pady=5, undo=True, maxundo=-1)
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root
        
        self.init()

    def init(self):
        self.do_highlight_whitespace = False

        #linetools = Text(self.mainframe, state=DISABLED, yscrollcommand=self.scrollYUpdate, width=5, padx=5, pady=5, relief=FLAT)
        #linetools.pack(side=LEFT, fill=Y)
        #self.mainframe.LineTools = linetools

        #self.bind('<<Modified>>', self.changed) # works only once
        self.bind('<KeyRelease>', self.changed)
        self.bind('<Motion>', self.on_motion)
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)
        self.bind('<Return>', self.on_return)
        self.bind('<Tab>', self.on_tab)
        self.bind('<Shift-Tab>', self.on_shift_tab)

    def get_whitespace(self, text):
        "Finds and returns the whitespace of the beginning of text."
        whitespace = ''
        if text != text.lstrip():
            for c in text:
                if c.strip():
                    break
                whitespace += c
        return whitespace

    def getline_number(self, index=INSERT, widget=None):
        widget = widget or self
        index = widget.index(index)
        nline = int( index.split('.')[0] )
        return nline
        
    def getline_start_end(self, index=INSERT, widget=None):
        "Get the start and end indeces of retrieved line number."
        widget = widget or self
        nline = self.getline_number(index, widget)
        start = "%d.0" % nline
        end = "%d.0 - 1c" % (nline + 1)
        return start, end

    def getline(self, index=INSERT):
        "Get text content of line index. Index may be a tk text widget index or a line number."
        integer = 1
        if type(index) == type(integer):
            index = str(index) + '.0'
        start, end = self.getline_start_end(index)
        return self.get(start, end)
        
    def scrollY(self, action, position, type=None):
        self.yview_moveto(position)
        self.mainframe.LineTools.yview_moveto(position)

    def scrollYUpdate(self, first, last, type=None):
        # http://stackoverflow.com/a/37087317
        self.yview_moveto(first)
        self.mainframe.LineTools.yview_moveto(first)
        self.mainframe.scrollbarY.set(first, last)

    def changed(self, event=None):
        #print(repr(event.char))
        self.mainframe.LineTools.update_linenumbers(event)
        self.mainframe.highlight(event, forced=True)

    def on_motion(self, event=None):
        self.mainframe.HighLight.brackets(event)

    def on_leave(self, event=None):
        self.do_highlight_whitespace = True
        self.mainframe.highlight(event, forced=True)

    def on_enter(self, event=None):
        self.do_highlight_whitespace = False
        self.mainframe.highlight(event, forced=True)

    def on_return(self, event=None):
        "Create whitespace for new lines (same as above line)"
        line = self.getline()
        whitespace = self.get_whitespace(line)
        self.insert(INSERT, '\n' + whitespace)
        return "break"

    def on_tab(self, event=None):
        "Add whitespace (same as above line with more)"
        start, end = self.getline_start_end()
        if self.get(start, INSERT).lstrip():
            # normal tab if cursor not in leading whitespace
            return

        line = self.getline()
        whitespace = self.get_whitespace(line)
        nline = self.getline_number()
        # find nearest above line with lesser whitespace
        for i in range(nline + 1, self.getline_number('end - 1c')):
            line2 = self.getline(i)
            whitespace2 = self.get_whitespace(line2)
            if len(whitespace) < len(whitespace2):
                while not self.get(start, start + '+ 1c').lstrip():
                    self.delete(start, start + '+ 1c')
                self.insert(start, whitespace2)
                #print( repr(whitespace2) )
                return "break"

    def on_shift_tab(self, event=None):
        "Remove whitespace (same as above line with lesser)"
        line = self.getline()
        whitespace = self.get_whitespace(line)
        if whitespace:
            nline = self.getline_number()
            # find nearest above line with lesser whitespace
            for i in range(nline, 1, -1):
                line2 = self.getline(i)
                whitespace2 = self.get_whitespace(line2)
                if len(whitespace) > len(whitespace2):
                    start, end = self.getline_start_end()
                    while not self.get(start, start + '+ 1c').lstrip():
                        self.delete(start, start + '+ 1c')
                    self.insert(start, whitespace2)
                    #print( repr(whitespace2) )
                    break
        return "break"

