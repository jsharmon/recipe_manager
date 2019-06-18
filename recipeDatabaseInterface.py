"""
This set of functions makes it easier to create and work with the databases that contain recipes.
SQLite3 is used for the creation, management, and access of recipe databases.
"""

import sqlite3 as sql
import os

def createNewDB(recipePath):
    dbName = os.path.join(recipePath, 'RecipeFile.db')
    conn = sql.connect(dbName)
    c = conn.cursor()
    c.execute('''CREATE TABLE recipes
             (recipeName, recipeSummary, dateAdded, cuisine, ingredientNames, 
             ingredientAmounts, recipeText, prepTime, cookTime, calories,
             servings, userTags)''')
    conn.commit()
    conn.close()

def isDBEmpty(recipePath):
    dbName = os.path.join(recipePath, 'RecipeFile.db')
    conn = sql.connect(dbName)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM recipes")
    rowCount = c.fetchall()[0][0]
    conn.close()

    if(rowCount == 0):
        DBIsEmpty = True
    else:
        DBIsEmpty = False

    return DBIsEmpty

def insertRecipeRowTest(recipePath):
    dbName = os.path.join(recipePath, 'RecipeFile.db')
    conn = sql.connect(dbName)
    c = conn.cursor()
    c.execute("INSERT INTO recipes VALUES (1,1,1,1,1,1,1,1,1,1,1,1)")
    conn.commit()
    conn.close()