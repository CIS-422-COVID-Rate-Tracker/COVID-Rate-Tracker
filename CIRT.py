'''
File Name:      	CIRT.py
Program Name:   	COVID-Infection-Rate-Tracker
Class:         		CIS 422 - Winter22 - University of Oregon
Group memebers: 	Austin Mello
					Kai Xiong
					Rebecca Hu
					Xiang Hao

Created Date: 		3/1/2022
Last Update Date: 	3/4/2022

Author: 			Kai Xiong
					Xiang Hao

Modified: Rebecca Hu

Required library: 	Interface.py
					student_data.py
'''

from Interface import CIRTInterface
import student_data

def main():
	# loading data with dictionary
	students = student_data.student_data
	
	# try to load the last execution saved file, if not exists, then set none.
	try:
		with open('Student_Covid_Tracker.txt'):
			student_data.input_data(path = "Student_Covid_Tracker.txt")
			# loop for check isolate date and reset absent value
			for i in students.keys():
				students[i][4] = 0
			student_data.days_for_isolation()
							
	except IOError:
		students = {}
	
	# turn on the GUI Module
	main_UI = CIRTInterface(database = students, stdLine = 20)
	main_UI._turnOnGUI()
	
	# generate Saved/boot file.
	# if database is empty, ignore export action
	if student_data.student_data:
		student_data.export_data()
	
if __name__ == "__main__":
	main()
	
