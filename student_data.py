"""
File Name:      student_data.py
Program Name:   COVID-Infection-Rate-Tracker
Class:          CIS 422 - Winter22 - University of Oregon
Date Created:   2/27/2022
Authors:        Austin Mello
                Kai Xiong
                Rebecca Hu
                Xiang Hao

Descriptions: 
This file consists of student data management and input and export file logic.

For input_data() function: it is used to ask for a txt file that contains students information.
For student_search() function: it is used to match the student whose name is searched in the search bar of UI interface.
For student_absent() function: it is used to record student who is absent in class.
For get_data() function: it is used to extract dictionary from student data pickle file.
For days_for_isolation() function: it is used to calculate how many days the student has isolated.
For save_data() function: it is used to save dictionary to pickle file.
For export_daily_log_file() function: it is used to export the daily log file.
For export_data() function: it is used to export the file.

"""


import os
from tkinter import filedialog, messagebox
import pickle
from datetime import date


# Global student data dictionary
student_data = {}


"""
Function to allow user to import data
This function is called when "input data" button is clicked
"""
def input_data(path = None):
    # file input
    if path == None:
        # Allows user to input text file
        file = filedialog.askopenfilename(
            title="Select a tab-delimited file with student data",
            filetypes=[('textfiles', '*.txt')])
        
        # If cancel button
        if not file: 
            return
        
#       # Warning message for importing new data
#       warning_message = "Do you want to import "
#       warning_message += str(file)
#       warning_message += "?"
        
        # Check if student data exists
        if get_data():
            warning_message = "The following student data will be overridden. Do you want to continue?\n\n"
            current_students = get_data()
            # List all current students being saved by system
            for student, student_info in current_students.items():
                warning_message += student_info[0]
                warning_message += '\n'
                
        # Override warning
        confirm_override = messagebox.askyesno(
            title="Warning", 
            message=warning_message,
            default=messagebox.YES)
        
        student_file = open(file, "r")
        # File headers
        headers = student_file.readline().strip().split('\t')
        
        # Populate dictionary with email as key
        for student in student_file:
            student = student.strip().split('\t')
            student[3] = int(student[3])
            student[4] = int(student[4])
            student[5] = int(student[5])
            student[7] = int(student[7])
            student_data[student[0]] = student
            
        student_file.close()
        
    # Reading file
    else:
        student_file = open(path, "r")
        # File headers
        headers = student_file.readline().strip().split('\t')

        # Populate dictionary with email as key
        for student in student_file:
            student = student.strip().split('\t')
            student[3] = int(student[3])
            student[4] = int(student[4])
            student[5] = int(student[5])
            student[7] = int(student[7])
            student_data[student[0]] = student
            
        student_file.close()

    save_data(student_data)
        

#"""
#Function to match the student inputed in the search bar, where the parameters are email and status. Since email is unique, we use the email as the connected information.
#This function is called from project2_interface.py.
#
#Parameters
#_________
#email: string
#   String of unique student email
#status: string
#   String of type of status that was raised
#   "positive" or "negative"
#"""
#def student_search(full_name, status):
#   # Get student dictionary
#   students = get_data()
#   print(students)
#
#   # Find student data through email as key
#   student = students[full_name]
#
#   # Change the status of (negative or positive) by adding "x" or not
#   if status == "negative":
#       student[3] = ""
#   elif status == 'positive':
#       student[3] = "x"
#   else:
#       print("Status type must be 'negative' or 'positive'")
#       return
#   
#   # Track dates that student was called due to positive result in format MM/DD/YYY. Track days that student has isolated.
#   if status == "positive":
#       student[6].append(date.today().strftime("%m/%d/%Y"))
#       student[5] += 1
#
#   print("student called", student)
#
#   # Save new data
#   save_data(students)
#
#
#"""
#Function to mark student who is absent in class, where the parameters are email and absent. Since email is unique, we use the email as the connected information.
#This function is called from project2_interface.py.
#
#Parameters
#_________
#email: string
#   String of unique student email
#absent: string
#   String of type of absence
#"""
#def student_absent(full_name, absent):
#   # Get student dictionary
#   students = get_data()
#   
#   # Find student data through email as key
#   student = students[full_name]
#   
#   # Add an "x" sign to the absent part if the student is absent, and the user does not know whether this student tests positive or negative.
#   if absent == "absent" and student[4] == None and student[3] == None:
#       student[4] = "x"
#   elif absent == "absent" and student[4] != None and student[3] == None:
#       student[4] = ""
#   else:
#       print("Absent type must be 'absent' or 'present'")
#       return
#   
#   # Track dates that student was called due to absence in format MM/DD/YYY
#   if absent == "absent" and student[4] == None and student[3] == None:
#       student[6].append(date.today().strftime("%m/%d/%Y"))
#
#   print("student called", student)
#   
#   # Save new data
#   save_data(students)
    

