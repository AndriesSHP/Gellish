from tkinter import filedialog
import os
import sys
import csv
import json
from Bootstrapping import *
from Expr_Table_Def import *
from DatabaseAPI import Database
from Create_output_file import *
from Mapping_tables_IB import *
from Anything import Anything

class Gellish_file:
    """ Data about files. """
    def __init__(self, path_and_name, Gel_net):
        # The file file_name is without path or directory, but with file extension
        self.path_and_name = path_and_name
        self.Gel_net = Gel_net
        parts = path_and_name.rsplit('\\', maxsplit=1)
        if len(parts) == 1:
            parts2 = path_and_name.rsplit('/', maxsplit=1)
            if len(parts2) == 1:
                Message(Gel_net.GUI_lang_index, \
                        '\nFile name {} has no directory.'.format(path_and_name),\
                        '\nFilenaam {} heeft geen directory.'.format(path_and_name))
                self.name = parts2[0]
            else:
                self.name = parts2[1]
        else:
            self.name = parts[1]

        # Determine the file extension from path_and_name
        name_ext = self.path_and_name.rsplit('.', maxsplit=1)
        if len(name_ext) == 1:
            Message(Gel_net.GUI_lang_index, \
                    '\nFile name {} has no file extension.'.format(path_and_name),\
                    '\nFilenaam {} heeft geen file extensie.'.format(path_and_name))
            self.extension = '' 
            return
        elif name_ext[1] not in ['csv', 'json']:
            Message(Gel_net.GUI_lang_index, \
                    '\nFile name extension {} is not (yet) supported.'.format(name_ext[1]),\
                    '\nFilenaam extensie {} wordt (nog) niet ondersteund.'.format(name_ext[1]))
            self.extension = ''
        else:
            # Allocate file extension to file
            self.extension = name_ext[1]
#-------------------------------------------------------------
class Expression_list:
    '''Create a list of expressions in full Gellish Expression Format
       from any of various sources (such as CSV files),
       build a semantic network from it
       or export such a list in any of various formats (such as CSV or JSON files).
    '''
    def __init__(self, Gel_net):
        self.Gel_net = Gel_net
        self.expressions = []
        self.files_read  = []
        self.interpreted_lines = []

    def Build_new_network(self, Gel_net): #, Gel_db):
        ''' Build network from files as specified in Bootstrapping.py:
            First read a base ontology from a file 
            Then read UoMs and other dictionary files, knowledge files and model files
        '''
        self.Import_Base_Ontology(Gel_net) #, Gel_db)
        #Gel_net.Create_base_reltype_objects()
        Gel_net.Build_Base_Semantic_Network() #Gel_db.db_cursor) # incl. collecting rel_type_uids for validation
        
        # Import domain dictionaries in db from files (specified in Bootstrapping)
        self.Import_Model_Files(dict_file_names, dict_dirs, Gel_net) #, Gel_db)
        
        # Import product and process models in db from files (specified in Bootstrapping)
        # and extend the network with domain dictionaries and product models (if any)
        if len(prod_file_names) > 0:
            self.Import_Model_Files(prod_file_names, prod_dirs, Gel_net) #, Gel_db)
##        Gel_net.Extent_Semantic_Network() #Gel_db.db_cursor)

        Gel_net.Verify_network()

    def Import_Base_Ontology(self, Gel_net): #, Gel_db):
        ''' Read a base ontology CSV file and
            import its content in the base_ontology table of the database.
            The base_onto_path is specified in the bootstrapping module.
        '''
        # Build file path_and_name from list of dirs and file name in bootstrapping module
        onto_file_path = []
        dirs = dict_dirs[:]
        for dir in dirs:
            onto_file_path.append(dir)
        onto_file_path.append(base_onto_file_name)
        onto_path = os.path.join(*onto_file_path)
        #print('Ontology path:', onto_path)
        
        # Create file object
        file = Gellish_file(onto_path, Gel_net)
        
        self.Import_Gellish_from_file(file, Gel_net) #, Gel_db)
        #print('Imported: base ontology')

    def Import_Model_Files(self, file_names, model_dirs, Gel_net): #, Gel_db): # model_path
        ''' Read models in CSV file(s) as specified in the bootstrapping module
            and import their content in the appropriate database table.
        '''
        # Create list of files with their paths, names and extensions
        model_files = []
        #model_file_names_paths = []
        for file_name in file_names:
            
            # Build path and name from list of dirs and name
            path_and_name = []
            dirs = model_dirs[:]
            for dir in dirs:
                path_and_name.append(dir)
            path_and_name.append(file_name)
            model_path = os.path.join(*path_and_name)
            file = Gellish_file(model_path, Gel_net)
            #print('Model file: ', file.path_and_name)
            model_files.append(file)

        # Read model files and import their content in the applicable table(s)
        for file in model_files:
            self.Import_Gellish_from_file(file, Gel_net) #, Gel_db)

    def Read_verify_and_merge_files(self, Gel_net):
        # Read one or more files, verify their content
##        # and load them in the various tables in :memory: database
        # and combine them with the semantic network
