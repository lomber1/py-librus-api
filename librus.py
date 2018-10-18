import requests
from getpass import getpass


class Librus:
    host = "https://api.librus.pl/"
    headers = {
        "Authorization": "Basic Mjg6ODRmZGQzYTg3YjAzZDNlYTZmZmU3NzdiNThiMzMyYjE="
    }

    lucky_number = 0
    grades = {}
    subjects = {}
    categories = {}
    teachers = {}

    def __init__(self):
        self.make_connection()

    # Make connection and get access token
    def make_connection(self):
        r = requests.post(self.host + "OAuth/Token", data={"username": str(input("Login: ")),
                                                           "password": str(getpass(prompt="Hasło: ")),
                                                           "librus_long_term_token": "1",
                                                           "grant_type": "password"},
            headers=self.headers)

        self.headers["Authorization"] = "Bearer " + r.json()["access_token"]

    def get_lucky_number(self):
        r = requests.get(self.host + "2.0/LuckyNumbers", headers=self.headers)
        self.lucky_number = r.json()["LuckyNumber"]["LuckyNumber"]

        return self.lucky_number

    def get_grades(self):
        r = requests.get(self.host + "2.0/Grades", headers=self.headers)

        if not self.subjects:
            self.get_subjects()

        if not self.categories:
            self.get_categories()

        if not self.teachers:
            self.get_teachers()

        self.grades = {i: [] for i in self.subjects.values()}
        grades_comments = self.get_comments()

        for i in r.json()["Grades"]:
            if "Comments" in i:
                comment = grades_comments[i["Comments"][0]["Id"]]["Text"]
            else:
                comment = "Brak komentarza"

            self.grades[self.subjects[i["Subject"]["Id"]]].append({
                "Ocena": i["Grade"],
                "Waga": self.categories[i["Category"]["Id"]]["Weight"],
                "Kategoria": self.categories[i["Category"]["Id"]]["Name"],
                "Nauczyciel": "%s %s" % (self.teachers[i["AddedBy"]["Id"]]["FirstName"],
                                         self.teachers[i["AddedBy"]["Id"]]["LastName"]),
                "Komentarz": comment,
                "Do średniej": self.categories[i["Category"]["Id"]]["CountToTheAverage"]
            })

        return self.grades

    def get_subjects(self):
        r = requests.get(self.host + "2.0/Subjects", headers=self.headers)

        self.subjects = {i["Id"]: i["Name"] for i in r.json()["Subjects"]}

    def get_categories(self):
        r = requests.get(self.host + "2.0/Grades/Categories", headers=self.headers)

        w = None
        for i in r.json()["Categories"]:
            if "Weight" in i:
                w = i["Weight"]
            else:
                w = None

            if i["CountToTheAverage"]:
                i["CountToTheAverage"] = "Tak"
            else:
                i["CountToTheAverage"] = "Nie"

            self.categories[i["Id"]] = {
                "Name": i["Name"],
                "Weight": w,
                "CountToTheAverage": i["CountToTheAverage"],
            }

    def get_teachers(self, *, mode="normal"):
        r = requests.get(self.host + "2.0/Users", headers=self.headers)

        self.teachers = {
            i["Id"]: {
                "FirstName": i["FirstName"],
                "LastName": i["LastName"]
            } for i in r.json()["Users"]
        }

        if mode == "print":
            return ["%s %s" % (data["FirstName"], data["LastName"]) for t_id, data in self.teachers.items()]
        elif mode == "print-with-id":
            return ["%s: %s %s" % (t_id, data["FirstName"], data["LastName"]) for t_id, data in self.teachers.items()]

        return self.teachers

    def get_comments(self):
        r = requests.get(self.host + "2.0/Grades/Comments", headers=self.headers)

        return {
            i["Id"]: {
                "Text": i["Text"]
            } for i in r.json()["Comments"]
        }

    def get_lessons(self):
        r = requests.get(self.host + "2.0/Lessons", headers=self.headers)
