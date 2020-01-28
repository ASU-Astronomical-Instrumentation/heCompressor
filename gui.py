"""
author: Cody Roberson
Date: 2020-01-28
purpose: Serves as the main gui for the cryo controller
@copyright 2020 Arizona State University
"""
import tkinter as tk
import comp_serialif

## Serial Port ##
srCnxn = "/dev/ttyUSB0"

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        """
            Initalize serial connection to compressor
        """

        self.compressor = comp_serialif.f70L_HeCompressor(srCnxn)

        """
        Group 1 gui Elements.
        """
        
        group_1 = tk.LabelFrame(self, padx=25, pady=15,
                                text="Tempreture and Pressure")
        group_1.pack(padx=10, pady=5)

        tk.Label(group_1, text="Compressor Capsule Helium Discharge Temperature: ").grid(row=0)
        self.compressorcapsuletemp = tk.Label(group_1, text="Fetching Data").grid(row=0, column=1)
       
        tk.Label(group_1, text="Water Outlet Temperature: ").grid(row=1)
        self.outletTemp = tk.Label(group_1, text="Fetching Data").grid(row=1, column=1)
       
        tk.Label(group_1, text="Water inlet Temperature: ").grid(row=2)
        self.inletTemp = tk.Label(group_1, text="Fetching Data").grid(row=2, column = 1)
       
        tk.Label(group_1, text="Compressor Return Pressure: ").grid(row = 3)
        self.returnPressure = tk.Label(group_1, text="Fetching Data").grid(row=3, column=1)

        """
        Group 2 gui elements
        """
        group_2 = tk.LabelFrame(self, padx=25, pady=15, text="Controls")
        group_2.pack(padx=10, pady=5)

        tk.Button(group_2, text="Compressor On").grid(row=0)
        tk.Button(group_2, text="Compressor Off").grid(row=0, column=1)
        
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
        if data not None:
            self.compressorcapsuletemp = data[0] + " °C"
            self.outletTemp = data[1] + " °C"
            self.inletTemp = data[2] + " °C"
            self.returnPressure = data[3] + " PSIG"
            self.after(5000, self.updateStats)



if __name__ == "__main__":
    app = App()
    app.mainloop()
