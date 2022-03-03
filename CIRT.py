from Interface import CISTInterface
import student_data


def main():
	
	student_data.input_data("Student_Covid_Tracker.txt")
	print(student_data.student_data)
	
	
main()