import sqlite3
import os
import sys
import csv
from Expr_Table_Def import *
from tkinter import filedialog
from Bootstrapping import *
from GellishDict import GellishDict
from SemanticNetwork import Semantic_Network

class Database:
    """ Initialize a new database (:in memory: or on external memory)
        with two kinds of tables:
          expression tables including various tables for expressions,
          and a naming table for a dictionary with names_in_contexts and UIDs.
        Read CSV files and load them into the various tables.
    """
    def __init__(self, db_name):
        """ Create a database with two kinds of tables.
        """
        self.base_lang     = 'English'
        self.lang_dict     = {910036: "English", 910037: "Dutch"}
        self.comm_dict     = {492015: "Formal English", 492016: "Formeel Nederlands"}
        self.rel_types     = []
        self.rel_type_uids = base_rel_type_uids
        self.idea_uids     = []
        self.base_phrases  = boot_base_phrasesEN      + boot_base_phrasesNL
        self.inverse_phrases = boot_inverse_phrasesEN + boot_inverse_phrasesNL
        self.read_files    = []
        self.dictionary    = GellishDict()
        self.base = True
        
        # if db_name == ":memory:" then the database is created in internal RAM memory.
        self.name = db_name
##        self.Connect_to_database(db_name)
##
##    def Connect_to_database(self, db_name):
        if db_name == ":memory:":
            self.dbConnect = sqlite3.connect(db_name)
        else:
            self.dbConnect = sqlite3.connect("%s.db3"% db_name)
        self.dbCursor  = self.dbConnect.cursor()

    def CreateTables(self):
        """ Call the creation method for a number of tables
            with Gellish expressions and a naming table.
        """
        table_names = ["base_ontology", "domain_dictionaries", "productsANDprocesses", "namingTable"]
        # "knowledge", "requirements"
        for table_name in table_names:
            table = self.CreateTable(table_name)
            print("  Database '%s' table '%s' created." % (self.name, table_name))

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
        self.dbCursor.execute(command)                    
        self.dbConnect.commit()
#-------------------------------------------------------------
    def InsertRowInTable(self, table_name, row):
        """Insert one row in table_name into GellishDB'."""
        
        # Insert row of data in table table_name   
        try:
            command = "INSERT OR REPLACE INTO %s VALUES (?%s)" % (table_name,54*",?")
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
            command = "INSERT OR REPLACE INTO %s VALUES (?%s)" % (table_name,54*",?")
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
    def Import_Files_in_DB(self, GUI):
        """Select one or more Gellish files in dialog and import files into the database tables,
        after syntactic verification, but without consistency verification.
        If file == base ontology, then build (base)ontology
        """
        # Select one or more files to be imported
        modelFiles = filedialog.askopenfilenames(filetypes=(("CSV files","*.csv"),\
                                                            ("All files","*.*")), title="Select file")
        #print('Selected file(s):',modelFiles)
        if modelFiles == '':
            GUI.Message(
                '\nThe file name is blank or the inclusion is cancelled. There is no file read.',\
                '\nDe file naam is blanco of het inlezen is gecancelled. Er is geen file ingelezen.')
            return

        # Read Information Model(s) from file(s)
        fileType = 'csv'
        for modelFile in modelFiles:
            GUI.Message('\nReading file: %s' % (modelFile),\
                        '\nLees file   : %s' % (modelFile))
            self.Import_from_CSV(modelFile, GUI)
            self.read_files.append(modelFile)
            GUI.Message('\nRead file   : %s is added to list of read files.'              % (modelFile),\
                        '\nGelezen file: %s is toegevoegd aan lijst van gelezen files.\n' % (modelFile))

            if self.base == True:
                self.Build_Base_Semantic_Network()
                self.base = False

    def Import_Base_Ontology(self, GUI):
        ''' Read basic ontology CSV file and import content in base_ontology table.
            base_onto_path is specified in boothtrapping module.
        '''
        onto_file_path = []
        dirs = dict_dirs[:]
        for dir in dirs:
            onto_file_path.append(dir)
        onto_file_path.append(base_onto_file)
        #print('Ontology file:', onto_file_path)
        onto_path = os.path.join(*onto_file_path)
        fill = self.Import_from_CSV(onto_path, GUI)
        print('Imported: base ontology')

