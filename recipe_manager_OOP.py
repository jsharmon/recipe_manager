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
11) Make it pretty.

"""

import tkinter as tk

LARGE_FONT= ("Verdana", 12)

# Creating a class for the actual recipe manager GUI backend
class RecipeManager(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        frame = StartPage(container, self)
        self.frames[StartPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Creating class for the start page
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="This is the start page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
		

app = RecipeManager()
app.mainloop()

"""
# Create a class for each recipe
class Recipe():
    def __init__(self, *args, **kwargs):
        pass
"""