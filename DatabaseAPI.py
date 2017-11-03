import sqlite3
import os
import sys
import csv
from Expr_Table_Def import *
from tkinter import filedialog
from Bootstrapping import *
from GellishDict import GellishDict
    
class Database:
    """ Initialize a new SQLite database (:in memory: or on external memory)
        with two kinds of tables:
          expression tables including various tables for expressions,
          and a naming table for a dictionary with names_in_contexts and UIDs.
        Read CSV files and load them into the various tables.
    """
    def __init__(self, db_name):
        """ Create a database with two kinds of tables.
        """
        self.name          = db_name
        # Initially the base ontology is loaded
        self.base = True
        
        if db_name == ":memory:":
            self.db_connect = sqlite3.connect(db_name)
        else:
            self.db_connect = sqlite3.connect("%s.db3"% db_name)
        self.db_cursor = self.db_connect.cursor()

    def Create_tables(self):
        """ Call the creation method for a number of tables
            with Gellish expressions and a naming table.
        """
        table_names = ["base_ontology", "domain_dictionaries", "productsANDprocesses", "namingTable"]
        # "knowledge", "requirements"
        for table_name in table_names:
            table = self.CreateTable(table_name)
            #print("  Database '%s' table '%s' created." % (self.name, table_name))

    def CreateTable(self, table_name):
        """ Create a generic Gellish SQL expression table in 'database' (cursor)
        or a naming table that relates (language,community,name) to UID.
        """
        # Define fields for expression table
        exprFields = [("presSeq", "text")     , ("langUID", "integer"),\
                      ("langName", "text")    , ("commUID", "integer"),\
                      ("commName", "text")    , ("reality", "text"),\
                      ("intentUID", "integer"), ("intentName", "text"),\
                      ("lhCard", "text")      , ("lhUID", "integer"),\
                      ("lhName", "text")      , ("lhRoleUID", "integer"),\
                      ("lhRoleName", "text")  , ("applContUID", "integer"),\
                      ("applContName", "text"), ("ideaUID", "integer primary key"),\
                      ("ideaDesc", "text")    , ("relUID", "integer"),\
                      ("relName", "text")     , ("phraseTypeUID", "integer"),\
                      ("rhRoleUID", "integer"), ("rhRoleName", "text"),\
                      ("rhCard", "text")      , \
                      ("rhUID", "integer")    , ("rhName", "text")      , \
                      ("partDef", "text")     , ("fullDef", "text")     , \
                      ("uomUID", "integer")   , ("uomName", "text")     , \
                      ("accUID", "integer")   , ("accName", "text")     , \
                      ("pickListUID","integer"),("pickListName", "text"),\
                      ("remarks", "text")     , ("status", "text"),\
                      ("reason", "text")      , ("succUID", "integer"),\
                      ("dateStartApp", "text"), ("dateStartAvail", "text"),\
                      ("dateCreaCopy", "text"), ("dateLatCh", "text"),\
                      ("originatorUID","integer"),("originatorName", "text"),\
                      ("authLatChUID","integer") ,("authLatChName", "text"),\
                      ("addrUID", "integer")  , ("addrName", "text"),\
                      ("refs", "text")        , ("exprUID", "integer"),\
                      ("collUID", "integer")  , ("collName", "text"),\
                      ("fileName", "text")    , ("lhStringComm", "text"),\
                      ("rhStringComm", "text"), ("relStringComm", "text")]
                       # 55 columns (id 0..54)

        # namingColIDs are [69,71,101,60,2] # languageUID, langCommUID, name, relUID, UID
        # Define columns for namingTable.
        namingFields = [("langUID", "integer"), ("commUID", "integer"),\
                        ("termName", "text")  , ("relUID", "integer") ,\
                        ("nameUID", "integer")]
        
        if table_name == 'namingTable':
            fields = namingFields
        else:
            fields = exprFields

        fieldsString = ""
        for f in fields:
            if f == fields[-1]:
                # last field does not have a trailing comma
                fieldsString += "\n%-16s%s" % f
            else:
                fieldsString += "\n%-16s%s," % f

        # print(table_name, fieldsString)
        command = "CREATE TABLE %s(%s)" % (table_name, fieldsString)
        self.db_cursor.execute(command)                    
        self.db_connect.commit()