##        if Gel_net.db_name != ":memory:":
##            self.Gel_db = Database(":memory:")   # create an in-memory database
##            self.Gel_db.Create_tables()          # create empty tables
##            self.db_cursor = self.Gel_db.db_cursor
##            #print("Database: %s created." % (self.Gel_db.name))
        self.Combine_Files_with_Network(Gel_net) #, self.Gel_db)
        addition = 'n'  # 'y' means option for importing more input files
        while addition == 'y':
            addition = input("More import files? (y/n):")
            if addition == 'y':
                self.Combine_Files_with_Network(Gel_net) #, self.Gel_db)

    def Combine_Files_with_Network(self, Gel_net): #, Gel_db):
        """Select one or more Gellish files in a dialog and import files into the database tables,
        after syntactic verification, but without consistency verification.
        """
        # Select one or more files to be imported
        file_path_names = filedialog.askopenfilenames(filetypes=[("CSV files","*.csv"),("JSON files","*.json"),\
                                                             ("All files","*.*")], title="Select file")
        #print('Selected file(s):',modelFiles)
        if file_path_names == '':
            Message(Gel_net.GUI_lang_index, \
                '\nThe file name is blank or the inclusion is cancelled. There is no file read.',\
                '\nDe file naam is blanco of het inlezen is gecancelled. Er is geen file ingelezen.')
            return

        # Read file(s)
        for file_path_and_name in file_path_names:
            # Split file_path_and_name in file path and file name
            path_name = file_path_and_name.rsplit('/', maxsplit=1)
            if len(path_name) == 2:
                Message(Gel_net.GUI_lang_index, \
                        '\nReading file <{}> from directory {}.'.format(path_name[1], path_name[0]),\
                        '\nLees file <{}> van directory {}.'.format(path_name[1], path_name[0]))
                file_name = path_name[1]
                file_path = path_name[0]
            else:
                Message(Gel_net.GUI_lang_index, \
                        '\nReading file <{}> from current directory.'.format(file_path_and_name),\
                        '\nLees file <{}> van actuele directory.'.format(file_path_and_name))
                file_name = file_path_and_name
                file_path = ''
                
            # Create file object
            file = Gellish_file(file_path_and_name, Gel_net)

            # Import expressions from file
            self.Import_Gellish_from_file(file, Gel_net) #, Gel_db)
            self.files_read.append(file)
                
