from tkinter import E
import requests
import os
import json
from todoist_api_python.api import TodoistAPI
import datetime as time
import sys
from canvas import Canvas



# Will update date if a different date is found on a Canvas assignment compared to what is on that Todoist task.
UPDATE_DUE_DATE = True

# Will NOT create a Todoist task if the Canvas assignment is past due and was NOT submitted.
PAST_DUE = True

# Print Task/Project messages in console.
PRINT_MESSAGE = True
api = TodoistAPI("6f61895728ce2c2ab9ea51cc3917a35b913a7e0b")

class Class:
    def __init__(self, courseName="", courseID="", projID = "1234567890"):
        self.name = courseName
        self.id = courseID
        self.projectID = projID
        self.assignments = []

def printMessage(print):
    if print:
        sys.stdout = sys.__stdout__
    else:
        sys.stdout = open(os.devnull, 'w')



canvasCourses = Canvas()

def updateCourses(courses):
    courseList =  canvasCourses.getCourses()
    for course in courses:
        courseList[course.id] = [course.name, course.projectID]




def pullSources():

    
    canvasCourses.getInfo()
    # It is import to call getInfo because initilalizing class canvas intiliazes 
    # both canvas key and todoist keys to an empty string
    canvasAPI = canvasCourses.getCanvasKey()
    todoistAPI = canvasCourses.getTodoistKey()
    courseList = []

    header = {"Authorization": "Bearer " + canvasAPI}

    parameter = {'per_page': 9999, 'include': 'submission'}
    for ID, course in canvasCourses.getCourses().items():
        try:
       
            assignments = requests.get("https://canvas.instructure.com/api/v1/courses/"+str(ID)+"/assignments", 
            headers=header, params=parameter).json()
            newCourse = Class(course[0], str(ID), str(course[1]))
            print(assignments)
            for assignment in assignments:
                print(assignment)
                if not assignment['submission']['submitted_at']:
                    newCourse.assignments.append([assignment['name'], assignment['due_at'], assignment['submission']['submitted_at']])   
            courseList.append(newCourse)
        except Exception as e:
            print(e)
            print(f"Error requesting {course[0]} from Canvas API")
        
  
    createProjects(courseList, api)
    createTasks(api, courseList)


#---------------------------------------------------------

# The folllowing are not class methods


def createProjects(courseList, todoistAPI):
    project_names = []
    try:
        projects = todoistAPI.get_projects()
        for project in projects:
            project_names.append(project.name)
    except Exception as error:
            print(error)

    
    for course in courseList:
        if course.name in project_names:
            print('Project already exists. Moving on...')  
        else:
            try:
                new_project = api.add_project(name=course.name)
                course.projectID = new_project.id
            except Exception as e:
                print(e)
            
     
    return courseList


def createTasks(todoistAPI, courseList):
    for course in courseList:
        for assignment in course.assignments:
            if assignment[1] != None and assignment[1] < time.datetime.isoformat(time.datetime.now()):
                print('Assignment is past due..')
                if assignment[2] == 'None':
                    print('Assignment is past due and not submitted')
                    return 
            else:
                print('Adding assignment to task')
                try:
                    task = api.add_task(
                        content=assignment[0],
                        due_string=assignment[1],
                        due_lang='en',
                        priority=1,
                        project_id=course.projectID
                    )
                    
                except Exception as error:
                    print(error)

   

   
if __name__ == "__main__":
    a= Class()
    pullSources()