##    def Import_Domain_Dictionaries(self, GUI):
##        ''' Read domain dictionary CSV file(s) and import content in domain_dictionaries table.'''
##        # Create list of file paths for domain dictionaries
##        dict_files_paths = []
##        for file in dict_files:
##            dict_file_path = []
##            dirs = dict_dirs[:]
##            for dir in dirs:
##                dict_file_path.append(dir)
##            dict_file_path.append(file)
##            print('Dict file:', dict_file_path)
##            dict_files_paths.append(dict_file_path)
##        
##        dictionary_files = []
##        for file_path in dict_files_paths:
##            #print('file_path: ', file_path)
##            f_path = os.path.join(*file_path)
##            dictionary_files.append(f_path)
##
##        # Read taxonomic dictionary files and import their content in domain_dictionaries table
##        for file in dictionary_files:
##            fill = self.Import_from_CSV(file, GUI)
##            print('Imported: domain dictionary:', file)

    def Import_Model_Files(self, model_files, model_dirs, GUI): # model_path
        ''' Read models in CSV file(s) and import content in database table.'''
        # Create list of file paths
        #print('Files:', model_files, model_dirs)
        model_files_paths = []
        for file in model_files:
            model_file_path = []
            dirs = model_dirs[:]
            for dir in dirs:
                model_file_path.append(dir)
            model_file_path.append(file)
            model_files_paths.append(model_file_path)
        #print('Model files: ', model_files_paths)
        # Read CSV files and import content in database table.
        mod_files = []
        for file_path in model_files_paths:
            m_path = os.path.join(*file_path)
            mod_files.append(m_path)

        # Read model files and import their content in applicable table(s)
        for file in mod_files:
            fill = self.Import_from_CSV(file, GUI)
            print('Imported file:', file)

    # Add and/or modify database content
        # *** TO BE DONE ***
        #elif action == 'e':
    
    def Build_Base_Semantic_Network(self):
        # Build Semantic Network from database table,
        # primarily to add defined kinds of relations to list(rel_type_uids)
        base_net = Semantic_Network('base network')
        table = 'base_ontology'
        base_net.Add_table_content_to_network(self.dbCursor, table)
        print('Base network: %s; nr of objects = %i; nr of rels = %i; nr of rel_types = %i' % \
          (base_net.name, len(base_net.objects), len(base_net.rels), len(base_net.rel_types)))
        base_net.rel_types = base_net.DetermineSubtypeList(5935)
        for rel in base_net.rel_types:
            base_net.rel_type_uids.append(rel.uid)
        #print('Network rel_type_uids: ', base_network.rel_type_uids)
        return base_net

    def Import_from_CSV(self, fname, GUI):
        """
        Read file fname in a Gellish Expression Format.
        Rearrange the expressions,
        Verify the quality and
        if correct then store rows in an expressions table in database db_name
        """
        try:
            #fname = 'Formal English base ontology.csv'
            f = open(fname, "r")
        except IOError:
            GUI.Message("File '%s' does not exist or is not readable." % (fname), \
                        "File '%s' bestaat niet of is niet leesbaar."  % (fname))
            sys.exit()
        
##        # determine dialect
##        sample = f.read(2048)
##        dialect = csv.Sniffer().sniff(sample, delimiters=';')
##        
##        # rewind to start
##        f.seek(0)
##        
        # initialise csv reading
##        reader = csv.reader(f, dialect)
        reader = csv.reader(f, delimiter=';')
        model_lang_ind = 0 # 'English'
        
        # Read first line
        header = next(reader)
        if header[0] != "Gellish":
            GUI.Message("First field in file %s not 'Gellish', file skipped.", \
                        "Eerste veld in file %s niet 'Gellish', file overgeslagen.")
        file_type = header[5]
        self.base_ontology = False
        if file_type in ['Base ontology', 'Base Ontology', 'basisontologie', 'Basisontologie']:
            self.base_ontology = True
            table_name = "base_ontology"
        elif file_type in ['Domain dictionary', 'Domain Dictionary', 'Domeinwoordenboek', 'Woordenboek']:
            table_name = "domain_dictionaries"
        elif file_type in ['Product models', 'Process models', 'Product and process models', \
                           'Productmodellen','Procesmodellen', 'Product- en procesmodellen']:
            table_name = "productsANDprocesses"
        else:
            # "knowledge", "requirements"
            print('Error: file type %s unknown. File %s ignored' % (file_type, header[6]))
            return
        print('\nImporting file "%s" in table %s.' % (header[6], table_name))

        # Read in which language the textual fields (e.g. definitions) are expressed.
        self.base_lang  = header[1]
        if self.base_lang == 'Nederlands':
            self.model_lang_ind = 1
        else:
            self.model_lang_ind = 0