##            Message(Gel_net.GUI_lang_index, \
##                    '\nRead file   : %s is added to list of read files.'              % (file.path_and_name),\
##                    '\nGelezen file: %s is toegevoegd aan lijst van gelezen files.\n' % (file.path_and_name))

    def Import_Gellish_from_file(self, file, Gel_net): #, Gel_db):
        """ Read file file_name in a Gellish Expression Format.
        Rearrange the expressions,
        Verify the quality and
        if correct then store rows in an expressions table in database db_name
        """
        print('=== Read file {}'.format(file.path_and_name))
        try:
            f = open(file.path_and_name, "r", encoding="utf-8")
        except IOError:
            Message(Gel_net.GUI_lang_index, \
                    "File '%s' does not exist or is not readable." % (file.name), \
                    "File '%s' bestaat niet of is niet leesbaar."  % (file.name))
            sys.exit()

        # Determine the file extension
        if file.extension == 'csv':
    ##        # determine dialect
    ##        sample = f.read(4096)
    ##        dialect = csv.Sniffer().sniff(sample, delimiters=';')
    ##        
    ##        # rewind to start
    ##        f.seek(0)
    ##        
            # Initialise csv reading and read first line
    ##        self.reader = csv.reader(f, dialect)
            self.reader = csv.reader(f, delimiter=';')
            self.header = next(self.reader)
        elif file.extension == 'json':
            self.json_dict = json.load(f)
            
            # Determine JSON file type: list or dict?
            # Convert dict to list
            #print('JSON File type', type(self.json_dict))
            self.json_list = list(self.json_dict.items())
            self.header = self.json_list[0]
        else:
            print('File extension {} is not supported.'.format(file.extension))
            return
        
        # Read first line and determine whether it is a Gellish file or not
        #print('Header line:', self.header)
        if self.header[0] != "Gellish":
            Message(Gel_net.GUI_lang_index, \
                    "File {} is not in Gellish expression format, \
bacause the first field has not as content 'Gellish'.".format(file.name), \
                    "File {} is niet in Gellish expressie formaat, \
want het eerste veld heeft niet als inhoud 'Gellish'.".format(file.name))
            if file.extension == 'json':
                self.Interpret_non_gellish_JSON_file()
        else:
            self.Import_expressions_from_Gellish_file(file, Gel_net) #, Gel_db)

    def Interpret_non_gellish_JSON_file(self):
        ''' Read a non-Gellish JSON file and convert it into a Gellish file
        '''
        #print('JSON file: {}'.format(self.json_list))
        
        quantification = [('5737', 'has by definition on scale a value equal to', '6066'),\
                          ('5737', 'heeft per definitie op schaal een waarde gelijk aan', '6066')]

        new_article = True
        self.object_uid = 100
        self.idea_uid   = 200
        self.gel_expressions = []
        values = []
        of_text = [' of ', ' van ']
        lang_index = 1  # Nederlands (as Gellish output file language)
        lang_comm = ['910037', 'Nederlands', '2700929', 'IB']
        while new_article:
            #list_of_keys = list(self.json_dict.keys())
            # Find article name as value of a first level key
            for key_map in keys_map:
                if key_map[0] in self.json_dict:    #was list_of_keys:
                    if key_map[1] == '970047':
                        article_identifier = self.json_dict[keys_map[0][0]]
                        self.object_uid += + 1
                        article_uid = str(self.object_uid)
                        #print('Article id:', article_identifier)
                    elif key_map[1] == '5605':
                        article_name = self.json_dict[keys_map[1][0]]
                        #print('Article name:', article_name)
                        
                    elif key_map[1] == '493676':
                        # Find attributes_map and determine list of attributes ('properties') as value of a first level key
                        attribute_dict = self.json_dict[key_map[0]]
                        #print('Attribute type:', type(attribute_dict))
                        #print('Attribute:', attribute_dict)
                        list_of_attrib = list(attribute_dict.keys())
                    
                        # For each attribute find sub_attr_dict and its list of sub_attrib
                        for attrib_map in attributes_map:                  # e.g. soort object, hoogte, breedte
                            if attrib_map[0] in list_of_attrib:            # e.g. ibProductsoort, breedteMm, hoogteMm
                                #print('attrib_map[0]', attrib_map[0])
                                sub_attrib_dict = attribute_dict[attrib_map[0]] # e.g. label, name, value, unit
                                # Determine list of values
                                del values[:]
                                for sub in value_key_map:
                                    if sub[0] in sub_attrib_dict:
                                        val = sub_attrib_dict[sub[0]]    # e.g. 
                                    else:
                                        val = ''
                                    values.append(val)
                                #print('Values:', values)    # label, name, value, unit
                                
                                # For each type of attrib_map (kind of relation), depending on attribute (attrib_map[0]),
                                # create Gellish expression(s)
                                # e.g. ibProductsoort indicates: <is a model of> 730066, 'soort object' or
                                #      breedteMn indicates: <# has by definition as aspect a> 550464, 'breedte'
                                 
                                # If attrib_map indicates a <# is a model of> relation, then
                                if attrib_map[1][1] == '5396':
                                    self.idea_uid += +1
                                    lh_uid_name         = [article_uid, article_identifier]
                                    rel_uid_phrase_type = list(attrib_map[1][1:4])
                                    rh_role_uid_name    = ['', '']
                                    rh_uid_name         = list(values_map[values[2]]) # e.g. 43769 , 'dakvenster'
                                    uom_uid_name        = ['', '']
                                    description         = article_name
                                    intent_uid_name     = ['491285', 'bewering']
                                    gellish_expr = Create_gellish_expression(lang_comm, str(self.idea_uid), intent_uid_name,\
                                                                             lh_uid_name, rel_uid_phrase_type,\
                                                                             rh_role_uid_name, rh_uid_name, \
                                                                             uom_uid_name, description)
                                    #print('Gellish_expr1:', gellish_expr)
                                    self.gel_expressions.append(gellish_expr)
                                    
                                # If attrib_map indicates a <has by definition as aspect a> relation, then
                                # create two expressions: 1. for indicating the intrinsic aspect and the kind of aspect
                                #                         2. for quantification of the intrinsic aspect
                                elif attrib_map[1][1] == '5527':
                                    self.object_uid += + 1
                                    self.idea_uid   += +1
                                    lh_uid_name      = [article_uid, article_identifier]
                                    rel_uid_phrase_type = list(attrib_map[1][1:4])
                                    rh_uid_name      = list(attrib_map[1][4:6])    # e.g. 550464 , 'breedte'
                                    rh_role_uid_name = [str(self.object_uid), rh_uid_name[1] + of_text[lang_index] + article_identifier]
                                    uom_uid_name     = ['', '']
                                    description      = ''
                                    intent_uid_name = ['491285', 'bewering']
                                    gellish_expr = Create_gellish_expression(lang_comm, str(self.idea_uid), intent_uid_name,\
                                                                             lh_uid_name, rel_uid_phrase_type,\
                                                                             rh_role_uid_name, rh_uid_name, \
                                                                             uom_uid_name, description)
                                    #print('Gellish_expr2:', gellish_expr)
                                    self.gel_expressions.append(gellish_expr)
                                    
                                    # Create an expression for qualification or quantification of the aspect
                                    # If the value (values[2]) is a whole number then create a uid in the 2 billion range for it
                                    if values[2].isdecimal():
                                        value_uid = str(int(values[2]) + 2000000000)
                                        value_uid_name = [value_uid, values[2]]  # e.g. '2000000940', '940'
                                    else:
                                        # If value[2] includes a decimal comma, then replace the comma by a dot
                                        commas_replaced = values[2].replace(',', '.')
                                        dots_removed = commas_replaced.replace('.', '')
                                        # If the value without dots is numeric, then create a uid for a floating point number
                                        if dots_removed.isdecimal():
                                            self.object_uid += + 1
                                            value_uid_name = [str(self.object_uid), commas_replaced]
                                        else:
                                            # Value[2] is not numeric
                                            value_uid_name = values_map[values[2]] # e.g. '310024' , 'grenen'
                                    self.idea_uid += +1
                                    rh_role_uid_name_2 = ['', '']
                                    uom_uid_name = list(values_map[values[3]])
                                    description  = ''
                                    intent_uid_name = ['491285', 'bewering']
                                    gellish_expr = Create_gellish_expression(lang_comm, str(self.idea_uid), intent_uid_name,\
                                                                             rh_role_uid_name, quantification[lang_index],\
                                                                             rh_role_uid_name_2, value_uid_name, \
                                                                             uom_uid_name, description)
                                    #print('Gellish_expr3:', gellish_expr)
                                    self.gel_expressions.append(gellish_expr)
                new_article = False
            else:
                new_article = False
        subject_name = ['catalogue articles', 'catalogusartikelen']
        lang_name = 'Nederlands'
        serialization = 'csv'
        Open_output_file(self.gel_expressions, subject_name[lang_index], lang_name, serialization)

    def Import_expressions_from_Gellish_file(self, file, Gel_net): #, Gel_db):
        file.lang_ind = 0 # Default: 'English'
        
        # Initialize expressions table
        self.expressions = []
        self.interpreted_lines = []

        # Determine database table_name for storing expressions, based on file type (header[5])
        self.base_ontology = False
        if self.header[5] in ['Base ontology', 'Base Ontology', 'basisontologie', 'Basisontologie']:
            self.base_ontology = True
            table_name = "base_ontology"
            self.content_type = "dictionary"
        elif self.header[5] in ['domain dictionary', 'Domain dictionary', 'Domain Dictionary', \
                                'domeinwoordenboek', 'Domeinwoordenboek', 'Woordenboek']:
            table_name = "domain_dictionaries"
            self.content_type = "dictionary"
        elif self.header[5] in ['Product models', 'Process models', 'Product and process models', \
                           'Productmodellen','Procesmodellen', 'Product- en procesmodellen', \
                           'Productmodel', 'Product model', \
                           'Product type model', 'Producttypemodel', 'Producttypemodellen']:
            table_name = "productsANDprocesses"
            self.content_type = "product_model"
        elif self.header[5] in ['Query', 'Queries', 'Vraag', 'Vragen']:
            table_name = "none"
            self.content_type = "queries"
        elif self.header[5] in ['Mapping']:
            table_name = "none"
            self.content_type = "mapping"
        else:
            # "knowledge", "requirements"
            print("\n**Warning: File type '{}' is not standard. File with title '{}' processed".\
                  format(self.header[5], self.header[6]))
            table_name = "none"
            self.content_type = "unknown"
        #print('\nImporting file "%s" in table %s.' % (self.header[6], table_name))
        file.descr = self.header[6]

        # Read the language in which the textual fields (e.g. definitions) in the file generally are expressed.
        file.lang_name  = self.header[1]
        if file.lang_name == 'Nederlands':
            file.lang_ind = 1
            file.lang_uid = '910037'
            file.comm_uid = '492014'        # denotes 'Gellish'
            file.comm_name = "Gellish"      # default
        elif file.lang_name == 'English':
            file.lang_ind = 0
            file.lang_uid = '910036'
            file.comm_uid = '492014'
            file.comm_name = "Gellish"    # default
        else:
            print('Name of file language {} is unknown'.format(file.lang_name))
            return

        # Create language object if not yet existing
        if file.lang_uid not in Gel_net.lang_uid_dict:
            lang = Anything(file.lang_uid, file.lang_name)
            Gel_net.languages.append(lang)
            Gel_net.lang_uid_dict[file.lang_uid] = file.lang_name

        # Determine the UID ranges for new objects and relations in this file
        if len(self.header) > 10:
            Gel_net.unknown_obj_uid     = self.UID_range_limit(self.header[7] , 100)
            Gel_net.upper_obj_range_uid = self.UID_range_limit(self.header[8] , 499)
            Gel_net.unknown_rel_uid     = self.UID_range_limit(self.header[9] , 500)
            Gel_net.upper_rel_range_uid = self.UID_range_limit(self.header[10], 999)
            
            if Gel_net.upper_obj_range_uid <= Gel_net.unknown_obj_uid or\
               Gel_net.unknown_rel_uid     <= Gel_net.upper_obj_range_uid or\
               Gel_net.upper_rel_range_uid <= Gel_net.unknown_rel_uid :
                print('Object range UIDs not in proper position or sequence')
            print('Obj_range_UIDs: {}, {}; Rel_range_UIDs: {} {}'.\
                  format(Gel_net.unknown_obj_uid, Gel_net.upper_obj_range_uid, \
                         Gel_net.unknown_rel_uid, Gel_net.upper_rel_range_uid))
        else:
            Gel_net.unknown_obj_uid     = 100
            Gel_net.upper_obj_range_uid = 499
            Gel_net.unknown_rel_uid     = 500
            Gel_net.upper_rel_range_uid = 999
        
        # Read 2nd line ==== with field codes and convert them to integers
        row2 = next(self.reader)
        in_col = []
        for col_id in row2:
            if col_id == '':
                int_val = 0
            else:
                int_val, integer = Convert_numeric_to_integer(col_id)
                if integer == False:
                    print('Error: Value {} on row 2 is not a whole number. Column ignored'.format(int_val))
                    int_val = 0
            in_col.append(int(int_val))
        source_ids = list(map(int, in_col))

        # Check if idea_uid column is present
        if 1 not in source_ids:
            print('Warning: Idea UID column is missing. File not loaded in database.')
            idea_col_in = 0
        else:
            # the column nr where idea_uid is located (for error messageing)
            idea_col_in   = source_ids.index(1)

        # Check if status column is present
        if 8 not in source_ids:
            print('Warning: Status column is missing. File not loaded in database.')
            status_col_in = 0
        else:
            status_col_in = source_ids.index(8)

        lang_name_col_id  = {}
        lang_descr_col_id = {}
        # For all column source_ids in self.reader find the corresponding column in expr_col_ids
        # and store them in source_id_dict. 
        # Columns ids for names in other languages are not stored in destionarion ids but in lang_name_col_id
        # (those names will not be stored in destination tables for ideas (thus not in the sql_database)
        # but will be stored in the dictionary only)
        self.source_id_dict = {}
        #self.test = True
        #dest_ids = []
        for source_id in source_ids:
            if source_id in expr_col_ids:
                self.source_id_dict[source_id] = expr_col_ids.index(source_id)
                #dest_ids.append(expr_col_ids.index(source_id))
            else:
                self.source_id_dict[source_id] = 0
                #dest_ids.append(0)
                # If source_id indicates another language column or definition column,
                # and that language does not exist yet, then create a language object
                str_id = str(source_id)
                if source_id >= 910036 and source_id < 912000:
                    lang_name_col_id[source_id] = source_ids.index(source_id)
                    #print('Col nr of alt_name', lang_name_col_id[source_id])
                    
                    # If language uid not in uid_dict then create language object
                    if str_id not in Gel_net.uid_dict:
                        lang = Anything(str_id, Gel_net.lang_dict_EN[str_id])
                        lang.defined = False
                        Gel_net.objects.append(lang)
                        Gel_net.uid_dict[lang.uid] = lang.name
                        Gel_net.lang_uid_dict[lang.uid] = lang.name
                elif source_id >= 1910036 and source_id < 1912000:
                    lang_descr_col_id[source_id] = source_ids.index(source_id)
                else:
                    print('  Column ID {} is unknown. Column is ignored.'.format(source_id))
                    #lang_name_col_id[source_id] = 0    # source_ids.index(source_id)
        #print('Source_ids: ', source_ids)
        #print('Source_id_dict', self.source_id_dict)

        # Skip 3rd line ====
        next(self.reader)
        
        # Read line 4 etc. where data starts ====
        loc_default_row = default_row[:]
        idea_uid = 0
        db_row   = []
        db_rows  = []
        
        for in_row in self.reader:
            # skip empty rows
            if in_row == []:
                #print('Empty row following idea {} skipped.'.format(idea_uid))
                continue
            # Skip rows with status 'ignore' or equivalent
            if in_row[status_col_in] in ignores:
                #print('Expression with status = "ignore etc." following idea {} skipped.'.format(idea_uid))
                continue
            
            # Rearrange the values in in_row in the sequence of the database
            # and add defaults for missing values and remove commas (,) from uids
            db_row = self.Rearrange_input_row(idea_col_in, in_row, source_ids, loc_default_row)

            # Save idea_uid for later reference to the preceeding row.
            idea_uid = db_row[idea_uid_col]
            
            # If row in input file contains default values for the file, then copy them to local defaults
            if db_row[status_col] == "default" or db_row[status_col] == "defaults":
                loc_default_row = db_row[:]
                continue

            # Verify existence and uniqueness of idea_uid
            if idea_uid == '':
                Gel_net.unknown_rel_uid += 1
                if str(Gel_net.unknown_rel_uid) not in Gel_net.idea_uids and \
                   Gel_net.unknown_rel_uid <= Gel_net.upper_rel_range_uid:
                    idea_uid = str(Gel_net.unknown_rel_uid)
                    db_row[idea_uid_col] = idea_uid
                    Gel_net.idea_uids.append(idea_uid)
                    #print('Idea_uid {} added'.format(idea_uid))
                else:
                    print('UID {} already used in network'.format(Gel_net.unknown_rel_uid))
            elif idea_uid not in Gel_net.idea_uids:
                    Gel_net.idea_uids.append(idea_uid)
            else:
                print('Error: Duplicate idea UID {}. Latter idea ignored.'.format(idea_uid))
                continue

            # VERIFY input row values, amend where applicable
            correct, db_row = self.Verify_row(file, db_row, Gel_net)

            names_and_descriptions = []
            if correct:
                # If an additional language column is present
                # then append the dictionary with the terms available in the language column
                #print('Col_ids',lang_name_col_id)
                for col_id in lang_name_col_id:
                    # Only for rows with a specialization and alias relation
                    if (db_row[rel_type_uid_col] in Gel_net.specialRelUIDs or \
                        db_row[rel_type_uid_col] in Gel_net.alias_uids):
                        # Check whether column value (name of object) is not blank,
                        # then include name_in_context in the dictionary (if not yet present)
                        if in_row[lang_name_col_id[col_id]] != '':
                            if db_row[rel_type_uid_col] in Gel_net.alias_uids:
                                naming_uid = db_row[rel_type_uid_col]
                                
                                # Collect base_phrase or inverse_phrase of additional language column
                                if db_row[rel_type_uid_col] == '6066':
                                    Gel_net.base_phrases.append(in_row[lang_name_col_id[col_id]])
                                elif db_row[rel_type_uid_col] == '1986':
                                    Gel_net.inverse_phrases.append(in_row[lang_name_col_id[col_id]])
                            else:
                                naming_uid = '5117'
                            # Note: col_id is integer, whereas lang_uid should be a string
                            name_in_context = (str(col_id), db_row[comm_uid_col], in_row[lang_name_col_id[col_id]])
                            
                            # Check whether a description column is present
                            key_descr = col_id + 1000000
                            if key_descr in lang_descr_col_id:
                                lang_descr = in_row[lang_descr_col_id[key_descr]]
                            else:
                                lang_descr = ''
                                
                            if name_in_context not in Gel_net.dictionary:
                                value_triple = (db_row[lh_uid_col], naming_uid, lang_descr)
                                Gel_net.dictionary[name_in_context] = value_triple
                                name_and_descr = [str(col_id), db_row[comm_uid_col],\
                                                  in_row[lang_name_col_id[col_id]], naming_uid, lang_descr]
                                names_and_descriptions.append(name_and_descr)
                                #print('Name and descr', name_and_descr)
                
                # Add file name to expression
                db_row[file_name_col] = file.name
