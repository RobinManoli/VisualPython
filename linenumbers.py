try:
    from tkinter import *
except:
    from Tkinter import *

class LineNumbers(Canvas):
    """
    """
    def __init__(self, parent, textarea):
        Canvas.__init__(self, parent, relief=FLAT, width='1.5c')
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root
        self.textarea = textarea
        self.textarea.linenumbers = self

        self.last_motion_index = ''
        self.linenumber_items = []

        self.bind('<Motion>', self.on_motion)
        self.bind('<Double-Button-1>', self.on_dclick)

    def on_motion(self, event=None):
        self.draw()


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

    def draw(self, event=None):
        for item in self.linenumber_items:
            self.delete(item)
        tv = self.textarea.texthelper.top_visible(self.textarea)
        bv = self.textarea.texthelper.bottom_visible(self.textarea)
        tvline = self.textarea.texthelper.Line(self.textarea, tv)
        bvline = self.textarea.texthelper.Line(self.textarea, bv)
        for i in range(tvline.n, bvline.n + 1):
            bbox = self.textarea.bbox('%d.%d' % (i,tvline.column))
            if bbox:
                x, y, width, height = bbox
                item = self.create_text((x,y), text="%d" % i, anchor=NW)
                self.linenumber_items.append( item )
