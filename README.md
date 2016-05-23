# vpy.py
Proof of concept of visualizing Python code more than just keyword highlighting.

## Requirements
- Python 3
- tkinter
- Pygments 2.1.3 (only version tested)

## Features
- highlights (nested, though only single-line tested) brackets, ()[]{}<>, when hovering the mouse cursor over them.
![hover over code to highlight brackets](https://raw.githubusercontent.com/RobinManoli/VisualPython/master/img/brackets.jpg)
- highlights whitespace with colors, when the mouse cursor moves outside the textarea (to easier distinguish for example tabs from spaces)

