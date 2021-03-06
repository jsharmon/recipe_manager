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
3) Ability to edit and update recipes in real-time while viewing.
4) Recipe viewing in a standard format, i.e. html/CSS with a single CSS format for all recipes.
   Recipes will be viewed in the web browser.
5) Recipe randomizer - have the app select a random recipe for you.
6) Search feature. Search recipes by tags, ingredients, or time it takes to cook them.
7) Meal planning. Interface the app with Google calendar.
8) Include pictures in recipe, allow user to add photos.
9) Grocery list generator based on a number of selected recipes and an ingredient inventory provided
   by the user.
10) Recipe grabber. Take a url from the user, scan the webpage, and automatically load in and save 
    the recipe.
11) Cooking tracker. Show how many times in a week/month you cooked, give ability to sort or color by 
    ingredient.
12) Make it pretty.

"""

import tkinter as tk
from tkinter import scrolledtext as tkst
from tkinter import ttk
from tkinter import tix
import urllib
import json
import pandas as pd
import numpy as np
import os
import webbrowser as wb
import recipe_database_interface as rdi

LARGE_FONT = ("Verdana", 12)

# Save lines of the recipe file into global variable called 'recipeLines'
global isDBEmpty
isDBEmpty = True
global recipePath
recipePath = ''
global recipeDB
recipeDBName = 'RecipeFile.db'



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
        pageTuple = (StartPage, HomePage, HomePageEmptyDB, AddPage, SearchPage, RandomPage, URLAddPage, 
                     MealPlanPage, GroceryPage, MealTrackPage)
        for F in pageTuple:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Create menu bar
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)

        recipeMenu = tk.Menu(menubar, tearoff=0)
        recipeMenu.add_command(label="Add recipe", command=lambda:self.show_frame(AddPage))
        recipeMenu.add_separator()
        recipeMenu.add_command(label="Get random recipe", command=lambda:self.show_frame(RandomPage))
        recipeMenu.add_separator()
        recipeMenu.add_command(label="Search recipes", command=lambda:self.show_frame(SearchPage))
        recipeMenu.add_separator()
        recipeMenu.add_command(label="Get recipe from URL", command=lambda:self.show_frame(URLAddPage))
        menubar.add_cascade(label="Recipes", menu=recipeMenu)

        planningMenu = tk.Menu(menubar, tearoff=0)
        planningMenu.add_command(label="Meal planning", command=lambda:self.show_frame(MealPlanPage))
        planningMenu.add_separator()
        planningMenu.add_command(label="Grocery list generator", command=lambda:self.show_frame(GroceryPage))
        planningMenu.add_separator()
        planningMenu.add_command(label="Meal tracking", command=lambda:self.show_frame(MealTrackPage))
        menubar.add_cascade(label="Meal Planning", menu=planningMenu)

        tk.Tk.config(self, menu=menubar)

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()










###################################################################################################### 
# Define start and home page classes.
######################################################################################################

# Creating class for the start page
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        # Add label, entry, and button for login with existing username
        label = ttk.Label(self, text="Enter Username:", font=LARGE_FONT)
        label.pack(pady=(70,10),padx=10)
        entry = ttk.Entry(self)
        entry.pack(ipadx = 30)
        button = ttk.Button(self, text="Login",
                            command=lambda:self.getUsernameReturning(entry, controller))
        button.pack(pady=5)

        # Add label, entry, button for login with new username
        label2 = ttk.Label(self,text='New User? Enter Username Below:',
                      font=LARGE_FONT)
        label2.pack(pady=(50,10),padx=10)
        entry2 = ttk.Entry(self)
        entry2.pack(ipadx = 30)
        button2 = ttk.Button(self, text="Login",
                            command=lambda:self.getUsernameNew(entry2, controller))
        button2.pack(pady=5)
    
    def getUsernameReturning(self, entry, controller):
        # Get entry from UI
        usernameReturning = entry.get()

        # If folder exists, read recipe file and save lines into a list
        thisFileDir = os.getcwd() + '\\' + 'RecipeManager'
        if(os.path.isdir(thisFileDir + '\\' + usernameReturning)):
            recipePath = thisFileDir + '\\' + usernameReturning

            # Grab database containing recipes, check if it is empty
            isDBEmpty = rdi.is_DB_empty(recipePath)
            # HomePage label redefinition needs to be done here
            if(isDBEmpty):
                controller.show_frame(HomePageEmptyDB)
            else:
                controller.show_frame(HomePage)

        # If directory does not exist, display 'username not found'
        elif(not(os.path.isdir(thisFileDir + '\\' + usernameReturning))):
            entry.delete(0, len(usernameReturning))
            entry.insert(0, "That username does not exist.")
            return
    
    def getUsernameNew(self, entry, controller):
        # Get entry from UI
        usernameNew = entry.get()
    
        # Get current working directory; for me, it's /Users/jsharmon
        thisFileDir = os.getcwd() + '\\' + 'RecipeManager'

        # If running on new computer, create recipe manager folder
        if(not(os.path.isdir(thisFileDir))):
            os.mkdir(thisFileDir)

        # If folder doesn't already exist, make it and make a new recipe text file
        recipePath = thisFileDir + '\\' + usernameNew
        if(not(os.path.isdir(recipePath))):
            # Save the recipe path as a global variable to use file later
            os.mkdir(recipePath) # create folder w username

            # Create new SQL database to hold recipes
            rdi.create_new_DB(recipePath)

            # Go to empty DB home page from login page
            controller.show_frame(HomePageEmptyDB)

        # If directory exists, display 'username already exists'
        elif(os.path.isdir(recipePath)):
            entry.delete(0, len(usernameNew))
            entry.insert(0, "That username is already taken.")

# Need to actualy do something with the home page here
class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Recipes exist! Press button for summary', font=LARGE_FONT)
        label.pack(pady=10)

class HomePageEmptyDB(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='No recipes yet!', font=LARGE_FONT)
        label.pack(pady=10)









###################################################################################################### 
# Begin defining Recipe menu page classes.
######################################################################################################

class AddPage(tix.ScrolledWindow):
    def __init__(self, root, controller):
        sw = tix.ScrolledWindow(self, scrollbar=tix.Y)
        sw.pack(fill=tix.BOTH, expand=1)

        colList = ['Recipe Name:', 'Recipe Summary:', "Today's Date:", 'Type of cuisine:', 
                   'Ingredients (format - ingredient,amount,unit then enter):', 'Recipe Text:', 
                   'Prep Time:', 'Cook Time:', 'Calories:', 'Servings:', 'Tags:']
        label = [0]*len(colList)
        text = [0]*len(colList)
        for i in range(0,len(colList)):
            label[i] = ttk.Label(self, text=colList[i], font=LARGE_FONT)
            label[i].pack(padx=15, pady=2, anchor='nw')
            if (i in [0,2,3,6,7,8,9,10]):
                text[i] = tk.Entry(self, borderwidth=2)
                text[i].pack(ipadx=720-30, padx=15, pady=(5,20), anchor='nw')
            else:
                text[i] = tkst.ScrolledText(self, height=7, borderwidth=2)
                text[i].pack(ipadx=720-30, padx=15, pady=(5,20), anchor='nw')




class SearchPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self,text='search page',font=LARGE_FONT)
        label.pack(pady=10)



class RandomPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self,text='random page',font=LARGE_FONT)
        label.pack(pady=10)



class URLAddPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self,text='Enter recipe URL:',font=LARGE_FONT)
        label.pack(pady=(70,10),padx=10)
        entry = ttk.Entry(self)
        entry.pack(ipadx = 30)
        button = ttk.Button(self,text='Add + Preview',command=lambda:self.getURLText(entry))
        button.pack(pady=5)

    def getURLText(self, entry):
        recipeURL = entry.get()
        wb.open(recipeURL)
        # Add code that grabs the recipe from the webpage, adds to the text file, writes an html
        # file for display, then opens that html file for the user to view. Add easy way to edit
        # if it isn't correct?










###################################################################################################### 
# Begin defining meal planning menu page classes.
######################################################################################################

class MealPlanPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self,text='meal plan/calendar page',font=LARGE_FONT)
        label.pack(pady=10)



class GroceryPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self,text='grocery list page',font=LARGE_FONT)
        label.pack(pady=10)



class MealTrackPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self,text='meal tracker page',font=LARGE_FONT)
        label.pack(pady=10)


'''
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
'''








######################################################################################################
# Run main loop of app
######################################################################################################

app = RecipeManager()
app.geometry("720x480")
app.mainloop()