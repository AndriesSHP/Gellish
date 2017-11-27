#!/usr/bin/python3
import sys
import os
import csv
import sqlite3
import pickle
from tkinter import *
from tkinter.ttk import *

from Expr_Table_Def import *
from Anything import Anything, Object, Individual, Kind, Relation, RelationType
from Bootstrapping import *
from GellishDict import GellishDict
from ModelViews import Display_views
from Create_output_file import Create_gellish_expression, Convert_numeric_to_integer, Open_output_file

class Semantic_Network():
    """ Create a Semantic_Network model (called net_name) from a Gellish database (db_name).
        Gel_dict = naming dictionary that is extended by the concepts and names in the network.
        The model contains things and their relations.
        Start initially with bootstrapping base relation types,
              base_phrases being bootstrapping base phrases
              and inverse_phrases being bootstrapping inverse phrases
    """
    def __init__(self, net_name, user):
        self.name          = net_name
        self.user          = user
        self.rels          = []
        self.idea_uids     = []
        self.rel_types     = [] # initialize and collect all binary relation types
                                # (being 'binary relation' and its subtypes)
        self.rel_type_uids = base_rel_type_uids
        self.uid_dict  = {}     # key = uid; value = obj (an instance of Anything)
        self.objects       = []
        #self.object_uids   = []
        self.rh_objects    = []
        self.languages     = []
        # A dictionary for names in a context that refers to the denoted concepts
        self.dictionary      = GellishDict('Dictionary of Gellish formal languages')
        self.GUI_lang_name_dict   = {"English":'910036', "Nederlands":'910037'}
        self.reply_lang_name_dict = {'English':'910036', 'Nederlands':'910037', 'American':'911689', \
                                     'Chinese':'911876', 'Deutsch'   :'910038', 'Francais':'910039'}
        self.lang_uid_dict   = {} #{910036: "English", 910037: "Nederlands" , 589211: "international"}
        self.community_dict  = {} #{492015: "Formal English", 492016: "Formeel Nederlands", \
                                  # 492014: "Gellish", 589830: "Gellish alternative"}
        self.lang_dict_EN    = {'910036': "English", '910037': "Dutch"     , '589211': "international",\
                                '910038': "German" , '910039': "French"    , '911689': "American"}
        self.lang_dict_NL    = {'910036': "Engels" , '910037': "Nederlands", '589211': "internationaal",\
                                '910038': "Duits"  , '910039': "Frans"     , '911689': "Amerikaans"}
        self.comm_dict_EN    = {'492014': "Gellish"}
        self.comm_dict_NL    = {'492014': "Gellish"}
        self.GUI_lang_pref_uids = []
        self.reply_lang_pref_uids  = []
        self.comm_pref_uids  = ['492014'] # Default: 'Gellish'
        self.base_phrases    = boot_base_phrasesEN    + boot_base_phrasesNL
        self.inverse_phrases = boot_inverse_phrasesEN + boot_inverse_phrasesNL
        self.specialRelUIDs  = ['1146']   # 1146 base UID for 'is a kind of'
        self.classifUIDs     = []       # 1225 base UID for 'is classified as a'
        self.subComposUIDs   = []
        self.subConcComposUIDs = []
        #self.names_in_contexts = [] # list of [lang_uid, comm_uid, name, naming_rel_uid, description]
        self.alias_uids      = boot_alias_uids
        #self.allBinRel_types = [] # initialize and collect all binary relation types
                                # (being 'binary relation' and its subtypes)
        self.unknown_quid = 0   # start UID for unknowns in queries
        self.new_obj_uid = 100  # default start UID for new things in model mappings
        self.new_things  = {}   # collection of new things in model mappings
        self.new_rel_uid = 500  # default start UID for unknown relations in model mappings
        self.select_dict = {}
        self.unknowns    = []   # The list(s) unkown objects that are denoted by an unknown in a query
        self.names_of_unknowns   = []
        self.unknown_kind        = ['unknown kind' ,'onbekende soort']
        self.base_ontology = False

        self.lh_options  = [] 
        self.rel_options = []
        self.rh_options  = []
        self.ex_candids  = []

        # Set default terms for query in user interface
        #term_list = [row[i] for row in namingTable for i in range(2,3)]
        self.lh_terms     = ['elektriciteitskabel', '3 aderige kabel', 'YMvK kabel', 'breedte', 'materiaal','isolatieplaat']
        self.lh_terms.sort()
        self.rel_terms = ['is een soort', 'kan als aspect hebben een', 'moet als aspect hebben een',\
                          'heeft per definitie als aspect een', 'heeft per definitie een schaalwaarde gelijk aan',\
                          'heeft per definitie een schaalwaarde kleiner dan',\
                          'heeft per definitie een schaalwaarde groter dan',\
                          'is per definitie gekwalificeerd als']
        self.rel_terms.sort()
        self.rh_terms  = self.lh_terms[:]
        #self.lh_terms.sort() # lh_terms are already sorted
        self.uoms      = ['m', 'mm', 'bar', 'deg C']
        self.uoms.sort()

        self.uid_name_desc_list = [] # list of [uid, name, description] of candidates for mapping

        self.kind_model   = []
        self.prod_model   = []
        self.query_table  = []
        self.summ_model   = []
        self.summ_objects = []
        self.taxon_model  = []
        self.taxon_objects  = []
        self.possibilities_model = []
##        self.possib_objects = []
        self.indiv_model    = []
        self.indiv_objects  = []
        self.info_model     = []
        self.all_subtypes   = []
        self.occ_model      = []
        self.involv_table   = []
        self.seq_table      = []
        self.part_whole_occs = []

        self.taxon_row    = ['','','','','','','','','','','','','','']
        self.summary_row  = ['','','','','','','','','','','','','','']
        self.possibility_row   = ['','','','','','','','','','','','','','','']
        self.indiv_row    = ['','','','','','','','','','','','','','','']
        self.occ_row      = ['','','','','','','','','','','','','','']
        self.taxon_aspect_uids   = ['','','','']
        self.taxon_column_names  = ['','','','']
        self.taxon_uom_names     = ['','','','']
        self.summ_aspect_uids    = ['','','','']
        self.summ_column_names   = ['','','','']
        self.summ_uom_names      = ['','','','']
        self.possib_aspect_uids  = ['','','','','']
        self.possib_column_names = ['','','','','']
        self.possib_uom_names    = ['','','','','']
        self.indiv_aspect_uids  = ['','','','','']
        self.indiv_column_names = ['','','','','']
        self.indiv_uom_names    = ['','','','','']

        self.occ_aspects  = ['','','','','','','','','','','']
        self.occ_kinds    = ['','','','','','','','','','','']
        self.occ_uoms     = ['','','','','','','','','','','']
        self.nr_of_occurrencies = 0
        self.max_nr_of_rows = 500   # in treeviews

        self.nameless = ['nameless', 'naamloos', '']
        self.categories_of_kinds = ['kind', 'kind of physical object', 'kind of occurrence',\
                                    'kind of aspect'  , 'kind of role', \
                                    'kind of relation', 'qualitative kind']
        self.non_object = Anything('', '')
        self.idea_uid = 211000000
        self.classification = ['is classified as a', 'is geclassificeerd als een']
        self.test = False

    def Set_GUI_Language(self, GUI_lang):
        '''Set the GUI language of the user'''
        if GUI_lang in self.GUI_lang_name_dict:
            self.GUI_lang_name = GUI_lang
            self.GUI_lang_uid  = self.GUI_lang_name_dict[GUI_lang]
            if GUI_lang == 'Nederlands':
                self.GUI_lang_index = 1
            else:
                self.GUI_lang_index = 0
            GUI_set = True
            if self.GUI_lang_uid == '910036':
                # Set default GUI_preferences at international, English, American
                self.GUI_lang_pref_uids = ['589211', '910036', '911689']
            elif self.GUI_lang_uid == '910037':
                # Set default preferences at international, Dutch, English
                self.GUI_lang_pref_uids = ['589211', '910037', '910036']
            else:
                # Set default preferences at international, user_language, English
                self.GUI_lang_pref_uids = ['589211', self.GUI_lang_uid, '910036']
        else:
            print('GUI language %s unknown. Default = English.' % (GUI_lang))
            GUI_set = False
        return GUI_set

    def Set_reply_language(self, reply_lang_name):
        '''Set the reply language for display of the user views'''
        if reply_lang_name in self.reply_lang_name_dict:
            self.reply_lang_name = reply_lang_name
            self.reply_lang_uid  = self.reply_lang_name_dict[reply_lang_name]
            if self.reply_lang_uid == '910036':
                # Set default preferences at international, English, American
                self.reply_lang_pref_uids = ['589211', '910036', '911689']
            elif self.reply_lang_uid == '910037':
                # Set default preferences at international, Dutch, English
                self.reply_lang_pref_uids = ['589211', '910037', '910036']
            else:
                # Set default preferences at international, user_language, English
                self.reply_lang_pref_uids = ['589211', self.reply_lang_uid, '910036']
        else:
            print('Reply language %s unknown. Default = English.' % (reply_lang_name))
            self.reply_lang_name = 'English'
            self.reply_lang_uid  = '910037'

    def Create_base_reltype_objects(self):
        '''Create relation_type objects conform Bootstrapping base_rel_type_uids'''
        for rel_type_uid in base_rel_type_uids:
            rel_type_name = base_rel_type_uids[rel_type_uid]
            rel_type = RelationType(rel_type_uid, rel_type_name)
            self.rel_types.append(rel_type)
            self.uid_dict[rel_type_uid] = rel_type
            #self.object_uids.append(rel_type_uid)
    
    def Build_Base_Semantic_Network(self): #, db_cursor):
        ''' Build a Semantic Network from 'base_ontology' table,
            primarily to add defined kinds of relations to list(rel_type_uids).
            Then complete and verify base semantic network
        '''
##        # Add basic_ontology table from database to the semantic network net_name
##        table = 'base_ontology'
##        self.Add_table_content_to_network(db_cursor, table)

        # Complete and Verify base semantic network
        # Determine all subtypes of binary relation (5935)
        # and first_roles and second_roles and role players for all subtypes of binary relation
        # thus extending the list of kinds of relations, base phrases and inverse phrases
        
        kind_rel    = self.uid_dict[binRelUID]
        kind_rel.category = 'kind of relation' # Denoting binary relation
        # Determine list of subtypes of binary relation (5935)
        # and specify their self.category as 'kind of relation'
        # and determine their first and second kind of role (self.first_role and self.second_role)
        self.rel_types, self.rel_type_uids = self.DetermineSubtypeList(binRelUID) 
        print('  Base network: {}; nr of objects = {}; nr of rels = {}; nr of rel_type_uids = {}'.\
              format(self.name, len(self.objects), len(self.rels), len(self.rel_type_uids)))

        # Check whether each concept has at least one supertype concept.
        for obj in self.objects:
            if obj.category in ['kind', 'kind of physical object', 'kind of occurrence', 'kind of aspect', \
                                'kind of role', 'kind of relation']:
                if len(obj.supertypes) == 0:
                    print('Kind ({}) {} has no supertype(s).'.format(obj.uid, obj.name))

        # Determine lists of various kinds and their subtypes
        self.BuildHierarchies()

        # Add kinds of roles
        # Add kinds of role_players to kinds of binary relations because of relation types
        for rel_type in self.rel_types:
##            self.Determine_inherited_kind_of_role(rel_type)
            rel_type.role_players_types, rel_type.role_player_type_lh, rel_type.role_player_type_rh \
                                         = self.Determine_role_players_types(rel_type.uid)

##    def Determine_inherited_kind_of_role(self, kind_of_relaton):
##        ''' Given the kind of relation object
##            verify whether it has a first and second kind of role,
##            if not, then determine the kind of role that is inherited
##            from its nearest supertype kind of relation
##        '''
##        kinds = []
##        if kind_of_relaton.first_role.name == '': #'relator':
##            for supertype in kind_of_relaton.supertypes:
##                if supertype.first_role:
##                    kind_of_relaton.first_role = supertype.first_role
##                    print('kind_of_relaton', kind_of_relaton.name, kind_of_relaton.first_role.name)
##                    break
##                else:
##                    kinds.append(supertype)
##            if not kind_of_relaton.first_role:
##                for kind in kinds:
##                    for supertype_1 in kind.supertypes:
##                        if supertype_1.first_role:
##                            kind_of_relaton.first_role = supertype_1.first_role
##                            print('kind_of_relaton-1', kind_of_relaton.name, kind_of_relaton.first_role.name)
##                            break
##                        else:
##                            kinds.append(supertype_1)
##                    if kind_of_relaton.first_role:
##                        break
##                if not kind_of_relaton.first_role:
##                    print('No supertype of <{}> ({}) found'.format(kind_of_relaton.name, kind_of_relaton.uid))
##
##        else:
##            print('First role:', kind_of_relaton.name, kind_of_relaton.uid, kind_of_relaton.first_role.name)
##
##        #if not kind_of_relaton.second_role:
        
        self.base_ontology = True
    
    def Extent_Semantic_Network(self): #, db_cursor):
        '''Build a Semantic Network from database db_cursor'''

        # Extent network by reading domain dictionaries table from DB content
        table = 'domain_dictionaries'
        self.Add_table_content_to_network(db_cursor, table)
        print('  Extended network: {}; nr of objects = {}; nr of rels = {}; nr of rel_type_uids = {}'.\
              format(self.name, len(self.objects), len(self.rels), len(self.rel_type_uids)))
        
        # Extent network by reading product and process table from DB content
        table = 'productsANDprocesses'
        self.Add_table_content_to_network(db_cursor, table)
        print('  Including product network: {}; nr of objects = {}; nr of rels = {}; nr of rel_type_uids = {}'.\
              format(self.name, len(self.objects), len(self.rels), len(self.rel_type_uids)))

    def Add_table_content_to_network(self, db_cursor, table):
        '''The content of a 'table' in Gel_db database is added to the Semantic Network
           and the new names_in_context are added to the network.dictionary.
        '''
        #db_cursor.execute("select name from sqlite_master where type='table';")
        #print("Tables:", db_cursor.fetchall())
        
        # read an expressions table
        command = 'select * from ' + table
        print("  Read table '{}' from database.".format(table))
        db_cursor.execute(command)
        rows = db_cursor.fetchall()
        #print('rows:',len(rows))
        
        # Add each row to the semantic network
        for row in rows:
            self.Add_row_to_network(row)

        self.Verify_rh_objects()

    def Verify_rh_objects(self):

        lang_uid = English_uid   # English
        comm_uid = '492014'           # Gellish
        description = ''
        
        # Verify whether all rh_objects are defined as (lh_)objects
        if len(self.rh_objects) > 0:
            for obj in self.rh_objects:
                # If obj is not defined and it is not 'anything' and not a whole number then display a warning
                if obj.defined == False and obj.uid != anythingUID:
                    int_obj_uid, integer = Convert_numeric_to_integer(obj.uid)
                    if integer == True and (int_obj_uid < 1000000000 or int_obj_uid > 3000000000):
                        self.user.Message(
                            'Warning: RH object {} ({}) is not yet defined'           .format(obj.name, obj.uid),\
                            'Waarschuwing: RH object {} ({}) is nog niet gedefinieerd'.format(obj.name, obj.uid))
                        # Add provisional data to semi-defined rh_object
                        obj.defined = True
                        anything = self.uid_dict[anythingUID]
                        obj.kind = anything
                        #self.object_uids.append(obj.uid)
                        # Create a name in context with description and add to object and dictionary
                        self.Add_name_in_context(lang_uid, comm_uid, obj.name, is_called_uid, description)
                    else:
                        # obj is a number
                        obj.category = 'number'
                else:
                    # The object has been defined later than discovered as rh_object
                    if len(obj.candidate_names) > 0:
                        for cand_name in obj.candidate_names:
                            # Verify whether rh_name is included in rh.names_in_contexts
                            rh_name_found = False
                            if len(obj.names_in_contexts) > 0:
                                for name_in_context in obj.names_in_contexts:
                                    if cand_name == name_in_context[2]:
                                        rh_name_found = True
                                        continue
                            else:
                                print("Error: no name in context given for {}".format(cand_name))

                            # If no rh_name is found and obj.uid does not denote an integer number then report warning
                            int_obj_uid, integer = Convert_numeric_to_integer(obj.uid)
                            if rh_name_found == False and obj.uid != anythingUID and \
                               (integer == False or (int_obj_uid < 1000000000 or int_obj_uid > 3000000000)):
                                print("Warning: rh_name '{}' ({}) not known for uid '{}'. Correct or add a synonym.".\
                                      format(cand_name, obj.uid, obj.names_in_contexts[0][2]))
                                # Create a name in context with description and add to object and dictionary
                                self.Add_name_in_context(lang_uid, comm_uid, cand_name, is_called_uid, description)
                    
                        obj.candidate_names[:] = []
            
                self.rh_objects.remove(obj)
