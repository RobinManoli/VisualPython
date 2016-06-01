# Visual Python - vpy.py
Proof of concept editor, visualizing Python code more than just keyword highlighting.

![keyword highlighting](https://raw.githubusercontent.com/RobinManoli/VisualPython/master/img/highlight.jpg)


## Requirements
- Python 2 or 3
- Tkinter, ttk
- Pygments (tested v2.1.3)

## Features
- highlights (nested) brackets - ()[]{}<> - when hovering the mouse cursor over them.
![hover over code to highlight brackets](https://raw.githubusercontent.com/RobinManoli/VisualPython/master/img/brackets.jpg)


- highlights whitespace with colors, when the mouse cursor moves outside the main text widget (you can easily distinguish for example tabs from spaces, and trailing spaces)

![move mouse cursor outside textarea to see whitespace](https://raw.githubusercontent.com/RobinManoli/VisualPython/master/img/whitespace.jpg)

- comments/uncomments lines when clicking the corresponding line number