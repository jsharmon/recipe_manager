import PyQt5.QtWidgets as wid
import RecipeDatabaseInterface as rdi
import os

# Subclass QDialog - just an empty container - to serve as the container for the login page
# Have the login run as a dialog before going to main app
######################################################################################################################
# Add checks to make sure usernames are valid - basically just if the chars can be used in a directory
# If not valid, display somethign like "Username invalid; no special chars" or something
######################################################################################################################
class LoginDialog(wid.QDialog):
    '''
    This dialog serves as a login page for users.

    This class inherits from PyQt5.QtWidgets.QDialog.

    Attributes:
        None.

    Constructor Args:
        None.
    '''

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