##        if len(self.rh_objects) > 0:
##            for obj in self.rh_objects:
##                print('To be defined: ', obj.name)

    def Add_name_in_context(self, lang_uid, comm_uid, name, naming_uid, description):
        ''' Create a name in context with description and add to object and dictionary'''
        name_and_descr = (lang_uid, comm_uid, name, naming_uid, description)
        name_in_context = (lang_uid, comm_uid, name)
        if name_and_descr not in obj.names_in_contexts:
            obj.names_in_contexts.append(name_and_descr)
        if name_in_context not in self.dictionary:
            value_triple = (obj.uid, naming_uid, description)
            self.dictionary[name_in_context] = value_triple

    def Add_row_to_network(self, row, names_and_descriptions):
        '''Add a row (that contains an expression) to the network.'''
        # take the uids and names from row
        idea_uid  = row[idea_uid_col]
        lang_uid  = row[lang_uid_col]
        comm_uid  = row[comm_uid_col]
        intent_uid  = row[intent_uid_col]

        lh_uid, lh_name = row[lh_uid_col], row[lh_name_col]
        if lh_name == '':
            
            if lang_uid == Dutch_uid:
                lh_name = self.nameless[1]
            else:
                lh_name = self.nameless[0]
        rh_uid, rh_name = row[rh_uid_col], row[rh_name_col]
        if rh_name == '':
            if lang_uid == Dutch_uid:
                rh_name = self.nameless[1]
            else:
                rh_name = self.nameless[0]
        rel_type_uid, rel_type_name = row[rel_type_uid_col], row[rel_type_name_col]
        phrase_type_uid = row[phrase_type_uid_col]
        description     = row[part_def_col]
        uom_uid, uom_name = row[uom_uid_col], row[uom_name_col]

        # collect used languages for naming left hand objects in dict. (for use by preferences)
        if lang_uid not in self.lang_uid_dict:
           self.lang_uid_dict[lang_uid] = row[lang_name_col]
           if lang_uid not in self.uid_dict:
               lang = Anything(lang_uid, row[lang_name_col])
               lang.defined = False
               #self.object_uids.append(lang_uid)
               self.objects.append(lang)
               self.uid_dict[lang_uid] = lang
           # Add language object to list of rh_objects for later verification of the presence of a definition
           self.rh_objects.append(lang)

        # Collect language communities for naming left hand objects in dict. (for use by preferences)
        if comm_uid not in self.community_dict:
            self.community_dict[comm_uid] = row[comm_name_col]
            if comm_uid not in self.uid_dict:
                comm = Anything(comm_uid, row[comm_name_col])
                comm.defined = False
                comm.candidate_names.append(row[comm_name_col])
                #self.object_uids.append(comm_uid)
                self.objects.append(comm)
                self.uid_dict[comm_uid] = comm
                # Add comm to list of rh_objects for later verification of the presence of a definition
                self.rh_objects.append(comm)

        # Create the left hand object if it does not exist and add to naming_table dictionary
        if lh_uid not in self.uid_dict: 
            if lh_name in self.nameless:  # ['nameless', 'naamloos', '']
                ind = 0
                if lang_uid == Dutch_uid:
                    ind = 1
                lh_name = self.nameless[ind] + '-' + str(lh_uid)
            # Create new (lh) object
            lh = Anything(lh_uid, lh_name)
            #self.object_uids.append(lh_uid)
            self.objects.append(lh)
            self.uid_dict[lh_uid] = lh
            if rel_type_uid in self.alias_uids:
                naming_uid = rel_type_uid
            else:
                naming_uid = is_called_uid
                
            # Add name and description to object list of names_in_contexts
            lh_name_and_descr = (lang_uid, comm_uid, lh_name, naming_uid, description)
            if rel_type_uid in self.specialRelUIDs or rel_type_uid in self.classifUIDs:
                lh.defined = True
                lh.names_in_contexts.append(lh_name_and_descr)
            elif rel_type_uid in self.alias_uids:
                lh.names_in_contexts.append(lh_name_and_descr)
                
            # If names and descriptions in other languages are available add them as well
            if len(names_and_descriptions) > 0:
                for name_and_description in names_and_descriptions:
                    lh.names_in_contexts.append(name_and_description)
                
            # Add name_in_context to dictionary
            lh_name_in_context = (lang_uid, comm_uid, lh_name)
            if lh_name_in_context not in self.dictionary:
                value_triple = (lh_uid, naming_uid, description)
                #print('Dict entry: ', lh_name_in_context, value_triple)
                self.dictionary[lh_name_in_context] = value_triple
            
        else:
            # lh_uid is known, thus find the existing lh object from its uid in uid_dict. 
            lh = self.uid_dict[lh_uid]
            #print('lh2.name, kind:', lh.name, lh.kind)
            # If existing lh.name is 'nameless', but new lh_name is given,
            #    then insert name_and_descr and change the name from nameless into the given name
            ind = 0
            if lang_uid == Dutch_uid:
                ind = 1
            if lh.name == self.nameless[ind] + '-' + str(lh_uid) and\
               lh_name not in self.nameless:
                lh_name_and_descr = (lang_uid, comm_uid, lh_name, is_called_uid, description)
                lh.names_in_contexts.insert(0, lh_name_and_descr)
                lh.name = lh_name
            
            # If rel_type is een alias relation, then add name_in_context to object and to dict
            if rel_type_uid in self.alias_uids:
                if lh_name not in self.nameless:
                    naming_uid = rel_type_uid
                    lh_name_and_descr = (lang_uid, comm_uid, lh_name, naming_uid, description)
                    lh.names_in_contexts.append(lh_name_and_descr)
                    lh_name_in_context = (lang_uid, comm_uid, lh_name)
                    if lh_name_in_context not in self.dictionary:
                        value_triple = (lh_uid, rel_type_uid, description)
                        self.dictionary[lh_name_in_context] = value_triple
                # If alias names and descriptions in other languages are available add them as well
                if len(names_and_descriptions) > 0:
                    for name_and_description in names_and_descriptions:
                        lh.names_in_contexts.append(name_and_description)
                        
            # If rel_type is a subtyping relation then add a name_in_context to dict
            elif rel_type_uid in self.specialRelUIDs or rel_type_uid in self.classifUIDs:
                #print('Definition of existing object', lh.name)
                naming_uid = is_called_uid
                lh.defined = True
                lh_name_and_descr = (lang_uid, comm_uid, lh_name, naming_uid, description)
                lh_name_in_context = (lang_uid, comm_uid, lh_name)
                if lh_name_and_descr not in lh.names_in_contexts:
                    lh.names_in_contexts.append(lh_name_and_descr)
                if lh_name_in_context not in self.dictionary:
                    value_triple = (lh_uid, naming_uid, description)
                    #print('Dict entry: ', lh_name_in_context, value_triple)
                    self.dictionary[lh_name_in_context] = value_triple
                # If names and descriptions in other languages are available add them as well
                if len(names_and_descriptions) > 0:
                    for name_and_description in names_and_descriptions:
                        lh.names_in_contexts.append(name_and_description)

        # If rh object does not exist yet, then create an object with a name
        # and with a temporary name for later verification,
        # but without a name_in_context and without a description and defined = False
        if rh_uid not in self.uid_dict:
            #  Create new (rh) object
            rh = Anything(rh_uid, rh_name)
            rh.defined = False
            rh.candidate_names.append(rh_name)
            #self.object_uids.append(rh_uid)
            self.objects.append(rh)
            self.uid_dict[rh_uid] = rh
            # Add rh to list of rh_objects for later verification of the presence of a definition
            self.rh_objects.append(rh)

        # rh object is known
        else:
            # Find rh object in the uid dictionary
            rh = self.uid_dict[rh_uid]
            # If rh_name is still unknown, then collect the rh_names for future reference
            # Verify whether rh_name is included in rh.names_in_contexts
            existing_name = False
            for name_in_context in rh.names_in_contexts:
                if rh_name == name_in_context[2]:
                    existing_name = True
            if existing_name == False:
                if rh_name not in rh.candidate_names:
                    rh.candidate_names.append(rh_name)
                    self.rh_objects.append(rh)

        # UOM
        # Verify existence of unit of measure
        if uom_uid != '' and uom_uid != '0':
            if uom_uid not in self.uid_dict:
                print('Unit of measure {} ({}) is not yet known'.format(uom_name, uom_uid))
                uom = Anything(uom_uid, uom_name)
                uom.defined = False
                uom.candidate_names.append(uom_name)
                #self.object_uids.append(uom_uid)
                self.objects.append(uom)
                self.uid_dict[uom_uid] = uom
                # Add uom to list of rh_objects for later verification of the presence of a definition
                self.rh_objects.append(uom)
            else:
                # Find uom in the uid dictionary
                uom = self.uid_dict[uom_uid]
        else:
            # Equality of 'none' object (with uid == '')
            uom = self.non_object
                
        # Rel
        # Create a relation object (with uid = idea_uid)
        # and add the relation between objects to both objects, except when lh == rh
        if rh_uid != lh_uid:
            rel_type = self.uid_dict[rel_type_uid]

            # If base_ontology is created, then kinds of relations have kinds of roles
            if self.base_ontology == True:
                # If no lh or rh kinds of roles are given then allocate kind of role
                # conform first and second role of kind of relation
                if row[lh_role_uid_col] == '':
                    if phrase_type_uid == basePhraseUID: 
                        row[lh_role_uid_col] = rel_type.first_role.uid
                        row[lh_role_name_col] = rel_type.first_role.name
                    else:
                        row[lh_role_uid_col] = rel_type.second_role.uid
                        row[lh_role_name_col] = rel_type.second_role.name
                if row[rh_role_uid_col] == '':
                    if phrase_type_uid == basePhraseUID:
                        row[rh_role_uid_col] = rel_type.second_role.uid
                        row[rh_role_name_col] = rel_type.second_role.name
                    else:
                        row[rh_role_uid_col] = rel_type.first_role.uid
                        row[rh_role_name_col] = rel_type.first_role.name
                
            # Default: category == None
            relation = Relation(lh, rel_type, rh, phrase_type_uid, uom, row)
##            # Verify whether phrase corresponds to uid
##            if rel_type_name not in rel_type.basePhrases and rel_type_name not in rel_type.inversePhrases:
##                print('Phrase <{}> does not correspond with UID {}'.format(rel_type_name, rel_type_uid))
            # Add the relation with reled objects (self.obj_1 and self.obj_2) and the self. rel_type object to both objects
            lh.add_relation(relation)
            rh.add_relation(relation)
            
            self.idea_uids.append(idea_uid)
            self.rels.append(relation)

            # Add information to object depending in kind of relation (rel_type_uid)
            
            # If rel_type is a specialization relation (1146 or one of its subtypes),
            # then add subtype and supertype to lh and rh object
            if rel_type_uid in specialRelUIDs:
                if phrase_type_uid == basePhraseUID:
                    lh.name = lh_name
                    lh.add_supertype(rh)
                    lh.kind = lh.supertypes[0]
                    rh.add_subtype(lh)
                    
                    # Set lh object category as 'kind' after check on consistency with earlier categorization
                    if lh.category != 'anything' and lh.category not in self.categories_of_kinds:
                        print ("** Warning: Idea {} Object '{}' category '{}' is inconsistent with earlier categorization as 'kind'.".\
                               format(idea_uid, lh_name, lh.category))
                    else:
                        # lh category is not yet categorized (initially by default set as 'anything')
                        if rh.category == 'anything':
                            lh.category = 'kind'
                            rh.category = 'kind'
                        else:
                            lh.category = rh.category
                # For the inverse
                else:
                    lh.add_subtype(rh)
                    rh.add_supertype(lh)

            # If classification relation (1225 or one of its subtypes), then add classifier and classified to objects
            elif rel_type_uid in self.classifUIDs:
                if phrase_type_uid == basePhraseUID:
                    lh.name = lh_name
                    lh.add_classifier(rh)
                    rh.add_individual(lh)
                    lh.kind = lh.classifiers[0]
                    # Set object category as 'individual' after check on consistency with earlier classification
                    if lh.category != 'anything':
                        if lh.category not in ['individual', 'physical object', 'aspect', 'occurrence', 'role']:
                            print ("Error: Idea {} Object '{}' category '{}' should be 'individual'".\
                                   format(idea_uid, lh_name, lh.category))
                            lh.category = 'individual'
                    else:
                        # lh object category is still the default ('anything') thus make it 'individual'
                        # rh object category should be 'kind' or one of its subtypes
                        lh.category = 'individual'
                        if rh.category == 'anything':
                            rh.category = 'kind'
                        elif rh.category not in ['kind', 'kind of physical object', 'kind of aspect', \
                                                 'kind of occurrence', 'kind of role', 'kind of relation', \
                                                 'number']:
                            print("Error: Idea {} Object '{}' category '{}' should be 'kind'".\
                                  format(idea_uid, rh_name, rh.category))
                            rh.category = 'kind'
                else:
                    lh.add_individual(rh)
                    rh.add_classifier(lh)

            # If part-whole relation (composUID 1260 or concComposUID 1261 or one of their subtypes),
            # then add part to collection of parts of the whole object
            elif rel_type_uid in self.subComposUIDs or rel_type_uid in self.subConcComposUIDs:
                if phrase_type_uid == basePhraseUID:
                    rh.add_part(lh)
                else:
                    lh.add_part(rh)

            # If rel_type_uid == uid of <has by definition as first/second role a> relation
            # then add first/second kind of role to the kind of relation
            elif rel_type_uid == first_role_uid:
                if phrase_type_uid == basePhraseUID:
                    lh.add_first_role(rh)
            elif rel_type_uid == second_role_uid:
                if phrase_type_uid == basePhraseUID:
                    lh.add_second_role(rh)

            # If rel_type_uid == uid of <is by definition a role of a> kind of role player,
            # then add the kind of role_player to the kind of role 
            elif rel_type_uid == by_def_role_of_ind:
                lh.add_role_player(rh)
                if phrase_type_uid == basePhraseUID:
                    # Verify whether lh is indeed a kind of role
                    if lh.category == 'anything':
                        lh.category = 'kind of role'
                    elif lh.category != 'kind of role':
                        print("** Warning: Idea {} object ({}) {} expects being a kind of role and not a {}"\
                              .format(idea_uid, lh.uid, lh.name, lh.category))
        else:
            # lh_uid == rh_uid
            # If rel_type_uid == uid of <is a base phrase for> (6066) name of a kind of relation
            # or rel_type_uid == uid of <is a inverse phrase for> (1986) name of a kind of relation,
            # then add the name in context to the list of base phrases resp. inverse phrase in context for the object
            # and add the name to the list of base_phrases or inverse_phrases
            if rel_type_uid == basePhraseUID:
                phrase_in_context = [lang_uid, comm_uid, lh_name]
                lh.add_base_phrase(phrase_in_context)
                lh.basePhrases.append(lh_name)
                self.base_phrases.append(lh_name)
            elif rel_type_uid == inversePhraseUID:
                phrase_in_context = [lang_uid, comm_uid, lh_name]
                lh.add_inverse_phrase(phrase_in_context)
                lh.inversePhrases.append(lh_name)
                self.inverse_phrases.append(lh_name)

    def BuildHierarchies(self):
        ''' Build lists of subtype concepts and subtype concept_uids of various kinds,
            including the kinds themselves
        '''
        
        # Determine lists of various kinds and their subtypes
        self.sub_classifs,    self.sub_classif_uids    = self.DetermineSubtypeList(classifUID)
        self.subClassifieds,  self.subClassifiedUIDs   = self.DetermineSubtypeList(classifiedUID)
        self.indOrMixRels,    self.indOrMixRelUIDs     = self.DetermineSubtypeList(indOrMixRelUID)
        self.indivBinRels,    self.indivBinRelUIDs     = self.DetermineSubtypeList(indivRelUID)     # 4658 binary relation between individual things
        self.kindHierRels,    self.kindHierRelUIDs     = self.DetermineSubtypeList(kindHierUID)
        self.kindKindRels,    self.kindKindRelUIDs     = self.DetermineSubtypeList(kindKindUID)
        self.kindBinRels,     self.kindBinRelUIDs      = self.DetermineSubtypeList(kindRelUID)
        self.mixedBinRels,    self.mixedBinRelUIDs     = self.DetermineSubtypeList(mixedRelUID)
        self.specialRels,     self.specialRelUIDs      = self.DetermineSubtypeList(specialRelUID)
        self.subtypeSubs,     self.subtypeSubUIDs      = self.DetermineSubtypeList(subtypeRoleUID)  # 3818 UID of 'subtype' (role)
        self.subPossAsps,     self.subPossAspUIDs      = self.DetermineSubtypeList(possAspUID)
        self.subPossessors,   self.subPossessorUIDs    = self.DetermineSubtypeList(possessorUID)
        self.transitiveRel,   self.transitiveRelUIDs   = self.DetermineSubtypeList(transRelUID)
        self.subConcPossAsps, self.subConcPossAspUIDs  = self.DetermineSubtypeList(concPossAspUID)  # 2069
        self.subConcComplRels,self.subConcComplRelUIDs = self.DetermineSubtypeList(concComplRelUID) # 4902
        self.qualSubtypes,    self.qualSubtypeUIDs     = self.DetermineSubtypeList(qualSubtypeUID)  # 4328
        self.qualOptionss,    self.qualOptionsUIDs     = self.DetermineSubtypeList(qualOptionsUID)  # 4848
        self.concCompls,      self.concComplUIDs       = self.DetermineSubtypeList(concComplUID)    # 4951
        self.concQuants,      self.concQuantUIDs       = self.DetermineSubtypeList(concQuantUID)    # 1791
        self.subQuals,        self.subQualUIDs         = self.DetermineSubtypeList(qualifUID)
        self.subQuants,       self.subQuantUIDs        = self.DetermineSubtypeList(quantUID)        # 2044 quantification
        self.subInformatives, self.subInformativeUIDs  = self.DetermineSubtypeList(informativeUID)
        self.subOccurrences,  self.subOccurrenceUIDs   = self.DetermineSubtypeList(occurrenceUID)
        self.subComposs,      self.subComposUIDs       = self.DetermineSubtypeList(composUID)     # composition relation and its subtypes
        self.subCompons,      self.subComponUIDs       = self.DetermineSubtypeList(componUID)     # component role and its subtypes
        self.subConcComposs,  self.subConcComposUIDs   = self.DetermineSubtypeList(concComposUID) # conceptual composition relation and its subtypes
        self.subConcCompons,  self.subConcComponUIDs   = self.DetermineSubtypeList(concComponUID) # conceptual component role and its subtypes
        #self.subInvolveds,    self.subInvolvedUIDs     = self.DetermineSubtypeList(involvedUID)   # 4546 = being a second role in an <involvement in an occurrence> relation
        self.subInvolvs,      self.subInvolvUIDs       = self.DetermineSubtypeList(involvUID)     # 4767 = involvement in an occurrence (relation)
        self.subNexts,        self.subNextUIDs         = self.DetermineSubtypeList(nextUID)       # 5333 next element (role)
        self.subtypesOfShall, self.subtypesOfShall     = self.DetermineSubtypeList(shallUID)
        self.aliass,          self.alias_uids          = self.DetermineSubtypeList(aliasUID)
        self.concWholes,      self.concWholeUIDs       = self.DetermineSubtypeList(concWholeUID)
        self.concPosss,       self.concPossUIDs        = self.DetermineSubtypeList(concPosessorUID)
        self.transs,          self.transUIDs           = self.DetermineSubtypeList(transUID)
        self.classifs,        self.classifUIDs         = self.DetermineSubtypeList(classifUID)  # 1225 classification relation
        self.specials,        self.specialUIDs         = self.DetermineSubtypeList(specialUID)
        self.concBinRelbetKinds,self.concBinRelbetKinds = self.DetermineSubtypeList(concBinRelKindsUID) # 1231 = conc.bin. relation between things of specified kinds.
        #self.props,          self.propUIDs            = self.DetermineSubtypeList(propUID)       # 551004 = property
        self.conc_playings,   self.conc_playing_uids   = self.Determine_subtypes_of_kind('4714')  # 4714 = can be a role of a 

#-------------------------------------------------------------------------
    def Determine_subtypes_of_kind(self, kind_uid):
        """Determine the list of a kind and its subtypes""" 
        kind = self.uid_dict[kind_uid]
        all_subs = []
        all_sub_uids = []
        if kind == None:
            print('Kind {} not found'.format(kind_uid))
        else:
            direct_subs = kind.subtypes
            if len(direct_subs) > 0:
                for sub in direct_subs:
                    if sub not in all_subs:
                        all_subs.append(sub)
                        all_sub_uids.append(sub.uid)
                for sub_i in all_subs:
                    sub_subs = sub_i.subtypes
                    if len(sub_subs) > 0:
                        for sub_sub in sub_subs:
                            if sub_sub not in all_subs:
                                all_subs.append(sub_sub)
                                all_sub_uids.append(sub_sub.uid)
            all_subs.append(kind)
            all_sub_uids.append(kind.uid)
        return all_subs, all_sub_uids
