from canvasapi import Canvas;
from datetime import datetime;
from bs4 import BeautifulSoup;
#cleans description of assignments
def removeHTMLtags(text):
    if(text == None):
        return ''
    return BeautifulSoup(text, "lxml").text

#creates a due date that can be compared 
def assignmentToDate(dueTime):
    return datetime(int(dueTime[0:4]),int(dueTime[5:7]),int(dueTime[8:10]))

def main():
    #get current date to compare future assignments.
    current = datetime.now()
    current = datetime(current.year,current.month,current.day)
    #get current user/api key and setup assignments.
    print("Please input your canvas API key. This can be created in your Canvas account settings. ")
    apiKey = input()
    canvas = Canvas("https://canvas.instructure.com",apiKey)
    user = canvas.get_current_user()
    assignmentsDueLater = []
    for course in user.get_courses():
        for assignment in course.get_assignments():
            #creates a duedate to compare to.
            dueTime = assignment.due_at
            if(dueTime != None):
                assignmentDate = assignmentToDate(dueTime)
                #adds assignment to list if it is due in the future
                if(assignmentDate > current):
                    assignmentsDueLater.append(assignment)
    print("Check each assignment to add? Y/N")
    answer = input()
    if(answer[0] == 'Y' or answer[0] == 'y'):
        #loops for all assignments, asking the user if they want to add it to their calendar. 
        #we do [:] in the array to be able to remove from it without interrupting the loop.
        for assignment in assignmentsDueLater[:]:
            print("\n\nAdd this assignment? Y/N")
            print(assignment.name)
            print(assignmentToDate(assignment.due_at))
            print(removeHTMLtags(assignment.description)[:300])
            answer = input()
            if(answer[0] == 'N' or answer[0] == 'n'):
                assignmentsDueLater.remove(assignment)
            print(chr(27) + "[2J")
    for x in assignmentsDueLater:
        print(x.name)

main()