##                # Collect rows for insertion in database
##                db_rows.append(db_row)
            else:
                #print('    == Error in expression of idea ', idea_uid) #, 'row ignored.')
                pass

            # Add expressions to the semantic network, except for queries
            if self.content_type != 'queries':
                Gel_net.Add_row_to_network(db_row, names_and_descriptions)
                names_and_descriptions.clear()
##            # Add non-language defining expressions to the language defining semantic network from DB
##            if self.content_type in ['mapping', 'product_model', 'unknown']:
##                Gel_net.Add_row_to_network(db_row, names_and_descriptions)
##
##            # Store batch of 2000 db_rows in database table provided that idea uids are present 
##            if len(db_rows) > 2000 and table_name != 'none':
##                if idea_col_in > 0:
##                    Gel_db.InsertRowsInTable(table_name, db_rows)
##                #print('Insert1:', len(db_rows), table_name, self.name)
##                db_rows = []
##                
##        if len(db_rows) > 0 and table_name != 'none':
##            #print('Insert2:', len(db_rows), table_name, self.name)
##            # If idea uids present, then store remaining batch of db_rows in database table
##            if idea_col_in > 0:
##                Gel_db.InsertRowsInTable(table_name, db_rows)

        #if self.content_type in ['mapping', 'product_model', 'unknown']:
