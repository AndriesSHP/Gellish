#!/usr/bin/python3
import sys
import os
import csv
#import sqlite3
#import pickle
from tkinter import *
from tkinter.ttk import *

from Expr_Table_Def import *
#from Anything import Anything, Object, Individual, Kind, Relation, RelationType
from Bootstrapping import *
from GellishDict import GellishDict
from Create_output_file import Create_gellish_expression, Convert_numeric_to_integer, \
     Open_output_file

class Query:
    def __init__(self, gel_net, user_interface):
        #self.main = main
        self.gel_net = gel_net
        self.user_interface = user_interface
        #self.views = user_interface.views
        self.unknown_quid = user_interface.unknown_quid
        self.query_spec = []
        self.query_expr = []
        # Candidate objects that are excluded from search results,
        # because they do not satisfy a condition
        self.ex_candids = []

        self.obj_list = []
        
        self.objects_in_focus = []
        self.UIDsInFocus = []
        self.namesInFocus = []
        self.kindUIDsInFocus = []
        self.kindNamesInFocus = []
        self.hierarchical_net = []
        self.hierarchical_net_uids = []
        #self.condition_table = []
        
        # Options are ...
        # options = [optionNr, whetherKnown, lang_uid, comm_uid, name, uid, is_called_uid, \
        #           objectTypeKnown, 'unknown kind'/'onbekende soort']

        self.candid_expressions = []
        self.candidates = []
        self.candid_uid_dict = {}
        
        self.lhCondVal = []
        self.relCondVal = []
        self.rhCondVal = []
        self.uomCondVal = []
        self.lhSel = []
        self.relSel = []
        self.rhSel = []
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
            
            # Interpret the search string,
            # being either a single term (string) or an expression (a<rel>b).
            known_strings, interpreted = self.Interpret_query_line(search_string)
            print('Interpreted query: ', interpreted)
            self.query_spec.append(interpreted)
            if len(interpreted) > 5:
                # An expression was given with 6 or more fields
                # (lh, rel, rh and possibly uom)
                search_string = input("\nEnter a condition specification "
                                      "or search (s) cq display (d): ")
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
        
        # Split search_string in lh, rel and rh strings
        # to enable search for its component
        strings = []
        known_strings = []
        # Split between lh and the rest if present
        expr = search_string.split('<', maxsplit=1)
        # lh_term is expr[0]
        strings.append(expr[0].strip())             # append lh term
        if len(expr) > 1:
            # There is a rest,
            # thus split it between kind of relation and rh + uom if present
            rel_rh_uom = expr[1].split('>', maxsplit=1)
            # Append rel phrase
            strings.append(rel_rh_uom[0].strip())
            # Split third part in rh term and uom term
            rh_uom = rel_rh_uom[1].split('=', maxsplit=1)
            # Append rh term
            strings.append(rh_uom[0].strip())
            if len(rh_uom) > 1:
                # Append uom term
                strings.append(rh_uom[1].strip())
            print('Query =', strings)

        # Search for lh_string, and if present for rel_string and rh_string
        interpreted = []
        for string in strings:
            known_string = True
            print('Search for {}'.format(string))
            candidates = self.gel_net.Query_network_dict(string, com)
            
            if len(candidates) > 0:
                # If candidates found, then show candidates for selection
                for candidate in candidates:
                    obj_uid  = candidate[1][0]
                    obj_name = candidate[0][2]
                    print("  Candidate {} {}s".format(obj_uid, obj_name))
                    
                sel_uid = input("\nEnter UID of selected candidate, "
                                "last = 'Enter' or quit (q): ")
                # Split sel_uid to enable multiple selection (a,b,c...) === to be done ===
                int_val, integer = Convert_numeric_to_integer(sel_uid)
                while sel_uid != 'q':
                    # If a blank ("") is entered, then select the last candidate
                    if sel_uid == "":
                        sel_uid = obj_uid
                    # If selected uid < 100 then the object is an unknown
                    elif integer == True and int_val < 100:
                    #elif int(sel_uid) < 100:
                        self.unknown_quid += + 1
                        obj_uid = self.unknown_quid
                        obj_name = string
                        known_string = False
                    # If there is only one candidate, then select the last candidate
                    elif len(candidates) == 1:
                        sel_uid = obj_uid
                        
                    # Search for selected uid in network
                    try:
                        obj = self.gel_net.uid_dict[sel_uid]
                        s = obj.show(self.gel_net)
                        obj_uid  = obj.uid
                        obj_name = obj.name
                        sel_uid = 'q'
                    except KeyError:
                        print("Selected UID '{}' is not known in the network.".\
                              format(sel_uid))
                        if integer is False or int_val >= 100:
                        #if int(sel_uid) >= 100:
                            sel_uid = input("\nEnter a UID of a selected candidate, "
                                            "'Enter' or quit (q): ")  
            else:
                # No candidates found: the serach_string denotes an (next) unknown
                self.unknown_quid += 1
                obj_uid = self.unknown_quid
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
        # Interpreted is a list
        # [lh_uid,lh_name,rel_uid,rel_name,rh_uid,rh_name,uom_uid,uom_name]
        return known_strings, interpreted  # list of Booleans, list

    def Formulate_query_spec_from_individual(self, selected_kind):
        ''' Determine from a selected individual (to be modified object)
            a query_spec that searches for
            subtypes of its kind (selected_kind)
            that satisfy the aspects of the individual object.
            Thus using the aspects of the individual as criteria for selection of options.
        '''
        shall_have_as_aspect_phrase = ['shall have as aspect a', \
                                       'moet als aspect hebben een']
        shall_be_phrase          = ['shall be', 'moet als kwalitatief aspect hebben']
        shall_be_made_of_phrase  = ['shall be made of', 'moet gemaakt zijn van']
        # query_spec expression = lh_uid, lh_name, rel_type_uid, rel_type_name, \
        #                         rh_uid, rh_name, \
        #                         uom_uid, uom_name, phrase_type_uid
        self.query_spec[:] = []
        query_expr = []
        print('\nFormulate query spec for ',selected_kind.name)

        # Determine an aspect of the individual modified object
        # and the classifier of that aspect
        for obj_rel in self.user_interface.views.modified_object.relations:
            # Search for relation type <has as aspect> (1727) or its subtypes
            # to find an individual aspect
            if obj_rel.rel_type.uid in self.gel_net.subPossAspUIDs:
                if obj_rel.phrase_type_uid == basePhraseUID:
                    aspect = obj_rel.rh_obj
                    if len(aspect.classifiers) > 0:
                        classifier = aspect.classifiers[0]
                    else:
                        print('Aspect {} is not classified. '
                              'Not usable for formulating a condition'.format(aspect.name))
                        continue
                    # Formulate expression:
                    # selected_kind 'has by definition as aspect a' aspect_kind, uom
                    query_expr = [selected_kind.uid, selected_kind.name, \
                                  '4956', \
                                  shall_have_as_aspect_phrase[self.gel_net.GUI_lang_index], \
                                  classifier.uid, classifier.name, '' , '', basePhraseUID]
                    self.query_spec.append(query_expr)
                    
                    self.rolePlayersQTypes = 'thingsOfKinds'
                    self.q_lh_category = 'kind'
                    self.q_rh_category = 'kind of aspect'
                    
