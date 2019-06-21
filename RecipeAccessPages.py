import PyQt5.QtWidgets as wid
import PyQt5.QtCore as core
import PyQt5.QtGui as gui
import RecipeDatabaseInterface as rdi
import os
import sys

# Subclass QWidget as empty container for browse page
class BrowsePage(wid.QWidget):
    def __init__(self, DBPath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the path to the database as instance variable
        self.DBPath = DBPath



# Subclass QWidget as empty container for search page
class SearchPage(wid.QWidget):
    def __init__(self, DBPath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the path to the database as instance variable
        self.DBPath = DBPath



# Subclass QWidget as empty container for random page
class RandomPage(wid.QWidget):
    def __init__(self, DBPath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the path to the database as instance variable
        self.DBPath = DBPath