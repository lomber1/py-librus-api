# python-librus
API do e-dziennika librus synergia.
# Spis treści
1. [Instalacja](#instalacja)
2. [Przykładowe użycie](#przykładowe-użycie)
3. [Spis funkcji](#spis-funkcji)
# Instalacja
...
# Przykładowe użycie
```python
from librus import Librus()

librus = Librus()
print(librus.get_lucky_number())
# 14
```
# Spis funkcji
## get_lucky_number()
Zwraca szczęśiwy numerek w formacie `int`
## get_grades()
Zwraca wszystkie oceny w formacie
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
## get_teachers()
Funkcja zawiera różne tryby, np. print:
```
get_teachers(mode="print")
```
### Lista trybów i format:
#### normal (domyślny)
```
{
  1123576: {'FirstName': 'Jan', 'LastName': 'Kowalski'},
  1983456: {'FirstName': 'Grażyna', 'LastName': 'Kowalska'},
  ...
}
```
#### print
```
[
  "Jan Kowalski",
  "Grażyna Kowalska",
  ...
]
```
#### print-with-id
```
[
  '1476937: Jan Kowalski',
  '1484010: Grazyna Kowalska',
  ...
 ]
