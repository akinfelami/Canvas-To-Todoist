import requests
import os
import sys
import json
from todoist.api import TodoistAPI


class Canvas:

    canvasCourses = {}

    def __init__(self):
        self.canvasKey = ""
        self.todoistKey = ""
        self.courseIDs = {}

    
    def getCourses(self):
        return self.courseIDs

    def getCanvasKey(self):
        return self.canvasKey

    def getTodoistKey(self):
        return self.todoistKey


    def getInfo(self):
        while not self.canvasKey:
            usrKey = input("Paste your Canvas API key here: ").strip()
            check = requests.get("https://canvas.instructure.com/api/v1/courses",
                                headers={"Authorization": "Bearer "+usrKey})
            if check.ok:
                self.canvasKey = usrKey
            else:
                print("Could not make connection. Check API key")

        while not self.todoistKey:
            usrKey = input("Paste your Todoist API key here: ").strip()
            api = TodoistAPI(usrKey)
            if 'error' not in api.sync():
                self.todoistKey = usrKey
            else:
                print("Could not make connection. Check API key")
        courseID = self.listCourses(self.canvasKey)
        return self.canvasKey, self.todoistKey, courseID


    def listCourses(self, canvasKey):

        API_KEY = self.canvasKey
        header = {"Authorization": "Bearer " + API_KEY}
        parameter = {'per_page': 9999}

        courseList = requests.get(
            'https://canvas.instructure.com/api/v1/courses', headers=header, params=parameter).json()


        for index, name in enumerate(courseList):
            try:
                #Todoist has a funny way of handling brackets
                name['name'] = name['name'].replace('(', '').replace(')', '')
                print(str(index+1) + ".)", name['name'])
            except:
                continue
        userIn = int(
            input("Enter number of course you would like to sync (Enter -1 when done): "))
        while userIn != -1:
            try:
                if courseList[userIn-1]:
                    self.courseIDs[courseList[userIn-1]["id"]
                            ] = [courseList[userIn-1]["name"], "0"]
            except:
                print("Entry out of range")
            userIn = int(
                input("Enter number of course you would like to sync (Enter -1 when done): "))
        return self.courseIDs


if __name__ == "__main__":
    a = Canvas()
    a.getInfo()