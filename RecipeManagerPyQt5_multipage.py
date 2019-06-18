import PyQt5.QtWidgets as wid
import PyQt5.QtCore as core
import PyQt5.QtGui as gui
import recipeDatabaseInterface as rdi
import os
import sys

# Subclass QMainWindow to serve as empty container for z-stack of page widgets
class RecipeManager(wid.QMainWindow):   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.homePage = LoginPage()
        self.homePageEmptyDB = LoginPage()
        self.addPage = LoginPage()
        self.randomPage = LoginPage()
        self.searchPage = LoginPage()
        self.urlPage = LoginPage()
        self.mealPlanningPage = LoginPage()
        self.groceryListPage = LoginPage()
        self.mealTrackingPage = LoginPage()

        self.generateMenu()
        # Implement stacking of pages below

    def generateMenu(self):
        # Generate parent menu bar
        navMenu = self.menuBar()
        
        # Populate file submenu
        self.populateFileMenu(navMenu)
        
        # Populate recipe submenu
        self.populateRecipeMenu(navMenu)

        # Populate planning submenu
        self.populatePlanningMenu(navMenu)

    def populateFileMenu(self, navMenu):
        # Define quit action and callback
        quitAction = wid.QAction('&Quit', self)
        quitAction.triggered.connect(sys.exit)

        # Generate submenu, add action
        fileMenu = navMenu.addMenu('&File')
        fileMenu.addAction(quitAction)

    def populateRecipeMenu(self, navMenu):
        # Define actions and assign signals to callback slots
        # NOTE: I need to define the pages before this and somehow pass to these methods!
        addRecipe = wid.QAction('&Add recipe', self)
        addRecipe.triggered.connect(lambda: self.showFrame('addPage', self.addPage))

        randomRecipe = wid.QAction('&Get random recipe', self)
        randomRecipe.triggered.connect(lambda: self.showFrame('randomPage', self.randomPage))

        searchRecipe = wid.QAction('&Search recipes', self)
        searchRecipe.triggered.connect(lambda: self.showFrame('searchPage', self.searchPage))

        urlRecipe = wid.QAction('&Grab recipe from URL', self)
        urlRecipe.triggered.connect(lambda: self.showFrame('urlPage', self.urlPage))

        # Generate submenu, add actions
        recipeMenu = navMenu.addMenu('&Recipes')
        recipeMenu.addAction(addRecipe)
        recipeMenu.addAction(randomRecipe)
        recipeMenu.addAction(searchRecipe)
        recipeMenu.addAction(urlRecipe)
    
    def populatePlanningMenu(self, navMenu):
        # Define actions and assign signals to callback slots
        # NOTE: I need to define the pages before this and somehow pass to these methods!
        mealPlan = wid.QAction('&Meal planning', self)
        mealPlan.triggered.connect(lambda: self.showFrame('mealPlanningPage', self.mealPlanningPage))

        groceryListGen = wid.QAction('&Grocery list generator', self)
        groceryListGen.triggered.connect(lambda: self.showFrame('groceryListPage', self.groceryListPage))

        mealTracking = wid.QAction('&Meal tracking', self)
        mealTracking.triggered.connect(lambda: self.showFrame('mealTrackingPage', self.mealTrackingPage))

        # Generate submenu, add actions
        planningMenu = navMenu.addMenu('&Planning')
        planningMenu.addAction(mealPlan)
        planningMenu.addAction(groceryListGen)
        planningMenu.addAction(mealTracking)

    def showFrame(self, page, pageObject):
        # Navigate to a specified page based on pageObject.
        # page is just a string used for testing at the moment.
        print(page)



# Subclass QWidget - just an empty container - to serve as the container for the login page
class LoginPage(wid.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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
            # Repopulate QLineEdit to indicate user can now navigate to
            # other pages in app after successful login
            lineEdit.setText('Login successful! Use menu to navigate to other pages...')

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

            # Repopulate QLineEdit to indicate user can now navigate to
            # other pages in app after successful login
            lineEdit.setText('Account creation successful! Use menu to navigate to other pages...')

        # If directory exists, display 'That username is already taken.'
        else:
            lineEdit.setText('That username is already taken.')


if __name__ == '__main__':
    app = wid.QApplication([])
    window = LoginPage()
    window.show()
    app.exec_()