#----------------------------------------------------------------------------
    def DetermineSubtypeList(self, kind_uid):
        """Determine the list of uids of a kind and its subtypes""" 
        kind = self.uid_dict[kind_uid]  #self.find_object(kind_uid)
        if kind == None:
            print('Kind {} not found'.format(kind_uid))
        sub_kinds, sub_kind_uids = self.Determine_subtypes(kind)
        sub_kinds.insert(0, kind)
        sub_kind_uids.insert(0, kind_uid)
        return sub_kinds, sub_kind_uids

#----------------------------------------------------------------------------
    def Determine_subtypes(self, supertype):
        """Determine and return all_subtypes and all_subtype_uids of supertype
           (except the supertype itself) including subSubs etc. and \
           if supertype.uid = binRelUID (5935, binary relation),
           then start building the relRolesTable
        """
        # Collect subtypes of a given supertypeUID. E.g. binary relation (5935)
        all_subtypes = []
        all_subtype_uids = []
        top = supertype
        rel_taxonomy = False
        if top.uid == binRelUID:          # if supertypeUID == binary relation (5935)
            rel_taxonomy = True
##            self.relRolesTable.append(initialRelRow) # load the first line of the relRolesTable
        # Collect the subtypes of the supertype in focus
        subs = supertype.subtypes
        if len(subs) > 0: 
            for sub in subs:
                # Add each subtype to the list of subtypes
                if sub not in all_subtypes:
                    all_subtypes.append(sub)      # Add subtype to total list of subtypes
                    all_subtype_uids.append(sub.uid)
                    
                    # If sub belongs to taxonomy of relations then inherit by definition first and second kinds of roles
                    if rel_taxonomy == True:
                        self.Inherit_kinds_of_roles(sub, supertype)
                #print ('Supertype:',supertype.uid,"Subtypes:",subs,subtypeRow)

            # For each subtype determine the further subtypes                
            for subX in subs:
                sub_subs = subX.subtypes    # Possibly empty! Then the loop terminates
                for sub in sub_subs:
                    # Add the sub_sub to the list of subtypes
                    if sub not in all_subtypes:
                        all_subtypes.append(sub)
                        all_subtype_uids.append(sub.uid)
                        # Increase the list of subs that is current
                        subs.append(sub)

                        # If sub belongs to taxonomy of relations
                        # then inherit by definition first and second kinds of roles
                        if rel_taxonomy == True:
                            self.Inherit_kinds_of_roles(sub, subX)
                            
        return all_subtypes, all_subtype_uids

    def Inherit_kinds_of_roles(self, sub, supertype):
        sub.category = 'kind of relation'
        try:
            if sub.first_role: # != None:
                # Check whether supertype of kind of role == role of supertype
                equality = False
                if len(sub.first_role.supertypes) > 0:
                    for supertype_role in sub.first_role.supertypes:
                        if supertype_role == supertype.first_role:
                            equality = True
                            break
                    if equality == False:
                        print('Supertype of first kind of role {} not equal role of supertype {}'\
                              .format(supertype_role.name, supertype.first_role.name))
                else:
                    print('First kind of role {} has no supertypes'.format(sub.first_role.name))
                #print('sub.first_role_def:', sub.first_role.name)
            #else:
                #print('sub.first_role_inh:', sub.first_role.name)
        except AttributeError:
            sub.first_role = supertype.first_role
            #print('sub.inherited first_role', sub.name, sub.uid, sub.first_role.name)
            
        try:
            if sub.second_role != None:
                # Check whether supertype of kind of role == role of supertype
                equality = False
                if len(sub.second_role.supertypes) > 0:
                    for supertype_role in sub.second_role.supertypes:
                        if supertype_role == supertype.second_role:
                            equality = True
                            break
                    if equality == False:
                        print('Supertype of second kind of role {} not equal role of supertype {}'\
                              .format(supertype_role.name, supertype.second_role.name))
                else:
                    print('Second kind of role {} has no supertypes'.format(sub.second_role.name))
        except AttributeError:
            sub.second_role = supertype.second_role
#----------------------------------------------------------------
    def Determine_role_players_types(self, rel_uid):  #, phrase):
        # Individual or kind? Determine whether the query relation type denotes:
        #                        (1) a relation between individual things
        #                     or (2) between kinds
        #                     or (3) between an individual and a kind
        #                     or (4) between an individual and either another individual \
        #                            or a kind (a combination of (1) and (3))
        rolePlayersTypes = 'unknown'
        rolePlayerTypeLH = 'unknown'    # Required kind of LH object, because of kind of rel_uid
        rolePlayerTypeRH = 'unknown'    # Required kind of RH object
        int_rel_uid, integer = Convert_numeric_to_integer(rel_uid)
        if int_rel_uid >= 100:
            if rel_uid in self.indivBinRelUIDs:      # subtypes of 4658 = binary relation between individual things
                rolePlayersTypes = 'individuals'
                rolePlayerTypeLH = 'individual'
                rolePlayerTypeRH = 'individual'
            elif rel_uid in self.kindHierRelUIDs:    # subtypes of 5052 = hierarchical relation between kinds of things
                rolePlayersTypes = 'hierOfKinds'
                rolePlayerTypeLH = 'kind'
                rolePlayerTypeRH = 'kind'
            elif rel_uid in self.kindKindRelUIDs:    # subtypes of 1231 = binary relation between things of specified kinds
                rolePlayersTypes = 'thingsOfKinds'
                rolePlayerTypeLH = 'kind'
                rolePlayerTypeRH = 'kind'
            #elif rel_uid in self.kindBinRelUIDs:     # subtypes of 5937 = binary relation between kinds of things
            #    rolePlayersTypes = 'kinds'
            elif rel_uid == indOrMixRelUID:     # 6068 = binary relation between an individual thing and any (kind or individual)
                rolePlayersTypes = 'individualsOrMixed'  # is related to (a)
                #print('RolePlayers-IndividualsOrMixed:',rolePlayersTypes,relName,self.base_phrases)
##                if relName in self.base_phrases:
##                    rolePlayersTypes = 'individualAndMixed'
##                    rolePlayerTypeLH = 'individual'
##                    rolePlayerTypeRH = 'mixed'
##                else:
##                    rolePlayersTypes = 'mixedAndIndividual'
##                    rolePlayerTypeLH = 'mixed'
##                    rolePlayerTypeRH = 'individual'
            elif rel_uid in self.mixedBinRelUIDs:        # binary relation between an individual thing and a kind
                rolePlayersTypes = 'mixed'
##                if relName in self.base_phrases:
##                    rolePlayersTypes = 'individualAndKind'
##                    rolePlayerTypeLH = 'individual'
##                    rolePlayerTypeRH = 'kind'
##                else:
##                    rolePlayersTypes = 'kindAndIndividual'
##                    rolePlayerTypeLH = 'kind'
##                    rolePlayerTypeRH = 'individual'
            elif rel_uid == kindAndMixRelUID:     # 7071 = binary relation between a kind and any (kind or individual)
                rolePlayersTypes = 'kindsOrMixed'  # can be related to (a)
##                if relName in self.base_phrases:
##                    rolePlayersTypes = 'kindsAndMixed'  # can be related to (a)
##                    rolePlayerTypeLH = 'kind'
##                    rolePlayerTypeRH = 'mixed'
##                else:
##                    rolePlayersTypes = 'mixedAndKind'  # is or can be related to a
##                    rolePlayerTypeLH = 'mixed'
##                    rolePlayerTypeRH = 'kind'
            else:
                rolePlayersTypes = 'other'
        else:
            print('Relation type uid {} is unknown'.format(rel_uid))
        return rolePlayersTypes, rolePlayerTypeLH, rolePlayerTypeRH

#----------------------------------------------------------------
    def Verify_network(self):
        '''Execute various checks on completeness and consistency of the semantic network'''

        # Check whether each concept has at least one supertype concept or at least one classifier.
        for obj in self.objects:
            if obj.category in ['kind', 'kind of physical object', 'kind of occurrence', 'kind of aspect', \
                                'kind of role', 'kind of relation']:
                if len(obj.supertypes) == 0:
                    print('Kind ({}) {} has no supertype(s).'.format(obj.uid, obj.name))
            elif obj.category in ['individual', 'physical object', 'occurrence', 'aspect', \
                                  'role', 'relation']:
                if len(obj.classifiers) == 0:
                    print('Individual ({}) {} has no classifier(s).'.format(obj.uid, obj.name))
            elif obj.category not in ['number', 'anything']:
                print('The category of object {} ({}) is {}.'.format(obj.name, obj.uid, obj.category))

    
#----------------------------------------------------------------
    def Query_network_dict(self, search_string, string_commonality):
        '''Search for string as (part of) name in a names_in_contexts dictionary.
           The string_commonality specifies to what extent the string
           should correspond with the name.
           A list of candidates is returned.
           E.g.: term_in_context, value_triple = {('910036', '193259', "anything"),('730000', '5117', 'descr'))
        '''
        # Split search_string in 'chunks' separated by one or more spaces
        # while treating multiple consecutive whitespaces as one separator
        chunks = search_string.split(None)
        ref_list = []
        candids = []
        first_chunk = False
        for chunk in chunks:
            if first_chunk == False:
                # Find list of candidates based on first chunk. Use that list as a reference list
                cand_list = list(self.dictionary.filter_on_key(chunk, string_commonality))
                ref_list = cand_list[:]
                first_chunk = True
            elif len(chunks) > 1:
                candids[:] = []
                string_commonality = 'cspi'
                chunk_list = list(self.dictionary.filter_on_key(chunk, string_commonality))
                if len(chunk_list) > 0:
                    for chunk_candid in chunk_list:
                        # Check whether chunck_candid also appears in first list of candidates
                        if chunk_candid in ref_list:
                            candids.append(chunk_candid)
                    ref_list = candids[:]
                #print('Chunks:', ref_list)
                
        #candidates = list(cand_dict)
        #print('Nr of candidates for {} is {}'.format(search_string, len(candidates)))
        return ref_list

    def Find_object_by_name(self, name, string_commonality):
        '''Search for object uid by name in semantic network.
           Present candidates to user and select candidate or confirm single candidate.
           Floating point numbers should be a notation with decimal dots,
           for example in 1234.567 notation or its equivalent value 1,234.567.
           Semicolons (;) optionally followed by one or more spaces separates values.
           For example 3D coordinates may be given as: 1.0; 2.3; 3.4
        '''
        #print("  Search for object with name '%s'." % (name))
        unknown_uid = False
        candid_nr = 0
        self.uid_name_desc_list [:] = []

        # Determine the uid for an integer when name is a positive or negative whole number.
        int_uid = self.Determine_uid_for_integer(name)
        # int_uid > 0 means integer number is found and allocated uid is in range 2.000.000.001-2.999.999.999
        # Non whole numbers should be found in the dictionary (for the time being)
        if int_uid > 0:
            candidates = []
            international = '589211'  # language
            community     = '191697'      # language community mathematics
            term_in_context = [international, community, name]
            value_triple    = [str(int_uid), is_called_uid, 'decimal number ' + name]
            candidates.append([term_in_context, value_triple])
            print('Whole number', candidates[0])
        else:  
            # Search for list of candidates: [term_in_context, value_triple]
            candidates = self.Query_network_dict(name, string_commonality)
            
        if len(candidates) > 0:
            for candidate in candidates:
                candid_nr += 1
                obj_uid = candidate[1][0]   # The first value in the value_triple
                if len(candidates) > 1:
                    # candidate[0] is lang_uid, comm_uid, obj_name of first candidate
                    comm_name = self.comm_dict_NL[candidate[0][1]]
                    print("    Candidate {}: object {}, {} ({})".\
                          format(candid_nr, candidate[0][2], comm_name, obj_uid))
                # uid_name_desc = [uid, name, description]
                uid_name_desc = [obj_uid, candidate[0][2], candidate[1][2]] 
                self.uid_name_desc_list.append(uid_name_desc)
        else:
            # No candidates available, thus name is unknown.
            # Then collect unknown names and allocate UIDs in dictionary of new_things.
            unknown_uid = True
            if name not in self.new_things:
                self.new_obj_uid += 1
                if self.new_obj_uid < self.upper_obj_range_uid:
                    self.new_things[name] = self.new_obj_uid
                    int_un_id = self.new_obj_uid
                else:
                    print('Upper limit for range of UIDs %s reached. Unknown object ignored.' % \
                          (upper_obj_range_uid))
                    int_un_id = 0
            else:
                int_un_id = self.new_things[name]
            candid_nr += 1
            print("    No candidates for mapping found. Unknown {}: object ({}) {}"\
                  .format(candid_nr, int_un_id, name))
            uid_name_desc = [str(int_un_id), name, '']
            self.uid_name_desc_list.append(uid_name_desc)
            
        # Select one of the candidates.
        selected = False
        while selected == False:
            # If two candidates with identical UIDs then select the first one
            if len(candidates) == 2 and self.uid_name_desc_list[0][0] == self.uid_name_desc_list [1][0]:
                selection = self.uid_name_desc_list[0]
                selected = True
            elif len(candidates) > 1:
                if selected == False:
                    # If candidate selected earlier, then make the same selection             
                    for uid_name_desc in self.uid_name_desc_list:
                        #print('Compare {} with {}'.format(uid_name_desc[0], self.select_dict))
                        if uid_name_desc[0] in self.select_dict:
                            selection = uid_name_desc
                            selected = True
                            continue
                    cand_str = input("Select candidate number or 'Enter' to select the first one: ")
                    if cand_str != '':
                        cand_nr = int(cand_str)
                        if cand_nr > 0 and cand_nr <= len(candidates):
                            selection = self.uid_name_desc_list[cand_nr-1]
                            selected = True
                            self.select_dict[selection[0]] = selection
                        else:
                            print("Incorrect entry '" + cand_nr + "'. Select again.")
                    else:
                        # selection = '', thus select the first candidate
                        selection = self.uid_name_desc_list[0]
                        selected = True
            else:
                # If 0 or 1 candidate then automatically select the single candidate or the unknown.
                selection = self.uid_name_desc_list[0]
                selected = True
        return unknown_uid, selection

    def Determine_uid_for_integer(self, string):
        ''' Determine a UID for a string that represents an integer number.
            First remove comma separation if present, e.g. -1,234 becomes -1234.
            Then verify whether the string value is a positive or negative integer number.
            Determine the uid: uid = 2.000.000.000 + pos_number or 1.000.000.000 - neg_number
        '''
        uid = 0
        commas_removed = string.replace(',', '')
        # Check on negative number
        if commas_removed[0] == '-':
            pos_number = - commas_removed
        else:
            pos_number = commas_removed
        if pos_number.isdecimal():
            number = int(pos_number)
            if commas_removed[0] == '-':
                uid = 1000000000 + number
            else:
                uid = 2000000000 + number
        return uid
#---------------------------------------
    def Pickle_Dump(self, fname):
        f = open(fname, "bw")
        pickle.dump(self, f)
        f.close()
#---------------------------------------  
    def Build_product_views(self, obj_list):
        ''' Create product model views for one or more objects'''

        self.kind_model[:]    = []
        self.prod_model[:]    = []
        self.taxon_model[:]   = []
        self.taxon_objects[:] = []
        self.summ_model[:]    = []
        self.summ_objects[:]  = []
        self.possibilities_model[:] = []
##        self.possib_objects[:] = []
        self.indiv_model[:]   = []
        self.indiv_objects[:] = []
        self.query_table[:]   = []
        self.info_model[:]    = []
        self.occ_model[:]     = []
        self.involv_table[:]  = []
        self.seq_table[:]     = []
        self.part_whole_occs[:]= []
        self.all_subtypes[:]  = []
        self.summ_aspect_uids[:]   = ['','','','']
        self.summ_column_names[:]  = ['','','','']
        self.summ_uom_names[:]     = ['','','','']
        self.taxon_aspect_uids[:]  = ['','','','']
        self.taxon_column_names[:] = ['','','','']
        self.taxon_uom_names[:]    = ['','','','']
        self.indiv_aspect_uids[:]  = ['','','','','']
        self.indiv_column_names[:] = ['','','','','']
        self.indiv_uom_names[:]    = ['','','','','']

        self.messages = []

        for obj in obj_list:
            lang_name, comm_name, preferred_name, descr = \
                       self.Determine_name_in_language_and_community(obj)
            obj.name = preferred_name
            self.object_in_focus  = obj
            
            # Initialize subtype list of object in focus
            # Excluding duplicates due to multiple inheritance
            self.all_subtypes[:] = []
            # If object is excluded because it did not satisfy a condition then skip it
            if obj in self.ex_candids:
                print('Excluded candidate-1: {}'.format(obj.name))
                continue
            self.subtype_level = 0
            self.Build_single_product_view(obj)
        
    def Build_single_product_view(self, obj):
        ''' Create product model views in
            kind_model, prod_model, query_table (with Gellish expressions),
            taxon_model (taxonomy view) summ_model (tabular view),
            possibilities_model and indiv_model'''

        # Verify whether object is excluded from list of candidates
        if obj in self.ex_candids:
            print('Excluded candidate: {}'.format(obj.name))
            return
        #self.line_nr = 3
        
        self.implied_parts_dict = {}
        self.nr_of_occurrencies = 0
        self.occ_in_focus = 'no'
        nr_of_occ_aspect_kinds  = 3
        self.decomp_level = 0
        role = ''

        self.Create_prod_model_view_header(obj)

        if obj.category in ['kind', 'kind of physical object', 'kind of occurrence', \
                            'kind of aspect', 'kind of role', 'kind of relation', 'number']:
            # Search for the first supertype relation that generalizes the obj (= self.object_in_focus)
            if len(obj.supertypes) == 0:
                # No supertypes found for kind: report omission
                kindUID  = 0
                kindName = 'Not found'
                descrOfUID = ''
                print('No supertype of {} found'.format(obj.name))
            else:
                # There is one or more supertype of the kind in focus:
                # collect all supertype relations in query_table
                for supertype in obj.supertypes:
                    for rel_obj in obj.relations:
                        expr = rel_obj.expression
                        if expr[rel_type_uid_col] in ['1146', '1726', '5396', '1823']:
                            if len(self.query_table) < self.max_nr_of_rows:
                                self.query_table.append(expr)

        # Individual thing: Object category is not a kind, thus indicates an indiv.
        # Verify whether the individual thing is classified (has one or more classifiers)
        elif len(obj.classifiers) == 0:
            print('For object {} neither a supertype nor a classifier is found'.format(obj.name))
        else:
            # The object_in_focus is classified (once or more times)
            # thus it is indeed an individual, such as an individual physical object or occurrence:
            # Search for classifying kind and classification relation that classifies the object_in_focus
            classifier = obj.classifiers[0]
            # kindUID is the kind that classifies the self.object_in_focus
            kind_uid   = classifier.uid
            # Determine name etc. of the kind of the object_in_focus
            lang_name, comm_name, kind_name, descrOfKind = \
                       self.Determine_name_in_language_and_community(classifier)

            # Verify whether the individual is an occurrence.
            if kind_uid in self.subOccurrenceUIDs:
                obj.category = 'occurrence'

        # If obj is an occurrence then store occurrence in occ_model
        if obj.category == 'occurrence' or obj.category == 'kind of occurrence':
            self.nr_of_occurrencies += + 1

            #self.occ_model.append([occ.uid, occ.name, higher.name, involv.uid, kind_occ.uid,\
            #                       occ.name, part_occ.name, \
            #                       involv.name, kind_part_occ.name, role_of_involved])
            self.occ_model.append([obj.uid, '', '', '', '', \
                                   obj.name, '', '', kind_name, ''])
    
        # Search for aspects of the whole object_in_focus and their values and UoMs

        # Find kinds of aspects and their values of kind_in_focus (and implied parts)
        if obj.category in ['kind', 'kind of physical object', 'kind of occurrence', \
                            'kind of aspect', 'kind of role' , 'kind of relation', 'number']:
            # Find preferred name of object in required language and community
            lang_name, comm_name, obj_name, descr = \
                       self.Determine_name_in_language_and_community(obj)
            obj.name = obj_name
        
            self.taxon_row[0] = obj.uid
            self.taxon_row[1] = obj.name    # preferred name
            #self.taxon_row[2] = supertype_name   # name of the first supertype
            self.taxon_row[3] = comm_name

            if len(obj.supertypes) > 0:
                lang_name, comm_name_supertype, supertype_name, descr_of_super = \
                           self.Determine_name_in_language_and_community(obj.supertypes[0])
            else:
                supertype_name = 'unknown'

