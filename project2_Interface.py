'''
Graphic User Interface
Project 2
Created Date: 2/22/2022
Author: Kai Xiong

Required library: Tkinter
# How to install Tkinter: sudo apt-get install python3.7-tk

'''
import tkinter as tk
from tkinter import *
from tkinter import filedialog

# testing dataset here (you can delete after decide final version)
test_case = [["Kai Xiong", 0, 0],["Rebecca Hu", 0, 0],["Xiang Hao", 0, 0],["Austin Mello", 0, 0]]	# [name, pos/neg, absent]
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
		
		# loading deadline
		self.standard_line = std_line
		
		# loading the current 
		self.curr_pos_per = current_percentage
		
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
		if (self.curr_pos_per < self.standard_line):
			self.pertext = self.canvas.create_text(self.win_w-self.win_w/5, self.win_h/15, text=(str(self.curr_pos_per) + '%'), fill="green", font=('Helvetica 30 bold'), anchor='w')
		else:
			self.pertext = self.canvas.create_text(self.win_w-self.win_w/5, self.win_h/15, text=(str(self.curr_pos_per) + '%'), fill="red", font=('Helvetica 30 bold'), anchor='w')
		
		# setup the input button and export button
		self.canvas.create_text(self.win_w/20, self.win_h/5 + 150, text=("Input New Student Roster:"), font = ('Helvetica 20 bold'), anchor='w')
		self.canvas.create_text(self.win_w/20, self.win_h/3 + 150, text=("Export Current LOG File:"), font = ('Helvetica 20 bold'), anchor='w')
		
		self.confirmButton = Button(self._topBar, text="Input", font = ('Helvetica 20 bold'), command = self._testaction)
		self.confirmButton.pack()
		self.confirmButton.place(x = self.win_w-self.win_w/4, y = self.win_h/5 + 140)
		
		self.rejectButton = Button(self._topBar, text="Export", font = ('Helvetica 20 bold'), command = self._testaction)
		self.rejectButton.pack()
		self.rejectButton.place(x = self.win_w-self.win_w/4, y = self.win_h/3 + 140)
		
		# pack up the canvas (ready to show on)
		self.canvas.pack()
		
	def _updatePercentage(self):
		if(self.curr_pos_per < self.standard_line):
			self.canvas.itemconfigure(self.pertext, text = str(self.curr_pos_per) + '%', fill='green')
		else:
			self.canvas.itemconfigure(self.pertext, text = str(self.curr_pos_per) + '%', fill='red')
	
	def _testaction(self):
		print("button activate!!!\n")
		self.curr_pos_per+=1
		self._updatePercentage()
	
	def _turnOnGUI(self):
		self._topBar.mainloop()
	
	def _closeOffGUI(self):
		self._topBar.destroy()
		
		
		
		
# Testing		
if __name__ == "__main__":
	main_window = CISTInterface()
	main_window._turnOnGUI()