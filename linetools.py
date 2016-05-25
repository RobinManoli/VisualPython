from tkinter import *

class LineTools(Text):
    """
    """
    def __init__(self, parent):
        Text.__init__(self, parent, state=DISABLED, wrap=NONE, yscrollcommand=parent.mainframe.TextArea.scrollYUpdate, width=5, padx=5, pady=5, relief=FLAT)
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root

        self.last_motion_index = ''

        self.init()

    def init(self):
        self.bind('<Motion>', self.on_motion)
        self.bind('<Double-Button-1>', self.on_dclick)

    def on_motion(self, event=None):
        index = self.index(CURRENT)
        line = self.mainframe.texthelper.Line(self, index)
        if not line.text.strip():
            return

        if index != self.last_motion_index:
            self.config(state=NORMAL)
            if self.last_motion_index:
                # delete # chars from last motion
                nline0 = self.mainframe.texthelper.linenumber(self, self.last_motion_index)
                self.delete('%d.end - 7c' % nline0, '%d.end' % nline0)
            # add # chars at end of current line's motion
            self.insert(line.end, ' ######')
            self.config(state=DISABLED)
            self.last_motion_index = index

    def on_dclick(self, event=None):
        toolline = self.mainframe.texthelper.Line(self, CURRENT)
        while not toolline.text.strip():
            # textarea wrapped lines are newlines in linetools, so find the closest above written line number
            toolline = self.mainframe.texthelper.Line(self, toolline.n - 1)
        neditorline = int(toolline.text.rstrip('#'))
        editorline = self.mainframe.texthelper.Line(self.mainframe.TextArea, neditorline)

        if not editorline.text:
            return

        #while not self.mainframe.TextArea.get(start, start + '+ 1c').lstrip():
        if editorline.text.lstrip().startswith('#'):
            self.mainframe.TextArea.delete(editorline.start + ' + %dc' % len(editorline.indent), editorline.start + '+ %dc + 1c' % len(editorline.indent))
        else:
            self.mainframe.TextArea.insert(editorline.start + ' + %dc' % len(editorline.indent), '#')

    def update_linenumbers(self, event=None):
        # get content, but don't include the last newline inserted by tkinter
        content = self.mainframe.TextArea.get(1.0, "end-1c")
        linenumbers = ''
        width = self.mainframe.TextArea.cget('width')
        for i, text in enumerate(content.split('\n')):
            linenumbers += str(i+1)
            linenumbers += '\n'
            bbox_first_char = self.mainframe.TextArea.bbox("%d.0" % (i+1))
            bbox_last_char = self.mainframe.TextArea.bbox("%d.0 - 1c" % (i+2))
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
        self.config(state=NORMAL)
        self.delete(1.0, END)
        self.insert(1.0, linenumbers)
        self.config(state=DISABLED)
        # sbstatus can for some reason not be retrieved when auto-open files at start
        if len(sbstatus) == 2:
            sbfirst, sblast = sbstatus
            self.mainframe.TextArea.scrollYUpdate(sbfirst, sblast)
