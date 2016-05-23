from tkinter import *

# todo: delete this comment  <html onload="calc(multiply(3,4),multiply(4,multiply(5,multi[2])))">

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
        textarea.bind('<Motion>', self.motion_textarea)
        textarea.bind('<Enter>', self.enter_textarea)
        textarea.bind('<Leave>', self.leave_textarea)
        self.mainframe.textarea = textarea

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

    def motion_textarea(self, event=None):
        self.mainframe.HighLight.brackets(event)

    def leave_textarea(self, event=None):
        self.do_highlight_whitespace = True
        self.mainframe.highlight(event, forced=True)


    def enter_textarea(self, event=None):
        self.do_highlight_whitespace = False
        self.mainframe.highlight(event, forced=True)


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
        