##        Gel_net.Verify_rh_objects()

        print('=== File {} read ==='.format(file.name))

        # If file contains a query or mapping then save expressions
        # in a CSV file (if required)
        if self.content_type in ['mapping', 'queries']:
            serialization = input('\nSave mapping results or query on output file? (csv/xml/n3/json/n): ')
            if serialization != 'n':
                if serialization in ['csv', 'xml', 'n3', 'json']:
                    Open_output_file(self.expressions, self.header[6], self.header[1], serialization)

        # If file contains a query then create a query object and query_spec
        if self.content_type == 'queries':
            query = Query(Gel_net, main)
            # Create query_spec
            query.query_spec = self.interpreted_lines
            query.Interpret_query_spec()

    def UID_range_limit(self, string, default):
        ''' Determine a UID range value from numeric string, otherwise make default'''
        uid = default
        if string != '':
            parts = string.partition('=')
            if parts[2] != '':
                number = parts[2]
            else:
                number = parts[0]
            dots_removed   = number.replace('.','')
            commas_removed = dots_removed.replace(',','')
            spaces_removed = commas_removed.replace(' ','')
            if spaces_removed.isdecimal():
                uid = int(spaces_removed)
        return uid

    def Rearrange_input_row(self, idea_col_in, in_row, source_ids, loc_default_row):
        '''Rearrange values in in_row into db_row conform the destination column ids specified in source_id_dict.
        Missing values are loaded with local default values, possibly from an in_row with default values.
        '''
        # Load default values in row
        db_row = loc_default_row[:]
        # Put input fields from in_row in destination fields in db_row
        for source_id in source_ids:
            if source_id == 0 or self.source_id_dict[source_id] == 0:
                continue
            else:
                # Remove commas and convert source_id to integer
                #if self.test == True:
                    #print('source_id', source_id, source_ids.index(source_id), in_row[source_ids.index(source_id)])
                if source_id in \
                   set([69, 71, 5, 2, 72, 19, 1, 60, 85, 74, 15, 66, 76, 70, 67, 11, 6, 78, 53, 50]):
                    uid, integer = Convert_numeric_to_integer(in_row[source_ids.index(source_id)])
                    value = str(uid)
