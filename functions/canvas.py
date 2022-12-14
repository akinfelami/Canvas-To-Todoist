import requests
import os
import sys
import json
from todoist_api_python.api import TodoistAPI


class Canvas:

    canvasCourses = {}

    def __init__(self):
        self.canvasKey = ""
        self.todoistKey = ""
        self.courseIDs = {}
        self.allcourses = []

    
    def getCourses(self):
        return self.courseIDs

    def getCanvasKey(self):
        return self.canvasKey

    def getTodoistKey(self):
        return self.todoistKey


    def getInfo(self, canvaskey, todoistkey):
        while not self.canvasKey:
            # usrKey = input("Paste your Canvas API key here: ").strip()
            check = requests.get("https://canvas.instructure.com/api/v1/courses",
                                headers={"Authorization": "Bearer "+canvaskey})
            if check.ok:
                self.canvasKey = canvaskey
            else:
                print("Could not make connection. Check API key")

        while not self.todoistKey:
            # usrKey = input("Paste your Todoist API key here: ").strip()
            api = TodoistAPI(todoistkey)
            self.todoistKey = todoistkey
        self.allcourses = self.listCourses(self.canvasKey)
        return self.allcourses


    def listCourses(self, canvasKey):

        API_KEY = self.canvasKey
        header = {"Authorization": "Bearer " + API_KEY}
        parameter = {'per_page': 9999}

        courseList = requests.get(
            'https://canvas.instructure.com/api/v1/courses', headers=header, params=parameter).json()
        return courseList


if __name__ == "__main__":
    a = Canvas()
    a.getInfo()
