import os

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, filedialog
from operator import itemgetter

from Bootstrapping import ini_out_path, basePhraseUID, inversePhraseUID
from Expr_Table_Def import *
from Query import Query
from Create_output_file import Create_gellish_expression, Convert_numeric_to_integer, \
     Open_output_file
from Occurrences_diagrams import Occurrences_diagram
from utils import open_file


class Display_views():
    ''' Various models about object(s)
        are created resulting from a query on a semantic network
        and the are presented in various treeviews in a notebook.
    '''
    def __init__(self, gel_net, user_interface):
        self.gel_net = gel_net
        self.user_interface = user_interface
        self.root = user_interface.root
        self.GUI_lang_index = user_interface.GUI_lang_index
        self.uid_dict = gel_net.uid_dict

        self.network_model = []
        self.rels_in_network_model = []
        self.kind_model = []
        self.prod_model = []
        self.expr_table = []
        self.summ_model = []
        self.summ_objects = []
        self.taxon_model = []
        self.possibilities_model = []
        self.indiv_model = []
        self.indiv_objects = []
        self.info_model = []
        self.all_subtypes = []
        self.occ_model = []
        self.involv_table = []
        self.seq_table = []
        self.part_whole_occs = []

        self.taxon_row = ['','','','','','','','','','','','','','']
        self.summary_row = ['','','','','','','','','','','','','','']
        self.possibility_row = ['','','','','','','','','','','','','','','']
        self.indiv_row = ['','','','','','','','','','','','','','','']
        self.occ_row = ['','','','','','','','','','','','','','']
        self.taxon_aspect_uids = ['','','','']
        self.taxon_column_names = ['','','','']
        self.taxon_uom_names = ['','','','']
        self.summ_aspect_uids = ['','','','']
        self.summ_column_names = ['','','','']
        self.summ_uom_names = ['','','','']
        self.possib_aspect_uids = ['','','','','']
        self.possib_column_names = ['','','','','','']
        self.possib_uom_names = ['','','','','']
        self.indiv_aspect_uids = ['','','','','']
        self.indiv_column_names = ['','','','','']
        self.indiv_uom_names = ['','','','','']

        self.subs_head = ['Subtypes', 'Subtypen']
        self.comp_head = ['Part hierarchy', 'Compositie']
        self.occ_head = ['Occurrences', 'Gebeurtenissen']
        #self.role_head = ['Role', 'Rol']
        #self.involv_head = ['Involved', 'Betrokkene']
        self.kind_head = ['Kind', 'Soort']
        self.aspect_head = ['Aspect', 'Aspect']
        self.part_occ_head = ['Part occurrence', 'Deelgebeurtenis']
        self.info_head = ['Document', 'Document']
        self.name_head = ['Name', 'Naam']
        self.parent_head = ['Upper concept', 'Hoger concept']
        self.comm_head = ['Community', 'Taalgemeenschap']
        self.unknown = ['unknown', 'onbekend']
        self.unknown_kind = ['unknown kind' ,'onbekende soort']

        self.occ_aspects = ['','','','','','','','','','','']
        self.occ_kinds = ['','','','','','','','','','','']
        self.occ_uoms = ['','','','','','','','','','','']

        self.num_idea_uid = 211000000
        self.classification = ['is classified as a', 'is geclassificeerd als een']
        self.nr_of_occurrencies = 0
        self.max_nr_of_rows = 500   # in treeviews

        self.modification = None

        # Define a notebook in window
        self.Define_notebook()

    def empty_models(self):
        ''' Make models empty enabling the creation of new models'''
        self.network_model[:] = []
        self.rels_in_network_model[:] = []
        self.kind_model[:] = []
        self.prod_model[:] = []
        self.expr_table[:] = []
        self.taxon_model[:] = []
        #self.taxon_objects[:] = []
        self.summ_model[:] = []
        self.summ_objects[:] = []
        self.possibilities_model[:] = []
        #self.possib_objects[:] = []
        self.indiv_model[:] = []
        self.indiv_objects[:] = []
        self.info_model[:] = []
        self.all_subtypes[:] = []
        self.occ_model[:] = []
        self.involv_table[:] = []
        self.seq_table[:] = []
        self.part_whole_occs[:] = []

        self.summ_aspect_uids[:] = ['','','','']
        self.summ_column_names[:] = ['','','','']
        self.summ_uom_names[:] = ['','','','']
        self.taxon_aspect_uids[:] = ['','','','']
        self.taxon_column_names[:] = ['','','','']
        self.taxon_uom_names[:] = ['','','','']
        self.indiv_aspect_uids[:] = ['','','','','']
        self.indiv_column_names[:] = ['','','','','']
        self.indiv_uom_names[:] = ['','','','','']

    def Build_product_views(self, obj_list):
        ''' Create product model views for one or more objects in obj_list.'''

        self.empty_models()

        for obj in obj_list:
            lang_name, comm_name, preferred_name, descr = \
                       self.user_interface.Determine_name_in_context(obj)
            obj.name = preferred_name
            self.object_in_focus  = obj

            # Initialize subtype list of object in focus
            # Excluding duplicates due to multiple inheritance
            self.all_subtypes[:] = []
            # If object is excluded because it did not satisfy a condition then skip it
            if obj in self.user_interface.query.ex_candids:
                self.Display_message(
                    'Excluded candidate-1: {}'.format(obj.name),\
                    'Uitgesloten kandidaat-1: {}'.format(obj.name))
                continue
            self.subtype_level = 0
            self.Build_single_product_view(obj)

    def Build_single_product_view(self, obj):
        ''' Create various model views for a single object,
            being either an individual thing or a kind.
            This includes a network_model,
            kind_model, prod_model, expr_table (with Gellish expressions),
            taxon_model (taxonomy view), summ_model (multi-product view),
            possibilities_model and indiv_model.
        '''

        # Verify whether object is excluded from list of candidates
        if obj in self.user_interface.query.ex_candids:
            self.Display_message(
                'Excluded candidate: {}'.format(obj.name),\
                'Uitgesloten kandidaat: {}'.format(obj.name))
            return

        self.implied_parts_dict = {}
        self.nr_of_occurrencies = 0
        self.occ_in_focus = 'no'
        nr_of_occ_aspect_kinds  = 3
        self.decomp_level = 0
        role = ''

        self.Create_prod_model_view_header(obj)

        # If object_in_focus is a kind, then collect its supertypes
        if obj.category in ['kind', 'kind of physical object', 'kind of occurrence', \
                            'kind of aspect', 'kind of role', 'kind of relation', 'number']:
            # Search for the first supertype relation
            # that generalizes the obj (= self.object_in_focus)
            if len(obj.supertypes) == 0:
                # No supertypes found for kind: report omission
                kindUID = 0
                kindName = 'Not found'
                descrOfUID = ''
                self.Display_message(
                    'No supertype of {} found.'.format(obj.name),
                    'Geen supertype van {} gevonden.'.format(obj.name))
            else:
                # There is one or more supertype of the kind in focus:
                # collect all generalization relations in the expr_table and the network
                for supertype in obj.supertypes:
                    for rel_obj in obj.relations:
                        expr = rel_obj.expression
                        if expr[rel_type_uid_col] in ['1146', '1726', '5396', '1823']:
                            if len(self.expr_table) < self.max_nr_of_rows:
                                self.expr_table.append(expr)
                                self.Add_line_to_network_model(rel_obj, expr)

        # Individual thing: Object category is not a kind, thus indicates an indiv.
        # Verify whether the individual thing is classified (has one or more classifiers)
        elif len(obj.classifiers) == 0:
            self.Display_message(
                'For object {} neither a supertype nor a classifier is found.'.\
                format(obj.name),\
                'Voor object {} is geen supertype noch een classificeerder gevonden.'.\
                format(obj.name))
        else:
            # The object_in_focus is classified (once or more times)
            # thus it is an individual, such as an individual physical object or occurrence:
            # Search for the first classifying kind and classification relation
            # that classifies the object_in_focus
            classifier = obj.classifiers[0]
            # kindUID is the kind that classifies the object_in_focus
            kind_uid = classifier.uid
            # Determine name etc. of the kind of the object_in_focus
            lang_name, comm_name, kind_name, descrOfKind = \
                       self.user_interface.Determine_name_in_context(classifier)

            # Verify whether the individual is an occurrence.
            if kind_uid in self.gel_net.subOccurrenceUIDs:
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
                       self.user_interface.Determine_name_in_context(obj)
            obj.name = obj_name

            self.taxon_row[0] = obj.uid
            self.taxon_row[1] = obj.name    # preferred name
            #self.taxon_row[2] = supertype_name   # name of the first supertype
            self.taxon_row[3] = comm_name

            if len(obj.supertypes) > 0:
                lang_name, comm_name_supertype, supertype_name, descr_of_super = \
                           self.user_interface.Determine_name_in_context(obj.supertypes[0])
            else:
                supertype_name = self.unknown[self.GUI_lang_index]

##            self.possibility_row[0:5] = obj.uid, obj_name, '', supertype_name, comm_name
##                   # comm_name of obj name (not of supertype name)
            # Add object_in_focus to possibilities_model with comm_name of obj (not of supertype)
            # Second (extended) obj_name enables duplicate branches in display tree
            possib_row = [obj.uid, obj_name, obj_name, '', supertype_name, comm_name]
            if possib_row not in self.possibilities_model:
                self.possibilities_model.append(possib_row)

            # Find kinds of aspects for kind in focus
            nr_of_aspects = self.Find_kinds_of_aspects(obj, role)

            # Find kinds of parts of kind in focus and their conceptual or qualitative aspects
            self.Find_kinds_of_parts_and_their_aspects(obj)

            # Find (qualitative) information about the kind in focus and build info_model
            self.Find_information_about_object(obj)

            # Determine whether the kind is a classifier for individual things
            # and collect individual things that are classified by the kind in focus
            self.Determine_individuals(obj)

            # Determine subtypes of kind_in_focus and build product models of those subtypes
            self.subtype_level += 1
            for sub in obj.subtypes:
                if sub not in self.all_subtypes:
                    self.all_subtypes.append(sub)
                    self.Build_single_product_view(sub)

        # Individual object_in_focus:
        # Find aspects, their classification and their values of the individual object_in_focus
        elif obj.category in ['individual', 'physical object', 'occurrence']:

            community_name = self.gel_net.community_dict[obj.names_in_contexts[0][1]]
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
            self.Display_message(
                "Object category '{}' is not programmed for searching for aspects.".\
                format(obj.category),\
                "Object categorie '{}' is niet geprogrammeerd voor het zoeken naar aspecten.".\
                format(obj.category))

        #self.parts_of_occ_table= []       # parts of occurrence in focus
        if obj.category != 'occurrence':
            # Search for occurrences about the object_in_focus
            # and for other objects that are involved in those occurrences.
            self.decomp_level = 0
            self.Occurs_and_involvs(obj)

    def Add_line_to_network_model(self, rel_obj, expr):
        ''' Add a row to the network_model for display in a network view.
            rel_obj is the relation object which lh or rh object is the object in focus.
            expr is the full expression.
            Branch is an expression that is added to the network_model.
        '''
        # If the left hand object is the object in focus,
        # then find the base phrase or inverse phrase for the relation
        # in the preferred language and language community
        if rel_obj.lh_obj == self.object_in_focus:
            # Determine the preferred name of the related object
            kind_name, kind_uid = self.Determine_preferred_kind_name(rel_obj.rh_obj)
            # Determine the preferred phrase for the kind of relation
            #print('Base phrases:', expr[rel_type_name_col], rel_obj.rel_type.base_phrases)
            if expr[rel_type_name_col] in rel_obj.rel_type.base_phrases:
                lang_name, comm_name, rel_type_phrase, full_def = \
                       self.user_interface.Determine_name_in_context(rel_obj.rel_type, 'base')
            else:
                # Rel_type_name is an inverse phrase
                lang_name, comm_name, rel_type_phrase, full_def = \
                       self.user_interface.Determine_name_in_context(rel_obj.rel_type, 'inverse')
            branch = [rel_obj.rh_obj.uid, rel_obj.lh_obj.uid, expr[lh_name_col], \
                      rel_type_phrase, expr[rh_name_col], kind_uid, \
                      rel_obj.rh_obj.name, rel_obj.lh_obj.name, kind_name]
        else:
            # rh_obj is the object_in_focus
            kind_name, kind_uid = self.Determine_preferred_kind_name(rel_obj.lh_obj)
            if expr[rel_type_name_col] in rel_obj.rel_type.base_phrases:
                lang_name, comm_name, rel_type_phrase, full_def = \
                       self.user_interface.Determine_name_in_context(rel_obj.rel_type, 'inverse')
            else:
                lang_name, comm_name, rel_type_phrase, full_def = \
                       self.user_interface.Determine_name_in_context(rel_obj.rel_type, 'base')
            branch = [rel_obj.lh_obj.uid, rel_obj.rh_obj.uid, expr[rh_name_col], \
                      rel_type_phrase, expr[lh_name_col], kind_uid, \
                      rel_obj.lh_obj.name, rel_obj.rh_obj.name, kind_name]

        #print('Branch-1:', rel_obj.phrase_type_uid, branch)
        # Add the branch to the network_model, if not yet present
        if branch not in self.network_model:
            is_related_to = branch[3] # rel_type_phrase
            # If the branch is about the object in focus, then make parent empty (= root)
            # and insert an intermediate line with the expressed kind of relation
            if branch[1] == self.object_in_focus.uid and \
               is_related_to not in self.rels_in_network_model:
                if len(self.rels_in_network_model) == 0:
                    kind_name, kind_uid = self.Determine_preferred_kind_name(self.object_in_focus)
                    root = [self.object_in_focus.uid, \
                            '', '', '', '', kind_uid, \
                            self.object_in_focus.name, '', kind_name]
                    self.network_model.append(root)

                intermediate = [rel_obj.rel_type.uid, '', '', '', '', '', \
                                is_related_to, branch[7]]
                self.network_model.append(intermediate)
                self.rels_in_network_model.append(is_related_to)
                #print('Branch-2:', rel_obj.phrase_type_uid, intermediate)

            # If the branch is a direct child of the object in focus,
            # then link the child to the intermediate instead of to its parent
            if branch[1] == self.object_in_focus.uid:
                branch[7] = is_related_to
                # If kind of relation is a possession of characteristic or one of its subtypes
                # then determine that value of the characteristic.
                if rel_obj.rel_type.uid in self.gel_net.subPossAspUIDs:
                    # Determine the value of the aspect
                    qualifier = 'quantitative'
                    aspect = self.uid_dict[branch[0]]
                    equality, value_name, uom_name, value_uid, uom_uid = \
                              self.Determine_aspect_value(aspect, qualifier)
                    branch += [equality, value_name, uom_name]
                    print('Branch:', branch)
                self.network_model.append(branch)
            else:
                self.network_model.append(branch)
            #print('Branch-3:', rel_obj.phrase_type_uid, branch)
##        else:
##            print('Duplicate branch: {}, {}, {}'.format(branch[1], branch[5], branch[2]))

    def Create_prod_model_view_header(self, obj):
        ''' Create prod_model view header '''

        # Verify if object is classified or has a supertype
        # === should become the status of the classification cr specialization relation ===
        status_text = ['accepted', 'geaccepteerd']
        if len(obj.classifiers) == 0 and len(obj.supertypes) == 0:
            obj_kind_uid  = ''
            obj_kind_name = self.unknown[self.GUI_lang_index]
            status = status_text[self.GUI_lang_index]
        else:
            obj_kind_uid  = obj.kind.uid
            lang_name, comm_name, obj_kind_name, descr = \
                               self.user_interface.Determine_name_in_context(obj.kind)
            status = 'unknown'
        is_a = ['is a ', 'is een ']
        form_text  = ['Product form for:', 'Product formulier voor:']
        kind_text  = ['Kind:'            , 'Soort:']
        descr_text = ['Description:'     , 'Omschrijving:']
        if len(obj.names_in_contexts) > 0:
            description = is_a[self.GUI_lang_index] + obj_kind_name \
                          + '' + obj.names_in_contexts[0][4]
        else:
            description = is_a[self.GUI_lang_index] + obj_kind_name

        prod_line_0 = [obj.uid  , obj_kind_uid , '', 1 , form_text[self.GUI_lang_index], \
                       obj.name, '', '',\
                       kind_text[self.GUI_lang_index], obj_kind_name, '', '', '', status]
        prod_line_1 = ['','','',2,'', descr_text[self.GUI_lang_index], description,\
                       '','','','','','','']

        prod_head_NL2I= ['','','',3,'','','','','Aspect','Soort aspect',\
                         '>=<','Waarde','Eenheid','Status']
        prod_head_NL2K= ['','','',3,'','','','','Soort aspect',''      ,\
                         '>=<','Waarde','Eenheid','Status']

        prod_head_EN2I= ['','','',3,'','','','','Aspect','Aspect type',\
                         '>=<','Value','UoM','Status']
        prod_head_EN2K= ['','','',3,'','','','','Kind of aspect',''   ,\
                         '>=<','Value','UoM','Status']

        self.line_nr = 3

        #prod_line_3 = [part_uid, part_kind_uid, aspect_uid, self.line_nr, part, \
        #               '','', kindOfPart, aspect.name, kindOfAspect, value,UoM, status]
        #prod_line_4 = [part_of_part.uid, part_kind_uid, aspect_uid, self.line_nr, '', \
        #               partOfPart,'',kindOfPart, aspect.name, kindOfAspect, value,UoM, status]
        #prod_line_5 = [occur_uid, occ_kind_uid, aspect_uid, self.line_nr, occur, \
        #               '','',kindOfOcc, aspect.name, kindOfAspect, value,UoM, status]
        #prod_line_6 = [inv_obj.uid, inv_kind_uid, aspect_uid, self.line_nr, '', \
        #               invObject,role,kindOfInv, aspect.name, kindOfAspect, value,UoM, status]
        #prod_line_7 = [part_uid, part_kind_uid,aspect_uid , self.line_nr, '', \
        #               '','','', aspect.name, kindOfAspect, value,UoM, status]
        #prod_line_8 = [obj.uid, obj_kind_uid, file_uid, self.line_nr, obj, \
        #               document,'',kind_of_document, file, kind_of_file, '','', status]

        if obj.category in ['kind', 'kind of physical object', 'kind of occurrence']:
            self.kind_model.append(prod_line_0)
            if len(obj.supertypes) > 1:
                for super_type in obj.supertypes[1:]:
                    lang_name, comm_name, supert_type_name, descr = \
                               self.user_interface.Determine_name_in_context(super_type)
                    self.kind_model.append([obj.uid,super_type.uid,'',1,\
                                            '','','','','',supert_type_name])
            self.kind_model.append(prod_line_1)
            if self.user_interface.GUI_lang_name == 'Nederlands':
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
                               self.user_interface.Determine_name_in_context(classifier)
                    self.prod_model.append([obj.uid,classifier.uid,'',1,\
                                            '','','','','',classifier_name])
            self.prod_model.append(prod_line_1)
            if self.user_interface.GUI_lang_name == 'Nederlands':
                self.prod_model.append(prod_head_NL2I)
            else:
                self.prod_model.append(prod_head_EN2I)

    def Find_aspects(self, indiv, role):
        """ Search for aspects of an individual thing (indiv)
            and their qualifications or quantifications
            and store results in lines in prod_model
            indiv     = the individual thing
            kind.name = the name of the kind of individual thing
            (for messages only)
            decomp_level = decomposition_level:
              0 = objectInFocus, 1 = part, 2 = part of part, etc.
            categoryInFocus = category of the object in focus,
              being individual or phys object or occurrence
            The prod_model lineType is 3A: aspects of a product
            - conform the header line for aspects (line type 3)
        """

        # Search for aspects and their values
        nr_of_aspects = 0  # nr of found aspects for this indiv object
        aspect_uid = ''
        aspect_name = ''
        equality = ''

        # Determine the kind that classifies the individual object
        # If the individual object is not classified
        # then the classifying kind is called 'unknown'
        if len(indiv.classifiers) == 0:
            indiv.kind_uid  = ''
            indiv.kind_name = self.unknown_kind[self.GUI_lang_index]
        else:
            # Determine the preferred name of the first classifier of the individual object
            lang_name_cl, comm_name_cl, pref_cl_name, descr = \
                          self.user_interface.Determine_name_in_context(indiv.classifiers[0])
            indiv.kind_uid  = indiv.classifiers[0].uid
            indiv.kind_name = pref_cl_name

        for rel_obj in indiv.relations:
            expr = rel_obj.expression
            qualifier = None
            # Add each expression to the expr_table with each idea
            # about the object in focus
            if len(self.expr_table) < self.max_nr_of_rows \
               and expr not in self.expr_table:
                self.expr_table.append(expr)
                #print('Rel_obj', rel_obj.lh_obj.uid, rel_obj.lh_obj.name, \
                #      rel_obj.rel_type.base_phrases[0], rel_obj.rh_obj.name)
                self.Add_line_to_network_model(rel_obj, expr)

            # Find possession of aspect relations (or its subtypes)
            if indiv.uid == expr[lh_uid_col] \
               and expr[rel_type_uid_col] in self.gel_net.subPossAspUIDs:
                if expr[phrase_type_uid_col] == basePhraseUID:
                    aspect_uid = expr[rh_uid_col]
                    qualifier = 'quantitative'
                else:
                    self.Display_message(
                        'The phrase type uid of idea {} is incompatible '
                        'with the expression.'.format(expr.uid),\
                        'De uid van de soort frase van idee {} is niet compatibel '
                        'met de uitdrukking.'.format(expr.uid))
            # And for the inverse
            elif indiv.uid == expr[rh_uid_col] \
                 and expr[rel_type_uid_col] in self.gel_net.subPossAspUIDs:
                if expr[phrase_type_uid_col] == inversePhraseUID:
                    aspect_uid   = expr[lh_uid_col]
                    qualifier = 'quantitative'
                else:
                    self.Display_message(
                        'The phrase type uid of idea {} is incompatible '
                        'with the expression.'.format(expr.uid),\
                        'De uid van de soort frase van idee {} is niet compatibel '
                        'met de uitdrukking.'.format(expr.uid))
            else:
                # It is not a possession of (intrinsic) aspect relation,
                # thus search for possession of a qualitative aspect relations
                # and for an <is made of> relation
                if indiv.uid == expr[lh_uid_col] \
                   and expr[rel_type_uid_col] in ['5843', '5423']:
                    if expr[phrase_type_uid_col] == basePhraseUID:
                        aspect_uid = expr[rh_uid_col]
                        qualifier = 'qualitative'
                elif indiv.uid == expr[rh_uid_col] \
                     and expr[rel_type_uid_col] in ['5843', '5423']:
                    if expr[phrase_type_uid_col] == inversePhraseUID:
                        aspect_uid = expr[lh_uid_col]
                        qualifier = 'qualitative'
                else:
                    continue
##                if expr[rel_type_uid_col] in self.gel_net.sub_classif_uids:
##                    if len(self.expr_table) < self.max_nr_of_rows
##                       and expr not in self.expr_table:
##                        self.expr_table.append(expr)
##                #print('classif:', expr[lh_name_col], expr[rel_type_name_col], expr[rh_name_col])

        # Aspect is found or qualitative aspect is found
