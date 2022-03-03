from Interface import CISTInterface
import student_data


def main():
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
		students = None
	
	main_UI = CISTInterface(database = students, stdLine = 20)
	main_UI._turnOnGUI()
	student_data.export_data()
	
	
	
if __name__ == "__main__":
	main()
