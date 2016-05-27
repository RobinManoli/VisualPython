from tkinter import *

class HighLight():
    """
    """
    def __init__(self, parent):
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root

        self.init()

    def init(self):
        self.prevdata = ''
        self.mainframe.TextArea.tag_configure("Token.Keyword", foreground="#CC7A00")
        self.mainframe.TextArea.tag_configure("Token.Keyword.Constant", foreground="#CC7A00")
        self.mainframe.TextArea.tag_configure("Token.Keyword.Declaration", foreground="#CC7A00")
        self.mainframe.TextArea.tag_configure("Token.Keyword.Namespace", foreground="#CC7A00")
        self.mainframe.TextArea.tag_configure("Token.Keyword.Pseudo", foreground="#CC7A00")
        self.mainframe.TextArea.tag_configure("Token.Keyword.Reserved", foreground="#CC7A00")
        self.mainframe.TextArea.tag_configure("Token.Keyword.Type", foreground="#CC7A00")

        self.mainframe.TextArea.tag_configure("Token.Name.Class", foreground="#003D99")
        self.mainframe.TextArea.tag_configure("Token.Name.Exception", foreground="#003D99")
        self.mainframe.TextArea.tag_configure("Token.Name.Function", foreground="#003D99")
        self.mainframe.TextArea.tag_configure("Token.Name.Namespace", foreground="#003D99")
        self.mainframe.TextArea.tag_configure("Token.Name.Builtin.Pseudo", foreground="#003D99")

        self.mainframe.TextArea.tag_configure("Token.Comment", foreground="#B80000")
        self.mainframe.TextArea.tag_configure("Token.Comment.Single", foreground="#B80000")
        self.mainframe.TextArea.tag_configure("Token.Comment.Hashbang", foreground="#B80000")

        self.mainframe.TextArea.tag_configure("Token.Literal.String", foreground="#248F24")
        self.mainframe.TextArea.tag_configure("Token.Literal.String.Double", foreground="#248F24")
        self.mainframe.TextArea.tag_configure("Token.Literal.String.Single", foreground="#248F24")
        self.mainframe.TextArea.tag_configure("Token.Literal.String.Doc", foreground="#248F24")

        #self.mainframe.TextArea.tag_configure("Token.Text", foreground="#248F24", background="#eeeeee")
        self.mainframe.TextArea.tag_configure("Token.Text.Whitespace.Leading0", foreground="#248F24", background="#ccffcc")
        self.mainframe.TextArea.tag_configure("Token.Text.Whitespace.Leading1", foreground="#248F24", background="#ccffff")
        self.mainframe.TextArea.tag_configure("Token.Text.Whitespace.Leading2", foreground="#248F24", background="#ccccff")
        self.mainframe.TextArea.tag_configure("Token.Text.Whitespace.Newline", foreground="#248F24", background="#dddddd")
        #self.mainframe.TextArea.tag_configure("Token.Text.Whitespace.Trailing", foreground="#248F24", background="#eeeeee")

        self.mainframe.TextArea.tag_configure("Bracket.Token.Punctuation.Bracket1", foreground="#ffffff", background="#000000")
        self.mainframe.TextArea.tag_configure("Bracket.Token.Punctuation.Bracket2", foreground="#ffffff", background="#555555")
        self.mainframe.TextArea.tag_configure("Bracket.Token.Punctuation.Bracket3", foreground="#000000", background="#999999")
        self.mainframe.TextArea.tag_configure("Bracket.Token.Punctuation.Bracket4", foreground="#000000", background="#cccccc")
        self.mainframe.TextArea.tag_configure("Bracket.Token.Punctuation.Bracket5", foreground="#ffffff", background="#000000")
        self.mainframe.TextArea.tag_configure("Bracket.Token.Punctuation.Bracket6", foreground="#ffffff", background="#555555")
        self.mainframe.TextArea.tag_configure("Bracket.Token.Punctuation.Bracket7", foreground="#000000", background="#999999")
        self.mainframe.TextArea.tag_configure("Bracket.Token.Punctuation.Bracket8", foreground="#000000", background="#cccccc")

        #self.mainframe.TextArea.tag_configure("Token.Punctuation", foreground="#248F24", background="#eeeeee")
        #self.mainframe.TextArea.tag_configure("Token.Operator", foreground="#248F24", background="#eeeeee")
        self.mainframe.TextArea.tag_configure("Token.Operator.Word", foreground="#CC7A00")

    #def index_is_visible(self, index):
    #    return bool( self.mainframe.TextArea.bbox(index) )

    def clear_whitespace(self, event=None):
        for tag in self.mainframe.TextArea.tag_names():
            if tag.startswith('Token.Text.Whitespace.'):
                self.mainframe.TextArea.tag_remove(tag, 1.0, END)

    def whitespace( self, event=None ):
        tv = self.mainframe.texthelper.top_visible(self.mainframe.TextArea)
        bv = self.mainframe.texthelper.bottom_visible(self.mainframe.TextArea)
        last_newline = 0
        content = self.mainframe.TextArea.get(tv, bv)
        for i, char in enumerate(content):
            if char == '\n':
                tag = 'Token.Text.Whitespace.Newline'
                last_newline = i
            elif not char.strip():
                if i > 0 and content[i-1].strip():
                    # prev char not whitespace
                    continue
                if i <= len(content) and content[i+1].strip():
                    # next char not whitespace
                    continue
                tag = 'Token.Text.Whitespace.Leading' + str( (i-last_newline)%3 )
            else:
                continue
            self.mainframe.TextArea.mark_set("range_start", tv + ' + %dc' % i)
            self.mainframe.TextArea.mark_set("range_end", 'range_start + 1 c')
            self.mainframe.TextArea.tag_add(tag, "range_start", "range_end")
    
    def clear_brackets(self, event=None):
        for tag in self.mainframe.TextArea.tag_names():
            if tag.startswith('Bracket.'):
                self.mainframe.TextArea.tag_remove(tag, 1.0, END)

    def brackets(self, event=None):
        "Highlights brackets, where brackets in this context includes ()[]{}."
        #print( "@%d,%d" % (event.x, event.y) ) # mouse coords
        self.clear_brackets()

        index = self.mainframe.TextArea.index(CURRENT)
        nline, nchar = index.split('.')
        try:
            # no selection rasies TclError
            self.mainframe.TextArea.index(SEL_FIRST)
            if nline == self.mainframe.TextArea.index(SEL_FIRST).split('.')[0] or nline == self.mainframe.TextArea.index(SEL_LAST).split('.')[0]:
                # fix invisible selection when selecting highlighted brackets by not highlighting during selection on that line
                return
        except TclError:
            pass
        nline = int(nline)
        #nchar = int(nchar)
        start = "%d.0" % nline
        #end = "%d.0 - 1c" % (nline+1)
        text = self.mainframe.TextArea.get(start, END)
        found = ''
        for i, c in enumerate(text):
            current = "%s + %dc" % (start,i)
            if not self.mainframe.texthelper.visible(self.mainframe.TextArea, current): #self.index_is_visible(current):
                # this char (and following at least when using wrap) not visible anymore
                break


            found += c if c in '()[]{}<>' else ''
            poc = found.count('(')
            pcc = found.count(')')
            pb = poc - pcc
            boc = found.count('[')
            bcc = found.count(']')
            bb = boc - bcc
            coc = found.count('{')
            ccc = found.count('}')
            cb = coc - ccc
            toc = found.count('<')
            tcc = found.count('>')
            tb = toc - tcc
            b = pb + bb + cb + tb
            
            if found and not pb and not bb and not cb:
                # stop looking for brackets if all brackets are closed and at least the line of the mouse cursor (CURRENT) is fully scanned
                index2 = self.mainframe.TextArea.index(current)
                nline2, nchar2 = index2.split('.')
                nline2 = int(nline2)
                if nline2 != nline:
                    break

            tag = "Bracket.Token.Punctuation.Bracket" + str( b+1 )
            if c == '(':
                if pb > 0:
                    self.mainframe.TextArea.mark_set("range_start_pb%d"%b, "%s + %dc" % (start,i))
                    #print('(', poc, pb, b, i, tag)
            elif c == ')':
                if pb >= 0:
                    self.mainframe.TextArea.mark_set("range_end_pb%d"%(b+1), "%s + %dc" % (start,i+1))
                    self.mainframe.TextArea.tag_add(tag, "range_start_pb%d"%(b+1), "range_end_pb%d"%(b+1))
                    #print(')', poc, pb, b, i)
            elif c == '[':
                if bb > 0:
                    self.mainframe.TextArea.mark_set("range_start_pb%d"%b, "%s + %dc" % (start,i))
            elif c == ']':
                if bb >= 0:
                    self.mainframe.TextArea.mark_set("range_end_pb%d"%(b+1), "%s + %dc" % (start,i+1))
                    self.mainframe.TextArea.tag_add(tag, "range_start_pb%d"%(b+1), "range_end_pb%d"%(b+1))
            elif c == '{':
                if cb > 0:
                    self.mainframe.TextArea.mark_set("range_start_pb%d"%b, "%s + %dc" % (start,i))
            elif c == '}':
                if cb >= 0:
                    self.mainframe.TextArea.mark_set("range_end_pb%d"%(b+1), "%s + %dc" % (start,i+1))
                    self.mainframe.TextArea.tag_add(tag, "range_start_pb%d"%(b+1), "range_end_pb%d"%(b+1))
            elif c == '<':
                if tb > 0:
                    self.mainframe.TextArea.mark_set("range_start_pb%d"%b, "%s + %dc" % (start,i))
            elif c == '>':
                if tb >= 0:
                    self.mainframe.TextArea.mark_set("range_end_pb%d"%(b+1), "%s + %dc" % (start,i+1))
                    self.mainframe.TextArea.tag_add(tag, "range_start_pb%d"%(b+1), "range_end_pb%d"%(b+1))

            #self.mainframe.TextArea.mark_set("range_start", "%s + %dc" % (start,i))
            #self.mainframe.TextArea.mark_set("range_end", "range_start + 1c")
            #self.mainframe.TextArea.tag_add(tag, "range_start", "range_end")
        
        #print( self.mainframe.TextArea.index(CURRENT), self.mainframe.TextArea.get(start, end) )

        #self.mainframe.TextArea.mark_set("range_start", "%d.0" % nline)
        #self.mainframe.TextArea.mark_set("range_end", "%d.0 - 1c" % (nline+1))
        #self.mainframe.TextArea.tag_add(tag, "range_start", "range_end")
        #content = self.mainframe.TextArea.get("range_start", "range_end")

        
    def clear_tokens(self, event=None):
        for tag in self.mainframe.TextArea.tag_names():
            # although only Token.Literal.String.Doc gets messed up, to fix this I've only found (inefficiently) removing all token tags to work
            # do not remove SEL "sel" tags
            if tag.startswith('Token.'):
                self.mainframe.TextArea.tag_remove(tag, 1.0, END)
        #self.mainframe.TextArea.tag_remove('Token.Literal.String.Doc', 1.0, END) # failed to fix (editing ending chars of) multiline string bug

    def tokens(self, event=None):
        # http://stackoverflow.com/a/30199105
        from pygments import lex, highlight
        from pygments.lexers import PythonLexer
        from pygments.formatters import HtmlFormatter

        # don't use because multiline strings can start at beginning and end in visible view
        #tv = self.mainframe.texthelper.top_visible(self.mainframe.TextArea)
        # use since highlight works if multiline str not properly closed
        bv = self.mainframe.texthelper.bottom_visible(self.mainframe.TextArea)
        data = self.mainframe.TextArea.get("1.0", bv) # "end-1c"

        if data == self.prevdata:
            return

        self.clear_tokens()

        #print( highlight(data, PythonLexer(), HtmlFormatter()))
        prev_content = ''

        i = 0
        for token, content in lex(data, PythonLexer()):
            lencontent = len(content)

            # delete this block if never happens
            if not content:
                print('no content in HighLight.tokens() loop')
                continue

            #strtoken == 'Token.Literal.String.Doc' \
            if self.mainframe.texthelper.visible(self.mainframe.TextArea, '1.0 + %dc' % i) \
            or self.mainframe.texthelper.visible(self.mainframe.TextArea, '1.0 + %dc' % (i+lencontent)):
                strtoken = str(token)
                self.mainframe.TextArea.mark_set("range_start", "1.0 + %dc" %i )
                self.mainframe.TextArea.mark_set("range_end", "range_start + %dc" % lencontent)
                self.mainframe.TextArea.tag_add(strtoken, "range_start", "range_end")

            i += lencontent

        self.prevdata = data