##            # Add the found relation expression to the expr_table
##            if len(self.expr_table) < self.max_nr_of_rows and expr not in self.expr_table:
##                self.expr_table.append(expr)
            status = expr[status_col]
            nr_of_aspects += 1

            # Find the aspect object from its uid
            # being the aspect in the <has as aspect> relation
            # or the qualitative aspect in a qualification relation (such as <is made of>)
            aspect = self.uid_dict[aspect_uid]
            aspect_name = aspect.name

            # Determine the value of the aspect
            equality, value_name, uom_name, value_uid, uom_uid = \
                      self.Determine_aspect_value(aspect, qualifier)

            # Verify if aspect has a known value
            if value_uid == '':
                unknownVal = ['unknown value','onbekende waarde']
                value_name = unknownVal[self.GUI_lang_index]
                #warnText  = ['Aspect','Waarschuwing: Aspect']
                #valueMess = ['has no value.','heeft geen waarde.']
                self.Display_message(
                    'Aspect {} ({}) has no value.'.\
                    format(aspect_name, aspect_uid),
                    'Aspect {} ({}) heeft geen waarde.'.\
                    format(aspect_name, aspect_uid))
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

        # Store result in various models (display views)
            # Network_model and expr_table
            # If quantitative sspect value is found
            # then add expression to network_model and expr_table
            if qualifier == 'quantitative' and value_name != 'unknown':
                if len(self.expr_table) < self.max_nr_of_rows \
                   and expr not in self.expr_table:
                    self.expr_table.append(expr)
                    self.Add_line_to_network_model(rel_obj, expr)

            # Summary_table
            # If the object is the object_in_focus and not one of its parts,
            # then collect the aspect in a summary_table
            if self.decomp_level == 0:
                # Build summary_view table header
                # with list of kinds of aspects (summ_column_names)
                if aspect.kind_name not in self.summ_column_names \
                   and len(self.summ_column_names) <= 14:
                    self.summ_aspect_uids.append(aspect.kind_uid)
                    self.summ_column_names.append(aspect.kind_name)
                    self.summ_uom_names.append(uom_name)
                self.summ_ind = 3
                for kind_uid in self.summ_aspect_uids[4:]:
                    self.summ_ind += + 1
                    # Build list of values conform list of aspects.
                    # Note: sumRow[0] = component
                    if aspect.kind_uid == kind_uid:
                        #print('Aspects of phys:', indiv.name, len(self.summ_aspect_uids), \
                        #      aspect_name, aspect.kind_name, self.summ_ind, value_name)
                        self.summary_row[self.summ_ind] = value_name
                        if uom_name != self.summ_uom_names[self.summ_ind]:
                            self.Display_message(
                                'The unit of measure {} ({}) of the value of {} differs '
                                'from summary table header UoM {}.'.\
                                format(uom_name, uom_uid, aspect_name, \
                                       self.summ_uom_names[self.summ_ind]),\
                                'De meeteenheid {} ({}) van de waarde van {} verschilt '
                                'van de overzichtstabel kop_eenheid {}.'.\
                                format(uom_name, uom_uid, aspect_name, \
                                       self.summ_uom_names[self.summ_ind]))

            # Indiv_table
            # If the object is the object_in_focus and not one of its subtypes,
            # then collect the aspect in an indiv_table
            if self.subtype_level == 0:
                # Build individual_view table header with list of aspects
                # (indiv_column_names)
                #print('Aspect kind', aspect.uid, aspect_name)
                if aspect.kind_name not in self.indiv_column_names \
                   and len(self.indiv_column_names) <= 15:
                    self.indiv_aspect_uids.append(aspect.kind_uid)
                    self.indiv_column_names.append(aspect.kind_name)
                    self.indiv_uom_names.append(uom_name)
                self.indiv_ind = 4
                for kind_uid in self.indiv_aspect_uids[5:]:
                    self.indiv_ind += + 1
                    # Build list of values conform list of aspects.
                    # Note: sumRow[0] = component
                    if aspect.kind_uid == kind_uid:
                        #print('Aspects of phys:', indiv.name, len(self.indiv_aspect_uids), \
                        #      aspect_name, aspect.kind_name, self.indiv_ind, value_name)
                        self.indiv_row[self.indiv_ind] = value_name
                        if uom_name != self.indiv_uom_names[self.indiv_ind]:
                            if uom_name == '':
                                self.Display_message(
                                    'The unit of measure of the value of {} is missing.'.\
                                    format(aspect_name),\
                                    'De meeteenheid van de waarde van {} ontbreekt.'.\
                                    format(aspect_name))
                            else:
                                self.Display_message(
                                    'The unit of measure {} ({}) of the value of {} differs '
                                    'from the table header UoM {}.'.\
                                    format(uom_name, uom_uid, aspect_name, \
                                           self.indiv_uom_names[self.indiv_ind]),\
                                    'De meeteenheid {} ({}) van de waarde van {} verschilt '
                                    'van de eenheid {} in de kop van de tabel.'.\
                                    format(uom_name, uom_uid, aspect_name, \
                                           self.indiv_uom_names[self.indiv_ind]))

            # Prod_model
            # Create prod_model text line for output view
            self.line_nr += 1
            #print('Aspect of obj.:', self.decomp_level, nr_of_aspects, indiv.name, aspect_name)
            if self.decomp_level == 0 and nr_of_aspects == 1:
                prod_line_3 = [indiv.uid   , indiv.kind_uid, aspect_uid, \
                               self.line_nr, indiv.name, role,''  ,indiv.kind_name,\
                               aspect_name , aspect.kind_name, equality, \
                               value_name, uom_name, status]
            elif self.decomp_level == 1 and nr_of_aspects == 1:
                prod_line_3 = [indiv.uid   , indiv.kind_uid, aspect_uid, \
                               self.line_nr, indiv.name, role,''  ,indiv.kind_name,\
                               aspect_name , aspect.kind_name, equality, \
                               value_name, uom_name, status]
            elif self.decomp_level == 2 and nr_of_aspects == 1:
                prod_line_3 = [indiv.uid   , indiv.kind_uid, aspect_uid, \
                               self.line_nr, role, indiv.name,''  ,indiv.kind_name,\
                               aspect_name , aspect.kind_name, equality, \
                               value_name, uom_name, status]
            elif self.decomp_level == 3 and nr_of_aspects == 1:
                prod_line_3 = [indiv.uid   , indiv.kind_uid, aspect_uid, \
                               self.line_nr,'' , role, indiv.name, indiv.kind_name,\
                               aspect_name , aspect.kind_name, equality, \
                               value_name, uom_name, status]
            else:
                prod_line_3 = [indiv.uid   , indiv.kind_uid, aspect_uid, \
                               self.line_nr,'','','','',\
                               aspect_name , aspect.kind_name, equality, \
                               value_name, uom_name, status]
            if len(self.prod_model) < self.max_nr_of_rows:
                self.prod_model.append(prod_line_3)

        # If aspect is possessed by object_in_focus (thus not possessed by a part)
        # then add row to summ_model
        #print('Indiv', self.decomp_level, indiv.uid, self.summary_row)
        if self.decomp_level == 0:
            if len(self.summ_model) < self.max_nr_of_rows:
                if indiv not in self.summ_objects:
                    self.summ_objects.append(indiv)
                    # If summary row is about object in focus,
                    # then make parent of object in focus blank
                    # because treeview requires that parent is known or blank
                    if self.summary_row[0] == self.object_in_focus.uid:
                        self.summary_row[2] = ''
                    self.summ_model.append(self.summary_row[:])

            self.summary_row = ['','','','','','','','','','','','','','']

        # For whole and for parts of whole create a row in indiv_model (not for occurences)
        if self.occ_in_focus != 'occurrence' \
           and len(self.indiv_model) < self.max_nr_of_rows:
            if indiv not in self.indiv_objects:
                self.indiv_objects.append(indiv)
                # If indiv row is about object in focus,
                # then make whole of object in focus blank
                # because treeview requires that whole is known or blank
                if self.indiv_row[0] == self.object_in_focus.uid:
                    self.indiv_row[2] = ''
                self.indiv_model.append(self.indiv_row[:])

        self.indiv_row = ['','','','','','','','','','','','','','']
        return nr_of_aspects

    def Determine_aspect_value(self, aspect, qualifier):
        ''' Determine the equality, value and unit of measure of the aspect object.
            And if found, then add expression to expr_table and network_model
        '''
        # Verify if the aspect of the individual object is classified
        # (thus no qualitative aspect found)
        if qualifier is 'quantitative':
            # Normal individual aspect found (not a qualitative aspect such as a substance)
            aspect_name = aspect.name

            # Determine the kind that classifies the individual aspect
            if len(aspect.classifiers) == 0:
                aspect.kind_uid = ''
                aspect.kind_name = self.unknown_kind[self.GUI_lang_index]
            else:
                # Determine the preferred name of the first classifier
                # of the individual aspect
                #print('Lang_prefs for classifier of aspect', self.reply_lang_pref_uids, \
                #      aspect.classifiers[0].names_in_contexts)
                lang_name_as, comm_name_as, pref_kind_name, descr = \
                    self.user_interface.Determine_name_in_context(aspect.classifiers[0])
                aspect.kind_uid = aspect.classifiers[0].uid
                aspect.kind_name = pref_kind_name

            # Determine the value of the aspect
            value_uid = ''
            value_name = 'unknown'
            uom_uid = ''
            uom_name = ''
            equality = '='

            # Find the first qualification or quantification relation for the aspect
            for rel_obj in aspect.relations:
                expr = rel_obj.expression

                # Add expression to expr_table and to network_model
                if len(self.expr_table) < self.max_nr_of_rows \
                   and expr not in self.expr_table:
                    self.expr_table.append(expr)
                    self.Add_line_to_network_model(rel_obj, expr)

                # Search for the first expression that qualifies or quantifies the aspect
                # by searching for the kinds of qualifying relations or their subtypes
                if aspect.uid == expr[lh_uid_col]:
                    if expr[rel_type_uid_col] in self.gel_net.subQualUIDs \
                       or expr[rel_type_uid_col] in self.gel_net.subQuantUIDs:
                        if len(self.expr_table) < self.max_nr_of_rows:
                            value_uid = expr[rh_uid_col]
                            value_name = expr[rh_name_col]
                            uom_uid = expr[uom_uid_col]
                            uom_name = expr[uom_name_col]
                    else:
                        continue
                elif aspect.uid == expr[rh_uid_col]:
                    if expr[rel_type_uid_col] in self.gel_net.subQualUIDs \
                       or expr[rel_type_uid_col] in self.gel_net.subQuantUIDs:
                        if len(self.expr_table) < self.max_nr_of_rows:
                            value_uid = expr[lh_uid_col]
                            value_name = expr[lh_name_col]
                            uom_uid = expr[uom_uid_col]
                            uom_name = expr[uom_name_col]
                    else:
                        continue
                else:
                    continue

                # If the found value_uid is not a whole number
                # or is outside the standard whole number range,
                #    then determine the value name in the preferred language
                #    (and in the preferred language community)
                #print('Value', aspect_uid, value_uid, value_name, expr[0:25])
                numeric_uid, integer = Convert_numeric_to_integer(value_uid)
                if integer is False or numeric_uid not in range(1000000000, 3000000000):
                    value = self.uid_dict[value_uid]
                    lang_name, comm_name, value_name, descr = \
                           self.user_interface.Determine_name_in_context(value)

        elif qualifier is 'qualitative':
            # Qualitative aspect found (e.g. a substance such as PVC)
            equality = '='
            # Determine the first supertype of the qualitative aspect
            if len(aspect.supertypes) > 0:
                super_aspect = aspect.supertypes[0]
            #super_aspect = self.uid_dict['431771']     # subtance or stuff
            lang_name, comm_name, pref_kind_name, descr = \
                       self.user_interface.Determine_name_in_context(super_aspect)
            aspect.kind_name = pref_kind_name
            aspect.kind_uid = super_aspect.uid # '431771'
            value_uid = aspect.uid
            # Determine preferred name of qualitative value
            lang_name, comm_name, value_name, descr = \
                       self.user_interface.Determine_name_in_context(aspect)
            uom_uid = ''
            uom_name = ''

        return equality, value_name, uom_name, value_uid, uom_uid

    def Find_information_about_object(self, obj):
        ''' Search for information and files about the object obj
            (kind or individual)
            (and its supertypes?) and build info_model
        '''
        obj_head          = ['Object'      ,'Object']
        info_head         = ['Document'    ,'Document']
        dir_head          = ['Directory'   ,'Directory']
        kind_of_doc_head  = ['Kind'        ,'Soort']
        file_head         = ['File'        ,'File']
        kind_of_file_head = ['Kinf of file','Soort file']
        status_head       = ['Status'      ,'Status']
        descr_avail_text  = ['Description available', \
                             'Omschrijving beschikbaar']

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
##                self.expr_table.append(expr)
                info = self.uid_dict[info_uid]
                # Create header line_type 8 info, only the first time for prod_model or kind_model
                if info_header:
                    self.line_nr += + 1
                    prod_head_8 = ['','','',self.line_nr, info_head[self.GUI_lang_index], \
                                   dir_head[self.GUI_lang_index],'',\
                                   kind_of_doc_head[self.GUI_lang_index], \
                                   file_head[self.GUI_lang_index],\
                                   kind_of_file_head[self.GUI_lang_index],'','','',\
                                   status_head[self.GUI_lang_index]]
                    #print('obj.cat',obj.category)
                    if obj.category in ['kind', 'kind of physical object', \
                                        'kind of occurrence', 'kind of aspect', \
                                        'kind of role', 'kind of relation']:
                        self.kind_model.append(prod_head_8)
                    else:
                        self.prod_model.append(prod_head_8)
                    info_header = False

                # Determine the name of the supertype of info
                # and verify if info is presented on a carrier.
                # And store full description
                qualified = False
                presented = False
                super_info_uid  = ''
                super_info_name = self.unknown[self.GUI_lang_index]
                info.description = ''
                for rel_info in info.relations:
                    info_expr = rel_info.expression
                    info_status = info_expr[status_col]
                    # Determine the qualifier of the info (its supertype)
                    if info_expr[rel_type_uid_col] in self.gel_net.specialRelUIDs:
                        super_info_uid   = info_expr[rh_uid_col]
                        super_info_name  = info_expr[rh_name_col]
                        info.description = info_expr[full_def_col]
                        qualified = True
                        self.expr_table.append(info_expr)
                        self.Add_line_to_network_model(rel_info, info_expr)

                    # Verify whether info <is presented on> (4996) physical object
                    # (typically an electronic data file)
                    # or info <is presented on at least one of> (5627)
                    # collection of physical objects
                    elif info_expr[rel_type_uid_col] in ['4996', '5627']:
                        if info_expr[lh_uid_col] == info.uid:
                            carrier_uid = info_expr[rh_uid_col]
                        elif info_expr[rh_uid_col] == info.uid:
                            carrier_uid = info_expr[lh_uid_col]
                        else:
                            continue

                        # Info is presented on a carrier
                        presented = True
                        self.expr_table.append(info_expr)
                        self.Add_line_to_network_model(rel_info, info_expr)

                        carrier = self.uid_dict[carrier_uid]
                        if len(carrier.classifiers) > 0:
                            carrier_kind_name = carrier.classifiers[0].name
                        else:
                            carrier_kind_name = self.unknown[self.GUI_lang_index]

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
                                self.expr_table.append(car_expr)
                                self.Add_line_to_network_model(rel_carrier, car_expr)
                                directory_name = directory.name

                        if directory_name == '':
                            self.Display_message(
                                'The name of the directory for file {} is unknown.'.\
                                format(carrier.name),\
                                'De naam van de directory voor file {} is onbekend.'.\
                                format(carrier.name))

                        # Store info about object in info_model
                        #print('Carrier {} is located on directory {}.'.\
                        #      format(carrier.name, directory_name))
                        info_row = [info.uid, obj.uid, carrier.uid, directory_name,\
                                    info.name, super_info_name, directory_name, obj.name, \
                                    carrier.name, carrier_kind_name]
                        self.info_model.append(info_row)

                        # Store info about object in prod_model or kind_model
                        self.line_nr += + 1
                        prod_line_8 = [info.uid, super_info_uid, carrier.uid, self.line_nr, \
                                       info.name, directory_name, '',\
                                       super_info_name, carrier.name, carrier_kind_name,\
                                       '','','',info_status]
                        if obj.category in ['kind', 'kind of physical object', \
                                            'kind of occurrence', 'kind of aspect', \
                                            'kind of role', 'kind of relation']:
                            self.kind_model.append(prod_line_8)
                        else:
                            self.prod_model.append(prod_line_8)

                if qualified is False:
                    self.Display_message(
                        'A qualification relation for information {} is missing.'.\
                        format(info.name),\
                        'Een kwalificatierelatie voor informatie {} ontbreekt.'.\
                        format(info.name))

                if presented is False:
                    # Store info about object in info_model
                    info_row = [info.uid, obj.uid, info.description, '', \
                                info.name, super_info_name, '', obj.name, '',\
                                descr_avail_text[self.GUI_lang_index], '', '']
                    self.info_model.append(info_row)

                    # Store info about object in prod_model or kind_model
                    self.line_nr += + 1
                    prod_line_8 = [info.uid, super_info_uid, obj.uid, self.line_nr, \
                                   info.name, '', '', \
                                   super_info_name, '', '','','','',info_status]
                    if obj.category in ['kind', 'kind of physical object', \
                                        'kind of occurrence', 'kind of aspect', \
                                        'kind of role', 'kind of relation']:
                        self.kind_model.append(prod_line_8)
                    else:
                        self.prod_model.append(prod_line_8)

    def Find_parts_and_their_aspects(self, obj):
        """ Search for parts of individual object obj
            (and their aspects) in expr_table.
            Store results in prod_model or occ_model
        """
        unknownClassifierText = ['unknown kind','onbekende soort']
        compHead = ['Part hierarchy','Compositie']
        partHead = ['Part of part','Deel van deel']
        par3Head = ['Further part','Verder deel']
        kindHead = ['Kind','Soort']

        #self.coll_of_subtype_uids = []
        self.nr_of_parts = 0
        self.decomp_level += + 1
        if self.decomp_level > 3:
            self.decomp_level += - 1
            return
        #print('Indentation_level of parts of:',self.decomp_level,name,obj.uid)

        # Search for <has as part> relation or any of its subtypes
        part_uid = ''
        for rel_obj in obj.relations:
            expr = rel_obj.expression
            if expr[rel_type_uid_col] in self.gel_net.subComposUIDs:
                if expr not in self.expr_table and expr not in self.expr_table:
                    self.expr_table.append(expr)
                    #print('Rel_obj-parts', rel_obj.lh_obj.uid, rel_obj.lh_obj.name, \
                    #      rel_obj.rel_type.base_phrases[0], rel_obj.rh_obj.name)
                    self.Add_line_to_network_model(rel_obj, expr)

                # If base phrase <is a part of> and right hand is the object in focus
                # then lh is a part
                if expr[phrase_type_uid_col] == basePhraseUID:
                    if obj.uid == expr[rh_uid_col]:
                        part_uid = expr[lh_uid_col]

                # If inverse phrase <has as part> and left hand is the object in focus
                # then rh is a part
                elif expr[phrase_type_uid_col] == inversePhraseUID:
                    if obj.uid == expr[lh_uid_col]:
                        part_uid = expr[rh_uid_col]
                else:
                    self.Display_message(
                        'The uid of the phrase type {} is incorrect'.\
                        format(expr[phrase_type_uid_col]),\
                        'De uid van de soort frase {} is niet correct'.\
                        format(expr[phrase_type_uid_col]))
                    continue

                if part_uid != '':
                    # There is an explicit part found; create part_header, prod_head_4,
                    # the first time only
                    if self.part_head_req is True:
                        self.line_nr += 1
                        prod_head_4 = ['','','',self.line_nr, compHead[self.GUI_lang_index], \
                                       partHead[self.GUI_lang_index],\
                                       par3Head[self.GUI_lang_index], \
                                       kindHead[self.GUI_lang_index],'','','','','']
                        if len(self.prod_model) < self.max_nr_of_rows:
                            # Header of part list
                            self.prod_model.append(prod_head_4)
                        self.part_head_req = False
                    part = self.uid_dict[part_uid]

                    status = expr[status_col]

                    # Verify if the classification of the part is known
                    if len(part.classifiers) == 0:
                        part_kind_uid  = ''
                        part_kind_name = unknownClassifierText[self.GUI_lang_index]
                    else:
                        part_kind_uid  = part.classifiers[0].uid
                        # Determine name etc. of the kind that classifies the part
                        if len(part.classifiers[0].names_in_contexts) > 0:
                            #print('Part classifier names', self.reply_lang_pref_uids, \
                            #      part.classifiers[0].names_in_contexts)
                            lang_name, comm_name, part_kind_name, descrOfKind = \
                                self.user_interface.Determine_name_in_context(part.classifiers[0])
                        else:
                            part_kind_name = part.classifiers[0].name
                            #print('Part_classifier_name', part_kind_name)
                            comm_name = self.unknown[self.GUI_lang_index]

                    # Determine the preferred name of the part
                    if len(part.names_in_contexts) > 0:
                        lang_name, community_name, part_name, descrOfKind = \
                            self.user_interface.Determine_name_in_context(part)
                    else:
                        part_name = part.name
                        community_name = self.unknown[self.GUI_lang_index]
                        self.Display_message(
                            'Part {} has no defined name for its language community.'.\
                            format(part.name),\
                            'Deel {} heeft geen gedefinieerde naam van zijn taalgemeenschap.'.\
                            format(part.name))

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


    def Find_kinds_of_aspects(self, obj, role):
        ''' Search for kinds of aspects that can/shall or are by definition possessed
            by a kind of thing (obj)
            and search for their qualitative subtypes
            and possible collection of allowed values.
            obj = the kind in focus
            role = the role played by an involved object that is involved in an occurrence
            decomp_level = indentation level:
                           0 = objectInFocus, 1 = part, 2 = part of part, etc.
            obj.category = category of the object in focus,
                being individual or kind or phys object or occurrence or kind of occurrence
        '''

        unknownKind  = ['unknown supertype','onbekend supertype']
        noValuesText = ['No specification','Geen specificatie']
        self.has_as_subtypes = ['has as subtypes', 'heeft als subtypes']
        possible_aspect_text = ['possible characteristic of a ', 'mogelijk kenmerk van een ']
        of_text = [' (of ', ' (van ']

        # Collect all relations in expr_table
        # and include line in network_model view
        for rel_obj in obj.relations:
                expr = rel_obj.expression
                if len(self.expr_table) < self.max_nr_of_rows and expr not in self.expr_table:
                    self.expr_table.append(expr)
                    self.Add_line_to_network_model(rel_obj, expr)

        # Search for expressions that are <can have as aspect a> kind of relation
        # or subtypes of that kind of relation
        # with the obj.uid (or its supertypes) at left or at right.

        # Initialize number of kinds of aspects that are possessed by this kind of object
        nr_of_aspects = 0
        value_name = ''
        aspect_uid = ''
        aspect_name = ''
        uom_uid = ''
        uom_name = ''
        equality = ''
        status = ''

        # Determine preferred obj name
        if len(obj.names_in_contexts) > 0:
            lang_name, comm_name, obj_name, descr = \
                       self.user_interface.Determine_name_in_context(obj)
        else:
            obj_name = obj.name

        # Collect list of obj and its supertypes in the complete hierarchy
        # for searching inherited aspects
        all_supers = self.Determine_supertypes(obj)

        # For each object in the hierarchy find aspects and inherited aspect values
        # but exclude the roles
        for obj_i in all_supers:
            value_presence = False
            for rel_obj in obj_i.relations:
                expr = rel_obj.expression
                # Find expression with poss_of_aspect relations about the object
                # (or its supertype)
                if expr[lh_uid_col] == obj_i.uid \
                   and (expr[rel_type_uid_col] in self.gel_net.subConcPossAspUIDs \
                        and not expr[rel_type_uid_col] in self.gel_net.conc_playing_uids):
                    aspect_uid   = expr[rh_uid_col]
                    aspect_name  = expr[rh_name_col]
                    role_uid     = expr[rh_role_uid_col]
                    role_name    = expr[rh_role_name_col]
                elif expr[rh_uid_col] == obj_i.uid \
                     and (expr[rel_type_uid_col] in self.gel_net.subConcPossAspUIDs \
                          and not expr[rel_type_uid_col] in self.gel_net.conc_playing_uids):
                    aspect_uid   = expr[lh_uid_col]
                    aspect_name  = expr[lh_name_col]
                    role_uid     = expr[lh_role_uid_col]
                    role_name    = expr[lh_role_name_col]
                else:
                    continue

                # There is a kind of aspect found
                nr_of_aspects += 1
                status = expr[status_col]
                equality = '='
                value_uid = ''
                value_name = ''
                uom_uid = ''
                uom_name = ''
                value_presence = False

                # Searching for values/criteria for the kind of aspect
                # Therefore, find a rh_role object (intrinsic aspect)
                # of the <can have as aspect a> relation.
                if role_uid != '':
                    role = self.uid_dict[role_uid]

                    # Find collection of allowed values
                    # or other criterion, constraints or value for intrinsic aspect, if any.
                    for rel_obj2 in role.relations:
                        expr2 = rel_obj2.expression
                        # Find collection of qualitative aspects for intrinsic aspect (=role),
                        # if any.
                        if role_uid == expr2[lh_uid_col] \
                           and expr2[rel_type_uid_col] in self.gel_net.qualOptionsUIDs:
                            value_uid  = expr2[rh_uid_col]   # collection of allowed values
                            value_name = expr2[rh_name_col]
                            value_presence = True
                            break
                        elif role_uid == expr2[rh_uid_col] \
                             and expr2[rel_type_uid_col] in self.gel_net.qualOptionsUIDs:
                            value_uid  = expr2[lh_uid_col]   # collection of allowed values
                            value_name = expr2[lh_name_col]
                            value_presence = True
                            break

                        # Find conceptual compliancy criterion, (4951)
                        # for intrinsic aspect (=role), if any.
                        elif role_uid == expr2[lh_uid_col] \
                             and expr2[lh_role_uid_col] in self.gel_net.concComplUIDs:
                            value_uid  = expr2[rh_uid_col]   # compliancy criterion or constraint
                            value_name = expr2[rh_name_col]
                            value_presence = True
                            break
                        elif role_uid == expr2[rh_uid_col] \
                             and expr2[rh_role_uid_col] in self.gel_net.concComplUIDs:
                            value_uid  = expr2[lh_uid_col]   # compliancy criterion or constraint
                            value_name = expr2[lh_name_col]
                            value_presence = True
                            break

                        # Find conceptual quantification (1791) for intrinsic aspect (=role),
                        # if any.
                        elif role_uid == expr2[lh_uid_col] \
                             and expr2[rel_type_uid_col] in self.gel_net.concQuantUIDs:
                            value_uid  = expr2[rh_uid_col]   # value (on a scale)
                            value_name = expr2[rh_name_col]
                            uom_uid        = expr2[uom_uid_col]
                            uom_name       = expr2[uom_name_col]
                            value_presence = True
                            break
                        elif role_uid == expr2[rh_uid_col] \
                             and expr2[rel_type_uid_col] in self.gel_net.concQuantUIDs:
                            value_uid  = expr2[lh_uid_col]   # value (on a scale)
                            value_name = expr2[lh_name_col]
                            uom_uid        = expr2[uom_uid_col]
                            uom_name       = expr2[uom_name_col]
                            value_presence = True
                            break

                        # Find conceptual compliance criterion/qualif (4902)
                        # for intrinsic aspect (=role), if any.
                        elif role_uid == expr2[lh_uid_col] \
                             and expr2[rel_type_uid_col] in self.gel_net.subConcComplRelUIDs:
                            # Compliance criterion or def qualification
                            value_uid  = expr2[rh_uid_col]
                            value_name = expr2[rh_name_col]
                            value_presence = True
                            break
                        elif role_uid == expr2[rh_uid_col] \
                             and expr2[rel_type_uid_col] in self.gel_net.subConcComplRelUIDs:
                            # Compliance criterion or def qualification
                            value_uid  = expr2[lh_uid_col]
                            value_name = expr2[lh_name_col]
                            value_presence = True
                            break

                # Determine preferred names for aspect, aspect_supertype, and value
                # Preferred aspect name
                asp = self.uid_dict[aspect_uid]
                if len(asp.names_in_contexts) > 0:
                    lang_name, comm_name, aspect_name, descr = \
                               self.user_interface.Determine_name_in_context(asp)
                else:
                    aspect_name = asp.name

                # Preferred supertype name
                if len(asp.supertypes) > 0:
                    if len(asp.supertypes[0].names_in_contexts) > 0:
                        lang_name, comm_name, asp_supertype_name, descr = \
                                   self.user_interface.Determine_name_in_context(asp.supertypes[0])
                    else:
                        asp_supertype_name = asp.supertypes[0].name
                else:
                    asp_supertype_name = self.unknown[self.GUI_lang_index]

                # Preferred value name
                if value_uid != '':
                    value = self.uid_dict[value_uid]
                    lang_name, comm_name, value_name, descr = \
                           self.user_interface.Determine_name_in_context(value)
                else:
                    value_name = ''

                # If the item is not a subtype (subtype_level == 0)
                # then create a row in the possibilities_model
                #   for any decomp_level
                if self.subtype_level == 0:
                    # Create and insert header for possible characteristics of part
                    # (only preceding the first aspect)
                    if nr_of_aspects == 1:
                        self.poss_asp_of_obj_text = possible_aspect_text[self.GUI_lang_index] + obj_name
                        self.possibility_row[0] = obj.uid
                        self.possibility_row[1] = obj_name
                        self.possibility_row[2] = self.poss_asp_of_obj_text
                        self.possibility_row[3] = obj_name # parent
                        self.possibilities_model.append(self.possibility_row[:])

                    if len(self.possibilities_model) < self.max_nr_of_rows:
                        if len(obj.names_in_contexts) > 0:
                            # The community uid == obj.names_in_contexts[0][1]
                            community_name = self.gel_net.community_dict[obj.names_in_contexts[0][1]]
                        else:
                            community_name = self.unknown[self.GUI_lang_index]
                        self.possibility_row[0] = obj.uid
                        self.possibility_row[1] = aspect_name
                        self.possibility_row[2] = aspect_name + of_text[self.GUI_lang_index] \
                                                  + obj_name + ')'
                        self.possibility_row[3] = self.poss_asp_of_obj_text
                        #print('Aspect:', obj_name, asp.uid, aspect_name, value_name)
                        self.possibility_row[4] = asp_supertype_name
                        self.possibility_row[5] = community_name # of obj
                        self.possibility_row[6] = value_name
                        self.possibility_row[7] = uom_name
                        if self.possibility_row not in self.possibilities_model:
                            self.possibilities_model.append(self.possibility_row[:])
                        else:
                            print('Duplicate possibility row',len(self.possibilities_model), \
                                  self.possibility_row)
                        self.possibility_row  = ['','','','','','','','','','','','','','','']

