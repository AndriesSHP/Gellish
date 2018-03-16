import os
import csv
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *

from Bootstrapping import *
from Expr_Table_Def import *

class Anything:
    def __init__(self, uid, name, category = None):
        self.uid = uid
        # Name (out of context) at time of creation of the object
        self.name = name
        # Candidate_names = rh object names that need to be verified later with lh object names
        self.candidate_names = []
        self.defined = False
        # Categories are upper level concepts: individual, kind, etc.
        # for guiding logic and the GUI views
        # If category not specified than allocate 'anything' as category.
        self.category = category if category is not None else 'anything'
        self.names_in_contexts = [] #[lang_uid, comm_uid, name, naming_rel_uid, description]
        self.relations = [] # expressions (including used names)
        self.base_phrases = []
        self.base_phrases_in_contexts = []
        self.inverse_phrases = []
        self.inverse_phrases_in_contexts = []
        # Supertypes are the direct supertype objects
        # that duplicate the uid refs in specialization relations (subset), invalid for individuals
        self.supertypes = []
        # Subtypes are the direct subtype objects
        # that duplicate the uid refs in specialization relations (subset), invalid for individuals
        self.subtypes = []
        # Classifiers are kinds, that duplicate the uid refs in classification relations (subset)
        self.classifiers = []
        # Individuals, are individual things
        # that duplicate the uid refs in classification relations (subset), invalid for kinds
        self.individuals = []
        # Parts are the parts of kinds or of individual things (duplicates part-whole relations)
        self.parts = []
        # Aspects are the aspects and intrinsic aspects of kinds or of individual things
        # (duplicates possession relations)
        #self.aspects = [] 

    # add name or alias to collection of names:
    # name_in_context = (lanuageUID, communityUID, naming_relationUID, name).
    def add_name_in_context(self, name_in_context):
        if name_in_context not in self.names_in_contexts:
            self.names_in_contexts.append(name_in_context)

    # add relation object to collection of relations with self
    def add_relation(self, relation):
        if relation not in self.relations:
            self.relations.append(relation)
        else:
            print('Duplicate relation uid {} ignored: ',format(relation.uid))
    
    def add_classifier(self, classifier):   # only applicable for individuals
        if classifier not in self.classifiers:
            self.classifiers.append(classifier)

    def add_supertype(self, supertype):     # only applicable for kinds
        if supertype not in self.supertypes:
            self.supertypes.append(supertype)

    def add_subtype(self, subtype):         # only applicable for kinds
        if subtype not in self.subtypes:
            self.subtypes.append(subtype)

    def add_individual(self, individual):   # only applicable for kinds
        if individual not in self.individuals:
            self.individuals.append(individual)

    def add_part(self, part):   # applicable for individual things and for kinds
        if part not in self.parts:
            self.parts.append(part)
    
    def add_first_role(self, kind_of_role):
        self.first_role = kind_of_role

    def add_second_role(self, kind_of_role):
        self.second_role = kind_of_role

    def add_role_player(self, kind_of_role_player):
        self.role_player = kind_of_role_player

    def add_first_role_player(self, kind_of_role_player):
        self.first_role_player = kind_of_role_player

    def add_second_role_player(self, kind_of_role_player):
        self.second_role_player = kind_of_role_player

    def show(self, network):
        uid = self.uid
        query_results = []
        print('\nProduct model of object UID: %i' % (uid))
        for nam in self.names_in_contexts:
            if len(nam) > 0:
                if nam[4] != '':
                    print('  Name: %s %s.'    % (nam[2], nam[0:2]))
                    print('  Description: %s' % (nam[4]))
                else:
                    print('  Name: %s %s.'    % (nam[2], nam[0:2]))
            else:
                print('  Name: %s %s.' % (self.name))
        # Show all relations
        for rel in self.relations:
            lh = network.uid_dict[rel.expression[lh_uid_col]]
            if len(lh.names_in_contexts) > 0:
                # pref_name should be determined by preferences
                lh_pref_name = lh.names_in_contexts[0][2]
            else:
                lh_pref_name = lh.name
                print('  LH name in context missing:', lh.name, lh.names_in_contexts)
            rh = network.uid_dict[rel.expression[rh_uid_col]]
            if len(rh.names_in_contexts) > 0:
                # pref_name should be determined by preferences
                rh_pref_name = rh.names_in_contexts[0][2]
            else:
                rh_pref_name = rh.name 
            print('  Idea {}: ({}) {} ({}) {} ({}) {}'.format\
                  (rel.uid, \
                   rel.expression[lh_uid_col]      , lh_pref_name,\
                   rel.expression[rel_type_uid_col], rel.expression[rel_type_name_col], \
                   rel.expression[rh_uid_col]      , rh_pref_name))
            query_results.append(rel.expression)
            
        save_on_file = input('\nSave query results on output file? (y/n): ')
        if save_on_file == 'y':
            lang_name = 'Naderlands'
            serialization = 'CSV'
            Open_output_file(query_results, self.name, lang_name, serialization)
            Save_expressions_in_file(query_results, output_file, header1, serialization)

    def __repr__(self):
        #return(self.uid, self.names_in_contexts)
        return(' ({}) {}'.format(self.uid, self.names_in_contexts))

    def add_base_phrase(self, phrase_in_context):
        self.base_phrases_in_contexts.append(phrase_in_context)
        if phrase_in_context[2] not in self.base_phrases:
            self.base_phrases.append(phrase_in_context[2])

    def add_inverse_phrase(self, phrase_in_context):
        self.inverse_phrases_in_contexts.append(phrase_in_context)
        if phrase_in_context[2] not in self.inverse_phrases:
            self.inverse_phrases.append(phrase_in_context[2])

