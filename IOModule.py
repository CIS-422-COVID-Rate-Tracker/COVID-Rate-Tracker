import Student

studentList = []

def importNewData(filePath=""):
    #Check if the user provided a file path.  If not, defer to a hard-coded, default file.
    if filePath == "":
        filePath = "./testRoster.txt"

    #begin reading from the file
    with open(filePath, "r") as file:
        for i in file:
            #use python's split function to tokenize the values up by their tabs
            i = i.split("\t")
            #create a new Student class and add the data.  I don't know if this
            #will actually work yet, because python is an inferior language that
            #doesn't declare its variable types upon declaration.
            studentList.append(Student(i))