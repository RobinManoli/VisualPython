#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Known bugs (TODO):
    - 
"""

from tkinter import *
import filemenu
import textarea
import highlight

class MainFrame(Frame):
    "The main container (Frame) of the program."
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
        self.root = parent

        self.root.title("Visual Python")
        self.pack(fill=BOTH, expand=1)
        self.maximize()
        self.FileMenu = filemenu.FileMenu(self)
        self.TextArea = textarea.TextArea(self)
        self.HighLight = highlight.HighLight(self)

        # auto-open file at startup (after inits)
        # something is not ready when auto-opening, resulting in for example multiline-counter being messed up
        # though fixed with update
        self.root.update()
        
        import sys
        if len( sys.argv ) > 1:
            self.FileMenu.open( sys.argv[1] )

        #self.root.wait_visibility(self.textarea) # FREEZES
        #self.root.wait_window(self.textarea) # never happens
        #self.root.update_idletasks()

    def maximize(self):
        self.root.state('zoomed')


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