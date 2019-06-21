# General imports
import PyQt5.QtWidgets as wid
import PyQt5.QtCore as core
import PyQt5.QtGui as gui
import os
import sys

# Import custom widgets - pages and dialogs
from LoginManager import LoginDialog
from RecipeAccessPages import BrowsePage, SearchPage, RandomPage
from RecipeAdditionPages import AddPage, URLImportPage
from PlanningPages import MealPlanningPage, GroceryListPage, MealTrackingPage

# Import custom function modules
import RecipeDatabaseInterface as rdi



# Subclass QWidget to serve as empty container for home page
class HomePage(wid.QWidget):
    def __init__(self, DBPath, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set path to DB
        self.DBPath = DBPath



# Subclass QMainWindow to serve as empty container for tab widget
class RecipeManager(wid.QMainWindow):   
    def __init__(self, DBPath, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set DB path, passed from dialog
        self.DBPath = DBPath

        # Set window title
        self.setWindowTitle('Recipe Manager')

        # Generate tab widget to contain pages, navigate using tabs
        tabs = wid.QTabWidget()
        tabs.setDocumentMode(True)
        tabs.setTabPosition(wid.QTabWidget.North)
        tabs.setMovable(True)

        # Generate list of page names for labeling tabs
        pageNames = ['Home', 'Browse', 'Search', 'Random', 'Add', 'Import Recipe',
                     'Meal Planning', 'Grocery List', 'Meal Tracking']
        
        # Generate list of page objects for assigning to tabs
        pageObjects = [HomePage(self.DBPath), BrowsePage(self.DBPath), SearchPage(self.DBPath), 
                       RandomPage(self.DBPath), AddPage(self.DBPath), URLImportPage(self.DBPath), 
                       MealPlanningPage(self.DBPath), GroceryListPage(self.DBPath), 
                       MealTrackingPage(self.DBPath)]

        for name, pageObj in zip(pageNames, pageObjects):
            tabs.addTab(pageObj, name)

        # Create scroll area in case window is resized, contain tabs within it
        scrollArea = wid.QScrollArea()
        scrollArea.setMinimumWidth(tabs.sizeHint().width() + scrollArea.verticalScrollBar().sizeHint().width())
        scrollArea.setHorizontalScrollBarPolicy(core.Qt.ScrollBarAlwaysOff)
        scrollArea.setWidget(tabs)
        scrollArea.setWidgetResizable(True)

        # Set the scroll area as the central widget
        self.setCentralWidget(scrollArea)



# Run main loop; protect with __name__ == '__main__' check, although
# it's unlikely this file would be imported for other uses.
if __name__ == '__main__':
    app = wid.QApplication([])
    login = LoginDialog()
    
    # If dialog has been accepted, close and run main app
    if login.exec_() == wid.QDialog.Accepted:
        window = RecipeManager(login.DBPath)
        window.show()
        app.exec_()