try:
    from tkinter import *
except:
    from Tkinter import *

class LineTools(Text):
    """
    """
    def __init__(self, parent, textarea):
        Text.__init__(self, parent, state=DISABLED, wrap=NONE, yscrollcommand=textarea.scrollYUpdate, width=5, padx=5, pady=5, relief=FLAT)
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root
        self.textarea = textarea
        self.textarea.linetools = self

        self.last_motion_index = ''

        self.tag_configure("CurrentLine", foreground="#000000", background="#ffff00")

        self.bind('<Motion>', self.on_motion)
        self.bind('<Double-Button-1>', self.on_dclick)

    def on_motion(self, event=None):
        if not self.get(1.0, END).strip():
            return
        index = self.index(CURRENT)
        line = self.mainframe.texthelper.Line(self, index)
        
        if index != self.last_motion_index:
            self.tag_remove('CurrentLine', 1.0, END)
            if not line.text.strip():
                # find above numbered line
                i = 1
                while not self.get('current - %dc' % i).strip():
                    i += 1
                start = self.mainframe.texthelper.Line(self, 'current - %dc' % i)
            else:
                start = line
            if self.get('%d.end' % line.n, END).rstrip():
                # there are non whitespace chars below CURRENT
                j = 1
                while not self.get('%d.end + %dc' % (line.n, j)).strip():
                    j += 1
                # move j back to last whitespace char
                j -= 1
                end = self.mainframe.texthelper.Line(self, '%d.end + %dc' % (line.n, j))
            else:
                end = line
            # find below numbered line or end
            self.tag_add('CurrentLine', '%d.0' % start.n, '%d.end + 1c' % end.n)
            self.last_motion_index = index

    def on_dclick(self, event=None):
        toolline = self.mainframe.texthelper.Line(self, CURRENT)
        while not toolline.text.strip():
            # textarea wrapped lines are newlines in linetools, so find the closest above written line number
            toolline = self.mainframe.texthelper.Line(self, toolline.n - 1)
        neditorline = int(toolline.text.rstrip('#'))
        editorline = self.mainframe.texthelper.Line(self.textarea, neditorline)

        if not editorline.text:
            return

        #while not self.mainframe.TextArea.get(start, start + '+ 1c').lstrip():
        if editorline.text.lstrip().startswith('#'):
            self.textarea.delete(editorline.start + ' + %dc' % len(editorline.indent), editorline.start + '+ %dc + 1c' % len(editorline.indent))
        else:
            self.textarea.insert(editorline.start + ' + %dc' % len(editorline.indent), '#')

    def update_linenumbers(self, event=None):
        """
        Write linenumbers corresponding to the lines in textarea.
        Will not work with multilines, unless there is no wrap.
        The reason is that there is no way to measure multilines that are not visible.
        (It is possible with bbox for visible ones, but still a bit problematic.)
        It might be possible however using the scrollbar to measure wrapped lines.
        """
        # get content, but don't include the last newline inserted by tkinter
        content = self.textarea.get(1.0, "end-1c")
        # need to update_idletasks before bbox working, according to http://effbot.org/tkinterbook/text.htm#Tkinter.Text.bbox-method
        # self.textarea.update_idletasks() # no effect though
        linenumbers = ''
        #width = self.textarea.cget('width')
        for i, text in enumerate(content.split('\n')):
            linenumbers += str(i+1)
            linenumbers += '\n'
            bbox_first_char = self.textarea.bbox("%d.0" % (i+1))
            bbox_last_char = self.textarea.bbox("%d.0 - 1c" % (i+2))
            if bbox_first_char and bbox_last_char:
                wrapped_line_height = bbox_last_char[1] - bbox_first_char[1]
                unwrapped_line_height = bbox_first_char[3]
                # add one new line per visual line that actual line takes up
                linenumbers += '\n' * int(wrapped_line_height/unwrapped_line_height)
                # works except width doesn't mean actual width
                # linenumbers += '\n' * (1 + int(len(text)/width))
            else:
                # instead of update_idletasks(), to get bbox, redo this function after 100ms
                # todo BUG: doesn't work when cursor has gone outside visibility (ie on resize, since invisible should return None for bbox)
                print(bbox_first_char, bbox_last_char)
                #self.after(100, self.update_linenumbers)
                return

        # remove last addition (of loop) of new line
        linenumbers = linenumbers[:-1]

        # fix unwanted scrolling when inserting linenumbers
        sbstatus = self.textarea.scrollbarY.get()
        self.config(state=NORMAL)
        self.delete(1.0, END)
        self.insert(1.0, linenumbers)
        self.config(state=DISABLED)
        # sbstatus can for some reason not be retrieved when auto-open files at start
        if len(sbstatus) == 2:
            sbfirst, sblast = sbstatus
            self.textarea.scrollYUpdate(sbfirst, sblast)
