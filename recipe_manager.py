#!/usr/bin/env python
#Above line used for running in command line
# -*- coding: utf-8 -*-

# Run this in Python 3!

"""
Created on Tue Sep 04 21:04:45 2018

@author: jsharmon
"""

import tkinter as tk
import webbrowser as wb

"""
Make tkinter UI.
"""
class Window(tk.Frame):
    
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()
    
    # Creation of init window
    def init_window(self):
        # changing the title of our master widget      
        self.master.title("Recipe Manager")

        # creating a menu instance
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        # Create file, add option from dropdown + functionality, add file to menu
        fileMen = tk.Menu(menu)
        fileMen.add_command(label="Exit", command=self.client_exit)
        fileMen.add_command(label="New User")
        menu.add_cascade(label="File", menu=fileMen)

        # Create edit, add option from dropdown, add edit to menu
        edit = tk.Menu(menu)
        edit.add_command(label="Undo")
        menu.add_cascade(label="Edit", menu=edit)

    def client_exit(self):
        exit()

"""
Define callback function to open recipe in web browser using wb.
"""

root = tk.Tk()

#size of the window
root.geometry("400x300")

app = Window(root)
root.mainloop()  
    

"""
Get username. This will tell the program in which folder it will find the
recipes, images, etc.
"""