##                if value_presence is False:
##                    value_name = '' # noValuesText[self.GUI_lang_index]
##                    warnText  = ['Kind of aspect','Soort aspect']
##                    valueMess = ['has no specification of (allowed) values.',\
##                                 'heeft geen specificatie van (toegelaten) waarden.']
##                    print('%s %s (%i) %s' % \
##                          (warnText[self.GUI_lang_index],aspect_name,aspect_uid,\
##                                    valueMess[self.GUI_lang_index]))
                #print('obj_i', value_presence, obj_i.name, nr_of_aspects, aspect_name, \
                #      value_name, len(self.taxon_aspect_uids))

                if value_presence is True:
                    #print('Value present:', obj_i.name, aspect_name, value_name)
                    if len(self.expr_table) < self.max_nr_of_rows:
                        self.expr_table.append(expr2)
                        self.Add_line_to_network_model(rel_obj2, expr2)

                    if self.decomp_level == 0:
                        # Build summary_view header add a column for aspects if not yet included
                        if value_presence is True and aspect_name not in self.taxon_column_names \
                           and len(self.taxon_column_names) <= 14:
                            #print('Summm_header', aspect_name, len(self.taxon_aspect_uids))
                            self.taxon_aspect_uids.append(aspect_uid)
                            self.taxon_column_names.append(aspect_name)
                            self.taxon_uom_names.append(uom_name)
                        self.taxon_ind = 3
                        #print('Sums:',len(self.taxon_aspect_uids), self.taxon_aspect_uids, \
                        #      self.taxon_column_names, value_name)
                        # Find column in taxon_row where value should be stored
                        for kind_uid in self.taxon_aspect_uids[4:]:
                            self.taxon_ind += + 1
                            # Build list of values conform list of aspects.
                            if kind_uid == aspect_uid:
                                #print('Aspects of phys:',len(self.taxon_aspect_uids), \
                                #      aspect_name, self.taxon_ind, value_name)
                                self.taxon_row[self.taxon_ind] = value_name
                                # Check whether there the uom corresponds with the table uom
                                # (when there is a value)
                                if value_name != '' \
                                   and uom_name != self.taxon_uom_names[self.taxon_ind]:
                                    self.Display_message(
                                        'Unit of measure {} ({}) of the value of {} differs'
                                        'from summary table header UoM {}'.\
                                        format(uom_name, uom_uid, aspect_name, \
                                               self.taxon_uom_names[self.taxon_ind]),\
                                        'Meeteenheid {} ({}) van de waarde van {} verschilt'
                                        'van de overzichtstabel kop_eenheid {}'.\
                                        format(uom_name, uom_uid, aspect_name, \
                                               self.taxon_uom_names[self.taxon_ind]))

##                    if self.subtype_level == 0:
##                        # Build composition_view header add a column for aspects,
##                        # if not yet included
##                        if value_presence is True and aspect_name not in self.possib_column_names\
##                                  and len(self.possib_column_names) <= 15:
##                            #print('Compon_header', aspect_name, len(self.possib_aspect_uids))
##                            self.possib_aspect_uids.append(aspect_uid)
##                            self.possib_column_names.append(aspect_name)
##                            self.possib_uom_names.append(uom_name)
##                        self.possib_ind = 4
##                        #print('Sums:',len(self.possib_aspect_uids), self.possib_aspect_uids, \
##                               self.possib_column_names, value_name)
##                        # Find column in possibility_row where value should be stored
##                        for kind_uid in self.possib_aspect_uids[5:]:
##                            self.possib_ind += + 1
##                            # Build list of values conform list of aspects.
##                            if aspect_uid == kind_uid:
##                                #print('Aspects of phys:',len(self.possib_aspect_uids), \
##                                       aspect_name, self.possib_ind, value_name)
##                                self.possibility_row[self.possib_ind] = value_name
##                                if uom_name != self.possib_uom_names[self.possib_ind]:
##                                    print('Unit of measure {} ({}) of the value of {} differs '
##                                          'from composition table header UoM {}'\
##                                          .format(uom_name, uom_uid, aspect_name, \
##                                                  self.possib_uom_names[self.possib_ind]))

                    # Add a line of Line_type 3 to prod_model
                    self.subtype_level = 0 # not a subtype of object in focus
                    #self.line_nr += 1
                    if len(obj.supertypes) > 0:
                        supertype_uid  = obj.supertypes[0].uid
                        supertype_name = obj.supertypes[0].name
                    else:
                        supertype_uid  = ''
                        supertype_name = self.unknown[self.GUI_lang_index]
                    self.Add_prod_model_line_type3(self.subtype_level, \
                                                   obj_i.uid, supertype_uid, aspect_uid, \
                                                   nr_of_aspects, obj.name, role, \
                                                   supertype_name, aspect_name, equality, \
                                                   value_name, uom_name, status)

                    # Determine implied part if any
                    # by determining whether the possessed aspect is an intrinsic aspect, because
                    # rel_type is a <has by definition as intrinsic aspect a> relation (6149)
                    # or its subtype
                    # If that is the case, then it implies that
                    #    there is an implied part of the object in focus that possesses the aspect
                    if expr[rel_type_uid_col] in ['6149', '5848']:
                        # Determine the implied part and its possessed aspect
                        # from the definition of the intrinsic aspect
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
                            if expr_asp[lh_uid_col] == aspect_uid \
                               and expr_asp[rel_type_uid_col] == '5738':
                                part_uid = expr_asp[rh_uid_col]
                                part_name = expr_asp[rh_name_col]
                            elif expr_asp[rh_uid_col] == aspect_uid \
                                 and expr_asp[rel_type_uid_col] == '5738':
                                part_uid = expr_asp[lh_uid_col]
                                part_name = expr_asp[lh_name_col]

                            # If lh_uid is the kind of intr_aspect
                            # and rel_type is <is by definition an intrinsic> (5817)
                            # then rh_obj is the kind of aspect of the kind of part  (and inverse)
                            if expr_asp[lh_uid_col] == aspect_uid \
                               and expr_asp[rel_type_uid_col] == '5817':
                                asp_of_part_uid = expr_asp[rh_uid_col]
                                asp_of_part_name = expr_asp[rh_name_col]
                            if expr_asp[rh_uid_col] == aspect_uid \
                               and expr_asp[rel_type_uid_col] == '5817':
                                asp_of_part_uid = expr_asp[lh_uid_col]
                                asp_of_part_name = expr_asp[lh_name_col]

                        #print('Whole {} has implied part ({}) {} identified with aspect ({}) {}.'\
                        #      .format(obj.name, part_uid, part_name, \
                        #              asp_of_part_uid, asp_of_part_name))
                        key = (part_uid, asp_of_part_uid)
                        self.implied_parts_dict[key] = (part_name, asp_of_part_uid, \
                                                        asp_of_part_name, \
                                                        equality, value_name, uom_name, status)

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
        #                    # Build list of values conform list of aspects.
        #                    # Note: sumRow[0] = component
        #                    if aspect.kind == kind_name:
        #                        #print('Aspects of occ :',nrOfAspOccKinds,aspect_name,\
        #                               aspect.kind,self.taxon_ind,value_name)
        #                        occRow[self.taxon_ind] = value_name
        #                        if uom_name != self.occ_uoms[self.taxon_ind]:
##                                    print('Unit of measure {} ({}) '
##                                          'of the value of {} of kind {} '
##                                          'differs from activity table header UoM {}'.\
##                                          format(uom_name,uom_uid,aspect_name,\
##                                                 aspect.kind, self.occ_uoms[self.taxon_ind]))
        #        # If not a kind of occurrence, then build header for summaryTable
        #        elif self.decomp_level == 0:

        # If obj is object_in_focus (thus not a part)
        # then create one or more rows in taxon_model
        if self.decomp_level == 0:
            if len(obj.supertypes) > 0:
                # Create a row in the taxonomy per direct supertype
                for supertype in obj.supertypes:
                    lang_name, comm_name_super, preferred_name, descr = \
                               self.user_interface.Determine_name_in_context(supertype)
                    self.taxon_row[2] = preferred_name  # of the supertype
                    if len(self.taxon_model) < self.max_nr_of_rows:
                        # If summary row is about object in focus,
                        # then make supertype of object in focus empty
                        # Because treeview parent (taxon_row[2] should be supertype or blank.
                        #print('Subtype_level-1:', self.subtype_level, self.object_in_focus.uid, \
                        #      self.object_in_focus.name, obj.uid, obj.name, self.taxon_row[0:4])
                        if self.taxon_row[0] == self.object_in_focus.uid:
                            self.taxon_row[2] = ''
                            self.taxon_model.append(self.taxon_row[:])

                        # If the object not a subtype of the object_in_focus,
                        # then insert an inter_row header line for the subtypes
                        if self.subtype_level == 0:
                            inter_row = [obj.uid, self.has_as_subtypes[self.GUI_lang_index], \
                                         obj.name, '']
                            self.taxon_model.append(inter_row)

                        # If the supertype is the object_in_focus,
                        # then make the object a sub of the inter_row
                        else:
                            if self.taxon_row[2] == self.object_in_focus.name:
                                self.taxon_row[2] = self.has_as_subtypes[self.GUI_lang_index]
                                self.taxon_model.append(self.taxon_row[:])
                            else:
                                self.taxon_model.append(self.taxon_row[:])
                        #print('Subtype_level-2:', self.subtype_level, obj.name, \
                        #      self.taxon_row[0:4])

            self.taxon_row = ['','','','','','','','','','','','','','']

##        # If not a subtype (subtype_level == 0) and for any decomp_level
##        #    create a row in possibilities_model
##        if self.subtype_level == 0:
##            if len(self.possibilities_model) < self.max_nr_of_rows:
####                if obj not in self.possib_objects:
####                    self.possib_objects.append(obj)
##                # If possibilities row is about object in focus,
##                # then make whole of object in focus empty
##                # Because treeview parent should be whole or blank.
##                if self.possibility_row[0] == obj.uid:
##                    self.possibility_row[2] = ''
##                if self.possibility_row not in self.possibilities_model:
##                    self.possibilities_model.append(self.possibility_row[:])
##                else:
##                    print('Duplicate composition row',len(self.possibilities_model), \
##                          self.possibility_row)
##            self.possibility_row  = ['','','','','','','','','','','','','','','']

        return nr_of_aspects

    def Determine_preferred_kind_name(self, obj):
        ''' Determine the preferred name of the first kind that classified obj
            or the name of the first supertype of obj.
        '''
        kind = None
        if len(obj.classifiers) > 0:
            kind = obj.classifiers[0]
        elif len(obj.supertypes) > 0:
            kind = obj.supertypes[0]
        if kind is not None:
            lang_name, comm_name, kind_name, full_def = \
                       self.user_interface.Determine_name_in_context(kind)
            kind_uid = kind.uid
        else:
            kind_uid = self.unknown[self.GUI_lang_index]
            kind_name = self.unknown[self.GUI_lang_index]
        return kind_name, kind_uid

    def Determine_supertypes(self, obj):
        ''' Collect a list of obj and its supertypes, including super_supers, etc. '''
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

    def Find_kinds_of_parts_and_their_aspects(self, obj):
        """ Search for explicit kinds of parts and combine them with implied kinds of parts"""

        compHead = ['Part hierarchy','Compositie']
        partHead = ['Part of part','Deel van deel']
        par3Head = ['Further part','Verder deel']
        kindHead = ['Kind','Soort']
        of_text = [' (of ', ' (van ']

        role = ''
        self.part_head_req = True
        # Search for kinds of parts of object_in_focus
        for rel_obj in obj.relations:
                expr = rel_obj.expression
                if expr[lh_uid_col] == obj.uid \
                   and expr[rel_type_uid_col] in self.gel_net.subConcComposUIDs\
                   and expr[phrase_type_uid_col] == '1986':
                    part_uid   = expr[rh_uid_col]
                    part_name  = expr[rh_name_col]
                    #role_uid     = expr[rh_role_uid_col]
                    #role_name    = expr[rh_role_name_col]
                elif expr[rh_uid_col] == obj.uid \
                     and expr[rel_type_uid_col] in self.gel_net.subConcComposUIDs\
                     and expr[phrase_type_uid_col] == '6066'  :
                    part_uid   = expr[lh_uid_col]
                    part_name  = expr[lh_name_col]
                    #role_uid     = expr[lh_role_uid_col]
                    #role_name    = expr[lh_role_name_col]
                else:
                    continue

                # There is an explicit kind of part found;
                # create part_header in kind_model, the first time only
                #print('Kind of part', part_name)
                if self.part_head_req is True:
                    self.line_nr += 1
                    prod_head_4 = ['','','',self.line_nr, compHead[self.GUI_lang_index], \
                                   partHead[self.GUI_lang_index],\
                                   par3Head[self.GUI_lang_index], \
                                   kindHead[self.GUI_lang_index],'','','','','']
                    if len(self.kind_model) < self.max_nr_of_rows:
                        # Add header of part to kind_model
                        self.kind_model.append(prod_head_4)
                    self.part_head_req = False

                # Add the expression to the expr_table output table
                if len(self.expr_table) < self.max_nr_of_rows:
                    self.expr_table.append(expr)
                    self.Add_line_to_network_model(rel_obj, expr)

                # Determine preferred name of object (= kind)
                if len(obj.names_in_contexts) > 0:
                    lang_name, community_name, obj_name, descr_of_obj = \
                               self.user_interface.Determine_name_in_context(obj)
                else:
                    obj_name = obj.name

                # Determine preferred name of part (= kind)
                part = self.uid_dict[part_uid]
                if len(part.names_in_contexts) > 0:
                    lang_name, community_name, part_name, descr_of_part = \
                               self.user_interface.Determine_name_in_context(part)
                else:
                    part_name = part.name
                    community_name = self.unknown[self.GUI_lang_index]

                # Determine preferred name of first supertype of part
                if len(part.supertypes) > 0:
                    if len(part.supertypes[0].names_in_contexts) > 0:
                        lang_name, comm_kind_name, part_kind_name, descr_of_kind = \
                            self.user_interface.Determine_name_in_context(part.supertypes[0])
                    else:
                        part_kind_name = part.supertypes[0].name
                else:
                    part_kind_name = self.unknown[self.GUI_lang_index]

                # Create row about possible aspect of kind in possibilities_model
                self.possibility_row[0] = part.uid
                self.possibility_row[1] = part_name
                self.possibility_row[2] = part_name + of_text[self.GUI_lang_index] \
                                          + obj_name + ')'
                self.possibility_row[3] = obj_name  # parent
                self.possibility_row[4] = part_kind_name
                self.possibility_row[5] = community_name # of part
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
                                self.Display_message(
                                    'Object ({}) {} has part ({}) {}'
                                    'with implied aspect ({}) {}.'.\
                                    format(obj.uid, obj.names_in_contexts[0][2], key[0], \
                                           implied_tuple(0), implied_tuple(1), \
                                           implied_tuple(2)),\
                                    'Object ({}) {} heeft als deel ({}) {}'
                                    'met als geïmpliceerd aspect ({}) {}.'.\
                                    format(obj.uid, obj.names_in_contexts[0][2], key[0], \
                                           implied_tuple(0), implied_tuple(1), \
                                           implied_tuple(2)))
                                del self.implied_parts_dict[key]

        # If there are implied kinds of parts left, then create kind_model lines.
        if len(self.implied_parts_dict) > 0:
            #print('Nr of implied parts', len(self.implied_parts_dict))

            # There is an implied part left; thus create a part_header,
            # the first time only
            if self.part_head_req is True:
                self.line_nr += 1
                prod_head_4 = ['','','',self.line_nr, compHead[self.GUI_lang_index], \
                               partHead[self.GUI_lang_index],\
                               par3Head[self.GUI_lang_index], \
                               kindHead[self.GUI_lang_index],'','','','','']
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

                self.Add_prod_model_line_type3(subtype_of_part_level, \
                                               key[0], part_kind_uid, implied_tuple[1], \
                                               nr_of_aspects, part_name, role, \
                                               part_kind_name, aspect_name, equality, \
                                               value_name, uom_name, status)

    def Add_prod_model_line_type3(self, subtype_level, \
                                  part_uid, part_kind_uid, aspect_uid, nr_of_aspects, \
                                  part_name, role, part_kind_name, \
                                  aspect_name, equality, value_name, uom_name, status):
        ''' Create a line_type 3 for product model view '''
        self.line_nr += 1
        # Decomp_level = 0 means object in focus, 1 means: part (2 = part of part, etc.)
        if self.decomp_level == 1 and nr_of_aspects <= 1:
            prod_line_3 = [part_uid, part_kind_uid, aspect_uid, self.line_nr, \
                           part_name, role, '', part_kind_name, aspect_name, '', equality, \
                           value_name, uom_name, status]
        # Decomp_level = 2 means: part of part
        elif self.decomp_level == 2 and nr_of_aspects == 1:
            prod_line_3 = [part_uid, part_kind_uid, aspect_uid, self.line_nr, \
                           role, part_name, '', part_kind_name, aspect_name, '', equality,\
                           value_name, uom_name, status]
        elif self.decomp_level == 3 and nr_of_aspects == 1:
            prod_line_3 = [part_uid, part_kind_uid, aspect_uid, self.line_nr, \
                           '', role, part_name, part_kind_name, aspect_name, '', equality,\
                           value_name, uom_name, status]

        # Subtype_level = 1 means: first decomp_level subtype
        elif subtype_level > 0 and nr_of_aspects == 1:
            prod_line_3 = [part_uid, part_kind_uid, aspect_uid, self.line_nr, \
                           part_name, role, '', part_kind_name, aspect_name, '', equality,\
                           value_name, uom_name, status]
        else:
            prod_line_3 = [part_uid, part_kind_uid, aspect_uid, self.line_nr, \
                           '', '', '', '', aspect_name, '', equality, \
                           value_name, uom_name, status]

        if len(self.kind_model) < self.max_nr_of_rows:
            self.kind_model.append(prod_line_3)

    def Determine_individuals(self, obj):
        ''' Determine whether a kind_in_focus (obj) is a classifier for individual things
            if so, then add individual things to taxonomy (taxon_model) of kinds
        '''
