from librus import Librus
from pprint import pprint

if __name__ == "__main__":
    librus = Librus()
    print(librus.get_lucky_number())
    pprint(librus.get_grades())
    pprint(librus.get_teachers(mode="print"))
