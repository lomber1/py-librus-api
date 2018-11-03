import requests
import sys


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
    students = None
    teachers = None
    comments = None
    lessons = None
    school_free_days = None
    teacher_free_days = None
    teacher_free_days_types = None
    attendances = None
    attendances_types = None

    # Checks data and decides method of login
    def login(self, login, password):
        if not self.logged_in:
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

                if r.ok:
                    self.logged_in = True
                    self.headers["Authorization"] = "Bearer " + r.json()["access_token"]

                    return True
                else:
                    return False
            except requests.exceptions.Timeout:
                if loop >= 10:
                    return False
                else:
                    loop += 1
                    continue
            except requests.exceptions.RequestException:
                raise requests.exceptions.ConnectionError

    def get_data(self, url):
        if self.logged_in:
            try:
                return requests.get(self.host + "2.0/" + url, headers=self.headers)
            except (requests.exceptions.ConnectionError, TimeoutError, requests.exceptions.Timeout,
                    requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout):
                    raise Exception("Connection error")
        else:
            raise Exception("User not logged in")

    def get_lucky_number(self):
        if self.lucky_number is None:
            r = self.get_data("LuckyNumbers")
            self.lucky_number = r.json()["LuckyNumber"]["LuckyNumber"]
            
            return self.lucky_number

        return self.lucky_number

    def get_grades(self):
        r = self.get_data("Grades")

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
                "Grade": i["Grade"],
                "Weight": self.categories[i["Category"]["Id"]]["Weight"],
                "Category": self.categories[i["Category"]["Id"]]["Name"],
                "Teacher": self.teachers[i["AddedBy"]["Id"]],
                "Comment": comment,
                "To_the_average": self.categories[i["Category"]["Id"]]["CountToTheAverage"]
            })

        return self.grades

    def get_subjects(self):
        if self.subjects is None:
            r = self.get_data("Subjects")

            self.subjects = {i["Id"]: i["Name"] for i in r.json()["Subjects"]}

        return self.subjects

    def get_categories(self):
        if self.categories is None:
            self.categories = {}

            r = self.get_data("Grades/Categories")

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

        return self.categories

    def get_teachers(self, *, mode="normal"):
        if self.teachers is None:
            r = self.get_data("Users")

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
            r = self.get_data("Grades/Comments")

            self.comments = {
                i["Id"]: {
                    "Text": i["Text"]
                } for i in r.json()["Comments"]
            }

        return self.comments

    def get_school_free_days(self):
        if self.school_free_days is None:
            r = self.get_data("SchoolFreeDays")
            self.school_free_days = r.json()["SchoolFreeDays"]

            for i in self.school_free_days:
                for e in ["Id", "Units"]:
                    i.pop(e)

        return self.school_free_days

    def get_teacher_free_days(self):
        if self.teachers is None:
            self.get_teachers()

        if self.teacher_free_days_types is None:
            r = self.get_data("TeacherFreeDays/Types")

            self.teacher_free_days_types = {
                i["Id"]: i["Name"] for i in r.json()["Types"]
            }

        if self.teacher_free_days is None:
            r = self.get_data("TeacherFreeDays")

            self.teacher_free_days = r.json()["TeacherFreeDays"]

            for i in self.teacher_free_days:
                i.pop("Id")
                i["Teacher"] = self.teachers[i["Teacher"]["Id"]]
                i["Type"] = self.teacher_free_days_types[i["Type"]["Id"]]

        return self.teacher_free_days

    def get_lessons(self):
        if self.lessons is None:
            if self.subjects is None:
                self.get_subjects()

            if self.teachers is None:
                self.get_teachers()

            r = self.get_data("Lessons")

            self.lessons = {
                i["Id"]: {
                    "Subject": self.subjects[i["Subject"]["Id"]],
                    "Teacher": self.teachers[i["Teacher"]["Id"]]

                } for i in r.json()["Lessons"]
            }

        return self.lessons

    def get_attendances(self):
        if self.attendances is None:
            if self.attendances_types is None:
                r = self.get_data("Attendances/Types")

                self.attendances_types = {
                    i["Id"]: {
                        "Name": i["Name"],
                        "Short": i["Short"],
                        "Standard": i["Standard"],
                        "IsPresenceKind": i["IsPresenceKind"],
                        "Order": i["Order"]
                    } for i in r.json()["Types"]
                }

            if self.lessons is None:
                self.get_lessons()

            self.attendances = self.get_data("Attendances").json()["Attendances"]

            for i in self.attendances:
                i.pop("Student")
                i["Type"] = self.attendances_types[i["Type"]["Id"]]
                i["AddedBy"] = self.teachers[i["AddedBy"]["Id"]]
                i["Lesson"] = self.lessons[i["Lesson"]["Id"]]

        return self.attendances
