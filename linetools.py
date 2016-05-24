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
        self.bind('<Button-1>', self.on_click)

    def on_motion(self, event=None):
        index = self.index(CURRENT)
        text = self.mainframe.TextArea.getline(index, self)
        if not text.strip():
            return

        if index != self.last_motion_index:
            self.config(state=NORMAL)
            if self.last_motion_index:
                # delete # chars from last motion
                nline0 = self.mainframe.TextArea.getline_number(self.last_motion_index, self)
                self.delete('%d.end - 7c' % nline0, '%d.end' % nline0)
            # add # chars at end of current line's motion
            start, end = self.mainframe.TextArea.getline_start_end(index, self)
            self.insert(end, ' ######')
            self.config(state=DISABLED)
            self.last_motion_index = index

    def on_click(self, event=None):
        nline = ''
        i = 0
        while not nline.strip():
            # textarea wrapped lines are newlines in linetools, so find the closest above written line number
            i += 1
            nline = self.mainframe.TextArea.getline('current - %dc' % i, widget=self)
        nline = int(nline.rstrip('#'))
        #start, end = self.mainframe.TextArea.getline_start_end(nline)
        line = self.mainframe.TextArea.getline(nline)
        if not line:
            return

        start, end = self.mainframe.TextArea.getline_start_end(nline)
        whitespace = self.mainframe.TextArea.get_whitespace(line)

        #while not self.mainframe.TextArea.get(start, start + '+ 1c').lstrip():
        if line.lstrip().startswith('#'):
            self.mainframe.TextArea.delete(start + ' + %dc' % len(whitespace), start + '+ %dc + 1c' % len(whitespace))
        else:
            self.mainframe.TextArea.insert(start + ' + %dc' % len(whitespace), '#')

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
