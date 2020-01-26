"""



"""
import tkinter as tk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        group_1 = tk.LabelFrame(self, padx=25, pady=15,
                                text="Tempreture and Pressure")
        group_1.pack(padx=10, pady=5)

        tk.Label(group_1, text="Compressor Capsule Helium Discharge Temperature: ").grid(row=0)
        tk.Label(group_1, text="Water Outlet Temperature: ").grid(row=1)
        tk.Label(group_1, text="Water inlet Temperature: ").grid(row=2)




if __name__ == "__main__":
    app = App()
    app.mainloop()
