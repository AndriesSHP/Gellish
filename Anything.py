from Bootstrapping import *

class Anything:
    def __init__(self, uid):
        self.uid = uid
        self.names_in_contexts = []  #[lang_uid, comm_uid, name, naming_rel_uid, description]
        self.relations      = [] # expressions (including used names)
        self.basePhrases    = []
        self.inversePhrases = []
        self.supertypes     = [] # duplicate of uids in relations (subset), invalid for individuals
        self.subtypes       = [] # duplicate of uids in relations (subset), invalid for individuals
        self.classifiers    = [] # kinds, duplicate of uids in relations (subset)
        self.individuals    = [] # individuals, duplicate of uids in relations (subset), invalid for individuals

    # add name or alias to collection of names:
    # name_in_context = (lanuageUID, communityUID, naming_relationUID, name).
    def add_name_in_context(self, name_in_context):
        if name_in_context not in self.names_in_contexts:
            self.names_in_contexts.append(name_in_context)

    # add relation to collection of relations with self
    # relation = [ideaUID, intentUID, Obj1UID, relTypeUID, phraseType, Obj2UID]
    def add_relation(self, relation):
        if relation not in self.relations:
            self.relations.append(relation)
        else:
            print('Duplicate relation ignored: ',relation)
    
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

    def show(self, network):
        uid = self.uid
        print('\nObject UID: %i' % (uid)) # , self.names_in_contexts), ('Python id: %i'% (id(self))
        for nam in self.names_in_contexts:
            if len(nam) > 0:
                if nam[4] != '':
                    print('  Name: %s %s.'    % (nam[2], nam[0:2]))
                    print('  Description: %s' % (nam[4]))
                else:
                    print('  Name: %s %s.'    % (nam[2], nam[0:2]))
            else:
                print('  Name: %s %s.' % (self.name))
        for rel in self.relations:
            lh = network.find_object(rel.lh_uid)
            if len(lh.names_in_contexts) > 0:
                lh_pref_name = lh.names_in_contexts[0][2] # name should be determined by preferences
            else:
                lh_pref_name = lh.name
                print('  LH name in context missing:', lh.name, lh.names_in_contexts)
            rh = network.find_object(rel.rh_uid)
            if len(rh.names_in_contexts) > 0:
                rh_pref_name = rh.names_in_contexts[0][2] # name should be determined by preferences
            else:
                rh_pref_name = rh.name 
            print('  Idea %i: (%i) %s (%i) %s (%i) %s' % \
                  (rel.uid, \
                   rel.lh_uid      , lh_pref_name,\
                   rel.rel_type_uid, rel.rel_type_name, \
                   rel.rh_uid      , rh_pref_name))
        #    header += "\t%s\n" % str(rel)

    def __repr__(self):
        #return(self.uid, self.names_in_contexts)
        return(" (%i) %s" % (self.uid, self.names_in_contexts))

class Object(Anything):
    pass

class Individual(Object):
    kind = "individual thing"

class Kind(Object):
    kind = "kind"
    
class RelationType(Kind):
    kind = "kind of relation"
    def add_base_phrase(self, phrase):
        self.basePhrases.append(phrase)

    def add_inverse_phrase(self, phrase):
        self.inversePhrases.append(phrase)

class Relation(Anything):
    kind = "binary relation" # expression kernel
    def __init__(self, ideaUID, idea_desc, intentUID, intent_name, \
                 lhUID, lhName, relTypeUID, relTypeName, phraseTypeUID, \
                 rhUID, rhName, uomUID, uomName):
        self.uid           = ideaUID
        self.intent_uid    = intentUID
        self.rel_type_uid  = relTypeUID
        self.lh_uid        = lhUID
        self.rh_uid        = rhUID
        self.phrase_type_uid = phraseTypeUID
        self.name          = idea_desc
        self.intent_name   = intent_name
        self.lh_name       = lhName
        self.rel_type_name = relTypeName
        self.rh_name       = rhName
        self.uom_uid       = uomUID
        self.uom_name      = uomName
        #relation = [self.uid         , self.intent_uid     , self.lh_uid,\
        #            self.rel_type_uid, self.phrase_type_uid, self.rh_uid]
        #self.lh_uid.add_relation(relation)
        #self.rh_uid.add_relation(relation)

    def add_contextual_fact(self, cont_fact):
        try:
            self.cont_facts.append(cont_fact)
        except AttributeError:
            self.cont_facts = [cont_fact]

    def __repr__(self):
        #return(self.uid, self.lh_uid, self.rel_type_uid, self.phrase_type_uid, self.rh_uid)
        return("Idea %i %i (%i) %i %i" % (self.uid, self.lh_uid, self.rel_type_uid,\
                                          self.phrase_type_uid, self.rh_uid))

