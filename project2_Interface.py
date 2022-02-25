'''
Graphic User Interface
Project 2
Created Date: 2/22/2022
Author: Kai Xiong，Rebecca Hu

Required library: Tkinter
# How to install Tkinter: sudo apt-get install python3.7-tk

'''

import tkinter as tk
from tkinter import *
from search_box import SearchBox
from tkinter import filedialog

# testing dataset here (you can delete after decide final version)
#test_case = [["Kai Xiong", 1, 0],["Rebecca Hu", 0, 0],["Xiang Hao", 1, 0],["Austin Mello", 0, 0], ["Nick Johnstone", 0, 0],["Jeager Jochimsen", 0, 0],["Haoran Zhang", 0, 0],["Geli Zhang", 0, 0],["Amy Reichhold", 0, 0],["Nick Onofrei", 0, 0],["Kalyn Koyanagi", 0, 0],["Kenny Nguyen", 0, 0],["Kelly Schombert", 0, 0]]	# [name, pos/neg, absent]
test_case = {"Kai Xiong":[1, 0],"Rebecca Hu":[0, 0],"Xiang Hao":[1, 0],"Austin Mello":[0, 0], "Nick Johnstone":[0, 0],"Jeager Jochimsen":[ 0, 0],"Haoran Zhang":[ 0, 0],"Geli Zhang":[ 0, 0],"Amy Reichhold":[ 0, 0],"Nick Onofrei":[0, 0],"Kalyn Koyanagi":[0, 0],"Kenny Nguyen":[0, 0],"Kelly Schombert":[0, 0]}	# [name, pos/neg, absent]
current_percentage = 10
std_line = 20

class CISTInterface():
	def __init__(self):
		# main GUI window
		self._topBar = tk.Tk()
		
		# main GUI window title
		self._topBar.title("Covid Infection Rate Tracker")
		
		# loading the roster file
		self.roster = test_case
		self.namelist = []
		self.totalnum = len(self.roster)
		self.count = 0
#		for i in range(self.totalnum):
#			self.namelist.append(self.roster[i][0])
		for i in self.roster.keys():
			self.namelist.append(i)
		print(self.namelist)
		self.positive_num = 0
		for j in self.roster:
			if self.roster[j][0]!=0:
				self.positive_num+=1
		
		# loading deadline
		self.standard_line = std_line
		
		# loading the current 
		self.current_positive_persentage = round(self.positive_num/self.totalnum*100, 1)
		
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
		if (self.current_positive_persentage < self.standard_line):
			self.pertext = self.canvas.create_text(self.win_w-self.win_w/5, self.win_h/15, text=(str(self.current_positive_persentage) + '%'), fill="green", font=('Helvetica 30 bold'), anchor='w')
		else:
			self.pertext = self.canvas.create_text(self.win_w-self.win_w/5, self.win_h/15, text=(str(self.current_positive_persentage) + '%'), fill="red", font=('Helvetica 30 bold'), anchor='w')
		
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
		self.canvas.create_text(self.win_w/15, self.win_h/4, text = "Search name", font = ('Helvetica 13 bold'), anchor='w')
		self.search = SearchBox(self.canvas, callback = self._searchbox_callback)
		self.search.pack()
		self.search.place(x = self.win_w/4, y = self.win_h/5)
		self.returnButton = Button(self._topBar, text="Return", font = ('Helvetica 20 bold'), command = self.return_command)
		self.returnButton.pack()
		self.returnButton.place(x = self.win_w-self.win_w/4, y = self.win_h/5)
		
		# pack up the canvas (ready to show on)
		self.canvas.pack()
		
	def _updatePercentage(self):
		if(self.current_positive_persentage < self.standard_line):
			self.canvas.itemconfigure(self.pertext, text = str(self.current_positive_persentage) + '%', fill='green')
		else:
			self.canvas.itemconfigure(self.pertext, text = str(self.current_positive_persentage) + '%', fill='red')
	
	def _testaction(self):
#		print("button activate!!!\n")
		self.current_positive_persentage+=3
		self._updatePercentage()
	
	def _turnOnGUI(self):
		self._topBar.mainloop()
	
	def _closeOffGUI(self):
		self._topBar.destroy()
		
	# callback function for search box 
	# credit: https://github.com/arcticfox1919/tkinter-tabview
	def _searchbox_callback(self, text):
#		print(text)
		if not text:
			self.search.update(None)
			return
		tmp = []
		for i in self.namelist:
			if i.startswith(text):
				tmp.append(i)
		self.search.update(tmp)
	
	def return_command(self):
		name = self.search._return_name()
		self.count += 1
		print("return count",self.count)
		print("name", name)
		if self.count > 1:
			self.canvas.delete("name_delete")
			if name == None:
				print("none")
				self.canvas.delete("name_delete")
				self.positiveButton.destroy()
				self.negativeButton.destroy()
				self.absentButton.destroy()
		self.canvas.create_text(self.win_w/15, self.win_h/2, text = name, font = ('Helvetica 15 bold'), anchor='w', tags = "name_delete")
		self.positiveButton = Button(self._topBar, text="Positive", font = ('Helvetica 15 bold'), command = self.return_command)
		self.positiveButton.pack()
		self.positiveButton.place(x = self.win_w/4, y = self.win_h/2.1)
		self.negativeButton = Button(self._topBar, text="Negative", font = ('Helvetica 15 bold'), command = self.return_command)
		self.negativeButton.pack()
		self.negativeButton.place(x = self.win_w/2, y = self.win_h/2.1)
		self.absentButton = Button(self._topBar, text="Absent", font = ('Helvetica 15 bold'), command = self.return_command)
		self.absentButton.pack()
		self.absentButton.place(x = self.win_w-self.win_w/4, y = self.win_h/2.1)
		print(name, self.roster[name][0])
		if self.roster[name][0] == 1:
			print("should change color")
			self.positiveButton.configure(highlightbackground='red')
		
		
# Testing
if __name__ == "__main__":
	main_window = CISTInterface()
	main_window._turnOnGUI()