##                    if integer == False and value != '':
##                        print('Warning Idea {}: UID <{}> in column {} is not a whole number'.\
##                              format(in_row[idea_col_in], in_row[source_ids.index(source_id)], source_id))
                else:
                    value = in_row[source_ids.index(source_id)]
                db_row[self.source_id_dict[source_id]] = value
                

                # Index for UID of UoM, successorUID, appContUID and collUID are optional
                if source_id in [2, 1, 60, 15]:
                    if idea_col_in != 0 and value == '':
                        print('*Warning Idea {}: UID in column {} is missing'.\
                              format(in_row[idea_col_in], source_id))
        #if self.test == True:
        #    print('db_row', db_row)
        #self.test = False
        return db_row

    def Verify_row(self, file, db_row, Gel_net):
        ''' Verify values in db_row before loading in database and amend where applicable.
            Per rel_type and kind first role and kind of second role add/verify kind of role players. 
            Collect rows in expressions table.
        '''
        correct = True

        # Collect used languages that denote language of left hand objects
        # Verify consistency of language names.
        lang_uid = db_row[lang_uid_col]
        if lang_uid != '':
            # If file language is Dutch then lang_uid and name must be in or added to lang_dict_NL
            if file.lang_ind == 1:
                if lang_uid not in Gel_net.lang_dict_NL:
                   Gel_net.lang_dict_NL[lang_uid] = db_row[lang_name_col]
                try:
                    if db_row[lang_name_col] == Gel_net.lang_dict_NL[lang_uid]:
                        pass
                except KeyError:
                    print('  Waarschuwing: Naam van de taal {} correspondeert niet met eerdere naam {} voor UID {}'.\
                          format(db_row[lang_name_col], Gel_net.lang_dict_NL[lang_uid], lang_uid))
            elif file.lang_ind == 0:
                # If file language is English then lang_uid and name must be in or added to lang_dict_EN
                if lang_uid not in Gel_net.lang_dict_EN:
                   Gel_net.lang_dict_EN[lang_uid] = db_row[lang_name_col]
                try:
                    if db_row[lang_name_col] == Gel_net.lang_dict_EN[lang_uid]:
                        pass
                except KeyError:
                    print('  Warning: Language name {} does not correspond to earlier name {} for UID {}'.\
                          format(db_row[lang_name_col], Gel_net.lang_dict_EN[lang_uid], lang_uid))
            else:
                print('Language of file {} is not English or Nederlands'.format(file.lang_name))
        else:
            # No lang_uid present: check whether lang_name present
            if db_row[lang_name_col] != '':
                recognized = False
                if file.lang_ind == 1:
                    # Find the lang_uid for a given lang_name in db_row[lang_name_col]
                    for key,value in Gel_net.lang_dict_NL.items():
                        if db_row[lang_name_col] == value:
                            db_row[lang_uid_col] = key
                            recognized = True
                            continue
                else:
                    for key,value in Gel_net.lang_dict_EN.items():
                        if db_row[lang_name_col] == value:
                            db_row[lang_uid_col] = key
                            recognized = True
                            continue
                if recognized == False:
                    print('Language name {} not recognized. File language added as default'.format(db_row[lang_name_col]))
                    db_row[lang_uid_col]  = file.lang_uid
                    db_row[lang_name_col] = file.lang_name
            else:
                # If lang_name also not present, then use file.lang_name
                db_row[lang_uid_col]  = file.lang_uid
                db_row[lang_name_col] = file.lang_name
                
        # Collect language communities that denote context for unique name of left hand objects
        # And verify consistency of community names.
        comm_uid = db_row[comm_uid_col]
        if comm_uid != '':
            if file.lang_ind == 1:
                if comm_uid not in Gel_net.comm_dict_NL:
                    Gel_net.comm_dict_NL[comm_uid] = db_row[comm_name_col]
                if db_row[comm_name_col] != Gel_net.comm_dict_NL[comm_uid]:
                    print('  Warning: Community name {} does not correspond to earlier name {} for UID {}.'.\
                          format(db_row[comm_name_col], Gel_net.comm_dict_NL[comm_uid], comm_uid))
            else:
                if comm_uid not in Gel_net.comm_dict_EN:
                    Gel_net.comm_dict_EN[comm_uid] = db_row[comm_name_col]
                if db_row[comm_name_col] != Gel_net.comm_dict_EN[comm_uid]:
                    print('  Warning: Community name {} does not correspond to earlier name {} for UID {}.'.\
                          format(db_row[comm_name_col], Gel_net.comm_dict_EN[comm_uid], comm_uid))

        else:
            # No community_uid present: check whether comm_name present
            if db_row[comm_name_col] != '':
                comm_recignized = False
                # Find the comm_uid for a given comm_name in db_row[comm_name_col]
                if file.lang_ind == 1:
                    for key,value in Gel_net.comm_dict_NL.items():
                        if db_row[comm_name_col] == value:
                            db_row[comm_uid_col] = key
                            comm_recignized = True
                            continue
                else:
                    for key,value in Gel_net.comm_dict_EN.items():
                        if db_row[comm_name_col] == value:
                            db_row[comm_uid_col] = key
                            comm_recignized = True
                            continue
                if comm_recignized == False:
                    Gel_net.unknown_obj_uid += 1
                    print('Community name {} is not yet known. New UID {} and name added'\
                          .format(db_row[comm_name_col], Gel_net.unknown_obj_uid))
                    db_row[comm_uid_col] = str(Gel_net.unknown_obj_uid)
                    if file.lang_ind == 1:
                        Gel_net.comm_dict_NL[db_row[comm_uid_col]] = db_row[comm_name_col]
                    else:
                        Gel_net.comm_dict_EN[db_row[comm_uid_col]] = db_row[comm_name_col]
            else:
                db_row[comm_uid_col] = '492014'
                db_row[comm_name_col] = 'Gellish'
            
        # If rel_type_uid, rh_uid or lh_uid does not exist (=0), but name is present
        # then search for its name in network to find uid.
        # and select from candidates or confirm single candidate.
        string_commonality = 'csi'
        mapping = False
        
        # REL_name: Remove leading and/or trailing whitespaces in rel_name if applicable.
        stripped_name = db_row[rel_type_name_col].strip()
        if stripped_name != db_row[rel_type_name_col]:
            print("Warning: Relation type name {} in idea {} contains leading and/or trailing spaces, which are removed."\
                  .format(db_row[rel_type_name_col], db_row[idea_uid_col]))
            db_row[rel_type_name_col] = stripped_name
            
        # REL_uid: If rel_type_uid is unknown, then find it from its phrase (name)
        if db_row[rel_type_uid_col] == '' and db_row[rel_type_name_col] != '':
            uid_new, rel_map = Gel_net.Find_object_by_name(db_row[rel_type_name_col], string_commonality)
            db_row[rel_type_uid_col] = rel_map[0]
            mapping = True
            #print('rel_map:', rel_map)
            if uid_new:
                print('Unknown name of relation type {} in idea {}; should be added to the language definition before being used.'.\
                      format(db_row[rel_type_name_col], db_row[idea_uid_col]))
        else:
            # rel_map = uid, name, blank
            rel_map = [db_row[rel_type_uid_col], db_row[rel_type_name_col], '']

        # RH_name: Remove leading and/or trailing whitespaces in rh_name if applicable.
        stripped_name = db_row[rh_name_col].strip()
        if stripped_name != db_row[rh_name_col]:
            print("**Warning: Right hand name '{}' in idea {} contains leading and/or trailing spaces, which are removed.".\
                  format(db_row[rh_name_col], db_row[idea_uid_col]))
            db_row[rh_name_col] = stripped_name

        # RH_uid (in case of alias relation, rel_type_phrase_uid == 6066 is assumed) *** check later ***
        if db_row[rh_uid_col] == '' and db_row[rh_name_col] != '':
            uid_new, rh_map = Gel_net.Find_object_by_name(db_row[rh_name_col], string_commonality)
            db_row[rh_uid_col] = rh_map[0]
            mapping = True
            #print('rh_map :', rh_map)
        else:
            rh_map = [db_row[rh_uid_col], db_row[rh_name_col], '']

        # LH_name: Remove leading and/or trailing whitespaces in lh_name if applicable.
        stripped_name = db_row[lh_name_col].strip()
        if stripped_name != db_row[lh_name_col]:
            print("**Warning: Left hand name '{}' in idea {} contains leading and/or trailing spaces, which are removed.".\
                  format(db_row[lh_name_col], db_row[idea_uid_col]))
            db_row[lh_name_col] = stripped_name
            
        # LH_uid: check after rel and rh, because in case of alias lh_uid = rh_uid
        # If lh_uid == '' but name is given, then determine uid from name in dictionary
        if db_row[lh_uid_col] == '' and db_row[lh_name_col] != '':
            new_name = False
            # If alias relation type lh uid = rh uid
            if db_row[rel_type_uid_col] in Gel_net.alias_uids:
                db_row[lh_uid_col] = db_row[rh_uid_col]
                lh_map = [db_row[lh_uid_col], db_row[lh_name_col], '']
                new_name = True
            else:
                # Not an alias relation: find lh_map = [uid, name, description]
                new_name, lh_map = Gel_net.Find_object_by_name(db_row[lh_name_col], string_commonality)
                db_row[lh_uid_col] = lh_map[0] 
                new_name = True
            #print('lh_map :', lh_map)
            if new_name:
                # Add unknown name to the dictionary
                name_in_context = (db_row[lang_uid_col], db_row[comm_uid_col], db_row[lh_name_col])
                value_triple = (db_row[lh_uid_col], 5117, db_row[part_def_col])
                Gel_net.dictionary[name_in_context] = value_triple
        else:
            # lh_uid is known
            # If alias relation type, then check whether indeed lh_uid == rh_uid
            if db_row[rel_type_uid_col] in Gel_net.alias_uids:
                if db_row[lh_uid_col] != db_row[lh_uid_col]:
                    print('** Error: Alias relation of idea {} requires that left hand uid {} is equal to right hand uid {}'\
                          .format(db_row[idea_uid_col], db_row[lh_uid_col], db_row[rh_uid_col]))
            lh_map = [db_row[lh_uid_col], db_row[lh_name_col], db_row[part_def_col]]

        # UOM
        if db_row[uom_uid_col] == '' and db_row[uom_name_col] != '':
            # find uom_map = [uid, name, description] via name of uom
            new_name, uom_map = Gel_net.Find_object_by_name(db_row[uom_name_col], string_commonality)
            if new_name:
                print('**Error: Unit of measure name {} in idea {} is unknown.'.\
                      format(db_row[uom_name_col], db_row[idea_uid_col]))

        # If comm_uid and name still unknown, then use defaults
        if db_row[comm_uid_col] == '':
            # If comm_uid still unknown, then use default file.comm_uid and name
            db_row[comm_uid_col]  = file.comm_uid
            db_row[comm_name_col] = file.comm_name
         
        # Prepare an interpretation in the expressions table
            db_row[lh_uid_col]        = lh_map[0]
            db_row[lh_name_col]       = lh_map[1]
            db_row[rel_type_uid_col]  = rel_map[0]
            db_row[rel_type_name_col] = rel_map[1]
            db_row[rh_uid_col]        = rh_map[0]
            db_row[rh_name_col]       = rh_map[1]
            db_row[uom_uid_col]       = uom_map[0]
            db_row[uom_name_col]      = uom_map[1]
            if self.content_type == 'queries':
                db_row[intent_uid_col] = '790665'
                if file.lang_ind == 1:
                    db_row[intent_name_col] = 'vraag'
                else:
                    db_row[intent_name_col] = 'question'
            
            interpreted_line = [lh_map[0], lh_map[1], rel_map[0], rel_map[1], rh_map[0], rh_map[1],
                                uom_map[0], uom_map[1]]
            self.interpreted_lines.append(interpreted_line)

        # Verify whether the relation type UID is known in the current language definition:
        rel_type_uid = db_row[rel_type_uid_col]
        if rel_type_uid not in Gel_net.rel_type_uids:
            print("  Error: Relation type uid ({}) '{}' is not (yet) defined as a binary relation. Idea {} ignored.".\
                  format(rel_type_uid, db_row[rel_type_name_col], db_row[idea_uid_col]))     
            db_row[rel_type_uid_col] = 5935 # binary relation
            correct = False

        # Collect base_phrases and inverse_phrases in list
        elif db_row[rel_type_uid_col] == '6066':
            Gel_net.base_phrases.append(db_row[lh_name_col])
        elif db_row[rel_type_uid_col] == '1986':
            Gel_net.inverse_phrases.append(db_row[lh_name_col])
        
        # If phrase_type == 0 (unknown) then determine the phrase type;
        # base_phrase_type_uid = 6066 inverse_phrase_type_uid = 1986.
        # In case of the base ontology, where only bootstrapping relations may be present,
        # the base_phrases are the collection of bootstrapping phrases: base_boot_phrases
        # and inverse_phrases are the initial inverse_boot_phrases.
        elif db_row[phrase_type_uid_col] == '':
            if db_row[rel_type_name_col] in Gel_net.base_phrases:
                db_row[phrase_type_uid_col] = '6066'
            elif db_row[rel_type_name_col] in Gel_net.inverse_phrases:
                db_row[phrase_type_uid_col] = '1986'
            else:
                print("Error: Phrase <{}> ({}) not yet defined. Idea {} ignored".\
                      format(db_row[rel_type_name_col], db_row[rel_type_uid_col], db_row[idea_uid_col]))
                correct = False

        # If partial_definition known, then delete full_definition.
        if db_row[part_def_col] != '':
            db_row[full_def_col] = ''
