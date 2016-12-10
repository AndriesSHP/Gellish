#!/usr/bin/python3
import sys
import os
import csv
import sqlite3

from Expr_Table_Def import *
from Anything import Anything, Object, Individual, Kind, Relation, RelationType, \
     Language, GUI_Language
from Bootstrapping import *
from GellishDict import GellishDict

class Semantic_Network():
    """ Build a Semantic_Network model (called net_name) from a Gellish database (db_name).
        Gel_dict = naming dictionary that is extended by the concepts and names in the network.
        The model contains things and their relations.
        Start initially with bootstrapping base relation types,
              base_phrases being bootstrapping base phrases
              and inverse_phrases being bootstrapping inverse phrases
    """
    def __init__(self, net_name):
        self.name          = net_name
        self.base_lang     = 'English'
        self.rels          = []
        self.rel_uids      = []
        self.rel_types     = []
        self.rel_type_uids = base_rel_type_uids
        self.objects       = []
        self.object_uids   = []
        self.rh_objects    = []
        self.rh_object_uids  = []
        self.dictionary      = GellishDict()
        self.languages       = {}
        self.communities     = {}
        self.base_phrases    = boot_base_phrasesEN    + boot_base_phrasesNL
        self.inverse_phrases = boot_inverse_phrasesEN + boot_inverse_phrasesNL
        #self.names_in_contexts = []
        self.alias_uids    = boot_alias_uids
        self.allBinRels    = [] # initialize and collect all binary relation types (being 'binary relation' and its subtypes)
##        # initialize a table of kinds of binary relations and their supertype and kinds of roles
##        # TOP: bin_rel_uid(5935), super_rel_uid(2850), 4729, 'relator', 4824, 'related', 730000, 'anything', 730000, 'anything'
##        #self.relRolesTable = [] # initialize table of binary kinds of relations and their required roles and rolePlayersQTypes
##        #self.allBinRelNamesIn = []
        
##        if self.base_lang == 'Nederlands':
##            self.base_phrases    = boot_base_phrasesNL
##            self.inverse_phrases = boot_inverse_phrasesNL
##        else:
##            self.base_phrases    = boot_base_phrasesEN
##            self.inverse_phrases = boot_inverse_phrasesEN

    def Add_table_content_to_network(self, dbCursor, table):
        '''The content of 'table' in Gel_db database is added to the Semantic Network
           and the new names_in_context are added to the network.dictionary.
        '''
        #dbCursor.execute("select name from sqlite_master where type='table';")
        #print("Tables:", dbCursor.fetchall())
        
        # read an expressions table
        command = 'select * from ' + table
        print('  Command:', command)
        dbCursor.execute(command)
        rows = dbCursor.fetchall()
        #print('rows:',len(rows))
        for fields in rows:
            # read the idea uid and name
            idea_uid  = fields[idea_uid_col]
            lang_uid  = fields[lang_uid_col]
            comm_uid  = fields[comm_uid_col]
            intent_uid  = fields[intent_uid_col]

            lh_uid, lh_name = fields[lh_uid_col], fields[lh_name_col]
            rh_uid, rh_name = fields[rh_uid_col], fields[rh_name_col]
            rel_type_uid, rel_type_name = fields[rel_type_uid_col], fields[rel_type_name_col]
            phrase_type_uid = fields[phrase_type_uid_col]
            description     = fields[full_def_col]

            # collect used languages for naming left hand objects. (for use by preferences)
            if lang_uid not in self.languages:
               self.languages[lang_uid] = fields[lang_name_col]

            # collect language communities for naming left hand objects. (for use by preferences)
            if comm_uid not in self.communities:
               self.communities[comm_uid] = fields[comm_name_col]

            # create the left hand object if it does not exist and add to naming_table dictionary
            if lh_uid not in self.object_uids:
                lh = Object(lh_uid)
                self.object_uids.append(lh_uid)
                self.objects.append(lh)
                if rel_type_uid in self.alias_uids:
                    naming_uid = rel_type_uid
                else:
                    naming_uid = 5117
                lh_name_and_descr = (lang_uid, comm_uid, lh_name, naming_uid, description)
                lh.names_in_contexts.append(lh_name_and_descr)
                lh_name_in_context = (lang_uid, comm_uid, lh_name)
                value_pair = (lh_uid, naming_uid)
                #print('Dict entry: ', lh_name_in_context, value_pair)
                self.dictionary[lh_name_in_context] = value_pair
            else:
                # lh is an existing object; if alias relation, then add name_in_context to object and to dict
                lh = self.find_object(lh_uid)
                if rel_type_uid in self.alias_uids:
                    lh_name_and_descr = (lang_uid, comm_uid, lh_name, naming_uid, description)
                    lh.names_in_contexts.append(lh_name_and_descr)
                    lh_name_in_context = (lang_uid, comm_uid, lh_name)
                    value_pair = (lh_uid, rel_type_uid)
                    self.dictionary[lh_name_in_context] = value_pair
                # if rel is a subtyping relation then add a name_in_context to dict
                elif rel_type_uid in specialRelUIDs:
                    lh_name_in_context = (lang_uid, comm_uid, lh_name, naming_uid, description)
                    if lh_name_in_context not in lh.names_in_contexts:
                        lh.names_in_contexts.append(lh_name_in_context)

            # if rh object does not exist yet, then create an object
            # with a name, but without a name_in_context and without a description
            if rh_uid not in self.object_uids:
##                descr = ""
                rh = Object(rh_uid)
                rh.name = rh_name
                self.object_uids.append(rh_uid)
                self.objects.append(rh)
                self.rh_object_uids.append(rh_uid)
                self.rh_objects.append(rh)
            else:
                rh = self.find_object(rh_uid)
            
            # add the relation between objects to both objects, except when lh == rh
            if rh_uid != lh_uid:
                relation = Relation(idea_uid, fields[idea_desc_col], intent_uid, fields[intent_name_col],\
                                    lh_uid, lh_name, rel_type_uid, rel_type_name, phrase_type_uid, \
                                    rh_uid, rh_name, fields[uom_uid_col], fields[uom_name_col])
                # add the relation to both objects
                lh.add_relation(relation)
                rh.add_relation(relation)
                self.rel_uids.append(idea_uid)
                self.rels.append(relation)
                
                # if specialization relation (1146 or one of its subtypes), then add subtype and supertype to objects
                if rel_type_uid in specialRelUIDs:
                    lh.name = lh_name
                    if phrase_type_uid == 6066:
                        lh.add_supertype(rh)
                        rh.add_subtype(lh)
                    else:
                        lh.add_subtype(rh)
                        rh.add_supertype(lh)

                # if classification relation (1225 or one of its subtypes), then add classifier and classified to objects
                if rel_type_uid in classifUIDs:
                    lh.name = lh_name
                    if phrase_type_uid == 6066:
                        lh.add_classifier(rh)
                        rh.add_individual(lh)
                    else:
                        lh.add_individual(rh)
                        rh.add_classifier(lh)

        # Verify whether all rh_object_uids are defined as (lh_)object_uids
        if len(self.rh_object_uids) > 0:
            for obj_uid in self.rh_object_uids:
                obj = self.find_object(obj_uid)
                if obj.uid not in self.object_uids:
                    GUI_Language.Message(
                        '\nWarning: RH object %s (%i) not yet defined'            % (obj.name, obj.uid),\
                        '\nWaarschuwing: RH object %s (%i) nog niet gedefinieerd' % (obj.name, obj.uid))
##                else:
##                    #print('To be removed: ', obj_uid)
##                    self.rh_objects.remove(obj)
##                    #self.rh_object_uids.remove(obj.uid)
##        if len(self.rh_objects) > 0:
##            for obj in self.rh_objects:
##                print('To be defined: ', obj.uid)

    def find_object(self, obj_uid):
        '''Search in network objects for an object with uid == obj_uid.'''
        for obj in self.objects:
            if obj.uid == obj_uid:
                return(obj)

    def BuildHierarchies(self):
        ''' Build a naming table (extend the language vocabulary) and expression table
        Extent the information model by data entry and extending namingTable and exprTable,
        Append model file
        Search in ontology and informationm model (on-line or via GUI)

        Determine all subtypes of binary relation (5935)
        and firstRoles and secondRoles and role players for all subtypes of binary relation
        '''
        # Determine the list of binary relations (binRelUID = 5935) and its subtypes
        self.rel_type_uids  = self.DetermineSubtypeList(binRelUID)
        
