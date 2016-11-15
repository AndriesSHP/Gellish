import os
from copy import deepcopy
from InitializeFormal Language import *
import ColNameIndexes as Cind
import Data.TestDBcontent as Rows

# Determine and initialize GUI_language
GUI_language    = "English"
GUI = GUILanguage(GUI_language)

# Determine and initialize formal_language
formal_language = "English"
Gellish = FormalLanguage(formal_language)

# Determine and initialize output language preferences
party = "Andries"
output_language = OutputLanguage(party)

# Create a new language defining database
# remove the old database for enabling to create a database with the same name.
FL_name = "FormalEnglishDB"
FLDB = Database(FL_name)     # create Formal Language Database

# Read CSV files and import content in FE dictionary database
ont_file_name = os.path.join("Data", "TestDBcontent.csv")
# file_name = os.path.join("Data", "Taxonomic Dictionary of Formal English (core).csv")
ontology_files = [ont_file_name]
for file in ontology_files:
    fill = ImportCSVinDatabase(file)

PR_name = "ProductDatabase"
PRDB = Database(PR_name)
# Read CSV file and import content in knowledge/requirements or product database.
mod_file_name = os.path.join("Data", "TestDBcontent2.csv")
# file_name = os.path.join("Data", "Semantic Model of a Road network N5.csv")
model_files = [mod_file_name]
for file in model_files:
    fill = ImportCSVinDatabase(file)

# Add and/or modify database content
# *** TO BE DONE ***

# Read database and Build semantic network from DBs content
f_eng = SemanticNetwork(FLDB)
f_eng = SemanticNetwork(PRDB)

# Search for data about kinds or individuals and display in various views
