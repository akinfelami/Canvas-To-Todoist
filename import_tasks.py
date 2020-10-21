import requests
import os
import json
from todoist.api import TodoistAPI
import datetime as time
import sys

# Will update date if a different date is found on a Canvas assignment compared to what is on that Todoist task.
UPDATE_DUE_DATE = True

# Will NOT create a Todoist task if the Canvas assignment is past due and was NOT submitted.
PAST_DUE = True

# Print Task/Project messages in console.
PRINT_MESSAGE = True

def printMessage(print):
    if print:
        sys.stdout = sys.__stdout__
    else:
        sys.stdout = open(os.devnull, 'w')

def loadKeys():
    try:
        with open("keys.txt", "r") as file:
            keys = json.load(file)
        return keys
    except:
        print("Could not find API key file. Please run import_classes.py first or make sure keys.txt is in the root directory.")


def pullSources(keys):
    canvasAPI = keys['Canvas']
    todoistAPI = keys['Todoist']
    assignmentList = {}
    projectList = {}

    header = {"Authorization": "Bearer " + canvasAPI}
    parameter = {'per_page': 9999, 'include': 'submission'}
    for ID, course in keys['Courses'].items():
        assignments = requests.get("https://canvas.instructure.com/api/v1/courses/" +
                                   ID+"/assignments", headers=header, params=parameter).json()
        for assignment in assignments:
            if not assignment['submission']['submitted_at']:
                if course not in assignmentList:
                    assignmentList[course] = [
                        [assignment['name'], assignment['due_at']]]
                else:
                    assignmentList[course].append(
                        [assignment['name'], assignment['due_at']])

    api = TodoistAPI(todoistAPI)
    api.sync()
    projectList = createProjects(assignmentList, api)
    api.sync()
    createTasks(assignmentList, api, projectList)


def createProjects(assignmentList, todoistAPI):
    projectList = {}
    for course in assignmentList:
        for project in todoistAPI.state['projects']:
            found = False
            if course in project['name']:
                projectList[course] = project['id']
                found = True
                break
        if not found:
            print("Project not found. Adding", course, "as a project")
            project = todoistAPI.projects.add(course)
            projectList[course] = project['id']
    todoistAPI.commit()
    return projectList


def createTasks(assignmentList, todoistAPI, projectList):
    for course, assignments in assignmentList.items():
        for assignment in assignments:
            found = False
            for task in todoistAPI.projects.get_data(projectList[course])['items']:
                if assignment[0].strip() == task['content'].strip():
                    if assignment[1] != None and assignment[1] != task['due']['date'] and UPDATE_DUE_DATE:
                        print("Newer date found on",
                              assignment[0], "Updating date")
                        todoistAPI.items.update(
                            task['id'], due={'string': assignment[1], 'date': assignment[1]})
                    found = True
            if not found:
                if assignment[1] != None and assignment[1] < time.datetime.isoformat(time.datetime.now()) and PAST_DUE:
                    print(
                        assignment[0], "is past due and not submitted. Not adding task")
                else:
                    print("Could not find task",
                          assignment[0], "adding new task to project", course)
                    todoistAPI.items.add(assignment[0].strip(), due={
                                         "date": assignment[1]}, project_id=projectList[course])
    todoistAPI.commit()


if __name__ == "__main__":
    printMessage(PRINT_MESSAGE)
    apiKeys = loadKeys()
    pullSources(apiKeys)