##        allBinRelNamesIn = DetermineNames(allBinRelUIDs,modelLangUID)
##        relTermList = allBinRelNamesIn[:]
        #if test: print('RelNames:',langUID, langName, allBinRelNamesIn[1:5])

        # Determine lists of various kinds and their subtypes
        self.subClassifiedUIDs   = self.DetermineSubtypeList(classifiedUID)
        self.indOrMixRelUIDs     = self.DetermineSubtypeList(indOrMixRelUID)
        self.indivBinRelUIDs     = self.DetermineSubtypeList(indivRelUID)
        self.kindHierRelUIDs     = self.DetermineSubtypeList(kindHierUID)
        self.kindKindRelUIDs     = self.DetermineSubtypeList(kindKindUID)
        self.kindBinRelUIDs      = self.DetermineSubtypeList(kindRelUID)
        self.mixedBinRelUIDs     = self.DetermineSubtypeList(mixedRelUID)
        self.specialRelUIDs      = self.DetermineSubtypeList(specialRelUID)
        self.subtypeSubUIDs      = self.DetermineSubtypeList(subtypeRoleUID)
        self.subPossAspUIDs      = self.DetermineSubtypeList(possAspUID)
        self.subPossessorUIDs    = self.DetermineSubtypeList(possessorUID)
        self.transitiveRelUIDs   = self.DetermineSubtypeList(transRelUID)
        self.subConcPossAspUIDs  = self.DetermineSubtypeList(concPossAspUID)
        self.subConcComplRelUIDs = self.DetermineSubtypeList(concComplRelUID)
        self.qualSubtypeUIDs     = self.DetermineSubtypeList(qualSubtypeUID)
        self.qualOptionsUIDs     = self.DetermineSubtypeList(qualOptionsUID)
        self.concComplUIDs       = self.DetermineSubtypeList(concComplUID)
        self.concQuantUIDs       = self.DetermineSubtypeList(concQuantUID)
        self.subQualUIDs         = self.DetermineSubtypeList(qualifUID)
        self.subQuantUIDs        = self.DetermineSubtypeList(quantUID)
        self.subInformativeUIDs  = self.DetermineSubtypeList(informativeUID)
        self.subOccurrenceUIDs   = self.DetermineSubtypeList(occurrenceUID)
        self.subComposUIDs       = self.DetermineSubtypeList(composUID)     # composition relation and its subtypes
        self.subComponUIDs       = self.DetermineSubtypeList(componUID)     # component role and its subtypes
        self.subConcComponUIDs   = self.DetermineSubtypeList(concComponUID) # conceptual component role and its subtypes
        self.subInvolvedUIDs     = self.DetermineSubtypeList(involvedUID)
        self.subNextUIDs         = self.DetermineSubtypeList(nextUID)
        self.subtypesOfShall     = self.DetermineSubtypeList(shallUID)
        self.aliasUIDList        = self.DetermineSubtypeList(aliasUID)
        self.concWholeUIDs       = self.DetermineSubtypeList(concWholeUID)
        self.concPossUIDs        = self.DetermineSubtypeList(concPosessorUID)
        self.transUIDs           = self.DetermineSubtypeList(transUID)
        self.classifUIDs         = self.DetermineSubtypeList(classifUID)  # 1225 classification relation
        self.specialUIDs         = self.DetermineSubtypeList(specialUID)
        self.concBinRelbetKinds  = self.DetermineSubtypeList(concBinRelKindsUID) # 1231 = conc.bin. relation between things of specified kinds.
        #self.propUIDs            = self.DetermineSubtypeList(propUID)       # 551004 = property

    #----------------------------------------------------------------------------
    def DetermineSubtypeList(self, kind_uid):
        """Determine the list of a kind and its subtypes"""
        kind = self.find_object(kind_uid)
        if kind == None:
            print('Kind %i not found' % (kind_uid))
        sub_kinds = self.Determine_Subtypes(kind)
        sub_kinds.append(kind)
        return sub_kinds