##        else:
##            db_row[part_def_col] = db_row[full_def_col]
##            db_row[full_def_col] = ''

        # if for specialization relations lh and rh kinds of roles are missing, load them with defaults
        if correct and db_row[rel_type_uid_col] in ['1146']:
            if db_row[lh_role_uid_col]  == '': db_row[lh_role_uid_col]  = subtypeRoleUID
            if db_row[lh_role_name_col] == '': db_row[lh_role_name_col] = subtypeName[file.lang_ind]
            if db_row[rh_role_uid_col]  == '': db_row[rh_role_uid_col]  = supertypeRoleUID
            if db_row[rh_role_name_col] == '': db_row[rh_role_name_col] = supertypeName[file.lang_ind]

        # Store row in self.expressions
        if correct:
            self.expressions.append(db_row[:])
        return correct, db_row
#----------------------------------------------------
if __name__ == "__main__":
    from SystemUsers import System, User
    from SemanticNetwork import Semantic_Network

    user = User('Andries')
    # Create semantic network and define user
    Gel_net = Semantic_Network("Network", user)

    expr_list = Expression_list(Gel_net)
    expr_list.expressions = [(101,'lh-101',1726,'is een kwalitatief subtype van',102,'rh-102'),
                             (102,'lh-102',1146,'is een soort'                  ,103,'rh-103')]
    
    # Read base ontology
    Import_Base_Ontology(Gel_net) #, Gel_db)
    
    subject_name = 'test'
    lang_name = 'Nederlands'
    
    serialization = 'csv'
    Open_output_file(expr_list.expressions, subject_name, lang_name, serialization)
    
    serialization = 'xml'
    Open_output_file(expr_list.expressions, subject_name, lang_name, serialization)
    
    serialization = 'n3'
    Open_output_file(expr_list.expressions, subject_name, lang_name, serialization)
    
    serialization = 'json'
    Open_output_file(expr_list.expressions, subject_name, lang_name, serialization)
