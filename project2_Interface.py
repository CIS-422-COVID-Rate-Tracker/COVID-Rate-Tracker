'''
Graphic User Interface
Project 2
Created Date: 2/22/2022
Last Update Date: 2/25/2022
Author: Kai Xiong，Rebecca Hu

Required library: Tkinter
# How to install Tkinter: sudo apt-get install python3.7-tk

'''
import sys
import tkinter as tk
from tkinter import *
from search_box import SearchBox
from tkinter import filedialog
from tkinter import Toplevel, Listbox
from tkinter import Entry
from tkinter import StringVar
from tkinter import messagebox

# testing dataset here (you can delete after decide final version)
test_case = {"Kai Xiong":[1, 1],"Rebecca Hu":[0, 0],"Xiang Hao":[1, 0],"Austin Mello":[0, 0], "Nick Johnstone":[0, 0],"Jeager Jochimsen":[0, 0],"Haoran Zhang":[0, 0],"Geli Zhang":[0, 0],"Amy Reichhold":[ 0, 0],"Nick Onofrei":[0, 0],"Kalyn Koyanagi":[0, 0],"Kenny Nguyen":[0, 0],"Kelly Schombert":[0, 0]}	# [name, pos/neg, absent,第一个标记时间]
std_line = 20

class CISTInterface():
	def __init__(self, database = None, stdLine = 20):
		if database == None:
			print("Error: Failed to read data")
			sys.exit()
		
		# main GUI window
		self._topBar = tk.Tk()
		
		# main GUI window title
		self._topBar.title("Covid Infection Rate Tracker")
		
		# loading the roster file
		self.database = database
		self.namelist = []
		self.totalnum = len(self.database)
		self.count = 0
		self.positive = 0
		self.negative = 0
		self.absent = 0
		for i in self.database.keys():
			self.namelist.append(i)
		self.positive_num = 0
		self.countPositiveNumber()
		
		# loading deadline
		self.standard_line = stdLine
		
		# loading the current 
		self.current_positive_persentage = 0
		self.renewCurrentPercentage()
		
		# Gets native screen resolution width and height + ...
		self.screen_w = self._topBar.winfo_screenwidth()
		self.screen_h = self._topBar.winfo_screenheight()
		self.win_w = self.screen_w / 3;
		self.win_h = self.screen_h / 3;
		
		# Sets the self.window size to these dimensions
		self._topBar.geometry("%dx%d+%d+%d" % (self.win_w, self.win_h, 0, 0))
		
		# setup the canvas in GUI
		self.canvas = Canvas(self._topBar, width = self.win_w, height = self.win_h)
		
		# setting current percentage part
		self.canvas.create_text(self.win_w/20, self.win_h/15, text=("Current Covid positive percentage:"), font = ('Helvetica 20 bold'), anchor='w')
		
		# according standard line to show the percentage with color
		self.pertext = ""
		self._setPercentage()
		
		# setup the input button and export button
		self.canvas.create_text(self.win_w/20, self.win_h/1.4, text=("Input New Student Roster:"), font = ('Helvetica 20 bold'), anchor='w')
		self.canvas.create_text(self.win_w/20, self.win_h/1.2, text=("Export Current LOG File:"), font = ('Helvetica 20 bold'), anchor='w')
		self.inputButton = Button(self._topBar, text="Input", font = ('Helvetica 20 bold'), command = self._testaction)
		self.exportButton = Button(self._topBar, text="Export", font = ('Helvetica 20 bold'), command = self._testaction)
		self.inputButton.pack()
		self.exportButton.pack()
		self.inputButton.place(x = self.win_w-self.win_w/4, y = self.win_h/1.5)
		self.exportButton.place(x = self.win_w-self.win_w/4, y = self.win_h/1.25)
		
		# setup search box
		self.searchCurrentName = ""
		self.canvas.create_text(self.win_w/15, self.win_h/4, text = "Search name", font = ('Helvetica 13 bold'), anchor='w')
		self.search = SearchBox(self.canvas, callback = self._searchbox_callback)
		self.search.pack()
		self.search.place(x = self.win_w/4, y = self.win_h/5)
		
		# setup return button
		self.returnButton = Button(self._topBar, text="Return", font = ('Helvetica 20 bold'), command = self.return_command)
		self.returnButton.pack()
		self.returnButton.place(x = self.win_w-self.win_w/4, y = self.win_h/5)
		
		# pack up the canvas (ready to show up)
		self.canvas.pack()
	
	
	
