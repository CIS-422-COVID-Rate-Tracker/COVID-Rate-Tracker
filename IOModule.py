import Student

studentList = []



def importNewData(filePath=""):
    #Check if the user provided a file path.  If not, defer to a hard-coded, default file.
    if filePath == "":
        print("File path not specified.  Using the test roster.")
        filePath = "./test_roster.txt"

    #begin reading from the file
    with open(filePath, "r") as file:
        for i in file:
            #use python's split function to tokenize the values up by their tabs
            i = i.split("\t")

            #Snip the newline character off the last entry:
            i[1] = i[1].strip("\n")

            studentList.append(Student.Student(i))
            
    # Create the list and return.
    studentNames = makeNameList(studentList)

    #print(studentNames)
    return studentNames

def makeNameList(classList):
#Utility function to take a list of Student classes and return a list of corresponding names.
    
    returnList = []
    for obj in studentList:
        returnList.append(obj.name)

    return returnList

# Testing
if __name__ == "__main__":
    importNewData()