##            self.possibility_row[0] = obj.uid
##            self.possibility_row[1] = obj_name
##            self.possibility_row[2] = ''
##            self.possibility_row[3] = supertype_name
##            self.possibility_row[4] = comm_name     # of obj (not of supertype)
            # Add object_in_focus to possibilities_model with comm_name of obj (not of supertype)
            self.possibilities_model.append([obj.uid, obj_name, '', supertype_name, comm_name])
            
            nr_of_aspects = self.Find_kinds_of_aspects(obj, role)
            
            # Find kinds of parts and their conceptual aspects
            self.Find_kinds_of_parts_and_their_aspects(obj)

            # Find (qualitative) information about the object and build info_model
            self.Find_information_about_object(obj)

            # Determine whether the kind is a classifier for individual things
            self.Determine_individuals(obj)

            # Determine subtypes of kind_in_focus and build product models of those subtypes
            self.subtype_level += 1
            for sub in obj.subtypes:
                if sub not in self.all_subtypes:
                    self.all_subtypes.append(sub)
                    self.Build_single_product_view(sub)

        # Find aspects, their classification and their values of the individual object_in_focus
        elif obj.category in ['individual', 'physical object', 'occurrence']:

            community_name = self.community_dict[obj.names_in_contexts[0][1]] # community uid
            self.summary_row[0] = obj.uid
            self.summary_row[1] = obj.name
            self.summary_row[2] = kind_name
            self.summary_row[3] = community_name
            
            self.indiv_row[0] = obj.uid
            self.indiv_row[1] = obj.name
            self.indiv_row[2] = ''
            self.indiv_row[3] = kind_name
            self.indiv_row[4] = community_name
            
            # Find aspects of individual object_in_focus
            nr_of_aspects = self.Find_aspects(obj, role)

            # Find parts and their aspects
            self.part_head_req = True
            self.Find_parts_and_their_aspects(obj)
            
        else:
            print("Object category '{}' not programmed for searching for aspects".format(obj.category))
                
        #self.parts_of_occ_table= []       # parts of occurrence in focus
        if obj.category != 'occurrence':
            # Search for occurrences about the object_in_focus and other involved objects in those occurrences.
            self.decomp_level = 0
            self.OccursAndInvolvs(obj)    
    
##    def Create_prod_model_subtypes(self, obj):
##        ''' Create header in prod_model for subtypes of obj and
##            Determine subtypes of obj in hierarchy of kinds
##        '''
##        
##        subsHead = ['Subtypes','Subtypen']
##        sub2Head = ['Sub-subs','Sub-subs']
##        sub3Head = ['Further subs','Verdere subs']
##        collOfSubtypes = []
##        #self.subtype_level = 0
##        # Create header line for subtypes in prod_model
##        self.line_nr  += 1
##        prod_head_5 = ['','',self.line_nr, subsHead[self.GUI_lang_index], sub2Head[self.GUI_lang_index],\
##                     sub3Head[self.GUI_lang_index],'','','','','','']
##        if len(self.prod_model) < self.max_nr_of_rows:
##            self.prod_model.append(prod_head_5)
##
##        if obj.category in ['kind', 'kind of occurrence']:
##            self.Subtypes_of_kinds(obj)

##    def Subtypes_of_kinds(self, obj):
##        """Determine subtype hierarchy""" 
##        self.coll_of_subtype_uids = []
##
##        # Start with direct subtype, except when they should be excluded
##        subs = []
##        if len (obj.subtypes) > 0:
##            for subtype in obj.subtypes:
##                if subtype in self.ex_candids:
##                    continue
##                subs.append(subtype)
##        self.subtype_level = 0
##        role = ''
##        subsLocal = subs
##        if len(subsLocal) > 0:
##            self.subtype_level += + 1
##            for s in subsLocal:
##                for rel in s.relations:
##                    if len(self.query_table) < self.max_nr_of_rows:
##                        self.query_table.append(rel.expression)
##            # Determine subtypes of subtypes recursively
##            for sub in subs:
##                if sub in self.ex_candids or sub.uid in self.coll_of_subtype_uids:
##                    continue
##                # Summary_row = [uid, community_name, obj.name, supertype name]
##                community_name = self.community_dict[obj.names_in_contexts[0][1]] # community uid
##                self.summary_row[0] = obj.uid
##                self.summary_row[1] = obj.names_in_contexts[0][2] # obj.name
##                self.summary_row[2] = sub.names_in_contexts[0][2] # why not supertype?
##                self.summary_row[3] = community_name
##                self.coll_of_subtype_uids.append(sub.uid)
##                #print('self.summary_row',self.summary_row)
##                nr_of_aspects = self.Find_kinds_of_aspects(sub, role)
##                # Determine sub-subtypes
##                Subtypes_of_kinds(sub)

    def OccursAndInvolvs(self, obj):
        """ Search for occurrences in which the obj (in focus) is involved.
            The occurrences are related with an involver role or one of its subtypes to the (physical) object_in_focus
            and search for (physical) objects that are involved in those occurrences in various roles.
            Search for aspects of the occurrences (such as duration).
            Store results in prod_model and the composition in partWholeOcc.
        """

        occur_head   = ['Occurrences' ,'Gebeurtenissen']
        role_head    = ['Role'        ,'Rol']
        involv_head  = ['Involved object','Betrokken object']
        kind_head    = ['Kind'        ,'Soort']
        #print('**** OccursAndInvolvs:',obj.uid, obj.name, obj.category)

        nr_of_occur = 0
        self.occ_in_focus = 'no'
        self.line_nr += + 1
        
        # Search for UID and <involved> role or its subtypes to find occurrences (involver role players)
        for rel_obj in obj.relations:
            expr = rel_obj.expression
            if (expr[rh_uid_col] == obj.uid and expr[rel_type_uid_col] in self.subInvolvUIDs):
                occ_uid   = expr[lh_uid_col]
                #occ_name  = expr[lh_name_col]
            elif expr[lh_uid_col] == obj.uid and expr[rel_type_uid_col] in self.subInvolvUIDs:
                occ_uid   = expr[rh_uid_col]
                #occ_name  = expr[rh_name_col]
            else:
                continue

            # An occurrence is found
            nr_of_occur += + 1
            occ = self.uid_dict[occ_uid]
            occ_name = occ.name
            self.decomp_level = 1
            #print('Occ     :',obj.name, occ_uid, occ_name,'roles:', expr[rel_type_name_col],\
            #      expr[lh_role_name_col], expr[rh_role_name_col])
            
            # Display occurrences header, only the first time
            if nr_of_occur == 1:
                prod_head_5 = ['', '', '', self.line_nr, \
                               occur_head[self.GUI_lang_index] , role_head[self.GUI_lang_index], \
                               involv_head[self.GUI_lang_index], kind_head[self.GUI_lang_index],'','','','','']
                self.prod_model.append(prod_head_5)
            
            if len(self.query_table) < self.max_nr_of_rows:
                self.query_table.append(expr)

            # Record the role playing occurrence in occ_model
            # Find classifying kind of occurrence
            if len(occ.classifiers) > 0:
                occ_kind = occ.classifiers[0]
                occ_kind_name = occ_kind.name
                occ_kind_uid = occ_kind.uid
            else:
                print('Occurrence {} classifier is unknown'.format(occ.name))
                occ_kind_name = 'unknown'
                occ_kind_uid = ''

            #self.occ_model.append([occ.uid, occ.name, higher.name, involv.uid, occ_kind.uid,\
            #                       occ.name, part_occ.name, \
            #                       involv.name, kind_part_occ.name, role_of_involved])
            self.occ_model.append([occ.uid, occ.name, '', '', occ_kind_uid, \
                                   occ.name, '', '', occ_kind_name, ''])
            #print('Occ-3:',[nr_of_occur, occ.name, occ_uid, occ_kind_name])

            status = expr[status_col]
            occ_role = ''
            self.occ_in_focus = 'occurrence'
            # Find possession of aspect relations for aspects of occurrence
            nr_of_aspects = self.Find_aspects(occ, occ_role)
            
            # If no aspects found then line without aspects (otherwise line is included in Find_aspects
            if nr_of_aspects == 0:
                self.line_nr += + 1
                prod_line_5 = [occ.uid, occ_kind.uid, '', self.line_nr, occ_name,'','',occ_kind_name,\
                               '','','','','',status]
                self.prod_model.append(prod_line_5)
                
            # Search for objects that are involved in the found occurrence
            # decomp_level determines print layout in product model.
            self.decomp_level = 3
            for rel_occ in occ.relations:
                expr_occ = rel_occ.expression
                # Search <is involved in> or <is involving> or any of its subtypes relations in occ
                # excluding the object in focus (obj)
                if expr_occ[rh_uid_col] != obj.uid and \
                   (expr_occ[lh_uid_col] == occ.uid and expr_occ[rel_type_uid_col] in self.subInvolvUIDs):
                    involved_uid   = expr_occ[rh_uid_col]
                    #involved_name  = expr_occ[rh_name_col]
                    inv_role_name  = expr_occ[rh_role_name_col]
                elif expr_occ[lh_uid_col] != obj.uid and \
                     (expr_occ[rh_uid_col] == occ.uid and expr_occ[rel_type_uid_col] in self.subInvolvUIDs):
                    involved_uid   = expr_occ[lh_uid_col]
                    #involved_name  = expr_occ[lh_name_col]
                    inv_role_name  = expr_occ[lh_role_name_col]
                else:
                    continue

                # An object is found that is involved in the occurrence
                involved = self.uid_dict[involved_uid]
                #print('Involved:',obj.uid, involved.uid, involved.name,\
                #      'roles:',expr_occ[lh_role_uid_col],expr_occ[rh_role_uid_col])
                
                self.query_table.append(expr_occ)
                status = expr_occ[status_col]
                
                # Determine the kind of the involved individual object
                if len(involved.classifiers) > 0:
                    involved_kind = involved.classifiers[0]
                    involved_kind_name = involved_kind.name
                else:
                    print('Involved object {} has no classifier'.format(involved.name))
                    involved_kind_name = 'unknown'
                
                # Search for aspects of objects that are involved in occurrence
                # Find possession of aspect relations of involved object
                nr_of_aspects = self.Find_aspects(involved, inv_role_name)
                
                # if no aspects of part found, then record part only
                if nr_of_aspects == 0:
                    self.line_nr += + 1
                    prod_line_6 = [involved.uid, involved_kind.uid, '', \
                                   self.line_nr, '', inv_role_name, involved.name, involved_kind_name,\
                                   '','','','','',status]
                    self.prod_model.append(prod_line_6)

            # Search for successors or predecessors of found occurrence
            #   with inputs and outputs and parts (? see below)
            self.OccurrenceSequences(occ)

            # Search for parts of found occurrence and parts of parts, etc.
            occ_level = 1
            self.PartOfOccur(occ, occ_level)

##        # Check whether nr of occurrences = 0
##        if nr_of_occur == 0:
##            #if self.GUI_lang_index == 1:
##            #    MessagesQ.insert('end','\nGeen gebeurtenissen gevonden in antwoord op vraag over %s (%i)' % (name,UID))
##            #else:
##            #    MessagesQ.insert('end','\nNo involving occurrences found in query results for %s (%i)' % (name,UID))
##            self.line_nr += + 1
##            none = ['None','Geen']
##            prod_head_5A = ['','','',self.line_nr, none[self.GUI_lang_index],'','','','','','','','']
##            self.prod_model.append(prod_head_5A)

    def OccurrenceSequences(self, occ):
        """ Build activities and their components with sequence between the components in the seq_table
            and inputs and outputs in involv_table.
            seq_table:    previusUID, previusName, nextUID,     nextName.
            involv_table: occurUID,   occurName,   involvedUID, involvedName, roleUID, roleName (of invObj), invKindName.
            p_occ_table:  wholeUID,   wholeName,   partUID,     partName,  kindOfPartName
        """    

        #print('OccurrenceSequences',occ.uid, occ.name)
        
        part_uids = []
        nr_of_sequences = 0
        nr_of_ins_and_outs = 0
        nr_of_parts = 0
        # Build sequence table (seq_table) for sequence of occurrences
        for rel_occ in occ.relations:
            expr = rel_occ.expression
            # Search for predecessor - successor relations
            if expr[rh_uid_col] == occ.uid and expr[rh_role_uid_col] in self.subNextUIDs:
                predecessor = self.uid_dict[expr[lh_uid_col]]
                self.seq_table.append([predecessor, occ])
                nr_of_sequences += 1
            elif expr[lh_uid_col] == occ.uid and expr[lh_role_uid_col] in self.subNextUIDs: # inverse
                predecessor = self.uid_dict[expr[rh_uid_col]]
                self.seq_table.append([predecessor, occ])
                nr_of_sequences += 1
                
            # Search for inputs and outputs (streams) in involv_table
            elif expr[lh_uid_col] == occ.uid and expr[rel_type_uid_col] in self.subInvolvUIDs:
                involved = self.uid_dict[expr[rh_uid_col]]
                if len(involved.classifiers) > 0:
                    inv_kind_name = involved.classifiers[0].name
                if expr[rh_role_uid_col] != '':
                    inv_role_kind = self.uid_dict[expr[rh_role_uid_col]]
                else:
                    inv_role_kind = self.uid_dict['160170']
##                ioRow = []
##                ioRow.append(expr[lh_uid_col])       # occurrence UID
##                ioRow.append(expr[lh_name_col])      # occName
##                ioRow.append(expr[rh_uid_col])       # involved object UID
##                ioRow.append(expr[rh_name_col])      # involved object Name
##                ioRow.append(expr[rh_role_uid_col])   # role UID of involved object
##                ioRow.append(expr[rhKindRoleNameExC])  # role Name of involved object
##                kindOfInvData = FindClassification(expr[rh_uid_col],expr[rh_name_col])
##                ioRow.append(kindOfInvData[1])
                self.involv_table.append([occ, involved, inv_role_kind, inv_kind_name])
                nr_of_ins_and_outs += 1
            elif expr[rh_uid_col] == occ.uid and expr[rel_type_uid_col] in self.subInvolvUIDs: # inverse
                involved = self.uid_dict[expr[lh_uid_col]]
                if len(involved.classifiers) > 0:
                    inv_kind_name = involved.classifiers[0].name
                inv_role_kind = self.uid_dict[expr[lh_role_uid_col]]
##                ioRow = []
##                ioRow.append(expr[rh_uid_col])       # occurrence UID
##                ioRow.append(expr[rh_name_col])      # occName
##                ioRow.append(expr[lh_uid_col])       # involved object UID
##                ioRow.append(expr[lh_name_col])      # involved object Name
##                ioRow.append(expr[lh_role_uid_col])   # role UID of involved object
##                ioRow.append(expr[lhKindRoleNameExC])  # role Name of involved object
##                kindOfInvData = FindClassification(expr[lh_uid_col],expr[lh_name_col])
##                ioRow.append(kindOfInvData[1])
                self.involv_table.append([occ, involved, inv_role_kind, inv_kind_name])
                nr_of_ins_and_outs += 1
                
