class Student:
    def __init__(self, studentData):
        self.name = studentData[0]
        self.email = studentData[1]
        self.isolation = 0
        self.endIsolation = 0

    def toggleIsolation(self):
        if self.isolation == 0:
            self.isolation = 1
            #TODO: Push onto isolation queue.
        else:
            self.isolation = 0;
            #TODO: Pop from isolation queue.
            #TODO: Puch onto follow-up queue.