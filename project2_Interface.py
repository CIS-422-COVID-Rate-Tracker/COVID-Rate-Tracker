'''
Graphic User Interface
Project 2
Created Date: 2/22/2022
Last Update Date: 2/28/2022
Author: Kai Xiong，Rebecca Hu

Required library: Tkinter
# How to install Tkinter: sudo apt-get install python3.7-tk

credit: cite the components to build the search box part:
		https://github.com/arcticfox1919/tkinter-tabview
'''
import tkinter as tk
from tkinter import *
from search_box import SearchBox
from tkinter import filedialog
from tkinter import messagebox

# testing dataset here (you can delete after decide final version)
test_case = {"Kai Xiong":[1, 1],"Rebecca Hu":[0, 0],"Xiang Hao":[1, 0],"Austin Mello":[0, 0], "Nick Johnstone":[0, 0],"Jeager Jochimsen":[0, 0],"Haoran Zhang":[0, 0],"Geli Zhang":[0, 0],"Amy Reichhold":[ 0, 0],"Nick Onofrei":[0, 0],"Kalyn Koyanagi":[0, 0],"Kenny Nguyen":[0, 0],"Kelly Schombert":[0, 0]}	# [name, pos/neg, absent,第一个标记时间]
std_line = 20

class CISTInterface():
	def __init__(self, database = None, stdLine = 20):
		# main GUI window
		self._mainWindow = tk.Tk()
		
		# main GUI window title name
		self._mainWindow.title("Covid Infection Rate Tracker")
		
		# loading the roster file
		if database == None:
			# when database is empty, give an example to execute UI
			self.database = {"Empty": [0,0]}
		else:
			self.database = database
		# create a list with student full names
		self.namelist = []
		self.totalnum = len(self.database)
		for i in self.database.keys():
			self.namelist.append(i)
		# count how many positive students
		self.positive_num = 0
		self.countPositiveNumber()
		
		# setup flags of positive/negative/absent buttons
		self.count = 0
		self.positive = 0
		self.negative = 0
		self.absent = 0
		
		# loading deadline
		self.standard_line = stdLine
		
		# loading the current 
		self.current_positive_persentage = 0
		self.renewCurrentPercentage()
		
		# Gets native screen resolution width and height + ...
		self.screen_w = self._mainWindow.winfo_screenwidth()
		self.screen_h = self._mainWindow.winfo_screenheight()
		self.win_w = self.screen_w / 3;
		self.win_h = self.screen_h / 3;
		
		# Sets the self.window size to these dimensions
		self._mainWindow.geometry("%dx%d+%d+%d" % (self.win_w, self.win_h, 0, 0))
		
		# setup the canvas in GUI
		self.canvas = Canvas(self._mainWindow, width = self.win_w, height = self.win_h)
		
		# setting current percentage part
		self.canvas.create_text(self.win_w/20, self.win_h/15, text=("Current Covid positive percentage:"), font = ('Helvetica 20 bold'), anchor='w')
		
		# according standard line to show the percentage with color
		self.pertext = ""
		self._setPercentage()
		
		# setup the input button
		self.canvas.create_text(self.win_w/20, self.win_h/1.4, text=("Input New Student Roster:"), font = ('Helvetica 20 bold'), anchor='w')
		self.inputButton = Button(self._mainWindow, text="Input", font = ('Helvetica 20 bold'), command = self.getInputFile)
		self.inputButton.pack()
		self.inputButton.place(x = self.win_w-self.win_w/4, y = self.win_h/1.5)
		
		# setup the export button
		self.canvas.create_text(self.win_w/20, self.win_h/1.2, text=("Export Current LOG File:"), font = ('Helvetica 20 bold'), anchor='w')
		self.exportButton = Button(self._mainWindow, text="Export", font = ('Helvetica 20 bold'), command = self.generateLOGFile)
		self.exportButton.pack()
		self.exportButton.place(x = self.win_w-self.win_w/4, y = self.win_h/1.25)
		
		# setup search box
		self.searchCurrentName = ""
		self.canvas.create_text(self.win_w/15, self.win_h/4, text = "Search name", font = ('Helvetica 13 bold'), anchor='w')
		self.search = SearchBox(self.canvas, callback = self._searchbox_callback)
		self.search.pack()
		self.search.place(x = self.win_w/4, y = self.win_h/5)
		
		# setup return button
		self.returnButton = Button(self._mainWindow, text="Return", font = ('Helvetica 20 bold'), command = self.return_command)
		self.returnButton.pack()
		self.returnButton.place(x = self.win_w-self.win_w/3, y = self.win_h/5)
		
		# setup return button
		self.cleanButton = Button(self._mainWindow, text="Clean", font = ('Helvetica 20 bold'), command = self.clean_command)
		self.cleanButton.pack()
		self.cleanButton.place(x = self.win_w-self.win_w/6, y = self.win_h/5)
		
		# pack up the canvas (ready to show up)
		self.canvas.pack()
		
	
