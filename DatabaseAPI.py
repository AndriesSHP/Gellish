import sqlite3
import os
import csv
import Expr_Table_Def as Ex
from InitializeFormalLanguage import *
from tkinter import filedialog

class Database:
    """ Create a database with two kinds of tables:
        one for expressions and one for a dictionary with names_in_contexts and UIDs.
    """
    def __init__(self, DB_name):
        # if DB_name == ":memory:" then the database is created in internal RAM memory.
        self.name = DB_name
        try:
            os.remove(DB_name + ".db3")
        except OSError:
            pass
        if DB_name == ":memory:":
            self.dbConnect = sqlite3.connect(DB_name)
        else:
            self.dbConnect = sqlite3.connect("%s.db3"% DB_name)
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
        
        table_name_1 = "expressions"
        table_name_2 = "namingTable"
        exprs = self.CreateTable(table_name_1)
        names = self.CreateTable(table_name_2)
        print("Database %s created and/or connected. Tables %s and %s are created."\
              % (self.name, table_name_1, table_name_2))

    def CreateTable(self, table_name):
        """ Create a generic Gellish SQL expression table in 'database' (cursor)
        or a naming table that relates (language,community,name) to UID.
        """

        if table_name == 'namingTable':
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

        command = "CREATE TABLE %s(%s)" % (table_name, fieldsString)
        self.dbCursor.execute(command)                    
        self.dbConnect.commit()
#-------------------------------------------------------------
    def InsertRowInTable(self, table_name, row):
        """Insert one row in table_name into GellishDB'."""
        
        # Insert row of data in table table_name   
        try:
            command = "INSERT INTO %s VALUES (?%s)" % (table_name,54*",?")
            self.dbCursor.execute(command, row)
            # self.dbCursor.execute("INSERT INTO table_name VALUES (?%s)" % (54*",?"),row)
        except sqlite3.IntegrityError:
            print('ERROR: FactUID %i already exists. Insertion ignored.' % (row[15]))
            
        # Save (commit) the addition
        self.dbConnect.commit()
#-------------------------------------------------------------
    def InsertRowsInTable(self, table_name, rows):
        """Insert a number of rows in table_name in GellishDB.
        """
   
        # Insert a number of rows of data in table table_name 
        try:
            command = "INSERT INTO %s VALUES (?%s)" % (table_name,54*",?")
            self.dbCursor.executemany(command, rows)
            # self.dbCursor.executemany("INSERT INTO table_name VALUES (?%s)" % (54*",?"), rows)
        except sqlite3.IntegrityError:
            print('Error: An Idea UID in the table already exists. Insertion ignored.')
            
        # Save (commit) the additions
        self.dbConnect.commit()