# ------Percentage Number Part--------------------------------------------------------
	def _setPercentage(self):
		if (self.current_positive_persentage < self.standard_line):
			self.pertext = self.canvas.create_text(self.win_w-self.win_w/5, self.win_h/15, text=(str(self.current_positive_persentage) + '%'), fill="green", font=('Helvetica 30 bold'), anchor='w')
		else:
			self.pertext = self.canvas.create_text(self.win_w-self.win_w/5, self.win_h/15, text=(str(self.current_positive_persentage) + '%'), fill="red", font=('Helvetica 30 bold'), anchor='w')
	
	def _updatePercentage(self):
		if(self.current_positive_persentage < self.standard_line):
			self.canvas.itemconfigure(self.pertext, text = str(self.current_positive_persentage) + '%', fill='green')
		else:
			self.canvas.itemconfigure(self.pertext, text = str(self.current_positive_persentage) + '%', fill='red')
			
	def countPositiveNumber(self):
		self.positive_num = 0
		for j in self.database:
			if self.database[j][0]!=0:
				self.positive_num+=1
		self.renewCurrentPercentage()
				
	def renewCurrentPercentage(self):
		self.current_positive_persentage = round(self.positive_num/self.totalnum*100, 1)
		
# -----Search Box Part function-------------------------------------------------------
	# callback function for search box 
	# credit: https://github.com/arcticfox1919/tkinter-tabview
	def _searchbox_callback(self, text):
		print("text", text)
		if text == "":
#			清空positive，negative按钮
			self.canvas.delete("name_delete")
			if self.positive == 1:
				self.positiveButton.destroy()
			if self.negative == 1:
				self.negativeButton.destroy()
			if self.absent == 1:
				self.absentButton.destroy()
			print("none")
		if not text:
			self.search.update(None)
			return
		self.searchCurrentName = text
		tmp = []
		for i in self.namelist:
			if text == i:
				self.search._hide()
				self.searchCurrentName = text
				print("sea",self.searchCurrentName)
				self.search.update(None)
				return
			elif i.startswith(text):
				tmp.append(i)
		self.search.update(tmp)
		

# -----Return Button Part-----------------------------------------------------------	
#		warning：打错名字; absent
	def return_command(self):
		name = self.searchCurrentName
		check = False
		self.count += 1
#		print("return count",self.count)
		print("name", name)
		for i in self.database.keys():
			if name == i:
				check = True
		if check == False:
			print("Warning")
			print("pna", self.positive,self.negative, self.absent)
			self.canvas.delete("name_delete")
			messagebox.showwarning('Warning','please input correct name！')
			if self.positive == 1:
				self.positiveButton.destroy()
			if self.negative == 1:
				self.negativeButton.destroy()
			if self.absent == 1:
				self.absentButton.destroy()
			return 
		if self.count > 1:
			self.canvas.delete("name_delete")
			if name == None:
				print("none")
				self.canvas.delete("name_delete")
				self.positiveButton.destroy()
				self.negativeButton.destroy()
				self.absentButton.destroy()
		# selected name set upon buttons
		self.canvas.create_text(self.win_w/15, self.win_h/2.5, text = name, font = ('Helvetica 20 bold'),fill="blue" ,anchor='w', tags = "name_delete")
		
		# positive button set up
		self.positiveButton = Button(self._topBar, text="Positive", font = ('Helvetica 15 bold'), command = self.positiveAction)
		self.positiveButton.pack()
		self.positiveButton.place(x = self.win_w/4, y = self.win_h/2.1)
		self.positive = 1
		
		# negative button set up
		self.negativeButton = Button(self._topBar, text="Negative", font = ('Helvetica 15 bold'), command = self.negativeAction)
		self.negativeButton.pack()
		self.negativeButton.place(x = self.win_w/2, y = self.win_h/2.1)
		self.negative = 1
		
		# absent button set up
		self.absentButton = Button(self._topBar, text="Absent", font = ('Helvetica 15 bold'), command = self.absentAction)
		self.absentButton.pack()
		self.absentButton.place(x = self.win_w-self.win_w/4, y = self.win_h/2.1)
		self.absent = 1
		
		print(name, self.database[name][0])
		self._updateColorButton(name)
		
# ------Positive & Negative Buttons---------------------------------------------------
	def _updateColorButton(self, name):
		if self.database[name][0] == 1:
			self.positiveButton.configure(highlightbackground='red', fg='red')
			self.negativeButton.configure(highlightbackground='white', fg='black')
		else:
			self.positiveButton.configure(highlightbackground='white', fg='black')
			self.negativeButton.configure(highlightbackground='green', fg='green')
			
	def positiveAction(self):
		self.database[self.searchCurrentName][0] = 1
		self._updateColorButton(self.searchCurrentName)
		self.countPositiveNumber()
		self._updatePercentage()
		
	def negativeAction(self):
		self.database[self.searchCurrentName][0] = 0
		self._updateColorButton(self.searchCurrentName)
		self.countPositiveNumber()
		self._updatePercentage()
		
	def absentAction(self):
		self.database[self.searchCurrentName][1] += 1
		self.absentButton.destroy()
		print(self.database)
			
# ------Main Window Part------------------------------------------------------------
	def _testaction(self):
		# test function (removeable)
		self.current_positive_persentage+=3
		self._updatePercentage()
		
	def _turnOnGUI(self):
		self._topBar.mainloop()
		
	def _closeOffGUI(self):
		self._topBar.destroy()

# Testing
if __name__ == "__main__":
	main_window = CISTInterface(test_case, std_line)
	main_window._turnOnGUI()
	