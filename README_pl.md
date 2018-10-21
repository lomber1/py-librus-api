Documentation in english can be found [there.](README.md)
# py-librus-api
# Spis treści
1. [Wstęp](#wstęp)
2. [Instalacja](#instalacja)
3. [Przykładowe użycie](#przykładowe-użycie)
4. [Spis funkcji](#spis-funkcji)
# Wstęp
API do e-dziennika librus synergia.
Nie ma gwarancji na to, że API będzie rozwijane!
# Instalacja
Kiedyś będzie
# Przykładowe użycie
```python
from librus import Librus()

librus = Librus()
librus.login(login, password) # Więcej info w spisie funkcji.
print(librus.get_lucky_number())
# 14
```
# Spis funkcji
**Wymagane parametry/funkcje zaznaczone są prefixem `!`**<br>
**Jeżeli przy nazwie jest `*` oznacza to, że poniżej będzie wyjaśnienie jakiejś rzeczy**
## !login(login*, password*, mode*)
Funkcja zwraca true gdy logowanie powiodło się i false gdy nie.<br>
`login` - Zmienna string z loginem użytkownika **domyślnie None**<br>
`password` - Zmienna string z hasłem użytkownika **domyślnie None**<br>
`mode` - Zmienna string **domyślnie custom**<br>
**Logowanie przez konsolę**
```python
librus.login(mode="console")
```
**Logowanie bez konsoli (dane logowania w argumentach)**
```python
librus.login(login_var, password_var)
```
#### Możliwe kombinacje argumentu mode
**mode="console"** - Zmusza funkcję do użycia konsoli w celu logowania.<br>
**mode="custom"** - Zmusza funkcję do użycia zmiennych z danymi.<br>
## Przed użyciem funkcji powinno sprawdzić się, czy użytkownik jest zalogowany!
```python
if librus.logged_in:
    ...
```
## get_lucky_number()
Zwraca szczęśiwy numerek w formacie `int`
## get_grades()
Zwraca wszystkie oceny użytkownika w poniższym formacie.<br>
**Do wypisania ocen w konsoli zaleca się używanie pretty-print (pprint)!**
```
grades = {
  "Biologia": [
    {
      "grade": "5",
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
## get_teachers(mode*)
Funkcja zwraca dane nauczycieli, w formacie zależnym od wybranego trybu.
Np. `print`
```
get_teachers(mode="print")
```
### Lista trybów oraz format w jakim zwracane są dane:
#### normal (domyślny)
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
Zwraca listę dni wolnych od szkoły w formacie:
```
[
    {'DateFrom': '2019-01-01', 'DateTo': '2019-01-01', 'Name': 'Nowy Rok'},
    ...
]
```
## get_teacher_free_days()
Zwraca listę nieobecności nauczyciela w formacie*:
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
**Może się zdarzyć, że pola `TimeFrom` i `TimeTo` nie będą istniały!**

