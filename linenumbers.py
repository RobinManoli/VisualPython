try:
    from tkinter import *
except:
    from Tkinter import *

class LineNumbers(Canvas):
    """
    """
    def __init__(self, parent, textarea):
        Canvas.__init__(self, parent, relief=FLAT, width='1.6c')
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root
        self.textarea = textarea
        self.textarea.linenumbers = self

        self.linenumber_items = []
        self.linetool_item = None

        self.bind('<Motion>', self.on_motion)
        self.bind('<Leave>', self.clear_linetool_item)
        self.bind('<Button-1>', self.on_click)

    def clear_linetool_item(self, event=None):
        if self.linetool_item:
            self.delete( self.linetool_item )
            self.linetool_item = None
        
    def on_motion(self, event=None):
        #print(dir(event))
        coords = '@%d,%d' % (event.x, event.y)
        bbox = self.textarea.bbox(coords)
        if bbox:
            x, y, width, height = bbox
            item = self.create_text((40,y), text="#//", anchor=NW)
            self.clear_linetool_item()
            self.linetool_item = item

    def on_click(self, event=None):
        "Comment or uncomment corresponding line in textarea."
        coords = '@%d,%d' % (event.x, event.y)
        index = self.textarea.index(coords)

        line = self.textarea.texthelper.Line(self.textarea, index)
        if not line.text or line.text.lstrip().startswith('##'):
            return

        #while not self.mainframe.TextArea.get(start, start + '+ 1c').lstrip():
        if line.text.lstrip().startswith('#'):
            len_leading_whitespace_after_comment = len(line.text.lstrip()[1:]) - len(line.text.lstrip()[1:].lstrip())
            start = line.start + ' + %dc' % len(line.indent)
            end = line.start + '+ %dc + %dc' % (len(line.indent), len_leading_whitespace_after_comment + 1)
            self.textarea.delete(start, end)
        else:
            self.textarea.insert(line.start + ' + %dc' % len(line.indent), '# ')

    def draw(self, event=None):
        for item in self.linenumber_items:
            self.delete(item)
        tv = self.textarea.texthelper.top_visible(self.textarea)
        bv = self.textarea.texthelper.bottom_visible(self.textarea)
        tvline = self.textarea.texthelper.Line(self.textarea, tv)
        bvline = self.textarea.texthelper.Line(self.textarea, bv)
        tag = 'LineNumber'
        for i in range(tvline.n, bvline.n + 1):
            bbox = self.textarea.bbox('%d.%d' % (i,tvline.column))
            if bbox:
                x, y, width, height = bbox
                item = self.create_text((x,y), text="%d" % i, anchor=NW, tags=tag)
                self.linenumber_items.append( item )
        # binds created items only
        #self.tag_bind(tag, '<Motion>', self.on_motion)
