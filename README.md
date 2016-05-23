# vpy.py
Proof of concept of visualizing Python code more than just keyword highlighting.

![keyword highlighting](https://raw.githubusercontent.com/RobinManoli/VisualPython/master/img/highlight.jpg)


## Requirements
- Python 3
- tkinter
- Pygments 2.1.3 (only version tested)

## Features
- highlights (nested, though only single-line tested) brackets, ()[]{}<>, when hovering the mouse cursor over them.
![hover over code to highlight brackets](https://raw.githubusercontent.com/RobinManoli/VisualPython/master/img/brackets.jpg)


- highlights whitespace with colors, when the mouse cursor moves outside the textarea (you can easily distinguish for example tabs from spaces, and trailing spaces)

![move mouse cursor outside textarea to see whitespace](https://raw.githubusercontent.com/RobinManoli/VisualPython/master/img/whitespace.jpg)

