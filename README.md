Dokumentacja w języku polskim jest [tutaj.](README_pl.md)
# py-librus-api
# Table of contents
1. [Intro](#intro)
2. [Instalation](#instalation)
3. [Exmaple usage](#example-usage)
4. [Functions](#functions)
# Intro
API for librus e-register.<br>
There is no guarantee of developing this API further more!
# Instalation
`pip install py-librus-api`
# Example usage
```python
from py_librus_api import Librus


librus = Librus()

"""Loops until user logs in successfully"""
while not librus.logged_in:
    if not librus.login(login, password):
        print("Log in failed! Check your username and/or password!")
    else:
        print("Logged in successfully!")

# Your code goes here
```
More info in [functions](#functions)
# Functions
**Required params/functions are marked with `!` prefix.**<br>
**`*` means that there is explanation below or something is optional.**
## !login(!login, !password)
Function returns `true` if logging in was successful and `false` when not.<br>
`login` - Variable that contains user login. <br>
`password` - Variable that contains user password.<br>
Example usage:
```python
librus.login(login_var, password_var)
```
## You can check if user is logged in!
```python
if librus.logged_in:
    ...
```
## If user is not logged in, "User not logged in" exception will be raised!
## If connection error occurs, "Connection error" will be raised!
## get_lucky_number()
Returns lucky number (`int`).
## get_grades()
**For displaying grades in the console, it is recommended to use pretty-print (pprint)!**
Returns all user grades in this foramt:<br>
```
grades = {
  "Biologia": [
    {
      "Grade": "5",
      "Weight": "3",
      "Category": "Kartkówka",
      'Teacher': {'FirstName': 'Jan', 'LastName': 'Kowalski'},
      "Comment": "kartkówka z działu o płazach",
      "To_the_average": "Tak"
    }
    ...
  ]
  ...
}
```
**Note that subject names are in language provided by Librus API (in this example it's polish)**
## get_teachers(mode*)
Returns teachers' personal data (firstname, lastname) in couple of formats.
You can choose format like that:
```python
librus.get_teachers(mode="print") # etc.
```
### List of formats:
#### normal (default)
```
{
  1123576: {'FirstName': 'Jan', 'LastName': 'Kowalski'},
  1983456: {'FirstName': 'Grażyna', 'LastName': 'Kowalska'},
  ...
}
```
#### fullname
```
[
  "Jan Kowalski",
  "Grażyna Kowalska",
  ...
]
```
#### fullname-id
```
[
  '1476937: Jan Kowalski',
  '1484010: Grazyna Kowalska',
  ...
 ]
```
## get_school_free_days()
Returns a list of days free from school.
Format:
```
[
    {'DateFrom': '2019-01-01', 'DateTo': '2019-01-01', 'Name': 'Nowy Rok'},
    ...
]
```
## get_teacher_free_days()
Returns a list of teachers' absence.
Format:
```
[
    {
        'DateFrom': '2018-10-24',
        'DateTo': '2018-10-26',
        'Teacher': {'FirstName': 'Jan', 'LastName': 'Kowalski'},
        'TimeFrom': '13:40:00',
        'TimeTo': '15:15:00',
        'Type': 'szkolenie'
    },
]
```
**It can happen that `TimeFrom` and `TimeTo` won't exist!**

## get_attendances()
Returns attendances in this format:
```
[
{'AddDate': '2018-10-29 12:52:51',
  'AddedBy': {'FirstName': 'Jan', 'LastName': 'Kowalski'},
  'Date': '2018-10-29',
  'Id': 123456,
 'Lesson': {'Subject': 'Chemia',
            'Teacher': {'FirstName': 'Jan', 'LastName': 'Kowalski'}},
 'LessonNo': 6,
 'Semester': 1,
 'Type': {'IsPresenceKind': True,
           'Name': 'Obecność',
           'Order': 1,
           'Short': 'ob',
           'Standard': True}
           }
 ...
]
```