import os
import sys
import csv
import json
from tkinter import filedialog

from Bootstrapping import *
from Expr_Table_Def import *
from Create_output_file import *
from Mapping_tables_IB import *
from Anything import Anything
#from User_interface import Message
##from Display_views import Display_views

class Gellish_file:
    """ Data about files, especially Gellish files.
        A Gellish file is a list of expressions in full Gellish Expression Format
        read from any of various sources (such as CSV files),
        build a semantic network from it
        or export such a list in any of various formats (such as CSV or JSON files).
    """
    
    def __init__(self, path_and_name, gel_net):
        ''' Initialize a file that is read from a given location (path)
            The file_name is without path or directory, but with file extension.
        '''
        self.path_and_name = path_and_name
        self.gel_net = gel_net
        self.expressions = []
        self.query_lines = []
        
        # Determine the directory, if present
        parts = path_and_name.rsplit('\\', maxsplit=1)
        if len(parts) == 1:
            parts2 = path_and_name.rsplit('/', maxsplit=1)
            if len(parts2) == 1:
                Message(self.gel_net.GUI_lang_index,
                    'File name {} has no directory.'.format(path_and_name),\
                    'Filenaam {} heeft geen directory.'.format(path_and_name))
                self.name = parts2[0]
            else:
                self.name = parts2[1]
        else:
            self.name = parts[1]

        # Determine the file extension from path_and_name
        name_ext = self.path_and_name.rsplit('.', maxsplit=1)
        if len(name_ext) == 1:
            Message(self.gel_net.GUI_lang_index,
                'File name {} has no file extension.'.format(path_and_name),\
                'Filenaam {} heeft geen file extensie.'.format(path_and_name))
            self.extension = ''
            return
        elif name_ext[1] not in ['csv', 'json']:
            Message(self.gel_net.GUI_lang_index,
                'File name extension {} is not (yet) supported.'.format(name_ext[1]),\
                'Filenaam extensie {} wordt (nog) niet ondersteund.'.format(name_ext[1]))
            self.extension = ''
        else:
            # Allocate file extension to file
            self.extension = name_ext[1]
            