##                    print('Query line-1a: {} ({}) <{}> ({}) {} ({})'.\
##                          format(query_expr[1], query_expr[0], query_expr[3], \
##                                 query_expr[2], query_expr[5], query_expr[4]))

                    # Formulate_condition(s) for kind from_individual aspect value
                    for asp_rel in aspect.relations:
                        # Search for qualification or quantification of the aspect
                        if asp_rel.rel_type.uid in self.gel_net.subQuantUIDs:
                            
                            # Quantification relation found:
                            # Expression becomes:
                            # classifier <shall have on scale a value ...> value (on scale:) uom
                            # Transform rel_type of individual to rel_type for requirement
                            if asp_rel.rel_type.uid == '5025':
                                # If rel-type is <has on scale a value equal to> (5025)
                                #    then rel_type becomes:
                                #    <shall have on scale a value equal to> (5492)
                                conceptual_rel_type = self.gel_net.uid_dict['5492']

                            elif asp_rel.rel_type.uid == '5026':
                                # If rel-type is <has on scale a value greater than> (5026)
                                #    then rel_type becomes:
                                #    <shall have on scale a value greater than> (5493)
                                conceptual_rel_type = self.gel_net.uid_dict['5493']
                                
                            elif asp_rel.rel_type.uid == '5027':
                                # If rel-type is <has on scale a value less than> (5027)
                                #    then rel_type becomes:
                                #    <shall have on scale a value less than> (5494)
                                conceptual_rel_type = self.gel_net.uid_dict['5494']

                            elif asp_rel.rel_type.uid == '5489':
                                # If rel_type is:
                                # <has on scale a value greater than or equal to> (5489)
                                #    then rel_type becomes:
                                #    <shall have on scale a value greater than or equal to> (5632)
                                conceptual_rel_type = self.gel_net.uid_dict['5632']

                            elif asp_rel.rel_type.uid == '5490':
                                # If rel-type is:
                                # <has on scale a value less than or equal to> (5490)
                                #    then rel_type becomes:
                                #    <shall have on scale a value less than or equal to> (5633)
                                conceptual_rel_type = self.gel_net.uid_dict['5633']

                            else:
                                continue
                            # Conversion from qualification to conceptual qualification found:
                            # thus formulate condition in query_spec
                            # Determine base phrase of relation type in GUI language
                            #print('Condition rel_type', conceptual_rel_type.name, \
                            #      len(conceptual_rel_type.base_phrases_in_contexts))
                            if len(conceptual_rel_type.base_phrases_in_contexts) > 0:
                                rel_type_name = conceptual_rel_type.base_phrases_in_contexts[0][2]
                                for phrase_in_context in \
                                    conceptual_rel_type.base_phrases_in_contexts:
                                    if phrase_in_context[0] == self.user_interface.GUI_lang_uid:
                                        rel_type_name = phrase_in_context[2]
                                        continue
                                #print('Rel_type_name', rel_type_name, \
                                #      self.user_interface.GUI_lang_uid, \
                                #      conceptual_rel_type.base_phrases_in_contexts)
                                # Formulate condition expression:
                                #   kind_of)aspect 'shall have on scale a value ...' value, uom
                                print('Condition: {} <{}> {} {}'.\
                                      format(classifier.name, rel_type_name, \
                                             asp_rel.rh_obj.name, asp_rel.uom.name))
                                condition = [classifier.uid, classifier.name, \
                                             conceptual_rel_type.uid, rel_type_name, \
                                             asp_rel.rh_obj.uid, asp_rel.rh_obj.name, \
                                             asp_rel.uom.uid, asp_rel.uom.name, basePhraseUID]
                                self.query_spec.append(condition)
                                #self.condition_table.append(condition)
                                
                            else:
                                print('No conversion base phrase available for {} ({})'.\
                                      format(conceptual_rel_type.name, conceptual_rel_type.uid))
                elif obj_rel.rel_type.uid == '4853':
                    # Object is classified/qualified by a qualitative aspect (<is>)
                    # results in requirement: <shall be> (5791)
                    qual_aspect = obj_rel.rh_obj
                    # Formulate expression:
                    # selected_kind 'is by definition qualified as' qualitative aspect, uom
                    query_expr = [selected_kind.uid, selected_kind.name, \
                                  '5791', shall_be_phrase[self.gel_net.GUI_lang_index], \
                                  qual_aspect.uid, qual_aspect.name, '' , '', basePhraseUID]
