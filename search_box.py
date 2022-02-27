# credit: https://github.com/arcticfox1919/tkinter-tabview
import tkinter as tk
from tkinter import Toplevel, Listbox
from tkinter import Entry
from tkinter import StringVar


class SearchBox(Entry):

    def __init__(self, master=None, callback=None, cnf={}):
        super().__init__(master, cnf)
        self.stringVariable = tk.StringVar()
        self["textvariable"] = self.stringVariable
        self.stringVariable.trace('w', self._callback)
        self.searchWindow = None
        self.callback = callback
        self.master = master
        self.listVariable = StringVar()
        self.prevText = ""
        self.currentItem = ""

    def _callback(self, *_):
        current_text = self.stringVariable.get()
        if current_text != self.prevText:
            self.prevText = current_text
            self.callback(current_text)

    def update(self, item_list):
        if item_list and self.searchWindow:
            self.listVariable.set(item_list)
        elif not item_list and self.searchWindow:
            self._hide()
        elif item_list and not self.searchWindow:
            self._show()
            self.listVariable.set(item_list)

    def _show(self):
        self.searchWindow = Toplevel()
        self.searchWindow.transient(self.master)
        self.searchWindow.overrideredirect(True)
        self.searchWindow.attributes("-alpha", 0.9)
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 6
        self.searchWindow.wm_geometry("%dx%d+%d+%d" % (190, 95, x, y))
        self._create_list()

    def _hide(self):
        if self.searchWindow:
            self.searchWindow.destroy()
            self.searchWindow = None

    def _listbox_click(self, event):
        widget = event.widget
        self.currentItem = widget.get(widget.curselection())
        self.stringVariable.set(self.currentItem)
        print("string", self.currentItem)
        self._hide()

    def _create_list(self):
        listBox = Listbox(self.searchWindow, selectmode=tk.SINGLE, listvariable=self.listVariable)
        listBox.bind('<<ListboxSelect>>', self._listbox_click)
        listBox.pack(fill=tk.BOTH, expand=tk.YES)

    