##
##class Expression_list:
##    ''' A Gellish file is a list of expressions in full Gellish Expression Format
##        read from any of various sources (such as CSV files),
##        build a semantic network from it
##        or export such a list in any of various formats (such as CSV or JSON files).
##    '''
##    def __init__(self, gel_net):
##        self.gel_net = gel_net

    def Import_Gellish_from_file(self):
        """ Read current file in a Gellish Expression Format.
            Rearrange the expressions.
            Verify the quality
            and if correct then store rows in an expressions table
            and extent the semantic network with its content.
        """
        Message(self.gel_net.GUI_lang_index,
            '>>> Read file {}'.format(self.path_and_name),\
            '>>> Lees file {}'.format(self.path_and_name))
        try:
            f = open(self.path_and_name, "r", encoding="utf-8")
        except IOError:
            Message(self.gel_net.GUI_lang_index,
                "File '{}' does not exist or is not readable.".format(self.name),\
                "File '{}' bestaat niet of is niet leesbaar.".format(self.name))
            sys.exit()

        # Determine the file extension of the current file
        if self.extension == 'csv':
    ##        # determine dialect
    ##        sample = f.read(4096)
    ##        dialect = csv.Sniffer().sniff(sample, delimiters=';')
    ##
    ##        # rewind to start
    ##        f.seek(0)
    ##
            # Initialise csv reading and read first line
    ##        self.reader = csv.reader(f, dialect)
            reader = csv.reader(f, delimiter=';')
            self.header = next(reader)
        elif self.extension == 'json':
            self.json_dict = json.load(f)

            # Determine JSON file type: list or dict?
            # Convert dict to list
            #print('JSON File type', type(self.json_dict))
            self.json_list = list(self.json_dict.items())
            self.header = self.json_list[0]
        else:
            Message(self.gel_net.GUI_lang_index,
                'File extension {} is not supported.'.format(self.extension),
                'File extensie {} wordt niet ondersteund.'.format(self.extension))
            return

        # Read first line and determine whether the current file is a Gellish file or not
        #print('Header line:', self.header)
        if self.header[0] != "Gellish":
            Message(self.gel_net.GUI_lang_index,
                "File {} is not in Gellish expression format, "\
                "because the first field has not as content 'Gellish'.".\
                format(self.name), \
                "File {} is niet in Gellish expressie formaat, "\
                "want het eerste veld heeft niet als inhoud 'Gellish'.".\
                format(self.name))
            if self.extension == 'json':
                self.Interpret_non_gellish_JSON_file()
        else:
            self.Import_expressions_from_Gellish_file(reader)

    def Interpret_non_gellish_JSON_file(self):
        ''' Read a non-Gellish JSON file and convert it into a Gellish file
            Guided by a mapping table
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
        # Set the Gellish output file language to 0 = English
        self.gel_net.reply_lang_index = 0
        lang_comm = ['910036', 'English', '910037', 'Nederlands', '2700929', 'IB']
        while new_article:
            #list_of_keys = list(self.json_dict.keys())
            # Find article name as value of a first level key
            for key_map in keys_map:
                if key_map[0] in self.json_dict:
                    if key_map[1] == '970047':
                        article_identifier = self.json_dict[keys_map[0][0]]
                        self.object_uid += + 1
                        article_uid = str(self.object_uid)
                        #print('Article id:', article_identifier)
                    elif key_map[1] == '5605':
                        article_name = self.json_dict[keys_map[1][0]]
                        #print('Article name:', article_name)

                    elif key_map[1] == '493676':
                        # Find attributes_map and determine list of attributes ('properties')
                        # as value of a first level key
                        attribute_dict = self.json_dict[key_map[0]]
                        #print('Attribute type:', type(attribute_dict))
                        #print('Attribute:', attribute_dict)
                        list_of_attrib = list(attribute_dict.keys())

                        # For each attribute find sub_attr_dict and its list of sub_attrib
                        # attrib_map e.g. soort object, hoogte, breedte
                        # list_of_attrib e.g. ibProductsoort, breedteMm, hoogteMm
                        for attrib_map in attributes_map:
                            if attrib_map[0] in list_of_attrib:
                                #print('attrib_map[0]', attrib_map[0])
                                # sub_attrib_dict e.g. label, name, value, unit
                                sub_attrib_dict = attribute_dict[attrib_map[0]]
                                # Determine list of values
                                del values[:]
                                for sub in value_key_map:
                                    if sub[0] in sub_attrib_dict:
                                        val = sub_attrib_dict[sub[0]]
                                    else:
                                        val = ''
                                    values.append(val)
                                #print('Values:', values)    # label, name, value, unit

                                # For each type of attrib_map (kind of relation),
                                # depending on attribute (attrib_map[0]),
                                # create Gellish expression(s)
                                # e.g. ibProductsoort indicates:
                                #        <is a model of> 730066, 'soort object' or
                                #      breedteMn indicates:
                                #        <# has by definition as aspect a> 550464, 'breedte'

                                # If attrib_map indicates a <# is a model of> relation, then
                                if attrib_map[1][1] == '5396':
                                    self.idea_uid += +1
                                    lh_uid_name         = [article_uid, article_identifier]
                                    rel_uid_phrase_type = list(attrib_map[1][1:4])
                                    rh_role_uid_name    = ['', '']
                                    # rh_uid_name e.g. 43769 , 'dakvenster'
                                    rh_uid_name         = list(values_map[values[2]])
                                    uom_uid_name        = ['', '']
                                    description         = article_name
                                    intent_uid_name     = ['491285', 'bewering']
                                    gellish_expr = Create_gellish_expression(
                                        lang_comm, str(self.idea_uid), intent_uid_name,\
                                        lh_uid_name, rel_uid_phrase_type,\
                                        rh_role_uid_name, rh_uid_name, \
                                        uom_uid_name, description)
                                    #print('Gellish_expr1:', gellish_expr)
                                    self.gel_expressions.append(gellish_expr)

                                # If attrib_map indicates
                                #   a <has by definition as aspect a> relation, 
                                # then create two expressions:
                                #   1. for indicating the intrinsic aspect and the kind of aspect
                                #   2. for quantification of the intrinsic aspect
                                elif attrib_map[1][1] == '5527':
                                    self.object_uid += + 1
                                    self.idea_uid   += +1
                                    lh_uid_name      = [article_uid, article_identifier]
                                    rel_uid_phrase_type = list(attrib_map[1][1:4])
                                    # rh_uid_name e.g. 550464 , 'breedte'
                                    rh_uid_name      = list(attrib_map[1][4:6])
                                    rh_role_uid_name = [str(self.object_uid), \
                                                        rh_uid_name[1] \
                                                        + of_text[self.gel_net.reply_lang_index] \
                                                        + article_identifier]
                                    uom_uid_name     = ['', '']
                                    description      = ''
                                    intent_uid_name = ['491285', 'bewering']
                                    gellish_expr = Create_gellish_expression(
                                        lang_comm, str(self.idea_uid), intent_uid_name,\
                                        lh_uid_name, rel_uid_phrase_type,\
                                        rh_role_uid_name, rh_uid_name, \
                                        uom_uid_name, description)
                                    #print('Gellish_expr2:', gellish_expr)
                                    self.gel_expressions.append(gellish_expr)

                                    # Create an expression
                                    # for qualification or quantification of the aspect.
                                    # If the value (values[2]) is a whole number
                                    # then create a uid in the 2 billion range for it
                                    if values[2].isdecimal():
                                        value_uid = str(int(values[2]) + 2000000000)
                                        # value_uid_name e.g. '2000000940', '940'
                                        value_uid_name = [value_uid, values[2]]
                                    else:
                                        # If value[2] includes a decimal comma,
                                        # then replace the comma by a dot
                                        commas_replaced = values[2].replace(',', '.')
                                        dots_removed = commas_replaced.replace('.', '')
                                        # If the value without dots is numeric,
                                        # then create a uid for a floating point number
                                        if dots_removed.isdecimal():
                                            self.object_uid += + 1
                                            value_uid_name = [str(self.object_uid),commas_replaced]
                                        else:
                                            # Value[2] is not numeric
                                            # value_uid_name e.g. '310024' , 'grenen'
                                            value_uid_name = values_map[values[2]]
                                    self.idea_uid += +1
                                    rh_role_uid_name_2 = ['', '']
                                    uom_uid_name = list(values_map[values[3]])
                                    description  = ''
                                    intent_uid_name = ['491285', 'bewering']
                                    gellish_expr = Create_gellish_expression(
                                        lang_comm, str(self.idea_uid), intent_uid_name,\
                                        rh_role_uid_name, \
                                        quantification[self.gel_net.reply_lang_index],\
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
        Open_output_file(self.gel_expressions, subject_name[self.gel_net.reply_lang_index], \
                         lang_name, serialization)

    def Import_expressions_from_Gellish_file(self, reader):
        ''' Read the expressions from the current file in Gellish expression format
            verify its quality
            and add its content to the semantic network
        '''

        # Initialize expressions table
        self.expressions = []
        self.query_lines = []

        self.Interpret_the_first_header_line()

        # Read 2nd line ==== with column ids and convert them to integers
        row2 = next(reader)
        in_col = []
        for col_id in row2:
            if col_id == '':
                int_val = 0
            else:
                int_val, is_integer = Convert_numeric_to_integer(col_id)
                if is_integer is False:
                    Message(self.gel_net.GUI_lang_index,
                        'Value {} on row 2 is not a whole number. Column is ignored'.\
                        format(int_val),\
                        'Waarde {} op rij 2 is geen geheel getal. Kolom wordt genegeerd'.\
                        format(int_val))
                    int_val = 0
            in_col.append(int(int_val))
        source_ids = list(map(int, in_col))

        # Check if idea_uid column is present
        if 1 not in source_ids:
            Message(self.gel_net.GUI_lang_index,
                'Warning: Column for UID of idea is missing. '
                'The file is not added to the semantic network.',\
                'Waarschuwing: Kolom voor UID van idee ontbreekt. '
                'De file is niet toegevoegd aan het semantische netwerk.')
            idea_col_in = 0
        else:
            # the column nr where idea_uid is located (for error messageing)
            idea_col_in = source_ids.index(1)

        # Check if status column is present
        if 8 not in source_ids:
            Message(self.gel_net.GUI_lang_index,
                'Warning: Column for status is missing. '
                'File is not added to the semantic network.',\
                'Waarschuwing: Kolom voor status ontbreekt. '
                'De file is niet toegevoegd aan het semantische netwerk.')
            status_col_in = 0
        else:
            status_col_in = source_ids.index(8)

        lang_name_col_id  = {}
        lang_descr_col_id = {}
        # For all column source_ids in reader
        # find the corresponding column in expr_col_ids
        # and store them in source_id_dict.
        # Columns ids for names in other languages are not stored in destionarion ids
        # but in lang_name_col_id
        # (those names will not be stored in destination tables for ideas
        # (thus not in the sql_database)
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
                    if str_id not in self.gel_net.uid_dict:
                        lang = Anything(str_id, self.gel_net.lang_dict_EN[str_id])
                        lang.defined = False
                        self.gel_net.objects.append(lang)
                        self.gel_net.uid_dict[lang.uid] = lang.name
                        self.gel_net.lang_uid_dict[lang.uid] = lang.name
                elif source_id >= 1910036 and source_id < 1912000:
                    lang_descr_col_id[source_id] = source_ids.index(source_id)
                else:
                    Message(self.gel_net.GUI_lang_index,
                        'Column ID {} is unknown. Column is ignored.'.format(source_id),
                        'Kolom ID {} is onbekend. De kolom is genegeerd.'.format(source_id))
                    #lang_name_col_id[source_id] = 0    # source_ids.index(source_id)
        #print('Source_ids: ', source_ids)
        #print('Source_id_dict', self.source_id_dict)

        # Skip 3rd line ====
        next(reader)

        # Read line 4 etc. where data starts ====
        loc_default_row = default_row[:]
        idea_uid = 0
        db_row   = []

        for in_row in reader:
            # skip empty rows
            if in_row == []:
                #print('Empty row following idea {} skipped.'.format(idea_uid))
                continue
            # Skip rows with status 'ignore' or equivalent
            if in_row[status_col_in] in ignores:
                #print('Expression with status = "ignore etc." following idea {} skipped.'.\
                #      format(idea_uid))
                continue

            # Rearrange the values in in_row in the sequence of the database
            # and add defaults for missing values and remove commas (,) from uids
            db_row = self.Rearrange_input_row(idea_col_in, in_row, source_ids, loc_default_row)

            # Save idea_uid for later reference to the preceeding row.
            idea_uid = db_row[idea_uid_col]

            # If row in current file contains default values for the file,
            # then copy them to local defaults
            if db_row[status_col] == "default" or db_row[status_col] == "defaults":
                loc_default_row = db_row[:]
                continue

            # Verify existence and uniqueness of idea_uid
            # If no idea_uid is provided, then add a uid conform prefix and range
            if idea_uid == '':
                self.gel_net.new_rel_uid += 1
                if str(self.gel_net.new_rel_uid) not in self.gel_net.idea_uids \
                   and self.gel_net.new_rel_uid <= self.upper_rel_range_uid:
                    idea_uid = self.prefix + str(self.gel_net.new_rel_uid)
                    db_row[idea_uid_col] = idea_uid
                    self.gel_net.idea_uids.append(idea_uid)
                    #print('Idea_uid {} added'.format(idea_uid))
                else:
                    Message(self.gel_net.GUI_lang_index,
                        'UID {} already used in the network'.format(self.gel_net.new_rel_uid),\
                        'UID {} is al gebruikt in het netwerk'.format(self.gel_net.new_rel_uid))
            elif idea_uid not in self.gel_net.idea_uids:
                    self.gel_net.idea_uids.append(idea_uid)
            else:
                Message(self.gel_net.GUI_lang_index,
                    'Duplicate idea UID {}. Latter idea ignored.'.format(idea_uid),
                    'Dubbele idea UID {}. De laatste is genegeerd.'.format(idea_uid))
                continue

            # VERIFY input row values, amend where applicable
            correct, db_row = self.Verify_row(db_row)

            names_and_descriptions = []
            if correct:
                # If an additional language column is present
                # then append the dictionary with the terms available in the language column
                #print('Col_ids',lang_name_col_id)
                for col_id in lang_name_col_id:
                    # Only for rows with a specialization and alias relation
                    if (db_row[rel_type_uid_col] in self.gel_net.specialRelUIDs or \
                        db_row[rel_type_uid_col] in self.gel_net.alias_uids):
                        # Check whether column value (name of object) is not blank,
                        # then include name_in_context in the dictionary (if not yet present)
                        if in_row[lang_name_col_id[col_id]] != '':
                            if db_row[rel_type_uid_col] in self.gel_net.alias_uids:
                                naming_uid = db_row[rel_type_uid_col]

                                # Collect base_phrase or inverse_phrase
                                # of additional language column
                                if db_row[rel_type_uid_col] == '6066':
                                    self.gel_net.total_base_phrases.append(\
                                        in_row[lang_name_col_id[col_id]])
                                elif db_row[rel_type_uid_col] == '1986':
                                    self.gel_net.total_inverse_phrases.append(
                                        in_row[lang_name_col_id[col_id]])
                            else:
                                naming_uid = '5117'
                            # Note: col_id is integer, whereas lang_uid should be a string
                            name_in_context = (str(col_id), db_row[comm_uid_col], \
                                               in_row[lang_name_col_id[col_id]])

                            # Check whether a description column is present
                            key_descr = col_id + 1000000
                            if key_descr in lang_descr_col_id:
                                lang_descr = in_row[lang_descr_col_id[key_descr]]
                            else:
                                lang_descr = ''

                            if name_in_context not in self.gel_net.dictionary:
                                value_triple = (db_row[lh_uid_col], naming_uid, lang_descr)
                                self.gel_net.dictionary[name_in_context] = value_triple
                                name_and_descr = [str(col_id), db_row[comm_uid_col],\
                                                  in_row[lang_name_col_id[col_id]], \
                                                  naming_uid, lang_descr]
                                names_and_descriptions.append(name_and_descr)
                                #print('Name and descr', name_and_descr)

                # Add name of current file to expression
                db_row[file_name_col] = self.name
            else:
                #print('    == Error in expression of idea ', idea_uid) #, 'row ignored.')
                pass

            # Add expressions to the semantic network, except for queries
            if self.content_type != 'queries':
                self.gel_net.Add_row_to_network(db_row, names_and_descriptions)
                names_and_descriptions.clear()

        Message(self.gel_net.GUI_lang_index,
            '<<< File read: {}'.format(self.name),
            '<<< File gelezen: {}'.format(self.name))

        # If the current file contains a query or mapping then save expressions
        # in a CSV file (if required)
        if self.content_type in ['mapping', 'queries']:
            serialization = input('\nSave mapping results or query on output file? '
                                  '(csv/xml/n3/json/n): ')
            if serialization != 'n':
                if serialization in ['csv', 'xml', 'n3', 'json']:
                    Open_output_file(self.expressions, self.header[6], self.header[1], \
                                     serialization)

        # If the current file contains a query then create a query object and query_spec
        if self.content_type == 'queries':
            query = Query(self.gel_net, main)
            # Create query_spec
            query.query_spec = self.query_lines
            query.Interpret_query_spec()

    def Interpret_the_first_header_line(self):
        ''' Interpret the (first) header line of a file with Gellish expressions.
        '''
        # Determine the file type (header[5]) and verify whether base ontology is first provided
        self.base_ontology = False
        if self.header[5] in ['base ontology', 'Base ontology', 'Base Ontology', \
                              'basisontologie', 'Basisontologie']:
            self.content_type = "dictionary"
            self.base_ontology = True
            
        elif self.header[5] in ['domain dictionary', 'Domain dictionary', 'Domain Dictionary', \
                                'domeinwoordenboek', 'Domeinwoordenboek', 'Woordenboek']:
            self.content_type = "dictionary"
            
        elif self.header[5] in ['Product models', 'Process models', 'Product and process models', \
                           'Productmodellen','Procesmodellen', 'Product- en procesmodellen', \
                           'Productmodel', 'Product model', \
                           'Product type model', 'Producttypemodel', 'Producttypemodellen']:
            self.content_type = "product_model"
            
        elif self.header[5] in ['Query', 'Queries', 'Vraag', 'Vragen']:
            # A file that contains one or more queries that need to be answered
            self.content_type = "queries"
            
        elif self.header[5] in ['Mapping']:
            # A file that required identification and/or allocation of uids
            self.content_type = "mapping"
        else:
            # A file with unknown content type
            Message(self.gel_net.GUI_lang_index,
                "File type '{}' is not standard. File with title '{}' processed".\
                format(self.header[5], self.header[6]), \
                "File type '{}' is niet standaard. File met titel '{}' is verwerkt".\
                format(self.header[5], self.header[6]))
            self.content_type = "unknown"
        
        self.descr = self.header[6]

        # Read the language name in which the textual fields (e.g. definitions)
        # in the current file generally are expressed (header[1]).
        # Set the default model language in the current file to: 0 = 'English'
        self.lang_ind = 0
        
        self.lang_name = self.header[1]
        if self.lang_name == 'Nederlands':
            self.lang_ind = 1
            self.lang_uid = '910037'
            self.comm_uid = '492014'        # 492014 denotes 'Gellish'
            self.comm_name = "Gellish"      # default
        elif self.lang_name == 'English':
            self.lang_ind = 0
            self.lang_uid = '910036'
            self.comm_uid = '492014'
            self.comm_name = "Gellish"    # default
        else:
            Message(self.gel_net.GUI_lang_index,
                'Name of file language {} is unknown. File is ignored.'.\
                format(self.lang_name),\
                'De naam van de taal voor de file {} is onbekend. De file is genegeerd.'.\
                format(self.lang_name))
            return

        # Create language object if not yet existing
        if self.lang_uid not in self.gel_net.lang_uid_dict:
            lang = Anything(self.lang_uid, self.lang_name)
            self.gel_net.languages.append(lang)
            self.gel_net.lang_uid_dict[self.lang_uid] = self.lang_name

        # Set defaults for prefix and uid range limits
        self.prefix = 'test:'
        self.lower_obj_range_uid = 100
        self.upper_obj_range_uid = 499
        self.lower_rel_range_uid = 500
        self.upper_rel_range_uid = 999
            
        if len(self.header) > 7:
            params = ['prefix', \
                      'Lower_obj_uid', 'Upper_obj_uid', 'Lower_rel_uid', 'Upper_rel_uid']
            for value in self.header[7:]:
                value_parts = value.partition('=')
                if len(value_parts) > 1:
                    integer, number = self.Clean_whole_number(value_parts[2])
                    if value_parts[0] == params[0]:
                        self.prefix = value_parts[2]
                    elif value_parts[0] == params[1]:
                        self.lower_obj_range_uid = number # self.UID_range_limit(number, 100)
                    elif value_parts[0] == params[2]:
                        self.upper_obj_range_uid = number # self.UID_range_limit(number, 499)
                    elif value_parts[0] == params[3]:
                        self.lower_rel_range_uid = number # self.UID_range_limit(number, 500)
                    elif value_parts[0] == params[4]:
                        self.upper_rel_range_uid = number # self.UID_range_limit(number, 999)

            # Verify whether values indicate proper ranges
            if self.upper_obj_range_uid <= self.lower_obj_range_uid \
                    or self.lower_rel_range_uid <= self.upper_obj_range_uid \
                    or self.upper_rel_range_uid <= self.lower_rel_range_uid :
                Message(self.gel_net.GUI_lang_index,
                    'Object range UIDs are not in proper position or sequence.',\
                    'Object range UIDs staan niet op de juiste plaats '
                    'of in de juiste volgorde.')
                
        print('    Prefix: {}, Obj_range_UIDs: {}, {}, Rel_range_UIDs: {} {}'.\
              format(self.prefix, \
                     self.lower_obj_range_uid, \
                     self.upper_obj_range_uid, \
                     self.lower_rel_range_uid, \
                     self.upper_rel_range_uid))
        # Determine highest uid used within range for obj and rel
        # === to be done ===
        self.gel_net.new_obj_uid = self.lower_obj_range_uid
        self.gel_net.new_rel_uid = self.lower_rel_range_uid

##        # Determine the UID ranges for new objects and relations in this current file
##        if len(self.header) > 10:
##            # If range limits are given, then allocate or apply defaults
##            self.gel_net.lower_obj_range_uid = self.UID_range_limit(self.header[7] , 100)
##            self.gel_net.upper_obj_range_uid = self.UID_range_limit(self.header[8] , 499)
##            self.gel_net.lower_rel_range_uid = self.UID_range_limit(self.header[9] , 500)
##            self.gel_net.upper_rel_range_uid = self.UID_range_limit(self.header[10], 999)
##            # Verify whether values indicate proper ranges
##            if self.gel_net.upper_obj_range_uid <= self.gel_net.lower_obj_range_uid or\
##               self.gel_net.lower_rel_range_uid <= self.gel_net.upper_obj_range_uid or\
##               self.gel_net.upper_rel_range_uid <= self.gel_net.lower_rel_range_uid :
##                print('    Object range UIDs not in proper position or sequence.')
##            print('    Obj_range_UIDs: {}, {}; Rel_range_UIDs: {} {}'.\
##                  format(self.gel_net.lower_obj_range_uid, self.gel_net.upper_obj_range_uid, \
##                         self.gel_net.lower_rel_range_uid, self.gel_net.upper_rel_range_uid))
##        else:
##            self.gel_net.lower_obj_range_uid = 100
##            self.gel_net.upper_obj_range_uid = 499
##            self.gel_net.lower_rel_range_uid = 500
##            self.gel_net.upper_rel_range_uid = 999

##    def UID_range_limit(self, string, default):
##        ''' Determine a UID range value from numeric string, otherwise make default'''
##        limits = ['Lower_obj_uid', 'Upper_obj_uid', 'Lower_rel_uid', 'Upper_rel_uid']
##        uid = default
##        if string != '':
##            parts = string.partition('=')
##            if parts[2] != '':
##                if parts[1] not in limits:
##                    print('UID range limit name <{}> not in list {}'.format(parts[1], limits))
##                number = parts[2]
##            else:
##                number = parts[0]
##            dots_removed   = number.replace('.','')
##            commas_removed = dots_removed.replace(',','')
##            spaces_removed = commas_removed.replace(' ','')
##            if spaces_removed.isdecimal():
##                uid = int(spaces_removed)
##        return uid

    def Clean_whole_number(self, number):
        ''' Ensure that a whole number is coded as an integer '''
        integer = True
        dots_removed   = number.replace('.','')
        commas_removed = dots_removed.replace(',','')
        spaces_removed = commas_removed.replace(' ','')
        if spaces_removed.isdecimal():
            uid = int(spaces_removed)
        else:
            integer = False
            uid = number
        return integer, uid

    def Rearrange_input_row(self, idea_col_in, in_row, source_ids, loc_default_row):
        ''' Rearrange values in in_row into db_row
            conform the destination column ids specified in source_id_dict.
            Missing values are loaded with local default values,
            possibly from an in_row with default values.
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
                    #print('source_id', source_id, source_ids.index(source_id),
                    #      in_row[source_ids.index(source_id)])
                if source_id in \
                   set([69, 71, 5, 2, 72, 19, 1, 60, 85, 74, 15, 66, \
                        76, 70, 67, 11, 6, 78, 53, 50]):
                    uid, integer = Convert_numeric_to_integer(in_row[source_ids.index(source_id)])
                    value = str(uid)
