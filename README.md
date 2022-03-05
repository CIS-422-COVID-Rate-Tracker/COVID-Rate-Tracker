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
2. tkinter 
3. pickle

## File Manifest
*Software Files*
1. CIRT.py
2. Interface.py
3. search_box.py
4. student_data.py

*Data Files*
1. .student_data.pickle
2. test.txt

## Known Bugs and Fixes
TO-DO

## Credits
1. **"Software Engineering 10th Edition" Ian Sommerville:** UML reference and general Software methods.
2. **`requirments from interviews`** TO-DO
3. **Search_Box module** cited from github: `https://github.com/arcticfox1919/tkinter-tabview`
4. **`Other cites in student_data.py`** TO-DO
