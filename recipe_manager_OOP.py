"""
This script uses tkinter to make a GUI-based recipe management app. The recipes are stored in a
txt file and displayed in the web browser.

RECIPES:
Recipes should have a picture, short description that will be used for display in the recipe
selector, cook time, ingredients, and the actual step by step instructions.

INTENDED FEATURES:
1) Fully navigatable app using only GUI controls.
2) Ability to add recipes and append these to a single txt file. Each recipe will be one line with
   a unique separator to allow for easy splitting into the constituent parts for display.
3) Ability to edit and update recipes.
4) Recipe viewing in a standard format, i.e. html/CSS with a single CSS format for all recipes.
   Recipes will be viewed in the web browser.
5) Recipe randomizer - have the app select a random recipe for you.
6) Search feature. Search recipes by tags, ingredients, or time it takes to cook them.
7) Meal planning. Interface the app with Google calendar.
8) Include pictures in recipe, allow user to add photos.
9) Grocery list generator based on a number of selected recipes.
10) Recipe grabber. Take a url from the user, scan the webpage, and automatically load in and save 
    the recipe.
11) Cooking tracker. Show how many times in a week/month you cooked, give ability to sort or color by 
    ingredient.
12) Make it pretty.

"""

import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
style.use('ggplot')
import urllib
import json
import pandas as pd
import numpy as np
import os

LARGE_FONT= ("Verdana", 12)

# Creating a class for the actual recipe manager GUI backend
class RecipeManager(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        # tk.Tk.iconbitmap(self,default='clienticon.ico')
        tk.Tk.wm_title(self, "Recipe Manager")

        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Creating class for the start page
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        label = ttk.Label(self, text="Enter Username:", font=LARGE_FONT)
        label.pack(pady=20,padx=10)
        entry = ttk.Entry(self)
        entry.pack(ipadx = 30)
        button = ttk.Button(self, text="Login",
                            command=lambda:self.getUsernameReturning(entry))
        button.pack()

        label2 = ttk.Label(self,text='New User? Enter Username Below:',
                      font=LARGE_FONT)
        label2.pack(pady=80,padx=10)
        entry2 = ttk.Entry(self)
        entry2.pack(ipadx = 30)
        button2 = ttk.Button(self, text="Login",
                            command=lambda:self.getUsernameNew(entry2))
        button2.pack()

        button3 = ttk.Button(self,text='visit page 3',
                             command=lambda:controller.show_frame(PageThree))
        button3.pack()
    
    def getUsernameReturning(self, entry):
        usernameReturning = entry.get()
        # If directory does not exist, display 'username not found'
        thisFileDir = os.getcwd() + '\\' + 'RecipeManager'
        if(os.path.isdir(thisFileDir + '\\' + usernameReturning)):
            print('It exists!')
            # Do things with that folder, e.g. get recipes, store them, whatever
        elif(not(os.path.isdir(thisFileDir + '\\' + usernameReturning))):
            entry.delete(0, len(usernameReturning))
            entry.insert(0, "That username does not exist.")
    
    def getUsernameNew(self, entry):
        usernameNew = entry.get()
        # If directory does not exist, display 'username already exists'
        thisFileDir = os.getcwd() + '\\' + 'RecipeManager'
        if(not(os.path.isdir(thisFileDir + '\\' + usernameNew))):
            os.mkdir(thisFileDir + '\\' + usernameNew)
        elif(os.path.isdir(thisFileDir + '\\' + usernameNew)):
            entry.delete(0, len(usernameNew))
            entry.insert(0, "That username is already taken.")

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                            command=lambda: controller.show_frame(PageOne))
        button2.pack()

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

        

        canvas = FigureCanvasTkAgg(f, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

app = RecipeManager()
app.geometry("720x480")
app.mainloop()

"""
# Create a class for each recipe
class Recipe():
    def __init__(self, *args, **kwargs):
        pass
"""