##            # Search for parts of occurrence, being part - whole relations
##            elif expr[lh_uid_col] == occ.uid and expr[rh_role_uid_col] in self.subComponUIDs:
##                part = self.uid_dict[expr[rh_uid_col] 
##                part_uids.append(part.uid)
##                self.parts_of_occ_table.append([occ, part])
##                nr_of_parts += 1
##            elif expr[rh_uid_col] == occ.uid and expr[lh_role_uid_col] in self.subComponUIDs: # inverse
##                part = self.uid_dict[expr[lh_uid_col]]
##                part_uids.append(part.uid)
##                self.parts_of_occ_table.append([occ, part])
##                nr_of_parts += 1
        
        if len(occ.parts) > 0:
            # Determine sequences, IOs and parts of parts
            for part_occ in occ.parts:
                self.OccurrenceSequences(part_occ)

    def PartOfOccur(self, occ, occ_level):
        """ Determine whole-parts hierarchy for occurrences
            Store results in prod_model
        """

        parts = False
        part_head   = ['Part occurrence', 'Deelgebeurtenis']
        kind_part_head = ['Kind of part', 'Soort deel']
        for rel_occ in occ.relations:
            expr = rel_occ.expression 
            if expr[lh_uid_col] == occ.uid and expr[rel_type_uid_col] in self.subComposUIDs:
                # Create header line, only after finding a part the first time
                if parts == False:
                    self.line_nr += + 1
                    prod_line_7 = ['', '', '', self.line_nr, '', part_head[self.GUI_lang_index],'',\
                                   kind_part_head[self.GUI_lang_index],'','','','','','']
                    self.prod_model.append(prod_line_7)
                    parts = True
                part_occ = self.uid_dict[expr[rh_uid_col]]
                status = expr[status_col]
                
                self.query_table.append(expr)
                
                if len(part_occ.classifiers) > 0:
                    kind_part_occ = part_occ.classifiers[0]
                    kind_part_occ_uid = kind_part_occ.uid
                    kind_part_occ_name = kind_part_occ.name
                else:
                    print('Part of occurrnce {} has no classifier'.format(part_occ.name))
                    kind_part_occ = 'unknown'
                    kind_part_occ_uid = '0'
                    kind_part_occ_name = 'unknown'
                    
                if occ_level < 2:
                    self.line_nr += + 1
                    prod_line_8 = [part_occ.uid, kind_part_occ_uid, '', self.line_nr, '', part_occ.name, '',\
                                   kind_part_occ_name, '','','','','', status]
                    self.prod_model.append(prod_line_8)
                    self.nr_of_occurrencies += + 1
                    involv_uid = ''
                    role_of_involved = ''
                    #self.occ_model.append([part_occ.uid, part_occ.name, whole_occ.name, involv.uid, kind_occ.uid,\
                    #                       occ.name, part_occ.name, involv.name, \
                    #                       kind_part_occ.name, role_of_involved])
                    self.occ_model.append([part_occ.uid, part_occ.name, occ.name, involv_uid, kind_part_occ_uid,\
                                           '', part_occ.name,  '', \
                                           kind_part_occ_name, role_of_involved])

                # Add whole, part and kind of part occurrence to part_whole_occs hierarchy
                self.part_whole_occs.append([occ, part_occ, kind_part_occ])

                # Search for part on next decomposition level (part_of_part of occurrence)
                part_level = occ_level + 1
                self.PartOfOccur(part_occ, part_level)

    def Determine_name_in_language_and_community(self, obj):
        ''' Given an object and preferred language sequence uids and community sequence uids,
            determine lang_name, comm_name, obj_name for user interface
        '''
        name_known = False
        if len(obj.names_in_contexts) > 0:
            # For language_prefs search for name  === for comm_pref_uids to be done ===
            for lang_uid in self.reply_lang_pref_uids:
                for name_in_context in obj.names_in_contexts:
                    # Verify if language uid corresponds with required reply language uid
                    if name_in_context[0] == lang_uid:
                        obj_name  = name_in_context[2]
                        lang_name = self.lang_uid_dict[name_in_context[0]]
                        comm_name = self.community_dict[name_in_context[1]] # community uid
                        part_def  = name_in_context[4]
                        name_known = True
                        break
                        #return lang_name, comm_name, obj_name, part_def
                if name_known == True:
                    break
            if name_known == False:
                # If no name is available in the preferred language, then use the first available name
                obj_name  = obj.names_in_contexts[0][2]
                lang_name = self.lang_uid_dict[obj.names_in_contexts[0][0]]
                comm_name = self.community_dict[obj.names_in_contexts[0][1]] # community uid
                part_def  = obj.names_in_contexts[0][4]
        else:
            print('No names in contexts for {}'.format(obj.name))
            obj_name  = obj.name
            lang_name = 'unknown'
            comm_name = 'unknown'
            part_def  = ''

        # Determine supertype name in the preferred language and concatenate with part_def
        super_name_known = False
        if len(obj.supertypes) > 0 and len(obj.supertypes[0].names_in_contexts) > 0:
            for lang_uid in self.reply_lang_pref_uids:
                for name_in_context in obj.supertypes[0].names_in_contexts:
                    # Verify if language uid corresponds with required reply language uid
                    if name_in_context[0] == lang_uid:
                        super_name  = name_in_context[2]
                        super_name_known = True
                        break
                if super_name_known == True:
                    break
        if super_name_known == True:
            full_def = super_name + ' ' + part_def
        else:
            full_def = part_def
        
        return lang_name, comm_name, obj_name, full_def

    def Create_prod_model_view_header(self, obj):
        # Create prod_model view header

        # Verify if object is classified or has a supertype
        status_text = ['accepted', 'geaccepteerd'] # === should become the status of the classification cr specialization relation ===
        if len(obj.classifiers) == 0 and len(obj.supertypes) == 0:
            obj_kind_uid  = ''
            obj_kind_name = 'unknown'
            status = status_text[self.GUI_lang_index]
        else:
            obj_kind_uid  = obj.kind.uid
            lang_name, comm_name, obj_kind_name, descr = \
                               self.Determine_name_in_language_and_community(obj.kind)
            status = 'unknown'
        is_a = ['is a ', 'is een ']
        form_text  = ['Product form for:', 'Product formulier voor:']
        kind_text  = ['Kind:'            , 'Soort:']
        descr_text = ['Description:'     , 'Omschrijving:']
        if len(obj.names_in_contexts) > 0:
            description = is_a[self.GUI_lang_index] + obj_kind_name + '' + obj.names_in_contexts[0][4]
        else:
            description = is_a[self.GUI_lang_index] + obj_kind_name

        prod_line_0 = [obj.uid  , obj_kind_uid , '', 1 , form_text[self.GUI_lang_index], obj.name, '', '',\
                       kind_text[self.GUI_lang_index], obj_kind_name, '', '', '', status]    # names_in_contexts[0][2]
        prod_line_1 = ['','','',2,'', descr_text[self.GUI_lang_index], description,'','','','','','','']
        
##        prod_line_NL0 = [obj.uid,obj_kind_uid,'',1,'Product formulier voor:',obj.name,'','',\
##                         'Soort:',obj_kind_name,'','','',status]
##        prod_line_NL1 = ['','','',2,'','Omschrijving:',description,'','','','','','','']
        prod_head_NL2I= ['','','',3,'','','','','Aspect','Soort aspect','>=<','Waarde','Eenheid','Status']
        prod_head_NL2K= ['','','',3,'','','','','Soort aspect',''      ,'>=<','Waarde','Eenheid','Status']

##        prod_line_EN0 = [obj.uid,obj_kind_uid,'',1,'Product form for:',obj.name,'','',\
##                         'Kind:',obj_kind_name,'','','',status]
##        prod_line_EN1 = ['','','',2,'','Description:',description,'','','','','','','']
        prod_head_EN2I= ['','','',3,'','','','','Aspect','Aspect type','>=<','Value','UoM','Status']
        prod_head_EN2K= ['','','',3,'','','','','Kind of aspect',''   ,'>=<','Value','UoM','Status']

        self.line_nr = 3

        #prod_line_3 = [part_uid   , part_kind_uid, aspect_uid, self.line_nr, part,  '','',kindOfPart,\
        #               aspect.name, kindOfAspect, value,UoM,status]
        #prod_line_4 = [part_of_part.uid,part_kind_uid,aspect_uid, self.line_nr,'',  partOfPart,'',kindOfPart,\
        #               aspect.name, kindOfAspect, value,UoM,status]
        #prod_line_5 = [occur_uid  , occ_kind_uid, aspect_uid , self.line_nr, occur, '','',kindOfOcc,\
        #               aspect.name, kindOfAspect, value,UoM,status]
        #prod_line_6 = [inv_obj.uid, inv_kind_uid, aspect_uid , self.line_nr, ''   , invObject,role,kindOfInv,\
        #               aspect.name, kindOfAspect, value,UoM,status]
        #prod_line_7 = [part_uid   , part_kind_uid,aspect_uid , self.line_nr, ''   , '','','',\
        #               aspect.name, kindOfAspect, value,UoM,status]
        #prod_line_8 = [obj.uid    , obj_kind_uid, file_uid   , self.line_nr, obj  , document,'',kind_of_document,\
        #               file       , kind_of_file, '','',status]

        if obj.category in ['kind', 'kind of physical object', 'kind of occurrence']:
            self.kind_model.append(prod_line_0)
            if len(obj.supertypes) > 1:
                for super_type in obj.supertypes[1:]:
                    lang_name, comm_name, supert_type_name, descr = \
                               self.Determine_name_in_language_and_community(super_type)
                    self.kind_model.append([obj.uid,super_type.uid,'',1,'','','','','',supert_type_name])
            self.kind_model.append(prod_line_1)
            if self.GUI_lang_name == 'Nederlands':
                self.kind_model.append(prod_head_NL2K)
            else:
                self.kind_model.append(prod_head_EN2K)
        else:
            # Category is individual
            self.prod_model.append(prod_line_0)
            # If there are several classifiers, then add a line per classifier
            if len(obj.classifiers) > 1:
                for classifier in obj.classifiers[1:]:
                    lang_name, comm_name, classifier_name, descr = \
                               self.Determine_name_in_language_and_community(classifier)
                    self.prod_model.append([obj.uid,classifier.uid,'',1,'','','','','',classifier_name])
            self.prod_model.append(prod_line_1)
            if self.GUI_lang_name == 'Nederlands':
                self.prod_model.append(prod_head_NL2I)
            else:
                self.prod_model.append(prod_head_EN2I)

    def Find_kinds_of_aspects(self, obj, role):
        '''Search for kinds of aspects that can/shall or are by definition possessed by a kind of thing (obj)
        and search for their qualitative subtypes and possible collection of allowed values.
        obj      = the kind in focus
        role     = the role played by an involved object that is involved in an occurrence
        decomp_level = indentation level: 0 = objectInFocus, 1 = part, 2 = part of part, etc.
        obj.category = category of the object in focus,
                      being individual or kind or phys object or occurrence or kind of occurrence'''

        unknownKind  = ['unknown supertype','onbekend supertype']
        noValuesText = ['No specification','Geen specificatie']
        self.has_as_subtypes = ['has as subtypes', 'heeft als subtypes']
        possible_aspect_text = ['possible characteristic of a ', 'mogelijk kenmerk van een ']
        of_text = [' (of ', ' (van ']

        # Search for expressions that are (subtypes of) the <can have as aspect a> kind of relation
        # with the obj.uid (or its supertypes) at left or at right.
        nr_of_aspects = 0   # number of kinds of aspects that are possessed by this kind of object
        value_name = ''
        aspect_uid  = ''
        aspect_name = ''
        uom_uid   = ''
        uom_name  = ''
        equality  = ''
        status    = ''
        obj_name  = obj.name

        # Collect all relations in query_table
        for rel_obj in obj.relations:
                expr = rel_obj.expression
                if len(self.query_table) < self.max_nr_of_rows and expr not in self.query_table:
                        self.query_table.append(expr)
        
        # Collect list of obj and its supertypes in the complete hierarchy for searching inherited aspects
        all_supers = self.Determine_supertypes(obj)
        
        # For each object in the hierarchy find aspects and inherited aspect values but exclude the roles
        for obj_i in all_supers:
            value_presence = False
            for rel_obj in obj_i.relations:
                expr = rel_obj.expression
                # Find expression with poss_of_aspect relations about the object (or its supertype)
                if expr[lh_uid_col] == obj_i.uid \
                   and (expr[rel_type_uid_col] in self.subConcPossAspUIDs \
                        and not expr[rel_type_uid_col] in self.conc_playing_uids):
                    aspect_uid   = expr[rh_uid_col]
                    aspect_name  = expr[rh_name_col]
                    role_uid     = expr[rh_role_uid_col]
                    role_name    = expr[rh_role_name_col]
                elif expr[rh_uid_col] == obj_i.uid \
                     and (expr[rel_type_uid_col] in self.subConcPossAspUIDs \
                          and not expr[rel_type_uid_col] in self.conc_playing_uids):
                    aspect_uid   = expr[lh_uid_col]
                    aspect_name  = expr[lh_name_col]
                    role_uid     = expr[lh_role_uid_col]
                    role_name    = expr[lh_role_name_col]
                else:
                    continue
                # There is a kind of aspect found
##                # Add a found <can have as aspect a> relation (or its subtype) to the query_table for output
##                if len(self.query_table) < self.max_nr_of_rows:
##                    self.query_table.append(expr)

                nr_of_aspects += 1    
                #self.line_nr  += 1
                status = expr[status_col]     
                equality = '='
                value_uid  = ''
                value_name = ''
                uom_uid   = ''
                uom_name  = ''
                value_presence = False
                
                # Searching for values/criteria for the kind of aspect
                # Therefore, find a rh_role object (intrinsic aspect) of the <can have as aspect a> relation.
                if role_uid != '':
                    role = self.uid_dict[role_uid]

##                    # Derive implied relations between role and supertype, possessor and aspect
##                    implied_role_supertype = [role_uid, role.name, 1146, 4289, 'intrinsic aspect']
##                    implied_role_possessor = [role_uid, role.name, 5738, obj.uid, obj.name]
##                    implied_role_aspect    = [role_uid, role.name, 5817, aspect_uid, aspect_name]
                    
                    # Find collection of allowed values or other criterion, constraints or value for intrinsic aspect, if any.
                    for rel_obj in role.relations:
                        expr2 = rel_obj.expression
                        # Find collection of qualitative aspects for intrinsic aspect (=role), if any.
                        if role_uid == expr2[lh_uid_col] and expr2[rel_type_uid_col] in self.qualOptionsUIDs:
                            value_uid  = expr2[rh_uid_col]   # collection of allowed values
                            value_name = expr2[rh_name_col]
                            value_presence = True
                            break
                        elif role_uid == expr2[rh_uid_col] and expr2[rel_type_uid_col] in self.qualOptionsUIDs:
                            value_uid  = expr2[lh_uid_col]   # collection of allowed values
                            value_name = expr2[lh_name_col]
                            value_presence = True
                            break

                        # Find conceptual compliancy criterion, (4951) for intrinsic aspect (=role), if any.
                        elif role_uid == expr2[lh_uid_col] and expr2[lh_role_uid_col] in self.concComplUIDs:
                            value_uid  = expr2[rh_uid_col]   # compliancy criterion or constraint
                            value_name = expr2[rh_name_col]
                            value_presence = True
                            break
                        elif role_uid == expr2[rh_uid_col] and expr2[rh_role_uid_col] in self.concComplUIDs:
                            value_uid  = expr2[lh_uid_col]   # compliancy criterion or constraint
                            value_name = expr2[lh_name_col]
                            value_presence = True
                            break

                        # Find conceptual quantification (1791) for intrinsic aspect (=role), if any.
                        elif role_uid == expr2[lh_uid_col] and expr2[rel_type_uid_col] in self.concQuantUIDs:
                            value_uid  = expr2[rh_uid_col]   # value (on a scale)
                            value_name = expr2[rh_name_col]
                            uom_uid        = expr2[uom_uid_col]
                            uom_name       = expr2[uom_name_col]
                            value_presence = True
                            break
                        elif role_uid == expr2[rh_uid_col] and expr2[rel_type_uid_col] in self.concQuantUIDs:
                            value_uid  = expr2[lh_uid_col]   # value (on a scale)
                            value_name = expr2[lh_name_col]
                            uom_uid        = expr2[uom_uid_col]
                            uom_name       = expr2[uom_name_col]
                            value_presence = True
                            break

                        # Find conceptual compliance criterion/qualif (4902) for intrinsic aspect (=role), if any.
                        elif role_uid == expr2[lh_uid_col] and expr2[rel_type_uid_col] in self.subConcComplRelUIDs:
                            value_uid  = expr2[rh_uid_col]   # compliance criterion or def qualification
                            value_name = expr2[rh_name_col]
                            value_presence = True
                            break
                        elif role_uid == expr2[rh_uid_col] and expr2[rel_type_uid_col] in self.subConcComplRelUIDs:
                            value_uid  = expr2[lh_uid_col]   # compliance criterion or def qualification
                            value_name = expr2[lh_name_col]
                            value_presence = True
                            break

                # Determine preferred names for aspect, aspect_supertype, obj, and value 
                asp = self.uid_dict[aspect_uid]
                if len(asp.names_in_contexts) > 0:
                    lang_name, comm_name, aspect_name, descr = \
                               self.Determine_name_in_language_and_community(asp)
                else:
                    aspect_name = asp.name
                # Supertype name
                if len(asp.supertypes) > 0:
                    if len(asp.supertypes[0].names_in_contexts) > 0:
                        lang_name, comm_name, asp_supertype_name, descr = \
                                   self.Determine_name_in_language_and_community(asp.supertypes[0])
                    else:
                        asp_supertype_name = asp.supertypes[0].name
                else:
                    asp_supertype_name = 'unknown'
                # Obj name
                if len(obj.names_in_contexts) > 0:
                    lang_name, comm_name, object_name, descr = \
                               self.Determine_name_in_language_and_community(obj)
                else:
                    object_name = obj.name
                # Value name
                if value_uid != '':
                    value = self.uid_dict[value_uid]
                    lang_name, comm_name, value_name, descr = \
                           self.Determine_name_in_language_and_community(value)
                else:
                    value_name = ''

                # If not a subtype (subtype_level == 0) then create a row in the possibilities_model
                #   for any decomp_level
                if self.subtype_level == 0:
                    # Create header for possible characteristics of part (only preceding the first aspect)
                    if nr_of_aspects == 1:
                        poss_asp_of_obj_text = possible_aspect_text[self.GUI_lang_index] + obj_name
                        self.possibility_row[0] = obj.uid
                        self.possibility_row[1] = poss_asp_of_obj_text
                        self.possibility_row[2] = obj_name
                        self.possibilities_model.append(self.possibility_row[:])
                    
                    if len(self.possibilities_model) < self.max_nr_of_rows:
                        community_name = self.community_dict[obj.names_in_contexts[0][1]] # community uid
                        self.possibility_row[0] = obj.uid
                        self.possibility_row[1] = aspect_name + of_text[self.GUI_lang_index] + obj_name + ')'
                        self.possibility_row[2] = poss_asp_of_obj_text
                        print('Aspect', object_name, asp.uid, aspect_name, value_name, len(asp.supertypes)) # .kind
                        self.possibility_row[3] = asp_supertype_name
                        self.possibility_row[4] = community_name # of obj
                        self.possibility_row[5] = value_name
                        self.possibility_row[6] = uom_name
                        if self.possibility_row not in self.possibilities_model:
                            self.possibilities_model.append(self.possibility_row[:])
                        else:
                            print('Duplicate possibility row',len(self.possibilities_model), self.possibility_row)
                        self.possibility_row  = ['','','','','','','','','','','','','','','']
                
