import PyQt5.QtWidgets as wid
import PyQt5.QtCore as core
import PyQt5.QtGui as gui
import RecipeDatabaseInterface as rdi
import os
import sys

# Subclass QWidget as empty container for browse page
class BrowsePage(wid.QWidget):
    '''
    This page allows users to browse recipes without specific searches.

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



# Subclass QWidget as empty container for search page
class SearchPage(wid.QWidget):
    '''
    This page allows users to search for specific recipes.

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



# Subclass QWidget as empty container for random page
class RandomPage(wid.QWidget):
    '''
    This page selects and displays a random recipe from the database.

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