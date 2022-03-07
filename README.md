# COVID-Rate-Tracker
## Install Instructions
Clone COVID Rate Tracker: `git clone https://github.com/CIS-422-COVID-Rate-Tracker/COVID-Rate-Tracker.git`
## Operation Instructions
### Preparing before execute CIRT software program
Create a roster file includes student infomation.
1. The roster must be a text file (.txt).
2. Every line represent one students infomation, and it should be tab-delimited.

*Example:*
 Full_Name  | UO_ID  | Email  | Positive/Negative | Absent/Not  | Days_for_isolation | Date_added_for_testing_positive | Times_for_Absence
 -------- | ------ | ------  | --  | -- | -- | -- | -- 
 Peter Parker  | 950000000 | pparker@uoregon.edu | 0 | 0 | 0 | 0 | 0 

### First time executing CIRT software program
1. From terminal navigate to COVID-Rate-Tracker directory.
2. Execute the program `python3 CIRT.py`.
3. Press `input` button on the GUI window.
4. Select prepared roster file.
5. Confirm all of student full name that is ready into the system.
6. The search bar will pop accosiative names when user typing with **capital letters**.
7. Other operation see User document.

### Subsequent System Usage (Same Roster)
1. From terminal navigate to COVID-Rate-Tracker directory.
2. Execute the program `python3 CIRT.py`.

### Subsequent System Usage (Using a New Roster)
1. Press `input` button on the GUI window.
2. Chose a new roster file.
3. The CIRT software system will reset all student infomation.

### How to modify data
1. After first executing CIRT software program with correctly inputed roster file, should be generate a `Student_Covid_Tracker.txt` in directory.
2. User can modify student infomation in `Student_Covid_Tracker.txt`.
3. Format Difference: With one more tab in each end of line than the initial prepare file.

## Dependencies
The COVID Rate Tracker relies on:
1. [python3.X](https://www.python.org/downloads/) 
2. [tkinter](https://docs.python.org/3/library/tkinter.html)
3. [pickle](https://docs.python.org/3/library/pickle.html)

## File Manifest
*Software Files*
1. CIRT.py
2. Interface.py
3. search_box.py
4. student_data.py

*Data Files*
1. .student_data.pickle
2. test.txt

## Known Bugs
1. Clean Button: If a user searches for a student, then searches for another student, then presses the clean button to remove the student status menu from the Main Window, the Postive, Negative, and Absent buttons will remain.  Under normal operations, the Clean button should remove these buttons as well.  The buttons no longer seem to have any function, however.  They just stay there until a new name is searched.
2. Window Size Matters: If the user changes the size of the window, some elements of the GUI will automatically re-orient themselves with the new window size, while some elements will not.
3. Usability concerns: The font color of the student name is hard to read against the background for colorblind individuals.

## Credits
1. **"Software Engineering 10th Edition" Ian Sommerville:** UML reference and general Software methods.
2. **Requirments from Interviews**
 - One of the interviewee wanted this system can delete the student who tested positive after 14 days. And we searched online and modified this number to 10 days since we follow the instruction from the CDC: https://www.cdc.gov/coronavirus/2019-ncov/your-health/quarantine-isolation.html
  - One of the interviewee wanted us to give the access of this system to students, however, after we talked about this to another interviewee, he concerned about the privacy of students if giving the access to the students. Therefore, we set the database to the host desktop not a cloud database.
4. **Search_Box module** cited from github: `https://github.com/arcticfox1919/tkinter-tabview`
5. **Other cites in student_data.py**:
 - https://www.geeksforgeeks.org/python-program-to-find-number-of-days-between-two-given-dates/
 - https://stackoverflow.com/questions/11218477/how-can-i-use-pickle-to-save-a-dict
 - https://www.programiz.com/python-programming/datetime/current-datetime

## Notes
1: Make sure that the program directory you download names COVID-Rate-Tracker. If the name of the program directory is not COVID-Rate-Tracker please change the name to COVID-Rate-Tracker.
