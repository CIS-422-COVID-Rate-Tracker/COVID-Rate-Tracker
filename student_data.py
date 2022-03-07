"""
File Name:      student_data.py
Program Name:   COVID-Infection-Rate-Tracker
Class:          CIS 422 - Winter22 - University of Oregon
Team members:   Austin Mello
                Kai Xiong
                Rebecca Hu
                Xiang Hao

Author:         Xiang Hao

Date Created:   2/22/2022
Latest Modified: 3/4/2022

Descriptions: 
This file consists of student data management and input and export file logic.

For input_data() function: it is used to ask for a txt file that contains students information.
For get_data() function: it is used to extract dictionary from student data pickle file.
For numOfDays() function: it is used to get the difference between two days.
For days_for_isolation() function: it is used to calculate how many days the student has isolated.
For save_data() function: it is used to save dictionary to pickle file.
For export_daily_log_file() function: it is used to export the daily log file.
For export_data() function: it is used to export the file.

Code cited from: https://www.geeksforgeeks.org/python-program-to-find-number-of-days-between-two-given-dates/
                https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
                https://www.programiz.com/python-programming/datetime/current-datetime
"""


import os
from tkinter import filedialog, messagebox
import pickle
from datetime import date
from datetime import datetime


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
            return False
        
        # Warning message for importing new data
        warning_message = "Do you want to import "
        warning_message += str(file)
        warning_message += "?"
        
        student_file = open(file, "r")
        # File headers
        headers = student_file.readline().strip().split('\t')
        
        if headers != ['Full_Name   UO_ID   Email   Positive/Negative Absent/Not   Days_for_isolation   Date_added_for_testing_positive   Times_for_Absence']:
                warning_message_format = "Please check input file, the format is incorrect!"
                # Input file format waring
                format_warnning = messagebox.showerror(title="Error!", message=warning_message_format)
                return False
        
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
        
        # Populate dictionary with email as key
        for student in student_file:
            tab_num = str(student)
            if tab_num.count('\t') != 7:
                warning_message_format = "Please check input file, the format is incorrect!"
                # Input file format waring
                format_warnning = messagebox.showerror(title="Error!", message=warning_message_format)
                return False
            else:
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
            if str(student).count('\t') != 8:
                warning_message_format = "Please check input file, the format is incorrect!"
                # Input file format waring
                format_warnning = messagebox.showerror(title="Error!", message=warning_message_format)
                return False
            student = student.strip().split('\t')
            student[3] = int(student[3])
            student[4] = int(student[4])
            student[5] = int(student[5])
            student[7] = int(student[7])
            student_data[student[0]] = student
            
        student_file.close()

    save_data(student_data)
    

"""
Function to extract student dictionary from pickle file
"""
def get_data():
    # If there is no student data
    if os.path.getsize('.student_data.pickle') == 0:
        return False
    else:
        # Code from:
        # https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
        # Read from pickle file
        with open('.student_data.pickle', 'rb') as handle:
            data = pickle.load(handle)
        return data


"""
Function to calculate the difference of days between two given dates
"""
def numOfDays(date1, date2):
    return (date2-date1).days


"""
Function to get how many days the student who has isolated
"""
def days_for_isolation():
    # Get student dictionary
    students = get_data()
    
    # Get today's date
    # code from: https://www.programiz.com/python-programming/datetime/current-datetime
    today = date.today().strftime("%m/%d/%Y")
    
    today_date = today.split("/")
    date2 = date(int(today_date[2]), int(today_date[0]), int(today_date[1]))
    
    # Loop through each student to track how many days they have isolated
    for key in students:
        if students[key][5] != 0:
            added_date = students[key][6].split("/")
            date1 = date(int(added_date[2]), int(added_date[0]), int(added_date[1]))
            # Code from https://www.geeksforgeeks.org/python-program-to-find-number-of-days-between-two-given-dates/
            days = numOfDays(date1, date2)
            students[key][5] = str(days)
#           print("days", days)
        if int(students[key][5]) >= 14:
            students[key][3] = "0"
            students[key][5] = "0"
            students[key][6] = "0"
            student_data[key][3] = 0
            student_data[key][5] = 0
            student_data[key][6] = "0"
    
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
    with open('.student_data.pickle', 'wb') as handle:
        pickle.dump(student_data, handle, protocol=pickle.HIGHEST_PROTOCOL)


"""
Function to generate a daily log file about the information of the students to the user. And it can be used for the user to reload to continuously modify this file.
"""
def export_daily_log_file():
    # containing students' full name, 9-digit UO ID, Email address, sign for positive or negative, sign for absent or not, days has isolated, date added for testing positive, and date added for absent.
    
    # if database is empty, do nothing
    if not student_data:
        return
    
    date = str(datetime.now())
    
    path = "../COVID-Rate-Tracker/Log_Files"
    
    if not os.path.exists(path):
        os.mkdir("../COVID-Rate-Tracker/Log_Files")
#       os.mkdir("Log_Files")
    
    file = "../COVID-Rate-Tracker/Log_Files/Daily_log_file_" + date + ".txt"
    f = open(file, 'w+')
    
    title = "Full_Name      Email      Positive   Absent   Days_for_isolation\n"

    f.write(title)
    
    with open('.student_data.pickle', 'rb') as handle:
        data = pickle.load(handle)
        
        for each in data:
            if data[each][3] == 1 or data[each][4] ==1:
                if data[each][3] == 1:
                    data[each][3] = "x"
                if data[each][4] == 1:
                    data[each][4] = "x"
                string = ''
                string += str(data[each][0])
                string += "\t"
                string += str(data[each][2])
                string += "\t"
                string += str(data[each][3])
                string += "\t\t"
                string += str(data[each][4])
                string += "\t\t\t"
                string += str(data[each][5])
                string += "\n"
                f.write(string)
    f.close()


"""
Function to generate a file about the information of the students to the user. This will be called when the user clicks on the "Export" button.
"""
def export_data():
    # containing students' full name, 9-digit UO ID, Email address, sign for positive or negative, sign for absent or not, days has isolated, date added for testing positive, and date added for absent.
    # list of dates when student was called MM/DD/YY in order

    f = open("Student_Covid_Tracker.txt", 'w+')
    title = "Full_Name   UO_ID   Email   Positive/Negative   Absent/Not   Days_for_isolation   Date_added_for_testing_positive   Times_for_absence \n"

    f.write(title)
    
    with open('.student_data.pickle', 'rb') as handle:
        data = pickle.load(handle)
        time = ""
        for each in data:
            string = ''
            for info in data[each]:
                string += str(info)
                string += "\t"
            string += "\n"
            f.write(string)
    f.close()
    