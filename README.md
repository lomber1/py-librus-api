# python-librus
API do e-dziennika librus synergia.
# Spis treści
1. [Wstęp](#wstęp)
2. [Instalacja](#instalacja)
3. [Przykładowe użycie](#przykładowe-użycie)
4. [Spis funkcji](#spis-funkcji)
# Wstęp
Nie ma gwarancji na to, że API będzie rozwijane!
API może się zepsuć, gdy librus je zmieni!
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
**Wymagane parametry/funkcje zaznaczone są prefixem !**<br>
**Opcjonalne parametry/funkcje zaznaczone są suffixem** *
## !login(!login, !password, mode*)
Funkcja zwraca true gdy logowanie powiodło się i false gdy nie.<br>
`login` - Zmienna string z loginem użytkownika (None dla konsoli)<br>
`password` - Zmienna string z hasłem użytkownika (None dla konsoli)<br>
`mode` - Zmienna string **domyślnie custom**<br>
**Funkcja zawiera wbudowany system logowania konsolą! Wystarczy w miejscu `login` i `password` dać `None` oraz użyć argumentu `mode="console"` np.**
```python
librus.login(None, None, mode="console")
```
#### Możliwe kombinacje argumentu mode
**mode="console"** - Zmusza funkcję do użycia konsoli w celu logowania.<br>
**mode="custom"** - Zmusza funkcję do użycia zmiennych z danymi.<br>
## Przed użyciem funkcji powinno sprawdzić się, czy użytkownik jest zalogowany!
```python
if librus.logged_in:
    ...
```
## *get_lucky_number()
Zwraca szczęśiwy numerek w formacie `int`
## *get_grades()
Zwraca wszystkie oceny użytkownika w poniższym formacie.<br>
**Do wypisania ocen w konsoli zaleca się używanie pretty-print (pprint)!**
```
grades = {
  "Biologia": [
    {
      "Ocena": "5",
      "Waga": "3",
      "Kategoria": "Kartkówka",
      "Nauczyciel": "Janusz Kowalski",
      "Komentarz": "kartkówka z działu o płazach",
      "Do średniej": "Tak"
    }
    ...
  ]
  ...
}
```
## *get_teachers(*mode)
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