#------------------------------------------------ -------------
    def SearchRowsInTable(self, table_name, criteria):
        """Search for rows in databaseName where criteria
        specifies a list of triples (colName,' and ' or ' or ',value) for matching.
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
        #for row in dbConnect.execute('select * from table_name where lhName=? and rhName=?',(values)):
        #for row in dbConnect.execute(query,(values)):
        #    resultTable.append(row)
        self.dbCursor.execute(query,(values))
        resultTable = self.dbCursor.fetchall()
        return(resultTable)
#------------------------------------------------ -------------
    def IncludeFiles_in_DB(self, DB_name, language):
        """Import one or more Gellish files into the ontology,
        without consistency verification.
        """
        self.readFiles = []
        self.messagesM = []
        
        # Select files to be imported
        modelFiles = filedialog.askopenfilenames(filetypes=(("CSV files","*.csv"),\
                                                            ("All files","*.*")), title="Select file")
        #print('Selected file(s):',modelFiles)
        if modelFiles == '':
            if language.GUI_index == 1:
                self.messagesM.insert('end','\nDe file naam is blanco of het inlezen is gecancelled. Er is geen file ingelezen.')
            else:
                self.messagesM.insert('end','\nThe file name is blank or the inclusion is cancelled. There is no file read.')
            return

        # Read Information Model(s) from file(s)
        fileType = 'csv'
        readMess = ['Read file:','Lees file:   ']
        for modelFile in modelFiles:
            #self.messagesM.insert('end','\n%s %s' % (readMess[language.GUI_index], modelFile))
            self.Import_from_CSV(modelFile, DB_name, language)
            self.readFiles.append(modelFile)
            #if language.GUI_index == 1:
            #    self.messagesM.insert('end','\nGelezen file: %s is toegevoegd aan lijst van gelezen files.\n' % (modelFile))
            #else:
            #    self.messagesM.insert('end','\nRead file: %s is added to list of read files.' % (modelFile))

    def Import_from_CSV(self, fname, DB_name, language):
        """
        Read a file in a Gellish Expression Format.
        Rearrange the expressions and store rows in an expressions table.
        and store the names_in_context in a naming_table.
        """
        try:
            f = open(fname, "r")
        except IOError:
            print("File '%s' does not exist or is not readable." % fname)
            sys.exit()
        
        # determine dialect
        sample = f.read(1024)
        dialect = csv.Sniffer().sniff(sample)
        
        # rewind to start
        f.seek(0)
        
        # initialise csv reading
        reader = csv.reader(f, dialect)
        
        # skip first line
        next(reader)
        
        # read line with field codes and convert them to integers
        sourceIDs = list(map(int, next(reader)))

        destIDs = []
        # For available data columnIDs in reader find the destination columnID
        for ID in sourceIDs:
            if ID in Ex.expIDs:
                destIDs.append(Ex.expIDs.index(ID))
            else:
                print('\n Column ID %i is invalid. Column is ignored.' % (ID))
                destIDs.append(0)
        print('DestIDs: ',destIDs)

        # skip third line
        next(reader)

        tableName = "expressions"
        #self.dbConnect = sqlite3.connect("%s.db3"% DB_name)
        #self.dbCursor  = self.dbConnect.cursor()
        
        # Data starts at 4th line
        for in_row in reader:
            # load default values in row
            db_row = Ex.default_row[:]
            # put input fields in destination fields on row
            for ID in destIDs:
                db_row[ID] = in_row[destIDs.index(ID)]
            if db_row[Ex.status_col] == "default":
                Ex.default_row = db_row[:]
                continue

            # If phrase_type == 0 (unknown) then determine the phrase type,
            # being either 6066 for a base phrase or 1986 for an iverese phrase.
            # In case of the basic ontology, where only bootstrapping relations may be present,
            # the base_phrases are the collection of collection of bootstrapping phrases: baseBootPhrases
            # and inverse_phrases are the initial InverseBootPhrases.
            if db_row[Ex.phrase_type_uid_col] == 0:
                if db_row[Ex.rel_type_name_col] in language.base_phrases:
                    db_row[Ex.phrase_type_uid_col] = 6066
                elif db_row[Ex.rel_type_name_col] in language.inverse_phrases:
                    db_row[Ex.phrase_type_uid_col] = 1986
                else:
                    print("Phrase ", db_row[Ex.rel_type_name_col], " not yet defined; expression ignored")
                    continue

            #print('db_row: ',db_row)
            self.InsertRowInTable(tableName, db_row)

#-------------------------------------------------------------
if __name__ == "__main__":
    formal_language = "English"
    Gellish = FormalLanguage(formal_language)
    GUI_language    = "English"
    GUI = Gellish.GUILanguage(GUI_language)

    #DB_name = ':memory:'
    DB_name = 'FormalEnglishDB'
    FEDB = Database(DB_name)     # create Formal English Database
    FEDB.IncludeFiles_in_DB(DB_name, Gellish)

    expr_table_name = 'expressions'
    # Insert rows of expressions in expressions table
    # print(Rows.expr[0])
    #import Data.TestDBcontent as Rows
    #FEDB.InsertRowInTable (expr_table_name, Rows.expr[0])
    #FEDB.InsertRowsInTable(expr_table_name, Rows.expr[1:])

    # search for matching rows
    criteria = [('lhName', ' and ', "specialization relation between kinds of things")] #,('status',' and ', "accepted")]
    resultTable = FEDB.SearchRowsInTable(expr_table_name, criteria)
    for row in resultTable[0:10]:
        print('result-1: ',row[10],row[18],row[24])
    #FED.dbConnect.close()

    # read whole expressions table
    FEDB.dbCursor.execute('select * from expressions')
    result = FEDB.dbCursor.fetchall()
    for row in result[0:10]:
        print('result-2: ',row[10],row[18],row[24])

