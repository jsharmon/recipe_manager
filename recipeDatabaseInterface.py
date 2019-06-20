"""
This set of functions makes it easier to create and work with the databases that contain recipes.
SQLite3 is used for the creation, management, and access of recipe databases.
"""

import sqlite3 as sql
import os

# Create a new database if new user is creating username
def createNewDB(recipePath):
    dbName = os.path.join(recipePath, 'RecipeFile.db')
    conn = sql.connect(dbName)
    c = conn.cursor()
    c.execute('''CREATE TABLE recipes
             (recipeName, recipeSummary, dateAdded, cuisine, ingredientList,
              recipeText, prepTime, cookTime, calories, servings, userTags)''')
    conn.commit()
    conn.close()

# Check to see if the database is currently empty
def isDBEmpty(recipePath):
    dbName = os.path.join(recipePath, 'RecipeFile.db')
    conn = sql.connect(dbName)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM recipes')
    rowCount = c.fetchall()[0][0]
    conn.close()

    # Check row count
    if(rowCount == 0):
        DBIsEmpty = True
    else:
        DBIsEmpty = False

    return DBIsEmpty

# Insert a recipe into the table recipes as a single new row
def insertRecipe(recipePath, entryText):
    dbName = os.path.join(recipePath, 'RecipeFile.db')
    conn = sql.connect(dbName)
    c = conn.cursor()
    c.execute('INSERT INTO recipes VALUES (?,?,?,?,?,?,?,?,?,?,?)', entryText)
    conn.commit()
    conn.close()