#-------------------------------------------------------------
    def InsertRowInTable(self, table_name, row):
        """Insert one row in table_name into GellishDB'."""
        
        # Insert row of data in table table_name
        command = "INSERT OR REPLACE INTO %s VALUES (?%s)" % (table_name,54*",?")
        try:
            self.db_cursor.execute(command, row)
        except sqlite3.IntegrityError:
            print('ERROR: IdeaUID %i already exists. Insertion ignored.' % (row[15]))
            
        # Save (commit) the addition
        self.db_connect.commit()
#-------------------------------------------------------------
    def InsertRowsInTable(self, table_name, rows):
        """Insert a number of rows in table_name in GellishDB.
        """
        # Insert a number of rows of data in table table_name
        command = "INSERT OR REPLACE INTO %s VALUES (?%s)" % (table_name,54*",?")
        try:
            self.db_cursor.executemany(command, rows)
        except (sqlite3.IntegrityError, sqlite3.OperationalError):
            for row in rows:
                try:
                    self.db_cursor.execute(command, row)
                except sqlite3.IntegrityError:
                    print('** Error: IdeaUID %i already exists. Insertion ignored.' % (row[15]))
                except sqlite3.OperationalError:
                    print("** Error: Row could not be interpreted and is skipped: %s " % row)
            
        # Save (commit) the additions
        self.db_connect.commit()
#------------------------------------------------ -------------
    def SearchRowsInTable(self, table_name, criteria):
        """Search for rows in database where criteria
        specifies a list of triples (colName,' and ' or ' or ',value)
        that should all match on each found row.
        """
        values  = []
        command = 'select * from %s where ' % (table_name)
        first   = True
        for crit in criteria:
            if first == True:
                query = command + crit[0] + '=?'
                #query = 'select * from table_name where ' + crit[0] + '=?'
                values.append(crit[2])
                first = False
            else:
                query = query + crit[1] + crit[0] + '=?'
                values.append(crit[2])
        print(query)
        print(values)
        resultTable = []
        #for row in db_connect.execute('select * from table_name where lhName=? and rhName=?',(values)):
        #for row in db_connect.execute(query,(values)):
        #    resultTable.append(row)
        self.db_cursor.execute(query,(values))
        resultTable = self.db_cursor.fetchall()
        return(resultTable)

#-------------------------------------------------------------
if __name__ == "__main__":
    from SystemUsers import User
    # Test creation of new database and loading with data
    # Choose GUI language
    user = User('Andries')
    user.GUI_language = "English"
    user.GUI_index = 0

    # Create a semantic network
    net_name = 'Semantic network'
    Gel_net = Semantic_Network(net_name)
    # Create a new database external or in-memory with a number of tables.
    #db_name = ':memory:'
    db_name = 'TestEnglishDB'
    #db_name = 'RoadDB'
    new = input("Enter new (n) or existing (e): ")
    if new == "n":
        try:
            os.remove(db_name + ".db3")
        except OSError:
            pass
    Gel_db = Database(db_name)     # create or connect to Formal English Database
    if new == "n":
        print("Database: %s created." % (Gel_db.name))
        Gel_db.Create_tables()
    else:
        print("Database: %s connected." % (Gel_db.name))

    # Include one or more files in the various tables
    Gel_db.Combine_Files_with_Network(Gel_net)
    addition = 'y'  # y = Option for input of more than one file
    while addition == 'y':
        addition = input("\nMore import files? (y/n): ")
        if addition == 'y':
            Gel_db.Combine_Files_with_Network(Gel_net)

    # Test searching in table "base_ontology"
    expr_table_name = "base_ontology"
    # search for matching rows
    criteria = [('lhName', ' and ', "specialization relation between kinds of things")] #,('status',' and ', "accepted")]
    resultTable = Gel_db.SearchRowsInTable(expr_table_name, criteria)
    for row in resultTable[0:4]:
        print('result-1: ',row[10],row[18],row[24])
    #Gel_db.db_connect.close()

    # read whole "base_ontology" table
    Gel_db.db_cursor.execute('select * from base_ontology')
    result = Gel_db.db_cursor.fetchall()
    for row in result[0:4]:
        print('result-2: ',row[10],row[18],row[24])

    # Test searching in table "domain_dictionaries"
    expr_table_name = "domain_dictionaries"
    # search for matching rows
    criteria = [('lhName', ' and ', "m")] #,('status',' and ', "accepted")]
    resultTable = Gel_db.SearchRowsInTable(expr_table_name, criteria)
    for row in resultTable:
        print('result-1: ',row[10],row[18],row[24])
