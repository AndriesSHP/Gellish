import sqlite3

class Database:
    def __init__(self, DBName):
        self.name = DBName
        self.dbConnect = sqlite3.connect("%s.db3"% DBName)
        self.dbCursor  = self.dbConnect.cursor()
        self.exprFields = [("presSeq", "text")     , ("langUID", "integer"),\
                           ("langName", "text")    , ("commUID", "integer"),\
                           ("commName", "text")    , ("reality", "text"),\
                           ("intentUID", "integer"), ("intentName", "text"),\
                           ("lhCard", "text")      , ("lhUID", "integer"),\
                           ("lhName", "text")      , ("lhRoleUID", "integer"),\
                           ("lhRoleName", "text")  , ("applContUID", "integer"),\
                           ("applContName", "text"), ("ideaUID", "integer primary key"),\
                           ("ideaDesc", "text")    , ("relUID", "integer"),\
                           ("relName", "text")     , ("rhRoleUID", "integer"),\
                           ("rhRoleName", "text")  , ("rhCard", "text"),\
                           ("rhUID", "integer")    , ("rhName", "text"),\
                           ("partDef", "text")     , ("fullDef", "text"),\
                           ("uomUID", "integer")   , ("uomName", "text"),\
                           ("accUID", "integer")   , ("accName", "text"),\
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
                           ("rhStringComm", "text"), ("relStringComm", "text"),\
                           ("phraseTypeUID", "integer")]    # 55 columns (id 0..54)

        # namingColIDs = [69,71,101,60,2] # languageUID, langCommUID, name, relUID, UID
        # column names for namingTable.
        self.namingFields = [("langUID", "integer"), ("commUID", "integer"),\
                             ("termName", "text")   , ("relUID", "integer") ,\
                             ("nameUID", "integer")]

    def CreateTable(self, tableName):
        """ Create a generic Gellish SQL expression table in 'database' (cursor)
        or a naming table that relates (language,community,name) to UID.
        """

        if tableName == 'namingTable':
            self.fields = self.namingFields
        else:
            self.fields = self.exprFields

        fieldsString = ""
        for f in self.fields:
            if f == self.fields[-1]:
                # last field does not have a trailing comma
                fieldsString += "\n%-16s%s" % f
            else:
                fieldsString += "\n%-16s%s," % f

        command = "CREATE TABLE %s(%s)" % (tableName, fieldsString)
        self.dbCursor.execute(command)                    
        self.dbConnect.commit()
#-------------------------------------------------------------
    def InsertRowInTable(self, tableName, row):
        """Insert one row in tableName into GellishDB'."""
        
        # Insert row of data in table tableName   
        try:
            command = "INSERT INTO %s VALUES (?%s)" % (tableName,54*",?")
            self.dbCursor.execute(command, row)
            # self.dbCursor.execute("INSERT INTO tableName VALUES (?%s)" % (54*",?"),row)
        except sqlite3.IntegrityError:
            print('ERROR: FactUID %i already exists. Insertion ignored.' % (row[15]))
            
        # Save (commit) the addition
        self.dbConnect.commit()
#-------------------------------------------------------------
    def InsertRowsInTable(self, tableName, rows):
        """Insert a number of rows in tableName in GellishDB.
        """
   
        # Insert a number of rows of data in table tableName 
        try:
            command = "INSERT INTO %s VALUES (?%s)" % (tableName,54*",?")
            self.dbCursor.executemany(command, rows)
            # self.dbCursor.executemany("INSERT INTO tableName VALUES (?%s)" % (54*",?"), rows)
        except sqlite3.IntegrityError:
            print('Error: An Idea UID in the table already exists. Insertion ignored.')
            
        # Save (commit) the additions
        self.dbConnect.commit()
#------------------------------------------------ -------------
    def SearchRowsInTable(self, tableName, criteria):
        """Search for rows in databaseName where criteria
        specifies a list of triples (colName,' and ' or ' or ',value) for matching.
        """

        values  = []
        command = 'select * from %s where ' % (tableName)
        first   = True
        for crit in criteria:
            if first == True:
                query = command + crit[0] + '=?'
                #query = 'select * from tableName where ' + crit[0] + '=?'
                values.append(crit[2])
                first = False
            else:
                query = query + crit[1] + crit[0] + '=?'
                values.append(crit[2])
        print(query)
        print(values)
        resultTable = []
        #for row in dbConnect.execute('select * from tableName where lhName=? and rhName=?',(values)):
        #for row in dbConnect.execute(query,(values)):
        #    resultTable.append(row)
        self.dbCursor.execute(query,(values))
        resultTable = self.dbCursor.fetchall()
        return(resultTable)
#-------------------------------------------------------------

if __name__ == "__main__":
    import os
    from copy import deepcopy
    import ColNameIndexes as Cind
    import Data.TestDBcontent as Rows
    # remove the old database because otherwise we cannot create a database with the same name:
    try:
        os.remove("FormalEnglishDB.db3")
    except OSError:
        pass
    FED = Database("FormalEnglishDB")     # create Formal English Database
    tableName = "expressions"
    FED.CreateTable(tableName)
    print(FED.name, " database created and/or connected. Table %s created" % (tableName))
    #print(Rows.expr[0])
    FED.InsertRowInTable (tableName, Rows.expr[0])
    FED.InsertRowsInTable(tableName, Rows.expr[1:])
    criteria = [('lhName', ' and ', "specialization relation between kinds of things")] #,('status',' and ', "accepted")]
    resultTable = FED.SearchRowsInTable(tableName, criteria)
    print('resultTable:', resultTable)
    #FED.dbConnect.close()


