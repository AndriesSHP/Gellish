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
from GUI_views import Display_views
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
        #self.lang_index    = user.GUI_lang_index
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
        self.lang_uid_dict   = {} #{910036: "English", 910037: "Nederlands" , 589211: "international"}
        self.community_dict  = {} #{492015: "Formal English", 492016: "Formeel Nederlands", \
                                  # 492014: "Gellish", 589830: "Gellish alternative"}
        self.lang_dict_EN    = {'910036': "English", '910037': "Dutch"     , '589211': "international",\
                                '910038': "German" , '910039': "French"}
        self.lang_dict_NL    = {'910036': "Engels" , '910037': "Nederlands", '589211': "internationaal",\
                                '910038': "Duits"  , '910039': "Frans"}
        self.comm_dict_EN    = {'492014': "Gellish"}
        self.comm_dict_NL    = {'492014': "Gellish"}
        self.base_phrases    = boot_base_phrasesEN    + boot_base_phrasesNL
        self.inverse_phrases = boot_inverse_phrasesEN + boot_inverse_phrasesNL
        self.specialRelUIDs  = ['1146']   # 1146 base UID for 'is a kind of'
        self.classifUIDs     = []       # 1225 base UID for 'is classified as a'
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
        self.possib_objects = []
        self.indiv_model    = []
        self.indiv_objects  = []
        self.info_model     = []
        self.all_subtypes   = []
        self.occ_model      = []

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

    def Create_base_reltype_objects(self):
        '''Create relation_type objects conform Bootstrapping base_rel_type_uids'''
        for rel_type_uid in base_rel_type_uids:
            rel_type_name = base_rel_type_uids[rel_type_uid]
            rel_type = RelationType(rel_type_uid, rel_type_name)
            self.rel_types.append(rel_type)
            self.uid_dict[rel_type_uid] = rel_type
            #self.object_uids.append(rel_type_uid)
    
    def Build_Base_Semantic_Network(self): #, db_cursor):
        ''' Build a Semantic Network from 'base_ontology' database table,
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

        # Add role_players_types requirements to relation types because of relation types
        for rel_type in self.rel_types:
            rel_type.role_players_types, rel_type.role_player_type_lh, rel_type.role_player_type_rh \
                                         = self.Determine_role_players_types(rel_type.uid)
    
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
        if uom_uid != '':
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
            relation = Relation(lh, rel_type, rh, phrase_type_uid, uom, row) # Default: category == None
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
            elif rel_type_uid in classifUIDs:
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
                                                 'kind of occurrence', 'kind of role', 'number']:
                            print("Error: Idea {} Object '{}' category '{}' should be 'kind'".\
                                  format(idea_uid, rh_name, rh.category))
                            rh.category = 'kind'
                else:
                    lh.add_individual(rh)
                    rh.add_classifier(lh)

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
            elif rel_type_uid == invUID:
                phrase_in_context = [lang_uid, comm_uid, lh_name]
                lh.add_inverse_phrase(phrase_in_context)
                lh.inversePhrases.append(lh_name)
                self.inverse_phrases.append(lh_name)

    def BuildHierarchies(self):
        ''' Build a naming table (extend the language vocabulary) and expression table
        Extent the information model by data entry and extending namingTable,
        Append model file
        Search in ontology and informationm model (on-line or via GUI)
        '''
        
        # Determine lists of various kinds and their subtypes
        self.sub_classifs,    self.sub_classif_uids    = self.DetermineSubtypeList(classifUID)
        self.subClassifieds,  self.subClassifiedUIDs   = self.DetermineSubtypeList(classifiedUID)
        self.indOrMixRels,    self.indOrMixRelUIDs     = self.DetermineSubtypeList(indOrMixRelUID)
        self.indivBinRels,    self.indivBinRelUIDs     = self.DetermineSubtypeList(indivRelUID)     # 4658
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
        self.subConcCompons,  self.subConcComponUIDs   = self.DetermineSubtypeList(concComponUID) # conceptual component role and its subtypes
        self.subInvolveds,    self.subInvolvedUIDs     = self.DetermineSubtypeList(involvedUID)
        self.subNexts,        self.subNextUIDs         = self.DetermineSubtypeList(nextUID)
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
                        sub.category = 'kind of relation'
                        try:
                            if sub.first_role != None:
                                # Check whether supertype of kind of role == role of supertype
                                if sub.first_role.supertype.first_role != supertype.first_role:
                                    print('Supertype of first kind of role {} not equal role of supertype {}'\
                                          .format(sub.first_role.supertype.first_role, supertype.first_role))
                        except AttributeError:
                            sub.first_role = supertype.first_role
                            
                        try:
                            if sub.second_role != None:
                                # check whether supertype of kind of role == role of supertype
                                if sub.second_role.supertype.second_role != supertype.second_role:
                                    print('Supertype of second kind of role {} not equal role of supertype {}'\
                                          .format(sub.second_role.supertype.second_role, supertype.second_role))
                        except AttributeError:
                            sub.second_role = supertype.second_role
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

                        # If sub belongs to taxonomy of relations then inherit by definition first and second kinds of roles
                        if rel_taxonomy == True:
                            sub.category = 'kind of relation'
                            try:
                                if sub.first_role != None:
                                    # Check whether supertype of kind of role == role of supertype
                                    if sub.first_role.subX.first_role != subX.first_role:
                                        print('Supertype of first kind of role {} not equal role of supertype {}'\
                                              .format(sub.first_role.subX.first_role, subX.first_role))
                            except AttributeError:
                                sub.first_role = subX.first_role

                            try:
                                if sub.second_role != None:
                                    # check whether supertype of kind of role == role of supertype
                                    if sub.second_role.subX.second_role != subX.second_role:
                                        print('Supertype of second kind of role {} not equal role of supertype {}'\
                                              .format(sub.second_role.subX.second_role, subX.second_role))
                            except AttributeError:
                                sub.second_role = subX.second_role
                            #print('Roles of relations:', sub.name, sub.first_role.name, sub.second_role.name)
        return all_subtypes, all_subtype_uids
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
#-------------------------------------  
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
        self.possib_objects[:] = []
        self.indiv_model[:]   = []
        self.indiv_objects[:] = []
        self.query_table[:]   = []
        self.info_model[:]    = []
        self.occ_model[:]     = []
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
                       self.Determine_name_in_language_and_community(obj, self.user.lang_pref_uids)
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
        nr_of_occ_aspect_kinds  = 3
        self.decomp_level = 0
        role = ''

        self.Create_prod_model_view_header(obj)

        if obj.category in ['kind', 'kind of physical object', 'kind of occurrence', \
                            'kind of aspect', 'kind of role', 'number']:
            # Search for the first supertype relation that generalizes the self.object_in_focus
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

        # Object category is not a kind, thus indicates an individual thing.
        # Verify whether the individual thing is classified (has one or more classifiers)
        elif len(obj.classifiers) == 0:
            print('For object {} neither a supertype nor a classifier is found'.format(obj.name))
        else:
            # The object_in_focus is classified (once or more times)
            # thus it is indeed an individual, such as an individual physical object or occurrence:
            # Search for classifying kind and classification relation that classifies the self.object_in_focus
            classifier = obj.classifiers[0]
            # kindUID is the kind that classifies the self.object_in_focus
            kindUID    = classifier.uid
            # Determine name etc. of the kind of the self.object_in_focus
            lang_name, comm_name, kindName, descrOfKind = \
                       self.Determine_name_in_language_and_community(classifier, self.user.lang_pref_uids)
                
##            if kindUID in self.DetermineSubtypeList(occurrenceUID):     # Verify whether the individual is an occurrence. occurrenceUID
##                self.categoryInFocus = 'occurrence'

##        if self.categoryInFocus == 'occurrence' or self.categoryInFocus == 'kind of occurrence':
##            self.nr_of_occurrencies += + 1
##            occRow[0] = self.nr_of_occurrencies
##            occRow[1] = self.object_in_focus.name
##            occRow[2] = self.object_in_focus
##            occRow[3] = kindName
##            occ_model.append(occRow[:])
    
        # Search for aspects of the whole self.object_in_focus and their values and UoMs

        # Find kinds of aspects and their values of kind_in_focus (and implied parts)
        if obj.category in ['kind', 'kind of physical object', 'kind of occurrence', \
                            'kind of aspect', 'kind of role', 'number']:
            # Find preferred name of object in required language and community
            lang_name, comm_name, obj_name, descr = \
                       self.Determine_name_in_language_and_community(obj, self.user.lang_pref_uids)
            obj.name = obj_name
        
            self.taxon_row[0] = obj.uid
            self.taxon_row[1] = obj.name    # preferred name
            #self.taxon_row[2] = supertype_name   # name of the first supertype
            self.taxon_row[3] = comm_name

            if len(obj.supertypes) > 0:
                lang_name, comm_name_supertype, supertype_name, descr_of_super = \
                           self.Determine_name_in_language_and_community(obj.supertypes[0], self.user.lang_pref_uids)
            else:
                supertype_name = 'unknown'

            self.possibility_row[0] = obj.uid
            self.possibility_row[1] = obj_name
            self.possibility_row[2] = ''
            self.possibility_row[3] = supertype_name
            self.possibility_row[4] = comm_name     # of obj (not of supertype)
            
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
            self.summary_row[2] = kindName
            self.summary_row[3] = community_name
            
            self.indiv_row[0] = obj.uid
            self.indiv_row[1] = obj.name
            self.indiv_row[2] = ''
            self.indiv_row[3] = kindName
            self.indiv_row[4] = community_name
            
            # Find aspects of individual object_in_focus
            nr_of_aspects = self.Find_aspects(obj, role)

            # Find parts and their aspects
            self.part_head_req = True
            self.Find_parts_and_their_aspects(obj)
            
        else:
            print("Object category '{}' not programmed for searching for aspects".format(obj.category))
                
    ##    seqTable = []
    ##    ioTable  = []
    ##    pOccTable= []       # parts of occurrence in focus
    ##    involvedUID     = 4546        # 4546 = <involved> being a second role in an <involvement in an occurrence> relation
    ##    subInvolveds, subInvolvedUIDs = self.DetermineSubtypeList(involvedUID)
    ##    nextUID         = 5333        # 5333 next element (role)
    ##    subNexts, subNextUIDs     = self.DetermineSubtypeList(nextUID)
    ##    if obj.category != 'occurrence':
    ##        # Search for occurrences about the self.object_in_focus and other involved objects in those occurrences.
    ##        self.decomp_level = 0
    ##        OccursAndInvolvs(self.object_in_focus, self.object_in_focus.name,obj.category)    
    
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
##        prod_head_5 = ['','',self.line_nr, subsHead[self.user.GUI_lang_index], sub2Head[self.user.GUI_lang_index],\
##                     sub3Head[self.user.GUI_lang_index],'','','','','','']
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
##                # Summary_row = [uid, community_name, object_in_focus.name, supertype name]
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

    def Determine_name_in_language_and_community(self, obj, lang_pref_uids):
        ''' Given an object and preferred language sequence uids and community sequence uids,
            determine lang_name, comm_name, obj_name for user interface
        '''
        name_known = False
        if len(obj.names_in_contexts) > 0:
            # For language_prefs search for name  === for comm_pref_uids to be done ===
            for lang_uid in lang_pref_uids:
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
            for lang_uid in lang_pref_uids:
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
            status = status_text[self.user.GUI_lang_index]
        else:
            obj_kind_uid  = obj.kind.uid
            lang_name, comm_name, obj_kind_name, descr = \
                               self.Determine_name_in_language_and_community(obj.kind, self.user.lang_pref_uids)
            status = 'unknown'
        is_a = ['is a ', 'is een ']
        form_text  = ['Product form for:', 'Product formulier voor:']
        kind_text  = ['Kind:'            , 'Soort:']
        descr_text = ['Description:'     , 'Omschrijving:']
        if len(obj.names_in_contexts) > 0:
            description = is_a[self.user.GUI_lang_index] + obj_kind_name + '' + obj.names_in_contexts[0][4]
        else:
            description = is_a[self.user.GUI_lang_index] + obj_kind_name

        prod_line_0 = [obj.uid  , obj_kind_uid , '', 1 , form_text[self.user.GUI_lang_index], obj.name, '', '',\
                       kind_text[self.user.GUI_lang_index], obj_kind_name, '', '', '', status]    # names_in_contexts[0][2]
        prod_line_1 = ['','','',2,'', descr_text[self.user.GUI_lang_index], description,'','','','','','','']
        
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

        #prod_line_3 = [part_uid,aspect_uid,self.line_nr,part,'','',kindOfPart,aspect.name,kindOfAspect,value,UoM,status]
        #prod_line_4 = [partOfPart.uid,aspect_uid,self.line_nr,'',partOfPart,'',kindOfPart,aspect.name,kindOfAspect,value,UoM,status]
        #prod_line_5 = [occur_uid,aspect_uid,self.line_nr,occur,'','',kindOfOcc,aspect.name,kindOfAspect,value,UoM,status]
        #prod_line_6 = [invObj.uid,aspect_uid,self.line_nr,'',invObject,role,kindOfInv,aspect.name,kindOfAspect,value,UoM,status]
        #prod_line_7 = [part_uid,aspect_uid,self.line_nr,'','','','',aspect.name,kindOfAspect,value,UoM,status]
        #prod_line_8 = [obj.uid,file_uid,self.line_nr,obj,document,'',kind_of_document,file,kind_of_file,'','',status]

        if obj.category in ['kind', 'kind of physical object', 'kind of occurrence']:
            self.kind_model.append(prod_line_0)
            if len(obj.supertypes) > 1:
                for super_type in obj.supertypes[1:]:
                    self.kind_model.append([obj.uid,super_type.uid,'',1,'','','','','',super_type.name])
            self.kind_model.append(prod_line_1)
            if self.user.GUI_lang_name == 'Nederlands':
                self.kind_model.append(prod_head_NL2K)
            else:
                self.kind_model.append(prod_head_EN2K)
        else:
            # category is individual
            self.prod_model.append(prod_line_0)
            # If there are several classifiers, then add a line per classifier
            if len(obj.classifiers) > 1:
                for classifier in obj.classifiers[1:]:
                    self.prod_model.append([obj.uid,classifier.uid,'',1,'','','','','',classifier.name])
            self.prod_model.append(prod_line_1)
            if self.user.GUI_lang_name == 'Nederlands':
                self.prod_model.append(prod_head_NL2I)
            else:
                self.prod_model.append(prod_head_EN2I)
            
##        if self.user.GUI_lang_name == 'Nederlands':
##            if obj.category in ['kind', 'kind of physical object', 'kind of occurrence']:
##                self.prod_model.append(prod_head_NL2K)
##            else:
##                self.prod_model.append(prod_head_NL2I)
##        else:
##            if obj.category in ['kind', 'kind of physical object', 'kind of occurrence']:
##                self.prod_model.append(prod_head_EN2K)
##            else:
##                self.prod_model.append(prod_head_EN2I)
##        self.kind_model = self.prod_model[:]

    def Find_kinds_of_aspects(self, obj, role):
        '''Search for kinds of aspects that can/shall or are by definition possessed by a kind of thing (obj)
        and search for their qualitative subtypes and possible collection of allowed values.
        obj      = the kind in focus
        role     = the role played by an involved object that is involved in an occurrence
        decomp_level = decomposition level: 0 = objectInFocus, 1 = part, 2 = part of part, etc.
        obj.category = category of the object in focus,
                      being individual or kind or phys object or occurrence or kind of occurrence'''

        unknownKind  = ['unknown supertype','onbekend supertype']
        noValuesText = ['No specification','Geen specificatie']
        self.has_as_subtypes = ['has as subtypes', 'heeft als subtypes']

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

        # Collect relations other than subConcPossAspUIDs in query_table
        for rel_obj in obj.relations:
                expr = rel_obj.expression
                if len(self.query_table) < self.max_nr_of_rows and expr not in self.query_table:
                        self.query_table.append(expr)
##                if expr[lh_uid_col] == obj.uid \
##                   and not expr[rel_type_uid_col] in self.subConcPossAspUIDs:
##                    if len(self.query_table) < self.max_nr_of_rows:
##                        self.query_table.append(expr)
        
        # Collect list of obj and its supertypes in the complete hierarchy for searching inherited aspects
        all_supers = self.Determine_supertypes(obj)
        # For each object in the hierarchy find (inherited) aspect values but exclude the roles
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
                       
##                if value_presence == False:
##                    value_name = '' # noValuesText[self.user.GUI_lang_index]
##                    warnText  = ['  Warning: Kind of aspect','Waarschuwing: Soort aspect']
##                    valueMess = ['has no specification of (allowed) values.',\
##                                 'heeft geen specificatie van (toegelaten) waarden.']
##                    print('%s %s (%i) %s' % \
##                          (warnText[self.user.GUI_lang_index],aspect_name,aspect_uid,valueMess[self.user.GUI_lang_index]))
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

                    if self.subtype_level == 0:
                        # Build composition_view header add a column for aspects if not yet included
                        if value_presence == True and aspect_name not in self.possib_column_names and \
                           len(self.possib_column_names) <= 15:
                            #print('Compon_header', aspect_name, len(self.possib_aspect_uids))
                            self.possib_aspect_uids.append(aspect_uid)
                            self.possib_column_names.append(aspect_name)
                            self.possib_uom_names.append(uom_name)
                        self.possib_ind = 4
                        #print('Sums:',len(self.possib_aspect_uids), self.possib_aspect_uids, self.possib_column_names, value_name)
                        # Find column in possibility_row where value should be stored
                        for kind_uid in self.possib_aspect_uids[5:]:
                            self.possib_ind += + 1
                            # Build list of values conform list of aspects.
                            if aspect_uid == kind_uid:
                                #print('Aspects of phys:',len(self.possib_aspect_uids), aspect_name, self.possib_ind, value_name)
                                self.possibility_row[self.possib_ind] = value_name
                                if uom_name != self.possib_uom_names[self.possib_ind]:
                                    #MessagesM.insert('end','\n
                                    print('Unit of measure {} ({}) of the value of {} differs from composition table header UoM {}'\
                                          .format(uom_name, uom_uid, aspect_name, self.possib_uom_names[self.possib_ind]))

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
                                    
        #        elif self.decomp_level == 0:            # if not a kind of occurrence, then build header for summaryTable
            
        # If obj is object_in_focus (thus not a part) then create one or more rows in taxon_model             
        if self.decomp_level == 0:
            if len(obj.supertypes) > 0:
                # Create a row in the taxonomy per direct supertype
                for supertype in obj.supertypes:
                    lang_name, comm_name_super, preferred_name, descr = \
                               self.Determine_name_in_language_and_community(supertype, self.user.lang_pref_uids)
                    self.taxon_row[2] = preferred_name  # of the supertype
                    if len(self.taxon_model) < self.max_nr_of_rows:
                        # If summary row is about object in focus, then make supertype of object in focus empty
                        # Because treeview parent (taxon_row[2] should be supertype or blank.
                        #print('Subtype_level:', self.subtype_level, obj.name, self.taxon_row)
                        if self.taxon_row[0] == self.object_in_focus.uid:
                            self.taxon_row[2] = ''

                        # If the supertype is the object_in_focus, then make the object a sub of the inter_row
                        if self.taxon_row[2] == self.object_in_focus.name:
                            self.taxon_row[2] = self.has_as_subtypes[self.user.GUI_lang_index]
                        self.taxon_model.append(self.taxon_row[:])
                        
                        # If the object is the object_in_focus, then insert an inter_row header line for the subtypes
                        if self.subtype_level == 0:
                            inter_row = [obj.uid, self.has_as_subtypes[self.user.GUI_lang_index], obj.name, '']
                            self.taxon_model.append(inter_row)

            self.taxon_row = ['','','','','','','','','','','','','','']

        # If not a subtype (subtype_level == 0) and for any decomp_level create a row in possibilities_model
        if self.subtype_level == 0:
            if len(self.possibilities_model) < self.max_nr_of_rows:
                if obj not in self.possib_objects:
                    self.possib_objects.append(obj)
                    # If composition row is about object in focus, then make whole of object in focus empty
                    # Because treeview parent should be whole of blank.
                    if self.possibility_row[0] == self.object_in_focus.uid:
                        self.possibility_row[2] = ''
                    self.possibilities_model.append(self.possibility_row[:])
                else:
                    print('Duplicate composition row',len(self.possibilities_model), self.possibility_row)
            self.possibility_row  = ['','','','','','','','','','','','','','','']
        
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
                    header_text = has_as_individuals[self.user.GUI_lang_index]+obj.name
                    inter_row = [obj.uid, header_text, obj.name, '']
                    self.taxon_model.append(inter_row)
                    first_time = False

                # Create a row in the taxonomy for an individual thing under the header for individual things
                lang_name, community_name, preferred_name, descr = \
                           self.Determine_name_in_language_and_community(indiv, self.user.lang_pref_uids)
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
        #if test: print('PaA-level of parts of:',self.decomp_level,name,obj.uid)
        
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
##                    else:
##                        # The lh object in focus is itself a part of a rh whole
##                        # Add the relation with the whole to info about the object in focus
##                        if expr not in self.query_table:
##                            self.query_table.append(expr)
                        
                # If inverse phrase <has as part> and left hand is the object in focus then rh is a part
                elif expr[phrase_type_uid_col] == invUID:     # inverse
                    if obj.uid == expr[lh_uid_col]:
                        part_uid = expr[rh_uid_col]
##                    else:
##                        # The rh object in focus is itself a part of a lh whole
##                        # Add the relation with the whole to info about the object in focus
##                        if expr not in self.query_table:
##                            self.query_table.append(expr)
                else:
                    print('Phrase type uid {} incorrect'.format(expr[phrase_type_uid_col]))
                    continue

                if part_uid != '':
                    # There is an explicit part found; create part_header, prod_head_4, the first time only
                    if self.part_head_req == True:
                        self.line_nr += 1
                        prod_head_4 = ['','','',self.line_nr, compHead[self.user.GUI_lang_index], partHead[self.user.GUI_lang_index],\
                                     par3Head[self.user.GUI_lang_index], kindHead[self.user.GUI_lang_index],'','','','','']
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
                        part_kind_name = kind_unknown[self.user.GUI_lang_index]
                    else:
                        part_kind_uid  = part.classifiers[0].uid
                        # Determine name etc. of the kind that classifies the part
                        if len(part.classifiers[0].names_in_contexts) > 0:
                            #print('Part classifier names', self.user.lang_pref_uids, part.classifiers[0].names_in_contexts)
                            lang_name, comm_name, part_kind_name, descrOfKind = \
                                       self.Determine_name_in_language_and_community(part.classifiers[0], self.user.lang_pref_uids)
                        else:
                            part_kind_name = part.classifiers[0].name
                            comm_name = 'unknown'
                            
                    # Determine the preferred name of the part
                    if len(part.names_in_contexts) > 0:
                        lang_name, community_name, part_name, descrOfKind = \
                                       self.Determine_name_in_language_and_community(part, self.user.lang_pref_uids)
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
                            prod_line_4 = [part.uid,part_kind_uid,'',self.line_nr,part.name,'','',part_kind_name,'','','','','',status]
                        elif self.decomp_level == 2:
                            prod_line_4 = [part.uid,part_kind_uid,'',self.line_nr,'',part.name,'',part_kind_name,'','','','','',status]
                        elif self.decomp_level == 3:
                            prod_line_4 = [part.uid,part_kind_uid,'',self.line_nr,'','',part.name,part_kind_name,'','','','','',status]
                        if self.decomp_level < 4:
                            if len(self.prod_model) < self.max_nr_of_rows:
                                self.prod_model.append(prod_line_4)
                        
                    # Search for parts of part and their aspects
                    self.Find_parts_and_their_aspects(part)
                
        self.decomp_level += - 1        
        #if nrOfParts == 0:              # Check whether nr of parts = 0
        #    print('\nNo parts found in query results for {} ({})'.format(name,UID))

    def Find_kinds_of_parts_and_their_aspects(self, obj):
        """ Search for explicit kinds of parts and combine them with implied kinds of parts"""

        compHead = ['Part hierarchy','Compositie']
        partHead = ['Part of part','Deel van deel']
        par3Head = ['Further part','Verder deel']
        kindHead = ['Kind','Soort']
        
        role = ''
        self.part_head_req = True
        # Search for kinds of parts of self.object_in_focus
        for rel_obj in obj.relations:
                expr = rel_obj.expression
                if expr[lh_uid_col] == obj.uid and expr[rh_role_uid_col] in self.subConcComponUIDs:
                    part_uid   = expr[rh_uid_col]
                    part_name  = expr[rh_name_col]
                    #role_uid     = expr[rh_role_uid_col]
                    #role_name    = expr[rh_role_name_col]
                elif expr[rh_uid_col] == obj.uid and expr[lh_role_uid_col] in self.subConcComponUIDs:
                    part_uid   = expr[lh_uid_col]
                    part_name  = expr[lh_name_col]
                    #role_uid     = expr[lh_role_uid_col]
                    #role_name    = expr[lh_role_name_col]
                else:
                    continue
                
                # There is an explicit kind of part found; create part_header in kind_model, the first time only
                if self.part_head_req == True:
                    self.line_nr += 1
                    prod_head_4 = ['','','',self.line_nr, compHead[self.user.GUI_lang_index], partHead[self.user.GUI_lang_index],\
                                 par3Head[self.user.GUI_lang_index], kindHead[self.user.GUI_lang_index],'','','','','']
                    if len(self.kind_model) < self.max_nr_of_rows:
                        self.kind_model.append(prod_head_4) # Header of part list
                    self.part_head_req = False

                # Add the expression to the query_table output table
                if len(self.query_table) < self.max_nr_of_rows:
                    self.query_table.append(expr)

                part = self.uid_dict[part_uid]
                if len(part.supertypes) > 0:
                    part_kind_name = part.supertypes[0].name
                else:
                    part_kind_name = 'unknown'

                community_name = self.community_dict[part.names_in_contexts[0][1]] # community uid
                self.possibility_row[0] = part.uid
                self.possibility_row[1] = part.names_in_contexts[0][2] # part.name
                self.possibility_row[2] = obj.name
                self.possibility_row[3] = part_kind_name
                self.possibility_row[4] = community_name # of part

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
                prod_head_4 = ['','','',self.line_nr, compHead[self.user.GUI_lang_index], partHead[self.user.GUI_lang_index],\
                             par3Head[self.user.GUI_lang_index], kindHead[self.user.GUI_lang_index],'','','','','']
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
            decomp_level    = decomposition level: 0 = objectInFocus, 1 = part, 2 = part of part, etc.
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
                if expr[phrase_type_uid_col] == invUID:
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
                    if expr[phrase_type_uid_col] == invUID:
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
            self.line_nr  += 1

            # Find the aspect object of the <has as aspect> relation or the qualitative aspect
            aspect = self.uid_dict[aspect_uid]

            # Verify if the individual object is classified
            if len(indiv.classifiers) == 0:
                indiv.kind_uid  = ''
                indiv.kind_name = 'unknown kind'
            else:
                # Determine the preferred name of the first classifier of the individual object
                lang_name_cl, comm_name_cl, pref_cl_name, descr = \
                              self.Determine_name_in_language_and_community(indiv.classifiers[0], self.user.lang_pref_uids)
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
                    #print('Lang_prefs for classifier of aspect', self.user.lang_pref_uids, aspect.classifiers[0].names_in_contexts)
                    lang_name_as, comm_name_as, pref_kind_name, descr = \
                                  self.Determine_name_in_language_and_community(aspect.classifiers[0], self.user.lang_pref_uids)
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
                               self.Determine_name_in_language_and_community(value, self.user.lang_pref_uids)
                        
                    # Aspect value found: add expression to result table
                    if len(self.query_table) < self.max_nr_of_rows and expr not in self.query_table:
                        self.query_table.append(expr)
            else:
                # Qualitative aspect found (e.g. a substance such as PVC)
                substance = self.uid_dict['431771']     # subtance or stuff
                lang_name, comm_name, pref_kind_name, descr = \
                           self.Determine_name_in_language_and_community(substance, self.user.lang_pref_uids)
                aspect.kind_name = pref_kind_name
                aspect.kind_uid  = '431771'
                uom_uid  = ''
                uom_name = ''
                value_uid  = aspect.uid
                lang_name, comm_name, value_name, descr = \
                           self.Determine_name_in_language_and_community(aspect, self.user.lang_pref_uids)
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
                value_name = unknownVal[self.user.GUI_lang_index]
                warnText  = ['  Warning: Aspect','Waarschuwing: Aspect']
                valueMess = ['has no value.','heeft geen waarde.']
                #self.MessagesQ.insert('end','\n
                print('{} {} ({}) {}'.format(warnText[self.user.GUI_lang_index], aspect_name,aspect_uid, \
                                             valueMess[self.user.GUI_lang_index]))
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
            if self.decomp_level == 1 and nr_of_aspects == 1:
                prod_line_3 = [indiv.uid, indiv.kind_uid, aspect_uid, self.line_nr,indiv.name,role,''  ,indiv.kind_name,\
                             aspect_name, aspect.kind_name, equality, value_name, uom_name, status]
            elif self.decomp_level == 2 and nr_of_aspects == 1:
                prod_line_3 = [indiv.uid, indiv.kind_uid, aspect_uid, self.line_nr,role,indiv.name,''  ,indiv.kind_name,\
                             aspect_name, aspect.kind_name, equality, value_name, uom_name, status]
            elif self.decomp_level == 3 and nr_of_aspects == 1:
                prod_line_3 = [indiv.uid, indiv.kind_uid, aspect_uid, self.line_nr,''  ,role,indiv.name,indiv.kind_name,\
                             aspect_name, aspect.kind_name, equality, value_name, uom_name, status]
            else:
                prod_line_3 = [indiv.uid, indiv.kind_uid, aspect_uid, self.line_nr,'','','','',\
                             aspect_name, aspect.kind_name, equality, value_name, uom_name, status]
            if len(self.prod_model) < self.max_nr_of_rows:
                self.prod_model.append(prod_line_3)

        # If aspect is possessed by object_in_focus (thus not possessed by a part) then add row to summ_model
        #print('Indiv', self.decomp_level, self.object_in_focus.uid, self.summary_row)
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

        # For whole and for parts of whole create a row in indiv_model
        if len(self.indiv_model) < self.max_nr_of_rows:
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
                    prod_head_8 = ['','','',self.line_nr, info_head[self.user.GUI_lang_index], dir_head[self.user.GUI_lang_index],'',\
                                   kind_of_doc_head[self.user.GUI_lang_index]           , file_head[self.user.GUI_lang_index],\
                                   kind_of_file_head[self.user.GUI_lang_index],'','','',status_head[self.user.GUI_lang_index]]
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
                                info.name, super_info_name, obj.name, '',descr_avail_text[self.user.GUI_lang_index], '', '']
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
        nr_of_candidates = 0
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
                option.append(self.user.GUI_lang_pref_uids[1])
                option.append(self.user.comm_pref_uids[0])
                option.append(resultString)
                option.append(str(self.unknown_quid))
                option.append(is_called_uid)
                option.append(objectTypeKnown)
                option.append(self.unknown_kind[self.user.GUI_lang_index])

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
        nr_of_candidates = len(candidates)
                
##    #
##    # Determine whether searchString consist of multiple parts, separated by a space (' ')
##    # and whether those parts (subStrings) all occur in the same name
##        nrOfSubstrings = searchString.count(' ') + 1
##        subStrings = searchString.split(' ')
##        if self.test: print('subStrings:',nrOfSubstrings,subStrings)
##        if nrOfSubstrings > 0:             # If there are > 0 (sub)strings:
##            for name in nameList:
##                subInName = True
##                # Check whether the substrings are together part of the same term
##                for subString in subStrings:
##                    # If case insensitive; string_commonality is one of cipi, cspi, cii, csi, cifi, csfi
##                    if string_commonality in ['cipi', 'cii', 'cifi']:
##                        if subString.lower() not in name.lower():
##                            subInName = False
##                            break
##                    else:
##                        if subString not in name:
##                            subInName = False
##                            break
##                                               # subString does appear in name

##                    # If it is required that the first character of the first substring should match
##                    if string_commonality in ['cifi', 'csfi']:
##                        lenSub = len(subStrings[0])
##                        if subStrings[0] != name[0:lenSub]:
##                            #print('FirstChar:',subStrings[0],lenSub,name[0:lenSub])
##                            subInName = False
##                            break
##                if subInName == True:
##                    if fullNameFound == True and name == foundStrings[0]:
##                        continue
##                    nrOfFounds = nrOfFounds + 1
##                    foundStrings.append(name)
##                    foundIndexes.append(nameList.index(name))
##                    #if self.test: print('    Found part string:',name,nameList.index(name))
##
##        if self.test: print('Nr of found strings :',nrOfFounds, searchString)

        # Collect found option in 'options' list for display and selection
        if len(candidates) > 0:
            #print ("nr of candidates:",len(candidates), self.user.GUI_lang_uid)
            optionNr = 0
            for candidate in candidates:
                # Only add the candidate if uid of language corresponds with uid from GUI_lang_pref_uids
                # because the query is in the GUI_language
                if candidate[0][0] not in self.user.GUI_lang_pref_uids:
                    continue
                whetherKnown = 'known'
                option = []
                optionNr = optionNr + 1
                option.append(optionNr)
                option.append(whetherKnown)
                for part in candidate: # add candidate fields to option (in column (2,3,4),(5,6,7)
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
                                       self.Determine_name_in_language_and_community(obj.supertypes[0], \
                                                                                     self.user.GUI_lang_pref_uids)
                    elif len(obj.classifiers) > 0:
                        pref_kind_name = obj.classifiers[0].name
                        # Find the first name in the preferred language of the first classifier in the GUI_language
                        if len(obj.classifiers[0].names_in_contexts) > 0:
                            lang_name, comm_name_supertype, pref_kind_name, descr_of_super = \
                                       self.Determine_name_in_language_and_community(obj.classifiers[0], \
                                                                                     self.user.GUI_lang_pref_uids)
##                        for name_in_context in obj.classifiers[0].names_in_contexts:
##                            if name_in_context[0] == self.user.GUI_lang_uid:
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
                    option.append(self.unknown_kind[self.user.GUI_lang_index])

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
                option.append(self.user.GUI_lang_pref_uids[1])
                option.append(self.user.comm_pref_uids[0])
                option.append(searchString)
                option.append(str(self.unknown_quid))
                option.append(is_called_uid)
                option.append(objectTypeKnown)
                option.append(self.unknown_kind[self.user.GUI_lang_index])

                options.append(option)
                    
                if self.user.GUI_lang_index == 1:
                    #self.MessagesQ.insert('end','\n
                    print('Term <%s> is niet gevonden in het woordenboek. UID = {}. '.\
                          format(searchString,self.unknown_quid))
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
        # Append classifier to modified_object, and then add classification relation
        
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
        rel_uid_phrase_type = ['1225', self.classification[self.user.GUI_lang_index], basePhraseUID]
        rh_role_uid_name    = ['', '']
        rh_uid_name         = [selected_object.uid, selected_object.name] # e.g. 43769 , 'dakvenster'
        uom_uid_name        = ['', '']
        description         = ''
        intent_uid_name     = ['491285', statement[self.user.GUI_lang_index]]
        rel_type = self.uid_dict['1225']
        gellish_expr = Create_gellish_expression(lang_comm, self.idea_uid, intent_uid_name,\
                                                 lh_uid_name, rel_uid_phrase_type,\
                                       rh_role_uid_name, rh_uid_name, uom_uid_name, description)
        relation = Relation(modified_object, rel_type, selected_object, basePhraseUID, '', gellish_expr)
        modified_object.add_relation(relation)
        selected_object.add_relation(relation)
#--------------------------------------------------------------------
class Query:
    def __init__(self, Gel_net, main):
        self.Gel_net = Gel_net
        self.main    = main
        self.user    = main.user
        self.query_expr = []
        self.test    = False
        #self.lang_index = self.user.GUI_lang_index

        self.obj_list    = []
        
        self.objects_in_focus   = []
        self.UIDsInFocus        = []
        self.namesInFocus       = []
        self.kindUIDsInFocus    = []
        self.kindNamesInFocus   = []
        self.hierarchical_net      = []
        self.hierarchical_net_uids = []
        #self.condition_table = []
        
        # Options are ...
        # options = [optionNr, whetherKnown, lang_uid, comm_uid, name, uid, is_called_uid, \
        #           objectTypeKnown, 'unknown kind'/'onbekende soort']

        self.candid_expressions = []
        self.candidates = []
        self.candid_uid_dict = {}
        
        self.lhCondVal   = []
        self.relCondVal  = []
        self.rhCondVal   = []
        self.uomCondVal  = []
        self.lhSel  = []
        self.relSel = []
        self.rhSel  = []
        self.q_rel_subtype_uids = []

        # Initialize 
        self.net_uids = []
        self.branches = []

    def Specify_query_via_command_line(self):
        ''' Specify and interpret a query (q) about things in a semantic network.
            Search for terms in the dictionary'''

        # Search in the dictionary (using a filter function), which returns values if
        # 0) search_string is equal to the third position of the first(key) field of an item:
        #    case sensitive identical
        # 1) search_string is in that field:
        #    case sensitive partially identical
        # 2) search_string is in that field and starts with that string
        #    case sensitive front end identical
        # 3), 4), 5) idem, but case insensitive

        # Enter a search string
        search_string = input("\nEnter a query expression, string or quit (q): ")
    ##    while search_string not in ["q", "quit"]:
        while search_string not in ["s", "d", ""]:
            
            # Interpret the search string, being either a single term (string) or an expression (a<rel>b).
            known_strings, interpreted = self.Interpret_query_line(search_string)
            print('Interpreted query: ', interpreted)
            self.main.query_spec.append(interpreted)
            if len(interpreted) > 5:
                # An expression was given with 6 or more fields (lh, rel, rh and possibly uom)
                search_string = input("\nEnter a condition specification or search (s) cq display (d): ")
            else:
                search_string = 'd' # input("\nDisplay results (d): ")

    def Interpret_query_line(self, search_string):
        '''A query line via a command line consists either of a single term string 
           or an expression, being lh_string < rel_string > rh_string = uom_string,
           in which < and > mark the beging and end of a relation type phrase.
           Resulting in a list called 'interpreted':
           [lh_uid,lh_name,rel_uid,rel_name,rh_uid,rh_name,uom_uid,uom_name]
        '''
        string_commonalities = ['csi', 'cspi', 'csfi', 'cii', 'cipi', 'cifi']
        
        com = input("\nEnter string commonality (csi, cspi, csfi, cii, cipi, cifi): ")
        if com not in string_commonalities:
            print("String commonality {} unknown, 'cipi' used".format(com))
            com = 'cipi'
        
        # Split search_string in lh, rel and rh strings to enable search for its component
        strings = []
        known_strings = []
        # Split between lh and the rest if present
        expr = search_string.split('<', maxsplit=1)
        # lh_term is expr[0]
        strings.append(expr[0].strip())             # append lh term
        if len(expr) > 1:
            # There is a rest, thus split it between kind of relation and rh + uom if present
            rel_rh_uom = expr[1].split('>', maxsplit=1)
            strings.append(rel_rh_uom[0].strip())   # append rel phrase
            # Split third part in rh term and uom term
            rh_uom = rel_rh_uom[1].split('=', maxsplit=1)
            strings.append(rh_uom[0].strip())       # append rh term
            if len(rh_uom) > 1:
                strings.append(rh_uom[1].strip())   # append uom term
            print('Query =', strings)

        # Search for lh_string, and if present for rel_string and rh_string
        interpreted = []
        for string in strings:
            known_string = True
            print('Search for {}'.format(string))
            candidates = self.Gel_net.Query_network_dict(string, com)
            
            if len(candidates) > 0:
                # If candidates found, then show candidates for selection
                for candidate in candidates:
                    obj_uid  = candidate[1][0]
                    obj_name = candidate[0][2]
                    print("  Candidate {} {}s".format(obj_uid, obj_name))
                    
                sel_uid = input("\nEnter UID of selected candidate, last = 'Enter' or quit (q): ")
                # Split sel_uid to enable multiple selection (a,b,c...) ==== to be done ====
                int_val, integer = Convert_numeric_to_integer(sel_uid)
                while sel_uid != 'q':
                    # If a blank ("") is entered, then select the last candidate
                    if sel_uid == "":
                        sel_uid = obj_uid
                    # If selected uid < 100 then the object is an unknown
                    elif integer == True and int_val < 100:
                    #elif int(sel_uid) < 100:
                        self.Gel_net.unknown_quid += + 1
                        obj_uid = self.Gel_net.unknown_quid
                        obj_name = string
                        known_string = False
                    # If there is only one candidate, then select the last candidate
                    elif len(candidates) == 1:
                        sel_uid = obj_uid
                        
                    # Search for selected uid in network
                    try:
                        obj = self.Gel_net.uid_dict[sel_uid]    #= find_object(obj_uid)
                        s = obj.show(self.Gel_net, self.user)
                        obj_uid  = obj.uid
                        obj_name = obj.name
                        sel_uid = 'q'
                    except KeyError:
                        print("Selected UID '{}' is not known in the network.".format(sel_uid))
                        if integer == False or int_val >= 100:
                        #if int(sel_uid) >= 100:
                            sel_uid = input("\nEnter a UID of a selected candidate, 'Enter' or quit (q): ")  
            else:
                # No candidates found: the serach_string denotes an (next) unknown
                self.Gel_net.unknown_quid += 1
                obj_uid = self.Gel_net.unknown_quid
                obj_name = string
                known_string = False
                print("  No candidates found for ({}) {} \n".format(obj_uid, string))
            
            interpreted.append(obj_uid)
            interpreted.append(obj_name)
            known_strings.append(known_string)
            
        # If no UoMs specified then append interpreted query
        if len(strings) == 3:
            interpreted.append('')
            interpreted.append("")
            known_strings.append(False)
        # interpreted is a list[lh_uid,lh_name,rel_uid,rel_name,rh_uid,rh_name,uom_uid,uom_name]
        return known_strings, interpreted  # list of Booleans, list

    def Formulate_query_spec_for_individual(self, selected_object):
        ''' Determine from a selected individual (self.Gel_net.modified_object) a query_spec that searches for
            subtypes of its kind (self.Gel_net.selected_object) that satisfy the aspects of the individual object.
            Thus using the aspects of the individual as criteria for selection of options.
        '''
        shall_have_as_aspect_phrase = ['shall have as aspect a', 'moet als aspect hebben een']
        shall_be_phrase          = ['shall be', 'moet als kwalitatief aspect hebben']
        shall_be_made_of_phrase  = ['shall be made of', 'moet gemaakt zijn van']
        # query_spec expression = lh_uid, lh_name, rel_type_uid, rel_type_name, rh_uid_rh_name, \
        #                         uom_uid, uom_name, phrase_type_uid
        self.main.query_spec[:] = []
        query_expr = []
        print('\nFormulate query spec for ',selected_object.name)

        # Determine an aspect of the individual modified object and the classifier of the aspect
        for obj_rel in self.Gel_net.modified_object.relations:
##            expr = obj_rel.expression
##            # Search for relation type <has as aspect> (1727) to find individual aspect_uid
##            if expr[rel_type_uid_col] in self.Gel_net.subPossAspUIDs:
            # Search for relation type <has as aspect> (1727) to find an individual aspect
            if obj_rel.rel_type.uid in self.Gel_net.subPossAspUIDs:
                if obj_rel.phrase_type_uid == basePhraseUID:     # Base phrase
                    aspect = obj_rel.rh_obj
                    if len(aspect.classifiers) > 0:
                        classifier = aspect.classifiers[0]
                    else:
                        print('Aspect {} is not classified. Not usable for formulating a condition'.format(aspect.name))
                        continue
                    # Formulate expression: selected_object 'has by definition as aspect a' aspect_kind, uom
                    query_expr = [selected_object.uid, selected_object.name, \
                                  '4956', shall_have_as_aspect_phrase[self.user.GUI_lang_index], \
                                  classifier.uid, classifier.name, '' , '', basePhraseUID]
                    self.main.query_spec.append(query_expr)
                    
                    self.rolePlayersQTypes = 'thingsOfKinds'
                    self.q_lh_category = 'kind'
                    self.q_rh_category = 'kind of aspect'
                    
##                    print('Query line-1a: {} ({}) <{}> ({}) {} ({})'.\
##                          format(query_expr[1], query_expr[0], query_expr[3], \
##                                 query_expr[2], query_expr[5], query_expr[4]))

                    # Formulate_condition(s) for kind from_individual aspect value
                    for asp_rel in aspect.relations:
                        # Search for qualification or quantification of the aspect
                        if asp_rel.rel_type.uid in self.Gel_net.subQuantUIDs:
                            
                            # Quantification relation found:
                            # Expression becomes: classifier <shall have on scale a value ...> value (on scale:) uom
                            # Transform rel_type of individual to rel_type for requirement
                            if asp_rel.rel_type.uid == '5025':
                                # If rel-type is <has on scale a value equal to> (5025)
                                #    then rel_type becomes <shall have on scale a value equal to> (5492)
                                conceptual_rel_type = self.Gel_net.uid_dict['5492']

                            elif asp_rel.rel_type.uid == '5026':
                                # If rel-type is <has on scale a value greater than> (5026)
                                #    then rel_type becomes <shall have on scale a value greater than> (5493)
                                conceptual_rel_type = self.Gel_net.uid_dict['5493']
                                
                            elif asp_rel.rel_type.uid == '5027':
                                # If rel-type is <has on scale a value less than> (5027)
                                #    then rel_type becomes <shall have on scale a value less than> (5494)
                                conceptual_rel_type = self.Gel_net.uid_dict['5494']

                            elif asp_rel.rel_type.uid == '5489':
                                # If rel-type is <has on scale a value greater than or equal to> (5489)
                                #    then rel_type becomes <shall have on scale a value greater than or equal to> (5632)
                                conceptual_rel_type = self.Gel_net.uid_dict['5632']

                            elif asp_rel.rel_type.uid == '5490':
                                # If rel-type is <has on scale a value less than or equal to> (5490)
                                #    then rel_type becomes <shall have on scale a value less than or equal to> (5633)
                                conceptual_rel_type = self.Gel_net.uid_dict['5633']

                            else:
                                continue
                            # Conversion from qualification to conceptual qualification found:
                            # thus formulate condition in query_spec
                            # Determine base phrase of relation type in GUI language
                            #print('Condition rel_type', conceptual_rel_type.name, len(conceptual_rel_type.basePhrases_in_context))
                            if len(conceptual_rel_type.basePhrases_in_context) > 0:
                                rel_type_name = conceptual_rel_type.basePhrases_in_context[0][2]
                                for phrase_in_context in conceptual_rel_type.basePhrases_in_context:
                                    if phrase_in_context[0] == self.user.GUI_lang_uid:
                                        rel_type_name = phrase_in_context[2]
                                        continue
                                #print('Rel_type_name', rel_type_name, self.user.GUI_lang_uid, conceptual_rel_type.basePhrases_in_context)
                                # Formulate condition expression:
                                #   kind_of)aspect 'shall have on scale a value ...' value, uom
                                print('Condition: {} <{}> {} {}'.\
                                      format(classifier.name, rel_type_name, \
                                             asp_rel.rh_obj.name, asp_rel.uom.name))
                                condition = [classifier.uid, classifier.name, \
                                             conceptual_rel_type.uid, rel_type_name, \
                                             asp_rel.rh_obj.uid, asp_rel.rh_obj.name, \
                                             asp_rel.uom.uid, asp_rel.uom.name, basePhraseUID]
                                self.main.query_spec.append(condition)
                                #self.condition_table.append(condition)
                                
                            else:
                                print('No conversion base phrase available for {} ({})'.\
                                      format(conceptual_rel_type.name, conceptual_rel_type.uid))
                elif obj_rel.rel_type.uid == '4853':
                    # Object is classified/qualified by a qualitative aspect (<is>)
                    # results in requirement: <shall be> (5791)
                    qual_aspect = obj_rel.rh_obj
                    # Formulate expression: selected_object 'is by definition qualified as' qualitative aspect, uom
                    query_expr = [selected_object.uid, selected_object.name, \
                                  '5791', shall_be_phrase[self.user.GUI_lang_index], \
                                  qual_aspect.uid, qual_aspect.name, '' , '', basePhraseUID]
##                    print('Query line-1b: {} ({}) <{}> ({}) {} ({})'.\
##                          format(query_expr[1], query_expr[0], query_expr[3], \
##                                 query_expr[2], query_expr[5], query_expr[4]))
                    self.main.query_spec.append(query_expr)
                    
                    self.rolePlayersQTypes = 'thingsOfKinds'
                    self.q_lh_category = 'kind'
                    self.q_rh_category = 'kind of aspect'

                elif obj_rel.rel_type.uid == '5423':
                    # Expression found: Object <is made of> construction material
                    # results in requirement: <shall be made of> (4995)
                    qual_aspect = obj_rel.rh_obj
                    # Formulate expression: selected_object 'is by definition qualified as' qualitative aspect, uom
                    query_expr = [selected_object.uid, selected_object.name, \
                                  '4995', shall_be_made_of_phrase[self.user.GUI_lang_index], \
                                  qual_aspect.uid, qual_aspect.name, '' , '', basePhraseUID]
                    print('Query line-1c: {} ({}) <{}> ({}) {} ({})'.\
                          format(query_expr[1], query_expr[0], query_expr[3], \
                                 query_expr[2], query_expr[5], query_expr[4]))
                    self.main.query_spec.append(query_expr)
                    
                    self.rolePlayersQTypes = 'thingsOfKinds'
                    self.q_lh_category = 'kind'
                    self.q_rh_category = 'kind of aspect'

    def Interpret_query_spec(self):
        ''' Interpret a query_spec, consisting of one or more lines
            and if a single object is requested, then build product model and view
            or when possibly multiple objects are resulting, then execute the query
            and build the various product models and views.
        '''
        self.obj_list[:] = []
        #print('Query_spec:', self.main.query_spec)
        # If the query interpretation found a single known object (no query expression and not an unknown),
        # thus the first spec line has <= 2 fields and the uid >= 100,
        # then find the object by uid and show/display its data and its subtypes when applicable.
        int_uid, integer = Convert_numeric_to_integer(self.main.query_spec[0][0])
        if len(self.main.query_spec[0]) <= 2 and (integer == False or int_uid >= 100):
            # Single known object (uid) found. Find obj with uid in dictionary
            uid = self.main.query_spec[0][0]
            obj = self.Gel_net.uid_dict[uid]
            
            # If obj is a kind of role, then build model of kind of role player (if known) instead of kind of role
            if obj.category == 'kind of role':
                player_found = False
                for rel_obj in obj.relations:
                    expr = rel_obj.expression
                    # Determine whether the relation defines a kind of role player (5343 = is by def a role of a)
                    if expr[lh_uid_col] == obj.uid and expr[rel_type_uid_col] == by_def_role_of_ind:
                        role_player_uid = expr[rh_uid_col]
                        role_player = self.Gel_net.uid_dict[role_player_uid]
                        player_found = True
                        print('Role {} replaced by role player {}'.format(obj.name, role_player.name))
                        continue
                if player_found == False:
                     role_player = obj
                # Append role_player to list of objects to be displayed
                self.obj_list.append(role_player)    
            else:
                # Append object to list of objects to be displayed
                self.obj_list.append(obj)
                
            # Build single product model (list with one element)
            self.Gel_net.Build_product_views(self.obj_list)

        else:
            # Query is an expression
            self.Execute_query()

    def Create_query_file(self):
        ''' Create a file in Gellish Expression format on the basis of self.main.query_spec'''
        #print('Query_spec example:', self.main.query_spec)
        # Query_spec example:
        # [['251691', 'three core cable', '4956', 'moet als aspect hebben een', '550206', 'outside diameter', '', '', '6066'],
        #  ['550206', 'outside diameter', '5492', 'shall have as scale value', '2000000030', '30',    '570423', 'mm', '6066']]
        self.gel_expressions = []
        idea_uid = 100
        lang_uid  = '910037'
        lang_name = 'Nederlands'
        comm_uid  = ''
        comm_name = ''
        lang_comm = [lang_uid, lang_name, comm_uid, comm_name]
        intent_uid_name = ['790665','vraag']
    
        for row in self.main.query_spec:
            idea_uid += +1
            if len(row) == 9:
                lh_uid_name         = [row[0], row[1]]         # e.g. '251691', 'three core cable'
                rel_uid_phrase_type = [row[2], row[3], row[8]] # e.g. '4956'  , 'moet als aspect hebben een'
                rh_role_uid_name    = ['', '']
                rh_uid_name         = [row[4], row[5]]         # e.g. '550206', 'outside diameter'
                uom_uid_name        = [row[6], row[7]]
                description         = ''
                gellish_expr = Create_gellish_expression(lang_comm, str(idea_uid), intent_uid_name,\
                                                         lh_uid_name, rel_uid_phrase_type,\
                                                         rh_role_uid_name, rh_uid_name, \
                                                         uom_uid_name, description)
                #print('Gellish_expr1:', gellish_expr)
                self.gel_expressions.append(gellish_expr)

        # Save gel_expressions in query_file
        subject_name = ['query_spec', 'vraagspecificatie']
        file_lang_name = 'Nederlands'
        serialization = 'csv'
        Open_output_file(self.gel_expressions, 'query', file_lang_name, serialization)
        
    def Execute_query(self):
        """ Execute a query on the network for the relation type and its subtypes.
            Store resulting candidate objects in a list (self.candidates)
            with expressions in self.candid_expressions with the same table definition.

            - Options list definition:
              OptionNr, whetherKnown, lang_uid, comm_uid, resultString, self.Gel_net.unknown_quid
        """
        self.query_expr = self.main.query_spec[0]
        self.q_lh_uid      = self.query_expr[0]
        self.q_lh_name     = self.query_expr[1]
        self.q_rel_uid     = self.query_expr[2]
        self.q_rel_name    = self.query_expr[3]
        self.q_rh_uid      = self.query_expr[4]
        self.q_rh_name     = self.query_expr[5]
        self.phrase_type_uid = self.query_expr[8]
                    
        # query item: [self.q_lh_uid, self.q_lh_name, self.q_rel_uid, self.q_rel_name,
        #              self.q_rh_uid, self.q_rh_name, self.q_uom_uid, self.uom_name, self.q_phrase_type_uid]
        q_lh_uid_index   = 0
        q_lh_name_index  = 1
        q_rel_uid_index  = 2
        q_rel_name_index = 3 # Not used
        q_rh_uid_index   = 4
        q_rh_name_index  = 5
        #self.q_phrase_type_index = 8 # Not used
        #indOrMixRelUID= 6068      # 6068 binary relation between an individual thing and something (indiv or kind)
        
        self.Gel_net.sub_level = 0
        self.Gel_net.all_subtypes[:] = []

        list_of_categories = ['kind', 'kind of aspect', 'kind of occurrence']
        
    # Consistency check on query
        # If relation type specifies a relation between individual physical objects and the lh_object is known
        # then lh_object may not be a kind or kind of occurrence; idem for rh_object
        int_q_lh_uid, lh_integer = Convert_numeric_to_integer(self.q_lh_uid)
        int_q_rh_uid, rh_integer = Convert_numeric_to_integer(self.q_rh_uid)
        if self.rolePlayersQTypes == 'individuals' and \
           (((lh_integer == False or int_q_lh_uid >= 100) and self.q_lh_category in list_of_categories) or \
            ((rh_integer == False or int_q_rh_uid >= 100) and self.q_rh_category in list_of_categories)):
            print('Warning: Relation type <{}> relates individual things, \
but one or both related things are kinds of things. Try again.'.\
                                  format(self.q_rel_name, self.q_lh_uid, self.q_lh_category,\
                                         self.q_rh_uid  , self.q_rh_category))
            #return

        # If relation type specifies a relation between kinds and the lh_object is known
        # then lh_object shall be a kind or kind of occurrence; idem for rh_object   
        elif (self.rolePlayersQTypes == 'hierOfKinds' or self.rolePlayersQTypes == 'thingsOfKinds') and \
             (((lh_integer == False or int_q_lh_uid >= 100) and self.q_lh_category not in list_of_categories) or \
              ((rh_integer == False or int_q_rh_uid >= 100) and self.q_rh_category not in list_of_categories)):
            print('Warning: Relation type <{}> relates kinds of things, \
but left {} ({}) or right {} ({}) related things are not kinds. Try again.'.\
                                  format(self.q_rel_name, self.q_lh_uid, self.q_lh_category,\
                                         self.q_rh_uid  , self.q_rh_category))
            #return
            
        elif self.rolePlayersQTypes == 'individualAndKind':
            if ((lh_integer == False or int_q_lh_uid >= 100) and self.q_lh_category in list_of_categories):
                print('Warning: Relation type <{}> relates an individual thing to a kind, \
but the left hand object {} ({}) is a kind. Try again.'.format(self.q_rel_name, self.q_lh_uid, self.q_lh_category))
                
        elif self.rolePlayersQTypes == 'kindAndIndividual':
            if ((rh_integer == False or int_q_rh_uid >= 100) and self.q_rh_category in list_of_categories):
                print('Warning: Relation type <{}> relates a kind to an individual thing, \
but the right hand object {} ({}) is a kind. Try again.'.format(self.q_rel_name, self.q_rh_uid, self.q_rh_category))
                
        elif self.rolePlayersQTypes == 'individualAndMixed':
            if ((lh_integer == False or int_q_lh_uid >= 100) and self.q_lh_category in list_of_categories):
                print('Warning: Relation type <{}> relates an individual thing to an individual or kind, \
but the left hand object {} ({}) is a kind. Try again.'.format(self.q_rel_name, self.q_lh_uid, self.q_lh_category))

        # Determine UIDs of subtypes of relation type to enable searching also the subtypes of the relation type
        self.q_rel_subtype_uids[:] = []
        
        self.q_rel_subtype_uids.append(self.query_expr[q_rel_uid_index])
        
        # If relUID of query (self.query_expr) known then determine rel_type object and its list of subtypes
        int_q_rel_uid, rel_integer = Convert_numeric_to_integer(self.query_expr[q_rel_uid_index])
        if rel_integer == False or int_q_rel_uid >= 100:
            rel_type = self.Gel_net.uid_dict[self.query_expr[q_rel_uid_index]]
            # Find subtypes of specified relation type
            self.q_rel_subtypes, self.q_rel_subtype_uids = self.Gel_net.Determine_subtypes(rel_type)  
            #print('Subtypes of relation',self.query_expr[q_rel_uid_index],':',subRels)
            self.q_rel_subtype_uids.append(self.query_expr[q_rel_uid_index])
        #print('Relation type and subtypes:',self.q_rel_subtype_uids)
                
        # Candidate answers ========
        cand_text = ['Candidate answers:','Kandidaat antwoorden:']
        print('\n{}'.format(cand_text[self.user.GUI_lang_index]))

        # Initialize whether types are known
        self.q_lh_category = 'unknown'
        self.q_rh_category = 'unknown'
        # If lh object is a known, then ...
        
        if lh_integer == False or int_q_lh_uid >= 100:
            # If lh is possibly a kind then determine its subtypes
            if self.rolePlayersQTypes in ['kindAndIndividual', 'mixedAndIndividual', 'hierOfKinds',\
                                           'thingsOfKinds']:
                self.q_lh_category = 'kind'
                self.q_lh_subtypes, self.q_lh_subtype_uids = self.Gel_net.DetermineSubtypeList(self.q_lh_uid)
                
                # If relation type is a transitive relation type then
                # determine hierarchical network (chain) of rh_uids that relate to the q_lh_uid of the query
                if self.q_rel_uid in self.Gel_net.transitiveRelUIDs:
                    self.Transitive_hier_network(self.q_lh_subtypes, self.q_rel_subtype_uids, self.q_phrase_type_uid)
                    self.rh_hierarchical_net_uids = self.net_uids
            else:
                self.q_lh_category = 'individual'
                self.q_lh_subtypes[0] = self.q_lh_obj

        # If rh object is a known and is possibly a kind then determine its subtypes
        if rh_integer == False or int_q_rh_uid >= 100:
            if self.rolePlayersQTypes in ['individualAndKind', 'individualAndMixed', 'hierOfKinds',\
                                          'thingsOfKinds']:
                self.q_rh_category = 'kind'
                self.q_rh_subtypes, self.q_rh_subtype_uids = self.Gel_net.DetermineSubtypeList(self.q_rh_uid)
                
                # If relation type is a transitive relation type then
                # determine hierarchical network (chain) of lh_uids that relate to the q_rh_uid of the query
                if self.q_rel_uid in self.Gel_net.transitiveRelUIDs:
                    self.Transitive_hier_network(self.q_rh_subtypes, self.q_rel_subtype_uids, self.q_phrase_type_uid)
                    self.lh_hierarchical_net_uids = net_uids
            else:
                self.q_rh_category = 'individual'
                self.q_rh_subtypes[0] = self.q_rh_obj

        # Build list of candidates and candid_uid_dict
        # Collect expressions that match first self.query_expr expression in candid_expressions table.
        
        self.about  = ['about' ,'over']
        indeed = ['Indeed','Inderdaad']
        
        # If q_lh_object of query is unknown, (q_lh_uid < 100) ('what-1')
        if lh_integer == False or int_q_lh_uid < 100:
            # rh_object of query is known (q_rh_uid > 99) while q_lh object is unknown
            if rh_integer == False or int_q_rh_uid >= 100: 
                # If relation_type object of query is known (q_rel_uid > 99) is known, then
                if int_q_rel_uid >= 100:                  
                    # If self.q_rh_category == 'individual' then search for matches for the individual
                    # If self.q_rh_category == 'kind' then search for matches for the kind and its subtypes
                    # Search in the relations of rhq_object 
                    # for expressions with the specified relation type(s) or one of its subtypes
                    if self.q_rh_category == 'kind':
                        for rh_sub in self.q_rh_subtypes:
                            self.Find_candidates(rh_sub)
                    else:
                        # self.q_rh_category == 'individual'
                        self.Find_candidates(self.q_rh_obj)
                else:
                    # Relation type q_rel of query is unknown.
                    # Determine whether lh and rh objects (and their subtypes) are related
                    #           and if yes, by which kinds of relations
                    print('=== to be done === by which kinds of relations are lh object {} and rh object {} related?'.\
                          format(self.query_expr[q_lh_name_index], self.query_expr[q_rh_name_index]))
            
            # If rh_object of query is also unknown (q_rh_uid < 100) ('what-2') then error meassage
            else:
                # rh_object of query in also unknown (self.query_expr[q_rh_uid_index] < 100)
                # Both q_lh and q_rh object are unknown
                if self.user.GUI_lang_index == 1:
                    print('\n  Fout: Ofwel de linker term of de rechter term moet bekend zijn. Probeer opnieuw')
                else:
                    print('\n  Error: Either left hand term or right hand term should be known. Try again')
                return
                    
        # lhUID is in vocabulary (thus lh is known) because self.query_expr[q_lh_uid_index] >= 100.
        else:
            # For the self.q_lh object and its subtypes find expressions that match the first query expression 
            for q_lh_sub in self.q_lh_subtypes:
                # Search in the relations of lh_object for a relation type that corresponds with q_rel or its subtypes
                for lh_obj_rel in q_lh_sub.relations:
                    expr = lh_obj_rel.expression
                    if expr[rel_type_uid_col] in self.q_rel_subtype_uids:
                        # If rh object is also known (q_rh_uid >= 100) then verify whether expression complies with query 
                        if int_q_rh_uid >= 100:
                            # If also the rh or its subtype correpond with the q_rh
                            # (the expression complies with the self.query_expr),
                            #  then display message: confirm that the expression complies.
                            # === This does not hold for the inverse. Transitive!!! roles should comply (=== to be added ===)
                            if expr[rh_uid_col] in self.q_rh_subtype_uids:
                                print('  {}: {} <{}> {} {}'.\
                                      format(indeed[self.user.GUI_lang_index],expr[intent_name_col],\
                                             expr[lh_name_col],expr[rel_type_name_col],expr[rh_name_col]))
                                # Create candidate object and add object to list of candidates and expressions, if not yet present
                                self.Record_and_verify_candidate_object(expr)
                    
                            # If rh not in subtype list, but self.q_rel_uid is a transitive relation type
                            # then verify whether the transitive relation is satisfied.
                            elif self.q_rel_uid in self.Gel_net.transitiveRelUIDs:
                                if expr[rh_uid_col] in self.rh_hierarchical_net_uids:
                                    # Indeed, rh_object is by transitive chain related to lh_object
                                    print('\n  {}: {} {} {} {}'.\
                                          format(indeed[self.user.GUI_lang_index],expr[intent_name_col],\
                                                 expr[lh_uid_col],expr[rel_type_name_col],expr[rh_name_col]))
                                    # Create candidate object and add object to list of candidates, if not yet present
                                    # Add expression to the list of candidate expressions, if not yet present
                                    self.Record_and_verify_candidate_object(expr)
                                
    ##                # if self.q_lh_uid and self.q_rh_uid are both known, then: is the question confirmed?
    ##                if self.query_expr[q_lh_uid_index] > 99 and self.query_expr[q_rh_uid_index] > 99:
    ##                    if self.q_lh_uid == expr[lh_uid_col]:
    ##                        matchChain = TransitiveMatchChain(self.query_expr[q_lh_uid_index],self.query_expr[q_rh_uid_index],self.q_phrase_type_uid)
    ##                    elif self.q_lh_uid == expr[rh_uid_col]:
    ##                        matchChain = TransitiveMatchChain(self.query_expr[q_rh_uid_index],self.query_expr[q_lh_uid_index],self.q_phrase_type_uid)
    ##                    if matchChain[0]:
    ##                        because    = ['because...','omdat...']
    ##                        print('\n  {}: {} {} {} {} {}'.\
    ##                              format(indeed[self.user.GUI_lang_index],expr[intent_name_col],\
    ##                                     self.query_expr[q_lh_name_index],self.q_rel_name,self.query_expr[q_rh_name_index],\
    ##                                     because[self.user.GUI_lang_index]))
    ##                        for step in reversed(matchChain[1:]):
    ##                            print('\n    {} <{}> {}'.format(step[1],self.q_rel_name,step[3]))
    ##                    else:
    ##                        denial  = ['No, it is not true that','Nee, het niet waar dat']
    ##                        print('\n  {}: {} {} {}'.\
    ##                              format(denial[self.user.GUI_lang_index],\
    ##                              self.query_expr[q_lh_name_index],self.q_rel_name,self.query_expr[q_rh_name_index]))
    ##                        return
    ##            else:                   # self.q_lh_uid not on expr
    ##                #if self.rolePlayersQTypes == 'kindAndIndividual' or self.rolePlayersQTypes == 'mixedAndIndividual' \
    ##                #   or self.rolePlayersQTypes == 'hierOfKinds' or self.rolePlayersQTypes == 'thingsOfKinds':
    ##                if self.rolePlayerQTypeLH == 'kind':
    ##                    if expr[lh_uid_col] in self.q_lh_subtype_uids or expr[rh_uid_col] in self.q_lh_subtype_uids:
    ##                        self.Record_and_verify_candidate_object(expr)

        # Unknown relation type: Any relation type is O.K. self.q_rel_uid not in vocabulary ('what')
        if rel_integer == False or int_q_rel_uid < 100: 
            if lh_integer == False or int_q_lh_uid >= 100:              # is self.q_lh_uid of self.query_expr in vocabulary?
                # Search for facts about self.q_lh_uid
                for lh_obj_rel in self.q_lh_obj.relations:
                    expr = lh_obj_rel.expression   
                    if self.rolePlayersQTypes in ['mixed', 'individualAndKind', 'kindAndIndividual']:
                        self.Record_and_verify_candidate_object(expr)
            else:
                # self.q_lh_uid of self.query_expr not in vocabulary ('what')
                if rh_integer == False or int_q_rh_uid >= 100:          # is self.q_rh_uid of self.query_expr in vocabulary?
                    if self.q_rh_uid == row[rh_uid_col]:
                        for rel_rh_obj in self.q_rh_obj.relations:
                            expr = rel_rh_obj.expression 
                            if self.rolePlayersQTypes in ['mixed', 'individualAndKind', 'kindAndIndividual']:
                                self.Record_and_verify_candidate_object(expr)

        if len(self.candidates) == 0:
        #if len(self.candid_expressions) == 0:
            noExpressions = ['No candidates found','Geen kandidaten gevonden']
            print('\n{}'.format(noExpressions[self.user.GUI_lang_index]))
            return
        else: 
            # Candidates found
            satisText  = ['Confirmed','Bevestigd']
            #satisText2 = ['satisfies the query and conditions','voldoet aan de vraag en de voorwaarden']

            # If there are candidate expressions then show complying candidate expression
            if len(self.candid_expressions) > 0:
                for candid_expr in self.candid_expressions:
                    self.answer_expressions.append(candid_expr)
                    # Report confirmed candidate lh_name, rel_type_name, rh_name
                    print('\n    {} {}: <{}> <{}> <{}>'.\
                          format(satisText[self.user.GUI_lang_index],len(self.answer_expressions),candid_expr[lh_name_col],\
                                 candid_expr[rel_type_name_col], candid_expr[rh_name_col]))
##            if len(self.main.query_spec) > 1:
##                # Verify conditions on candidates (self.candidates / self.candid_expressions)
##                # and storeresults in self.answer_expressions
##                for candid in self.candidates:
##                    self.Verify_conditions(candid, candid_expr)
            
        print('Start generating views of {} candidate objects. Role player types: {}.'\
              .format(len(self.candid_expressions), self.rolePlayersQTypes))

        # Determine the objects_in_focus.
        # If lh and rh role players of query expression might be individual things
        # and not a kind or occurrence, then
        # if lh_object is known then the lh_object is the object_in_focus.
        if self.rolePlayersQTypes in ['individuals', 'individualAndMixed', 'mixedAndIndividual']:
            # if lhUID and lhName is known in namingTable, then determine object in focus
            if self.lhSel[1] == 'known':
                if self.q_lh_category != 'kind' and self.q_lh_category != 'occurrence':
                    # The left hand object in self.query_expr is the object in focus
                    object_in_focus = self.Gel_net.uid_dict[self.q_lh_uid]
                    self.objects_in_focus.append(object_in_focus)
##                    self.UIDsInFocus.append(self.q_lh_uid)
##                    self.namesInFocus.append(self.q_lh_name)
            elif self.rhSel[1] == 'known':
                # if lhUID is not known, and rhUID (and rhName) is known in namingTable, then:
                if self.q_rh_category != 'kind' and self.q_rh_category != 'occurrence':
                    # The right hand object in self.query_expr is the object in focus
                    object_in_focus = self.Gel_net.uid_dict[self.q_rh_uid]
                    self.objects_in_focus.append(object_in_focus)
##                    self.UIDsInFocus.append(self.q_rh_uid)
##                    self.namesInFocus.append(self.q_rh_name)
            else:
                if self.user.GUI_lang_index == 1:
                    print('\n  Fout: Zowel linker object <%s> als ook rechter object <%s> is onbekend; \
Probeer opnieuw.' % (self.q_lh_name,self.q_rh_name))
                else:
                    print('\n  Error: Left hand object <%s> as well as right hand object <%s> unknown; \
Try again.' % (self.q_lh_name,self.q_rh_name))
                return
            if self.test: print('UIDs in Focus:', self.rolePlayersQTypes, object_in_focus.name,\
                                self.q_lh_category, self.q_rh_category)
            self.categoryInFocus = 'individual'
            self.Gel_net.Build_single_product_view(object_in_focus)

        # Else if lh and rh role players of query expression are an individual and a kind    
        elif self.rolePlayersQTypes in ['mixed', 'individualAndKind', 'kindAndIndividual']:
            obj_list = []
            for expr in self.answer_expressions:
                object_in_focus = self.Gel_net.uid_dict[expr[lh_uid_col]]
                obj_list.append(object_in_focus)
            self.categoryInFocus = 'individual'

            # Start building product models about found self.candid_expressions
            self.Gel_net.Build_product_views(obj_list)

        # Build models/views for kinds
        elif self.rolePlayersQTypes in ['hierOfKinds', 'thingsOfKinds']:
            if self.lhSel[1] == 'known':
                # The left hand object in the self.query_expr is the object in focus
                object_in_focus = self.Gel_net.uid_dict[self.q_lh_uid]
                self.objects_in_focus.append(object_in_focus)
##                self.UIDsInFocus.append(self.q_lh_uid)
##                self.namesInFocus.append(self.q_lh_name)
            elif self.rhSel[1] == 'known':
                # The right hand object in the self.query_expr is the object in focus
                object_in_focus = self.Gel_net.uid_dict[self.q_rh_uid]
                self.objects_in_focus.append(object_in_focus)
##                self.UIDsInFocus.append(self.q_rh_uid)
##                self.namesInFocus.append(self.q_rh_name)
            else:
                print('\n  Error: Left hand kind <{}> as well as \
right hand kind <{}> unknown; Try again.'.format(self.q_lh_name,self.q_rh_name))
                return
            self.categoryInFocus = 'kind'
            obj_list = []
            obj_list.append(object_in_focus)
            self.Gel_net.Build_product_views(obj_list)
        else:
            self.Other_views()

    def Record_and_verify_candidate_object(self, expr):
        ''' Identify candidate object and add object to list of candidates, if not yet present
            Then verify additional conditions, if present
        '''
        candid_uid = expr[lh_uid_col]
        if candid_uid not in self.candid_uid_dict:
            candid = self.Gel_net.uid_dict[candid_uid]
            self.candidates.append(candid)
            self.candid_uid_dict[candid_uid] = candid
        else:
            candid = self.candid_uid_dict[candid_uid]
            
        if expr not in self.candid_expressions:
            self.candid_expressions.append(expr)
            print('  {} {} {} [{}]: <{}> <{}> <{}>. '.\
                  format(expr[intent_name_col], len(self.candid_expressions),\
                         self.about[self.user.GUI_lang_index], self.q_lh_name,\
                         expr[lh_name_col], expr[rel_type_name_col], expr[rh_name_col]))

            # If additional conditions are specified then verify conditions
            if len(self.main.query_spec) > 1:
                self.Verify_conditions(candid, expr)

    def Find_candidates(self, rhq):
        ''' Search for relations with object rhq that comply with the kind of relation in the query
            and collect the relations in self.candid_expressions
        '''
        for obj_rel in rhq.relations:
            expr = obj_rel.expression
            # If relation of q_rh_obj is equal to self.q_rel_uid or one of its subtypes
            if expr[rel_type_uid_col] in self.q_rel_subtype_uids:
                self.candid_expressions.append(expr)
                print('\n  {} {} {} [{}]: <{}> <{}> <{}>.'.\
                      format(expr[intent_name_col], len(self.candid_expressions), self.about[self.user.GUI_lang_index],\
                             self.q_rh_name, expr[lh_name_col], expr[rel_type_name_col], expr[rh_name_col]))
    
##                        #if row[rh_uid_col] in self.q_rh_subtype_uids or row[lh_uid_col] in self.q_rh_subtype_uids: 
##                            if self.rolePlayersQTypes == 'mixed' or self.rolePlayersQTypes == 'individualAndKind' \
##                               or self.rolePlayersQTypes == 'kindAndIndividual' or row[rel_type_uid_col] == classifUID\
##                               or self.rolePlayersQTypes == 'hierOfKinds' or self.rolePlayersQTypes == 'thingsOfKinds': 
##                                self.candid_expressions.append(row)
##                                #self.UIDsInFocus.append (row[lh_uid_col])  # To be moved to condition verification
##                                #self.namesInFocus.append(row[lh_name_col]) # To be moved to condition verification
##                            print('\n  {} {} {} [{}]: <{}> <{}> <{}>.'.\
##                                  format(row[intent_name_col], len(self.candid_expressions), self.about[self.user.GUI_lang_index],\
##                                         self.q_rh_name, row[lh_name_col], row[rel_type_name_col], row[rh_name_col]))
        
            # If self.q_rel_uid is a transitive relation type 
            if self.q_rel_uid in self.Gel_net.transitiveRelUIDs:
                if expr[rh_uid_col] in self.hierarchical_net_uids: 
                    #print ('candidate:', self.q_rel_name,row[rh_uid_col],row[rh_name_col])
                    self.candid_expressions.append(expr)
                    print('\n  {} {} {} [{}]: <{}> <{}> <{}>.'.\
                          format(expr[intent_name_col], len(self.candid_expressions), self.about[self.user.GUI_lang_index],\
                                 self.q_rh_name, expr[lh_name_col], expr[rel_type_name_col], expr[rh_name_col]))
                
##                        # self.q_rh_uid of Query is not equal l/rhUIDEx; maybe a classification by a subtype
##                        else:
              # if not a relation between individual things
##                            if not self.rolePlayersQTypes == 'individuals':      
                  # 'what' is related by a <is related to (a)> or its subtypes.
##                                if self.q_rel_uid in self.Gel_net.indOrMixRelUIDs:              
##                                    #print('row[rh_uid_col]:',row[rh_uid_col])
##                                    if self.rolePlayerQTypeRH == 'kind':
                          # If rhUID is a subtype of known kind (= self.q_rh_uid of self.query_expr)
##                                        if row[rh_uid_col] in self.q_rh_subtype_uids:
                              # 'what' <is classified as a> 'subtype of known kind'           
##                                            #self.rolePlayersQTypes == 'mixed':  # individual related to kind
##                                            self.candid_expressions.append(row)
##                                            #self.UIDsInFocus.append (row[lh_uid_col])  # To be moved to condition verification
##                                            #self.namesInFocus.append(row[lh_name_col]) # To be moved to condition verification
##                                            print('\n  {} {} {} [{}]: <{}> <{}> <{}>.'.\
##                                                  format(row[intent_name_col], len(self.candid_expressions), self.about[self.user.GUI_lang_index],\
##                                                         self.q_rh_name, row[lh_name_col], row[rel_type_name_col], row[rh_name_col]))
#--------------------------------------------------
    def Transitive_hier_network(self, base_objects, rel_subtype_uids, phrase_type_uid): # ,target_uid
        """ Search recursively for a chain (hierarchical network) of objects and uids
            that relate to base_uid and that are related by a relation of type q_rel_uid (or its subtypes)
            to a possible target_uid, in the required search direction (indicated by the phrase_type_uid).
            First a tree of branches may be found. When the target objects is found in a branch, then the inverse route
            is followed to find the chain.
            The resulta are a list of objects and a list of uids that are the chain of objects from base to target
        """
        self.net_uids[:] = []
        self.branches[:] = []
        self.Transitive_match(base_objects, rel_subtype_uids, phrase_type_uid)         

    def Transitive_match(self, base_objects, rel_subtype_uids, phrase_type_uid):
        #base_phrase_type_uid = '6066'
        new_direct_related_uids = []
        for obj in base_objects:
            for rel_obj in obj.relations:
                expr = rel_obj.expression
                # Search in relations of obj for expressions of type q_rel or its subtypes 
                if expr[rel_type_uid_col] in rel_subtype_uids:
                    if expr[lh_uid_col] == obj.uid and expr[phrase_type_uid_col] == phrase_type_uid:
                        related_uid = expr[rh_uid_col]
                        if related_uid not in self.net_uids:
                            self.net_uids.append(related_uid)
                            new_direct_related_uids.append(related_uid)
                        branch = [expr[lh_uid_col],expr[lh_name_col],expr[rh_uid_col],expr[rh_name_col]]
                        self.branches.append(branch)
                        
                    # Search for relations in inverse expressions        
                    elif expr[rh_uid_col] == obj.uid and expr[phrase_type_uid_col] != phrase_type_uid:
                        related_uid = expr[lh_uid_col]
                        if related_uid not in self.net_uids:
                            self.net_uids.append(related_uid)
                            new_direct_related_uids.append(related_uid)
                        branch = [expr[rh_uid_col],expr[rh_name_col],expr[lh_uid_col],expr[lh_name_col]]
                        self.branches.append(branch)
                            
        if new_direct_related_uids > 0:
            self.Transitive_match(new_direct_related_uids, rel_subtype_uids, phrase_type_uid)

#----------------------------------------------------------------
    def Other_views(self):
        print('Otherviews')
        
    def Formulate_conditions_from_gui(self):
        """ Determine conditions for GUI
        """
        self.answer_expressions = []
        condition = []
        #self.condition_table[:] = []
        condText = ['Condition','Voorwaarde']
        cond_satified = True
        
        # Get conditions and find condition UIDs
        for condNr in range(0,3):
            lh_cond_name  = self.lhCondVal[condNr].get()
            # Empty lh condition name marks the end of the conditions
            if lh_cond_name == '':
                continue
            string_commonality = 'csi' # case sensitive identical
            # Find uid, name and description of lh_cond_name
            unknown_lh, lh_uid_name_desc = self.Gel_net.Find_object_by_name(lh_cond_name, string_commonality)
            if unknown_lh == False:
                lh_cond_uid = lh_uid_name_desc[0]
            else:
                lh_cond_uid = 0
                print('Error: object {} not found'.format(lh_cond_name))
                      
            rel_cond_name = self.relCondVal[condNr].get()
            unknown_rel, rel_uid_name_desc = self.Gel_net.Find_object_by_name(rel_cond_name, string_commonality)
            #print('Condition name, known, uid-name-descr', rel_cond_name, unknown_rel, rel_uid_name_desc)
            if unknown_rel == False:
                rel_cond_uid = rel_uid_name_desc[0]
            else:
                rel_cond_uid = 0
                print('Error: object {} not found'.format(rel_cond_name))

            rh_cond_name  = self.rhCondVal[condNr].get()
            unknown_rh, rh_uid_name_desc = self.Gel_net.Find_object_by_name(rh_cond_name, string_commonality)
            if unknown_rh == False:
                rh_cond_uid = rh_uid_name_desc[0]
            else:
                rh_cond_uid = 0
                print('Error: object {} not found'.format(rh_cond_name))

            uom_cond_name = self.uomCondVal[condNr].get()
            if uom_cond_name != '':
                unknown_uom, uom_uid_name_desc = self.Gel_net.Find_object_by_name(uom_cond_name, string_commonality)
                if unknown_uom == False:
                    uom_cond_uid = uom_uid_name_desc[0]
                else:
                    uom_cond_uid = 0
                    print('Error: object {} not found'.format(uom_cond_name))
            else:
                uom_cond_uid = 0
            condition   = [lh_cond_uid, lh_cond_name, rel_cond_uid, rel_cond_name,\
                           rh_cond_uid, rh_cond_name, uom_cond_uid, uom_cond_name]
            print('\n{} {} {} ({}) {} ({}) {} ({}) {} ({})'.\
                  format(condText[self.user.GUI_lang_index],condNr+1, lh_cond_name,lh_cond_uid,\
                         rel_cond_name,rel_cond_uid,rh_cond_name,rh_cond_uid, uom_cond_name, uom_cond_uid))
            #self.condition_table.append(condition[:])
            self.main.query_spec.append(condition[:])
        
    def Verify_conditions(self, candid_obj, candidate_expr):
        ''' Conditions found thus
            verify whether the candidate object identified by self.candid_expressions
            satisfies the entered conditions, if any,
            and store the results in the self.answer_expressions
            with the same column definitions as the expressions.
        '''
        candid_expr = candidate_expr
        # Conditions found thus check candidate expressions on conditions
        answerHead  = ['Answer','Antwoord']
        answerText  = ['Candidate','Kandidaat']
        conditText  = ['Candidate aspect','Kandidaadaspect']
        nothing_satisfies  = ['There are no expressions found that satisfy the condition(s).',\
                       'Er zijn geen uitdrukkingen gevonden die aan de voorwaarde(n) voldoen.']
        
        print('\n{}:'.format(answerHead[self.user.GUI_lang_index]))
        candidNr = 0 

        # Verify for the candidate object whether it satisfies the other conditions.
##        for candid_expr in self.candid_expressions:
##            candid_obj = self.candid_uid_dict[candid_expr[lh_uid_col]]
        
##        for candid_rel in candid_obj.relations:
##            candid_expr = candid_rel.expression
        
        candidNr = candidNr + 1
        condNr   = 0
        candidAspectExpr = []
        rhCandidRoleUIDs = []
        rhCandidUIDs     = []
        condit_rel_subs  = []
        condit_rel_sub_uids = []

        # Verify the conditions
        # condit = [lh_cond_uid, lh_cond_name, rel_cond_uid, rel_cond_name,\
        #           rh_cond_uid, rh_cond_name, uom_cond_uid, uom_cond_name, phrase_type_uid]
        for condit in self.main.query_spec[1:]:
            condNr += + 1
            #print('\nVerify condition on', candid_obj.uid, candid_obj.name, condit)
            condit_rel_subs, condit_rel_sub_uids = self.Gel_net.DetermineSubtypeList(condit[2])
            #print('Condit_rel_subs', condit_rel_sub_uids)

            cond_obj = self.Gel_net.uid_dict[condit[0]]
            condit_lh_subs, condit_lh_sub_uids = self.Gel_net.DetermineSubtypeList(condit[0])
            if candid_obj.uid in condit_lh_sub_uids:
                # A new condition for the same object is identified.
                # Determine whether there is a relation that satisfies the condition
                satisfied_cond = False
                for obj_rel in candid_obj.relations:
                    candid_expr = obj_rel.expression
                    if candid_expr[rel_type_uid_col] in condit_rel_sub_uids:
                        #print('candid_expr[rel_type_uid_col]', candid_expr[rel_type_uid_col], candid_expr[rh_uid_col])
                        if candid_expr[rh_uid_col] == condit[4]:
                            # Condition is satisfied by expression
                            print('Candidate {} <{}> {} <with role player> {} and uom {}'.\
                                  format(candid_expr[lh_name_col], candid_expr[rel_type_name_col], \
                                         candid_expr[rh_role_name_col], candid_expr[rh_name_col], \
                                         candid_expr[uom_name_col]))
                            satisfied_cond = True
                            break
                if satisfied_cond == False:
                    print('No expression found that satisfies condition nr {}.'.format(condNr))
            else:
                # A condition on another object is detected. Possibly a qualification of the rh_role
                cond_satified = False
                candid_rh_role_uid = candid_expr[rh_role_uid_col]
                if candid_rh_role_uid == '':
                    print('** Warning: candidate expression {} <{}> {} does not have an intrinsic aspect defined'.\
                          format(candid_expr[lh_name_col], candid_expr[rel_type_name_col], candid_expr[rh_name_col]))
            
                
##                if condNr > 1:
##                    rhCandIndex = -1
##                    for rh_cand_uid in rhCandidUIDs:
##                        rhCandIndex = rhCandIndex + 1
##                        if condit[0] == rh_cand_uid:
##                            candid_rh_role_uid = rhCandidRoleUIDs[rhCandIndex]
##                            break
                else:
                    # rh_role_uid is not ''
                    # Does rh_role object have a (e.g. qualification) relation that satisfies condition
                    role_obj = self.Gel_net.uid_dict[candid_rh_role_uid]
                    for role_obj_rel in role_obj.relations:
                        expr = role_obj_rel.expression
                        #print('Lh_name and cond_name <{}> <{}> and lh_rel and cond_rel <{}> <{}>.'.\
                        #      format(expr[lh_name_col], candid_expr[rh_role_name_col], expr[rel_type_name_col], condit[3]))

                        # Verify whether the relation type of expression about the lh_uid object
                        # is 5737 <has by definition on scale a value equal to>
                        if expr[lh_uid_col] == candid_rh_role_uid and expr[rel_type_uid_col] == '5737':
                            # rh object should be a number; check that
                            #print('Verify equality of RH_value and condition value <{}>, <{}> and of both uoms {} {}?'.\
                            #      format(expr[rh_name_col], condit[5], expr[uom_name_col], condit[7]))
                            us_notation = expr[rh_name_col].replace(',','.')
                            value = us_notation.replace(' ','')
                            test_string = value.replace('.','')
                            if not test_string.isdecimal():
                                print('Warning: Value {} is not a number'.format(expr[rh_name_col]))
                            # Verify whether unit of measure differs from UoM of condition
                            if expr[uom_uid_col] != condit[6]:
                                print('** Warning: Unit of measure {} differs from condition unit {}.'.\
                                      format(expr[uom_name_col], condit[7]))
                                
                            # Verify required (in)equality depending on required kind of relation
                            int_condit_2, integer = Convert_numeric_to_integer(condit[2])
                            
                            # 5492 = shall have on scale a value equal to;
                            # 5737 = has by definition on scale a value equal to;
                            # 5025 = has on scale a value equal to
                            if condit[2] in ['5492', '5737', '5025']:
                                if float(value) == float(condit[5]):
                                    print('Condition satisfied that {} = {}'.format(float(expr[rh_name_col]),float(condit[5])))
                                    cond_satified = True

                            # 5493 = shall have on scale a value greater than;
                            # 6049 = has by definition on scale a value greater than;
                            # 5026 = has on scale a value greater than
                            if condit[2] in ['5493', '6049', '5026']:
                                if float(value) > float(condit[5]):
                                    print('Condition satisfied that {} > {}'.format(float(expr[rh_name_col]),float(condit[5])))
                                    cond_satified = True
                                    
                            # 5632 = shall have on scale a value greater than or equal to;
                            # 5978 = has by definition a value greater than or equal to;
                            # 5489 = has on scale a value greater than of equal to
                            elif condit[2] in ['5632', '5978', '5489']:
                                if float(expr[rh_name_col]) >= float(condit[5]):
                                    print('Condition satisfied that {} >= {}'.format(float(expr[rh_name_col]),float(condit[5])))
                                    cond_satified = True

                            # 5494 = shall have on scale a value less than;
                            # 6052 = has by definition on scale a value less than;
                            # 5027 = has on scale a value less than 
                            elif condit[2] in ['5494', '6052', '5027']:
                                if float(expr[rh_name_col]) < float(condit[5]):
                                    print('Condition satisfied that {} < {}'.format(float(expr[rh_name_col]),float(condit[5])))
                                    cond_satified = True
                                    
                            # 5633 = shall have on scale a value less than or equal to;
                            # 5979 = has by definition a value less than or equal to;
                            # 5490 = has on scale a value less than or equal to
                            elif condit[2] in ['5633', '5979', '5490']:
                                if float(expr[rh_name_col]) <= float(condit[5]):
                                    print('Condition satisfied that {} <= {}'.format(float(expr[rh_name_col]),float(condit[5])))
                                    cond_satified = True
                            
                            # Verify for lh_uid whether an expression with the correct relation type (or its subtype)
                            #        has an identical rh_uid
                            # condit[2] <= 99 means rh_cond_uid is an unknown.
                            elif expr[rh_uid_col] == condit[2] or int_condit_2 < 100:
                                cond_satified = True
        ##                    if expr[lh_uid_col] == candid_rh_role_uid and expr[rel_type_uid_col] in condit_rel_sub_uids and \
        ##                       (expr[rh_uid_col] == condit[4] or condit[4] < 100) or\
        ##                       expr[rh_uid_col] == candid_rh_role_uid and expr[rel_type_uid_col] in condit_rel_sub_uids and \
        ##                       (expr[lh_uid_col] == condit[4] or condit[4] < 100):
                                
                            if cond_satified == True:
                                candidAspectExpr.append(expr)
                                rhCandidRoleUIDs.append(expr[rh_role_uid_col])
                                rhCandidUIDs.append(expr[rh_uid_col])
                                print('    {} {}: <{}> <{}> <{}> <{}>'.format\
                                      (conditText[self.user.GUI_lang_index], condNr, expr[lh_name_col],\
                                       expr[rel_type_name_col], expr[rh_name_col], expr[uom_name_col]))
                                int_condit_4, integer = Convert_numeric_to_integer(condit[4])
                                if int_condit_4 >= 100:
                                    break

            if cond_satified == False:
                # If rel_cond_uid is a transitive relation type then: is the condition satisfied?
                if condit[2] in self.Gel_net.transitiveRelUIDs:
                    #if expr[lh_uid_col] == ? :
                    matchChain = TransitiveMatchChain(expr[lh_uid_col],condit_rel_subs,condit[4])
                    #elif expr[rh_uid_col] == ? :
                    #    matchChain = TransitiveMatchChain(expr[rh_uid_col],condit[2],condit[4])
                    if matchChain[0]:
                        indeed  = ['Indeed','Inderdaad']
                        because = ['because...','omdat...']
                        print('    {}: {} {} {} {}'.\
                              format(indeed[self.user.GUI_lang_index], expr[lh_name_col], condit[3],\
                                     condit[5], because[self.user.GUI_lang_index]))
                        for step in reversed(matchChain[1:]):
                            print('      {} <{}> {}'.format(step[1],condit[3],step[3]))
                        cond_satified = True
                        continue
                    else:
                        # Condition is not satisfied (even being transitive)
                        break
                else:
                    # Condition is not satisfied (cond_satified == False) and relation type is not transitive.
                    break
            
        # if last condition is also true, then:
        if cond_satified:
            self.answer_expressions.append(expr)
            satisText   = ['Confirmed','Bevestigd']
            becauseText = ['    because:','     omdat:']
            andText     = ['        and:','        en:']
            print('    {} {}: <{}> <{}> <{}> {}'.\
                  format(satisText[self.user.GUI_lang_index],len(self.answer_expressions), \
                         condit[1], condit[3], condit[5], condit[7]))
            first = True
            for candidAspect in candidAspectExpr:
                if first == True:
                    print('    {} <{}> <{}> <{}> <{}>'.\
                          format(becauseText[self.user.GUI_lang_index],    candidAspect[lh_name_col],\
                                 candidAspect[rel_type_name_col], candidAspect[rh_name_col],\
                                 candidAspect[uom_name_col]))
                    first = False
                else:
                    print('    {} <{}> <{}> <{}> <{}>'.\
                          format(andText[self.user.GUI_lang_index],candidAspect[lh_name_col],\
                                 candidAspect[rel_type_name_col],candidAspect[rh_name_col],\
                                 candidAspect[uom_name_col]))
        else:
            denial  = ['No, the condition is not satisfied that','Nee, er is niet voldaan aan de voorwaarde dat']
            print('    {}: {} {} {}'.\
                  format(denial[self.user.GUI_lang_index],expr[lh_name_col],condit[3],condit[5]))
            if candid_obj not in self.Gel_net.ex_candids:
                self.Gel_net.ex_candids.append(candid_obj)
        if len(self.answer_expressions) == 0:
            print('\n  {}'.format(nothing_satisfies[self.user.GUI_lang_index]))

    #-------------------------------------------------------------------------------
    def Verify_model(self):
        """ Build the model of an individual thing
            that is specified in a classification relation (of a query)
            and verify that model against the requirements about the kind.
        """

        shallUID = 5735
        subtypesOfShall, subShallUIDs = self.Gel_net.DetermineSubtypeList(shallUID)
        for obj in self.objects_in_focus:
            print('Verify model of %s on requirements about %s' % (nameInF, self.kindName))
            for obj_rel in obj.relations:
                expr = obj_rel.expression
                if expr[rel_type_uid_col] in subtypesOfShall:
                    lh  = expr[lh_name_col]
                    rel = expr[rel_type_name_col]
                    rh  = expr[rh_name_col]
                    #print('\n* Requirement for {}: {} <{}> {}'.format(nameInF,lh,rel,rh))
# Transform and search for satisfaction in query_table
# To be written

#-------------------------------------------------------------
if __name__ == "__main__":
    from DatabaseAPI import Database
    from SystemUsers import Language
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
    Gellish  = Language(formal_language)
    user = User('Andries')
    user.GUI_lang_name = "English"

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
