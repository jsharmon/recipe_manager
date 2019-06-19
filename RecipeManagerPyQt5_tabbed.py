import PyQt5.QtWidgets as wid
import PyQt5.QtCore as core
import PyQt5.QtGui as gui
import recipeDatabaseInterface as rdi
import os
import sys

# Subclass QDialog - just an empty container - to serve as the container for the login page
# Have the login run as a dialog before going to main app
class LoginDialog(wid.QDialog): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create variable for DB path to associate with dialog instance later,
        # pass to recipe manager upon creation
        self.DBPath = ''
        
        # Set window title
        self.setWindowTitle('Login')

        # Set layout; this is a vertical box orientation
        layout = wid.QVBoxLayout()

        # Add widgets to allow returning users to login
        self.populateReturningUser(layout)

        # Add widgets to allow new users to create username/new recipe DB
        self.populateNewUser(layout)

        # Set layout
        self.setLayout(layout)

    def populateReturningUser(self, layout):
        # Create a label
        returningUserLabel = wid.QLabel('For returning users, enter username:')
        layout.addWidget(returningUserLabel)

        # Create a text entry line, connect a signal (carriage return)
        loginEntry = wid.QLineEdit('Enter Username...')
        loginEntry.returnPressed.connect(lambda: self.loginCallback(loginEntry))
        layout.addWidget(loginEntry)

        # Create a push button, connect a signal (button press)
        loginButton = wid.QPushButton('Login')
        loginButton.pressed.connect(lambda: self.loginCallback(loginEntry))
        layout.addWidget(loginButton)

    def populateNewUser(self, layout):
        # Create a label
        newUserLabel = wid.QLabel('For new users, choose username:')
        layout.addWidget(newUserLabel)

        # Create a text entry line, connect a signal (carriage return)
        newUserEntry = wid.QLineEdit('Choose New Username...')
        newUserEntry.returnPressed.connect(lambda: self.newUserCallback(newUserEntry))
        layout.addWidget(newUserEntry)

        # Create a second push button, connect a signal (button press)
        newUserButton = wid.QPushButton('Register New User')
        newUserButton.pressed.connect(lambda: self.newUserCallback(newUserEntry))
        layout.addWidget(newUserButton)

    def loginCallback(self, lineEdit):
        # Get text from QLineEdit
        userNameReturning = lineEdit.text()

        # Define recipe path, check if directory exists
        recipePath = os.path.join(os.getcwd(), 'RecipeManager', userNameReturning)

        if(os.path.isdir(recipePath)):
            # Repopulate QLineEdit, close dialog, set path to pass to other page classes
            self.DBPath = recipePath
            lineEdit.setText('Login successful!')
            self.accept()

        # If directory does not exist, display 'That username does not exist.'
        else:
            lineEdit.setText('That username does not exist.')
    
    def newUserCallback(self, lineEdit):
        # Get text from QLineEdit
        usernameNew = lineEdit.text()
    
        # Get current working directory, add 'RecipeManager' for folder to store all
        # related files
        thisFileDir = os.getcwd() + '\\' + 'RecipeManager'

        # If running on new computer, create recipe manager folder
        if(not(os.path.isdir(thisFileDir))):
            os.mkdir(thisFileDir)

        # If folder doesn't already exist, make it and make a new recipe text file
        recipePath = thisFileDir + '\\' + usernameNew
        if(not(os.path.isdir(recipePath))):
            # Create folder with username
            os.mkdir(recipePath)

            # Create new SQL database to hold recipes
            rdi.createNewDB(recipePath)

            # Repopulate QLineEdit, close dialog, set path to pass to other classes
            self.DBPath = recipePath
            lineEdit.setText('Account creation successful!')
            self.accept()

        # If directory exists, display 'That username is already taken.'
        else:
            lineEdit.setText('That username is already taken.')