##        if self.individuals > 0:
##            for individual in self.individuals:
##                indiv_uid = individual.uid
        has_as_individuals = ['classifies as individual ', \
                              'classificeert als individuele ']
        first_time = True

        for rel_obj in obj.relations:
            expr = rel_obj.expression
            # Find a classification relation for the kind_in_focus
            if expr[rel_type_uid_col] in self.gel_net.sub_classif_uids:

                # Find the individual object that is classified
                if expr[lh_uid_col] == obj.uid:
                    indiv_uid = expr[rh_uid_col]
                elif expr[rh_uid_col] == obj.uid:
                    indiv_uid = expr[lh_uid_col]
                else:
                    continue
                # Store the expression in the expr_table for display and possible export
                if len(self.expr_table) < self.max_nr_of_rows:
                    self.expr_table.append(expr)
                    self.Add_line_to_network_model(rel_obj, expr)

                # Individual thing uid is found via classification relation
                indiv = self.uid_dict[indiv_uid]

                # Insert an inter_row header for classified individual things
                # in the taxonomy; the first time only
                if first_time is True:
                    header_text = has_as_individuals[self.GUI_lang_index]+obj.name
                    inter_row = [obj.uid, header_text, obj.name, '']
                    self.taxon_model.append(inter_row)
                    first_time = False

                # Create a row in the taxonomy for an individual thing
                # under the header for individual things
                lang_name, community_name, preferred_name, descr = \
                           self.user_interface.Determine_name_in_context(indiv)
##                # Indiv.names_in_contexts[0][1] == community uid
##                community_name = self.gel_net.community_dict[indiv.names_in_contexts[0][1]]
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

    def Occurs_and_involvs(self, obj):
        """ Search for occurrences in which the obj (in focus) is involved.
            The occurrences are related with an involver role
            or one of its subtypes to the (physical) object_in_focus
            and search for (physical) objects
            that are involved in those occurrences in various roles.
            Search for aspects of the occurrences (such as duration).
            Store results in prod_model and the composition in partWholeOcc.
        """
        occur_head   = ['Occurrences' ,'Gebeurtenissen']
        role_head    = ['Role'        ,'Rol']
        involv_head  = ['Involved object','Betrokken object']
        kind_head    = ['Kind'        ,'Soort']
        #print('**** Occurs_and_involvs:',obj.uid, obj.name, obj.category)

        nr_of_occur = 0
        self.occ_in_focus = 'no'
        self.line_nr += + 1

        # Search for UID and <involved> role or its subtypes to find occurrences
        # (involver role players)
        for rel_obj in obj.relations:
            expr = rel_obj.expression
            if (expr[rh_uid_col] == obj.uid and expr[rel_type_uid_col] in self.gel_net.subInvolvUIDs):
                occ_uid   = expr[lh_uid_col]
                #occ_name  = expr[lh_name_col]
            elif expr[lh_uid_col] == obj.uid and expr[rel_type_uid_col] in self.gel_net.subInvolvUIDs:
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
                               involv_head[self.GUI_lang_index], kind_head[self.GUI_lang_index], \
                               '','','','','']
                self.prod_model.append(prod_head_5)

            if len(self.expr_table) < self.max_nr_of_rows:
                self.expr_table.append(expr)
                self.Add_line_to_network_model(rel_obj, expr)

            # Record the role playing occurrence in occ_model
            # Find classifying kind of occurrence
            if len(occ.classifiers) > 0:
                occ_kind = occ.classifiers[0]
                occ_kind_name = occ_kind.name
                occ_kind_uid = occ_kind.uid
            else:
                self.Display_message(
                    'Occurrence {} classifier is unknown.'.format(occ.name),\
                    'Gebeurtenis {} classificeerder is onbekend.'.format(occ.name))
                occ_kind_name = self.unknown[self.GUI_lang_index]
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

            # If no aspects found then line without aspects
            # (otherwise line is included in Find_aspects
            if nr_of_aspects == 0:
                self.line_nr += + 1
                prod_line_5 = [occ.uid, occ_kind.uid, '', self.line_nr, occ_name,'','',\
                               occ_kind_name,'','','','','',status]
                self.prod_model.append(prod_line_5)

            # Search for objects that are involved in the found occurrence
            # decomp_level determines print layout in product model.
            self.decomp_level = 3
            for rel_occ in occ.relations:
                expr_occ = rel_occ.expression
                # Search <is involved in> or <is involving>
                # or any of its subtypes relations in occ
                # excluding the object in focus (obj)
                if expr_occ[rh_uid_col] != obj.uid \
                   and (expr_occ[lh_uid_col] == occ.uid \
                        and expr_occ[rel_type_uid_col] in self.gel_net.subInvolvUIDs):
                    involved_uid = expr_occ[rh_uid_col]
                    #involved_name = expr_occ[rh_name_col]
                    inv_role_name = expr_occ[rh_role_name_col]
                elif expr_occ[lh_uid_col] != obj.uid \
                     and (expr_occ[rh_uid_col] == occ.uid \
                          and expr_occ[rel_type_uid_col] in self.gel_net.subInvolvUIDs):
                    involved_uid = expr_occ[lh_uid_col]
                    #involved_name = expr_occ[lh_name_col]
                    inv_role_name = expr_occ[lh_role_name_col]
                else:
                    continue

                # An object is found that is involved in the occurrence
                involved = self.uid_dict[involved_uid]
                #print('Involved:',obj.uid, involved.uid, involved.name,\
                #      'roles:',expr_occ[lh_role_uid_col],expr_occ[rh_role_uid_col])

                self.expr_table.append(expr_occ)
                self.Add_line_to_network_model(rel_occ, expr_occ)
                status = expr_occ[status_col]

                # Determine the kind of the involved individual object
                if len(involved.classifiers) > 0:
                    involved_kind = involved.classifiers[0]
                    involved_kind_name = involved_kind.name
                else:
                    self.Display_message(
                        'The involved object {} has no classifier.'.\
                        format(involved.name),\
                        'Het betrokken object {} heeft geen classificeerder.'.\
                        format(involved.name))
                    involved_kind_name = self.unknown[self.GUI_lang_index]

                # Search for aspects of objects that are involved in occurrence
                # Find possession of aspect relations of involved object
                nr_of_aspects = self.Find_aspects(involved, inv_role_name)

                # if no aspects of part found, then record part only
                if nr_of_aspects == 0:
                    self.line_nr += + 1
                    prod_line_6 = [involved.uid, involved_kind.uid, '', \
                                   self.line_nr, '', inv_role_name, involved.name, \
                                   involved_kind_name, '','','','','', status]
                    self.prod_model.append(prod_line_6)

            # Search for successors or predecessors of found occurrence
            #   with inputs and outputs and parts (? see below)
            self.Determine_sequences_of_occurrences(occ)

            # Search for parts of found occurrence and parts of parts, etc.
            occ_level = 1
            self.PartOfOccur(occ, occ_level)

##        # Check whether nr of occurrences = 0
##        if nr_of_occur == 0:
##            #if self.GUI_lang_index == 1:
##            #    print('Geen gebeurtenissen gevonden '
##                       'in antwoord op vraag over {} ({})'.format(name,UID))
##            #else:
##            #    print('No involving occurrences found '
##                       'in query results for {} ({})'.format(name,UID))
##            self.line_nr += + 1
##            none = ['None','Geen']
##            prod_head_5A = ['','','',self.line_nr, none[self.GUI_lang_index],\
##                            '','','','','','','','']
##            self.prod_model.append(prod_head_5A)

    def Determine_sequences_of_occurrences(self, occ):
        """ Build occurrences (activities or processes or events)
            and their components
            with sequences between the occurrences and between components
            in the seq_table and inputs and outputs in involv_table.
            seq_table:    previus_obj, next_obj.
            involv_table: occur_obj,   involved_obj, role_obj (of invObj), invKindName.
            p_occ_table:  whole_obj,   part_obj,     kindOfPartName
        """
        #print('Determine_sequences_of_occurrences',occ.uid, occ.name)
        part_uids = []
        nr_of_sequences = 0
        nr_of_ins_and_outs = 0
        nr_of_parts = 0
        # Build sequence table (seq_table) for sequence of occurrences
        for rel_occ in occ.relations:
            expr = rel_occ.expression
            # Search for predecessor - successor relations
            if expr[rh_uid_col] == occ.uid and expr[rh_role_uid_col] in self.gel_net.subNextUIDs:
                predecessor = self.uid_dict[expr[lh_uid_col]]
                self.seq_table.append([predecessor, occ])
                nr_of_sequences += 1
            # And for the inverse expressions
            elif expr[lh_uid_col] == occ.uid and expr[lh_role_uid_col] in self.gel_net.subNextUIDs:
                predecessor = self.uid_dict[expr[rh_uid_col]]
                self.seq_table.append([predecessor, occ])
                nr_of_sequences += 1

            # Search for inputs and outputs (streams) in involv_table
            elif expr[lh_uid_col] == occ.uid and expr[rel_type_uid_col] in self.gel_net.subInvolvUIDs:
                involved = self.uid_dict[expr[rh_uid_col]]
                if len(involved.classifiers) > 0:
                    inv_kind_name = involved.classifiers[0].name
                else:
                    inv_kind_name = self.unknown[self.GUI_lang_index]
                rel_type = self.uid_dict[expr[rel_type_uid_col]]
                inv_role_kind = rel_type.second_role

                self.involv_table.append([occ, involved, inv_role_kind, inv_kind_name])
                nr_of_ins_and_outs += 1

            # Search for inverse relation
            elif expr[rh_uid_col] == occ.uid and expr[rel_type_uid_col] in self.gel_net.subInvolvUIDs:
                involved = self.uid_dict[expr[lh_uid_col]]
                if len(involved.classifiers) > 0:
                    inv_kind_name = involved.classifiers[0].name
                else:
                    inv_kind_name = self.unknown[self.GUI_lang_index]
                rel_type = self.uid_dict[expr[rel_type_uid_col]]
                inv_role_kind = rel_type.second_role

                self.involv_table.append([occ, involved, inv_role_kind, inv_kind_name])
                nr_of_ins_and_outs += 1

##            # Search for parts of occurrence, being part - whole relations
##            elif expr[lh_uid_col] == occ.uid \
##                 and expr[rh_role_uid_col] in self.gel_net.subComponUIDs:
##                part = self.uid_dict[expr[rh_uid_col]
##                part_uids.append(part.uid)
##                self.parts_of_occ_table.append([occ, part])
##                nr_of_parts += 1
##            # And for the inverse expressions
##            elif expr[rh_uid_col] == occ.uid \
##                 and expr[lh_role_uid_col] in self.gel_net.subComponUIDs:
##                part = self.uid_dict[expr[lh_uid_col]]
##                part_uids.append(part.uid)
##                self.parts_of_occ_table.append([occ, part])
##                nr_of_parts += 1

        if len(occ.parts) > 0:
            # Determine sequences, IOs and parts of parts
            for part_occ in occ.parts:
                self.Determine_sequences_of_occurrences(part_occ)

    def PartOfOccur(self, occ, occ_level):
        """ Determine whole-parts hierarchy for occurrences
            Store results in prod_model
        """

        parts = False
        part_head   = ['Part occurrence', 'Deelgebeurtenis']
        kind_part_head = ['Kind of part', 'Soort deel']
        for rel_occ in occ.relations:
            expr = rel_occ.expression
            if expr[lh_uid_col] == occ.uid \
               and expr[rel_type_uid_col] in self.gel_net.subComposUIDs:
                # Create header line, only after finding a part the first time
                if parts is False:
                    self.line_nr += + 1
                    prod_line_7 = ['', '', '', self.line_nr, '', part_head[self.GUI_lang_index],\
                                   '', kind_part_head[self.GUI_lang_index], '','','','','','']
                    self.prod_model.append(prod_line_7)
                    parts = True
                part_occ = self.uid_dict[expr[rh_uid_col]]
                status = expr[status_col]

                self.expr_table.append(expr)
                self.Add_line_to_network_model(rel_occ, expr)

                if len(part_occ.classifiers) > 0:
                    kind_part_occ = part_occ.classifiers[0]
                    kind_part_occ_uid = kind_part_occ.uid
                    kind_part_occ_name = kind_part_occ.name
                else:
                    self.Display_message(
                        'The part of occurrnce {} has no classifier'.\
                        format(part_occ.name),\
                        'De deelgebeurtenis {} heeft geen classificeerder'.\
                        format(part_occ.name))
                    kind_part_occ = self.unknown[self.GUI_lang_index]
                    kind_part_occ_uid = '0'
                    kind_part_occ_name = self.unknown[self.GUI_lang_index]

                if occ_level < 2:
                    self.line_nr += + 1
                    prod_line_8 = [part_occ.uid, kind_part_occ_uid, '', self.line_nr, '',\
                                   part_occ.name, '', kind_part_occ_name, '','','','','', status]
                    self.prod_model.append(prod_line_8)
                    self.nr_of_occurrencies += + 1
                    involv_uid = ''
                    role_of_involved = ''
                    self.occ_model.append([part_occ.uid, part_occ.name, occ.name, involv_uid, \
                                           kind_part_occ_uid, '', part_occ.name,  '', \
                                           kind_part_occ_name, role_of_involved])

                # Add whole, part and kind of part occurrence to part_whole_occs hierarchy
                self.part_whole_occs.append([occ, part_occ, kind_part_occ])

                # Search for part on next decomposition level (part_of_part of occurrence)
                part_level = occ_level + 1
                self.PartOfOccur(part_occ, part_level)

    def Define_notebook(self):
        """ Defines a Notebook with various view layouts and displays view contents.
            Starting in grid on row 1.
        """
        # Define the overall views_notebook
        self.views_noteb = Notebook(self.user_interface.main_frame, \
                                    height=600) # width=1000)
        self.views_noteb.grid(column=0, row=1,sticky=NSEW, columnspan=2)
        self.views_noteb.columnconfigure(0,weight=1)
        self.views_noteb.rowconfigure(0,weight=1)
        #self.views_noteb.rowconfigure(1,weight=1)

        self.Define_log_sheet()

    def Display_notebook_views(self):
        ''' For non-empty models define and display a treeview in a notebook tab.'''

    # Define and display Network view sheet = = = = = = = = = = = = =
        if len(self.network_model) > 0:
            self.Define_and_display_network()

    # Define and display Taxonomic view sheet for kinds of products = = = =
        if len(self.taxon_model) > 0:
            self.Define_and_display_taxonomy_of_kinds()

    # Define and display Possibilities_view sheet of kind = = = = = = = = = =
        if len(self.possibilities_model) > 0:
            self.Define_and_display_possibilities_of_kind()

    # Define and display model of a Kind = = = = = = = = = = = = = =
        if len(self.kind_model) > 0:
            self.Define_and_display_kind_view()

    # Define Summary_view sheet for individual products = = = = = = = = = = =
        if len(self.summ_model) > 0:
            # Destroy earlier summary_frame
            try:
                self.summ_frame.destroy()
            except AttributeError:
                pass

            self.Define_summary_sheet()

            self.Display_summary_view()

    # Define Individual_view sheet = = = = = = = = = = = = = = = = = = = = =
        if len(self.indiv_model) > 0:
            self.Define_and_display_individual_model()

    # Define Product_model_sheet view = = = = = = = = = = = = = = = =
        if len(self.prod_model) > 0:
            #print('prod_model',self.prod_model)
            # Destroy earlier product_frame
            try:
                self.prod_frame.destroy()
            except AttributeError:
                pass

            self.Define_product_model_sheet()
            #print('len prod model', len(self.prod_model))

            # Display prod_model in Composition_sheet view
            self.Display_product_model_view()

    # Define Data_sheet view = = = = = = = = = = = = = = = =
        if len(self.prod_model) > 0:
            # Destroy earlier data sheet
            try:
                self.data_sheet.destroy()
            except AttributeError:
                pass

            self.Define_data_sheet()

            # Display prod_model in Data_sheet view
            self.Display_data_sheet_view()

    # Activities view = = = = = = = = = = = = = = = = = = = = =
        if len(self.occ_model) > 0:
            # Destroy earlier activity sheet
            try:
                self.act_frame.destroy()
            except AttributeError:
                pass

            self.Define_activity_sheet()

            # Display occ_model in Activity sheet view
            self.Display_occ_model_view()

     # Define and display Documents_view sheet = = = = = = = = = =
        if len(self.info_model) > 0:
            self.Define_and_display_documents()

     # Define Expressions_view sheet = = = = = = = = = = = = = = = = = = =
        # Destroy earlier expression_frame
        try:
            self.expr_frame.destroy()
        except AttributeError:
            pass

        self.Define_expressions_sheet()

        # Display expressions from self.expr_table in Treeview:
        for query_line in self.expr_table:
            self.expr_tree.insert('', index='end', values=query_line, tags='val_tag')

    def Define_log_sheet(self):
        ''' Define a frame for errors and warnings'''
        self.log_frame = Frame(self.views_noteb)
        self.log_frame.grid (column=0, row=0,sticky=NSEW)
        self.log_frame.columnconfigure(0, weight=1)
        self.log_frame.rowconfigure(0, weight=1)
        log_head = ['Messages and warnings','Berichten en foutmeldingen']
        self.views_noteb.add(self.log_frame, text=log_head[self.GUI_lang_index], sticky=NSEW)
        self.views_noteb.insert("end", self.log_frame, sticky=NSEW)

        # Messages area - text widget definition
        self.log_message = Text(self.log_frame, width = 40, background='#efc') # height = 10,
        log_mess_scroll  = ttk.Scrollbar(self.log_frame,orient=VERTICAL,\
                                         command=self.log_message.yview)
        self.log_message.config(yscrollcommand=log_mess_scroll.set)

        self.log_message.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=NSEW)
        log_mess_scroll.grid(column=0, row=0, sticky=NS+E)

    def Display_message(self, text_en, text_nl):
        if self.GUI_lang_index == 1:
            self.log_message.insert(END, '\n' + text_nl)
        else:
            self.log_message.insert(END, '\n' + text_en)

    def Define_and_display_network(self):
        # Destroy earlier network_frame
        try:
            self.network_frame.destroy()
        except AttributeError:
            pass

        self.Define_network_sheet()

        self.Display_network_view()

    def Define_network_sheet(self):
        ''' Define a network sheet for display of network_model (a list of network rows)
            for display in a tab of Notebook
        '''
        self.network_frame = Frame(self.views_noteb)
        self.network_frame.grid (column=0, row=0, sticky=NSEW, rowspan=2, columnspan=4)
        self.network_frame.columnconfigure(0, weight=1)
        self.network_frame.columnconfigure(1, weight=1)
        self.network_frame.columnconfigure(2, weight=1)
        self.network_frame.columnconfigure(3, weight=1)
        self.network_frame.rowconfigure(0,weight=0)
        self.network_frame.rowconfigure(1,weight=1)

        network_text = ['Network','Netwerk']
        self.views_noteb.add(self.network_frame, text=network_text[self.GUI_lang_index], \
                             sticky=NSEW)
        #self.views_noteb.insert("end", self.network_frame, sticky=NSEW)

##        network_head = ['Network of objects and aspects',\
##                        'Netwerk van objecten en aspecten']
##        network_lbl  = Label(self.network_frame,text=network_head[self.GUI_lang_index])
        net_button_text = ['Display network of left-object', 'Toon netwerk van linker object']
        lh_button_text = ['Display details of left object', 'Toon details van linker object']
        rh_button_text = ['Display details of kind', 'Toon details van soort']
        classif_button_text = ['Classify left individual object', \
                               'Classificeer linker individueel object']

        self.net_button = Button(self.network_frame, text=net_button_text[self.GUI_lang_index], \
                                command=self.Prepare_lh_object_network_view)
        self.lh_button = Button(self.network_frame, text=lh_button_text[self.GUI_lang_index], \
                                command=lambda:self.Prepare_network_object_detail_view('lh_obj'))
        self.rh_button = Button(self.network_frame, text=rh_button_text[self.GUI_lang_index], \
                                command=lambda:self.Prepare_network_object_detail_view('rh_obj'))
        self.classif_button = Button(self.network_frame, \
                                     text=classif_button_text[self.GUI_lang_index], \
                                     command=self.Prepare_for_classification)

        headings = ['UID', 'Name', 'Parent', 'Kind', \
                    'Equal','Value','Unit']
        nr_of_cols = 7 # len(self.taxon_column_names)
        display_cols = headings[3:nr_of_cols]

        self.network_tree = Treeview(self.network_frame, columns=(headings[0:nr_of_cols]),\
                                     displaycolumns=display_cols, selectmode='browse', height=30)
        eqal_head = ['>=<', '>=<']
        valu_head = ['Value', 'Waarde']
        unit_head = ['Unit', 'Eenheid']
        self.network_tree.heading('#0'   , text='Object', anchor=W)
        self.network_tree.heading('UID'  , text='UID'   , anchor=W)
        self.network_tree.heading('Name' , text=self.name_head[self.GUI_lang_index], anchor=W)
        self.network_tree.heading('Parent', text=self.parent_head[self.GUI_lang_index], anchor=W)
        self.network_tree.heading('Kind' , text=self.kind_head[self.GUI_lang_index], anchor=W)
        self.network_tree.heading('Equal', text=eqal_head[self.GUI_lang_index], anchor=W)
        self.network_tree.heading('Value', text=valu_head[self.GUI_lang_index], anchor=W)
        self.network_tree.heading('Unit' , text=unit_head[self.GUI_lang_index], anchor=W)

        self.network_tree.column ('#0'   , minwidth=100, width=200)
        self.network_tree.column ('Parent', minwidth=20, width=50)
        self.network_tree.column ('Kind' , minwidth=20, width=50)
        self.network_tree.column ('Equal', minwidth=5, width=5)
        self.network_tree.column ('Value', minwidth=20, width=50)
        self.network_tree.column ('Unit' , minwidth=8, width=10)

        self.network_tree.tag_configure('rel_tag', option=None, background='#afa')
        self.network_tree.tag_configure('uom_tag', option=None, background='#ccf')
        self.network_tree.tag_configure('sum_tag', option=None, background='#cfc')

        # Locate buttons in grid
