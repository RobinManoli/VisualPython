#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Known bugs (TODO):
    - on_tab and _shift_tab buggy, and visualizing tabs need to differ from spaces in color
    - update linenumbers buggy when moving cursor to trailing whitespace with keys, and then moving cursor inside linetools area
    - if scroll down to hide top content, then resize window down and then maximize top content into view, it doesn't get highlighted
    - highlight.whitspace (line 74), string index out of range if i <= ... content[i+1]

Next features (todo):
    - create new file
    - if editor is too slow with multiple tabs, try to only have one mainframe.textarea, and make editors keep text contents only
"""

try:
    from tkinter import *
except:
    from Tkinter import *
import filemenu
import notebook
import texthelper

class MainFrame(Frame):
    "The main container (Frame) of the program."
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
        self.root = parent

        self.root.title("Visual Python")
        self.pack(fill=BOTH, expand=1)
        self.maximize()

        self.mainframe = self
        self.texthelper = texthelper

        self.menu = Menu(self)
        self.root.config(menu=self.menu)
        self.filemenu = filemenu.FileMenu(self)

        self.notebook = notebook.NoteBook(self)
        self.notebook.pack(side=LEFT, fill=BOTH, expand=True)

        import sys
        if len( sys.argv ) > 1:
            # auto-open file at startup (after inits)
            # something is not ready when auto-opening, resulting in for example multiline-counter being messed up
            # though fixed with update
            self.root.update()
            self.notebook.new_editor( sys.argv[1] )
        else:
            self.notebook.new_editor()

        #self.root.wait_visibility(self.textarea) # FREEZES
        #self.root.wait_window(self.textarea) # never happens
        #self.root.update_idletasks()

    def maximize(self):
        try:
            # windows only? at least not lubuntu
            self.root.state('zoomed')
        except:
            pass


def print_exception(e):
    import sys
    import traceback
    import os
    ex_type, ex, tb = sys.exc_info()
    traceback.print_tb(tb)
    print( '%s %s %s' % (str(ex_type),str(ex),str(traceback.extract_stack())) )
    print()

def main():
    root = Tk()
    root.geometry("250x150+300+300")
    app = MainFrame(root)
    root.mainloop()  


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print_exception(e)
        import os
        os.system("pause")



# http://www.alandmoore.com/blog/2013/07/25/tkinter-not-dead-yet/