##                if value_presence == False:
##                    value_name = '' # noValuesText[self.GUI_lang_index]
##                    warnText  = ['  Warning: Kind of aspect','Waarschuwing: Soort aspect']
##                    valueMess = ['has no specification of (allowed) values.',\
##                                 'heeft geen specificatie van (toegelaten) waarden.']
##                    print('%s %s (%i) %s' % \
##                          (warnText[self.GUI_lang_index],aspect_name,aspect_uid,valueMess[self.GUI_lang_index]))
                #print('obj_i', value_presence, obj_i.name, nr_of_aspects, aspect_name, value_name, len(self.taxon_aspect_uids))

                if value_presence == True:
                    #print('Value present:', obj_i.name, aspect_name, value_name)
                    if len(self.query_table) < self.max_nr_of_rows:
                        self.query_table.append(expr2)
                    if self.decomp_level == 0:
                        # Build summary_view header add a column for aspects if not yet included
                        if value_presence == True and aspect_name not in self.taxon_column_names and \
                           len(self.taxon_column_names) <= 14:
                            #print('Summm_header', aspect_name, len(self.taxon_aspect_uids))
                            self.taxon_aspect_uids.append(aspect_uid)
                            self.taxon_column_names.append(aspect_name)
                            self.taxon_uom_names.append(uom_name)
                        self.taxon_ind = 3
                        #print('Sums:',len(self.taxon_aspect_uids), self.taxon_aspect_uids, self.taxon_column_names, value_name)
                        # Find column in taxon_row where value should be stored
                        for kind_uid in self.taxon_aspect_uids[4:]:
                            self.taxon_ind += + 1
                            # Build list of values conform list of aspects.
                            if kind_uid == aspect_uid:
                                #print('Aspects of phys:',len(self.taxon_aspect_uids), aspect_name, self.taxon_ind, value_name)
                                self.taxon_row[self.taxon_ind] = value_name
                                # Check whether there the uom corresponds with the table uom (when there is a value) 
                                if value_name != '' and uom_name != self.taxon_uom_names[self.taxon_ind]:
                                    #MessagesM.insert('end','\n
                                    print('Unit of measure {} ({}) of the value of {} differs from summary table header UoM {}'\
                                          .format(uom_name, uom_uid, aspect_name, self.taxon_uom_names[self.taxon_ind]))

##                    if self.subtype_level == 0:
##                        # Build composition_view header add a column for aspects if not yet included
##                        if value_presence == True and aspect_name not in self.possib_column_names and \
##                           len(self.possib_column_names) <= 15:
##                            #print('Compon_header', aspect_name, len(self.possib_aspect_uids))
##                            self.possib_aspect_uids.append(aspect_uid)
##                            self.possib_column_names.append(aspect_name)
##                            self.possib_uom_names.append(uom_name)
##                        self.possib_ind = 4
##                        #print('Sums:',len(self.possib_aspect_uids), self.possib_aspect_uids, self.possib_column_names, value_name)
##                        # Find column in possibility_row where value should be stored
##                        for kind_uid in self.possib_aspect_uids[5:]:
##                            self.possib_ind += + 1
##                            # Build list of values conform list of aspects.
##                            if aspect_uid == kind_uid:
##                                #print('Aspects of phys:',len(self.possib_aspect_uids), aspect_name, self.possib_ind, value_name)
##                                self.possibility_row[self.possib_ind] = value_name
##                                if uom_name != self.possib_uom_names[self.possib_ind]:
##                                    #MessagesM.insert('end','\n
##                                    print('Unit of measure {} ({}) of the value of {} differs from composition table header UoM {}'\
##                                          .format(uom_name, uom_uid, aspect_name, self.possib_uom_names[self.possib_ind]))

                    # Add a line of Line_type 3 to prod_model
                    subtype_level = 0 # not a subtype of object in focus
                    #self.line_nr += 1
                    if len(obj.supertypes) > 0:
                        supertype_uid  = obj.supertypes[0].uid
                        supertype_name = obj.supertypes[0].name
                    else:
                        supertype_uid  = ''
                        supertype_name = 'unknown'
                    self.Add_prod_model_line_type3(subtype_level, \
                                                   obj_i.uid, supertype_uid, aspect_uid, nr_of_aspects, obj.name, role, \
                                                   supertype_name, aspect_name, equality, value_name, uom_name, status)

                    # Determine implied part if any
                    # by determining whether the possessed aspect is an intrinsic aspect
                    # because rel_type is a <has by definition as intrinsic aspect a> relation (6149) or its subtype
                    # If that is the case, then it implies that 
                    #    there is an implied part of the object in focus that possesses the aspect
                    if expr[rel_type_uid_col] in ['6149', '5848']:
                        # Determine the implied part and its possessed aspect from the definition of the intrinsic aspect
                        intr_aspect = self.uid_dict[aspect_uid]
                        part_uid = ''
                        part_name = 'undefined'
                        asp_of_part_uid = ''
                        asp_of_part_name = 'undefined'
                        for rel_asp in intr_aspect.relations:
                            expr_asp = rel_asp.expression
                            
                            # If lh_uid is the kind of intr_aspect
                            # and rel_type is <is by definition an intrinsic aspect of a> (5738)
                            # then rh_obj is the kind of part  (and inverse)
                            if expr_asp[lh_uid_col] == aspect_uid and expr_asp[rel_type_uid_col] == '5738':
                                part_uid = expr_asp[rh_uid_col]
                                part_name = expr_asp[rh_name_col]
                            elif expr_asp[rh_uid_col] == aspect_uid and expr_asp[rel_type_uid_col] == '5738':
                                part_uid = expr_asp[lh_uid_col]
                                part_name = expr_asp[lh_name_col]

                            # If lh_uid is the kind of intr_aspect
                            # and rel_type is <is by definition an intrinsic> (5817)
                            # then rh_obj is the kind of aspect of the kind of part  (and inverse)
                            if expr_asp[lh_uid_col] == aspect_uid and expr_asp[rel_type_uid_col] == '5817':
                                asp_of_part_uid = expr_asp[rh_uid_col]
                                asp_of_part_name = expr_asp[rh_name_col]
                            if expr_asp[rh_uid_col] == aspect_uid and expr_asp[rel_type_uid_col] == '5817':
                                asp_of_part_uid = expr_asp[lh_uid_col]
                                asp_of_part_name = expr_asp[lh_name_col]
                                
                        #print('Whole {} has implied part ({}) {} identified with aspect ({}) {}.'\
                        #      .format(obj.name, part_uid, part_name, asp_of_part_uid, asp_of_part_name))
                        key = (part_uid, asp_of_part_uid)
                        self.implied_parts_dict[key] = (part_name, asp_of_part_uid, asp_of_part_name, \
                                                        equality,value_name,uom_name,status)

        #        if obj.category == 'kind of occurrence':
        #            # Build list of kinds of aspects (taxon_column_names) for SummaryView
        #            if aspect.kind not in self.occ_kinds: 
        #                nrOfAspOccKinds = nrOfAspOccKinds + 1                
        #                self.occ_aspects[nrOfAspOccKinds] = aspect_name
        #                self.occ_kinds  [nrOfAspOccKinds] = aspect.kind
        #                self.occ_uoms   [nrOfAspOccKinds] = uom_name
        #                self.taxon_ind = 3
        #                for kind_name in self.occ_kinds[4:]:
        #                    self.taxon_ind += + 1
        #                    if aspect.kind == kind_name:           # Build list of values conform list of aspects. Note: sumRow[0] = component
        #                        #print('Aspects of occ :',nrOfAspOccKinds,aspect_name,aspect.kind,self.taxon_ind,value_name)
        #                        occRow[self.taxon_ind] = value_name
        #                        if uom_name != self.occ_uoms[self.taxon_ind]:
        #                            MessagesM.insert('end','\nUnit of measure %s (%i) of the value of %s of kind %s differs from activity table header UoM \
        #    %s' % (uom_name,uom_uid,aspect_name,aspect.kind,self.occ_uoms[self.taxon_ind]))
        #                            
        #        elif self.decomp_level == 0:            # if not a kind of occurrence, then build header for summaryTable
            
        # If obj is object_in_focus (thus not a part) then create one or more rows in taxon_model             
        if self.decomp_level == 0:
            if len(obj.supertypes) > 0:
                # Create a row in the taxonomy per direct supertype
                for supertype in obj.supertypes:
                    lang_name, comm_name_super, preferred_name, descr = \
                               self.Determine_name_in_language_and_community(supertype)
                    self.taxon_row[2] = preferred_name  # of the supertype
                    if len(self.taxon_model) < self.max_nr_of_rows:
                        # If summary row is about object in focus, then make supertype of object in focus empty
                        # Because treeview parent (taxon_row[2] should be supertype or blank.
                        #print('Subtype_level:', self.subtype_level, obj.name, self.taxon_row)
                        if self.taxon_row[0] == obj.uid:
                            self.taxon_row[2] = ''

                        # If the supertype is the object_in_focus, then make the object a sub of the inter_row
                        if self.taxon_row[2] == obj.name:
                            self.taxon_row[2] = self.has_as_subtypes[self.GUI_lang_index]
                        self.taxon_model.append(self.taxon_row[:])
                        
                        # If the object is the object_in_focus, then insert an inter_row header line for the subtypes
                        if self.subtype_level == 0:
                            inter_row = [obj.uid, self.has_as_subtypes[self.GUI_lang_index], obj.name, '']
                            self.taxon_model.append(inter_row)

            self.taxon_row = ['','','','','','','','','','','','','','']

##        # If not a subtype (subtype_level == 0) and for any decomp_level create a row in possibilities_model
##        if self.subtype_level == 0:
##            if len(self.possibilities_model) < self.max_nr_of_rows:
####                if obj not in self.possib_objects:
####                    self.possib_objects.append(obj)
##                # If possibilities row is about object in focus, then make whole of object in focus empty
##                # Because treeview parent should be whole or blank.
##                if self.possibility_row[0] == obj.uid:
##                    self.possibility_row[2] = ''
##                if self.possibility_row not in self.possibilities_model:
##                    self.possibilities_model.append(self.possibility_row[:])
##                else:
##                    print('Duplicate composition row',len(self.possibilities_model), self.possibility_row)
##            self.possibility_row  = ['','','','','','','','','','','','','','','']
        
        return nr_of_aspects

    def Determine_supertypes(self, obj):
        # Collect a list of obj and its supertypes, including super_supers, etc.
        all_supers = []
        direct_supers = obj.supertypes
        if len(direct_supers) > 0:
            for super_d in direct_supers:
                if super_d not in all_supers:
                    all_supers.append(super_d)
            for super_i in all_supers:
                super_supers = super_i.supertypes
                if len(super_supers) > 0:
                    for super_super in super_supers:
                        if super_super not in all_supers:
                            all_supers.append(super_super)
        all_supers.append(obj)                    
        return all_supers

    def Determine_individuals(self, obj):
        ''' Determine whether a kind_in_focus (obj) is a classifier for individual things
            if so, then add individual things to taxonomy (taxon_model) of kinds
        '''
##        if self.individuals > 0:
##            for individual in self.individuals:
##                indiv_uid = individual.uid
        has_as_individuals = ['classifies as individual ', 'classificeert als individueel ']
        first_time = True
        
        for rel_obj in obj.relations:
            expr = rel_obj.expression
            # Find a classification relation for the kind_in_focus
            if expr[rel_type_uid_col] in self.sub_classif_uids:
                
                # Find the individual object that is classified
                if expr[lh_uid_col] == obj.uid:
                    indiv_uid = expr[rh_uid_col]
                elif expr[rh_uid_col] == obj.uid:
                    indiv_uid = expr[lh_uid_col]
                else:
                    continue
                # Store the expression in the query_table for display and possible export
                if len(self.query_table) < self.max_nr_of_rows:
                    self.query_table.append(expr)
                    
                # Individual thing uid is found via classification relation
                indiv = self.uid_dict[indiv_uid]

                # Insert an inter_row header for classified individual things in the taxonomy
                # the first time only
                if first_time == True:
                    header_text = has_as_individuals[self.GUI_lang_index]+obj.name
                    inter_row = [obj.uid, header_text, obj.name, '']
                    self.taxon_model.append(inter_row)
                    first_time = False

                # Create a row in the taxonomy for an individual thing under the header for individual things
                lang_name, community_name, preferred_name, descr = \
                           self.Determine_name_in_language_and_community(indiv)
                community_name = self.community_dict[indiv.names_in_contexts[0][1]] # community uid
                self.taxon_row[0] = indiv.uid
                self.taxon_row[1] = preferred_name
                self.taxon_row[2] = header_text
                self.taxon_row[3] = community_name

                self.taxon_model.append(self.taxon_row[:])
                self.taxon_row = ['','','','','','','','','','','','','','']
##                # Find aspects of individual object_in_focus
##                role = ''
##                nr_of_aspects = self.Find_aspects(indiv, role)
##
##                # Find parts and their aspects
##                self.part_head_req = True
##                self.Find_parts_and_their_aspects(indiv)

    def Find_parts_and_their_aspects(self, obj):
        """ Search for parts of individual object obj (and their aspects) in query_table.
            Store results in prod_model or occ_model
        """
        unknownClassifierText = ['unknown kind','onbekende soort']
        compHead = ['Part hierarchy','Compositie']
        partHead = ['Part of part','Deel van deel']
        par3Head = ['Further part','Verder deel']
        kindHead = ['Kind','Soort']
        kind_unknown = ['unknown', 'onbekend']

        #self.coll_of_subtype_uids = []
        self.nr_of_parts = 0
        self.decomp_level += + 1
        if self.decomp_level > 3:
            self.decomp_level += - 1
            return
        #if test: print('Indentation_level of parts of:',self.decomp_level,name,obj.uid)
        
        # Search for <has as part> relation or any of its subtypes
        part_uid = ''
        for rel_obj in obj.relations:
            expr = rel_obj.expression 
            if expr[rel_type_uid_col] in self.subComposUIDs:
                if expr not in self.query_table and expr not in self.query_table:
                    self.query_table.append(expr)
                # If base phrase <is a part of> and right hand is the object in focus then lh is a part
                if expr[phrase_type_uid_col]   == basePhraseUID:     # base
                    if obj.uid == expr[rh_uid_col]:
                        part_uid = expr[lh_uid_col]
                        
                # If inverse phrase <has as part> and left hand is the object in focus then rh is a part
                elif expr[phrase_type_uid_col] == inversePhraseUID:     # inverse
                    if obj.uid == expr[lh_uid_col]:
                        part_uid = expr[rh_uid_col]
                else:
                    print('Phrase type uid {} incorrect'.format(expr[phrase_type_uid_col]))
                    continue

                if part_uid != '':
                    # There is an explicit part found; create part_header, prod_head_4, the first time only
                    if self.part_head_req == True:
                        self.line_nr += 1
                        prod_head_4 = ['','','',self.line_nr, compHead[self.GUI_lang_index], partHead[self.GUI_lang_index],\
                                     par3Head[self.GUI_lang_index], kindHead[self.GUI_lang_index],'','','','','']
                        if len(self.prod_model) < self.max_nr_of_rows:
                            self.prod_model.append(prod_head_4) # Header of part list
                        self.part_head_req = False
                    part = self.uid_dict[part_uid]

##                    if len(self.query_table) < self.max_nr_of_rows and expr not in self.query_table:
##                        self.query_table.append(expr)
                    status = expr[status_col]

                    # Verify if the classification of the part is known
                    if len(part.classifiers) == 0:
                        part_kind_uid  = ''
                        part_kind_name = kind_unknown[self.GUI_lang_index]
                    else:
                        part_kind_uid  = part.classifiers[0].uid
                        # Determine name etc. of the kind that classifies the part
                        if len(part.classifiers[0].names_in_contexts) > 0:
                            #print('Part classifier names', self.reply_lang_pref_uids, part.classifiers[0].names_in_contexts)
                            lang_name, comm_name, part_kind_name, descrOfKind = \
                                       self.Determine_name_in_language_and_community(part.classifiers[0])
                        else:
                            part_kind_name = part.classifiers[0].name
                            #print('Part_classifier_name', part_kind_name)
                            comm_name = 'unknown'
                            
                    # Determine the preferred name of the part
                    if len(part.names_in_contexts) > 0:
                        lang_name, community_name, part_name, descrOfKind = \
                                       self.Determine_name_in_language_and_community(part)
                    else:
                        part_name = part.name
                        community_name = 'unknown'
                        print('Part {} has no defined community name'.format(part.name))
                        
                    self.indiv_row[0] = part.uid
                    self.indiv_row[1] = part_name #part.names_in_contexts[0][2] # obj.name
                    self.indiv_row[2] = obj.name
                    self.indiv_row[3] = part_kind_name
                    self.indiv_row[4] = community_name
                    #self.coll_of_subtype_uids.append(part.uid)
                                   
                    # Search for aspects of part
                    role = ''
                    nr_of_aspects = self.Find_aspects(part, role)
                    
                    # if no aspects of part found, record part only (in prod_model)
                    if nr_of_aspects == 0: 
                        self.line_nr += + 1
                        if self.decomp_level == 1:
                            prod_line_4 = [part.uid,part_kind_uid,'',self.line_nr,part.name,'','',\
                                           part_kind_name,'','','','','',status]
                        elif self.decomp_level == 2:
                            prod_line_4 = [part.uid,part_kind_uid,'',self.line_nr,'',part.name,'',\
                                           part_kind_name,'','','','','',status]
                        elif self.decomp_level == 3:
                            prod_line_4 = [part.uid,part_kind_uid,'',self.line_nr,'','',part.name,\
                                           part_kind_name,'','','','','',status]
                        if self.decomp_level < 4:
                            if len(self.prod_model) < self.max_nr_of_rows:
                                self.prod_model.append(prod_line_4)
                        
                    # Search for parts of part and their aspects
                    self.Find_parts_and_their_aspects(part)
                
        self.decomp_level += - 1        
        #if nrOfParts == 0:              # Check whether nr of parts = 0
        #    print('\nNo parts found in query results for {} ({})'.format(obj.name, obj.uid))

    def Find_kinds_of_parts_and_their_aspects(self, obj):
        """ Search for explicit kinds of parts and combine them with implied kinds of parts"""

        compHead = ['Part hierarchy','Compositie']
        partHead = ['Part of part','Deel van deel']
        par3Head = ['Further part','Verder deel']
        kindHead = ['Kind','Soort']
        
        role = ''
        self.part_head_req = True
        # Search for kinds of parts of object_in_focus
        for rel_obj in obj.relations:
                expr = rel_obj.expression
                if expr[lh_uid_col] == obj.uid and expr[rel_type_uid_col] in self.subConcComposUIDs\
                   and expr[phrase_type_uid_col] == '1986':
                    part_uid   = expr[rh_uid_col]
                    part_name  = expr[rh_name_col]
                    #role_uid     = expr[rh_role_uid_col]
                    #role_name    = expr[rh_role_name_col]
                elif expr[rh_uid_col] == obj.uid and expr[rel_type_uid_col] in self.subConcComposUIDs\
                     and expr[phrase_type_uid_col] == '6066'  :
                    part_uid   = expr[lh_uid_col]
                    part_name  = expr[lh_name_col]
                    #role_uid     = expr[lh_role_uid_col]
                    #role_name    = expr[lh_role_name_col]
                else:
                    continue
                
                # There is an explicit kind of part found; create part_header in kind_model, the first time only
                #print('Kind of part', part_name)
                if self.part_head_req == True:
                    self.line_nr += 1
                    prod_head_4 = ['','','',self.line_nr, compHead[self.GUI_lang_index], partHead[self.GUI_lang_index],\
                                 par3Head[self.GUI_lang_index], kindHead[self.GUI_lang_index],'','','','','']
                    if len(self.kind_model) < self.max_nr_of_rows:
                        # Add header of part to kind_model
                        self.kind_model.append(prod_head_4)
                    self.part_head_req = False

                # Add the expression to the query_table output table
                if len(self.query_table) < self.max_nr_of_rows:
                    self.query_table.append(expr)

                # Determine preferred name of object (= kind)
                if len(obj.names_in_contexts) > 0:
                    lang_name, community_name, obj_name, descr_of_obj = \
                               self.Determine_name_in_language_and_community(obj)
                else:
                    obj_name = obj.name

                # Determine preferred name of part (= kind)
                part = self.uid_dict[part_uid]
                if len(part.names_in_contexts) > 0:
                    lang_name, community_name, part_name, descr_of_part = \
                               self.Determine_name_in_language_and_community(part)
                else:
                    part_name = part.name
                    community_name = 'unknown'

                # Determine preferred name of first supertype of part
                if len(part.supertypes) > 0:
                    if len(part.supertypes[0].names_in_contexts) > 0:
                        lang_name, comm_kind_name, part_kind_name, descr_of_kind = \
                                   self.Determine_name_in_language_and_community(part.supertypes[0])
                    else:
                        part_kind_name = part.supertypes[0].name
                else:
                    part_kind_name = 'unknown'

                # Create row about possible aspect of kind in possibilities_model
                self.possibility_row[0] = part.uid
                self.possibility_row[1] = part_name
                self.possibility_row[2] = obj_name
                self.possibility_row[3] = part_kind_name
                self.possibility_row[4] = community_name # of part
                # Add possibility for part to possibilities_model
