'''
File Name:      	Interface.py
Program Name:   	COVID-Infection-Rate-Tracker
Class:         		CIS 422 - Winter22 - University of Oregon
Group memebers: 	Austin Mello
					Kai Xiong
					Rebecca Hu
					Xiang Hao

Created Date: 		2/22/2022
Last Update Date: 	3/4/2022
Author: 			Kai Xiong
					Rebecca Hu

Required library: 	Tkinter
					SearchBox

How to install Tkinter: sudo apt-get install python3.10-tk

Cite Search Box class to help us to build searching function
SearchBox credit: 	cite the components to build the search box part:
					https://github.com/arcticfox1919/tkinter-tabview
'''
import tkinter as tk
import student_data
from datetime import date
from tkinter import *
from search_box import SearchBox
from tkinter import filedialog
from tkinter import messagebox

class CIRTInterface():
	def __init__(self, database = {}, stdLine = 20):
		# main GUI window
		self._mainWindow = tk.Tk()
		
		# main GUI window title name
		self._mainWindow.title("Covid Infection Rate Tracker")
		
		# loading the roster file
		if database:
			self.database = database
		else:
			# when database is empty, give an example to execute UI
			self.database = {"Empty": ['', '', '', 0, 0, 0, '[]   []']}
			
		# create a list with student full names
		self.namelist = []
		self.totalnum = len(self.database)
		for i in self.database.keys():
			self.namelist.append(i)
			
		# count how many positive students
		self.positive_num = 0
		
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
		self.win_w = self.screen_w / 2.7;
		self.win_h = self.screen_h / 2.7;
		
		# Sets the self.window size to these dimensions
		self._mainWindow.geometry("%dx%d+%d+%d" % (self.win_w, self.win_h, 0, 0))
		
		# setup the canvas in GUI
		self.canvas = Canvas(self._mainWindow, width = self.win_w, height = self.win_h)
		
		# setting current percentage part
		self.canvas.create_text(self.win_w/20, self.win_h/15, text=("Current Covid positive percentage:"), font = ('Helvetica 20 bold'), anchor='w')
		
		# according standard line to show the percentage with color
		self.pertext = ""
		if (self.current_positive_persentage < self.standard_line):
			self.pertext = self.canvas.create_text(self.win_w-self.win_w/5, self.win_h/15, text=(str(self.current_positive_persentage) + '%'), fill="green", font=('Helvetica 30 bold'), anchor='w')
		else:
			self.pertext = self.canvas.create_text(self.win_w-self.win_w/5, self.win_h/15, text=(str(self.current_positive_persentage) + '%'), fill="red", font=('Helvetica 30 bold'), anchor='w')
		
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
		self.searchPreviousName = ""
		self.canvas.create_text(self.win_w/15, self.win_h/4, text = "Search name", font = ('Helvetica 13 bold'), anchor='w')
		self.search = SearchBox(self.canvas, callback = self._searchbox_callback)
		self.search.pack()
		self.search.place(x = self.win_w/4, y = self.win_h/5)
		
		# setup return button
		self.returnButton = Button(self._mainWindow, text="Return", font = ('Helvetica 20 bold'), command = self.return_command)
		self.returnButton.pack()
		self.returnButton.place(x = self.win_w-self.win_w/2.6, y = self.win_h/5)
		
		# setup return button
		self.cleanButton = Button(self._mainWindow, text="Clean", font = ('Helvetica 20 bold'), command = self.clean_command)
		self.cleanButton.pack()
		self.cleanButton.place(x = self.win_w-self.win_w/5.5, y = self.win_h/5)
		
		# pack up the canvas (ready to show up)
		self.canvas.pack()
		
	
################################################################################
# ------Percentage Number Part--------------------------------------------------
################################################################################
	
	"""
	This function will renew the percentage part that showing in the main window
	It will auto change color when number bigger than standard line number.
	"""
	def _updatePercentage(self):
		if(self.current_positive_persentage < self.standard_line):
			self.canvas.itemconfigure(self.pertext, text = str(self.current_positive_persentage) + '%', fill='green')
		else:
			self.canvas.itemconfigure(self.pertext, text = str(self.current_positive_persentage) + '%', fill='red')
	
	"""
	This function renew the positive students number and renew the percentage number
	"""
	def renewCurrentPercentage(self):
		self.positive_num = 0
		for j in self.database:
			if self.database[j][3]!=0:
				self.positive_num+=1
		self.current_positive_persentage = round(self.positive_num/self.totalnum*100, 1)

################################################################################
# -----Search Box Part function-------------------------------------------------
################################################################################
		
	"""
	Callback function relate to search box _callback function.
	It will according the input string to show/hide the positive/negative/absent
	buttons and the student name.

	credit: https://github.com/arcticfox1919/tkinter-tabview
	"""
	def _searchbox_callback(self, text):
		if text == "":