##        network_lbl.grid(column=0, row=0, sticky=W)
        self.net_button.grid(column=0, row=0, sticky=W)
        self.lh_button.grid(column=1, row=0, sticky=W)
        self.rh_button.grid(column=2, row=0, sticky=W)
        self.classif_button.grid(column=3, row=0, sticky=W)

        self.network_tree.grid(column=0, row=1, sticky=NSEW, columnspan=4)
        network_scroll = Scrollbar(self.network_frame, orient=VERTICAL, \
                                   command=self.network_tree.yview)
        network_scroll.grid(column=3, row=1, sticky=NS+E)
        self.network_tree.config(yscrollcommand=network_scroll.set)

        self.network_tree.bind(sequence='<Double-1>', func=self.Network_object_detail_view)
        self.network_tree.bind(sequence='i'         , func=self.Network_object_detail_view)
        self.network_tree.bind(sequence='<Double-3>', func=self.Network_object_detail_view)

    def Display_network_view(self):
        # Display header row with units of measure
        #self.network_tree.insert('', index='end', values=self.taxon_uom_names, tags='uom_tag')

        # Display self.network_model rows in self.network_tree
        parents = []
        for network_line in self.network_model:
            # Verify whether network_line[7], being the parent (typically intermediate),
            # is blank or is in the list of parents
            openness = False
            if network_line[7] == '' or network_line[7] in parents:
                # Skip duplicate line
                if self.network_tree.exists(network_line[6]):
                    continue
                else:
                    if network_line[7] == '':
                        openness = True
                    color_tag = 'sum_tag'
                    rel_tag = ''
                    term = network_line[6].partition(' ')
                    if term[0] in ['has', 'heeft', 'classifies', 'classificeert', \
                                   'is', 'can', 'kan', 'shall', 'moet']:
                        rel_tag = 'rel_tag'
                    self.network_tree.insert(network_line[7], index='end', \
                                             values=network_line[5:],\
                                             tags=rel_tag,\
                                             iid=network_line[6], \
                                             text=network_line[6], open=openness)
                    parents.append(network_line[6])

    def Define_and_display_taxonomy_of_kinds(self):
        # Destroy earlier taxon_frame
        try:
            self.taxon_frame.destroy()
        except AttributeError:
            pass

        self.Define_taxonomy_sheet()

        self.Display_taxonomy_view()

    def Define_taxonomy_sheet(self):
        ''' Define a taxonomy sheet for display of taxon_model (a list of taxon_rows)
            for display in a tab of Notebook
        '''
        self.taxon_frame = Frame(self.views_noteb)
        self.taxon_frame.grid (column=0, row=0, sticky=NSEW, rowspan=2)
        self.taxon_frame.columnconfigure(0, weight=1)
        self.taxon_frame.rowconfigure(0,weight=0)
        self.taxon_frame.rowconfigure(1,weight=1)

        taxon_text = ['Taxonomy','Taxonomie']
        self.views_noteb.add(self.taxon_frame, text=taxon_text[self.GUI_lang_index], sticky=NSEW)
        #self.views_noteb.insert("end", self.taxon_frame, sticky=NSEW)

        taxon_head = ['Hierarchy of kinds and aspects per object of a particular kind',\
                      'Hiërarchie van soorten en aspecten per object van een bepaalde soort']
        taxon_lbl  = Label(self.taxon_frame,text=taxon_head[self.GUI_lang_index])

        headings = ['UID','Name', 'Kind','Community','Aspect1','Aspect2','Aspect3','Aspect4',\
                    'Aspect5','Aspect6','Aspect7','Aspect8','Aspect9','Aspect10']
        nr_of_cols = len(self.taxon_column_names)
        display_cols = headings[3:nr_of_cols]

        self.taxon_tree = Treeview(self.taxon_frame,columns=(headings[0:nr_of_cols]),\
                                  displaycolumns=display_cols, selectmode='browse', height=30)

        self.taxon_tree.heading('#0'    , text='Object', anchor=W)
        self.taxon_tree.heading('UID'   , text='UID', anchor=W)
        self.taxon_tree.heading('Name'  , text='Name', anchor=W)
        self.taxon_tree.heading('Kind'  , text='Kind', anchor=W)
        self.taxon_tree.heading('Community', text='Community', anchor=W)

        self.taxon_tree.column ('#0'    , minwidth=100, width=200)
        self.taxon_tree.column ('Community' , minwidth=20, width=50)
        asp = 0
        for column in self.taxon_column_names[4:]:
            asp += 1
            Asp_name = 'Aspect' + str(asp)
            self.taxon_tree.heading(Asp_name, text=self.taxon_column_names[asp +3] ,anchor=W)
            self.taxon_tree.column (Asp_name, minwidth=20 ,width=50)

##        self.taxon_tree.columnconfigure(0,weight=1)
##        self.taxon_tree.rowconfigure   (0,weight=1)

        self.taxon_tree.tag_configure('rel_tag', option=None, background='#afa')
        self.taxon_tree.tag_configure('uom_tag', option=None, background='#ccf')
        self.taxon_tree.tag_configure('sum_tag', option=None, background='#cfc')

        taxon_scroll = Scrollbar(self.taxon_frame, orient=VERTICAL, command=self.taxon_tree.yview)
        taxon_lbl.grid       (column=0, row=0,sticky=EW)
        self.taxon_tree.grid (column=0, row=1,sticky=NSEW)
        taxon_scroll.grid    (column=0, row=1,sticky=NS+E)
        self.taxon_tree.config(yscrollcommand=taxon_scroll.set)

        self.taxon_tree.bind(sequence='<Double-1>', func=self.Taxon_detail_view)
        self.taxon_tree.bind(sequence='c'         , func=self.Taxon_detail_view)

    def Display_taxonomy_view(self):
        # Display header row with units of measure
        self.taxon_tree.insert('', index='end', values=self.taxon_uom_names, tags='uom_tag')
        # Display self.taxon_model rows in self.taxon_tree
        parents = []
        for taxon_line in self.taxon_model:
            #print('Taxon_line', taxon_line)
            # Verify whether taxon_line[2], being the supertype,
            # is blank or in the list of parents
            if taxon_line[2] == '' or taxon_line[2] in parents:
                # Skip duplicates
                if self.taxon_tree.exists(taxon_line[1]):
                    continue
                else:
                    color_tag = 'sum_tag'
                    rel_tag = ''
                    term = taxon_line[1].partition(' ')
                    if term[0] in ['has', 'heeft', 'classifies', 'classificeert']:
                        rel_tag = 'rel_tag'
                    self.taxon_tree.insert(taxon_line[2],index='end',values=taxon_line,\
                                           tags=rel_tag,\
                                           iid=taxon_line[1],text=taxon_line[1], open=True)
                    parents.append(taxon_line[1])

    def Define_summary_sheet(self):
        ''' Define a summary_sheet for display of summ_model (a list of summary_rows)
            for display in a tab of Notebook
        '''
        self.summ_frame = Frame(self.views_noteb)
        self.summ_frame.grid (column=0, row=0,sticky=NSEW) #pack(fill=BOTH, expand=1)
        self.summ_frame.columnconfigure(0, weight=1)
        self.summ_frame.rowconfigure(0,weight=1)
        #self.summ_frame.rowconfigure(1,weight=1)

        summary = ['Summary','Overzicht']
        self.views_noteb.add(self.summ_frame, text=summary[self.GUI_lang_index], sticky=NSEW)
        self.views_noteb.insert("end", self.summ_frame, sticky=NSEW)

        summHead = ['Aspects per object of a particular kind',\
                    'Aspecten per object van een bepaalde soort']
        summ_lbl = Label(self.summ_frame,text=summHead[self.GUI_lang_index])

        headings = ['UID','Name', 'Kind','Community','Aspect1','Aspect2','Aspect3','Aspect4',\
                    'Aspect5','Aspect6','Aspect7','Aspect8','Aspect9','Aspect10']
        nr_of_cols = len(self.summ_column_names)
        display_cols = headings[3:nr_of_cols]

        self.summ_tree = Treeview(self.summ_frame,columns=(headings[0:nr_of_cols]),\
                                  displaycolumns=display_cols, selectmode='browse', height=30)

        self.summ_tree.heading('#0'       , text='Object', anchor=W)
        self.summ_tree.heading('UID'      , text='UID'   , anchor=W)
        self.summ_tree.heading('Name'     , text=self.name_head[self.GUI_lang_index], anchor=W)
        self.summ_tree.heading('Kind'     , text=self.kind_head[self.GUI_lang_index], anchor=W)
        self.summ_tree.heading('Community', text=self.comm_head[self.GUI_lang_index], anchor=W)

        self.summ_tree.column ('#0'       , minwidth=100, width=200)
        self.summ_tree.column ('Community', minwidth=20 , width=50)
        asp = 0
        for column in self.summ_column_names[4:]:
            asp += 1
            Asp_name = 'Aspect' + str(asp)
            self.summ_tree.heading(Asp_name, text=self.summ_column_names[asp +3], anchor=W)
            self.summ_tree.column (Asp_name, minwidth=20, width=50)

        self.summ_tree.columnconfigure(0,weight=1)
        self.summ_tree.rowconfigure   (0,weight=1)

        #self.summ_tree.tag_configure('col_tag', option=None, background='#9f9')
        self.summ_tree.tag_configure('uom_tag', option=None, background='#ccf')
        self.summ_tree.tag_configure('sum_tag', option=None, background='#cfc')

        summScroll = Scrollbar(self.summ_frame, orient=VERTICAL, command=self.summ_tree.yview)
        summ_lbl.grid      (column=0, row=0, sticky=EW)
        self.summ_tree.grid(column=0, row=1, sticky=NSEW)
        summScroll.grid    (column=0, row=1, sticky=NS+E)
        self.summ_tree.config(yscrollcommand=summScroll.set)

        self.summ_tree.bind(sequence='<Double-1>', func=self.Summ_detail_view)

    def Display_summary_view(self):
        ''' Display a summary view that provides a list of items and their aspects.
        '''
        # Display the header row with units of measure in summ_tree treeview
        self.summ_tree.insert('', index='end', values=self.summ_uom_names, tags='uom_tag')
        # Display the various summ_model rows in summ_tree treeview
        parents = []
        for summ_line in self.summ_model:
            if summ_line[2] == '' or summ_line[2] in parents:
                if self.summ_tree.exists(summ_line[1]):
                    continue
                else:
                    # Summ_line[2] is the supertype
                    self.summ_tree.insert(summ_line[2],index='end',values=summ_line,\
                                          tags='sum_tag',iid=summ_line[1],\
                                          text=summ_line[1], open=True)
                    parents.append(summ_line[1])

        # Sorting example
##        # Add command to heading as follows:
##        tree.heading(column1, text = 'some text', command = foo)

