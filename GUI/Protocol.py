import tkinter as tk 
from tkinter import *

# import config

LARGE_FONT = ("Verdana", 12)
class Protocol(tk.Frame):

    def __init__(self, parent, controller): 
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        self.displayFrame()


    def displayFrame(self):

        label = tk.Label(self, text = "Can:SUB-Protocol", font= LARGE_FONT )
        label.grid(row = 0, column = 1, sticky = "nsew")

        pdo_button = tk.Button(self, text = "PDO", fg = "black", command = lambda: self.controller.show_frame(PDO_Page))
        pdo_button.grid(row = 1, column = 1, sticky = "nsew")

        sdo_button = tk.Button(self, text = "SDO", fg = "black", command = lambda: self.controller.show_frame(PageOne))
        sdo_button.grid(row = 2, column = 1, sticky = "nsew")




class PDO_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Fill out the following fields: ", font=LARGE_FONT)
        label.grid(row = 0, column = 0, sticky = "nsew")

        label = tk.Label(self, text="Node Name", font=LARGE_FONT)
        label.grid(row = 1, column = 0, sticky = "nsew")

        nameEntered = tk.Entry(self, width = 15, textvariable = self.controller.can_data["nodeName"])
        nameEntered.grid(column = 1, row = 1)

        label_id = tk.Label(self, text="NodeID", font=LARGE_FONT)
        label_id.grid(row = 2, column = 0, sticky = "nsew")

        idEntered = tk.Entry(self, width = 15, textvariable = self.controller.can_data["nodeID"])
        idEntered.grid(column = 1, row = 2)

        label_structure = tk.Label(self, text="PDO Structure (Name for each byte", font=LARGE_FONT)
        label_structure.grid(row = 3, column = 0, sticky = "nsew")

        label_byte1 = tk.Label(self, text="Byte 1:", font=LARGE_FONT)
        label_byte1.grid(row = 4, column = 0, sticky = "nsew")

        byte1 = tk.Entry(self, width = 15, textvariable = self.controller.can_data["byte1"])
        byte1.grid(column = 1, row = 4)

        label_byte2 = tk.Label(self, text="Byte 2:", font=LARGE_FONT)
        label_byte2.grid(row = 5, column = 0, sticky = "nsew")

        byte2 = tk.Entry(self, width = 15, textvariable = self.controller.can_data["byte2"])
        byte2.grid(column = 1, row = 5)

        label_byte3 = tk.Label(self, text="Byte 3:", font=LARGE_FONT)
        label_byte3.grid(row = 6, column = 0, sticky = "nsew")

        byte3 = tk.Entry(self, width = 15, textvariable = self.controller.can_data["byte3"])
        byte3.grid(column = 1, row = 6)

        label_byte4 = tk.Label(self, text="Byte 4:", font=LARGE_FONT)
        label_byte4.grid(row = 7, column = 0, sticky = "nsew")

        byte4 = tk.Entry(self, width = 15, textvariable = self.controller.can_data["byte4"])
        byte4.grid(column = 1, row = 7)

        label_byte5 = tk.Label(self, text="Byte 5:", font=LARGE_FONT)
        label_byte5.grid(row = 8, column = 0, sticky = "nsew")

        byte5 = tk.Entry(self, width = 15, textvariable = self.controller.can_data["byte5"])
        byte5.grid(column = 1, row = 8)

        label_byte6 = tk.Label(self, text="Byte 6:", font=LARGE_FONT)
        label_byte6.grid(row = 9, column = 0, sticky = "nsew")

        byte6 = tk.Entry(self, width = 15, textvariable = self.controller.can_data["byte6"])
        byte6.grid(column = 1, row = 9)

        label_byte7 = tk.Label(self, text="Byte 7:", font=LARGE_FONT)
        label_byte7.grid(row = 10, column = 0, sticky = "nsew")

        byte7 = tk.Entry(self, width = 15, textvariable = self.controller.can_data["byte7"])
        byte7.grid(column = 1, row = 10)

        label_byte8 = tk.Label(self, text="Byte 8:", font=LARGE_FONT)
        label_byte8.grid(row = 11, column = 0, sticky = "nsew")

        byte8 = tk.Entry(self, width = 15, textvariable = self.controller.can_data["byte8"])
        byte8.grid(column = 1, row = 11)

        submit_button = tk.Button(self, text = "SUBMIT", fg = "black", command = lambda: self.write_to_file())
        submit_button.grid(row = 14, column = 3, sticky = "nsew")

        mainMenuButton = tk.Button(self, text = "Main Menu", fg = "black", command = lambda: self.controller.home_button("MainMenu"))
        mainMenuButton.grid(row = 18, column = 3, sticky = "nsew")

        back_button = tk.Button(self, text = "Back", fg = "black", command = lambda: self.controller.show_frame(Protocol))
        back_button.grid(row = 20, column = 3, sticky = "nsew")

        

    
    def write_to_file(self):
        print("Write to YAMl file here")