##                if part not in self.possib_objects:
##                    self.possib_objects.append(part)
                if self.possibility_row not in self.possibilities_model:
                    self.possibilities_model.append(self.possibility_row[:])

                # Search for aspects of the kind of part
                nr_of_aspects = self.Find_kinds_of_aspects(part, role)
                if nr_of_aspects > 0:
                    # Verify consistency between aspect values and implied aspect values.
                    # === to be completed ===
                    
                    #print('*** Nr of aspects to be verified', nr_of_aspects)
                    # Verify whether there are implied parts with aspect values
                    if len(self.implied_parts_dict) > 0:
                        for key, implied_tuple in self.implied_parts_dict:
                            if part.uid == key[0]:
                                print('Object ({}) {} has part ({}) {} with implied aspect ({}) {}.'.format\
                                      (obj.uid, obj.names_in_contexts[0][2], key[0], implied_tuple(0), \
                                       implied_tuple(1), implied_tuple(2)))
                                del self.implied_parts_dict[key]

        # If there are implied kinds of parts left, then create kind_model lines.
        if len(self.implied_parts_dict) > 0:
            #print('Nr of implied parts', len(self.implied_parts_dict))

            # There is an implied part left; thus create a part_header, the first time only
            if self.part_head_req == True:
                self.line_nr += 1
                prod_head_4 = ['','','',self.line_nr, compHead[self.GUI_lang_index], partHead[self.GUI_lang_index],\
                             par3Head[self.GUI_lang_index], kindHead[self.GUI_lang_index],'','','','','']
                if len(self.kind_model) < self.max_nr_of_rows:
                    self.kind_model.append(prod_head_4) # Header of part list
                self.part_head_req = False

            # Create kind_model lines of part
            for key, implied_tuple in self.implied_parts_dict.items():
                self.decomp_level = 1
                nr_of_aspects = 1
                part_name = implied_tuple[0]
                if len(self.uid_dict[key[0]].supertypes) > 0:
                    part_kind_uid  = self.uid_dict[key[0]].supertypes[0].uid
                    part_kind_name = self.uid_dict[key[0]].supertypes[0].name
                else:
                    part_kind_uid  = ''
                    part_kind_name = 'kind'
                aspect_name = implied_tuple[2]
                equality = implied_tuple[3]
                value_name = implied_tuple[4]
                uom_name = implied_tuple[5]
                status = 'implied'
                subtype_of_part_level = 0
##                print('Object ({}) {} has implied part ({}) {} with aspect ({}) {}.'.format\
##                      (obj.uid, obj.names_in_contexts[0][2], key[0], implied_tuple[0], \
##                       implied_tuple[1], implied_tuple[2]))
                self.Add_prod_model_line_type3(subtype_of_part_level, \
                                               key[0], part_kind_uid, implied_tuple[1], nr_of_aspects, part_name, role, \
                                               part_kind_name, aspect_name, equality, value_name, uom_name, status)
                
    def Add_prod_model_line_type3(self, subtype_level, \
                                  part_uid, part_kind_uid, aspect_uid, nr_of_aspects, part_name, role, part_kind_name, \
                                  aspect_name, equality, value_name, uom_name, status):
        # Create a line_type 3 for product model view
        self.line_nr += 1
        if self.decomp_level == 1 and nr_of_aspects <= 1:     # decomp_level = 0 means object in focus, 1 means: part
            prod_line_3 = [part_uid, part_kind_uid, aspect_uid, self.line_nr,part_name,role,''  ,part_kind_name,aspect_name,'',equality,value_name,uom_name,status]
        elif self.decomp_level == 2 and nr_of_aspects == 1:   # decomp_level = 2 means: part of part
            prod_line_3 = [part_uid, part_kind_uid, aspect_uid, self.line_nr,role,part_name,''  ,part_kind_name,aspect_name,'',equality,value_name,uom_name,status]
        elif self.decomp_level == 3 and nr_of_aspects == 1:
            prod_line_3 = [part_uid, part_kind_uid, aspect_uid, self.line_nr,''  ,role,part_name,part_kind_name,aspect_name,'',equality,value_name,uom_name,status]
            
        elif subtype_level > 0 and nr_of_aspects == 1:     # sub_level = 1 means: first decomp_level subtype
            prod_line_3 = [part_uid, part_kind_uid, aspect_uid, self.line_nr,part_name,role,''  ,part_kind_name,aspect_name,'',equality,value_name,uom_name,status]
        else:
            prod_line_3 = [part_uid, part_kind_uid, aspect_uid, self.line_nr,'','','','',aspect_name,'',equality,value_name,uom_name,status]
            
        if len(self.kind_model) < self.max_nr_of_rows:
            self.kind_model.append(prod_line_3)
            
    def Find_aspects(self, indiv, role):
        """ Search for aspects of an individual thing (indiv) and their qualifications or quantifications
            and store results in lines in prod_model
            indiv     = the individual thing
            kind.name = the name of the kind of individual thing (for messages only)
            decomp_level    = decomposition_level: 0 = objectInFocus, 1 = part, 2 = part of part, etc.
            categoryInFocus = category of the object in focus, being individual or phys object or occurrence
            The prod_model lineType is 3A: aspects of a product - conform the header line for aspects (line type 3)
        """

        # Search for aspects and their values
        nr_of_aspects = 0  # nr of found aspects for this indiv object
        aspect_uid    = ''
        aspect_name   = ''

        equality = '='
        for rel_obj in indiv.relations:
            expr = rel_obj.expression
            qual_aspect = False
            # Add each expression to the query_table with each idea about the object in focus
            if len(self.query_table) < self.max_nr_of_rows and expr not in self.query_table:
                self.query_table.append(expr)
                
            # Find possession of aspect relations (or its subtypes)
            if indiv.uid == expr[lh_uid_col] and expr[rel_type_uid_col] in self.subPossAspUIDs:
                if expr[phrase_type_uid_col] == basePhraseUID:
                    aspect_uid   = expr[rh_uid_col]
                else:
                    print('Phrase type uid of idea {} incompatible with expression'.format(expr.uid))
            elif indiv.uid == expr[rh_uid_col] and expr[rel_type_uid_col] in self.subPossAspUIDs: # inverse
                if expr[phrase_type_uid_col] == inversePhraseUID:
                    aspect_uid   = expr[lh_uid_col]
                else:
                    print('Phrase type uid of idea {} incompatible with expression'.format(expr.uid))
            else:
                # Search for possession of a qualitative aspect relations and <is made of>
                if indiv.uid == expr[lh_uid_col] and expr[rel_type_uid_col] in ['5843', '5423']:
                    if expr[phrase_type_uid_col] == basePhraseUID:
                        aspect_uid = expr[rh_uid_col]
                        qual_aspect = True
                elif indiv.uid == expr[rh_uid_col] and expr[rel_type_uid_col] in ['5843', '5423']:
                    if expr[phrase_type_uid_col] == inversePhraseUID:
                        aspect_uid = expr[lh_uid_col]
                        qual_aspect = True
                else:
                    continue
##                if expr[rel_type_uid_col] in self.sub_classif_uids:
##                    if len(self.query_table) < self.max_nr_of_rows and expr not in self.query_table:
##                        self.query_table.append(expr)
##                #print('classif:', expr[lh_name_col], expr[rel_type_name_col], expr[rh_name_col])

            # Aspect found or qualitative aspect found
##            # Add the found <has as aspect> relation expression to the query_table
##            if len(self.query_table) < self.max_nr_of_rows and expr not in self.query_table:
##                self.query_table.append(expr)
            #print('aspect:', expr[lh_name_col], expr[rel_type_name_col], expr[rh_name_col])
            status = expr[status_col]
            nr_of_aspects += 1
            #self.line_nr  += 1

            # Find the aspect object of the <has as aspect> relation or the qualitative aspect
            aspect = self.uid_dict[aspect_uid]

            # Verify if the individual object is classified
            if len(indiv.classifiers) == 0:
                indiv.kind_uid  = ''
                indiv.kind_name = 'unknown kind'
            else:
                # Determine the preferred name of the first classifier of the individual object
                lang_name_cl, comm_name_cl, pref_cl_name, descr = \
                              self.Determine_name_in_language_and_community(indiv.classifiers[0])
                indiv.kind_uid  = indiv.classifiers[0].uid
                indiv.kind_name = pref_cl_name

            # Verify if the aspect of the individual object is classified (when not being a qualitative aspect)
            if qual_aspect == False:
                # Normal individual aspect found (not a qualitative aspect, such as a substance
                aspect_name = aspect.name
                if len(aspect.classifiers) == 0:
                    aspect.kind_uid  = ''
                    aspect.kind_name = 'unknown kind'
                else:
                    # Determine the preferred name of the first classifier of the individual aspect
                    #print('Lang_prefs for classifier of aspect', self.reply_lang_pref_uids, aspect.classifiers[0].names_in_contexts)
                    lang_name_as, comm_name_as, pref_kind_name, descr = \
                                  self.Determine_name_in_language_and_community(aspect.classifiers[0])
                    aspect.kind_uid  = aspect.classifiers[0].uid
                    aspect.kind_name = pref_kind_name

                # Determine the value of the aspect
                value_uid    = ''
                value_name   = ''
                uom_uid      = ''
                uom_name     = ''

                # Find the first qualification or quantification of the aspect
                for rel_obj in aspect.relations:
                    expr = rel_obj.expression
                    if len(self.query_table) < self.max_nr_of_rows and expr not in self.query_table:
                        self.query_table.append(expr)
                    if aspect_uid == expr[lh_uid_col]:
                        # Find the first expression that qualifies or quantifies the aspect
                        # by searching for the kinds of qualifying relations or their subtypes
                        if expr[rel_type_uid_col] in self.subQualUIDs or expr[rel_type_uid_col] in self.subQuantUIDs:
                            if len(self.query_table) < self.max_nr_of_rows:
                                value_uid = expr[rh_uid_col]                           
                                value_name= expr[rh_name_col]
                                uom_uid   = expr[uom_uid_col]
                                uom_name  = expr[uom_name_col]
                        else:
                            continue
                    elif aspect_uid == expr[rh_uid_col]:
                        # Find the first expression that qualifies or quantifies the aspect
                        # by searching for the kinds of relations or their subtypes
                        if expr[rel_type_uid_col] in self.subQualUIDs or expr[rel_type_uid_col] in self.subQuantUIDs:
                            if len(self.query_table) < self.max_nr_of_rows:
                                value_uid = expr[lh_uid_col]                           
                                value_name= expr[lh_name_col]
                                uom_uid   = expr[uom_uid_col]
                                uom_name  = expr[uom_name_col]
                        else:
                            continue
                    else:
                        continue

                    # If the value_uid is not a whole number or is outside the standard number range, then
                    #    determine the value name in the preferred language (and in the preferred language community)
                    #print('Value', aspect_uid, value_uid, value_name, expr[0:25])
                    numeric_uid, integer = Convert_numeric_to_integer(value_uid)
                    if integer == False or (numeric_uid < 1000000000 or numeric_uid >= 3000000000):
                        value = self.uid_dict[value_uid]
                        lang_name, comm_name, value_name, descr = \
                               self.Determine_name_in_language_and_community(value)
                        
                    # Aspect value found: add expression to result table
                    if len(self.query_table) < self.max_nr_of_rows and expr not in self.query_table:
                        self.query_table.append(expr)
            else:
                # Qualitative aspect found (e.g. a substance such as PVC)
                substance = self.uid_dict['431771']     # subtance or stuff
                lang_name, comm_name, pref_kind_name, descr = \
                           self.Determine_name_in_language_and_community(substance)
                aspect.kind_name = pref_kind_name
                aspect.kind_uid  = '431771'
                uom_uid  = ''
                uom_name = ''
                value_uid  = aspect.uid
                lang_name, comm_name, value_name, descr = \
                           self.Determine_name_in_language_and_community(aspect)
                #value_name = aspect.name
                aspect_name = ''
                
            # If the object is the object_in_focus and not one of its parts, then collect the aspect in a summary_table
            if self.decomp_level == 0:
                # Build summary_view table header with list of kinds of aspects (summ_column_names)
                if aspect.kind_name not in self.summ_column_names and len(self.summ_column_names) <= 14:                
                    self.summ_aspect_uids.append(aspect.kind_uid)
                    self.summ_column_names.append(aspect.kind_name)
                    self.summ_uom_names.append(uom_name)
                self.summ_ind = 3
                for kind_uid in self.summ_aspect_uids[4:]:
                    self.summ_ind += + 1
                    # Build list of values conform list of aspects. Note: sumRow[0] = component
                    if aspect.kind_uid == kind_uid:
                        #print('Aspects of phys:', indiv.name, len(self.summ_aspect_uids), \
                        #      aspect_name, aspect.kind_name, self.summ_ind, value_name)
                        self.summary_row[self.summ_ind] = value_name
                        if uom_name != self.summ_uom_names[self.summ_ind]:
                            #self.MessagesQ.insert('end','\n
                            print('Unit of measure {} ({}) of the value of {} differs from summary table header UoM {}.'.\
                                  format(uom_name, uom_uid, aspect_name, self.summ_uom_names[self.summ_ind]))

            # If the object is the object_in_focus and not one of its subtypes, then collect the aspect in an indiv_table
            if self.subtype_level == 0:
                # Build individual_view table header with list of aspects (indiv_column_names)
                #print('Aspect kind', aspect.uid, aspect_name)
                if aspect.kind_name not in self.indiv_column_names and len(self.indiv_column_names) <= 15:                
                    self.indiv_aspect_uids.append(aspect.kind_uid)
                    self.indiv_column_names.append(aspect.kind_name)
                    self.indiv_uom_names.append(uom_name)
                self.indiv_ind = 4
                for kind_uid in self.indiv_aspect_uids[5:]:
                    self.indiv_ind += + 1
                    # Build list of values conform list of aspects. Note: sumRow[0] = component
                    if aspect.kind_uid == kind_uid:
                        #print('Aspects of phys:', indiv.name, len(self.indiv_aspect_uids), \
                        #      aspect_name, aspect.kind_name, self.indiv_ind, value_name)
                        self.indiv_row[self.indiv_ind] = value_name
                        if uom_name != self.indiv_uom_names[self.indiv_ind]:
                            if uom_name == '':
                                print('Unit of measure of the value of {} is missing.'.format(aspect_name))
                            else:
                                print('Unit of measure {} ({}) of the value of {} differs from table header UoM {}.'.\
                                      format(uom_name, uom_uid, aspect_name, self.indiv_uom_names[self.indiv_ind]))

            # Verify if aspect has a known value
            if value_uid == '':
                unknownVal = ['unknown value','onbekende waarde']
                value_name = unknownVal[self.GUI_lang_index]
                warnText  = ['  Warning: Aspect','Waarschuwing: Aspect']
                valueMess = ['has no value.','heeft geen waarde.']
                #self.MessagesQ.insert('end','\n
                print('{} {} ({}) {}'.format(warnText[self.GUI_lang_index], aspect_name,aspect_uid, \
                                             valueMess[self.GUI_lang_index]))
            else:
                # Determine (in)equality symbol
                if expr[rel_type_uid_col] == '5026':
                    equality = '>'
                elif expr[rel_type_uid_col] == '5027':
                    equality = '<'
                elif expr[rel_type_uid_col] == '5489':
                    equality = '>='
                elif expr[rel_type_uid_col] == '5490':
                    equality = '<='
                        
            # Create prod_model text line for output view
            self.line_nr += 1
            #print('Aspect of obj.:', self.decomp_level, nr_of_aspects, indiv.name, aspect_name)
            if self.decomp_level == 0 and nr_of_aspects == 1:
                prod_line_3 = [indiv.uid   , indiv.kind_uid, aspect_uid, \
                               self.line_nr, indiv.name, role,''  ,indiv.kind_name,\
                               aspect_name , aspect.kind_name, equality, value_name, uom_name, status]
            elif self.decomp_level == 1 and nr_of_aspects == 1:
                prod_line_3 = [indiv.uid   , indiv.kind_uid, aspect_uid, \
                               self.line_nr, indiv.name, role,''  ,indiv.kind_name,\
                               aspect_name , aspect.kind_name, equality, value_name, uom_name, status]
            elif self.decomp_level == 2 and nr_of_aspects == 1:
                prod_line_3 = [indiv.uid   , indiv.kind_uid, aspect_uid, \
                               self.line_nr, role, indiv.name,''  ,indiv.kind_name,\
                               aspect_name , aspect.kind_name, equality, value_name, uom_name, status]
            elif self.decomp_level == 3 and nr_of_aspects == 1:
                prod_line_3 = [indiv.uid   , indiv.kind_uid, aspect_uid, \
                               self.line_nr,'' , role, indiv.name, indiv.kind_name,\
                               aspect_name , aspect.kind_name, equality, value_name, uom_name, status]
            else:
                prod_line_3 = [indiv.uid   , indiv.kind_uid, aspect_uid, \
                               self.line_nr,'','','','',\
                               aspect_name , aspect.kind_name, equality, value_name, uom_name, status]
            if len(self.prod_model) < self.max_nr_of_rows:
                self.prod_model.append(prod_line_3)

        # If aspect is possessed by object_in_focus (thus not possessed by a part) then add row to summ_model
        #print('Indiv', self.decomp_level, indiv.uid, self.summary_row)
        if self.decomp_level == 0:
            if len(self.summ_model) < self.max_nr_of_rows:
                if indiv not in self.summ_objects:
                    self.summ_objects.append(indiv)
                    # If summary row is about object in focus, then make parent of object in focus blank
                    # because treeview requires that parent is known or blank
                    if self.summary_row[0] == self.object_in_focus.uid:
                        self.summary_row[2] = ''
                    self.summ_model.append(self.summary_row[:])

            self.summary_row = ['','','','','','','','','','','','','','']

        # For whole and for parts of whole create a row in indiv_model (not for occurences)
        if self.occ_in_focus != 'occurrence' and len(self.indiv_model) < self.max_nr_of_rows:
            if indiv not in self.indiv_objects:
                self.indiv_objects.append(indiv)
                # If indiv row is about object in focus, then make whole of object in focus blank
                # because treeview requires that whole is known or blank
                if self.indiv_row[0] == self.object_in_focus.uid:
                    self.indiv_row[2] = ''
                self.indiv_model.append(self.indiv_row[:])

        self.indiv_row = ['','','','','','','','','','','','','','']
        
        return nr_of_aspects

    def Find_information_about_object(self, obj):
        ''' Search for information and files about the object obj (kind or individual)
            (and its supertypes?) and build info_model
        '''
        obj_head          = ['Object'      ,'Object']
        info_head         = ['Document'    ,'Document']
        dir_head          = ['Directory'   ,'Directory']
        kind_of_doc_head  = ['Kind'        ,'Soort']
        file_head         = ['File'        ,'File']
        kind_of_file_head = ['Kinf of file','Soort file']
        status_head       = ['Status'      ,'Status']
        descr_avail_text  = ['Description available', 'Omschrijving beschikbaar']

        info_header = True

        for rel_obj in obj.relations:
            expr = rel_obj.expression
            # Verify whether object <is a kind that is described by> (5620) information
            #                       <is described by information>    (1273) information
            if expr[rel_type_uid_col] in ['5620', '1911', '5631', '1273']:
                if expr[lh_uid_col] == obj.uid:
                    info_uid = expr[rh_uid_col]
                elif expr[rh_uid_col] == obj.uid:
                    info_uid = expr[lh_uid_col]
                else:
                    continue

                # Information is identified.