##        if self.base_ontology == True:
##            self.base_phrases    = boot_base_phrasesNL    + boot_base_phrasesEN
##            self.inverse_phrases = boot_inverse_phrasesNL + boot_inverse_phrasesEN
##            if self.base_ontology == True:
##                self.base_phrases    = base_boot_phrasesEN
##                self.inverse_phrases = inverse_boot_phrasesEN
        
        # Read line with field codes and convert them to integers
        sourceIDs = list(map(int, next(reader)))

        # check if idea_uid is present
        if 1 not in sourceIDs or 8 not in sourceIDs:
            print('Error: Idea UID column or status column is missing. File not read.')
            return
        idea_col_in   = sourceIDs.index(1) # the column where idea_uid is located (for error messageing)
        status_col_in = sourceIDs.index(8)

        dest_ids = []
        # For available data columnIDs in reader find the destination columnID
        for ID in sourceIDs:
            if ID in expr_col_ids:
                dest_ids.append(expr_col_ids.index(ID))
            else:
                print('  Column ID %i is invalid. Column is ignored.' % (ID))
                dest_ids.append(0)
        #print('Dest_ids: ',dest_ids)

        # skip third line
        next(reader)
        
        # Read line 4 etc. where data starts
        loc_default_row = default_row[:]
        idea_uid = 0
        db_row   = []
        db_rows  = []
        
        for in_row in reader:
            # skip empty rows
            if in_row == []:
                #print('Empty row following idea %i skipped.', idea_uid)
                continue
            # skip rows with status 'ignore' or equivalent
            if in_row[status_col_in] in ignores:
                #print('Expression with status = "ignore etc." following idea %i skipped.', idea_uid)
                continue
            
            # rearrange the values in in_row in the sequence of the database
            # and add defaults for missing values
            db_row = self.Rearrange_input_row(idea_col_in, in_row, dest_ids, loc_default_row)

            # save idea_uid for later reference to the preceeding row.
            idea_uid = db_row[idea_uid_col]
            
            # if row in input file contains default values for the file, then copy them to local defaults
            if db_row[status_col] == "default":
                loc_default_row = db_row[:]
                continue

            # Verify uniqueness of idea_uid
            if idea_uid not in self.idea_uids:
                self.idea_uids.append(idea_uid)
            else:
                print('Error: Duplicate idea UID %i. Latter idea ignored.' % (idea_uid))
                continue

            # verify input row values, amend where applicable
            correct, db_row = self.Verify_row(db_row)
            
            if correct:
                #self.InsertRowInTable(table_name, db_row) # replaced by batchwise insert (see below)
                db_rows.append(db_row)
            else:
                print('Error in expression of idea ', idea_uid, 'row ignored.')
                pass

            if len(db_rows) > 999:
                self.InsertRowsInTable(table_name, db_rows)
                #print('Insert1:', len(db_rows), table_name, self.name)
                db_rows = []
                
        if len(db_rows) > 0:
            #print('Insert2:', len(db_rows), table_name, self.name)
            self.InsertRowsInTable(table_name, db_rows)

    def Rearrange_input_row(self, idea_col_in, in_row, dest_ids, loc_default_row):
        '''Rearrange values in in_row into db_row conform the column ids specified in dest_ids.
        Missing values are loaded with default values, possibly from an in_row with default values.
        '''
        # load default values in row
        db_row = loc_default_row[:]
        # put input fields in destination fields on row
        for ID in dest_ids:
            # if inputfield in list then convert to integer
            if ID in int_col_ids:
                if in_row[dest_ids.index(ID)] == '':
                    db_row[ID] = 0
                    # Index for UID of UoM, successorUID, appContUID and collUID are optional
                    if ID not in [27, 36, 13, 49]:
                        print('Idea %s UID in column %i is missing' % (in_row[idea_col_in], expr_col_ids[ID]))
                else:
                    db_row[ID] = int(in_row[dest_ids.index(ID)])
            else:
                db_row[ID] = in_row[dest_ids.index(ID)]
        return db_row

    def Verify_row(self, db_row):
        ''' Verify values in db_row before loading in database and amend where applicable
        '''
        correct = True

        # collect used languages for naming left hand objects and verify consistency of language names.
        lang_uid = int(db_row[lang_uid_col])
        if lang_uid not in self.lang_dict:
           self.lang_dict[lang_uid] = db_row[lang_name_col]
        elif db_row[lang_name_col] != self.lang_dict[lang_uid]:
            print('Warning: Language name %s does not correspond to earlier name %s for UID %i.' %\
                  (db_row[lang_name_col], self.lang_dict[lang_uid], lang_uid))

        # collect language communities for naming left hand objects and verify consistency of community names.
        comm_uid = int(db_row[comm_uid_col])
        if comm_uid not in self.comm_dict:
           self.comm_dict[comm_uid] = db_row[comm_name_col]
        elif db_row[comm_name_col] != self.comm_dict[comm_uid]:
            print('Community name %s does not correspond to earlier name %s for UID %i.' %\
                  (db_row[comm_name_col], self.comm_dict[comm_uid], comm_uid))
                    
        # Verify whether the relation type UID is defined in the current language definition:
        if int(db_row[rel_type_uid_col]) not in self.rel_type_uids:
            print("Error: Relation type (%i) %s is not (yet) defined as a binary relation. Idea %i ignored." % \
                  (int(db_row[rel_type_uid_col]), db_row[rel_type_name_col], db_row[idea_uid_col]))
            #print(self.rel_type_uids)
            correct = False

        # Collect base_phrases and inverse_phrases
        elif int(db_row[rel_type_uid_col]) == 6066:
            self.base_phrases.append(db_row[lh_name_col])
        elif int(db_row[rel_type_uid_col]) == 1986:
            self.inverse_phrases.append(db_row[lh_name_col])
        
        # If phrase_type == 0 (unknown) then determine the phrase type;
        # base_phrase_type_uid = 6066 inverse_phrase_type_uid = 1986.
        # In case of the basic ontology, where only bootstrapping relations may be present,
        # the base_phrases are the collection of collection of bootstrapping phrases: baseBootPhrases
        # and inverse_phrases are the initial InverseBootPhrases.
        elif int(db_row[phrase_type_uid_col]) == 0:
            if db_row[rel_type_name_col] in self.base_phrases:
                db_row[phrase_type_uid_col] = 6066
            elif db_row[rel_type_name_col] in self.inverse_phrases:
                db_row[phrase_type_uid_col] = 1986
            else:
                print("Error: Phrase <%s> not yet defined. Idea %i ignored" % \
                      (db_row[rel_type_name_col, db_row.idea_uid_col]))
                correct = False

        # if lh and rh kinds of roles are missing, load them with defaults
        if correct and int(db_row[rel_type_uid_col]) == 1146:
                if int(db_row[lh_role_uid_col])  == 0:  db_row[lh_role_uid_col]  = subtypeRoleUID
                if db_row[lh_role_name_col] == "": db_row[lh_role_name_col] = subtypeName[self.model_lang_ind]
                if int(db_row[rh_role_uid_col])  == 0:  db_row[rh_role_uid_col]  = supertypeRoleUID
                if db_row[rh_role_name_col] == "": db_row[rh_role_name_col] = supertypeName[self.model_lang_ind]
        return correct, db_row