################################################################################
# ------Percentage Number Part--------------------------------------------------
################################################################################

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

################################################################################
# -----Search Box Part function-------------------------------------------------
################################################################################
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
#				print("sea",self.searchCurrentName)
				self.return_command()
				self.search.update(None)
				return
			elif i.startswith(text):
				tmp.append(i)
		self.search.update(tmp)
		
################################################################################
# -----Return Button Part-------------------------------------------------------		
################################################################################

	def return_command(self):
		# if empty database, ask for input new one
		if 'Empty' in self.database.keys():
			messagebox.showwarning(title = 'Warning', message = 'please input initial roster！')
			return
		
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
		self.positiveButton = Button(self._mainWindow, text="Positive", font = ('Helvetica 15 bold'), command = self.positiveAction)
		self.positiveButton.pack()
		self.positiveButton.place(x = self.win_w/4, y = self.win_h/2.1)
		self.positive = 1
		
		# negative button set up
		self.negativeButton = Button(self._mainWindow, text="Negative", font = ('Helvetica 15 bold'), command = self.negativeAction)
		self.negativeButton.pack()
		self.negativeButton.place(x = self.win_w/2, y = self.win_h/2.1)
		self.negative = 1
		
		# absent button set up
		self.absentButton = Button(self._mainWindow, text="Absent", font = ('Helvetica 15 bold'), command = self.absentAction)
		self.absentButton.pack()
		self.absentButton.place(x = self.win_w-self.win_w/4, y = self.win_h/2.1)
		self.absent = 1
		
		print(name, self.database[name][0])
		self._updateColorButton(name)
		
################################################################################
# ------Clean button part-------------------------------------------------------
################################################################################

	def clean_command(self):
		self.search.delete(0, END)
		self.searchCurrentName = None

################################################################################
# ------Positive & Negative Buttons---------------------------------------------
################################################################################

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

################################################################################
# ------File Input Part---------------------------------------------------------
################################################################################

	def getInputFile(self):
		rosterFile = filedialog.askopenfile(initialdir = "", title = "Please chose your roster file")
		## here we should call file I/O function and get new database
#		self.database = # function that reurn new database
		## Then renew the other attributes
#		self.namelist = []
#		for i in self.database.keys():
#			self.namelist.append(i)
#		self.totalnum = len(self.database)
#		self.countPositiveNumber()
#		self.renewCurrentPercentage()
		
	def generateLOGFile(self):
		## here we need to send a signal to let File I/O prints LOG File with current database
		# fileIO.printLOGFile(self.database)
		print("LOG file generated")
		

################################################################################
# ------Main Window Part--------------------------------------------------------
################################################################################

	def _turnOnGUI(self):
		self._mainWindow.mainloop()
		
	def _closeOffGUI(self):
		self._mainWindow.destroy()

# Testing
if __name__ == "__main__":
	main_window = CISTInterface(test_case, std_line)
	main_window._turnOnGUI()
	