##                self.query_table.append(expr)
                info = self.uid_dict[info_uid]
                # Create header line_type 8 info, only the first time for prod_model or kind_model
                if info_header:
                    self.line_nr += + 1
                    prod_head_8 = ['','','',self.line_nr, info_head[self.GUI_lang_index], dir_head[self.GUI_lang_index],'',\
                                   kind_of_doc_head[self.GUI_lang_index]           , file_head[self.GUI_lang_index],\
                                   kind_of_file_head[self.GUI_lang_index],'','','',status_head[self.GUI_lang_index]]
                    #print('obj.cat',obj.category)
                    if obj.category in ['kind', 'kind of physical object', 'kind of occurrence', 'kind of aspect', \
                                        'kind of role', 'kind of relation']:
                        self.kind_model.append(prod_head_8)
                    else:
                        self.prod_model.append(prod_head_8)
                    info_header = False

                # Determine the name of the supertype of info and verify if info is presented on a carrier.
                # And store full description
                qualified = False
                presented = False
                super_info_uid  = ''
                super_info_name = 'unknown'
                info.description = ''
                for rel_info in info.relations:
                    info_expr = rel_info.expression
                    info_status = info_expr[status_col]
                    # Determine the qualifier of the info (its supertype)
                    if info_expr[rel_type_uid_col] in self.specialRelUIDs:
                        super_info_uid   = info_expr[rh_uid_col]
                        super_info_name  = info_expr[rh_name_col]
                        info.description = info_expr[full_def_col]
                        qualified = True
                        self.query_table.append(info_expr)
                        
                    # Verify whether info <is presented on> (4996) physical object (typically an electronic data file)
                    #        or info <is presented on at least one of> (5627) collection of physical objects
                    elif info_expr[rel_type_uid_col] in ['4996', '5627']:
                        if info_expr[lh_uid_col] == info.uid:
                            carrier_uid = info_expr[rh_uid_col]
                        elif info_expr[rh_uid_col] == info.uid:
                            carrier_uid = info_expr[lh_uid_col]
                        else:
                            continue
                        
                        # Info is presented on a carrier
                        presented = True
                        self.query_table.append(info_expr)
                        carrier = self.uid_dict[carrier_uid]
                        if len(carrier.classifiers) > 0:
                            carrier_kind_name = carrier.classifiers[0].name
                        else:
                            carrier_kind_name = 'unknown'

                        # Find directory where carrier file is located
                        directory_name = ''
                        for rel_carrier in carrier.relations:
                            car_expr = rel_carrier.expression
                            # Verify whether the carrier <is an element of> (1227) directory
                            if car_expr[rel_type_uid_col] == '1227':
                                if car_expr[lh_uid_col] == carrier.uid:
                                    directory_uid = car_expr[rh_uid_col]
                                elif info_expr[rh_uid_col] == carrier.uid:
                                    directory_uid = car_expr[lh_uid_col]
                                else:
                                    continue
                                # Directory for carrier is found
                                directory = self.uid_dict[directory_uid]
                                self.query_table.append(car_expr)
                                directory_name = directory.name

                        if directory_name == '':
                            print('== Warning: Directory name for file {} is unknown.'.format(carrier.name))
                            # Testmessage for display in log
                            message = '\n== Warning: Directory name for file ' + carrier.name + ' is unknown.'
                            self.messages.append(message)

                        # Store info about object in info_model
                        #print('Carrier {} is located on directory {}.'.format(carrier.name, directory_name))
                        info_row = [info.uid, obj.uid, carrier.uid, directory_name,\
                                    info.name, super_info_name, obj.name, \
                                    carrier.name, carrier_kind_name]
                        self.info_model.append(info_row)
                        
                        # Store info about object in prod_model or kind_model
                        self.line_nr += + 1
                        prod_line_8 = [info.uid, super_info_uid, carrier.uid, self.line_nr, info.name, directory_name, '',\
                                       super_info_name, carrier.name, carrier_kind_name,'','','',info_status]
                        if obj.category in ['kind', 'kind of physical object', 'kind of occurrence', 'kind of aspect', \
                                            'kind of role', 'kind of relation']:
                            self.kind_model.append(prod_line_8)
                        else:
                            self.prod_model.append(prod_line_8)

                if qualified == False:
                    print('Warning: Information {} is not qualified'.format(info.name))
                    
                if presented == False:
                    # Store info about object in info_model
                    info_row = [info.uid, obj.uid, info.description, '', \
                                info.name, super_info_name, obj.name, '',descr_avail_text[self.GUI_lang_index], '', '']
                    self.info_model.append(info_row)
                    
                    # Store info about object in prod_model or kind_model
                    self.line_nr += + 1
                    prod_line_8 = [info.uid, super_info_uid, obj.uid, self.line_nr, info.name, '', '', \
                                   super_info_name, '', '','','','',info_status]
                    if obj.category in ['kind', 'kind of physical object', 'kind of occurrence', 'kind of aspect', \
                                        'kind of role', 'kind of relation']:
                        self.kind_model.append(prod_line_8)
                    else:
                        self.prod_model.append(prod_line_8)

#---------------------------------------------------------------
    def SolveUnknown(self, searchString, string_commonality):
        """Determine the available options (UIDs and names) in the dictionary that match the searchString.
        Collect options in lh, rel and rh optionsTables for display and selection.

        - searchString = the string to be found in Gel_dict with corresponding lang_uid and comm_uid.
        - string_commonality is one of:
          cipi, cspi, cii, csi, cifi, csfi (case (in)sensitive partial/front end identical

        Returnparameters:
        == options (Lh, Rel or Rh):
           optionNr, whetherKnown, langUIDres, commUIDres, resultString, resultUID, isCalled, objectTypeKnown, kind (of resultUID).
           OptionTables have basically the same table structure as the namingTable, but is extended with extra columns.

        == Gel_dict columns: [lang_uid, comm_uid, term], [UID, naming_uid, part_def]
         
         Process: Determine whether searchString equals 'what' etc. or whether it occurs one or more times in vocabulary Gel_dict.
         Collect options in OptionTables, for selecting a preferred option.
        """
        self.test = False
        whetherKnown  = 'unknown'    # initialize indicator whether the search string is an unknown (UID 1-99) or not.
        objectTypeKnown = 'unknown'
        option        = []
        options       = []
        unknownTerms = ['','?','any','what','which','who','where', \
                        'wat', 'welke', 'wie', 'waar']
        foundUID = ''

        # If search string denotes an unknown from the list unknownTerms
        # then add unknown to the list of options
        if searchString in unknownTerms:
            if searchString == '':
                resultString = 'blank';
            else:
                resultString = searchString
            if resultString not in self.names_of_unknowns:
                # Create an object for the (list of) unknown(s)
                self.unknown_quid += 1
                unknown = Anything(str(self.unknown_quid), resultString)
                self.unknowns.append(unknown)
                self.names_of_unknowns.append(resultString)
                optionNr = 1
                option.append(optionNr) 
                option.append(whetherKnown)
                option.append(self.GUI_lang_pref_uids[1])
                option.append(self.comm_pref_uids[0])
                option.append(resultString)
                option.append(str(self.unknown_quid))
                option.append(is_called_uid)
                option.append(objectTypeKnown)
                option.append(self.unknown_kind[self.GUI_lang_index])

                options.append(option)
                foundUID = str(self.unknown_quid)
            else:
                # Search in earlier collected list of unknowns for object with name searchString
                for unknown in self.unknowns:
                    if unknown.name == searchString:
                        foundUID = unknown.uid
                        continue
            if foundUID == '':
                print('Something wrong')
            return foundUID, options
        
        # Search for full searchString in GellishDict   (was nameList in namingTable)
        candidates = self.Query_network_dict(searchString, string_commonality)

        # Collect found option in 'options' list for display and selection
        if len(candidates) > 0:
            #print ("nr of candidates:",len(candidates), self.GUI_lang_pref_uids)
            optionNr = 0
            for candidate in candidates:
                # Only add the candidate if uid of language corresponds with uid from GUI_lang_pref_uids
                # because the query is in the GUI_language
                if candidate[0][0] not in self.GUI_lang_pref_uids:
                    continue
                whetherKnown = 'known'
                option = []
                optionNr = optionNr + 1
                option.append(optionNr)
                option.append(whetherKnown)
                # Add candidate fields to option (in column (2,3,4),(5,6,7)
                for part in candidate:
                    for field in part:
                        option.append(field)
                #print ("option:",len(candidates), option)

                #== option: optionNr, whetherKnown, langUID, commUID, resultString, \
                #           resultUID, objectTypeKnown, kind_name (of resultUID).

                # If result_uid is a known uid (being alphanumeric or >= 100) then
                # then find the object and its supertype or classifier
                # and add the object to the list of options
                
                result_uid, integer = Convert_numeric_to_integer(option[5])
                if integer == False or result_uid >= 100:
                    # UID is of a known object (alpha or in range above unknowns (1-100)) then identify the object.
                    obj = self.uid_dict[str(result_uid)]
                    
                    # Find and append the name of the kind (the supertype or classifier of the option)
                    if len(obj.supertypes) > 0:
                        pref_kind_name = obj.supertypes[0].name
                        # Find the first name in the preferred language of the first supertype in the GUI_language
                        if len(obj.supertypes[0].names_in_contexts) > 0:
                            lang_name, comm_name_supertype, pref_kind_name, descr_of_super = \
                                       self.Determine_name_in_language_and_community(obj.supertypes[0])
                    elif len(obj.classifiers) > 0:
                        pref_kind_name = obj.classifiers[0].name
                        # Find the first name in the preferred language of the first classifier in the GUI_language
                        if len(obj.classifiers[0].names_in_contexts) > 0:
                            lang_name, comm_name_supertype, pref_kind_name, descr_of_super = \
                                       self.Determine_name_in_language_and_community(obj.classifiers[0])
##                        for name_in_context in obj.classifiers[0].names_in_contexts:
##                            if name_in_context[0] == self.GUI_lang_uid:
##                                pref_kind_name = name_in_context[2]
##                                continue
                    else:
                        pref_kind_name = obj.category
                    option.append(pref_kind_name)
                    
##                    # Determine the direct supertype(s), if any    
##                    supers = obj.supertypes
##                    option.append(obj.name) #names_in_contexts[0][2])
                else:
                    #option.append('unknown')       # objectType
                    option.append(self.unknown_kind[self.GUI_lang_index])

                # Add the option to the list of options 
                options.append(option)
                foundUID = option[5]
                
        # If not found in vocabulary, return with name of searchString (being the unknown) and next UID.
        else:   # nrOfFounds == 0:
            if searchString not in self.names_of_unknowns:
                # Create an object for the (list of) unknown(s)
                self.unknown_quid += 1
                unknown = Anything(str(self.unknown_quid), searchString)
                self.unknowns.append(unknown)
                whetherKnown = 'unknown'
                self.names_of_unknowns.append(searchString)
                optionNr = 1
                option.append(optionNr)
                option.append(whetherKnown)
                option.append(self.GUI_lang_pref_uids[1])
                option.append(self.comm_pref_uids[0])
                option.append(searchString)
                option.append(str(self.unknown_quid))
                option.append(is_called_uid)
                option.append(objectTypeKnown)
                option.append(self.unknown_kind[self.GUI_lang_index])

                options.append(option)
                    
                if self.GUI_lang_index == 1:
                    #self.MessagesQ.insert('end','\n
                    print('Term <{}> is niet gevonden in het woordenboek. UID = {}. '.\
                          format(searchString, self.unknown_quid))
                else:
                    #self.MessagesQ.insert('end','\n
                    print('String <{}> not found in the dictionary. UID = {}. '.\
                          format(searchString,self.unknown_quid))
                foundUID = self.unknown_quid
            else:
                # Search in unknowns for object with name searchString
                for obj in self.unknowns:
                    if obj.name == searchString:
                        foundUID = obj.uid
                        break
            if foundUID == '':
                print('Something wrong')
                 
        return foundUID, options

    def Determine_rel_types_for_lh_object(self, lh_object):
        ''' With given selected lh_object determine which kinds of relations are known
            and store results in self.lh_obj_relation_types
        '''
        self.lh_obj_relation_types = []
        for lh_obj_rel in lh_object.relations:
                expr = lh_obj_rel.expression
                rel_type = self.uid_dict[expr[rel_type_uid_col]]
                if rel_type == None:
                    print('Rel_type {} is not found'.format(rel_type_uid))
                else:
                    if rel_type not in self.lh_obj_relation_types:
                        self.lh_obj_relation_types.append(rel_type)
                        
                        # Determine_subtypes of the relation type
                        sub_rel_types, sub_rel_type_uids = self.Determine_subtypes(rel_type)
                        for sub_rel_type in sub_rel_types:
                            if sub_rel_type not in self.lh_obj_relation_types:
                                self.lh_obj_relation_types.append(sub_rel_type)
                
    def Add_classification_relation(self, modified_object, selected_object):
        ''' Append classifier to modified_object, and then add classification relation
        '''
        
        statement = ['statement', 'bewering']
        modified_object.classifiers.append(selected_object)
        
        # Add a classification expression to the list of expressions of the classified object
        # First determine the first available free uid in the range
        for idea in range(self.idea_uid, 212000000):
            if idea not in self.idea_uids:
                self.idea_uid = idea
                self.idea_uids.append(idea)
                break
        lang_uid  = modified_object.names_in_contexts[0][0]
        lang_name = self.lang_uid_dict[lang_uid]
        comm_uid  = modified_object.names_in_contexts[0][1]
        comm_name = self.community_dict[comm_uid]
        lang_comm           = [lang_uid, lang_name, comm_uid, comm_name]
        lh_uid_name         = [modified_object.uid, modified_object.name]
        rel_uid_phrase_type = ['1225', self.classification[self.GUI_lang_index], basePhraseUID]
        rh_role_uid_name    = ['', '']
        rh_uid_name         = [selected_object.uid, selected_object.name] # e.g. 43769 , 'dakvenster'
        uom_uid_name        = ['', '']
        description         = ''
        intent_uid_name     = ['491285', statement[self.GUI_lang_index]]
        rel_type = self.uid_dict['1225']
        gellish_expr = Create_gellish_expression(lang_comm, self.idea_uid, intent_uid_name,\
                                                 lh_uid_name, rel_uid_phrase_type,\
                                       rh_role_uid_name, rh_uid_name, uom_uid_name, description)
        relation = Relation(modified_object, rel_type, selected_object, basePhraseUID, '', gellish_expr)
        modified_object.add_relation(relation)
        selected_object.add_relation(relation)

#-------------------------------------------------------------
if __name__ == "__main__":
    from DatabaseAPI import Database
    from SystemUsers import User
    
##    # Connect to an existing database
##    #db_name  = 'FormalEnglishDB'
##    db_name  = ':memory:'
##    Gel_db = Database(db_name)
##    print("Database  : %s connected." % (Gel_db.name))
    
    # Create and initialize a semantic network
    net_name = 'Language definition network'
    network = Semantic_Network(net_name)
    
    # Choose GUI language and formal language
    formal_language = "English"
    user = User('Andries')
    network.GUI_lang_name = "English"

    # Create a naming dictionary
    dict_name = 'Gellish Multilingual Taxonomic Dictionary'
    Gel_dict  = GellishDict(dict_name)
    print('Created dictionary:', Gel_dict.name)

##    # Add the content of the 'base_ontology' database table to the Semantic Network and to the dictionary
##    table = 'base_ontology'
##    network.Add_table_content_to_network(Gel_db.db_cursor, table)
##
####    # Build hierarchies in base_ontology
####    network.BuildHierarchies()
##    print('network   : %s; nr of objects = %i; nr of rels = %i; nr of rel_types = %i' % \
##          (network.name, len(network.objects), len(network.rels), len(network.rel_type_uids)))
##
##    # Add the content of the 'domain_ontologies' database table to the Semantic Network and to the dictionary
##    table = 'domain_dictionaries'
##    network.Add_table_content_to_network(Gel_db.db_cursor, table)
##    print('network   : %s; nr of objects = %i; nr of rels = %i; nr of rel_types = %i' % \
##          (network.name, len(network.objects), len(network.rels), len(network.rel_type_uids)))

    # Query things in network
    qtext = input("\nEnter query string: ")
    while qtext != "quit" and qtext != "exit":
        com = input("\nEnter string commonality (cspi, csi): ") #(cipi, cspi, cii, csi, cifi, csfi)
        # string_commonality 'csi' = 'case sensitive identical' 'cspi' = 'case sensitive partially identical'
    
        candidates = network.Query_network_dict(qtext, string_commonality)
        if len(candidates) > 0:
            for candidate in candidates:
                obj_uid = candidate[1][0]
                #print("candidate %s %s" % (obj_uid, candidate[0][2]))
                obj = network.uid_dict[obj_uid]     #find_object(obj_uid)
                s = obj.show(network)
        else:
            print("No candidates found")
        qtext = input("\nEnter query string: ")
