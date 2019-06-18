import os 
import recipe_database_interface as rdi

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