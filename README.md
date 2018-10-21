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
Someday...
# Example usage
```python
from librus import Librus()

librus = Librus()
librus.login(login, password)
print(librus.get_lucky_number())
# 14
```
More info in [functions](#functions)
# Functions
**Required params/functions are marked with `!` prefix.**<br>
**`*` means that there is explanation below or something is optional.**
## !login(login*, password*, mode*)
Function returns `true` if logging in was successful and `false` when not.<br>
`login` - Variable that contains user login. Default `None`<br>
`password` - Variable that contains user password. Default `None`<br>
`mode` - Variable that contains login mode. Default `custom`. If using custom login system, it don't have to be set to anything.<br>
**This function have built-in console login system (note that password input is made by getpass() and not plain text input! You don't have to worry about visible password :)). To use it:**
```python
librus.login(mode="console")
```
**Logging in via custom login system**
```python
librus.login(login_var, password_var)
```
#### `mode` argument combinations
**mode="console"** - Use built-in console login system to log in.<br>
**mode="custom"** - Use custom login system (requires valid login data arguments).<br>
## You can check if user is logged in!
```python
if librus.logged_in:
    ...
```
If user is not logged in, `User not logged in` exception will be raised!!
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
      "Teacher": "Janusz Kowalski",
      "Comment": "kartkówka z działu o płazach",
      "To_the_average": "Tak"
    }
    ...
  ]
  ...
}
```
**Note that subject names in foreign language. (polish)**
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
        'DateFrom': '2018-10-09',
        'DateTo': '2018-10-09',
        'Teacher': 'Iwona Kuśmierczuk',
        'TimeFrom': '13:40:00',
        'TimeTo': '15:15:00',
        'Type': 'szkolenie'
    },
]
```
**It can happen that `TimeFrom` and `TimeTo` don't exist!**