##                    if integer is False and value != '':
##                        print('Warning Idea {}: UID <{}> in column {} is not a whole number'.\
##                              format(in_row[idea_col_in], in_row[source_ids.index(source_id)], \
##                                     source_id))
                else:
                    value = in_row[source_ids.index(source_id)]
                db_row[self.source_id_dict[source_id]] = value

                # Index for UID of UoM, successorUID, appContUID and collUID are optional
                if source_id in [2, 1, 60, 15]:
                    if idea_col_in != 0 and value == '':
                        Message(self.gel_net.GUI_lang_index,
                            'Idea {} - UID in column {} is missing'.\
                            format(in_row[idea_col_in], source_id),\
                            'Idee {} - UID in kolom {} ontbreekt'.\
                            format(in_row[idea_col_in], source_id))
        #if self.test == True:
        #    print('db_row', db_row)
        #self.test = False
        return db_row

    def Verify_row(self, db_row):
        ''' Verify values in db_row and amend where applicable,
            before loading in semantic network.
            Per rel_type and kind first role and kind of second role
            add/verify kind of role players.
            Collect rows in expressions table.
        '''
        correct = True

        # Collect used languages that denote language of left hand objects
        # Verify consistency of language names.
        lang_uid = db_row[lang_uid_col]
        if lang_uid != '':
            # If the modeling language of the current file is Dutch
            # then lang_uid and name must be in or added to lang_dict_NL
            if self.lang_ind == 1:
                if lang_uid not in self.gel_net.lang_dict_NL:
                   self.gel_net.lang_dict_NL[lang_uid] = db_row[lang_name_col]
                try:
                    if db_row[lang_name_col] == self.gel_net.lang_dict_NL[lang_uid]:
                        pass
                except KeyError:
                    Message(self.gel_net.GUI_lang_index,
                        'The name of the language {} does not correspond '
                        'with an earlier name {} for UID {}'.\
                        format(db_row[lang_name_col], \
                               self.gel_net.lang_dict_NL[lang_uid], lang_uid),\
                        'De naam van de taal {} correspondeert '
                        'niet met eerdere naam {} voor UID {}'.\
                        format(db_row[lang_name_col], \
                               self.gel_net.lang_dict_NL[lang_uid], lang_uid))
            elif self.lang_ind == 0:
                # If the modeling language of the current file is English
                # then lang_uid and name must be in or added to lang_dict_EN
                if lang_uid not in self.gel_net.lang_dict_EN:
                   self.gel_net.lang_dict_EN[lang_uid] = db_row[lang_name_col]
                try:
                    if db_row[lang_name_col] == self.gel_net.lang_dict_EN[lang_uid]:
                        pass
                except KeyError:
                    Message(self.gel_net.GUI_lang_index,
                        'Language name {} does not correspond '
                        'to earlier name {} for UID {}'.\
                        format(db_row[lang_name_col], \
                               self.gel_net.lang_dict_EN[lang_uid], lang_uid),\
                        'Naam van de taal {} correspondeert niet '
                        'met de eerdere naam {} voor UID {}'.\
                        format(db_row[lang_name_col], \
                               self.gel_net.lang_dict_EN[lang_uid], lang_uid))
            else:
                Message(self.gel_net.GUI_lang_index,
                    'Language of file {} is not English or Nederlands'.\
                    format(self.lang_name),\
                    'De taal van file {} is niet English of Nederlands'.\
                    format(self.lang_name))
        else:
            # No lang_uid present: check whether lang_name present
            if db_row[lang_name_col] != '':
                recognized = False
                if self.lang_ind == 1:
                    # Find the lang_uid for a given lang_name in db_row[lang_name_col]
                    for key,value in self.gel_net.lang_dict_NL.items():
                        if db_row[lang_name_col] == value:
                            db_row[lang_uid_col] = key
                            recognized = True
                            continue
                else:
                    for key,value in self.gel_net.lang_dict_EN.items():
                        if db_row[lang_name_col] == value:
                            db_row[lang_uid_col] = key
                            recognized = True
                            continue
                if recognized is False:
                    Message(self.gel_net.GUI_lang_index,
                        'Language name {} not recognized. '
                        'File language added as default'.\
                        format(db_row[lang_name_col]),\
                        'De naam van de taal {} is niet herkend. '
                        'De taal van de file is toegevoegd als default'.\
                        format(db_row[lang_name_col]))
                    db_row[lang_uid_col]  = self.lang_uid
                    db_row[lang_name_col] = self.lang_name
            else:
                # If lang_name also not present, then use self.lang_name
                db_row[lang_uid_col]  = self.lang_uid
                db_row[lang_name_col] = self.lang_name

        # Collect language communities
        # that denote context for unique name of left hand objects
        # And verify consistency of community names.
        comm_uid = db_row[comm_uid_col]
        if comm_uid != '':
            if self.lang_ind == 1:
                if comm_uid not in self.gel_net.comm_dict_NL:
                    self.gel_net.comm_dict_NL[comm_uid] = db_row[comm_name_col]
                if db_row[comm_name_col] != self.gel_net.comm_dict_NL[comm_uid]:
                    Message(self.gel_net.GUI_lang_index,
                        'Language community name {} does not correspond '
                        'to the earlier name {} for UID {}.'.\
                        format(db_row[comm_name_col], \
                               self.gel_net.comm_dict_NL[comm_uid], comm_uid),\
                        'De naam van de taalgemeenschap {} '
                        'correspondeert niet met de eerdere naam {} voor UID {}.'.\
                        format(db_row[comm_name_col], \
                               self.gel_net.comm_dict_NL[comm_uid], comm_uid))
            else:
                if comm_uid not in self.gel_net.comm_dict_EN:
                    self.gel_net.comm_dict_EN[comm_uid] = db_row[comm_name_col]
                if db_row[comm_name_col] != self.gel_net.comm_dict_EN[comm_uid]:
                    Message(self.gel_net.GUI_lang_index,
                        'Language community name {} does not correspond '
                        'to the earlier name {} for UID {}.'.\
                        format(db_row[comm_name_col], \
                               self.gel_net.comm_dict_EN[comm_uid], comm_uid),\
                        'De naam van de taalgemeenschap {} '
                        'correspondeert niet met de eerdere naam {} voor UID {}.'.\
                        format(db_row[comm_name_col], \
                               self.gel_net.comm_dict_NL[comm_uid], comm_uid))

        else:
            # No community_uid present: check whether comm_name present
            if db_row[comm_name_col] != '':
                comm_recognized = False
                # Find the comm_uid for a given comm_name in db_row[comm_name_col]
                if self.lang_ind == 1:
                    for key,value in self.gel_net.comm_dict_NL.items():
                        if db_row[comm_name_col] == value:
                            db_row[comm_uid_col] = key
                            comm_recognized = True
                            continue
                else:
                    for key,value in self.gel_net.comm_dict_EN.items():
                        if db_row[comm_name_col] == value:
                            db_row[comm_uid_col] = key
                            comm_recognized = True
                            continue
                if comm_recognized is False:
                    self.lower_obj_range_uid += 1
                    Message(self.gel_net.GUI_lang_index,
                        'The language community name {} is not yet known. '
                        'A new UID {} and the new name is added.'.\
                        format(db_row[comm_name_col], self.lower_obj_range_uid),\
                        'De naam van de taalgemeenschap {} is nog niet bekend. '
                        'Een nieuwe UID {} en de nieuwe naar zijn toegevoegd.'.\
                        format(db_row[comm_name_col], self.lower_obj_range_uid))
                    db_row[comm_uid_col] = str(self.lower_obj_range_uid)
                    if self.lang_ind == 1:
                        self.gel_net.comm_dict_NL[db_row[comm_uid_col]] = db_row[comm_name_col]
                    else:
                        self.gel_net.comm_dict_EN[db_row[comm_uid_col]] = db_row[comm_name_col]
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
            Message(self.gel_net.GUI_lang_index,
                'The name of the kind of relation {} in idea {} contains leading '
                'and/or trailing spaces, which are removed.'.\
                format(db_row[rel_type_name_col], db_row[idea_uid_col]),\
                'De naam van de soort relatie {} in idee {} bevat begin- '
                "en/of eindspaties. Die zijn verwijderd.".\
                format(db_row[rel_type_name_col], db_row[idea_uid_col]))
            db_row[rel_type_name_col] = stripped_name

        # REL_uid: If rel_type_uid is unknown,
        # then find rel_map = [uid, name, description] from its phrase (name)
        if db_row[rel_type_uid_col] == '' and db_row[rel_type_name_col] != '':
            uid_new, rel_map = self.gel_net.Find_object_by_name(db_row[rel_type_name_col],\
                                                                string_commonality)
            db_row[rel_type_uid_col] = rel_map[0]
            mapping = True
            #print('rel_map:', rel_map)
            if uid_new:
                Message(self.gel_net.GUI_lang_index,
                    'The unknown name of a kind of relation {} in idea {}; '
                    'should be added to the language definition before being used.'.\
                    format(db_row[rel_type_name_col], db_row[idea_uid_col]),\
                    'De onbekende naam van een soort relatie {} in idee {}; zou toegevoegd '
                    'moeten zijn aan de taaldefinitie voordat hij gebruikt wordt.'.\
                    format(db_row[rel_type_name_col], db_row[idea_uid_col]))
        else:
            # rel_map = uid, name, blank
            rel_map = [db_row[rel_type_uid_col], db_row[rel_type_name_col], '']

        # RH_name: Remove leading and/or trailing whitespaces in rh_name if applicable.
        stripped_name = db_row[rh_name_col].strip()
        if stripped_name != db_row[rh_name_col]:
            Message(self.gel_net.GUI_lang_index,
                "The name of the right hand object '{}' in idea {} contains leading "
                "and/or trailing spaces, which are removed.".\
                format(db_row[rh_name_col], db_row[idea_uid_col]),\
                "De naam van het rechter object '{}' in idee {} bevat begin- "
                "en/of eindspaties. Die zijn verwijderd.".\
                format(db_row[rh_name_col], db_row[idea_uid_col]))
            db_row[rh_name_col] = stripped_name

        # RH_uid (in case of alias relation, rel_type_phrase_uid == 6066 is assumed)
        # *** check later ***
        # RH_uid: If rh_uid is unknown,
        # then find rh_map = [uid, name, description] from its name
        if db_row[rh_uid_col] == '' and db_row[rh_name_col] != '':
            uid_new, rh_map = self.gel_net.Find_object_by_name(db_row[rh_name_col], \
                                                               string_commonality)
            db_row[rh_uid_col] = rh_map[0]
            mapping = True
            #print('rh_map :', rh_map)
        else:
            rh_map = [db_row[rh_uid_col], db_row[rh_name_col], '']

        # LH_name: Remove leading and/or trailing whitespaces in lh_name if applicable.
        stripped_name = db_row[lh_name_col].strip()
        if stripped_name != db_row[lh_name_col]:
            Message(self.gel_net.GUI_lang_index,
                "The name of the left hand object '{}' in idea {} contains leading "
                "and/or trailing spaces, which are removed.".\
                format(db_row[lh_name_col], db_row[idea_uid_col]),\
                "De naam van het linker object '{}' in idee {} bevat begin- "
                "en/of eindspaties. Die zijn verwijderd.".\
                format(db_row[lh_name_col], db_row[idea_uid_col]))
            db_row[lh_name_col] = stripped_name

        # LH_uid: check after rel and rh, because in case of alias lh_uid = rh_uid
        # If lh_uid == '' but name is given, then determine uid from name in dictionary
        if db_row[lh_uid_col] == '' and db_row[lh_name_col] != '':
            new_name = False
            # If alias relation type lh uid = rh uid
            if db_row[rel_type_uid_col] in self.gel_net.alias_uids:
                db_row[lh_uid_col] = db_row[rh_uid_col]
                lh_map = [db_row[lh_uid_col], db_row[lh_name_col], '']
                new_name = True
            else:
                # Not an alias relation:
                # Find lh_map = [uid, name, description]
                new_name, lh_map = self.gel_net.Find_object_by_name(db_row[lh_name_col], \
                                                                    string_commonality)
                db_row[lh_uid_col] = lh_map[0]
                new_name = True
            #print('lh_map :', lh_map)
            if new_name:
                # Add unknown name to the dictionary
                name_in_context = (db_row[lang_uid_col], db_row[comm_uid_col], db_row[lh_name_col])
                value_triple = (db_row[lh_uid_col], '5117', db_row[part_def_col])
                self.gel_net.dictionary[name_in_context] = value_triple
        else:
            # lh_uid is known
            # If alias relation type, then check whether indeed lh_uid == rh_uid
            if db_row[rel_type_uid_col] in self.gel_net.alias_uids:
                if db_row[lh_uid_col] != db_row[lh_uid_col]:
                    Message(self.gel_net.GUI_lang_index,
                        'The alias relation of idea {} requires '
                        'that the uid of the left hand object {} '
                        'is equal to the uid of the right hand object {}'.\
                        format(db_row[idea_uid_col], db_row[lh_uid_col], db_row[rh_uid_col]),\
                        'De alias relatie van idee {} vereist '
                        'dat de uid van het linker object {} '
                        'gelijk is aan de uid van het rechter object {}'.\
                        format(db_row[idea_uid_col], db_row[lh_uid_col], db_row[rh_uid_col]))
            lh_map = [db_row[lh_uid_col], db_row[lh_name_col], db_row[part_def_col]]

        # UOM
        if db_row[uom_uid_col] == '' and db_row[uom_name_col] != '':
            # find uom_map = [uid, name, description] via name of uom
            new_name, uom_map = self.gel_net.Find_object_by_name(db_row[uom_name_col], \
                                                                 string_commonality)
            if new_name:
                Message(self.gel_net.GUI_lang_index,
                    'The name of the unit of measure <{}> in idea {} is unknown.'.\
                    format(db_row[uom_name_col], db_row[idea_uid_col]),\
                    'De naam van de eenheid <{}> in idee {} is onbekend.'.\
                    format(db_row[uom_name_col], db_row[idea_uid_col]))

        # If comm_uid and name still unknown, then use defaults
        if db_row[comm_uid_col] == '':
            # If comm_uid still unknown, then use default self.comm_uid and name
            db_row[comm_uid_col]  = self.comm_uid
            db_row[comm_name_col] = self.comm_name