class Language:
    """ Determine which modelling language will be used
        Defaults = English
    """
    def __init__(self, language):
        lang_dict = {910036: "English", 910037: "Nederlands"}
        comm_dict = {492015: "Formal English", 492016: "Formeel Nederlands"}

        # language == 'Nederlands' then ..., otherwise English (default)
        if language == lang_dict[910037] or language == comm_dict[492016]:
            self.language  = self.lang_dict[910037]
            self.community = self.comm_dict[492016]
        else:
            self.language  = lang_dict[910036]
            self.community = comm_dict[492015]

class GUI_Language:
    '''The language of the user interface. Default is English.
       GUIlang = "English" or "Nederlands"
    '''
    def __init__(self, GUI_lang):
        self.GUI_lang_dict = {910036: "English", 910037: "Nederlands"}
        self.GUI_lang = GUI_lang
        if self.GUI_lang == self.GUI_lang_dict[910037]:
            self.GUI_index = 1
        else:
            self.GUI_index = 0

    def Message(self, mess_text_EN, mess_text_NL):
        if self.GUI_index == 1:
            print(mess_text_NL)
        else:
            print(mess_text_EN)
#------------------------------------------------------------------------------------
if __name__ == "__main__":
    import TestData.TestDBcontent as Exprs
    lang = Language("English")
    for ex in Exprs.expr:
        langUID   = ex[1];   langName   = ex[2] ; commUID = ex[3]    ; commName = ex[4]
        intentUID = ex[6];   intentName = ex[7] ; lhobUID = ex[9]    ; lhobName = ex[10];
        ideaUID   = ex[15];  ideaName   = ex[16]; relTypeUID = ex[17]; relTypePhrase = ex[18]; rhobUID  = ex[23];
        rhobName  = ex[24];  fullDef    = ex[25]; uomUID  = ex[26]   ; uomName[27]
        print("Expression: ",langName, commName, intentName, lhobName, relTypePhrase, rhobName)

        # Interpret an expression and create things, and main relation if they do not yet exist.

        rel = Relation(ideaUID, ideaName, intentUID, intentName, \
                       lhobUID, lhobName, relTypeUID, relTypePhrase, phraseTypeUID, \
                       rhobUID, rhobName, uomUID, uomName)
        lang.idea_uids.append(rel)
        
        #Id = Idea(ideaUID)
        #Id.descr = "idea-" + str(ideaUID)
        R1 = [0   , "has approval status",790375, "accepted"]
        R2 = [6023, "has as originator",0,"Andries van Renssen"]
        rel.add_contextual_fact(R1)
        rel.add_contextual_fact(R2)
        print('Lang_rel_uids: ', lang.idea_uids)

        naming_rel_uid = 5117
        description = 'text'
        O1 = Object(lhobUID, fullDef)
        if O1 not in lang.obj_uids:
            lang.obj_uids.append(O1)
            lhob_name_in_context = [langUID, commUID, lhobName, naming_rel_uid, description]
            O1.add_name_in_context(lhob_name_in_context)
        print('LH_obj.names_in_contexts: ', O1.names_in_contexts)

        O2 = Object(rhobUID,'')
        if O2 not in lang.obj_uids and O2 not in lang.rh_obj_uids:
            lang.rh_obj_uids.append(O2)
            O2.add_name_in_context(rhobName)
        print('RH+obj.names: ', O2.names_in_contexts)

        RT = RelationType(1260,'bla, bla')
        rt_name_in_context = [langUID, commUID, "composition relation between an individual thing \
and a composed individual thing", naming_rel_uid, description]
        RT.add_name_in_context(rt_name_in_context)
        RT.add_base_phrase("is a part of")
        RT.add_inverse_phrase("has as part")

        print(RT)
