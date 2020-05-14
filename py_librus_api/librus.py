import requests


class Librus:
    host = "https://api.librus.pl/"

    def __init__(self):
        self.headers = {
            "Authorization": "Basic Mjg6ODRmZGQzYTg3YjAzZDNlYTZmZmU3NzdiNThiMzMyYjE="
        }
        self.logged_in = False

    # Checks data and decides method of login
    def login(self, login, password):
        if not self.logged_in:
            if login is None or password is None or login == "" or password == "":
                return False
            else:
                """Make connection to the host and get auth token"""
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

    # Make connection and get access token

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
        """
        Get lucky number.
        :return: lucky number (int), -1 if lucky number does it exist
        """
        r = self.get_data("LuckyNumbers")

        try:
            lucky_number = r.json()["LuckyNumber"]["LuckyNumber"]

            return lucky_number
        except KeyError:
            return -1

    def get_lucky_number_json(self):
        """
        Get lucky number.
        :return: json response.
        """
        r = self.get_data("LuckyNumbers")

        return r.json()

    def get_grades(self):
        r = self.get_data("Grades")

        subjects = self.get_subjects()
        categories = self.get_categories()
        teachers = self.get_teachers()

        grades = {i: [] for i in subjects.values()}
        grades_comments = self.get_comments()

        for i in r.json()["Grades"]:
            if "Comments" in i:
                comment = grades_comments[i["Comments"][0]["Id"]]["Text"]
            else:
                comment = "Brak komentarza"

            grades[subjects[i["Subject"]["Id"]]].append({
                "Grade": i["Grade"],
                "Weight": categories[i["Category"]["Id"]]["Weight"],
                "Category": categories[i["Category"]["Id"]]["Name"],
                "Teacher": teachers[i["AddedBy"]["Id"]],
                "Comment": comment,
                "To_the_average": categories[i["Category"]["Id"]]["CountToTheAverage"]
            })

        return grades

    def get_grades_json(self):
        """
        Get grades.
        :return: json response.
        """
        r = self.get_data("Grades")

        return r.json()

    def get_subjects(self):
        r = self.get_data("Subjects")

        return {i["Id"]: i["Name"] for i in r.json()["Subjects"]}

    def get_subjects_json(self):
        """
        Get subjects.
        :return: json response.
        """
        r = self.get_data("Subjects")

        return r.json()

    def get_subject(self, subject_id):
        r = self.get_data("Subjects/{}".format(subject_id))

        return r.json()

    def get_categories(self):
        categories = {}

        r = self.get_data("Grades/Categories")

        for i in r.json()["Categories"]:
            if "Weight" in i:
                w = i["Weight"]
            else:
                w = None

            count_to_the_average = None
            try:
                count_to_the_average_bool = i["CountToTheAverage"]

                if count_to_the_average_bool:
                    count_to_the_average = "Tak"
                else:
                    count_to_the_average = "Nie"

            except KeyError:
                count_to_the_average = -1

            finally:
                categories[i["Id"]] = {
                    "Name": i["Name"],
                    "Weight": w,
                    "CountToTheAverage": count_to_the_average,
                }

        return categories

    def get_categories_json(self):
        """
        Get all categories.
        :return: json response.
        """
        r = self.get_data("Grades/Categories")

        return r.json()

    def get_category(self, category_id):
        """
        Get category.
        :param category_id: id of a category.
        :return: json response.
        """
        r = self.get_data("Grades/Categories/{}".format(category_id))

        return r.json()

    def get_teachers(self, *, mode="normal"):
        r = self.get_data("Users")

        teachers = {
            i["Id"]: {
                "FirstName": i["FirstName"],
                "LastName": i["LastName"]
            } for i in r.json()["Users"]
        }

        if mode == "fullname":
            return ["%s %s" % (data["FirstName"], data["LastName"]) for t_id, data in teachers.items()]
        elif mode == "fullname-id":
            return ["%s: %s %s" % (t_id, data["FirstName"], data["LastName"]) for t_id, data in teachers.items()]

        return teachers

    def get_users(self):
        """
        Get all users.
        :return: json response.
        """
        r = self.get_data("Users")

        return r.json()

    def get_user(self, user_id):
        """
        Get user details.
        :param user_id: id of a user.
        :return: json response.
        """
        r = self.get_data("Users/{}".format(user_id))

        return r.json()

    def get_comments(self):
        r = self.get_data("Grades/Comments")

        comments = {
            i["Id"]: {
                "Text": i["Text"]
            } for i in r.json()["Comments"]
        }

        return comments

    def get_comments_json(self):
        """
        Get all comments.
        :return: json.response
        """
        r = self.get_data("Grades/Comments")

        return r.json()

    def get_school_free_days(self):
        r = self.get_data("SchoolFreeDays")

        school_free_days = r.json()["SchoolFreeDays"]

        for i in school_free_days:
            for e in ["Id", "Units"]:
                i.pop(e)

        return school_free_days

    def get_school_free_days_json(self):
        """
        Get school free days.
        :return: json response
        """
        r = self.get_data("SchoolFreeDays")

        return r.json()

    def get_teacher_free_days(self):
        r = self.get_data("TeacherFreeDays")

        teacher_free_days = r.json()["TeacherFreeDays"]
        teachers = self.get_teachers()

        r = self.get_data("TeacherFreeDays/Types")
        teacher_free_days_types = {
            i["Id"]: i["Name"] for i in r.json()["Types"]
        }

        for i in teacher_free_days:
            i.pop("Id")
            i["Teacher"] = teachers[i["Teacher"]["Id"]]
            i["Type"] = teacher_free_days_types[i["Type"]["Id"]]

        return teacher_free_days

    def get_teacher_free_days_json(self):
        """
        Get all teacher free days.
        :return: json response
        """
        r = self.get_data("TeacherFreeDays")

        return r.json()

    def get_lessons(self):
        r = self.get_data("Lessons")

        subjects = self.get_subjects()
        teachers = self.get_teachers()

        lessons = {
            i["Id"]: {
                "Subject": subjects[i["Subject"]["Id"]],
                "Teacher": teachers[i["Teacher"]["Id"]]

            } for i in r.json()["Lessons"]
        }

        return lessons

    def get_lessons_json(self):
        """
        Get all lessons
        :return: json response
        """
        r = self.get_data("Lessons")

        return r.json()

    def get_lesson(self, lesson_id):
        """
        Get lesson details.
        :param lesson_id: id of a lesson.
        :return: json response.
        """
        r = self.get_data("Lessons/{}".format(lesson_id))

        return r.json()

    def get_attendances(self):
        r = self.get_data("Attendances/Types")

        attendances_types = {
            i["Id"]: {
                "Name": i["Name"],
                "Short": i["Short"],
                "Standard": i["Standard"],
                "IsPresenceKind": i["IsPresenceKind"],
                "Order": i["Order"]
            } for i in r.json()["Types"]
        }

        lessons = self.get_lessons()
        teachers = self.get_teachers()
        attendances = self.get_data("Attendances").json()["Attendances"]

        for i in attendances:
            i.pop("Student")
            i["Type"] = attendances_types[i["Type"]["Id"]]
            i["AddedBy"] = teachers[i["AddedBy"]["Id"]]
            i["Lesson"] = lessons[i["Lesson"]["Id"]]

        return attendances

    def get_attendances_json(self):
        """
        Get all attendances.
        :return: json response
        """
        r = self.get_data("Attendances")

        return r.json()

    # ---------- V2 ---------- #
    def get_class(self, class_id):
        """
        Get class details.
        :param class_id: id of a class
        :return: json response
        """
        r = self.get_data("Classes/{}".format(class_id))

        return r.json()

    def get_colors(self):
        """
        Get all colors.
        :return: json response
        """
        r = self.get_data("Colors/")

        return r.json()

    def get_color(self, color_id):
        """
        Get color details.
        :param color_id: id of a color
        :return: json response
        """
        r = self.get_data("Colors/{}".format(color_id))

        return r.json()

    def get_homework_assignments(self):
        """
        Get homework assignments. THIS WILL RETURN AN ERROR JSON IF USER DOES NOT HAVE PREMIUM!
        :return: json response
        """
        r = self.get_data("HomeWorkAssignments")

        return r.json()

    def get_text_grades(self):
        """
        Get all text grades.
        :return: json response
        """
        r = self.get_data("TextGrades")

        return r.json()