##            # Prepare an interpretation in the expressions table
##            db_row[lh_uid_col]        = lh_map[0]
##            db_row[lh_name_col]       = lh_map[1]
##            db_row[rel_type_uid_col]  = rel_map[0]
##            db_row[rel_type_name_col] = rel_map[1]
##            db_row[rh_uid_col]        = rh_map[0]
##            db_row[rh_name_col]       = rh_map[1]
##            db_row[uom_uid_col]       = uom_map[0]
##            db_row[uom_name_col]      = uom_map[1]
        if self.content_type == 'queries':
            db_row[intent_uid_col] = '790665'
            if self.lang_ind == 1:
                db_row[intent_name_col] = 'vraag'
            else:
                db_row[intent_name_col] = 'question'

            query_line = [lh_map[0], lh_map[1], rel_map[0], rel_map[1], rh_map[0], rh_map[1],
                          uom_map[0], uom_map[1]]
            self.query_lines.append(query_line)

        # Verify whether the relation type UID is known in the current language definition:
        rel_type_uid = db_row[rel_type_uid_col]
        if rel_type_uid not in self.gel_net.rel_type_uids:
            Message(self.gel_net.GUI_lang_index,
                "The kind of relation ({}) '{}' is not (yet) defined "
                "as a binary relation. The idea {} is ignored.".\
                format(rel_type_uid, db_row[rel_type_name_col], db_row[idea_uid_col]),\
                "De soort relatie ({}) '{}' is (nog) niet gedefinieerd "
                "als een binaire relatie. Idee {} is genegeerd.".\
                format(rel_type_uid, db_row[rel_type_name_col], db_row[idea_uid_col]))
            db_row[rel_type_uid_col] = '5935' # binary relation
            correct = False

        # Collect base_phrases and inverse_phrases in list of totals
        elif db_row[rel_type_uid_col] == '6066':
            if db_row[lh_name_col] not in self.gel_net.total_base_phrases:
                self.gel_net.total_base_phrases.append(db_row[lh_name_col])