##        l = [['a',2], ['a',1], ['b', 2], ['a',3], ['b',1], ['b',3]]
##        l.sort(key=itemgetter(1))
##        l.sort(key=itemgetter(0), reverse=True)
##        # [['b', 1], ['b', 2], ['b', 3], ['a', 1], ['a', 2], ['a', 3]]

    def Define_and_display_possibilities_of_kind(self):
        # Destroy earlier possib_frame
        try:
            self.possib_frame.destroy()
        except AttributeError:
            pass

        self.Define_possibilities_sheet()

        # Display possibilities_sheet
        # Display header row with units of measure
        self.possib_tree.insert('', index='end', values=self.possib_uom_names, tags='uom_tag')
        # Display self.possibilities_model rows in self.possib_tree
        parents = []
        for possib_line in self.possibilities_model:
            # If item parent is blank (has no defined parent, thus item is a top item)
            # or the parent appeared already,
            # then display the row in the tree
            if possib_line[3] == '' or possib_line[3] in parents:
                #print('Possib_line', possib_line)
                # Possib_line[3] is the whole
                self.possib_tree.insert(possib_line[3], index='end', values=possib_line, \
                                        tags='sum_tag', iid=possib_line[2], \
                                        text=possib_line[1], open=True)
                parents.append(possib_line[2])

    def Define_possibilities_sheet(self):
        ''' Define a possibilities_sheet for display of possibilities_model
            (a list of possib_rows)
            for display in a tab of Notebook
        '''
        self.possib_frame = Frame(self.views_noteb)
        self.possib_frame.grid(column=0, row=0, sticky=NSEW, rowspan=2)
        self.possib_frame.columnconfigure(0, weight=1)
        self.possib_frame.rowconfigure(0, weight=0)
        self.possib_frame.rowconfigure(1, weight=1)

        possib_text = ['Possibilities','Mogelijkheden']
        self.views_noteb.add(self.possib_frame, text=possib_text[self.GUI_lang_index],\
                             sticky=NSEW)
        self.views_noteb.insert("end", self.possib_frame, sticky=NSEW)

        possib_head  = ['Possible aspects per object of a particular kind',\
                        'Mogelijke aspecten per object van een bepaalde soort']
        possib_label = Label(self.possib_frame,text=possib_head[self.GUI_lang_index])
        headings = ['UID','Name','Ext_name','Parent','Kind','Community',\
                    'Aspect1','Aspect2','Aspect3','Aspect4','Aspect5',\
                    'Aspect6','Aspect7','Aspect8','Aspect9','Aspect10']
        nr_of_cols = len(self.possib_column_names)
        display_cols = headings[4:nr_of_cols]

        self.possib_tree = Treeview(self.possib_frame, columns=(headings[0:nr_of_cols]),\
                                    displaycolumns=display_cols, selectmode='browse', height=30)

        self.possib_tree.heading('UID'      ,text='UID', anchor=W)
        self.possib_tree.heading('Name'     ,text=self.name_head[self.GUI_lang_index], anchor=W)
        self.possib_tree.heading('Ext_name' ,text=self.name_head[self.GUI_lang_index], anchor=W)
        self.possib_tree.heading('Parent'   ,text=self.parent_head[self.GUI_lang_index], anchor=W)
        self.possib_tree.heading('Kind'     ,text=self.kind_head[self.GUI_lang_index], anchor=W)
        self.possib_tree.heading('Community',text=self.comm_head[self.GUI_lang_index], anchor=W)

        self.possib_tree.column ('#0'       ,minwidth=100, width=200)
        self.possib_tree.column ('Kind'     ,minwidth=20 , width=50)
        self.possib_tree.column ('Community',minwidth=20 , width=50)
        asp = 0
        for column in self.possib_column_names[6:]:
            asp += 1
            Asp_name = 'Aspect' + str(asp)
            self.possib_tree.heading(Asp_name, text=self.possib_column_names[asp +4], anchor=W)
            self.possib_tree.column (Asp_name, minwidth=20 ,width=50)

        self.possib_tree.columnconfigure(0,weight=1)
        self.possib_tree.columnconfigure(1,weight=1)
        self.possib_tree.rowconfigure   (0,weight=1)
        self.possib_tree.rowconfigure   (1,weight=1)

        self.possib_tree.tag_configure('uom_tag', option=None, background='#ccf')
        self.possib_tree.tag_configure('sum_tag', option=None, background='#cfc')

        possib_Scroll = Scrollbar(self.possib_frame, orient=VERTICAL, \
                                  command=self.possib_tree.yview)
        possib_label.grid     (column=0, row=0,sticky=EW)
        self.possib_tree.grid (column=0, row=1,sticky=NSEW)
        possib_Scroll.grid    (column=0, row=1,sticky=NS+E)
        self.possib_tree.config(yscrollcommand=possib_Scroll.set)

        self.possib_tree.bind(sequence='<Double-1>', func=self.Possibilities_detail_view)

    def Define_and_display_individual_model(self):
        # Destroy earlier indiv_frame
        try:
            self.indiv_frame.destroy()
        except AttributeError:
            pass

        self.Define_composition_sheet()

        # Display composition sheet
        self.Display_composition_view()

    def Define_composition_sheet(self):
        ''' Define a sheet for display of an individual thing
            (indiv_model, a list of indiv_rows)
            for display in a tab of Notebook
        '''
        self.indiv_frame  = Frame(self.views_noteb)
        self.indiv_frame.grid (column=0, row=0,sticky=NSEW) #pack(fill=BOTH, expand=1)
        self.indiv_frame.columnconfigure(0, weight=1)
        self.indiv_frame.rowconfigure(0,weight=1)
        self.indiv_frame.rowconfigure(1,weight=1)

        indiv_text = ['Composition','Samenstelling']
        self.views_noteb.add(self.indiv_frame, text=indiv_text[self.GUI_lang_index], sticky=NSEW)
        self.views_noteb.insert("end", self.indiv_frame, sticky=NSEW)

        indiv_Head = ['Aspects per individual object','Aspecten per individueel object']
        indiv_Lbl  = Label(self.indiv_frame,text=indiv_Head[self.GUI_lang_index])
        headings = ['UID','Name','Parent','Kind','Community','Aspect1','Aspect2','Aspect3',\
                    'Aspect4','Aspect5','Aspect6','Aspect7','Aspect8','Aspect9','Aspect10']
        nr_of_cols = len(self.indiv_column_names)
        display_cols = headings[3:nr_of_cols]

        self.indiv_tree = Treeview(self.indiv_frame,columns=(headings[0:nr_of_cols]),\
                                  displaycolumns=display_cols, selectmode='browse', height=30)

        self.indiv_tree.heading('#0'       ,text='Object', anchor=W)
        self.indiv_tree.heading('UID'      ,text='UID'   , anchor=W)
        self.indiv_tree.heading('Name'     ,text=self.name_head[self.GUI_lang_index], anchor=W)
        self.indiv_tree.heading('Parent'   ,text=self.parent_head[self.GUI_lang_index], anchor=W)
        self.indiv_tree.heading('Kind'     ,text=self.kind_head[self.GUI_lang_index], anchor=W)
        self.indiv_tree.heading('Community',text=self.comm_head[self.GUI_lang_index], anchor=W)

        self.indiv_tree.column ('#0'       ,minwidth=100, width=200)
        self.indiv_tree.column ('Kind'     ,minwidth=20 , width=50)
        self.indiv_tree.column ('Community',minwidth=20 , width=50)
        asp = 0
        for column in self.indiv_column_names[5:]:
            asp += 1
            Asp_name = 'Aspect' + str(asp)
            self.indiv_tree.heading(Asp_name, text=self.indiv_column_names[asp +4], anchor=W)
            self.indiv_tree.column (Asp_name, minwidth=20 ,width=50)

        self.indiv_tree.columnconfigure(0,weight=1)
        self.indiv_tree.columnconfigure(1,weight=1)
        self.indiv_tree.rowconfigure   (0,weight=1)
        self.indiv_tree.rowconfigure   (1,weight=1)

        self.indiv_tree.tag_configure('uom_tag', option=None, background='#ccf')
        self.indiv_tree.tag_configure('sum_tag', option=None, background='#cfc')

        indiv_Scroll = Scrollbar(self.indiv_frame, orient=VERTICAL, command=self.indiv_tree.yview)
        indiv_Lbl.grid      (column=0, row=0,sticky=EW)
        self.indiv_tree.grid(column=0, row=1,sticky=NSEW)
        indiv_Scroll.grid   (column=0, row=1,sticky=NS+E)
        self.indiv_tree.config(yscrollcommand=indiv_Scroll.set)

        self.indiv_tree.bind(sequence='<Double-1>', func=self.Indiv_detail_view)

    def Display_composition_view(self):
        ''' Display rows in indiv_model (composition of individual object)
            in composition sheet view
        '''
        # Display header row with units of measure
        self.indiv_tree.insert('', index='end', values=self.indiv_uom_names, tags='uom_tag')
        # Display self.indiv_model rows in self.indiv_tree
        indiv_parents = []
        for indiv_line in self.indiv_model:
            # Indiv_line[2] is the whole
            if indiv_line[2] == '' or indiv_line[2] in indiv_parents:
                self.indiv_tree.insert(indiv_line[2], index='end', \
                                       values=indiv_line,tags='sum_tag',iid=indiv_line[1],\
                                       text=indiv_line[1], open=True)
                indiv_parents.append(indiv_line[1])

    def Define_expressions_sheet(self):
        ''' Define expressions view sheet for display of expr_table in Notebook tab
        '''
        self.expr_frame = Frame(self.views_noteb)
        self.expr_frame.grid (column=0, row=0,sticky=NSEW, rowspan=4)
        self.expr_frame.columnconfigure(0,weight=1)
        self.expr_frame.rowconfigure(0,weight=0)
        self.expr_frame.rowconfigure(1,weight=0)
        self.expr_frame.rowconfigure(2,weight=0)
        self.expr_frame.rowconfigure(3,weight=1)

        expressions = ['Expressions' ,'Uitdrukkingen']
        save_on_CSV_file  = ['Save on CSV file','Opslaan op CSV file']
        save_on_JSON_file = ['Save on JSON file','Opslaan op JSON file']

        self.views_noteb.add(self.expr_frame, text=expressions[self.GUI_lang_index],sticky=NSEW)
        self.views_noteb.insert("end",self.expr_frame,sticky=NSEW)
        # Define button for display of contextual facts
        details_button   = Button(self.expr_frame, text='Context', command=self.Contextual_facts)
        save_CSV_button  = Button(self.expr_frame, text=save_on_CSV_file[self.GUI_lang_index], \
                                  command=self.Save_on_CSV_file)
        save_JSON_button = Button(self.expr_frame, text=save_on_JSON_file[self.GUI_lang_index], \
                                  command=self.Save_on_JSON_file)

        header = ['Model expressions in Gellish','Uitdrukkingen in Gellish']
        expr_lbl = Label(self.expr_frame, text=header[self.GUI_lang_index],justify='left')

        self.expr_tree = Treeview(self.expr_frame,\
            columns=('seq'       ,'langUID'    ,'langName'  ,'commUID'    ,'commName' ,\
                     'reality'   ,'intentUID'  ,'intentName','lhCard'     ,'lhUID'    ,\
                     'lhName'    ,'lhRoleUID'  ,'lhRoleName','validUID'   ,'validName',\
                     'ideaUID'   ,'ideaDescr'  ,'reltypeUID','reltypeName','phrasetypeUID',\
                     'rhRoleUID' ,'rhRoleName' ,'rhCard'    ,'rhUID'      ,'rhName'   ,\
                     'partDef'   ,'fullDef'    ,'uomUID'    ,'uomName'    ,'accUID'   ,\
                     'accName'   ,'pickUID'    ,'pickName'  ,'remarks'    ,'status'   ,\
                     'reason'    ,'succUID'    ,'dateStartVal','dateStartAv','dateCC' ,\
                     'dateLatChE','orignatorUID','originatorName','authorUID','authorName',\
                     'addrUID'   ,'addrName'   ,'refs'      ,'exprUID'    ,'collUID'  ,\
                     'collName'  ,'fileName'   ,'lhComm'    ,'rhComm'     ,'relComm' ),\
            displaycolumns=('langName','commName','ideaUID','lhUID'  ,'lhName','reltypeUID',\
                            'reltypeName','rhUID','rhName' ,'fullDef','uomUID','uomName',\
                            'remarks' ,'status') ,\
            selectmode='browse', height=20\
                                  )

        self.expr_tree.heading('seq'       ,text='Seq'       ,anchor=W)
        self.expr_tree.heading('langUID'   ,text='langUID'   ,anchor=W)
        self.expr_tree.heading('langName'  ,text='Language'  ,anchor=W)
        self.expr_tree.heading('commUID'   ,text='commUID'   ,anchor=W)
        self.expr_tree.heading('commName'  ,text='Community' ,anchor=W)
        self.expr_tree.heading('reality'   ,text='reality'   ,anchor=W)
        self.expr_tree.heading('intentUID' ,text='intentUID' ,anchor=W)
        self.expr_tree.heading('intentName',text='intentName',anchor=W)
        self.expr_tree.heading('lhCard'    ,text='lhCard'    ,anchor=W)
        self.expr_tree.heading('lhUID'     ,text='lhUID'     ,anchor=W)
        self.expr_tree.heading('lhName'    ,text='lhName'    ,anchor=W)
        self.expr_tree.heading('lhRoleUID' ,text='lhRoleUID' ,anchor=W)
        self.expr_tree.heading('lhRoleName',text='lhRoleName',anchor=W)
        self.expr_tree.heading('validUID'  ,text='validUID'  ,anchor=W)
        self.expr_tree.heading('validName' ,text='validName' ,anchor=W)
        self.expr_tree.heading('ideaUID'   ,text='ideaUID'   ,anchor=W)
        self.expr_tree.heading('ideaDescr' ,text='ideaDescr' ,anchor=W)
        self.expr_tree.heading('reltypeUID',text='reltypeUID',anchor=W)
        self.expr_tree.heading('reltypeName',text='relation type',anchor=W)
        self.expr_tree.heading('phrasetypeUID',text='phrase type',anchor=W)
        self.expr_tree.heading('rhRoleUID' ,text='rhRoleUID' ,anchor=W)
        self.expr_tree.heading('rhRoleName',text='rhRoleName',anchor=W)
        self.expr_tree.heading('rhCard'    ,text='rhCard'    ,anchor=W)
        self.expr_tree.heading('rhUID'     ,text='rhUID'     ,anchor=W)
        self.expr_tree.heading('rhName'    ,text='rhName'    ,anchor=W)
        self.expr_tree.heading('partDef'   ,text='partDef'   ,anchor=W)
        self.expr_tree.heading('fullDef'   ,text='Description',anchor=W)
        self.expr_tree.heading('uomUID'    ,text='uomUID'    ,anchor=W)
        self.expr_tree.heading('uomName'   ,text='UoM'       ,anchor=W)
        self.expr_tree.heading('accUID'    ,text='accUID'    ,anchor=W)
        self.expr_tree.heading('accName'   ,text='accName'   ,anchor=W)
        self.expr_tree.heading('pickUID'   ,text='pickUID'   ,anchor=W)
        self.expr_tree.heading('pickName'  ,text='pickName'  ,anchor=W)
        self.expr_tree.heading('remarks'   ,text='Remarks'   ,anchor=W)
        self.expr_tree.heading('status'    ,text='Status'    ,anchor=W)

        self.expr_tree.column ('#0'        ,minwidth=10,width=20)
        self.expr_tree.column ('seq'       ,minwidth=10,width=20)
        self.expr_tree.column ('langUID'   ,minwidth=20,width=55)
        self.expr_tree.column ('langName'  ,minwidth=15,width=80)
        self.expr_tree.column ('commUID'   ,minwidth=15,width=55)
        self.expr_tree.column ('commName'  ,minwidth=15,width=80)
        self.expr_tree.column ('reality'   ,minwidth=15,width=40)
        self.expr_tree.column ('intentUID' ,minwidth=15,width=55)
        self.expr_tree.column ('intentName',minwidth=15,width=80)
        self.expr_tree.column ('lhCard'    ,minwidth=15,width=40)
        self.expr_tree.column ('lhUID'     ,minwidth=15,width=55)
        self.expr_tree.column ('lhName'    ,minwidth=15,width=150)
        self.expr_tree.column ('lhRoleUID' ,minwidth=15,width=55)
        self.expr_tree.column ('lhRoleName',minwidth=15,width=80)
        self.expr_tree.column ('validUID'  ,minwidth=15,width=55)
        self.expr_tree.column ('validName' ,minwidth=15,width=80)
        self.expr_tree.column ('ideaUID'   ,minwidth=15,width=55)
        self.expr_tree.column ('ideaDescr' ,minwidth=15,width=80)
        self.expr_tree.column ('reltypeUID',minwidth=15,width=55)
        self.expr_tree.column ('reltypeName',minwidth=15,width=200)
        self.expr_tree.column ('phrasetypeUID',minwidth=15,width=40)
        self.expr_tree.column ('rhRoleUID' ,minwidth=15,width=55)
        self.expr_tree.column ('rhRoleName',minwidth=15,width=80)
        self.expr_tree.column ('rhCard'    ,minwidth=15,width=40)
        self.expr_tree.column ('rhUID'     ,minwidth=15,width=55)
        self.expr_tree.column ('rhName'    ,minwidth=15,width=150)
        self.expr_tree.column ('partDef'   ,minwidth=15,width=5)
        self.expr_tree.column ('fullDef'   ,minwidth=15,width=120)
        self.expr_tree.column ('uomUID'    ,minwidth=15,width=55)
        self.expr_tree.column ('uomName'   ,minwidth=15,width=60)
        self.expr_tree.column ('accUID'    ,minwidth=15,width=55)
        self.expr_tree.column ('accName'   ,minwidth=15,width=80)
        self.expr_tree.column ('pickUID'   ,minwidth=15,width=55)
        self.expr_tree.column ('pickName'  ,minwidth=15,width=80)
        self.expr_tree.column ('remarks'   ,minwidth=15,width=100)
        self.expr_tree.column ('status'    ,minwidth=15,width=120)

        exprScrollV = Scrollbar(self.expr_frame, orient=VERTICAL  , command=self.expr_tree.yview)
        exprScrollV.grid      (column=0, row=1, sticky=NS+E, rowspan=3)
        exprScrollH = Scrollbar(self.expr_frame, orient=HORIZONTAL, command=self.expr_tree.xview)
        exprScrollH.grid      (column=0, row=3, sticky=S+EW)
        expr_lbl.grid         (column=0, row=0, sticky=NSEW)
        self.expr_tree.grid   (column=0, row=1, sticky=NSEW, rowspan=3)
        details_button.grid   (column=1, row=0, sticky=N)
        save_CSV_button.grid  (column=1, row=1, sticky=N)
        save_JSON_button.grid (column=1, row=2, sticky=N)

        self.expr_tree.config(yscrollcommand=exprScrollV.set)
        self.expr_tree.config(xscrollcommand=exprScrollH.set)
        self.expr_tree.tag_configure('val_tag'  ,background='#cfc')

        self.expr_tree.columnconfigure(0,weight=1)

        self.expr_tree.bind(sequence='<Double-1>', func=self.Expr_detail_view)

    def Save_on_CSV_file(self):
        """ Saving query results in a CSV file in Gellish Expression Format."""
        import csv
        import time

        date = time.strftime("%x")
        # Create 3 header records of file
        header1 = ['Gellish', 'Nederlands', 'Version', '9.0', date, 'Query results',\
                   'Query results about '+self.object_in_focus.name,'','','','','']
        # header2 = expr_col_ids from initial settings
        # header3 is taken from Expr_Table_Def

        # Open an output file for saving the header lines and the expr_table
        # Note: the r upfront the string (rawstring) is
        #       to avoid interpretation as a Unicode string (and thus giving an error)
        # ini_out_path from bootstrapping
        ini_file_name = 'QueryResults.csv'
        outputFile = filedialog.asksaveasfilename(filetypes  = (("CSV files","*.csv"),\
                                                               ("All files","*.*")),\
                                                  title      = "Enter a file name",\
                                                  initialdir = ini_out_path,\
                                                  initialfile= ini_file_name,\
                                                  parent     = self.expr_frame)
        if outputFile == '':
            outputFile = ini_file_name
            self.Display_message(
                'File name for saving is blank or file selection is cancelled. '
                'If generated, the file is saved under the name <{}>'.\
                format(outputFile), \
                'De filenaam voor opslaan is blanco of the file opslag is gecancelled. '
                'Indien de file is gemaakt, dan is hij opgeslagen met de naam <{}>'.\
                format(outputFile))

        queryFile  = open(outputFile,mode='w',newline='')
        fileWriter = csv.writer(queryFile,dialect='excel',delimiter=';')

        # Save the expr_table results in a CSV file, including three header lines
        # Write the three header lines and then the file content from expr_table
        fileWriter.writerow(header1)
        fileWriter.writerow(expr_col_ids)
        fileWriter.writerow(header3)
        for expression in self.expr_table:
            fileWriter.writerow(expression)

        queryFile.close()
        self.Display_message(
            'File {} is saved.'.format(outputFile),
            'File {} is opgeslagen.'.format(outputFile))

        # Open written file in Excel
        open_file(outputFile)

    def Save_on_JSON_file(self):
        """ Saving query results in a JSON file in Gellish Expression Format."""
        subject_name = 'Query results'
        lang_name = 'Nederlands'
        serialization = 'json'
        Open_output_file(self.expr_table, subject_name, lang_name, serialization)

    def Define_and_display_kind_view(self):
        # Destroy earlier summary_frame
        try:
            self.kind_frame.destroy()
        except AttributeError:
            pass

        self.Define_kind_model_sheet()

        self.Display_kind_model_view()

    def Define_kind_model_sheet(self):
        ''' Kind_model View tab sheet for a kind in Notebook'''
        self.kind_frame  = Frame(self.views_noteb)
        self.kind_frame.grid (column=0, row=0,sticky=NSEW) #pack(fill=BOTH, expand=1)
        self.kind_frame.columnconfigure(0,weight=1)
        self.kind_frame.rowconfigure(0,weight=1)
        self.kind_frame.rowconfigure(1,weight=1)

        comp = ['Model of a kind','Model van een soort']
        self.views_noteb.add(self.kind_frame, text=comp[self.GUI_lang_index],sticky=NSEW)
        self.views_noteb.insert("end",self.kind_frame,sticky=NSEW)

        structure = ['Tree structure','Boomstructuur']

        kind_label = Label(self.kind_frame, text=structure[self.GUI_lang_index],justify='left')
        heads = ['uid_1','uid_2','uid-3','inFocus','Level1','Level2','Level3','kind',\
                'aspect','kAspect','>=<','value', 'UoM','status']
        display_heads = heads[3:]
        self.kind_tree = Treeview(self.kind_frame,columns=(heads), displaycolumns=display_heads,\
                                  selectmode='browse', height=30, padding=2)
        self.kind_treeHead = [('LineNr' ,'Object','','' ,'Kind' ,'Aspect','Kind of aspect',\
                               '>=<','Value' ,'UoM'    ,'Status'),\
                              ('RegelNr','Object','','','Soort','Aspect','Soort aspect'  ,\
                               '>=<','Waarde','Eenheid','Status')]
        col = -1
        for head_field in display_heads:
            col += + 1
            self.kind_tree.heading(head_field ,text=self.kind_treeHead[self.GUI_lang_index][col],\
                                   anchor=W)

        self.kind_tree.column ('#0'      ,minwidth=40,width=50)
        self.kind_tree.column ('inFocus' ,minwidth=10,width=10)
        self.kind_tree.column ('Level1'  ,minwidth=20,width=100)
        self.kind_tree.column ('Level2'  ,minwidth=20,width=50)
        self.kind_tree.column ('Level3'  ,minwidth=20,width=50)
        self.kind_tree.column ('kind'    ,minwidth=20,width=100)
        self.kind_tree.column ('aspect'  ,minwidth=20,width=100)
        self.kind_tree.column ('kAspect' ,minwidth=20,width=100)
        self.kind_tree.column ('>=<'     ,minwidth=20,width=20)
        self.kind_tree.column ('value'   ,minwidth=20,width=100)
        self.kind_tree.column ('UoM'     ,minwidth=20,width=50)
        self.kind_tree.column ('status'  ,minwidth=20,width=80)

        #self.kind_frame.grid  (column=0, row=3,sticky=EW)
        kind_label.grid       (column=0, row=0,sticky=EW)
        self.kind_tree.grid(column=0, row=1,sticky=NSEW)
        #self.kind_tree.grid(column=0, row=2,sticky=NSEW)

        self.kind_tree.columnconfigure(0,weight=1)
        self.kind_tree.columnconfigure(1,weight=1)
        self.kind_tree.columnconfigure(2,weight=1)
        self.kind_tree.columnconfigure(3,weight=1)
        self.kind_tree.columnconfigure(4,weight=1)
        self.kind_tree.columnconfigure(5,weight=1)
        self.kind_tree.columnconfigure(6,weight=1)
        self.kind_tree.columnconfigure(7,weight=1)
        self.kind_tree.columnconfigure(8,weight=1)
        self.kind_tree.columnconfigure(9,weight=1)
        self.kind_tree.columnconfigure(10,weight=1)
        self.kind_tree.columnconfigure(11,weight=1)

        self.kind_tree.columnconfigure(0,weight=1)
        self.kind_tree.rowconfigure(0,weight=1)
        self.kind_tree.rowconfigure(1,weight=1)

        kind_scroll = Scrollbar(self.kind_frame,orient=VERTICAL,command=self.kind_tree.yview)
        kind_scroll.grid (column=0,row=1,sticky=NS+E)
        self.kind_tree.config(yscrollcommand=kind_scroll.set)

        self.kind_tree.tag_configure('focus_tag', background='#9f9') # hell green
        self.kind_tree.tag_configure('head_tag', background='#bfb')
        self.kind_tree.tag_configure('val_tag', background='#dfd') # light green
        self.kind_tree.tag_configure('available', background='yellow')
        self.kind_tree.tag_configure('missing', background='#fcc') # red

        self.kind_tree.bind(sequence='<Double-1>', func=self.Kind_detail_view_left)
        self.kind_tree.bind(sequence='<Button-2>', func=self.Kind_detail_view_middle)
        self.kind_tree.bind(sequence='<Button-3>', func=self.Kind_detail_view_right)

    def Display_kind_model_view(self):
        ''' Kind_model Model view of a kind: Display prod_model in self.kind_tree:
            self.kind_tree.insert('',index=0,iid='UIDInFocus',values=[nameInFocus,kindDat],
            tags='focus_tag',open=True)
        '''
        unknownVal   = ['unknown value','onbekende waarde']
        unknownKind  = ['unknown kind' ,'onbekende soort']
        level0Part = ''
        level1Part = ''
        level2Part = ''

        for kindLine in self.kind_model:
            head = False
            head_line = []
            #print('kindLine:',kindLine)
            # If line_type == 1 then prepare header line for level 0 object
            # Note: line_type == 2 is skipped in this view
            if kindLine[3] == 1:
                head_line = kindLine[0:4]
                head_line.append(kindLine[5])
                head_line.append('')
                head_line.append('')
                head_line.append(kindLine[9])
                nameInFocus = head_line[4]
                level0Part = self.kind_tree.insert('', index='end', values=head_line,\
                                                   tags='focus_tag', open=True)
                previusPart = level0Part
            # In kind_treeview line_type 2 to 3 (indicated in kindLine[3])
            # are not displayed.
            elif kindLine[3] > 3:

                # Set value_tags at 'val_tag' or 'head_tag' for each field
                value_tags = 11*['val_tag']
                # If the line is a header line, then set value_tag to 'head_tag'
                if kindLine[4] in self.comp_head or kindLine[4] in self.occ_head or \
                   kindLine[4] in self.info_head or kindLine[8] in self.aspect_head or \
                   kindLine[5] in self.part_occ_head or kindLine[4] in self.subs_head:
                    head = True
                    value_tags = 11*['head_tag']
                # If the line is a value line (thus not a header line)
                # and there is a name of a part
                # then remember the part as a previous part
                elif kindLine[4] != '':
                    previusPart = level0Part
                elif kindLine[5] != '':
                    previusPart = level1Part
                elif kindLine[6] != '':
                    previusPart = level2Part

                # Set tag background color depending on value
                # If value is missing then bachgroumd color is yellow
                if kindLine[9] == '' or kindLine[9] in unknownVal:
                    value_tags[9] = 'missing'
                else:
                    value_tags[9] = 'available'
                if kindLine[7] in unknownVal:
                    value_tags[7] = 'missing'
                # Insert line
                #print('Value tags:', value_tags)
                id = self.kind_tree.insert(level0Part, index='end', values=kindLine,\
                                           tags=value_tags, open=True)

                # If the line is a header line, then continue to next line
                if head == True:
                    continue
                # If the line is a value line and there is a name of a part
                #    then remember the part as a previous part
                elif kindLine[4] != '':
                    level1Part = id
                    previusPart = level0Part
                elif kindLine[5] != '':
                    level2Part = id
                    previusPart = level1Part
                elif kindLine[6] != '':
                    previusPart = level2Part

    def Define_product_model_sheet(self):
        ''' Product_model view tab sheet in Notebook
            Preceded by a frame with a number of buttons corresponding with binds
        '''
        self.prod_frame = Frame(self.views_noteb)
        self.prod_frame.grid (column=0, row=0,sticky=NSEW, columnspan=6, rowspan=4)
        self.prod_frame.columnconfigure(0,weight=1)
        self.prod_frame.rowconfigure(0,weight=0)
        self.prod_frame.rowconfigure(1,weight=0)

        prod_text = ['Product model','Productmodel']
        self.views_noteb.add(self.prod_frame, text=prod_text[self.GUI_lang_index],sticky=NSEW)
        self.views_noteb.insert("end",self.prod_frame,sticky=NSEW)

        heads = ['uid_1','uid_2','uid-3','inFocus','Level1','Level2','Level3','kind',\
                'aspect','kAspect','>=<','value', 'UoM','status']
        display_heads = heads[5:]
        self.prod_tree = Treeview(self.prod_frame,columns=(heads), displaycolumns=display_heads, \
                                  selectmode='browse', height=30, padding=2)

        self.prod_tree.grid(column=0, row=1, columnspan=6, sticky=NSEW)

        self.prod_treeHead = [('','' ,'Kind' ,'Aspect','Kind of aspect',\
                               '>=<','Value' ,'UoM'    ,'Status'),\
                              ('','','Soort','Aspect','Soort aspect'  ,\
                               '>=<','Waarde','Eenheid','Status')]
        self.prod_tree.heading('#0' ,text='Object', anchor=W)
        col = -1
        for head_field in display_heads:
            col += + 1
            self.prod_tree.heading(head_field ,text=self.prod_treeHead[self.GUI_lang_index][col],\
                                   anchor=W)

        self.prod_tree.column ('#0'      ,minwidth=40,width=100)
        #self.prod_tree.column ('inFocus' ,minwidth=10,width=10)
        self.prod_tree.column ('Level1'  ,minwidth=20,width=100)
        self.prod_tree.column ('Level2'  ,minwidth=20,width=50)
        self.prod_tree.column ('Level3'  ,minwidth=20,width=50)
        self.prod_tree.column ('kind'    ,minwidth=20,width=100)
        self.prod_tree.column ('aspect'  ,minwidth=20,width=100)
        self.prod_tree.column ('kAspect' ,minwidth=20,width=100)
        self.prod_tree.column ('>=<'     ,minwidth=20,width=20)
        self.prod_tree.column ('value'   ,minwidth=20,width=100)
        self.prod_tree.column ('UoM'     ,minwidth=20,width=50)
        self.prod_tree.column ('status'  ,minwidth=20,width=80)

        self.prod_tree.columnconfigure(0,weight=1)
        self.prod_tree.columnconfigure(1,weight=1)
        self.prod_tree.columnconfigure(2,weight=1)
        self.prod_tree.columnconfigure(3,weight=1)
        self.prod_tree.columnconfigure(4,weight=1)
        self.prod_tree.columnconfigure(5,weight=1)
        self.prod_tree.columnconfigure(6,weight=1)
        self.prod_tree.columnconfigure(7,weight=1)
        self.prod_tree.columnconfigure(8,weight=1)
        self.prod_tree.columnconfigure(9,weight=1)
        self.prod_tree.columnconfigure(10,weight=1)
        self.prod_tree.columnconfigure(11,weight=1)

        self.prod_tree.columnconfigure(0,weight=1)
        self.prod_tree.rowconfigure(0,weight=1)
        self.prod_tree.rowconfigure(1,weight=1)

        prod_scroll = Scrollbar(self.prod_frame,orient=VERTICAL,command=self.prod_tree.yview)
        prod_scroll.grid (column=5,row=1,sticky=NS+E)
        self.prod_tree.config(yscrollcommand=prod_scroll.set)

        self.prod_tree.tag_configure('focus_tag', background='#9f9') # hell green
        self.prod_tree.tag_configure('head_tag', background='#bfb')
        self.prod_tree.tag_configure('val_tag', background='#dfd') # light green
        self.prod_tree.tag_configure('available', background='yellow')
        self.prod_tree.tag_configure('missing', background='#fcc') # red

        self.prod_tree.bind(sequence='<Double-1>', func=self.Prod_detail_view_left)
        self.prod_tree.bind(sequence='<Button-2>', func=self.Prod_detail_view_middle)
        self.prod_tree.bind(sequence='<Button-3>', func=self.Prod_detail_view_right)
        self.prod_tree.bind(sequence='c'         , func=self.Prod_detail_view_middle)

    def Display_product_model_view(self):
        ''' Product Model view: Display prod_model in self.prod_tree:
            self.prod_tree.insert('',index=0,iid='UIDInFocus',values=[nameInFocus,kindDat],
            tags='focus_tag',open=True)
        '''
        unknownVal   = ['unknown value','onbekende waarde']
        unknownKind  = ['unknown kind' ,'onbekende soort']
        further_part = ['Further part' ,'Verder deel']
        kind_of_part = ['Kind of part', 'Soort deel']
        possible_roles = False # No roles expected
        level0Part = ''
        level1Part = ''
        level2Part = ''

        for prod_line_0 in self.prod_model:
            prod_line = prod_line_0[:]
            head = False
            head_line = []
            #print('Prod_line:',prod_line)
            # If line_type (prod_line[3]) == 1
            # then prepare header line from prod_line for level 0 object
            # Note: line_type == 2 and 3 are skipped in this view
            if prod_line[3] == 1:
                head_line = prod_line[0:4]
                head_line.append(prod_line[5])
                head_line.append('')
                head_line.append('')
                head_line.append(prod_line[9])
                nameInFocus = head_line[4]
                #print('Head_line:',head_line)
                level0Part = self.prod_tree.insert('', index='end', values=head_line,
                                                   text=nameInFocus, tags='focus_tag', open=True)
                previusPart = level0Part
            # If line_type (prod_line[3]) == 4
            # then prepare header line from prod_line for level 0 object
            # Note: line_type == 1, 2 and 3 are skipped in this view
            if prod_line[3] == 4:
                #nameInFocus = prod_line[5]
                prod_name = prod_line[4]
                level0Part = self.prod_tree.insert('', index='end', values=prod_line,\
                                                   text=prod_name, tags='focus_tag',open=True)
                previusPart = level0Part

            # In prod_tree view line_type 2 to 3 (indicated in prod_line[3]) are not displayed.
            elif prod_line[3] > 4:
                # Set value_tags at 'val_tag' or 'head_tag' for each field
                value_tags = 11*['val_tag']

                # If the line is a header line, then set value_tag to 'head_tag'
                if prod_line[4] in self.comp_head or prod_line[4] in self.occ_head or \
                   prod_line[4] in self.info_head or prod_line[8] in self.aspect_head or \
                   prod_line[5] in self.part_occ_head or prod_line[4] in self.subs_head:
                    head = True
                    value_tags = 11*['head_tag']
                    prod_name = prod_line[4]
                    # Determine whether roles may appear in prod_line[4]
                    # in lines following the header line
                    # to avoid that they are included in the indented hierarchy
                    if prod_line[4] in self.occ_head:
                        possible_roles = True
                    elif prod_line[5] in self.part_occ_head:
                        possible_roles = False
                    # Remove header texts 'Further part' and 'Kind of part'
                    if prod_line[6] in further_part:
                        prod_line[6] = ''
                    if prod_line[7] in kind_of_part:
                        continue #prod_line[7] = ''

                # If the line is a value line (thus not a header line)
                # and there is a name of a part
                # then remember the part as a previous part
                elif prod_line[4] != '':
                    previusPart = level0Part
                    prod_name = prod_line[4]
                elif prod_line[5] != '':
                    previusPart = level1Part
                    prod_name = prod_line[5]
                elif prod_line[6] != '':
                    previusPart = level2Part
                    prod_name = prod_line[6]

                # Set tag background color depending on value
                # If value is missing then bachgroumd color is yellow
                if prod_line[9] == '' or prod_line[9] in unknownVal:
                    value_tags[9] = 'missing'
                else:
                    value_tags[9] = 'available'
                if prod_line[7] in unknownVal:
                    value_tags[7] = 'missing'

                if possible_roles == True and prod_line[4] == '':
                    prod_name = ''