# Subclass QWidget to serve as empty container for home page
class HomePage(wid.QWidget):
    def __init__(self, DBPath, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set path to DB
        self.DBPath = DBPath



# Subclass QWidget to serve as empty container for add page
class AddPage(wid.QWidget):
    def __init__(self, DBPath, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set path to DB
        self.DBPath = DBPath

        # Set layout; this is a vertical box orientation
        layout = wid.QVBoxLayout()

        # Populate entries for AddPage, get text entry objects to get text later
        textEntries = self.populateEntries(layout)

        # Create add button, connect a signal (button press)
        addButton = wid.QPushButton('Add Recipe')
        addButton.pressed.connect(lambda: self.addCallback(textEntries))
        layout.addWidget(addButton)

        # Set layout
        self.setLayout(layout)

    def addCallback(self, textEntries):
        # Get the text from each entry, read into list of strings
        entryText = []
        for entry in textEntries:
            # For line edits, use .text() method
            if type(entry) == type(wid.QLineEdit()):
                entryText.append(entry.text())

            if type(entry) == type(wid.QTextEdit()):
                entryText.append(entry.toPlainText())

        # Now, actually do some SQL stuff to add the recipe to the DB
        ############################################################################################################################
        # Need to implement recipe adding! will come from recipeDatabaseInterface.py!
        ############################################################################################################################

    def populateEntries(self, layout):
        # Names of text entries to add
        lineEntriesFirst = ['Recipe Name:', 'Recipe Summary:', "Today's Date (mm/dd/yyyy):", 'Type of cuisine:']
        plainTextEdits = ['Ingredients (format - ingredient,amount,unit then enter):', 'Recipe Text:']
        lineEntriesSecond = ['Prep Time:', 'Cook Time:', 'Calories:', 'Servings:', 'Tags:']

        # Create empty list to fill with entry objects
        entries = []

        # Create all entries, append objects to list
        for name in lineEntriesFirst:
            labelEntryF = self.newLabelEntry(layout, name)
            entries.append(labelEntryF)
        for name in plainTextEdits:
            textEdit = self.newPlainTextEdit(layout, name)
            entries.append(textEdit)
        for name in lineEntriesSecond:
            labelEntryS = self.newLabelEntry(layout, name)
            entries.append(labelEntryS)

        return entries

    def newLabelEntry(self, layout, name):
        # Generate label and add to layout
        label = wid.QLabel(name)
        layout.addWidget(label)

        # Generate associated text entry and add to layout
        entry = wid.QLineEdit()
        layout.addWidget(entry)

        # Return entry to get text later
        return entry

    def newPlainTextEdit(self, layout, name):
        # Generate label and add to layout
        label = wid.QLabel(name)
        layout.addWidget(label)

        # Generate associated plain text edit and add to layout
        edit = wid.QTextEdit()
        layout.addWidget(edit)

        return edit



# Subclass QMainWindow to serve as empty container for z-stack of page widgets
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
        pageNames = ['Home', 'Add', 'Random', 'Search', 'Import Recipe',
                     'Meal Planning', 'Grocery List', 'Meal Tracking']
        
        # Generate list of page objects for assigning to tabs
        pageObjects = [HomePage(self.DBPath), AddPage(self.DBPath), HomePage(self.DBPath), HomePage(self.DBPath), 
                       HomePage(self.DBPath), HomePage(self.DBPath), HomePage(self.DBPath), HomePage(self.DBPath)]

        for name, pageObj in zip(pageNames, pageObjects):
            tabs.addTab(pageObj, name)

        # Create scroll area in case window is resized, contain tabs within it
        scrollArea = wid.QScrollArea()
        scrollArea.setMinimumWidth(tabs.sizeHint().width())
        scrollArea.setHorizontalScrollBarPolicy(core.Qt.ScrollBarAlwaysOff)
        scrollArea.setWidget(tabs)
        scrollArea.setWidgetResizable(True)

        # Set the scroll area as the central widget
        self.setCentralWidget(scrollArea)



if __name__ == '__main__':
    app = wid.QApplication([])
    login = LoginDialog()
    
    # If dialog has been accepted, close and run main app
    if login.exec_() == wid.QDialog.Accepted:
        window = RecipeManager(login.DBPath)
        window.show()
        app.exec_()