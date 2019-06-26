import PyQt5.QtWidgets as wid
import PyQt5.QtCore as core
import PyQt5.QtGui as gui
import RecipeDatabaseInterface as rdi
import os
import sys

# Subclass QWidget as empty container for meal planning page
class MealPlanningPage(wid.QWidget):
    '''
    This page allows the user to plan meals for the week.

    This class inherits from PyQt5.QtWidgets.QWidget.

    Attributes:
        DBPath (str): The path to the recipe database as determined during login.

    Constructor Args:
        DBPath (str): The path to the recipe database as determined during login.
    '''
    def __init__(self, DBPath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the path to the database as instance variable
        self.DBPath = DBPath



# Subclass QWidget as empty container for grocery list page
class GroceryListPage(wid.QWidget):
    '''
    This page generates a grocery list based on a number of user-selected recipes.

    This class inherits from PyQt5.QtWidgets.QWidget.

    Attributes:
        DBPath (str): The path to the recipe database as determined during login.

    Constructor Args:
        DBPath (str): The path to the recipe database as determined during login.
    '''

    def __init__(self, DBPath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the path to the database as instance variable
        self.DBPath = DBPath



# Subclass QWidget as empty container for meal tracking page
class MealTrackingPage(wid.QWidget):
    '''
    This page analyzes and visualizes user data, primarily what they've been cooking.

    This class inherits from PyQt5.QtWidgets.QWidget.

    Attributes:
        DBPath (str): The path to the recipe database as determined during login.

    Constructor Args:
        DBPath (str): The path to the recipe database as determined during login.
    '''

    def __init__(self, DBPath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the path to the database as instance variable
        self.DBPath = DBPath