from tkinter import *
from tkinter.filedialog import askopenfilename

class HighLight():
    """
    """
    def __init__(self, parent):
        self.parent = parent
        self.mainframe = parent
        self.root = parent.root

        self.mainframe.highlight = self.highlight

        self.init()

    def init(self):
        self.prevdata = ''
        self.mainframe.textarea.tag_configure("Token.Keyword", foreground="#CC7A00")
        self.mainframe.textarea.tag_configure("Token.Keyword.Constant", foreground="#CC7A00")
        self.mainframe.textarea.tag_configure("Token.Keyword.Declaration", foreground="#CC7A00")
        self.mainframe.textarea.tag_configure("Token.Keyword.Namespace", foreground="#CC7A00")
        self.mainframe.textarea.tag_configure("Token.Keyword.Pseudo", foreground="#CC7A00")
        self.mainframe.textarea.tag_configure("Token.Keyword.Reserved", foreground="#CC7A00")
        self.mainframe.textarea.tag_configure("Token.Keyword.Type", foreground="#CC7A00")

        self.mainframe.textarea.tag_configure("Token.Name.Class", foreground="#003D99")
        self.mainframe.textarea.tag_configure("Token.Name.Exception", foreground="#003D99")
        self.mainframe.textarea.tag_configure("Token.Name.Function", foreground="#003D99")
        self.mainframe.textarea.tag_configure("Token.Name.Namespace", foreground="#003D99")
        self.mainframe.textarea.tag_configure("Token.Name.Builtin.Pseudo", foreground="#003D99")

        self.mainframe.textarea.tag_configure("Token.Comment", foreground="#B80000")
        self.mainframe.textarea.tag_configure("Token.Comment.Single", foreground="#B80000")
        self.mainframe.textarea.tag_configure("Token.Comment.Hashbang", foreground="#B80000")

        self.mainframe.textarea.tag_configure("Token.Literal.String", foreground="#248F24")
        self.mainframe.textarea.tag_configure("Token.Literal.String.Double", foreground="#248F24")
        self.mainframe.textarea.tag_configure("Token.Literal.String.Single", foreground="#248F24")
        self.mainframe.textarea.tag_configure("Token.Literal.String.Doc", foreground="#248F24")

        #self.mainframe.textarea.tag_configure("Token.Text", foreground="#248F24", background="#eeeeee")
        self.mainframe.textarea.tag_configure("Token.Text.Whitespace.Leading0", foreground="#248F24", background="#ccffcc")
        self.mainframe.textarea.tag_configure("Token.Text.Whitespace.Leading1", foreground="#248F24", background="#ccffff")
        self.mainframe.textarea.tag_configure("Token.Text.Whitespace.Leading2", foreground="#248F24", background="#ccccff")
        self.mainframe.textarea.tag_configure("Token.Text.Whitespace.Newline", foreground="#248F24", background="#dddddd")
        #self.mainframe.textarea.tag_configure("Token.Text.Whitespace.Trailing", foreground="#248F24", background="#eeeeee")

        self.mainframe.textarea.tag_configure("Bracket.Token.Punctuation.Bracket1", foreground="#ffffff", background="#000000")
        self.mainframe.textarea.tag_configure("Bracket.Token.Punctuation.Bracket2", foreground="#ffffff", background="#555555")
        self.mainframe.textarea.tag_configure("Bracket.Token.Punctuation.Bracket3", foreground="#000000", background="#999999")
        self.mainframe.textarea.tag_configure("Bracket.Token.Punctuation.Bracket4", foreground="#000000", background="#cccccc")
        self.mainframe.textarea.tag_configure("Bracket.Token.Punctuation.Bracket5", foreground="#ffffff", background="#000000")
        self.mainframe.textarea.tag_configure("Bracket.Token.Punctuation.Bracket6", foreground="#ffffff", background="#555555")
        self.mainframe.textarea.tag_configure("Bracket.Token.Punctuation.Bracket7", foreground="#000000", background="#999999")
        self.mainframe.textarea.tag_configure("Bracket.Token.Punctuation.Bracket8", foreground="#000000", background="#cccccc")

        #self.mainframe.textarea.tag_configure("Token.Punctuation", foreground="#248F24", background="#eeeeee")
        #self.mainframe.textarea.tag_configure("Token.Operator", foreground="#248F24", background="#eeeeee")
        self.mainframe.textarea.tag_configure("Token.Operator.Word", foreground="#CC7A00")

    def index_is_visible(self, index):
        return bool( self.mainframe.textarea.bbox(index) )

    def whitespace(self, strtoken, content, prev_content, event=None):
        #print("'%s'" % content)
        for i, char in enumerate(content):
            self.mainframe.textarea.mark_set("range_end", "range_start + 1c")
            if char == '\n':
                tag = strtoken + '.Whitespace.Newline'
            else:
                tag = strtoken + '.Whitespace.Leading' + str(i%3)
            self.mainframe.textarea.tag_add(tag, "range_start", "range_end")
            self.mainframe.textarea.mark_set("range_start", "range_end")


    def brackets(self, event=None):
        "Highlights brackets, where brackets in this context includes ()[]{}."
        #self.highlighted_punctuation += 'content'
        #print( "@%d,%d" % (event.x, event.y) ) # mouse coords
        for tag in self.mainframe.textarea.tag_names():
            if tag.startswith('Bracket.'):
                self.mainframe.textarea.tag_remove(tag, 1.0, END)

        index = self.mainframe.textarea.index(CURRENT)
        nline, nchar = index.split('.')
        nline = int(nline)
        #nchar = int(nchar)
        start = "%d.0" % nline
        #end = "%d.0 - 1c" % (nline+1)
        text = self.mainframe.textarea.get(start, END)
        found = ''
        for i, c in enumerate(text):
            current = "%s + %dc" % (start,i)
            if not self.index_is_visible(current):
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
                index2 = self.mainframe.textarea.index(current)
                nline2, nchar2 = index2.split('.')
                nline2 = int(nline2)
                if nline2 != nline:
                    break

            tag = "Bracket.Token.Punctuation.Bracket" + str( b+1 )
            if c == '(':
                if pb > 0:
                    self.mainframe.textarea.mark_set("range_start_pb%d"%b, "%s + %dc" % (start,i))
                    #print('(', poc, pb, b, i, tag)
            elif c == ')':
                if pb >= 0:
                    self.mainframe.textarea.mark_set("range_end_pb%d"%(b+1), "%s + %dc" % (start,i+1))
                    self.mainframe.textarea.tag_add(tag, "range_start_pb%d"%(b+1), "range_end_pb%d"%(b+1))
                    #print(')', poc, pb, b, i)
            elif c == '[':
                if bb > 0:
                    self.mainframe.textarea.mark_set("range_start_pb%d"%b, "%s + %dc" % (start,i))
            elif c == ']':
                if bb >= 0:
                    self.mainframe.textarea.mark_set("range_end_pb%d"%(b+1), "%s + %dc" % (start,i+1))
                    self.mainframe.textarea.tag_add(tag, "range_start_pb%d"%(b+1), "range_end_pb%d"%(b+1))
            elif c == '{':
                if cb > 0:
                    self.mainframe.textarea.mark_set("range_start_pb%d"%b, "%s + %dc" % (start,i))
            elif c == '}':
                if cb >= 0:
                    self.mainframe.textarea.mark_set("range_end_pb%d"%(b+1), "%s + %dc" % (start,i+1))
                    self.mainframe.textarea.tag_add(tag, "range_start_pb%d"%(b+1), "range_end_pb%d"%(b+1))
            elif c == '<':
                if tb > 0:
                    self.mainframe.textarea.mark_set("range_start_pb%d"%b, "%s + %dc" % (start,i))
            elif c == '>':
                if tb >= 0:
                    self.mainframe.textarea.mark_set("range_end_pb%d"%(b+1), "%s + %dc" % (start,i+1))
                    self.mainframe.textarea.tag_add(tag, "range_start_pb%d"%(b+1), "range_end_pb%d"%(b+1))

            #self.mainframe.textarea.mark_set("range_start", "%s + %dc" % (start,i))
            #self.mainframe.textarea.mark_set("range_end", "range_start + 1c")
            #self.mainframe.textarea.tag_add(tag, "range_start", "range_end")
        
        #print( self.mainframe.textarea.index(CURRENT), self.mainframe.textarea.get(start, end) )

        #self.mainframe.textarea.mark_set("range_start", "%d.0" % nline)
        #self.mainframe.textarea.mark_set("range_end", "%d.0 - 1c" % (nline+1))
        #self.mainframe.textarea.tag_add(tag, "range_start", "range_end")
        #content = self.mainframe.textarea.get("range_start", "range_end")


    def highlight(self, event=None, forced=False):
        # http://stackoverflow.com/a/30199105
        from pygments import lex, highlight
        from pygments.lexers import PythonLexer
        from pygments.formatters import HtmlFormatter

        data = self.mainframe.textarea.get("1.0", "end-1c")
        if data == self.prevdata and not forced:
            return

        # print(self.mainframe.textarea.tag_remove.__code__.co_varnames) # see parameter names of a function
        #print( self.mainframe.textarea.mark_names() )
        #print( self.mainframe.textarea.tag_names() )
        
        for tag in self.mainframe.textarea.tag_names():
            # although only Token.Literal.String.Doc gets messed up, to fix this I've only found (inefficiently) removing all tags to work
            # do not remove SEL "sel" tags
            if tag.startswith('Token.'):
                self.mainframe.textarea.tag_remove(tag, 1.0, END)
        #self.mainframe.textarea.tag_remove('Token.Literal.String.Doc', 1.0, END) # failed to fix (editing ending chars of) multiline string bug
        self.mainframe.textarea.mark_set("range_start", "1.0")
        #print( highlight(data, PythonLexer(), HtmlFormatter()))

        #prev_strtoken = ''
        prev_content = ''
        self.highlighted_punctuation = ''
        for token, content in lex(data, PythonLexer()):
            #if not content:
            #    continue
            if event and event.char == '\r':
                #print(content, token, len(content)) # on keypress enter
                pass

            strtoken = str(token)
            if self.mainframe.TextArea.do_highlight_whitespace \
            and strtoken == 'Token.Text' and not content.strip() and \
            (not prev_content.strip() or len(content) > 1 or '\n' in content):
                self.whitespace(strtoken, content, prev_content)
            else:
                self.mainframe.textarea.mark_set("range_end", "range_start + %dc" % len(content))
                self.mainframe.textarea.tag_add(strtoken, "range_start", "range_end")
                self.mainframe.textarea.mark_set("range_start", "range_end")
            
            #prev_strtoken = strtoken
            prev_content = content
        # end the starting range after last loop iteration
        self.mainframe.textarea.mark_set("range_end", END)

        #self.mainframe.textarea.mark_set("range_end", "range_start + %dc" % len(content))
        #self.mainframe.textarea.tag_add(str(token), "range_start", "range_end")
        #self.mainframe.textarea.mark_set("range_start", "range_end")
        
        self.prevdata = data
