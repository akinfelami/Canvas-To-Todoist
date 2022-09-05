import requests
import os
import json
from todoist.api import TodoistAPI
import datetime as time
import sys
from classes import Classes



# Will update date if a different date is found on a Canvas assignment compared to what is on that Todoist task.
UPDATE_DUE_DATE = True

# Will NOT create a Todoist task if the Canvas assignment is past due and was NOT submitted.
PAST_DUE = True

# Print Task/Project messages in console.
PRINT_MESSAGE = True
api = TodoistAPI("6f61895728ce2c2ab9ea51cc3917a35b913a7e0b")

class Class:
    def __init__(self, courseName="", courseID="", projID = "0"):
        self.name = courseName
        self.id = courseID
        self.projectID = projID
        self.assignments = []

def printMessage(print):
    if print:
        sys.stdout = sys.__stdout__
    else:
        sys.stdout = open(os.devnull, 'w')

# def loadKeys():
#     try:
#         with open("keys.txt", "r") as file:
#             keys = json.load(file)
#         return keys
#     except:
#         print("Could not find API key file. Please run import_classes.py first or make sure keys.txt is in the root directory.")

# Update keys file with project IDs

canvasCourses = Classes()

def updateCourses(courses):
    courseList =  canvasCourses.getCourses()
    for course in courses:
        courseList[course.id] = [course.name, course.projectID]




def pullSources():
    canvasAPI = "9713~PyTkUiMzVabmLAerxWckIPQ8uYyK2kytisQ79UP0GRwxwXqsehQoCtHGV0iCctZw"
    todoistAPI = "6f61895728ce2c2ab9ea51cc3917a35b913a7e0b"
    #  canvasAPI = Classes.getCanvasKey
    # todoistAPI = Classes.getTodoistKey
    courseList = []
    projectList = {}
    
    canvasCourses.getInfo()

    header = {"Authorization": "Bearer " + canvasAPI}

    parameter = {'per_page': 9999, 'include': 'submission'}
    for ID, course in canvasCourses.getCourses().items():
        try:
       
            assignments = requests.get("https://canvas.instructure.com/api/v1/courses/"+str(ID)+"/assignments", headers=header, params=parameter).json()
            newCourse = Class(course[0], str(ID), str(course[1]))
            for assignment in assignments:
        
                if not assignment['submission']['submitted_at']:
                    newCourse.assignments.append([assignment['name'], assignment['due_at']])
                    
            courseList.append(newCourse)
        except Exception as e:
            print(e)
            print(f"Error requesting {course[0]} from Canvas API")
        
        
    # api = TodoistAPI(todoistAPI)
    # api.sync()
    # projectList = createProjects(courseList, api)
    api.sync()
    createTasks(api, courseList)


# def createProjects(courseList, todoistAPI):
#     for course in courseList:      
#         for project in todoistAPI.state['projects']:
#             found = False
#             if course.projectID == str(project['id']):
#                 found = True
#                 break
#         if not found:
#             print("Project not found. Adding", course.name, "as a project")
#             todoistAPI.projects.add(course.name)
#             todoistAPI.commit()

#     todoistAPI.commit()
#     updateCourses(courseList)
#     return courseList


def createTasks(todoistAPI, courseList):
    for course in courseList:
        for assignment in course.assignments:
            try:
                task = api.add_item(
                    content=assignment[0],
                    due_string=assignment[1],
                    due_lang='en',
                    priority=1,
                )
                print(task)
            except Exception as error:
                print(error)

    # for project in projectList:
    #     for assignment in project.assignments:
    #         found = False
    #         for task in todoistAPI.projects.get_data(project.projectID)['items']:
    #             if assignment[0].strip() == task['content'].strip():
    #                 if assignment[1] != None and assignment[1] != task['due']['date'] and UPDATE_DUE_DATE:
    #                     print("Newer date found on",
    #                           assignment[0], "Updating date")
    #                     todoistAPI.items.update(
    #                         task['id'], due={'string': assignment[1], 'date': assignment[1]})
    #                 found = True
    #         if not found:
    #             if assignment[1] != None and assignment[1] < time.datetime.isoformat(time.datetime.now()) and PAST_DUE:
    #                 print(
    #                     assignment[0], "is past due and not submitted. Not adding task")
    #             else:
    #                 print("Could not find task",
    #                       assignment[0], "adding new task to project", project.name)
    #                 todoistAPI.items.add(assignment[0].strip(), due={
    #                                      "date": assignment[1]}, project_id=project.projectID)
    todoistAPI.commit()

   
if __name__ == "__main__":
    a= Class()
    pullSources()
    print(a.assignments)
    # printMessage(PRINT_MESSAGE)
    # apiKeys = loadKeys()
    # pullSources(apiKeys)