##            else:
##                # Boot base phrases will always be reported as duplicates
##                print('Duplicate base phrase <{}>, Idea {}'.\
##                      format(db_row[lh_name_col], db_row[idea_uid_col]))
        elif db_row[rel_type_uid_col] == '1986':
            if db_row[lh_name_col] not in self.gel_net.total_inverse_phrases:
                self.gel_net.total_inverse_phrases.append(db_row[lh_name_col])
##            else:
##                print('Duplicate inverse phrase <{}>, Idea {}'.\
##                      format(db_row[lh_name_col], db_row[idea_uid_col]))
        
        # If phrase_type == 0 (unknown) then determine the phrase type;
        # base_phrase_type_uid = 6066 inverse_phrase_type_uid = 1986.
        # In case of the base ontology, where only bootstrapping relations may be present,
        # the total_base_phrases are the collection of bootstrapping phrases (EN + NL):
        # boot_base_phrases and total_inverse_phrases are the initial boot_inverse_phrases.
        elif db_row[phrase_type_uid_col] == '':
            if db_row[rel_type_name_col] in self.gel_net.total_base_phrases:
                db_row[phrase_type_uid_col] = '6066'
            elif db_row[rel_type_name_col] in self.gel_net.total_inverse_phrases:
                db_row[phrase_type_uid_col] = '1986'
            else:
                Message(self.gel_net.GUI_lang_index,
                    "Phrase <{}> ({}) not yet defined. Idea {} ignored".\
                    format(db_row[rel_type_name_col], db_row[rel_type_uid_col], \
                           db_row[idea_uid_col]),\
                    "Frase <{}> ({}) is nog niet gedefinieerd. Idee {} is genegeerd.".\
                    format(db_row[rel_type_name_col], db_row[rel_type_uid_col], \
                           db_row[idea_uid_col]))
                correct = False

        # If partial_definition known, then delete full_definition.
        if db_row[part_def_col] != '':
            db_row[full_def_col] = ''
