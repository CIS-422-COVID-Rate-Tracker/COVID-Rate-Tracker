"""
File Name:      	search_box.py
Program Name:   	COVID-Infection-Rate-Tracker
Class:         		CIS 422 - Winter22 - University of Oregon
Group memebers: 	Austin Mello
                    Kai Xiong
                    Rebecca Hu
                    Xiang Hao

Created Date:       2/25/2022
modifier:           Kai Xiong
                    Rebecca Hu

Required library:   Tkinter

How to install Tkinter: sudo apt-get install python3.10-tk

credit: cite the components to build the search box part:
                    https://github.com/arcticfox1919/tkinter-tabview

Used By:
    interface.py
    
"""
import tkinter as tk
from tkinter import Toplevel, Listbox
from tkinter import Entry
from tkinter import StringVar


class SearchBox(Entry):
    """
    Init Attributes for class:
    Attribute name:         Type:        Default Val:       Description:
    stringVariable          StringVar()         ---         the variable record string in tkinter
    searchWindow            None/Toplevel()     None        the search window will be gerenated after callback
    callback                function/None       None        callback function will return the namelist and call update() function
    master                  tkinter component   None        take the last tkinter component, such as "tk.canvas"
    listVariable            StringVar()         ---         a string variable will append to the list and show on the search window
    prevText                string              ""          record previous string variable
    currentItem             string              ""          record current string variable
    """
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
    
    """
    build in current callback, will call the callback function from other class. 
    it records the input string variable in the search box
    """
    def _callback(self, *_):
        current_text = self.stringVariable.get()
        if current_text != self.prevText:
            self.prevText = current_text
            self.callback(current_text)
            
    """
    update function to decide generate or destroy search window.
    Would be called by other class (not been called by self)
    """
    def update(self, item_list):
        if item_list and self.searchWindow:
            self.listVariable.set(item_list)
        elif not item_list and self.searchWindow:
            self._hide()
        elif item_list and not self.searchWindow:
            self._show()
            self.listVariable.set(item_list)
    
    """
    function to genertae the search window
    """
    def _show(self):
        self.searchWindow = Toplevel()
        self.searchWindow.transient(self.master)
        self.searchWindow.overrideredirect(True)
        self.searchWindow.attributes("-alpha", 0.9)
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height() + 6
        self.searchWindow.wm_geometry("%dx%d+%d+%d" % (190, 95, x, y))
        self._create_list()

    """
    function to destory the search window
    """
    def _hide(self):
        if self.searchWindow:
            self.searchWindow.destroy()
            self.searchWindow = None

    """
    function return the chosed string variable on the 
    search window, then hide the window after click
    """
    def _listbox_click(self, event):
        widget = event.widget
        self.currentItem = widget.get(widget.curselection())
        self.stringVariable.set(self.currentItem)
        self._hide()

    """
    generate listbox in the search window, to show other 
    string variable which is similar as input string
    """
    def _create_list(self):
        listBox = Listbox(self.searchWindow, selectmode=tk.SINGLE, listvariable=self.listVariable)
        listBox.bind('<<ListboxSelect>>', self._listbox_click)
        listBox.pack(fill=tk.BOTH, expand=tk.YES)

    