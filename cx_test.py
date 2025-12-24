#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from tkinter import Tk, Label, Button, BOTTOM
except ImportError:
    from Tkinter import Tk, Label, Button, BOTTOM

# import pytorch_lightning
# import pytorch
# import transformers

def main():
    root = Tk()
    root.title('Button')
    Label(text='I am a button').pack(pady=15)
    Button(text='Button').pack(side=BOTTOM)
    root.mainloop()


if __name__ in ('__main__', 'simpletkapp__main__', 'SimpleTkApp__main__'):
    main()