##                elif possible_roles == False and prod_line[5] != '':
##                    prod_line[5] = ''

                # Insert line
                #print('Values:', prod_line[1], type(prod_line[1]))
                id = self.prod_tree.insert(previusPart, index='end', values=prod_line,\
                                           text=prod_name, tags=value_tags, open=True)

                # If the line is a header line, then continue to next line
                if head == True:
                    continue
                # If the line is a value line and the there is a name of a part
                #   then remember the part as a previous part
                elif prod_line[4] != '':
                    level1Part = id
                    previusPart = level0Part
                elif prod_line[5] != '':
                    level2Part = id
                    previusPart = level1Part
                elif prod_line[6] != '':
                    previusPart = level2Part

    def Define_data_sheet(self):
        # Define ProductView tab in Notebook = = = = = = = = = = = = = = = = = = =
        # Product_sheet is canvas for scrollbar
        self.data_sheet = Frame(self.views_noteb)
        self.data_sheet.grid (column=0, row=0,sticky=NSEW) #pack(fill=BOTH, expand=1)
        self.data_sheet.columnconfigure(0,weight=1)
        self.data_sheet.rowconfigure(0,weight=0)
        #self.data_sheet.rowconfigure(1,weight=0)
        prodText = ['Data sheet', 'Data sheet']
        self.views_noteb.add(self.data_sheet, text=prodText[self.GUI_lang_index], sticky=NSEW)
        self.views_noteb.insert("end",self.data_sheet,sticky=NSEW)

        data_canvas = Canvas(self.data_sheet, background='#ddf')
        #data_canvas.pack()
        data_canvas.grid(column=0,row=0,sticky=NSEW)
        #data_canvas.bind('<Button-2>', RightMouseButton)
        data_canvas.columnconfigure(0,weight=1)
        data_canvas.rowconfigure(0,weight=0)

        self.data_frame = Frame(data_canvas)
        self.data_frame.grid(column=0,row=0,sticky=NSEW)

        self.data_frame.columnconfigure(0,weight=1)
        self.data_frame.columnconfigure(1,weight=1)
        self.data_frame.columnconfigure(2,weight=1)
        self.data_frame.columnconfigure(3,weight=1)
        self.data_frame.columnconfigure(4,weight=1)
        self.data_frame.columnconfigure(5,weight=1)
        self.data_frame.columnconfigure(6,weight=1)
        self.data_frame.columnconfigure(7,weight=1)
        self.data_frame.columnconfigure(8,weight=1)
        self.data_frame.columnconfigure(9,weight=1)
        self.data_frame.columnconfigure(10,weight=1)
        self.data_frame.rowconfigure(0,weight=0)
        self.data_frame.rowconfigure(1,weight=0)

        data_scroll = Scrollbar(self.data_sheet,orient=VERTICAL,command=data_canvas.yview)
        data_scroll.grid(column=0, row=0, sticky=NS+E)
        data_canvas.config(yscrollcommand=data_scroll.set)

    def Display_data_sheet_view(self):
        ''' Produce a view of a product model in the form of a datasheet'''
        unknownVal   = ['unknown value','onbekende waarde']
        unknownKind  = ['unknown kind' ,'onbekende soort', 'anything', 'iets']

        # Set column widths in data sheet
        col_width = [4,20,10,10,20,15,20,4,10,5,10]
        line_nr = -1
        for prod_row in self.prod_model:
            line = prod_row[3:]
            line_nr += + 1
            column_nr  = -1
            head = False
            header1 = False
            header2 = False
            header3 = False
            body    = False
            back = 'white'
            fore = 'black'
            for field_value in line:
                column_nr += + 1
                fieldStr = StringVar()
                span = 1
                column_width = col_width[column_nr]

                # Detect start of header line 1:
                # Field_value 1 in column 0 means line_type_1 and header_1
                if column_nr == 0 and field_value == 1:
                    header1 = True
                if header1 == True:
                    if column_nr == 2: span=3
                    elif column_nr == 6: span=5

                # Display on line 1 the line nr, 'Product form' label and the 'kind' label
                if header1 == True and column_nr in [0, 1, 5]:
                    back = '#dfb' # light green
                    fd = ttk.Label(self.data_frame, text=field_value, width=column_width, \
                                   justify='left', background=back, foreground=fore)\
                                   .grid(row=line_nr, column=column_nr, columnspan=span, sticky=EW)

                # Display on line 1 the product_name and kind_name (with another background color)
                if header1 == True and column_nr in [2, 6]:
                    back = 'white'
                    fore = 'black'
                    fd = ttk.Label(self.data_frame, text=field_value, width=column_width, \
                                   background=back, foreground=fore, borderwidth=0)\
                                   .grid(row=line_nr, column=column_nr, columnspan=span, sticky=EW)

                # Detect start of header line 2: Value 2 in column 0 means line_type2 and header2
                if column_nr == 0 and field_value == 2:
                    header2 = True

                # Display on line 2 the description text
                if header2 == True and column_nr == 3:
                    span = 8
                    back = 'white'
                    fore = 'black'
                    fd = ttk.Label(self.data_frame, text=field_value, width=column_width, \
                                   justify='left', background=back, foreground=fore)\
                                   .grid(row=line_nr, column=column_nr, columnspan=span, \
                                         rowspan=2, sticky=EW)
                # Display on line 2 the description label
                if header2 == True and column_nr in range(0,3):
                    back = '#dfb'
                    fd = ttk.Label(self.data_frame, text=field_value, width=column_width, \
                                   justify='left', background=back, foreground=fore)\
                                   .grid(row=line_nr, column=column_nr, columnspan=span, \
                                         rowspan=2, sticky=EW)

                # Detect start of header line 3:
                # Value 3 in column 0 means line_type3 and header3
                if column_nr == 0 and field_value == 3:
                    header3 = True
                    line_nr += + 1

                # Display the line 3 subsequent values
                if header3 == True:
                    back = '#dfb'
                    fd = ttk.Label(self.data_frame, text=field_value, width=column_width, \
                                   justify="center", background=back, foreground=fore)\
                                   .grid(row=line_nr, column=column_nr, columnspan=span, \
                                         sticky=EW)

                # Detect start of body values: Value >3 in column 0 means body of values
                if column_nr == 0 and field_value > 3:
                    body = True
                # Display the subsequent body values on line type > 3
                if body == True:
                    # Set background color
                    # depending on either header, value present or 'unknown'
                    if (column_nr == 1 and (field_value in self.comp_head \
                                            or field_value in self.occ_head \
                                            or field_value in self.info_head)) \
                        or (column_nr == 2 and (field_value in self.part_occ_head)):
                        # Header line detected; set background color accordingly
                        head = True
                        back = '#dfb'
                    if column_nr == 8 and field_value != '':
                        back = 'yellow'
                    elif head != True:
                        back = 'white'
                    if field_value in unknownVal:
                        field_value = unknownVal[self.GUI_lang_index]
                        back = '#fcc'
                    elif field_value in unknownKind:
                        field_value = unknownKind[self.GUI_lang_index]
                        back = '#fcc'
                    # Display subsequent body values
                    fd = ttk.Label(self.data_frame, text=field_value, width=column_width, \
                                   background=back, foreground=fore,\
                                   wraplength=200, borderwidth=0, relief='ridge')\
                                   .grid(row=line_nr, column=column_nr, columnspan=span, \
                                         sticky=EW)

    def Define_activity_sheet(self):
        activity = ['Activities','Activiteiten']
        self.act_frame = Frame(self.views_noteb)
        self.act_frame.grid (column=0, row=0,sticky=NSEW) #pack(fill=BOTH, expand=1)
        self.act_frame.columnconfigure(0,weight=1)
        self.act_frame.rowconfigure(0,weight=0)
        self.act_frame.rowconfigure(1,weight=0)
        self.views_noteb.add(self.act_frame, text=activity[self.GUI_lang_index], sticky=NSEW)
        self.views_noteb.insert("end",self.act_frame,sticky=NSEW)
##        acts = ['Activity tree', 'Activiteitenboom']
##        actLbl = Label(self.act_frame,text=acts[self.GUI_lang_index])
        headings = ['OccUID', 'OccName' , 'WholeOccName', 'InvolvUID', 'KindOccUID',
                    'OccName','PartName', 'Involved'    , 'Kind'     , 'Role']
        display_cols = headings[7:]
        self.act_tree = Treeview(self.act_frame, columns=(headings),\
                               displaycolumns=display_cols,
                               selectmode='browse',height=30)

        occText  = ['Occurrence'     ,'Gebeurtenis']
        partText = ['Part occurrence','Deelgebeurtenis']
        strText  = ['Involved object','Betrokken object']
        kindText = ['Kind'           ,'Soort']
        roleText = ['Role'           ,'Rol']
        self.act_tree.heading('#0'      ,text=occText[self.GUI_lang_index] ,anchor=W)
        self.act_tree.heading('OccName' ,text=occText[self.GUI_lang_index] ,anchor=W)
        self.act_tree.heading('PartName',text=partText[self.GUI_lang_index],anchor=W)
        self.act_tree.heading('Involved',text=strText[self.GUI_lang_index] ,anchor=W)
        self.act_tree.heading('Kind'    ,text=kindText[self.GUI_lang_index],anchor=W)
        self.act_tree.heading('Role'    ,text=roleText[self.GUI_lang_index],anchor=W)

        self.act_tree.column('#0'       ,minwidth=20,width=20)
        self.act_tree.column('OccName'  ,minwidth=20,width=120)
        self.act_tree.column('PartName' ,minwidth=20,width=80)
        self.act_tree.column('Involved' ,minwidth=20,width=80)
        self.act_tree.column('Kind'     ,minwidth=20,width=60)
        self.act_tree.column('Role'     ,minwidth=20,width=60)

        #actLbl.grid (column=0,row=0,sticky=EW)
        self.act_tree.grid(column=0,row=1,sticky=NSEW)

        self.act_tree.columnconfigure(0,weight=0)
        self.act_tree.columnconfigure(1,weight=1)
        self.act_tree.columnconfigure(2,weight=1)
        self.act_tree.columnconfigure(3,weight=1)
        self.act_tree.columnconfigure(4,weight=1)
        self.act_tree.columnconfigure(5,weight=1)
##        self.act_tree.columnconfigure(6,weight=1)
##        self.act_tree.columnconfigure(7,weight=1)
##        self.act_tree.columnconfigure(8,weight=1)
        self.act_tree.rowconfigure(0,weight=0)
        self.act_tree.rowconfigure(1,weight=1)

        self.act_tree.tag_configure('uom_tag', option=None, background='#ccf')
        self.act_tree.tag_configure('actTag', option=None, background='#dfd')

        actScroll = Scrollbar(self.act_frame,orient=VERTICAL,command=self.act_tree.yview)
        actScroll.grid (column=0,row=1,sticky=NS+E)
        self.act_tree.config(yscrollcommand=actScroll.set)


    def Display_occ_model_view(self):
        ''' Display activities and occurrences in self.act_tree
            Followed by a display of IDEF0 diagram(s)
        '''

        self.act_tree.tag_configure('head_tag', option=None, background='#dfd')
        if len(self.occ_model) > 0:
            self.top_occurrences = []
            for occ_line in self.occ_model:
                #print('==OccTree:',occ_line)
                # If higher part (occ_linen[2]) is blank
                # then occ_line[0] contains top occ_UID
                if occ_line[2] == '':
                    top_occ = self.uid_dict[occ_line[0]]
                    self.top_occurrences.append(top_occ)
                level  = 0
                # Display self.act_tree line
                self.Display_occurrence_tree(occ_line, level) #,wholes

            # IDEF0: Display drawings of occurrences
            diagram = Occurrences_diagram(self.user_interface, self.gel_net)
            diagram.Create_occurrences_diagram(self.top_occurrences)

    def Display_occurrence_tree(self, occ_line, level):
        """ Display occurrences compositions with inputs and outputs and roles.
            occ_line = line in occ_model
            occ_model.append([occ.uid, occ.name, higher.name, involv.uid, \
                              kind_occ.uid,\
                              occ.name, part_occ.name, involv.name, \
                              kind_part_occ.name, role_of_involved])
            involv_table: occ, involved, inv_role_kind, inv_kind_name
        """
        #print('Occ_line:', occ_line)

        self.act_tree.tag_configure('occTag', option=None, background='#ddf')
        self.act_tree.tag_configure('ioTag' , option=None, background='#eef')
        space = ''

        # Display the occurrence
        id = self.act_tree.insert(occ_line[2], index='end', values=(occ_line),
                                  iid=occ_line[1], text=occ_line[1], tags='occTag' , open=True)

        # Find and display its inputs and outputs
        # involv_table = occ, involved_obj, inv_role_kind, inv_kind_name
        for io_objects in self.involv_table:
            io_line = ['','','','','','','', io_objects[1].name, io_objects[3], io_objects[2].name]
            #print('involv-line:', occ_line[1], io_objects[0].uid, io_objects[1].uid, io_line)
            # If uid of occurrence == uid of object
            # that has inputs or outputs then display io_line
            if occ_line[0] == io_objects[0].uid:
                self.act_tree.insert(id, index='end', values=(io_line), tags='ioTag' , open=True)
        level = 1
##        for whole_occ, part_occ, part_kind_occ in self.part_whole_occs:
##            # For each part of occurrence call Display_occurrence_tree recursively
##            # If uid of occurrence == uid whole then there is a part
##            if occ_line[0] == whole_part[0].uid:
##                print('part in part_whole_occs:', whole_occ.name, part_occ.name,
##                      part_kind_occ.name)
##                self.Display_occurrence_tree(whole_part, level)

    def Define_and_display_documents(self):
        # Destroy earlier documents sheet
        try:
            self.doc_frame.destroy()
        except AttributeError:
            pass

        self.Define_documents_sheet()

        # Documents: Display documents and files for selection for display
        for info_line in self.info_model:
            self.doc_tree.insert('',index='end',values=info_line,tags='docTag')

    def Define_documents_sheet(self):
        documents = ['Documents','Documenten']
        self.doc_frame = Frame(self.views_noteb)
        self.doc_frame.grid (column=0, row=0,sticky=NSEW) #pack(fill=BOTH, expand=1)
        self.doc_frame.columnconfigure(0,weight=1)
        self.doc_frame.rowconfigure(0,weight=0)
        self.views_noteb.add(self.doc_frame, text=documents[self.GUI_lang_index], sticky=NSEW)
        self.views_noteb.insert("end",self.doc_frame,sticky=NSEW)
        headings = ['info','obj','carrier','directory','infoName','infoKind', 'dirName',\
                    'objName','fileName','fileKind']
        display_cols = headings[4:]
        self.doc_tree = Treeview(self.doc_frame, columns=(headings),\
                                 displaycolumns=display_cols, selectmode='browse', height=30)
        self.doc_tree.heading('info' ,text='info'    ,anchor=W)
        self.doc_tree.heading('obj'  ,text='obj'     ,anchor=W)
        self.doc_tree.heading('carrier'  ,text='carrier'   ,anchor=W)
        self.doc_tree.heading('directory',text='directory' ,anchor=W)
        self.doc_tree.heading('infoName' ,text='Document'  ,anchor=W)
        self.doc_tree.heading('infoKind' ,text='Doc type'  ,anchor=W)
        self.doc_tree.heading('dirName'  ,text='Directory'  ,anchor=W)
        self.doc_tree.heading('objName'  ,text='about Object' ,anchor=W)
        self.doc_tree.heading('fileName' ,text='File name' ,anchor=W)
        self.doc_tree.heading('fileKind' ,text='File type' ,anchor=W)

        self.doc_tree.column('#0'        ,minwidth=10,width=10)
        self.doc_tree.column('infoName'  ,minwidth=100,width=150)
        self.doc_tree.column('infoKind'  ,minwidth=100,width=150)
        self.doc_tree.column('dirName'   ,minwidth=100,width=150)
        self.doc_tree.column('objName'   ,minwidth=100,width=150)
        self.doc_tree.column('fileName'  ,minwidth=100,width=150)
        self.doc_tree.column('fileKind'  ,minwidth=100,width=150)

        self.doc_tree.grid(column=0,row=0,sticky=NSEW)

        self.doc_tree.columnconfigure(0,weight=1)
        self.doc_tree.rowconfigure(0,weight=0)

        self.doc_tree.tag_configure('docTag', option=None, background='#cfc')

        docScroll = Scrollbar(self.doc_frame,orient=VERTICAL,command=self.doc_tree.yview)
        docScroll.grid (column=0,row=0,sticky=NS+E)
        self.doc_tree.config(yscrollcommand=docScroll.set)

        self.doc_tree.bind(sequence='<Double-1>', func=self.Doc_detail_view)
        self.doc_tree.bind(sequence='<Button-3>', func=self.Doc_detail_view)

#------------------------------------------------------------------------
    def Expr_detail_view(self, sel):
        """ Find the selected object from a user selection
            in the expr_table that is displayed in the expr_tree view."""

        cur_item = self.expr_tree.focus()
        item_dict = self.expr_tree.item(cur_item)
        values = list(item_dict['values'])

        selected_obj = self.uid_dict[str(values[lh_uid_col])]
        self.Display_message(
            'Display product details of: {}'.format(selected_obj.name),
            'Weergave van productdetails van: {}'.format(selected_obj.name))

        if selected_obj.category in ['kind', 'kind of physical object', \
                                     'kind of occurrence', 'kind of aspect', \
                                     'kind of role', 'kind of relation']:
            self.Define_and_display_kind_detail_view(selected_obj)
        else:
            self.Define_and_display_individual_detail_view(selected_obj)

#------------------------------------------------------------------------
    def Prepare_lh_object_network_view(self):
        ''' Set the uid of the left hand object in a selected treeview row
            as the chosen object
            for display of a new network view and other views.
        '''
        tree_values = self.Determine_network_tree_values()
        if len(tree_values) > 0:
            chosen_object_uid = str(tree_values[0])
            # Build single product model (list with one element)
            obj_list = []
            obj = self.uid_dict[chosen_object_uid]
            obj_list.append(obj)
            self.Build_product_views(obj_list)
            # Display query results in notebook sheets
            self.Display_notebook_views()

    def Prepare_network_object_detail_view(self, lh_or_rh):
        ''' Set the uid of the left hand or right hand object
            in a selected network treeview row
            as the chosen object for display of details
        '''
        tree_values = self.Determine_network_tree_values()
        if len(tree_values) > 0 and lh_or_rh == 'lh_obj':
            chosen_object_uid = tree_values[0]
            self.Determine_category_of_object_view(chosen_object_uid, tree_values)
        elif len(tree_values) > 4 and lh_or_rh == 'rh_obj':
            chosen_object_uid = tree_values[4]
            self.Determine_category_of_object_view(chosen_object_uid, tree_values)

    def Prepare_for_classification(self):
            #similar to def Prod_detail_view_middle(self, sel):
        """ Find the selected left classifier object from a user selection
            in the network that is displayed in the network_tree view.
            When the classification button was used the taxonomy of the selected kind
            is displayed and a search for a second classifier in the taxonomy
            (the subtype hierarchy of the selected kind) is started.
            The aspects of the individual object are used to create selection criteria for the
            subtypes in the hierarchy.
            The taxonomy of the selected kind is displayed for selection of the classifier.
        """
        tree_values = self.Determine_network_tree_values()

        if len(tree_values) > 0:
            if tree_values[4] == '' or tree_values[4] == 'unknown':
                self.Display_message(
                    'Classifying kind of object is unknown.',\
                    'Classificerende soort object is onbekend.')
            else:
                kind_uid = str(tree_values[4])
                individual_object_uid = str(tree_values[0])
                self.Classification_of_individual_thing(individual_object_uid, kind_uid)
        else:
            self.Display_message(
                'Select an item, then click the classification button for classying the object.',
                'Selecteer een object, click dan op de classifikatieknop '
                'om het object te classificeren')

    def Classification_of_individual_thing(self, to_be_classified_object_uid, kind_uid):
        ''' Start a classification process for a to be classified object
            by a subtype of a current classifying kind.
            When completed, a classification relation is added to the classified object.
        '''
        self.modification = 'classification started'
        kind = self.uid_dict[kind_uid]
        self.modified_object = self.uid_dict[to_be_classified_object_uid]
        self.Display_message(
            'Present the taxonomy of the kind <{}> that classifies <{}> '
            'for selection of a subtype that classifies the object'.\
            format(kind.name, self.modified_object.name),
            'Presenteer de taxonomie van de soort <{}> die classificeerder is van <{}> '
            'voor het selecteren van een subtype die het object classificeert'.\
            format(kind.name, self.modified_object.name))

        # Formulate query_spec including conditions from aspects of individual, if any
        self.user_interface.query.Formulate_query_spec_from_individual(kind)
        self.user_interface.query.Create_query_file()
        self.user_interface.query.Interpret_query_spec()

        obj_list = []
        obj_list.append(kind)
        self.Build_product_views(obj_list)
        # Display taxonomy in taxon view
        self.Define_and_display_taxonomy_of_kinds()
        # Display possibilities of kind in possibilities view
        self.Define_and_display_possibilities_of_kind()

        if len(self.info_model) > 0:
            self.Define_and_display_documents()

    def Network_object_detail_view(self, sel):
        """ Find the selected left hand object from a user selection with left button
            in the network_model that is displayed in the network_tree view.
        """
        tree_values = self.Determine_network_tree_values()
        #print('Network object detail view:', cur_item, tree_values)
        if len(tree_values) > 0:
            if sel.num == 1:
                chosen_object_uid = tree_values[0]
            else:
                chosen_object_uid = tree_values[4]
            self.Determine_category_of_object_view(chosen_object_uid, tree_values)

    def Determine_network_tree_values(self):
        ''' Determine the values on a selected focus row in a network treeview
        '''
        cur_item = self.network_tree.focus()
        tree_values = []
        if cur_item != '':
            item_dict = self.network_tree.item(cur_item)
            tree_values = list(item_dict['values'])
        else:
            self.Display_message(
                'No item in focus. Fist select a row, then click a button.',\
                'Geen object gevonden. Selecteer eerst een rij, click daarna op een knop.')
        return tree_values

    def Determine_category_of_object_view(self, chosen_object_uid, tree_values):
        ''' Determine kind of chosen object and as a consequence models and views
        '''
        description_text = ['description', 'beschrijving']
        obj_descr_title  = ['Information about ', 'Informatie over ']

        if chosen_object_uid != '':
            selected_obj   = self.uid_dict[str(chosen_object_uid)]

            # If info_kind is a description then display the destription in messagebox
            if len(tree_values) > 8 and tree_values[8] in description_text:
##                self.Display_message(
##                    'The information {} is not presented on an information carrier '
##                    'but reads as follows:\n   {}'.\
##                    format(tree_values[5], selected_obj.description),\
##                    'De informatie {} is niet aanwezig op een informatiedrager '
##                    'maar luidt als volgt:\n   {}'.\
##                    format(tree_values[5], selected_obj.description))
                messagebox.showinfo(obj_descr_title[self.GUI_lang_index] + selected_obj.name,\
                                    selected_obj.description)
            else:
                self.Display_message(
                    'Display object details of: {}'.format(selected_obj.name),
                    'Weergave van objectdetails van: {}'.format(selected_obj.name))
                if selected_obj.category in self.gel_net.categories_of_kinds:
                    self.Define_and_display_kind_detail_view(selected_obj)
                else:
                    self.Define_and_display_individual_detail_view(selected_obj)

            if len(self.info_model) > 0:
                self.Define_and_display_documents()

