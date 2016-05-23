from tkinter import *

class TextArea():
    def __init__(self, parent):
        self.parent = parent
        self.mainframe = parent
        self.root = parent.root
        
        self.init()

    def init(self):
        scrollbarY = Scrollbar(self.mainframe)
        scrollbarY.pack(side=RIGHT, fill=Y)
        scrollbarY.config(command=self.scrollY)
        self.mainframe.scrollbarY = scrollbarY

        self.do_highlight_whitespace = False

        linenumbers = Text(self.mainframe, state=DISABLED, yscrollcommand=self.scrollYUpdate, width=5, padx=5, pady=5, relief=FLAT)
        linenumbers.pack(side=LEFT, fill=Y)
        self.mainframe.linenumbers = linenumbers

        textarea = Text(self.mainframe, wrap=WORD, yscrollcommand=self.scrollYUpdate, padx=5, pady=5, undo=True, maxundo=-1)
        textarea.pack(side=LEFT, fill=BOTH, expand=True)
        #textarea.bind('<<Modified>>', self.changed) # works only once
        textarea.bind('<KeyRelease>', self.changed)
        textarea.bind('<Motion>', self.on_motion)
        textarea.bind('<Enter>', self.on_enter)
        textarea.bind('<Leave>', self.on_leave)
        textarea.bind('<Return>', self.on_return)
        textarea.bind('<Tab>', self.on_tab)
        textarea.bind('<Shift-Tab>', self.on_shift_tab)
        self.mainframe.textarea = textarea

    def get_whitespace(self, text):
        "Finds and returns the whitespace of the beginning of text."
        whitespace = ''
        if text != text.lstrip():
            for c in text:
                if c.strip():
                    break
                whitespace += c
        return whitespace

    def getline_number(self, index=INSERT):
        index = self.mainframe.textarea.index(index)
        nline = int( index.split('.')[0] )
        return nline
        
    def getline_start_end(self, index=INSERT):
        "Get the start and end indeces of retrieved line number."
        nline = self.getline_number(index)
        start = "%d.0" % nline
        end = "%d.0 - 1c" % (nline + 1)
        return start, end

    def getline(self, index=INSERT):
        "Get text content of line index. Index may be a tk text widget index or a line number."
        integer = 1
        if type(index) == type(integer):
            index = str(index) + '.0'
        start, end = self.getline_start_end(index)
        return self.mainframe.textarea.get(start, end)
        
    def scrollY(self, action, position, type=None):
        self.mainframe.textarea.yview_moveto(position)
        self.mainframe.linenumbers.yview_moveto(position)

    def scrollYUpdate(self, first, last, type=None):
        # http://stackoverflow.com/a/37087317
        self.mainframe.textarea.yview_moveto(first)
        self.mainframe.linenumbers.yview_moveto(first)
        self.mainframe.scrollbarY.set(first, last)

    def changed(self, event=None):
        #print(repr(event.char))
        self.update_linenumbers(event)
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
        self.mainframe.textarea.insert(INSERT, '\n' + whitespace)
        return "break"

    def on_tab(self, event=None):
        "Add whitespace (same as above line with more)"
        start, end = self.getline_start_end()
        if self.mainframe.textarea.get(start, INSERT).lstrip():
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
                while not self.mainframe.textarea.get(start, start + '+ 1c').lstrip():
                    self.mainframe.textarea.delete(start, start + '+ 1c')
                self.mainframe.textarea.insert(start, whitespace2)
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
                    while not self.mainframe.textarea.get(start, start + '+ 1c').lstrip():
                        self.mainframe.textarea.delete(start, start + '+ 1c')
                    self.mainframe.textarea.insert(start, whitespace2)
                    #print( repr(whitespace2) )
                    break
        return "break"

    def update_linenumbers(self, event=None):
        # get content, but don't include the last newline inserted by tkinter
        content = self.mainframe.textarea.get(1.0, "end-1c")
        linenumbers = ''
        width = self.mainframe.textarea.cget('width')
        for i, text in enumerate(content.split('\n')):
            linenumbers += str(i+1)
            linenumbers += '\n'
            bbox_first_char = self.mainframe.textarea.bbox("%d.0" % (i+1))
            bbox_last_char = self.mainframe.textarea.bbox("%d.0 - 1c" % (i+2))
            if bbox_first_char and bbox_last_char:
                wrapped_line_height = bbox_last_char[1] - bbox_first_char[1]
                unwrapped_line_height = bbox_first_char[3]
                # add one new line per visual line that actual line takes up
                linenumbers += '\n' * int(wrapped_line_height/unwrapped_line_height)
                # works except width doesn't mean actual width
                # linenumbers += '\n' * (1 + int(len(text)/width))
        # remove last addition (of loop) of new line
        linenumbers = linenumbers[:-1]

        # fix unwanted scrolling when inserting linenumbers
        sbstatus = self.mainframe.scrollbarY.get()
        self.mainframe.linenumbers.config(state=NORMAL)
        self.mainframe.linenumbers.delete(1.0, END)
        self.mainframe.linenumbers.insert(1.0, linenumbers)
        self.mainframe.linenumbers.config(state=DISABLED)
        # sbstatus can for some reason not be retrieved when auto-open files at start
        if len(sbstatus) == 2:
            sbfirst, sblast = sbstatus
            self.scrollYUpdate(sbfirst, sblast)
        