##    def add_first_kind_of_role(self, first_role_type):
##        self.first_role_type = first_role_type
##
##    def add_second_kind_of_role(self, second_role_type):
##        self.second_role_type = second_role_type

##class Object(Anything):
##    pass
##
##class Individual(Object):
##    #category = "individual thing"
##    pass
##
##class Kind(Object):
##    #category = "kind"
##    pass
##    
##class RelationType(Kind):
####    def __init__(self, uid, category = "kind of relation"):
####        Kind.__init__(self, uid, category = None):
####            self.base_phrases    = []
####            self.inverse_phrases = []
##    pass
##
##class Intention_type(Kind):
##    #category = "intention"
##    pass

class Relation(Anything):
    ''' lh, rel_type, rh, phrase_type, uom and expression
        that expresses a binary relation with contextual facts.
        Contextual facts are about this object.
        Default category is 'binary relation'
    '''
    def __init__(self, lh_obj, rel_type, rh_obj, phrase_type_uid, uom, expression, \
                 category = None):
        # intention_type = None
        self.uid        = expression[idea_uid_col]
        self.lh_obj     = lh_obj
        self.rel_type   = rel_type
        self.rh_obj     = rh_obj
        self.phrase_type_uid = phrase_type_uid
        self.uom        = uom
        # The intention_type default is 491285 (statement)
##        statement_uid = 491285
##        self.intention_type = intention_type if intention_type is not None else statement_uid
        self.expression = expression
        # The category of a relation (default: 'binary relation') is the highlevel category.
        self.category   = category if category is not None else 'binary relation'

    def add_contextual_fact(self, cont_fact):
        try:
            self.cont_facts.append(cont_fact)
        except AttributeError:
            self.cont_facts = [cont_fact]

    def __repr__(self):
        #return(self.uid, self.lh_uid, self.rel_type_uid, self.phrase_type_uid, self.rh_uid)
        return("Idea %i %i (%i) %i %i" % (self.uid, self.lh_uid, self.rel_type_uid,\
                                          self.phrase_type_uid, self.rh_uid))
#------------------------------------------------------------------------------------
if __name__ == "__main__":   
    import TestData.TestDBcontent as Exprs
    
    net_name = 'Semantic network'
    gel_net = Semantic_Network(net_name)
    for ex in Exprs.expr:
        langUID   = ex[1];   langName   = ex[2] ; commUID = ex[3]    ; commName = ex[4] ;
        intentUID = ex[6];   intentName = ex[7] ; lhobUID = ex[9]    ; lhobName = ex[10];
        ideaUID   = ex[15];  ideaName   = ex[16]; relTypeUID = ex[17]; relTypePhrase = ex[18];
        rhobUID  = ex[23];
        rhobName  = ex[24];  fullDef    = ex[25]; uomUID  = ex[26]   ; uomName  = ex[27]
        print("Expression: ",langName, commName, intentName, lhobName, relTypePhrase, rhobName)

        # Interpret an expression and create things, and main relation if they do not yet exist.

        rel = Relation(ex) #ideaName, intentUID, intentName, \
                       #lhobUID, lhobName, relTypeUID, relTypePhrase, phraseTypeUID, \
                       #rhobUID, rhobName, uomUID, uomName)

        R1 = ['0'   , "has approval status",'790375', "accepted"]
        R2 = ['6023', "has as originator",'0',"Andries van Renssen"]
        rel.add_contextual_fact(R1)
        rel.add_contextual_fact(R2)
        rel.show(gel_net)

        naming_rel_uid = '5117'
        description = 'text'
        O1 = Object(lhobUID, fullDef)
        if O1 not in gel_net.obj_uids:
            gel_net.obj_uids.append(O1)
            lhob_name_in_context = [langUID, commUID, lhobName, naming_rel_uid, description]
            O1.add_name_in_context(lhob_name_in_context)
        Q1.show(gel_net)

        O2 = Object(rhobUID,'')
        if O2 not in gel_net.obj_uids and O2 not in gel_net.rh_obj_uids:
            gel_net.rh_obj_uids.append(O2)
            O2.add_name_in_context(rhobName)
        Q2.show(gel_net)

        RT = Anything('1260','name', 'cat')
        rt_name_in_context = [langUID, commUID, "composition relation between an individual thing"
                              " and a composed individual thing", naming_rel_uid, description]
        RT.add_name_in_context(rt_name_in_context)
        RT.add_base_phrase("is a part of")
        RT.add_inverse_phrase("has as part")
        RT.show(gel_net)
    GUI_index = 0
    categoryInFocus = 'kind'
    root = Tk()
    root.title("Semantic model server")
    root.minsize(1000,400)
    myStyle = Style()
    myStyle.configure("TFrame"   ,background="#dfd")
    root.configure(background="#ddf")
    root.columnconfigure (0,weight=1)
    root.rowconfigure    (0,weight=0)
    root.rowconfigure    (1,weight=1)
