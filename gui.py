"""
author: Cody Roberson
Date: 2020-01-28
purpose: Serves as the main gui for the cryo controller
@copyright 2020 Arizona State University
"""
import tkinter as tk
from tkinter import messagebox
import comp_serialif
import sys

## Serial Port ##
srCnxn = "/dev/ttyUSB0"

class App(tk.Tk):

    def __init__(self):
        super().__init__()

        """
            Initalize serial connection to compressor
        """

        self.compressor = comp_serialif.f70L_HeCompressor(srCnxn)
        if self.compressor.startConnection() == False:
            self.destroy()
            return


        """
        Group 1 gui Elements.
        """
        
        group_1 = tk.LabelFrame(self, padx=25, pady=15,
                                text="Tempreture and Pressure", font=("Courier", 16))
        group_1.pack(padx=10, pady=5)

        tk.Label(group_1, text="Compressor Capsule Helium Discharge Temperature: ", font=("Courier", 14)).grid(row=0)
        self.compressorcapsuletemp = tk.Label(group_1, text="Fetching Data", font=("Courier", 14))
        self.compressorcapsuletemp.grid(row=0, column=1)
       
        tk.Label(group_1, text="Water Outlet Temperature: ", font=("Courier", 14)).grid(row=1)
        self.outletTemp = tk.Label(group_1, text="Fetching Data", font=("Courier", 14))
        self.outletTemp.grid(row=1, column=1)
       
        tk.Label(group_1, text="Water inlet Temperature: ", font=("Courier", 14)).grid(row=2)
        self.inletTemp = tk.Label(group_1, text="Fetching Data", font=("Courier", 14))
        self.inletTemp.grid(row=2, column = 1)
       
        tk.Label(group_1, text="Compressor Return Pressure: ", font=("Courier", 14)).grid(row = 3)
        self.returnPressure = tk.Label(group_1, text="Fetching Data", font=("Courier", 14))
        self.returnPressure.grid(row=3, column=1)
        """
        Group 2 gui elements
        """
        group_2 = tk.LabelFrame(self, padx=25, pady=15, text="Controls", font=("Courier", 16))
        group_2.pack(padx=10, pady=5)

        self.comp_on_bttn = tk.Button(group_2, text="Compressor On")
        self.comp_on_bttn.grid(row=0)
        self.comp_on_bttn.bind("<Button-1>", self.compressor.turnOn)
        self.comp_off_bttn = tk.Button(group_2, text="Compressor Off")
        self.comp_off_bttn.grid(row=0, column=1)
        self.comp_off_bttn.bind("<Button-1>", self.compressor.turnOff)
        
        """     
        TODO: Not Implemented in interface
        tk.Button(group_2, text="Cold Head Run").grid(row=1, column=0)
        tk.Button(group_2, text="Cold Head Pause").grid(row=1, column = 1)
        tk.Button(group_2, text="Cold Head Pause Off").grid(row=1, column = 2) 
        """
   
        self.updateStats()


    """
    Setup a timer to get the status of the compressor
    """
    def updateStats(self):
        print("Fetching Data")
        data = self.compressor.collectStats()
        #data = ["023", "024", "025", "026"]
        if not data == None:
            self.compressorcapsuletemp.config(text=data[0] + " °C")
            self.outletTemp.config(text=data[1] + " °C")
            self.inletTemp.config(text=data[2] + " °C")
            self.returnPressure.config(text=data[3] + " PSIG")
        else:
            messagebox.showerror(title="Update Stats Error", message="An error has occured while attempting to update stats")
            self.compressorcapsuletemp.config(text="ERROR")
            self.outletTemp.config(text="ERROR")
            self.inletTemp.config(text="ERROR")
            self.returnPressure.config(text="ERROR")
            return
    
        self.after(5000, self.updateStats)



if __name__ == "__main__":
    app = App()
    app.mainloop()
