import tkinter as tk
from pprint import pprint

from librus import Librus


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Login
        self.login_label = tk.Label(self.parent, text="Login")
        self.login_label.pack(fill=tk.X, padx=10)

        self.login_input = tk.Entry(self.parent)
        self.login_input.pack(fill=tk.X, padx=10)

        # Password
        self.password_label = tk.Label(self.parent, text="Password")
        self.password_label.pack(fill=tk.X, padx=10)

        self.password_input = tk.Entry(self.parent, show="*")
        self.password_input.pack(fill=tk.X, padx=10)

        # Submit btn
        self.submit_btn = tk.Button(self.parent, text="Zaloguj", command=self.callback_submit_btn)
        self.submit_btn.pack(fill=tk.X, padx=10, pady=10)

        # Loading label
        self.loading_label = tk.Label(self.parent, text="")
        self.loading_label.pack(fill=tk.X, padx=10)

        # Test btns
        self.lucky_btn = tk.Button(self.parent, text="Szczęśliwy numerek", command=self.callback_lucky_btn)
        self.lucky_btn.pack(fill=tk.X, padx=10, pady=10)

    def callback_submit_btn(self):
        self.login()

    def login(self):
        login = self.login_input.get()
        password = self.password_input.get()

        if not librus.logged_in:
            self.loading_label.config(text="Logowanie...")

            if librus.login(login, password):
                self.loading_label.config(text="Zalogowano!")
                print("Zalogowano.")
                # TODO: Nowe okno z gownami
            else:
                self.loading_label.config(text="Logowanie nie powiodło się!")
                print("Logowanie nie powiodło się!")
        else:
            print("Jesteś już zalogowany!")

    def callback_lucky_btn(self):
        if librus.logged_in:
            print(librus.get_lucky_number())
        else:
            print("Musisz się zalogować!")


if __name__ == "__main__":
    # Librus API init
    librus = Librus()

    # Tkinter
    root = tk.Tk()
    root.title = "Librus"
    MainApplication(root).pack(side="top", fill="both", expand=True)

    root.mainloop()