##        else:
##            db_row[part_def_col] = db_row[full_def_col]
##            db_row[full_def_col] = ''

        # if for specialization relations lh and rh kinds of roles are missing,
        # load them with defaults
        if correct and db_row[rel_type_uid_col] in ['1146']:
            if db_row[lh_role_uid_col]  == '':
                  db_row[lh_role_uid_col]  = subtypeRoleUID
            if db_row[lh_role_name_col] == '':
                  db_row[lh_role_name_col] = subtypeName[self.lang_ind]
            if db_row[rh_role_uid_col]  == '':
                  db_row[rh_role_uid_col]  = supertypeRoleUID
            if db_row[rh_role_name_col] == '':
                  db_row[rh_role_name_col] = supertypeName[self.lang_ind]

        # Store row in self.expressions
        if correct:
            self.expressions.append(db_row[:])
        return correct, db_row
#----------------------------------------------------
if __name__ == "__main__":

    from SemanticNetwork import Semantic_Network

    # Create semantic network
    gel_net = Semantic_Network("Network")
    
    # Create a base dictionary of kinds of relations from bootstrapping
    gel_net.Create_base_reltype_objects()
    
    path_and_name = '..\\GellishDictionary/Formal language definition base-UTF-8.csv'
    current_file = Gellish_file(path_and_name, gel_net)

    # Read base ontology
    current_file.Import_Gellish_from_file()

    subject_name = 'test'
    lang_name = 'Nederlands'

    serialization = 'csv'
    Open_output_file(current_file.expressions, subject_name, lang_name, serialization)

    serialization = 'xml'
    Open_output_file(current_file.expressions, subject_name, lang_name, serialization)

    serialization = 'n3'
    Open_output_file(current_file.expressions, subject_name, lang_name, serialization)

    serialization = 'json'
    Open_output_file(current_file.expressions, subject_name, lang_name, serialization)