#-------------------------------------------------------------
if __name__ == "__main__":
    from Anything import GUI_Language
    # Test creation of new database and loading with data
    # Choose GUI language
    GUI_language    = "English"
    GUI = GUI_Language(GUI_language)

    # Create a new database external or in-memory with a number of tables.
    #db_name = ':memory:'
    db_name = 'FormalEnglishDB'
    #db_name = 'RoadDB'
    new = input("Enter new (n) or existing (e):")
    if new == "n":
        try:
            os.remove(db_name + ".db3")
        except OSError:
            pass
    Gel_db = Database(db_name)     # create or connect to Formal English Database
    if new == "n":
        print("Database: %s created." % (Gel_db.name))
        Gel_db.CreateTables()
    else:
        print("Database: %s connected." % (Gel_db.name))

    # Include one or more files in the various tables
    Gel_db.Import_Files_in_DB(GUI)
    addition = 'y'
    while addition == 'y':
        addition = input("More import files? (y/n):")
        if addition == 'y':
            Gel_db.Import_Files_in_DB(GUI)
            

    # Test searching in table "base_ontology"
    expr_table_name = "base_ontology"
    # search for matching rows
    criteria = [('lhName', ' and ', "specialization relation between kinds of things")] #,('status',' and ', "accepted")]
    resultTable = Gel_db.SearchRowsInTable(expr_table_name, criteria)
    for row in resultTable[0:4]:
        print('result-1: ',row[10],row[18],row[24])
    #Gel_db.dbConnect.close()

    # read whole "base_ontology" table
    Gel_db.dbCursor.execute('select * from base_ontology')
    result = Gel_db.dbCursor.fetchall()
    for row in result[0:4]:
        print('result-2: ',row[10],row[18],row[24])

    # Test searching in table "domain_dictionaries"
    expr_table_name = "domain_dictionaries"
    # search for matching rows
    criteria = [('lhName', ' and ', "m")] #,('status',' and ', "accepted")]
    resultTable = Gel_db.SearchRowsInTable(expr_table_name, criteria)
    for row in resultTable:
        print('result-1: ',row[10],row[18],row[24])
