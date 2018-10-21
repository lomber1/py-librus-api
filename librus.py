import requests
import sys
from getpass import getpass


class Librus:
    host = "https://api.librus.pl/"
    headers = {
        "Authorization": "Basic Mjg6ODRmZGQzYTg3YjAzZDNlYTZmZmU3NzdiNThiMzMyYjE="
    }
    logged_in = False

    lucky_number = None
    grades = None
    subjects = None
    categories = None
    teachers = None
    comments = None

    # Checks data and decides method of login
    def login(self, login, password, mode="custom"):
        if not self.logged_in:
            if mode == "console":
                if self.make_connection(str(input("Login: ")), str(getpass(prompt="Hasło: "))):
                    return True
                else:
                    return False
            else:
                if login is None or password is None or login == "" or password == "":
                    return False
                else:
                    if self.make_connection(login, password):
                        return True
                    else:
                        return False

    # Make connection and get access token
    def make_connection(self, login, password):
        r = None
        loop = 0
        while r is None:
            try:
                r = requests.post(self.host + "OAuth/Token", data={"username": login,
                                                                   "password": password,
                                                                   "librus_long_term_token": "1",
                                                                   "grant_type": "password"},
                    headers=self.headers)

                self.logged_in = True
                self.headers["Authorization"] = "Bearer " + r.json()["access_token"]
                print("Nawiązano połączenie")

                return True
            except requests.exceptions.Timeout:
                if loop >= 10:
                    return False
                else:
                    loop += 1
                    continue
            except requests.exceptions.RequestException as e:
                print(e)
                return False

    def get_lucky_number(self):
        if self.lucky_number is None:
            try:
                r = requests.get(self.host + "2.0/LuckyNumbers", headers=self.headers)
                try:
                    self.lucky_number = r.json()["LuckyNumber"]["LuckyNumber"]
                    return self.lucky_number
                except KeyError:
                    return None
            except (requests.exceptions.ConnectionError, TimeoutError, requests.exceptions.Timeout,
                    requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as e:
                print(e)
                sys.exit(1)
        else:
            return self.lucky_number

    def get_grades(self):
        r = requests.get(self.host + "2.0/Grades", headers=self.headers)

        if not self.subjects:
            self.get_subjects()

        if not self.categories:
            self.get_categories()

        if not self.teachers:
            self.get_teachers()

        if self.grades is None:
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
        if self.subjects is None:
            r = requests.get(self.host + "2.0/Subjects", headers=self.headers)

            self.subjects = {i["Id"]: i["Name"] for i in r.json()["Subjects"]}

    def get_categories(self):
        if self.categories is None:
            self.categories = {}

            r = requests.get(self.host + "2.0/Grades/Categories", headers=self.headers)

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
        if self.teachers is None:
            r = requests.get(self.host + "2.0/Users", headers=self.headers)

            self.teachers = {
                i["Id"]: {
                    "FirstName": i["FirstName"],
                    "LastName": i["LastName"]
                } for i in r.json()["Users"]
            }

        if mode == "fullname":
            return ["%s %s" % (data["FirstName"], data["LastName"]) for t_id, data in self.teachers.items()]
        elif mode == "fullname-id":
            return ["%s: %s %s" % (t_id, data["FirstName"], data["LastName"]) for t_id, data in self.teachers.items()]

        return self.teachers

    def get_comments(self):
        if self.comments is None:
            r = requests.get(self.host + "2.0/Grades/Comments", headers=self.headers)

            self.comments = {
                i["Id"]: {
                    "Text": i["Text"]
                } for i in r.json()["Comments"]
            }

        return self.comments
