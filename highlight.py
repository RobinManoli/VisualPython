try:
    from tkinter import *
except:
    from Tkinter import *

class HighLight():
    """
    """
    def __init__(self, parent, textarea):
        self.parent = parent
        self.mainframe = parent.mainframe
        self.root = parent.root
        
        self.textarea = textarea
        self.textarea.highlight = self

        self.last_same = ''

        self.init()

    def clear(self, prefix=''):
        "Clears tags that start with prefix. Should be able to replace the other clear_ members of this class."
        for tag in self.textarea.tag_names():
            if tag.startswith(prefix):
                self.textarea.tag_remove(tag, 1.0, END)

    def same(self, event=None):
        "Highlights visible text that is the same as the current selection."
        tag = 'Same'
        sel = self.mainframe.texthelper.get_selection(self.textarea)
        
        if sel != self.last_same:
            self.clear(tag)
        self.last_same = sel

        if not sel:
            return

        tv = self.mainframe.texthelper.top_visible(self.textarea)
        bv = self.mainframe.texthelper.bottom_visible(self.textarea)
        content = self.textarea.get(tv, bv)

        from re import finditer, escape
        # list occurences of selection in visible content
        # http://stackoverflow.com/a/4664889
        occurrences = [m.start() for m in finditer(escape(sel), content)]
        
        if occurrences:
            for pos in occurrences:
                self.textarea.mark_set("range_start", tv + ' + %dc' % pos)
                self.textarea.mark_set("range_end", 'range_start + %dc' % len(sel))
                self.textarea.tag_add(tag, "range_start", "range_end")

            # remove same highlighting from actual selection
            self.textarea.tag_remove(tag, SEL_FIRST, SEL_LAST)
            

    def clear_whitespace(self):
        self.clear('Token.Text.Whitespace.')

    def whitespace( self, event=None ):
        tv = self.mainframe.texthelper.top_visible(self.textarea)
        bv = self.mainframe.texthelper.bottom_visible(self.textarea)
        last_newline = 0
        content = self.textarea.get(tv, bv)
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
            self.textarea.mark_set("range_start", tv + ' + %dc' % i)
            self.textarea.mark_set("range_end", 'range_start + 1 c')
            self.textarea.tag_add(tag, "range_start", "range_end")
    
    def clear_brackets(self):
        self.clear('Bracket.')

    def brackets(self, event=None):
        self.clear_brackets()
        line = self.mainframe.texthelper.Line(self.textarea, CURRENT)

        try:
            # no selection rasies TclError
            sel_first = self.mainframe.texthelper.Line(self.textarea, SEL_FIRST)
            sel_last = self.mainframe.texthelper.Line(self.textarea, SEL_LAST)
            if line.n in (sel_first.n, sel_last.n):
                # skip highlighting brackets when selecting text on that line (because otherwise the selected text is not visible)
                return
        except TclError:
            #print('no selection')
            pass

        bv = self.mainframe.texthelper.bottom_visible(self.textarea)
        text = self.textarea.get(line.start, bv)

        found = ''
        openers = '([{<'
        closers = ')]}>' # corresponds to openers' indeces
        # set 0 balance for each bracket type
        # where positive balance means there are more openers than closers for that type
        balance = [0 for o in openers]
        for i, c in enumerate(text):
            current = "%s + %dc" % (line.start, i)
            if not self.mainframe.texthelper.visible(self.textarea, current):
                # this char (and following text at least when using wrap) not visible anymore
                # if not using wrap, next line might be visible
                break

            if c in openers or c in closers:
                found += c
                
                if c in openers:
                    opener = True
                    index = openers.index(c)
                    balance[index] += 1
                else:
                    opener = False
                    index = closers.index(c)
                    balance[index] -= 1
                    
                balance_sum = sum(balance)
            
                if found and not balance_sum and balance.count(0) == len(openers):
                    # brackets found and all brackets closed
                    # stop looking for brackets if at least the line of the mouse cursor (CURRENT) is fully scanned
                    line2 = self.mainframe.texthelper.Line(self.textarea, current)
                    if line2.n != line.n:
                        break

                tag = "Bracket.Token.Punctuation.Bracket" + str( balance_sum+1 )
                
                if opener and balance[index] > 0:
                    mark = "range_start_%s%s%d" % (openers[index], closers[index], balance_sum)
                    pos = "%s + %dc" % (line.start, i)
                    self.textarea.mark_set(mark, pos)

                elif not opener and balance[index] >= 0:
                    mark = "range_end_%s%s%d" % (openers[index], closers[index], balance_sum+1)
                    pos = "%s + %dc" % (line.start, i+1)
                    self.textarea.mark_set(mark, pos)
                    self.textarea.tag_add(tag, mark.replace('range_end_', 'range_start_'), mark)


    def clear_tokens(self):
        # although only Token.Literal.String.Doc gets messed up, to fix this I've only found (inefficiently) removing all token tags to work
        #self.textarea.tag_remove('Token.Literal.String.Doc', 1.0, END) # failed to fix (editing ending chars of) multiline string bug
        self.clear('Token.')

    def tokens(self, event=None):
        """
        Highlight tokens as rendered by Pygments. Seems to only work after textarea is updated, though calling update_idletasks has no effect.
        The problem can be solved by recalling the function if there is no bbox, (as with update_linenumbers), or figure out what is not updated
        when running this function (bbox was the case in update_linenumbers).
        """
        # http://stackoverflow.com/a/30199105
        from pygments import lex, highlight
        from pygments.lexers import PythonLexer
        from pygments.formatters import HtmlFormatter

        # don't use because multiline strings can start at beginning and end in visible view
        #tv = self.mainframe.texthelper.top_visible(self.textarea)
        # use since highlight works if multiline str not properly closed
        bv = self.mainframe.texthelper.bottom_visible(self.textarea)
        data = self.textarea.get("1.0", bv) # "end-1c"

        if data == self.prevdata:
            return

        self.clear_tokens()

        #print( highlight(data, PythonLexer(), HtmlFormatter()))
        prev_content = ''

        i = 0
        for token, content in lex(data, PythonLexer()):
            lencontent = len(content)

            # this happens sometimes in lubuntu
            if not content:
                #print('no content in HighLight.tokens() loop')
                continue

            #str(token) == 'Token.Literal.String.Doc' \
            if self.mainframe.texthelper.visible(self.textarea, '1.0 + %dc' % i) \
            or self.mainframe.texthelper.visible(self.textarea, '1.0 + %dc' % (i+lencontent)):
                self.textarea.mark_set("range_start", "1.0 + %dc" %i )
                self.textarea.mark_set("range_end", "range_start + %dc" % lencontent)
                self.textarea.tag_add(str(token), "range_start", "range_end")

            i += lencontent

        self.prevdata = data

    def init(self):
        self.prevdata = ''
        self.textarea.tag_configure("Token.Keyword", foreground="#CC7A00")
        self.textarea.tag_configure("Token.Keyword.Constant", foreground="#CC7A00")
        self.textarea.tag_configure("Token.Keyword.Declaration", foreground="#CC7A00")
        self.textarea.tag_configure("Token.Keyword.Namespace", foreground="#CC7A00")
        self.textarea.tag_configure("Token.Keyword.Pseudo", foreground="#CC7A00")
        self.textarea.tag_configure("Token.Keyword.Reserved", foreground="#CC7A00")
        self.textarea.tag_configure("Token.Keyword.Type", foreground="#CC7A00")

        self.textarea.tag_configure("Token.Name.Class", foreground="#003D99")
        self.textarea.tag_configure("Token.Name.Exception", foreground="#003D99")
        self.textarea.tag_configure("Token.Name.Function", foreground="#003D99")
        self.textarea.tag_configure("Token.Name.Namespace", foreground="#003D99")
        self.textarea.tag_configure("Token.Name.Builtin.Pseudo", foreground="#003D99")

        self.textarea.tag_configure("Token.Comment", foreground="#B80000")
        self.textarea.tag_configure("Token.Comment.Single", foreground="#B80000")
        self.textarea.tag_configure("Token.Comment.Hashbang", foreground="#B80000")

        self.textarea.tag_configure("Token.Literal.String", foreground="#248F24")
        self.textarea.tag_configure("Token.Literal.String.Double", foreground="#248F24")
        self.textarea.tag_configure("Token.Literal.String.Single", foreground="#248F24")
        self.textarea.tag_configure("Token.Literal.String.Doc", foreground="#248F24")

        #self.textarea.tag_configure("Token.Text", foreground="#248F24", background="#eeeeee")
        self.textarea.tag_configure("Token.Text.Whitespace.Leading0", foreground="#248F24", background="#ccffcc")
        self.textarea.tag_configure("Token.Text.Whitespace.Leading1", foreground="#248F24", background="#ccffff")
        self.textarea.tag_configure("Token.Text.Whitespace.Leading2", foreground="#248F24", background="#ccccff")
        self.textarea.tag_configure("Token.Text.Whitespace.Newline", foreground="#248F24", background="#dddddd")
        #self.textarea.tag_configure("Token.Text.Whitespace.Trailing", foreground="#248F24", background="#eeeeee")

        self.textarea.tag_configure("Bracket.Token.Punctuation.Bracket1", foreground="#ffffff", background="#000000")
        self.textarea.tag_configure("Bracket.Token.Punctuation.Bracket2", foreground="#ffffff", background="#555555")
        self.textarea.tag_configure("Bracket.Token.Punctuation.Bracket3", foreground="#000000", background="#999999")
        self.textarea.tag_configure("Bracket.Token.Punctuation.Bracket4", foreground="#000000", background="#cccccc")
        self.textarea.tag_configure("Bracket.Token.Punctuation.Bracket5", foreground="#ffffff", background="#000000")
        self.textarea.tag_configure("Bracket.Token.Punctuation.Bracket6", foreground="#ffffff", background="#555555")
        self.textarea.tag_configure("Bracket.Token.Punctuation.Bracket7", foreground="#000000", background="#999999")
        self.textarea.tag_configure("Bracket.Token.Punctuation.Bracket8", foreground="#000000", background="#cccccc")

        self.textarea.tag_configure("Same", background="#ffff00")

        #self.textarea.tag_configure("Token.Punctuation", foreground="#248F24", background="#eeeeee")
        #self.textarea.tag_configure("Token.Operator", foreground="#248F24", background="#eeeeee")
        self.textarea.tag_configure("Token.Operator.Word", foreground="#CC7A00")