#------------------------------------------------------------------------
    def Kind_detail_view_left(self, sel):
        """ Find the selected left hand object from a user selection with left button
            in the kind_table that is displayed in the kind_tree view."""
        description_text = ['description', 'beschrijving']
        obj_descr_title  = ['Information about ', 'Informatie over ']
        cur_item = self.kind_tree.focus()
        item_dict = self.kind_tree.item(cur_item)
        tree_values = list(item_dict['values'])
        #print('Kind_detail_left:', cur_item, tree_values) #[0], tree_values[1], tree_values[2:]
        selected_obj   = self.uid_dict[str(tree_values[0])]

        # If info_kind is a description then display the destription in messagebox
        if tree_values[7] in description_text:
##            self.Display_message(
##                'The information {} is not presented on a carrier '
##                'but is as follows:\n   {}'.\
##                format(tree_values[4], selected_obj.description),\
##                'De informatie {} is niet aanwezig op een informatiedrager '
##                'maar luidt als volgt:\n   {}'.\
##                format(tree_values[4], selected_obj.description))
            messagebox.showinfo(obj_descr_title[self.GUI_lang_index] + selected_obj.name, \
                                selected_obj.description)
        else:
            print('Display kind details of: {}'.format(selected_obj.name))
            self.Define_and_display_kind_detail_view(selected_obj)
            if len(self.info_model) > 0:
                self.Define_and_display_documents()

#------------------------------------------------------------------------
    def Kind_detail_view_middle(self, sel):
        """ Find the selected left supertype object from a user selection with middle button
            in the kind_table that is displayed in the kind_tree view.
            Then display its taxonomy
        """

        cur_item = self.kind_tree.focus()
        item_dict = self.kind_tree.item(cur_item)
        tree_values = list(item_dict['values'])
        #print('Comp_detail_middle:', sel.type, sel.keysym, cur_item, tree_values)

        if len(tree_values) > 0:
            if tree_values[1] > 0:
                selected_obj   = self.uid_dict[str(tree_values[1])]

                # Save sel.type being either 'ButtonPress' or 'KeyPress' with sel.keysym = 'c'
                self.sel_type = sel.type

                self.Display_message(
                    'Display the taxonomy of: {}'.format(selected_obj.name),
                    'Weergave van de taxonomie van: {}'.format(selected_obj.name))
                obj_list = []
                obj_list.append(selected_obj)
                self.Build_product_views(obj_list)
                # Display taxonomy of selected kind
                self.Define_and_display_taxonomy_of_kinds()
                if len(self.info_model) > 0:
                    self.Define_and_display_documents()
            else:
                self.Display_message(
                    'The classifying kind of the object is unknown.',\
                    'De classificerende soort van het object is onbekend.')
        else:
            self.Display_message(
                'Select a line before clicking the second mouse button.',\
                'Selecteer een regel voor het clicken van de twee knop op de muis.')

#------------------------------------------------------------------------
    def Kind_detail_view_right(self, sel):
        """ Find the selected kind of aspect or file from a user selection with right button
            in the kind_table that is displayed in the kind_tree view."""

        cur_item  = self.kind_tree.focus()
        if cur_item == '':
            self.Display_message(
                'No item is selected. '
                '\nFirst select a line with a single left mouse button click, '
                '\nthen click the right mouse button.',\
                'Er is geen object geselecteerd. '
                '\nSelecteer eerst een regel met een enkele lenker muisclick '
                '\nclick daarna de rechter muisknop.')
            return
        item_dict = self.kind_tree.item(cur_item)
        tree_values = list(item_dict['values'])
        #print('Kind_detail_right:',cur_item, tree_values)

        if len(tree_values) > 8:
            # If tree_values[8] contains a dot (.)
            # then it is interpreted as a file.name with file extension,
            # else it is interpreted as a selected kind of aspect name
            parts = tree_values[8].rsplit('.', maxsplit=1)
            if len(parts) == 1:
                self.Display_message(
                    'The name <{}> does not contain a file extension, although expected. '
                    'The name is now interpreted as a kind of aspect.'.\
                    format(tree_values[8]),\
                    'De naam <{}> bevat geen file extensie, hoewel dat wel verwacht wordt. '
                    'Die naam is nu geïnterpreteerd als een soort aspect.'.\
                    format(tree_values[8]))
                selected_obj = tree_values[2]
                self.Display_message(
                    'Display the aspect details of: {}'.format(selected_obj.name),\
                    'Weergave van de aspectdetails van: {}'.format(selected_obj.name))
                # Display taxonomy of selected kind
                self.Define_and_display_taxonomy_of_kinds()
            else:
                # Open the file in the file format that is defined by its file extension
                # from directory+file_name
                file_path = os.path.join(tree_values[5], tree_values[8])
                normalized_path = os.path.normpath(file_path)
                open_file(normalized_path)
        else:
            self.Display_message(
                'There is no right hand object found to be displayed.',\
                'Er is geen rechter object gevonden om weergegeven te worden.')
#------------------------------------------------------------------------
    def Prod_detail_view_left(self, sel):
        self.Prod_detail_view_left_button()

    def Prod_detail_view_left_button(self):
        """ Find the selected left hand individual object
            from a user selection with left button
            in the prod_table that is displayed in the prod_tree view.
        """
        description_text = ['description', 'beschrijving']
        obj_descr_title  = ['Information about ', 'Informatie over ']
        cur_item = self.prod_tree.focus()
        item_dict = self.prod_tree.item(cur_item)
        tree_values = list(item_dict['values'])
        #print('Prod_detail_left:', cur_item, tree_values)
        if len(tree_values) > 0:
            if tree_values[0] != '':
                selected_obj = self.uid_dict[str(tree_values[0])]

                # If info_kind is a description
                # then display the destription in messagebox
                if tree_values[7] in description_text:
##                    self.Display_message(
##                        'The information {} is not presented on an information carrier '
##                        'but reads as follows:\n {}'.\
##                        format(tree_values[4], selected_obj.description),\
##                        'De informatie {} is niet aanwezig op een informatiedrager '
##                        'maar luidt als volgt:\n {}'.\
##                        format(tree_values[4], selected_obj.description))
                    messagebox.showinfo(obj_descr_title[self.GUI_lang_index] + selected_obj.name,\
                                        selected_obj.description)
                else:
                    self.Display_message(
                        'Display of product details of: {}'.format(selected_obj.name),\
                        'Weergave van de productdetails van: {}'.format(selected_obj.name))
                    self.Define_and_display_individual_detail_view(selected_obj)

                if len(self.info_model) > 0:
                    self.Define_and_display_documents()

#------------------------------------------------------------------------
    def Prod_detail_view_middle(self, sel):
        """ Find the selected left classifier object from a user selection
            in the prod_table that is displayed in the prod_tree view.
            When the middle mouse button was used
            the taxonomy of the selected kind is displayed.
            When the 'c' key was used a search for a second classifier in the taxonomy
            (the subtype hierarchy of the selected kind) is started.
            The aspects of the individual object are used to create selection criteria
            for the subtypes in the hierarchy.
            The taxonomy of the selected kind is displayed for selection of the classifier.
        """

        cur_item = self.prod_tree.focus()
        item_dict = self.prod_tree.item(cur_item)
        tree_values = list(item_dict['values'])
        #print('Prod_detail_middle:', sel.type, sel.keysym, cur_item, tree_values, type(tree_values[1]))

        if len(tree_values) > 0:
            kind_uid = str(tree_values[1])
            individual_object_uid = str(tree_values[0])
            if kind_uid != '':
                # Verify sel.type being either 'Button-2 Press' for display of taxonomy
                # or 'KeyPress' with sel.keysym = 'c'
                # (for display for classification by selection of subtype)
                #print('sel.type', sel.type, sel.keysym, sel.char)
                if sel.keysym == 'c':
                    # Perform a classification process by display the taxonomy of kind
                    # and selection of one of its subtypes
                    self.Classification_of_individual_thing(individual_object_uid, kind_uid)
                else:
                    # Mouse Button-2 Press: Build views for selected kind and display views
                    self.Display_message(
                        'Display taxonomy and possibilities of kind: {}'.\
                        format(selected_obj.name),\
                        'Weergave van de taxonomie en mogelijkheden van soort: {}'.\
                        format(selected_obj.name))
                    obj_list = []
                    obj_list.append(selected_obj)
                    self.Build_product_views(obj_list)
                    # Display taxonomy in taxon view
                    self.Define_and_display_taxonomy_of_kinds()
                    # Display possibilities of kind in possibilities view
                    self.Define_and_display_possibilities_of_kind()

                    if len(self.info_model) > 0:
                        self.Define_and_display_documents()
            else:
                self.Display_message(
                    'The kind of object is unknown.',
                    'De soort object is onbekend.')
        else:
            self.Display_message(
                "Select an item, then click the classification button "
                "or the second mouse button or press 'c' key "
                "for classying the object.",\
                "Selecteer een regel, click dan de classifikatieknop "
                "of click met de tweede muisknop of kies de 'c' toets "
                "voor het classificeren van het object.")

    def Prod_detail_view_right(self, sel):
        """ Find the selected aspect or file from a user selection with right button
            in the prod_table that is displayed in the prod_tree view."""

        cur_item  = self.prod_tree.focus()
        if cur_item == '':
            self.Display_message(
                'No item selected. First select item with single left button click. '
                'Then click right button.',\
                'Er is geen object deselecteerd. '
                'Kies eerst een regel met een enkele click van de linkermuisknop. '
                'Click daarna met de rechtermuisknop.')
            return
        item_dict = self.prod_tree.item(cur_item)
        tree_values = list(item_dict['values'])
        #print('Prod_detail_right:',cur_item, tree_values)

        if len(tree_values) > 8:
            # If tree_values[8] contains a dot (.)
            # then it is interpreted as a file.name with file extension,
            # else it is interpreted as an selected aspect
            parts = tree_values[8].rsplit('.', maxsplit=1)
            if len(parts) == 1:
                if str(tree_values[2]) == '':
                    self.Display_message(
                        'There is no right hand object found to be displayed.',\
                        'Er is geen rechter object gevonden om weergegeven te worden.')
                else:
                    self.Display_message(
                        'The name of right hand object {} does not contain a file extension. '
                        'It is interpreted as an aspect.'.\
                        format(tree_values[8]),\
                        'De naam van het rechter object <{}> bevat geen file extensie. '
                        'Het is geïnterpreteerd als een aspect.'.\
                        format(tree_values[8]))
                    selected_obj = self.uid_dict[str(tree_values[2])]
                    self.Display_message(
                        'Display aspect details of: {}'.format(selected_obj.name),\
                        'Weergave van aspectdetails van: {}'.format(selected_obj.name))
                    self.Define_and_display_individual_detail_view(selected_obj)
            else:
                # Open the file in the file format that is defined by its file extension
                # from directory+file_name
                file_path = os.path.join(tree_values[5], tree_values[8])
                normalized_path = os.path.normpath(file_path)
                open_file(normalized_path)
        else:
            self.Display_message(
                'There is no right hand object found to be displayed.',\
                'Er is geen rechter object gevonden om weergegeven te worden.')

    def Taxon_detail_view(self, sel):
        """ Find the selected object from a user selection that is made
            in the taxon_model that is displayed in the taxon_tree view."""

        classifier = ['classifies', 'classificeert']
        cur_item = self.taxon_tree.focus()
        item_dict = self.taxon_tree.item(cur_item)
        tree_values = list(item_dict['values'])
        #print('Taxon values, sel.', tree_values)
        selected_obj = self.uid_dict[str(tree_values[0])]

        if sel.num == 1:
            # If mousebutton-1 is used, then Create a detail view
            # Verify whether object is an individual thing due to being classified
            parts = str(tree_values[2]).partition(' ')
            if parts[0] in classifier:
                #print('Display details of individual:', tree_values[0], selected_obj.name)
                self.Define_and_display_individual_detail_view(selected_obj)
            else:
                #print('Display details of kind:',tree_values[0], selected_obj.name)
                self.Define_and_display_kind_detail_view(selected_obj)
        elif self.modification == 'classification started':
            # if sel.type = 'KeyPress' with sel.keysym = 'c' then
            # Append selected classifier to modified_object, and add classification relation
            if sel.keysym == 'c':
                self.Add_classification_relation(self.modified_object, selected_obj)

                # Display modified product view
                self.modification = 'classification completed'
                self.Define_and_display_individual_detail_view(self.modified_object)
                self.Display_message(
                    'A classification of <{}> by classifier <{}> is added '
                    'to the semantic network'.\
                    format(self.modified_object.name, selected_obj.name),\
                    'Een classifikatie van <{}> door classificeerder <{}> is toegevoegd '
                    'aan het semantische netwerk.'.\
                    format(self.modified_object.name, selected_obj.name))
            else:
                self.modification = 'classification completed'
                self.Display_message(
                    'The classification of {} by classifier {} is NOT performed.'.\
                    format(self.modified_object.name, selected_obj.name),\
                    'De classifikatie van <{}> door classificeerder <{}> is NIET uitgevoerd.'.\
                    format(self.modified_object.name, selected_obj.name))

    def Add_classification_relation(self, modified_object, selected_object):
        ''' Append the (selected) kind as a classifier to the modified_object,
            and then add a classification relation to the classified individual thing
            as well as to the classifying kind.
        '''

        statement = ['statement', 'bewering']
        modified_object.classifiers.append(selected_object)

        # Add a classification expression to the list of expressions
        # of the classified object
        # First determine the first available free idea uid in the range
        for num_uid in range(self.num_idea_uid, 212000000):
            idea_uid = str(num_uid)
            if idea_uid in self.idea_uids:
                continue
            else:
                self.num_idea_uid = num_uid
                self.idea_uids.append(idea_uid)
                break
            self.Display_message(
                'There is no uid for the idea available in the range {} to {}.'.\
                format(self.num_idea_uid, 212000000),\
                'Er is geen uid voor het idee beschikbaar in de range {} tot {}.'.\
                format(self.num_idea_uid, 212000000))

        lang_uid = modified_object.names_in_contexts[0][0]
        lang_name = self.lang_uid_dict[lang_uid]
        comm_uid = modified_object.names_in_contexts[0][1]
        comm_name = self.gel_net.community_dict[comm_uid]
        lang_comm = [lang_uid, lang_name, comm_uid, comm_name]
        lh_uid_name = [modified_object.uid, modified_object.name]
        rel_uid_phrase_type = ['1225', self.classification[self.GUI_lang_index], basePhraseUID]
        rh_role_uid_name = ['', '']
        rh_uid_name = [selected_object.uid, selected_object.name] #e.g. 43769, 'roofwindow'
        uom_uid_name = ['', '']
        description = ''
        intent_uid_name = ['491285', statement[self.GUI_lang_index]]
        rel_type = self.uid_dict['1225']
        gellish_expr = Create_gellish_expression(lang_comm, idea_uid, intent_uid_name,\
                                                 lh_uid_name, rel_uid_phrase_type,\
                                                 rh_role_uid_name, rh_uid_name, \
                                                 uom_uid_name, description)
        relation = Relation(modified_object, rel_type, selected_object, \
                            basePhraseUID, '', gellish_expr)
        modified_object.add_relation(relation)
        selected_object.add_relation(relation)

    def Summ_detail_view(self, sel):
        """ Find the selected object from a user selection that is made
            in the summ_model that is displayed in the summ_tree view."""

        #item_dict = self.summ_tree.selection()
        cur_item = self.summ_tree.focus()
        item_dict = self.summ_tree.item(cur_item)
        #print('Detail view item:', item_dict['values'])
        tree_values = list(item_dict['values'])

        selected_obj = self.uid_dict[str(tree_values[0])]
        #print('Display of product details of:',tree_values[0], selected_obj.name)
        # Create a detail view
        self.Define_and_display_individual_detail_view(selected_obj)

    def Possibilities_detail_view(self, sel):
        """ Find the selected object from a user selection that is made
            in the possibilities_model that is displayed in the possib_tree view."""

        #item_dict = self.possib_tree.selection()
        cur_item = self.possib_tree.focus()
        item_dict = self.possib_tree.item(cur_item)
        #print('Detail view item:', item_dict['values'])
        tree_values = list(item_dict['values'])

        selected_obj = self.uid_dict[str(tree_values[0])]
        #print('Display product details of:',tree_values[0], selected_obj.name)
        # Create a detail view
        self.Define_and_display_kind_detail_view(selected_obj)

    def Indiv_detail_view(self, sel):
        """ Find the selected object from a user selection that is made
            in the indiv_model that is displayed in the indiv_tree view."""

        #item_dict = self.indiv_tree.selection()
        cur_item = self.indiv_tree.focus()
        item_dict = self.indiv_tree.item(cur_item)
        #print('Detail view item:', item_dict['values'])
        tree_values = list(item_dict['values'])

        selected_obj = self.uid_dict[str(tree_values[0])]
        #print('Display product details of:',tree_values[0], selected_obj.name)
        # Create a detail view
        self.Define_and_display_individual_detail_view(selected_obj)

    def Define_and_display_kind_detail_view(self, selected_obj):
        """ Create a detail view of a kind from a user selection
            and display the view in the kind_model view."""
        self.kind_model[:] = []
        self.expr_table[:] = []
        self.Build_single_product_view(selected_obj)

        try:
            self.kind_frame.destroy()
        except AttributeError:
            pass

        self.Define_kind_model_sheet()
        self.Display_kind_model_view()

        try:
            self.expr_frame.destroy()
        except AttributeError:
            pass

        # Define Expressions view sheet = = = = = = = = = = = = = = = = = = =
        self.Define_expressions_sheet()

        # Expressions view: Display expressions from self.expr_table in Treeview:
        for expr_line in self.expr_table:
            self.expr_tree.insert('', index='end', values=expr_line, tags='val_tag')

    def Define_and_display_individual_detail_view(self, selected_obj):
        """ Create a detail view of a product from a user selection
            and display the view in the prod_model view."""
        self.prod_model[:] = []
        self.expr_table[:] = []
        self.Build_single_product_view(selected_obj)

        try:
            self.prod_frame.destroy()
        except AttributeError:
            pass
        self.Define_product_model_sheet()
        self.Display_product_model_view()

        try:
            self.data_sheet.destroy()
        except AttributeError:
            pass
        self.Define_data_sheet()
        self.Display_data_sheet_view()

        try:
            self.expr_frame.destroy()
        except AttributeError:
            pass
        # Define Expressions view sheet = = = = = = = = = = = = = = = = = = =
        self.Define_expressions_sheet()

        # Expressions view: Display expressions from self.expr_table in Treeview:
        for expr_line in self.expr_table:
            self.expr_tree.insert('', index='end', values=expr_line, tags='val_tag')

    def Doc_detail_view(self, sel):
        """ Find the selected object from a user selection
            in the info_model that is displayed in the doc_tree view.
            - info_row ('values') = [info.uid, obj.uid, carrier.uid, directory_name,\
                                    info.name, super_info_name, obj.name, \
                                    carrier.name, carrier_kind_name]
        """

        cur_item = self.doc_tree.focus()
        item_dict = self.doc_tree.item(cur_item)
        info_row = list(item_dict['values'])
        #print('Doc_detail_view:', cur_item, info_row)

        # If right hand mouse button is pressed (sel.num == 3),
        # then determine and display a product view of the object
        # about which the document provides info
        if sel.num == 3:
            if len(info_row) > 1:
                if info_row[1] != '':
                    selected_obj   = self.uid_dict[str(info_row[1])]
                    #print('Display product details of: {}'.format(selected_obj.name))
                    self.Define_and_display_kind_detail_view(selected_obj)

                    if len(self.info_model) > 0:
                        self.Define_and_display_documents()
        else:
            # Left hand mouse button is pressed
            # If info_kind is a description then display the destription
            description_text  = ['description', 'beschrijving']
            description_title = ['Information about ', 'Informatie over ']
            if info_row[5] in description_text:
                #print('Information {} is not presented on a carrier but is as follows:\n   {}'.\
                #      format(info_row[4], info_row[2]))
                messagebox.showinfo(description_title[self.GUI_lang_index] + info_row[6], \
                                    info_row[2])

            # Verify whether file name (info_row[7]) is presented on a file
            # And verify whether the file name has a file extension (indicated by a dot (.))
            parts = info_row[8].rsplit('.', maxsplit=1)
            if len(parts) == 1:
                self.Display_message(
                    'File name {} does not have a file extension'.format(info_row[7]),\
                    'Filenaam {} bevat geen file extensie'.format(info_row[7]))
            else:
                # Open the file in the file format that is defined by its file extension
                directory_name = info_row[3]
                file_name = info_row[8]
                if directory_name != '':
                    if not directory_name.startswith(os.sep):
                        # By default, we look in the app root dir.
                        # This assumes the app was started from the CommunicatorSource dir.
                        directory_name = ".." + os.sep + directory_name
                    file_path = os.path.join(directory_name, file_name)
                    normalized_path = os.path.normpath(file_path)
                    open_file(normalized_path)

    def Contextual_facts(self):
        print('Contextual_facts')

##    def Determine_prod_model_subtypes(self, obj):
##        ''' Create header in prod_model for subtypes of obj
##            and determine subtypes of obj in hierarchy of kinds
##        '''
##
##        subsHead = ['Subtypes','Subtypen']
##        sub2Head = ['Sub-subs','Sub-subs']
##        sub3Head = ['Further subs','Verdere subs']
##        collOfSubtypes = []
##        #self.subtype_level = 0
##        # Create header line for subtypes in prod_model
##        self.line_nr  += 1
##        prod_head_5 = ['','',self.line_nr, subsHead[self.GUI_lang_index], \
##                       sub2Head[self.GUI_lang_index],\
##                       sub3Head[self.GUI_lang_index],'','','','','','']
##        if len(self.prod_model) < self.max_nr_of_rows:
##            self.prod_model.append(prod_head_5)
##
##        if obj.category in ['kind', 'kind of occurrence']:
##            self.Determine_display_hierarchy(obj)

##    def Determine_display_hierarchy(self, obj):
##        """Determine subtype hierarchy"""
##        self.coll_of_subtype_uids = []
##
##        # Start with direct subtype, except when they should be excluded
##        subs = []
##        if len (obj.subtypes) > 0:
##            for subtype in obj.subtypes:
##                if subtype in self.user_interface.query.ex_candids:
##                    continue
##                subs.append(subtype)
##        self.subtype_level = 0
##        role = ''
##        subsLocal = subs
##        if len(subsLocal) > 0:
##            self.subtype_level += + 1
##            for s in subsLocal:
##                for rel in s.relations:
##                    if len(self.expr_table) < self.max_nr_of_rows:
##                        self.expr_table.append(rel.expression)
##                        self.Add_line_to_network_model(rel_obj, expr)
##            # Determine subtypes of subtypes recursively
##            for sub in subs:
##                if sub in self.user_interface.query.ex_candids or sub.uid in self.coll_of_subtype_uids:
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
##                Determine_display_hierarchy(sub)

#------------------------------------------------
class User_interface():
    def __init__(self):
        pass

    def Query_net(self):
        print('Query_net')

    def Stop_Quit(self):
        print('Stop_Quit')

    def build_network(self):
        print('Create and buid network')

    def Dump_net(self):
        print('Dump_net')

if __name__ == "__main__":
    root = Tk()
    user_interface = User_interface()
    gel_net = Semantic_network('name')
    views = Display_views(gel_net)
    views.GUI_lang_index = 0
    views.lang_name = 'English'
    views.categoryInFocus = 'kind'

    views.Define_notebook()
    views.Display_notebook_views()
    root.mainloop()