"""
Function to extract student dictionary from pickle file
"""
def get_data():
    # If there is no student data
    if os.path.getsize('student_data.pickle') == 0:
        return False
    else:
        # Code from:
        # https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
        # Read from pickle file
        with open('student_data.pickle', 'rb') as handle:
            data = pickle.load(handle)
        return data


"""
Function to get how many days the student who has isolated
"""
def days_for_isolation():
    # Get student dictionary
    students = get_data()
    
    # Get today's date
    today = date.today().strftime("%m/%d/%Y")
    
    # Loop through each student to track how many days they have isolated
    for key in students:
        if students[key][5] != 0:
            # Code from https://www.geeksforgeeks.org/python-program-to-find-number-of-days-between-two-given-dates/
            days = (today - students[key][6]).days
            students[key][6] = "days"
    
    # Save new data
    save_data(students)


"""
Function to save student dictionary to pickle file

Parameters
__________
student_data: dict
    Dictionary containing student data
"""
def save_data(student_data):
    # Code from
    # https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
    # Save to pickle file
    with open('student_data.pickle', 'wb') as handle:
        pickle.dump(student_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


#"""
#Function to generate a daily log file about the information of the students to the user. And it can be used for the user to reload to continuously modify this file.
#"""
#def export_daily_log_file():
#   # containing students' full name, 9-digit UO ID, Email address, sign for positive or negative, sign for absent or not, days has isolated, date added for testing positive, and date added for absent.
#   f = open("Daily_log_file.txt", 'w+')
#   title = "Full_Name   UO_ID   Email   Positive/Negative   Absent/ot   Days_for_isolation   Date_added_for_testing_positive   Date_added_for_absence \n"
#
#   f.write(title)
#   
#   with open('student_data.pickle', 'rb') as handle:
#       data = pickle.load(handle)
#       time = ""
#       print(data)
#       for each in data:
#           for info in data[each]:
#               print("info",info)
#               string = ''
#               if isinstance(info, list):
#                   time = str(info)
#               else:
#                   string += str(info)
#                   string += "\t"
#               f.write(string)
#   f.close()
    

"""
Function to generate a file about the information of the students to the user. This will be called when the user clicks on the "Export" button.
"""
def export_data():
    # containing students' full name, 9-digit UO ID, Email address, sign for positive or negative, sign for absent or not, days has isolated, date added for testing positive, and date added for absent.
    # list of dates when student was called MM/DD/YY in order

    f = open("Student_Covid_Tracker.txt", 'w+')
    title = "Full_Name   UO_ID   Email   Positive/Negative   Absent/Not   Days_for_isolation   Date_added_for_testing_positive   Times_for_absence \n"

    f.write(title)
    
    with open('student_data.pickle', 'rb') as handle:
        data = pickle.load(handle)
        time = ""
        print(data)
        for each in data:
            string = ''
            for info in data[each]:
                string += str(info)
                string += "\t"
            string += "\n"
            f.write(string)
    f.close()

def main():
    input_data("Student_Covid_Tracker.txt")
#   export_daily_log_file()
    print(student_data)

if __name__ == "__main__":
    main()