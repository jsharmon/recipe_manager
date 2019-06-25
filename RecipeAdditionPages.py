import PyQt5.QtWidgets as wid
import RecipeDatabaseInterface as rdi
import os
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

# Subclass QDialog for 'Recipe Added!' message
class RecipeAddedDialog(wid.QDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set layout; this is a vertical box orientation
        layout = wid.QVBoxLayout()

        # Add label and button
        label = wid.QLabel('Recipe Added!')
        layout.addWidget(label)
        button = wid.QPushButton('Return to app...')
        button.pressed.connect(lambda: self.accept())
        layout.addWidget(button)

        # Set layout for dialog
        self.setLayout(layout)

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

        # Insert the recipe as a new row in the DB, recipes table
        rdi.insertRecipe(self.DBPath, entryText)
        ############################################################################################################################
        # Bare minimum check to make sure a name, ingredients, and recipe text have been entered
        # Need to handle empty entries as well; empty strings
        # Check for duplicate recipes based on name, case insensitive
        # Setup another dialog window for failed addition, don't clear entries in that case
        # Return a flag from either successful added dialog or 
        # Don't do any more of this until after SQL on Coursera
        ############################################################################################################################

        # Show dialog stating that the recipe has been added
        recipeAdded = RecipeAddedDialog()
        recipeAdded.exec_()

        # Clear the entries after the dialog has been closed
        for entry in textEntries:
            entry.clear()

    def populateEntries(self, layout):
        # Names of text entries to add
        lineEntriesFirst = ['Recipe Name:', 'Recipe Summary:', "Today's Date (mm/dd/yyyy):", 'Type of cuisine:']
        plainTextEdits = ['Ingredients (format - ingredient,amount,unit then enter):', 'Recipe Text:']
        lineEntriesSecond = ['Prep Time (mins):', 'Cook Time (mins):', 'Calories:', 'Servings:', 'Tags:']

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

        # Return entry to get text later
        return edit



# Subclass QDialog for edit scraped entry dialog
# Had to copy/paste code from AddPage...wasn't sure how to
# inherit from it and have it still be a dialog object
class EditScrapedEntryDialog(wid.QDialog):
    def __init__(self, DBPath, recipeURL, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the path to the database as instance variable,
        # set recipe URL from text entry
        self.DBPath = DBPath
        self.recipeURL = recipeURL

        # Set layout; this is a vertical box orientation
        layout = wid.QVBoxLayout()

        # Populate entries for AddPage, get text entry objects to get text later
        textEntries = self.populateEntries(layout)

        # Use BeautifulSoup to parse html from web page, get list of
        # strings to populate dialog text entries
        self.scrapeRecipe(textEntries, self.recipeURL)

        # Create add button, connect a signal (button press)
        addButton = wid.QPushButton('Add Recipe')
        addButton.pressed.connect(lambda: self.addCallback(textEntries))
        layout.addWidget(addButton)

        # Set layout
        self.setLayout(layout)

    def scrapeRecipe(self, textEntries, recipeURL):
        # Grab the html from the webpage
        html = urllib.request.urlopen(recipeURL).read()

        # Create BeautifulSoup object to parse html
        soup = BeautifulSoup(html, 'html.parser')

        #######################################################################################
        # Get list of strings with appropriate data from
        # webpage

        # Populate text entries with scraped strings

        # Set up way to save original URL or at least have a source associated with recipe
        #######################################################################################

    def addCallback(self, textEntries):
        # Get the text from each entry, read into list of strings
        entryText = []
        for entry in textEntries:
            # For line edits, use .text() method
            if type(entry) == type(wid.QLineEdit()):
                entryText.append(entry.text())

            if type(entry) == type(wid.QTextEdit()):
                entryText.append(entry.toPlainText())

        # Insert the recipe as a new row in the DB, recipes table
        rdi.insertRecipe(self.DBPath, entryText)
        ############################################################################################################################
        # Bare minimum check to make sure a name, ingredients, and recipe text have been entered
        # Need to handle empty entries as well; maybe set to np.NaN
        # Check for duplicate recipes based on name, case insensitive
        # Setup another dialog window for failed addition, don't clear entries in that case
        # Return a flag from either successful added dialog or 
        # Don't do any more of this until after SQL on Coursera
        ############################################################################################################################

        # Show dialog stating that the recipe has been added
        recipeAdded = RecipeAddedDialog()
        recipeAdded.exec_()

        # Clear the entries after the dialog has been closed
        for entry in textEntries:
            entry.clear()

        # Close URL scraped text entry edit dialog
        self.accept()

    def populateEntries(self, layout):
        # Names of text entries to add
        lineEntriesFirst = ['Recipe Name:', 'Recipe Summary:', "Today's Date (mm/dd/yyyy):", 'Type of cuisine:']
        plainTextEdits = ['Ingredients (format - ingredient,amount,unit then enter):', 'Recipe Text:']
        lineEntriesSecond = ['Prep Time (mins):', 'Cook Time (mins):', 'Calories:', 'Servings:', 'Tags:']

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

        # Return entry to get text later
        return edit

# Subclass QWidget as empty container for url import page
class URLImportPage(wid.QWidget):
    def __init__(self, DBPath, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the path to the database as instance variable
        self.DBPath = DBPath

        # Set layout; this is a vertical box orientation
        layout = wid.QVBoxLayout()

        # Create QLineEdit for URL entry
        urlEntry = wid.QLineEdit()
        urlEntry.setText('Enter URL...')
        urlEntry.returnPressed.connect(lambda: self.urlCallback(urlEntry))
        layout.addWidget(urlEntry)

        # Create add button, connect a signal (button press)
        addButton = wid.QPushButton('Get Recipe')
        addButton.pressed.connect(lambda: self.urlCallback(urlEntry))
        layout.addWidget(addButton)

        # Set layout
        self.setLayout(layout)

    def urlCallback(self, urlEntry):
        # Show dialog for editing scraped recipe text
        url = urlEntry.text()
        editScrapedEntry = EditScrapedEntryDialog(self.DBPath, url)
        editScrapedEntry.exec_()