#----------------------------------------------------------------------------
    def Determine_Subtypes(self, supertype):
        """Determine and return allSubtypeUIDs of supertype
           (except the supertype itself) including subSubs etc. and \
           if supertype.uid = binRelUID (5935, binary relation),
           then start building the relRolesTable
        """
        # Collect subtypes of a given supertypeUID. E.g. binary relation (5935)
        all_subtypes = []
        sub_super = []
##        top = supertype
##        if top.uid == binRelUID:          # if supertypeUID == binary relation (5935)
##            self.relRolesTable.append(initialRelRow) # load the first line of the relRolesTable
        subs = supertype.subtypes
        if len(subs) > 0:
            for sub in subs:
                if sub not in all_subtypes:
                    all_subtypes.append(sub)      # Add subtype to total list of subtypes
                #print ('Supertype:',supertype.uid,"Subtypes:",subs,subtypeRow)
            for subX in subs:
                sub_subs = subX.subtypes
                for sub in sub_subs:
                    if sub not in all_subtypes:
                        all_subtypes.append(sub)
                        subs.append(sub)   
        return all_subtypes
#----------------------------------------------------------------
    def Query_Network(self, search_string, string_commonality):
        '''Search for string as (part of) name in a names_in_contexts dictionary.
           The string_commonality specifies to what extent the string
           should correspond with the name.
           A list of candidates is returned.
        '''
        cand_dict = self.dictionary.filter_on_key(search_string, string_commonality)
        candidates = list(cand_dict)
        return candidates
#----------------------------------------------------------------
if __name__ == "__main__":
    from DatabaseAPI import Database
    
    # Connect to an existing database
    db_name  = 'FormalEnglishDB'
    #db_name  = 'RoadDB'
    #db_name  = ':memory:'
    Gel_db = Database(db_name)
    print("Database  : %s connected." % (Gel_db.name))
    
    # Create and initialize a semantic network
    net_name = 'Language definition network'
    network = Semantic_Network(net_name)
    
    # Choose GUI language and formal language
    formal_language = "English"
    Gellish = Language(formal_language)
    GUI_language    = "English"
    GUI = GUI_Language(GUI_language)

    # Create a naming dictionary
    dict_name = 'Gellish Multilingual Taxonomic Dictionary'
    Gel_dict  = GellishDict()
    Gel_dict.name = dict_name
    print('Dictionary:', Gel_dict.name)

    # Add the content of the 'base_ontology' database table to the Semantic Network and to the dictionary
    table = 'base_ontology'
    network.Add_table_content_to_network(Gel_db.dbCursor, table)

    # Build hierarchies in baso_ontology
    network.BuildHierarchies()
    print('network   : %s; nr of objects = %i; nr of rels = %i; nr of rel_types = %i' % \
          (network.name, len(network.objects), len(network.rels), len(network.rel_types)))

    # Add the content of the 'domain_ontologies' database table to the Semantic Network and to the dictionary
    table = 'domain_dictionaries'
    network.Add_table_content_to_network(Gel_db.dbCursor, table)
    print('network   : %s; nr of objects = %i; nr of rels = %i; nr of rel_types = %i' % \
          (network.name, len(network.objects), len(network.rels), len(network.rel_types)))

    # Query things in network
    qtext = input("\nEnter query string: ")
    while qtext != "quit" and qtext != "exit":
        com = input("\nEnter string commonality (cs pi, cs i): ") #(ci pi, cs pi, ci i, cs i, ci fi, cs fi)
        if com == 'cs i':
            string_commonality = 'case sensitive identical'
        else:
            string_commonality = 'case sensitive partially identical'
    
        candidates = network.Query_Network(qtext, string_commonality)
        if len(candidates) > 0:
            for candidate in candidates:
                obj_uid = candidate[1][0]
                #print("candidate %s %s" % (obj_uid, candidate[0][2]))
                obj = network.find_object(obj_uid)
                s = obj.show(network)
        else:
            print("No candidates found")
        qtext = input("\nEnter query string: ")