##                    print('Query line-1b: {} ({}) <{}> ({}) {} ({})'.\
##                          format(query_expr[1], query_expr[0], query_expr[3], \
##                                 query_expr[2], query_expr[5], query_expr[4]))
                    self.query_spec.append(query_expr)
                    
                    self.rolePlayersQTypes = 'thingsOfKinds'
                    self.q_lh_category = 'kind'
                    self.q_rh_category = 'kind of aspect'

                elif obj_rel.rel_type.uid == '5423':
                    # Expression found: Object <is made of> construction material
                    # results in requirement: <shall be made of> (4995)
                    qual_aspect = obj_rel.rh_obj
                    # Formulate expression:
                    # selected_kind 'is by definition qualified as' qualitative aspect, uom
                    query_expr = [selected_kind.uid, selected_kind.name, \
                                  '4995', \
                                  shall_be_made_of_phrase[self.gel_net.GUI_lang_index], \
                                  qual_aspect.uid, qual_aspect.name, '' , '', basePhraseUID]
                    print('Query line-1c: {} ({}) <{}> ({}) {} ({})'.\
                          format(query_expr[1], query_expr[0], query_expr[3], \
                                 query_expr[2], query_expr[5], query_expr[4]))
                    self.query_spec.append(query_expr)
                    
                    self.rolePlayersQTypes = 'thingsOfKinds'
                    self.q_lh_category = 'kind'
                    self.q_rh_category = 'kind of aspect'

        if len(self.query_spec) == 0:
            query_expr = [selected_kind.uid, selected_kind.name]
            self.query_spec.append(query_expr)

    def Interpret_query_spec(self):
        ''' Interpret a query_spec, consisting of one or more lines
            and if a single object is requested, then build product model and view
            or when possibly multiple objects are resulting, then execute the query
            and build the various product models and views.
        '''
        self.obj_list[:] = []
        #print('Query_spec:', self.query_spec)
        # If the query interpretation found a single known object
        # (no query expression and not an unknown),
        # thus the first spec line has <= 2 fields and the uid >= 100,
        # then find the object by uid
        # and show/display its data and its subtypes when applicable.
        int_uid, integer = Convert_numeric_to_integer(self.query_spec[0][0])
        if len(self.query_spec[0]) <= 2 \
           and (integer is False or int_uid >= 100):
            # Single known object (uid) found. Find obj with uid in dictionary
            uid = self.query_spec[0][0]
            obj = self.gel_net.uid_dict[uid]
            
            # If obj is a kind of role,
            # then build model of kind of role player (if known) instead of kind of role
            if obj.category == 'kind of role':
                player_found = False
                for rel_obj in obj.relations:
                    expr = rel_obj.expression
                    # Determine whether the relation
                    # defines a kind of role player (5343 = is by def a role of a)
                    if expr[lh_uid_col] == obj.uid \
                       and expr[rel_type_uid_col] == by_def_role_of_ind:
                        role_player_uid = expr[rh_uid_col]
                        role_player = self.gel_net.uid_dict[role_player_uid]
                        player_found = True
                        print('Role {} replaced by role player {}'.\
                              format(obj.name, role_player.name))
                        continue
                if player_found is False:
                     role_player = obj
                # Append role_player to list of objects to be displayed
                self.obj_list.append(role_player)    
            else:
                # Append object to list of objects to be displayed
                self.obj_list.append(obj)
                
            # Build single product model (list with one element)
            self.user_interface.views.Build_product_views(self.obj_list)

        else:
            # Query is an expression
            self.Execute_query()

    def Create_query_file(self):
        ''' Create a file in Gellish Expression format
            on the basis of self.query_spec
        '''
        #print('Query_spec example:', self.query_spec)
        # Query_spec example:
        # [['251691', 'three core cable', '4956', 'shall have as aspect a',
        #   '550206', 'outside diameter', '', '', '6066'],
        #  ['550206', 'outside diameter', '5492', 'shall have as scale value',
        #   '2000000030', '30',    '570423', 'mm', '6066']]
        self.gel_expressions = []
        idea_uid = 100
        lang_uid  = '910037'
        lang_name = 'Nederlands'
        comm_uid  = ''
        comm_name = ''
        lang_comm = [lang_uid, lang_name, comm_uid, comm_name]
        intent_uid_name = ['790665','vraag']
    
        for row in self.query_spec:
            idea_uid += +1
            if len(row) == 9:
                # E.g. lh_uid_name = '251691', 'three core cable'
                lh_uid_name         = [row[0], row[1]]
                # E.g. rel_uid_phrase_type = '4956', 'shall have as aspect a'
                rel_uid_phrase_type = [row[2], row[3], row[8]]
                rh_role_uid_name    = ['', '']
                # E.g. rh_uid_name = '550206', 'outside diameter'
                rh_uid_name         = [row[4], row[5]]
                uom_uid_name        = [row[6], row[7]]
                description         = ''
                gellish_expr = Create_gellish_expression(
                    lang_comm, str(idea_uid), intent_uid_name,\
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
        """ Execute a query on the network to find the searched objects
            that satisfy the required relation type (if specified) and its subtypes.
            Store resulting candidate objects in a list (self.candidates)
            with expressions in self.candid_expressions with the same table definition.
            Then initiate the determination of views/models for the found object(s).
            - Options list definition:
              [OptionNr, whetherKnown, lang_uid, comm_uid, resultString, unknown_quid]
        """
        self.query_expr = self.query_spec[0]
        self.q_lh_uid = self.query_expr[0]
        self.q_lh_name = self.query_expr[1]
        self.q_rel_uid = self.query_expr[2]
        self.q_rel_name = self.query_expr[3]
        self.q_rh_uid = self.query_expr[4]
        self.q_rh_name = self.query_expr[5]
        self.phrase_type_uid = self.query_expr[8]
                    
        # query item: [self.q_lh_uid, self.q_lh_name, self.q_rel_uid, self.q_rel_name,
        #              self.q_rh_uid, self.q_rh_name, self.q_uom_uid, self.uom_name,
        #              self.q_phrase_type_uid]
        q_lh_uid_index = 0
        q_lh_name_index = 1
        q_rel_uid_index = 2
        q_rel_name_index = 3 # Not used
        q_rh_uid_index = 4
        q_rh_name_index = 5
        #self.q_phrase_type_index = 8 # Not used
        # Binary relation between an individual thing and something (indiv or kind) = 6068
        #indOrMixRelUID= 6068
        
        self.user_interface.views.subtype_level = 0
        self.user_interface.views.all_subtypes[:] = []

        list_of_categories = ['kind', 'kind of aspect', 'kind of occurrence']
        
    # Consistency check on query
        # If relation type specifies
        # a relation between individual physical objects and the lh_object is known
        # then lh_object may not be a kind or kind of occurrence; idem for rh_object
        int_q_lh_uid, lh_integer = Convert_numeric_to_integer(self.q_lh_uid)
        int_q_rh_uid, rh_integer = Convert_numeric_to_integer(self.q_rh_uid)
        if self.rolePlayersQTypes == 'individuals' \
           and (((lh_integer is False or int_q_lh_uid >= 100) \
                 and self.q_lh_category in list_of_categories) \
                or ((rh_integer is False or int_q_rh_uid >= 100) \
                    and self.q_rh_category in list_of_categories)):
            print('Warning: Relation type <{}> relates individual things, '
                  'but one or both related things are kinds of things. Try again.'.\
                  format(self.q_rel_name, self.q_lh_uid, self.q_lh_category,\
                         self.q_rh_uid  , self.q_rh_category))
            #return

        # If relation type specifies a relation between kinds and the lh_object is known
        # then lh_object shall be a kind or kind of occurrence; idem for rh_object   
        elif (self.rolePlayersQTypes == 'hierOfKinds' \
              or self.rolePlayersQTypes == 'thingsOfKinds') \
              and (((lh_integer is False or int_q_lh_uid >= 100) \
                    and self.q_lh_category not in list_of_categories) \
                   or ((rh_integer is False or int_q_rh_uid >= 100) \
                       and self.q_rh_category not in list_of_categories)):
            print('Warning: Relation type <{}> relates kinds of things, '
                  'but left {} ({}) or right {} ({}) related things are not kinds. '
                  'Try again.'.\
                  format(self.q_rel_name, self.q_lh_uid, self.q_lh_category,\
                         self.q_rh_uid  , self.q_rh_category))
            #return
            
        elif self.rolePlayersQTypes == 'individualAndKind':
            if ((lh_integer is False or int_q_lh_uid >= 100) \
                and self.q_lh_category in list_of_categories):
                print('Warning: Relation type <{}> relates an individual thing to a kind, '
                      'but the left hand object {} ({}) is a kind. Try again.'.\
                      format(self.q_rel_name, self.q_lh_uid, self.q_lh_category))
                
        elif self.rolePlayersQTypes == 'kindAndIndividual':
            if ((rh_integer is False or int_q_rh_uid >= 100) \
                and self.q_rh_category in list_of_categories):
                print('Warning: Relation type <{}> relates a kind to an individual thing, '
                      'but the right hand object {} ({}) is a kind. Try again.'.\
                      format(self.q_rel_name, self.q_rh_uid, self.q_rh_category))
                
        elif self.rolePlayersQTypes == 'individualAndMixed':
            if ((lh_integer is False or int_q_lh_uid >= 100) \
                and self.q_lh_category in list_of_categories):
                print('Warning: Relation type <{}> relates an individual thing '
                      'to an individual or kind, but the left hand object {} ({}) '
                      'is a kind. Try again.'.\
                      format(self.q_rel_name, self.q_lh_uid, self.q_lh_category))

        # Determine UIDs of subtypes of relation type
        # to enable searching also the subtypes of the relation type
        self.q_rel_subtype_uids[:] = []
        
        self.q_rel_subtype_uids.append(self.query_expr[q_rel_uid_index])
        
        # If relUID of query (self.query_expr) known
        # then determine rel_type object and its list of subtypes
        int_q_rel_uid, rel_integer = \
                       Convert_numeric_to_integer(self.query_expr[q_rel_uid_index])
        if rel_integer is False or int_q_rel_uid >= 100:
            rel_type = self.gel_net.uid_dict[self.query_expr[q_rel_uid_index]]
            # Find subtypes of specified relation type
            self.q_rel_subtypes, self.q_rel_subtype_uids = \
                                 self.gel_net.Determine_subtypes(rel_type)  
            #print('Subtypes of relation',self.query_expr[q_rel_uid_index],':',subRels)
            self.q_rel_subtype_uids.append(self.query_expr[q_rel_uid_index])
        #print('Relation type and subtypes:',self.q_rel_subtype_uids)
                
        # Candidate answers ========
        cand_text = ['Candidate answers:','Kandidaat antwoorden:']
        print('\n{}'.format(cand_text[self.gel_net.GUI_lang_index]))

        # Initialize whether types are known
        self.q_lh_category = 'unknown'
        self.q_rh_category = 'unknown'
        # If lh object is a known, then ...
        
        if lh_integer is False or int_q_lh_uid >= 100:
            # If lh is possibly a kind then determine its subtypes
            if self.rolePlayersQTypes in ['kindAndIndividual', \
                                          'mixedAndIndividual', \
                                          'hierOfKinds',\
                                          'thingsOfKinds']:
                self.q_lh_category = 'kind'
                self.q_lh_subtypes, self.q_lh_subtype_uids = \
                                    self.gel_net.Determine_subtype_list(self.q_lh_uid)
                
                # If relation type is a transitive relation type then
                # determine hierarchical network (chain) of rh_uids
                # that relate to the q_lh_uid of the query
                if self.q_rel_uid in self.gel_net.transitiveRelUIDs:
                    self.Transitive_hier_network(\
                        self.q_lh_subtypes, self.q_rel_subtype_uids, self.q_phrase_type_uid)
                    self.rh_hierarchical_net_uids = self.net_uids
            else:
                self.q_lh_category = 'individual'
                self.q_lh_subtypes[0] = self.q_lh_obj

        # If rh object is a known and is possibly a kind then determine its subtypes
        if rh_integer is False or int_q_rh_uid >= 100:
            if self.rolePlayersQTypes in ['individualAndKind', \
                                          'individualAndMixed', \
                                          'hierOfKinds',\
                                          'thingsOfKinds']:
                self.q_rh_category = 'kind'
                self.q_rh_subtypes, self.q_rh_subtype_uids = \
                                    self.gel_net.Determine_subtype_list(self.q_rh_uid)
                
                # If relation type is a transitive relation type then
                # determine hierarchical network (chain) of lh_uids
                # that relate to the q_rh_uid of the query
                if self.q_rel_uid in self.gel_net.transitiveRelUIDs:
                    self.Transitive_hier_network(\
                        self.q_rh_subtypes, self.q_rel_subtype_uids, self.q_phrase_type_uid)
                    self.lh_hierarchical_net_uids = net_uids
            else:
                self.q_rh_category = 'individual'
                self.q_rh_subtypes[0] = self.q_rh_obj

        # Build list of candidates and candid_uid_dict
        # Collect expressions that match first self.query_expr expression
        # in candid_expressions table.
        
        self.about  = ['about' ,'over']
        indeed = ['Indeed','Inderdaad']
        
        # If q_lh_object of query is unknown, (q_lh_uid < 100) ('what-1')
        if lh_integer is False or int_q_lh_uid < 100:
            # rh_object of query is known (q_rh_uid > 99) while q_lh object is unknown
            if rh_integer is False or int_q_rh_uid >= 100: 
                # If relation_type object of query is known (q_rel_uid > 99) is known, then
                if int_q_rel_uid >= 100:                  
                    # If self.q_rh_category == 'individual'
                    # then search for matches for the individual
                    # If self.q_rh_category == 'kind'
                    # then search for matches for the kind and its subtypes
                    # Search in the relations of rhq_object 
                    # for expressions with the specified relation type(s)
                    # or one of its subtypes
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
                    print('=== to be done === by which kinds of relations '
                          'are lh object {} and rh object {} related?'.\
                          format(self.query_expr[q_lh_name_index], \
                                 self.query_expr[q_rh_name_index]))
            
            # If rh_object of query is also unknown (q_rh_uid < 100) ('what-2')
            # then error meassage
            else:
                # rh_object of query in also unknown (self.query_expr[q_rh_uid_index] < 100)
                # Both q_lh and q_rh object are unknown
                if self.gel_net.GUI_lang_index == 1:
                    print('  Ofwel de linker term of de rechter term moet bekend zijn. '
                          'Probeer opnieuw')
                else:
                    print('  Either left hand term or right hand term should be known. '
                          'Try again')
                return
                    
        # lhUID is in vocabulary (thus lh is known) because self.query_expr[q_lh_uid_index] >= 100.
        else:
            # For the self.q_lh object and its subtypes find expressions
            # that match the first query expression 
            for q_lh_sub in self.q_lh_subtypes:
                # Search in the relations of lh_object for a relation type
                # that corresponds with q_rel or its subtypes
                for lh_obj_rel in q_lh_sub.relations:
                    expr = lh_obj_rel.expression
                    if expr[rel_type_uid_col] in self.q_rel_subtype_uids:
                        # If rh object is also known (q_rh_uid >= 100)
                        # then verify whether expression complies with query 
                        if int_q_rh_uid >= 100:
                            # If also the rh or its subtype correpond with the q_rh
                            # (the expression complies with the self.query_expr),
                            #  then display message: confirm that the expression complies.
                            # === This does not hold for the inverse.
                            #     Transitive!!! roles should comply (=== to be added ===)
                            if expr[rh_uid_col] in self.q_rh_subtype_uids:
                                print('  {}: {} <{}> {} {}'.\
                                      format(indeed[self.gel_net.GUI_lang_index],\
                                             expr[intent_name_col],\
                                             expr[lh_name_col], expr[rel_type_name_col], \
                                             expr[rh_name_col]))
                                # Create candidate object
                                # and add object to list of candidates and expressions,
                                # if not yet present
                                self.Record_and_verify_candidate_object(expr)
                    
                            # If rh not in subtype list,
                            # but self.q_rel_uid is a transitive relation type
                            # then verify whether the transitive relation is satisfied.
                            elif self.q_rel_uid in self.gel_net.transitiveRelUIDs:
                                if expr[rh_uid_col] in self.rh_hierarchical_net_uids:
                                    # Indeed, rh_object is by transitive chain related to lh_object
                                    print('\n  {}: {} {} {} {}'.\
                                          format(indeed[self.gel_net.GUI_lang_index],\
                                                 expr[intent_name_col],\
                                                 expr[lh_uid_col], expr[rel_type_name_col],\
                                                 expr[rh_name_col]))
                                    # Create candidate object
                                    # and add object to list of candidates, if not yet present
                                    # Add expression to the list of candidate expressions,
                                    # if not yet present
                                    self.Record_and_verify_candidate_object(expr)
                                
    ##                # If self.q_lh_uid and self.q_rh_uid are both known,
    ##                #                then: is the question confirmed?
    ##                if self.query_expr[q_lh_uid_index] > 99 \
    ##                                and self.query_expr[q_rh_uid_index] > 99:
    ##                    if self.q_lh_uid == expr[lh_uid_col]:
    ##                        matchChain = TransitiveMatchChain(\
    ##                                     self.query_expr[q_lh_uid_index], \
    ##                                     self.query_expr[q_rh_uid_index],self.q_phrase_type_uid)
    ##                    elif self.q_lh_uid == expr[rh_uid_col]:
    ##                        matchChain = TransitiveMatchChain(\
    ##                                     self.query_expr[q_rh_uid_index],\
    ##                                     self.query_expr[q_lh_uid_index],self.q_phrase_type_uid)
    ##                    if matchChain[0]:
    ##                        because    = ['because...','omdat...']
    ##                        print('  {}: {} {} {} {} {}'.\
    ##                              format(indeed[self.gel_net.GUI_lang_index],
    ##                                     expr[intent_name_col],\
    ##                                     self.query_expr[q_lh_name_index], self.q_rel_name,\
    ##                                     self.query_expr[q_rh_name_index],\
    ##                                     because[self.gel_net.GUI_lang_index]))
    ##                        for step in reversed(matchChain[1:]):
    ##                            print('    {} <{}> {}'.format(step[1],self.q_rel_name,step[3]))
    ##                    else:
    ##                        denial  = ['No, it is not true that','Nee, het niet waar dat']
    ##                        print('  {}: {} {} {}'.\
    ##                              format(denial[self.gel_net.GUI_lang_index],\
    ##                                     self.query_expr[q_lh_name_index],\
    ##                                     self.q_rel_name,self.query_expr[q_rh_name_index]))
    ##                        return
    ##            else:                   # self.q_lh_uid not on expr
    ##                #if self.rolePlayersQTypes == 'kindAndIndividual' \
    ##                #   or self.rolePlayersQTypes == 'mixedAndIndividual' \
    ##                #   or self.rolePlayersQTypes == 'hierOfKinds' \
    ##                #   or self.rolePlayersQTypes == 'thingsOfKinds':
    ##                if self.rolePlayerQTypeLH == 'kind':
    ##                    if expr[lh_uid_col] in self.q_lh_subtype_uids \
    ##                        or expr[rh_uid_col] in self.q_lh_subtype_uids:
    ##                        self.Record_and_verify_candidate_object(expr)

        # Unknown relation type: Any relation type is O.K.
        # self.q_rel_uid not in vocabulary ('what')
        if rel_integer is False or int_q_rel_uid < 100:
            # Is self.q_lh_uid or self.query_expr in vocabulary?
            if lh_integer is False or int_q_lh_uid >= 100:
                # Search for facts about self.q_lh_uid
                for lh_obj_rel in self.q_lh_obj.relations:
                    expr = lh_obj_rel.expression   
                    if self.rolePlayersQTypes \
                       in ['mixed', 'individualAndKind', 'kindAndIndividual']:
                        self.Record_and_verify_candidate_object(expr)
            else:
                # Is self.q_lh_uid or self.query_expr not in vocabulary ('what')
                if rh_integer is False or int_q_rh_uid >= 100:
                    if self.q_rh_uid == row[rh_uid_col]:
                        for rel_rh_obj in self.q_rh_obj.relations:
                            expr = rel_rh_obj.expression 
                            if self.rolePlayersQTypes \
                               in ['mixed', 'individualAndKind', 'kindAndIndividual']:
                                self.Record_and_verify_candidate_object(expr)

        if len(self.candidates) == 0:
        #if len(self.candid_expressions) == 0:
            noExpressions = ['No candidates found','Geen kandidaten gevonden']
            print('{}'.format(noExpressions[self.gel_net.GUI_lang_index]))
            return
        else: 
            # Candidates found
            satisText  = ['Confirmed','Bevestigd']
            #satisText2 = ['satisfies the query and conditions',\
            #              'voldoet aan de vraag en de voorwaarden']

            # If there are candidate expressions then show complying candidate expression
            if len(self.candid_expressions) > 0:
                for candid_expr in self.candid_expressions:
                    self.answer_expressions.append(candid_expr)
                    # Report confirmed candidate lh_name, rel_type_name, rh_name
                    print('\n    {} {}: <{}> <{}> <{}>'.\
                          format(satisText[self.gel_net.GUI_lang_index],\
                                 len(self.answer_expressions), candid_expr[lh_name_col],\
                                 candid_expr[rel_type_name_col], candid_expr[rh_name_col]))
##            if len(self.query_spec) > 1:
##                # Verify conditions on candidates
##                #    (self.candidates / self.candid_expressions)
##                # and storeresults in self.answer_expressions
##                for candid in self.candidates:
##                    self.Verify_conditions(candid, candid_expr)
            
        print('Start generating views of {} candidate objects. Role player types: {}.'\
              .format(len(self.candid_expressions), self.rolePlayersQTypes))

        # Determine the objects_in_focus.
        # If lh and rh role players of query expression might be individual things
        # and not a kind or occurrence, then
        # if lh_object is known then the lh_object is the object_in_focus.
        if self.rolePlayersQTypes \
           in ['individuals', 'individualAndMixed', 'mixedAndIndividual']:
            # if lhUID and lhName is known in namingTable, then determine object in focus
            if self.lhSel[1] == 'known':
                if self.q_lh_category != 'kind' and self.q_lh_category != 'occurrence':
                    # The left hand object in self.query_expr is the object in focus
                    object_in_focus = self.gel_net.uid_dict[self.q_lh_uid]
                    self.objects_in_focus.append(object_in_focus)
##                    self.UIDsInFocus.append(self.q_lh_uid)
##                    self.namesInFocus.append(self.q_lh_name)
            elif self.rhSel[1] == 'known':
                # if lhUID is not known, and rhUID (and rhName) is known in namingTable, then:
                if self.q_rh_category != 'kind' and self.q_rh_category != 'occurrence':
                    # The right hand object in self.query_expr is the object in focus
                    object_in_focus = self.gel_net.uid_dict[self.q_rh_uid]
                    self.objects_in_focus.append(object_in_focus)
##                    self.UIDsInFocus.append(self.q_rh_uid)
##                    self.namesInFocus.append(self.q_rh_name)
            else:
                if self.gel_net.GUI_lang_index == 1:
                    print('  Zowel linker object <{}> '
                          'als ook rechter object <{}> is onbekend. Probeer opnieuw.'. \
                          format(self.q_lh_name,self.q_rh_name))
                else:
                    print('  Left hand object <{}> '
                          'as well as right hand object <{}> is unknown. Try again.'. \
                          format(self.q_lh_name, self.q_rh_name))
                return
            #print('UIDs in Focus:', self.rolePlayersQTypes, object_in_focus.name,\
            #      self.q_lh_category, self.q_rh_category)
            self.categoryInFocus = 'individual'
            self.gel_net.Build_single_product_view(object_in_focus)

        # Else if lh and rh role players of query expression are an individual and a kind
        elif self.rolePlayersQTypes \
             in ['mixed', 'individualAndKind', 'kindAndIndividual']:
            obj_list = []
            for expr in self.answer_expressions:
                object_in_focus = self.gel_net.uid_dict[expr[lh_uid_col]]
                obj_list.append(object_in_focus)
            self.categoryInFocus = 'individual'

            # Start building product models about found self.candid_expressions
            self.user_interface.views.Build_product_views(obj_list)

        # Build models/views for kinds
        elif self.rolePlayersQTypes in ['hierOfKinds', 'thingsOfKinds']:
            if self.lhSel[1] == 'known':
                # The left hand object in the self.query_expr is the object in focus
                object_in_focus = self.gel_net.uid_dict[self.q_lh_uid]
                self.objects_in_focus.append(object_in_focus)
            elif self.rhSel[1] == 'known':
                # The right hand object in the self.query_expr is the object in focus
                object_in_focus = self.gel_net.uid_dict[self.q_rh_uid]
                self.objects_in_focus.append(object_in_focus)
            else:
                print('Left hand kind <{}> as well as '
                      'right hand kind <{}> unknown; Try again.'.\
                      format(self.q_lh_name,self.q_rh_name))
                return
            self.categoryInFocus = 'kind'
            obj_list = []
            obj_list.append(object_in_focus)
            self.user_interface.views.Build_product_views(obj_list)
        else:
            self.Other_views()

    def Record_and_verify_candidate_object(self, expr):
        ''' Identify candidate object and add object to list of candidates,
            if not yet present
            then verify additional conditions, if present
        '''
        candid_uid = expr[lh_uid_col]
        if candid_uid not in self.candid_uid_dict:
            candid = self.gel_net.uid_dict[candid_uid]
            self.candidates.append(candid)
            self.candid_uid_dict[candid_uid] = candid
        else:
            candid = self.candid_uid_dict[candid_uid]
            
        if expr not in self.candid_expressions:
            self.candid_expressions.append(expr)
            print('  {} {} {} [{}]: <{}> <{}> <{}>. '.\
                  format(expr[intent_name_col], len(self.candid_expressions),\
                         self.about[self.gel_net.GUI_lang_index], self.q_lh_name,\
                         expr[lh_name_col], expr[rel_type_name_col], expr[rh_name_col]))

            # If additional conditions are specified then verify conditions
            if len(self.query_spec) > 1:
                self.Verify_conditions(candid, expr)

    def Find_candidates(self, rhq):
        ''' Search for relations with object rhq
            that comply with the kind of relation in the query
            and collect the relations in self.candid_expressions
        '''
        for obj_rel in rhq.relations:
            expr = obj_rel.expression
            # If relation of q_rh_obj is equal to self.q_rel_uid or one of its subtypes
            if expr[rel_type_uid_col] in self.q_rel_subtype_uids:
                self.candid_expressions.append(expr)
                print('\n  {} {} {} [{}]: <{}> <{}> <{}>.'.\
                      format(expr[intent_name_col], len(self.candid_expressions), \
                             self.about[self.gel_net.GUI_lang_index],\
                             self.q_rh_name, expr[lh_name_col], \
                             expr[rel_type_name_col], expr[rh_name_col]))
    
##                        #if row[rh_uid_col] in self.q_rh_subtype_uids
##                        #    or row[lh_uid_col] in self.q_rh_subtype_uids: 
##                            if self.rolePlayersQTypes == 'mixed' \
##                               or self.rolePlayersQTypes == 'individualAndKind' \
##                               or self.rolePlayersQTypes == 'kindAndIndividual' \
##                               or row[rel_type_uid_col] == classifUID\
##                               or self.rolePlayersQTypes == 'hierOfKinds' \
##                               or self.rolePlayersQTypes == 'thingsOfKinds': 
##                                self.candid_expressions.append(row)
##                                # To be moved to condition verification:
##                                #self.UIDsInFocus.append (row[lh_uid_col])
##                                #self.namesInFocus.append(row[lh_name_col])
##
##                            print('\n  {} {} {} [{}]: <{}> <{}> <{}>.'.\
##                                  format(row[intent_name_col], len(self.candid_expressions),
##                                         self.about[self.gel_net.GUI_lang_index],\
##                                         self.q_rh_name, row[lh_name_col], \
##                                         row[rel_type_name_col], row[rh_name_col]))
        
            # If self.q_rel_uid is a transitive relation type 
            if self.q_rel_uid in self.gel_net.transitiveRelUIDs:
                if expr[rh_uid_col] in self.hierarchical_net_uids: 
                    #print ('candidate:', self.q_rel_name,row[rh_uid_col],row[rh_name_col])
                    self.candid_expressions.append(expr)
                    print('\n  {} {} {} [{}]: <{}> <{}> <{}>.'.\
                          format(expr[intent_name_col], len(self.candid_expressions), \
                                 self.about[self.gel_net.GUI_lang_index],\
                                 self.q_rh_name, expr[lh_name_col], \
                                 expr[rel_type_name_col], expr[rh_name_col]))
                
##                        # q_rh_uid of Query is not equal l/rhUIDEx;
##                          maybe a classification by a subtype
##                        else:
##              # if not a relation between individual things
##                            if not self.rolePlayersQTypes == 'individuals':      
##                  # 'what' is related by a <is related to (a)> or its subtypes.
##                                if self.q_rel_uid in self.gel_net.indOrMixRelUIDs:              
##                                    #print('row[rh_uid_col]:',row[rh_uid_col])
##                                    if self.rolePlayerQTypeRH == 'kind':
##                          # If rhUID is a subtype of known kind (= self.q_rh_uid of self.query_expr)
##                                        if row[rh_uid_col] in self.q_rh_subtype_uids:
##                              # 'what' <is classified as a> 'subtype of known kind'
##                                            # individual related to kind
##                                            #self.rolePlayersQTypes == 'mixed':
##                                            self.candid_expressions.append(row)
##                                            # To be moved to condition verification:
##                                            #self.UIDsInFocus.append (row[lh_uid_col])
##                                            #self.namesInFocus.append(row[lh_name_col])
##
##                                            print('\n  {} {} {} [{}]: <{}> <{}> <{}>.'.\
##                                                  format(row[intent_name_col],
##                                                         len(self.candid_expressions), \
##                                                         self.about[self.gel_net.GUI_lang_index],\
##                                                         self.q_rh_name, row[lh_name_col], \
##                                                         row[rel_type_name_col], row[rh_name_col]))

    def Transitive_hier_network(self, base_objects, rel_subtype_uids, phrase_type_uid):
        """ Search recursively for a chain (hierarchical network) of objects and uids
            that relate to base_uid
            and that are related by a relation of type q_rel_uid (or its subtypes)
            to a possible target_uid,
            in the required search direction (indicated by the phrase_type_uid).
            First a tree of branches may be found.
            When the target objects is found in a branch, then the inverse route
            is followed to find the chain.
            The resulta are a list of objects
            and a list of uids that are the chain of objects from base to target
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
                    if expr[lh_uid_col] == obj.uid \
                       and expr[phrase_type_uid_col] == phrase_type_uid:
                        related_uid = expr[rh_uid_col]
                        if related_uid not in self.net_uids:
                            self.net_uids.append(related_uid)
                            new_direct_related_uids.append(related_uid)
                        branch = [expr[lh_uid_col], expr[lh_name_col], \
                                  expr[rh_uid_col], expr[rh_name_col]]
                        self.branches.append(branch)
                        
                    # Search for relations in inverse expressions        
                    elif expr[rh_uid_col] == obj.uid \
                         and expr[phrase_type_uid_col] != phrase_type_uid:
                        related_uid = expr[lh_uid_col]
                        if related_uid not in self.net_uids:
                            self.net_uids.append(related_uid)
                            new_direct_related_uids.append(related_uid)
                        branch = [expr[rh_uid_col], expr[rh_name_col],\
                                  expr[lh_uid_col], expr[lh_name_col]]
                        self.branches.append(branch)
                            
        if new_direct_related_uids > 0:
            self.Transitive_match(new_direct_related_uids, rel_subtype_uids, phrase_type_uid)

    def Other_views(self):
        print('Otherviews')
        
    def Formulate_conditions_from_gui(self):
        """ Determine conditions in GUI if any
        """
        self.answer_expressions = []
        condition = []
        #self.condition_table[:] = []
        condText = ['Condition','Voorwaarde']
        cond_satified = True

        if self.user_interface.extended_query is False:
            return
        
        # Get conditions and find condition UIDs
        for condNr in range(0,3):
            lh_cond_name  = self.lhCondVal[condNr].get()
            # Empty lh condition name marks the end of the conditions
            if lh_cond_name == '':
                continue
            string_commonality = 'csi' # case sensitive identical
            # Find uid, name and description of lh_cond_name
            unknown_lh, lh_uid_name_desc = \
                        self.gel_net.Find_object_by_name(lh_cond_name, string_commonality)
            if unknown_lh is False:
                lh_cond_uid = lh_uid_name_desc[0]
            else:
                lh_cond_uid = 0
                print('Error: object {} not found'.format(lh_cond_name))
                      
            rel_cond_name = self.relCondVal[condNr].get()
            unknown_rel, rel_uid_name_desc = \
                         self.gel_net.Find_object_by_name(rel_cond_name, string_commonality)
            #print('Condition name, known, uid-name-descr', \
            #      rel_cond_name, unknown_rel, rel_uid_name_desc)
            if unknown_rel is False:
                rel_cond_uid = rel_uid_name_desc[0]
            else:
                rel_cond_uid = 0
                print('Error: object {} not found'.format(rel_cond_name))

            rh_cond_name  = self.rhCondVal[condNr].get()
            unknown_rh, rh_uid_name_desc = \
                        self.gel_net.Find_object_by_name(rh_cond_name, string_commonality)
            if unknown_rh is False:
                rh_cond_uid = rh_uid_name_desc[0]
            else:
                rh_cond_uid = 0
                print('Error: object {} not found'.format(rh_cond_name))

            uom_cond_name = self.uomCondVal[condNr].get()
            if uom_cond_name != '':
                unknown_uom, uom_uid_name_desc = \
                             self.gel_net.Find_object_by_name(uom_cond_name, string_commonality)
                if unknown_uom is False:
                    uom_cond_uid = uom_uid_name_desc[0]
                else:
                    uom_cond_uid = 0
                    print('Error: object {} not found'.format(uom_cond_name))
            else:
                uom_cond_uid = 0
            condition   = [lh_cond_uid, lh_cond_name, rel_cond_uid, rel_cond_name,\
                           rh_cond_uid, rh_cond_name, uom_cond_uid, uom_cond_name]
            print('\n{} {} {} ({}) {} ({}) {} ({}) {} ({})'.\
                  format(condText[self.gel_net.GUI_lang_index], condNr+1, \
                         lh_cond_name,lh_cond_uid,\
                         rel_cond_name, rel_cond_uid, rh_cond_name, rh_cond_uid, \
                         uom_cond_name, uom_cond_uid))
            #self.condition_table.append(condition[:])
            self.query_spec.append(condition[:])
        
    def Verify_conditions(self, candid_obj, candidate_expr):
        ''' Conditions found thus
            verify whether the candidate object identified by self.candid_expressions
            satisfies the entered conditions, if any,
            and store the results in the self.answer_expressions
            with the same column definitions as the expressions.
        '''
        candid_expr = candidate_expr
        # Conditions found thus check candidate expressions on conditions
        answerHead = ['Answer','Antwoord']
        answerText = ['Candidate','Kandidaat']
        conditText = ['Candidate aspect','Kandidaadaspect']
        nothing_satisfies = ['There are no expressions found that satisfy the condition(s).',\
                      'Er zijn geen uitdrukkingen gevonden die aan de voorwaarde(n) voldoen.']
        
        print('\n{}:'.format(answerHead[self.gel_net.GUI_lang_index]))
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
        for condit in self.query_spec[1:]:
            condNr += + 1
            #print('\nVerify condition on', candid_obj.uid, candid_obj.name, condit)
            condit_rel_subs, condit_rel_sub_uids = self.gel_net.Determine_subtype_list(condit[2])
            #print('Condit_rel_subs', condit_rel_sub_uids)

            cond_obj = self.gel_net.uid_dict[condit[0]]
            condit_lh_subs, condit_lh_sub_uids = self.gel_net.Determine_subtype_list(condit[0])
            if candid_obj.uid in condit_lh_sub_uids:
                # A new condition for the same object is identified.
                # Determine whether there is a relation that satisfies the condition
                satisfied_cond = False
                for obj_rel in candid_obj.relations:
                    candid_expr = obj_rel.expression
                    if candid_expr[rel_type_uid_col] in condit_rel_sub_uids:
                        #print('candid_expr[rel_type_uid_col]', candid_expr[rel_type_uid_col], \
                        #      candid_expr[rh_uid_col])
                        if candid_expr[rh_uid_col] == condit[4]:
                            # Condition is satisfied by expression
                            print('Candidate {} <{}> {} <with role player> {} and uom {}'.\
                                  format(candid_expr[lh_name_col], \
                                         candid_expr[rel_type_name_col], \
                                         candid_expr[rh_role_name_col], \
                                         candid_expr[rh_name_col], \
                                         candid_expr[uom_name_col]))
                            satisfied_cond = True
                            break
                if satisfied_cond is False:
                    print('No expression found that satisfies condition nr {}.'.\
                          format(condNr))
            else:
                # A condition on another object is detected.
                # Possibly a qualification of the rh_role
                cond_satified = False
                candid_rh_role_uid = candid_expr[rh_role_uid_col]
                if candid_rh_role_uid == '':
                    print('** Candidate expression {} <{}> {} '
                          'does not have an intrinsic aspect defined'.\
                          format(candid_expr[lh_name_col], \
                                 candid_expr[rel_type_name_col], \
                                 candid_expr[rh_name_col]))
            
##                if condNr > 1:
##                    rhCandIndex = -1
##                    for rh_cand_uid in rhCandidUIDs:
##                        rhCandIndex = rhCandIndex + 1
##                        if condit[0] == rh_cand_uid:
##                            candid_rh_role_uid = rhCandidRoleUIDs[rhCandIndex]
##                            break
                else:
                    # rh_role_uid is not ''
                    # Does rh_role object have a (e.g. qualification) relation
                    # that satisfies condition
                    role_obj = self.gel_net.uid_dict[candid_rh_role_uid]
                    for role_obj_rel in role_obj.relations:
                        expr = role_obj_rel.expression
                        #print('Lh_name and cond_name <{}> <{}> '
                        #      'and lh_rel and cond_rel <{}> <{}>.'.\
                        #      format(expr[lh_name_col], candid_expr[rh_role_name_col], \
                        #             expr[rel_type_name_col], condit[3]))

                        # Verify whether the relation type of expression about the lh_uid object
                        # is 5737 <has by definition on scale a value equal to>
                        if expr[lh_uid_col] == candid_rh_role_uid \
                           and expr[rel_type_uid_col] == '5737':
                            # rh object should be a number; check that
                            #print('Verify equality of RH_value and condition value <{}>, <{}> '
                            #      'and of both uoms {} {}?'.\
                            #      format(expr[rh_name_col], condit[5], \
                            #             expr[uom_name_col], condit[7]))
                            us_notation = expr[rh_name_col].replace(',','.')
                            value = us_notation.replace(' ','')
                            test_string = value.replace('.','')
                            if not test_string.isdecimal():
                                print('Value {} is not a number'.\
                                      format(expr[rh_name_col]))
                            # Verify whether unit of measure differs from UoM of condition
                            if expr[uom_uid_col] != condit[6]:
                                print('Unit of measure {} differs from condition unit {}.'.\
                                      format(expr[uom_name_col], condit[7]))
                                
                            # Verify required (in)equality
                            # depending on required kind of relation
                            int_condit_2, integer = Convert_numeric_to_integer(condit[2])
                            
                            # 5492 = shall have on scale a value equal to;
                            # 5737 = has by definition on scale a value equal to;
                            # 5025 = has on scale a value equal to
                            if condit[2] in ['5492', '5737', '5025']:
                                if float(value) == float(condit[5]):
                                    print('Condition satisfied that {} = {}'.\
                                          format(float(expr[rh_name_col]), float(condit[5])))
                                    cond_satified = True

                            # 5493 = shall have on scale a value greater than;
                            # 6049 = has by definition on scale a value greater than;
                            # 5026 = has on scale a value greater than
                            if condit[2] in ['5493', '6049', '5026']:
                                if float(value) > float(condit[5]):
                                    print('Condition satisfied that {} > {}'.\
                                          format(float(expr[rh_name_col]), float(condit[5])))
                                    cond_satified = True
                                    
                            # 5632 = shall have on scale a value greater than or equal to;
                            # 5978 = has by definition a value greater than or equal to;
                            # 5489 = has on scale a value greater than of equal to
                            elif condit[2] in ['5632', '5978', '5489']:
                                if float(expr[rh_name_col]) >= float(condit[5]):
                                    print('Condition satisfied that {} >= {}'.\
                                          format(float(expr[rh_name_col]), float(condit[5])))
                                    cond_satified = True

                            # 5494 = shall have on scale a value less than;
                            # 6052 = has by definition on scale a value less than;
                            # 5027 = has on scale a value less than 
                            elif condit[2] in ['5494', '6052', '5027']:
                                if float(expr[rh_name_col]) < float(condit[5]):
                                    print('Condition satisfied that {} < {}'.\
                                          format(float(expr[rh_name_col]), float(condit[5])))
                                    cond_satified = True
                                    
                            # 5633 = shall have on scale a value less than or equal to;
                            # 5979 = has by definition a value less than or equal to;
                            # 5490 = has on scale a value less than or equal to
                            elif condit[2] in ['5633', '5979', '5490']:
                                if float(expr[rh_name_col]) <= float(condit[5]):
                                    print('Condition satisfied that {} <= {}'.\
                                          format(float(expr[rh_name_col]), float(condit[5])))
                                    cond_satified = True
                            
                            # Verify for lh_uid whether an expression
                            #        with the correct relation type (or its subtype)
                            #        has an identical rh_uid
                            # condit[2] <= 99 means rh_cond_uid is an unknown.
                            elif expr[rh_uid_col] == condit[2] or int_condit_2 < 100:
                                cond_satified = True
        ##                    if expr[lh_uid_col] == candid_rh_role_uid \
        ##                       and expr[rel_type_uid_col] in condit_rel_sub_uids \
        ##                       and (expr[rh_uid_col] == condit[4] or condit[4] < 100) \
        ##                       or expr[rh_uid_col] == candid_rh_role_uid \
        ##                        and expr[rel_type_uid_col] in condit_rel_sub_uids \
        ##                        and (expr[lh_uid_col] == condit[4] or condit[4] < 100):
                                
                            if cond_satified == True:
                                candidAspectExpr.append(expr)
                                rhCandidRoleUIDs.append(expr[rh_role_uid_col])
                                rhCandidUIDs.append(expr[rh_uid_col])
                                print('    {} {}: <{}> <{}> <{}> <{}>'.format\
                                      (conditText[self.gel_net.GUI_lang_index], condNr, \
                                       expr[lh_name_col],\
                                       expr[rel_type_name_col], expr[rh_name_col], \
                                       expr[uom_name_col]))
                                int_condit_4, integer = Convert_numeric_to_integer(condit[4])
                                if int_condit_4 >= 100:
                                    break

            if cond_satified is False:
                # If rel_cond_uid is a transitive relation type
                # then: is the condition satisfied?
                if condit[2] in self.gel_net.transitiveRelUIDs:
                    #if expr[lh_uid_col] == ? :
                    matchChain = TransitiveMatchChain(expr[lh_uid_col], \
                                                      condit_rel_subs, condit[4])
                    #elif expr[rh_uid_col] == ? :
                    #    matchChain = TransitiveMatchChain(expr[rh_uid_col], \
                    #                                      condit[2], condit[4])
                    if matchChain[0]:
                        indeed  = ['Indeed','Inderdaad']
                        because = ['because...','omdat...']
                        print('    {}: {} {} {} {}'.\
                              format(indeed[self.gel_net.GUI_lang_index], \
                                     expr[lh_name_col], condit[3],\
                                     condit[5], because[self.gel_net.GUI_lang_index]))
                        for step in reversed(matchChain[1:]):
                            print('      {} <{}> {}'.format(step[1],condit[3],step[3]))
                        cond_satified = True
                        continue
                    else:
                        # Condition is not satisfied (even being transitive)
                        break
                else:
                    # Condition is not satisfied (cond_satified is False)
                    # and relation type is not transitive.
                    break
            
        # if last condition is also true, then:
        if cond_satified:
            self.answer_expressions.append(expr)
            satisText   = ['Confirmed','Bevestigd']
            becauseText = ['    because:','     omdat:']
            andText     = ['        and:','        en:']
            print('    {} {}: <{}> <{}> <{}> {}'.\
                  format(satisText[self.gel_net.GUI_lang_index], \
                         len(self.answer_expressions), \
                         condit[1], condit[3], condit[5], condit[7]))
            first = True
            for candidAspect in candidAspectExpr:
                if first == True:
                    print('    {} <{}> <{}> <{}> <{}>'.\
                          format(becauseText[self.gel_net.GUI_lang_index], \
                                 candidAspect[lh_name_col],\
                                 candidAspect[rel_type_name_col], \
                                 candidAspect[rh_name_col],\
                                 candidAspect[uom_name_col]))
                    first = False
                else:
                    print('    {} <{}> <{}> <{}> <{}>'.\
                          format(andText[self.gel_net.GUI_lang_index], \
                                 candidAspect[lh_name_col],\
                                 candidAspect[rel_type_name_col], \
                                 candidAspect[rh_name_col],\
                                 candidAspect[uom_name_col]))
        else:
            denial  = ['No, the condition is not satisfied that',\
                       'Nee, er is niet voldaan aan de voorwaarde dat']
            print('    {}: {} {} {}'.\
                  format(denial[self.gel_net.GUI_lang_index], \
                         expr[lh_name_col], condit[3], condit[5]))
            if candid_obj not in self.ex_candids:
                self.ex_candids.append(candid_obj)
        if len(self.answer_expressions) == 0:
            print('  {}'.format(nothing_satisfies[self.gel_net.GUI_lang_index]))

    def Verify_model(self):
        """ Build the model of an individual thing
            that is specified in a classification relation (of a query)
            and verify that model against the requirements about the kind.
        """

        shallUID = '5735'
        subtypesOfShall, subShallUIDs = self.gel_net.Determine_subtype_list(shallUID)
        for obj in self.objects_in_focus:
            print('Verify model of {} on requirements about {}'.\
                  format(nameInF, self.kindName))
            for obj_rel in obj.relations:
                expr = obj_rel.expression
                if expr[rel_type_uid_col] in subtypesOfShall:
                    lh  = expr[lh_name_col]
                    rel = expr[rel_type_name_col]
                    rh  = expr[rh_name_col]
                    #print('Requirement for {}: {} <{}> {}'.
                    #      format(nameInF,lh,rel,rh))
# Transform and search for satisfaction in expressions table
# To be written

#-------------------------------------------------------------
if __name__ == "__main__":
    from DatabaseAPI import Database
    
    # Create and initialize a semantic network
    net_name = 'Language definition network'
    network = Semantic_Network(net_name)
    
    # Choose GUI language and formal language
    formal_language = "English"

    # Create a naming dictionary
    dict_name = 'Gellish Multilingual Taxonomic Dictionary'
    Gel_dict  = GellishDict(dict_name)
    print('Created dictionary:', Gel_dict.name)

    # Query things in network
    qtext = input("\nEnter query string: ")
    while qtext != "quit" and qtext != "exit":
        # String commonalities: #(cipi, cspi, cii, csi, cifi, csfi)
        com = input("\nEnter string commonality (cspi, csi): ")
        # string_commonality 'csi' = 'case sensitive identical',
        #                   'cspi' = 'case sensitive partially identical'
    
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