#			清空positive，negative按钮
			self.canvas.delete("name_delete")
			if self.positive == 1:
				self.positiveButton.destroy()
			if self.negative == 1:
				self.negativeButton.destroy()
			if self.absent == 1:
				self.absentButton.destroy()
			self.searchPreviousName = None
			self.searchCurrentName = None
		if not text:
			self.search.update(None)
			return
		self.searchCurrentName = text
		tmp = []
		for i in self.namelist:
			if text == i:
				self.search._hide()
				self.searchCurrentName = text
				self.return_command()
				self.search.update(None)
				return
			elif i.startswith(text):
				tmp.append(i)
		self.search.update(tmp)
		
################################################################################
# -----Return Button Part-------------------------------------------------------		
################################################################################

	"""
	return_command function will build the student name and positive/negtive/absent buttons.
	When input name is error or none, it will hide those buttons and name in the main window.
	"""
	def return_command(self):
		
		if 'Empty' in self.database.keys():
			# if empty database, ask for input new one. (detect by searching example database)
			messagebox.showwarning(title = 'Warning', message = 'please input initial roster！')
			return
		elif self.searchPreviousName == self.searchCurrentName:
			# when search name is equal to the previous one, do nothing
			return
		
		name = self.searchCurrentName
		check = False
		self.count += 1
		
		for i in self.database.keys():
			if name == i:
				check = True
				
		if check == False:
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
		
		# change buttons color
		self._updateColorButton(name)
		# renew the previous name
		self.searchPreviousName = self.searchCurrentName
		
################################################################################
# ------Clean button part-------------------------------------------------------
################################################################################

	"""
	clean command will clean the string in the search box. and set current name string as none.
	"""
	def clean_command(self):
		self.search.delete(0, END)
		self.searchCurrentName = None
		self.searchPreviousName = None

################################################################################
# ------Positive & Negative Buttons---------------------------------------------
################################################################################
	
	"""
	This function will change the button's color according the student positive/negative status
	"""
	def _updateColorButton(self, name):
		if self.database[name][3] == 1:
			# positive
			self.positiveButton.configure(highlightbackground='red', fg='red')
			self.negativeButton.configure(highlightbackground='white', fg='black')
		else:
			# negative
			self.positiveButton.configure(highlightbackground='white', fg='black')
			self.negativeButton.configure(highlightbackground='green', fg='green')
	
	"""
	function active after click positive button. change student's status from negative to 
	positive and renew button color.
	"""
	def positiveAction(self):
		self.database[self.searchCurrentName][3] = 1
		self.database[self.searchCurrentName][5] = 1
		self._updateColorButton(self.searchCurrentName)
		self.renewCurrentPercentage()
		self._updatePercentage()
		self.database[self.searchCurrentName][6] = date.today().strftime("%m/%d/%Y")
		student_data.save_data(self.database)
	
	"""
	function active after click negative button. change student's status from poitive to 
	negative and renew button color.
	"""
	def negativeAction(self):
		self.database[self.searchCurrentName][3] = 0
		self._updateColorButton(self.searchCurrentName)
		self.renewCurrentPercentage()
		self._updatePercentage()
		self.database[self.searchCurrentName][6] = "1970/01/01"
		self.database[self.searchCurrentName][5] = 0
		student_data.save_data(self.database)
	
	"""
	function active after click absent button. Add times on the absent records and hide
	the button. Hiding button because prevent clicking multiple times on absent button.
	"""
	def absentAction(self):
		self.database[self.searchCurrentName][4] = 1
		self.database[self.searchCurrentName][7] += 1
		self.absentButton.destroy()
		student_data.save_data(self.database)

################################################################################
# ------File Input Part---------------------------------------------------------
################################################################################

	"""
	getInputFile function will input the new database file path to the file io module,
	Then renew the current database (in UI).
	"""
	def getInputFile(self):
		## here we should call file I/O function and get new database
		if student_data.input_data() != False:
			self.database = student_data.student_data
			self.namelist = []
			for i in self.database.keys():
				self.namelist.append(i)
			self.totalnum = len(self.database)
			self.renewCurrentPercentage()
			self._updatePercentage()
		
	
	"""
	generateLOGFile function will send a signal to let file io module to generate LOG
	file in directory.
	"""
	def generateLOGFile(self):
		## here we need to send a signal to let File I/O prints LOG File with current database

		student_data.export_daily_log_file()
#		print("LOG file generated")
		

################################################################################
# ------Main Window Part--------------------------------------------------------
################################################################################

	"""
	Start the GUI, create UI window.
	"""
	def _turnOnGUI(self):
		self._mainWindow.mainloop()
	
	"""
	turn off UI window.
	"""
	def _closeOffGUI(self):
		self._mainWindow.destroy()
		