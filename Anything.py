from InitializeFormalLanguage import FormalLanguage

class Anything:
    def __init__(self, UID, description):
        self.ID = UID
        self.descr = description
        self.names_in_contexts = []    # (languageUID, communityUID, name, naming_relUID)
        self.relations      = []
        self.basePhrases    = []
        self.inversePhrases = []

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

    def show(self):
        output = str(self) + "\n"
        for rel in self.relations:
            output += "\t%s\n" % str(rel)
        print(output)

    def __repr__(self):
        return(" (%i) %s" % (self.ID, self.names_in_contexts))

class NamingDictionary(dict):
    # key   = name_in_context(tuple) = (lanuageUID, communityUID, naming_relationUID, name).
    # value = UID

    def add_name_in_context(self, name_in_context, UID):
        if name_in_context not in self:
            self.key = name_in_context
            self.value = UID

    def find_candidates(self, q_string,string_commonality):
        if q_string in self:
            return(value)

    def find_anything(self, q_name_in_context):
        if q_name_in_context in self:
            return(self.value)

class Object(Anything):
    pass

class Individual(Object):
    kind = "individual thing"

class Kind(Object):
    kind = "kind"
    
class RelationType(Anything):
    def add_base_phrase(self, phrase):
        self.basePhrases.append(phrase)

    def add_inverse_phrase(self, phrase):
        self.inversePhrases.append(phrase)

class Relation(Anything):
    def __init__(self, ideaUID, intentUID, Obj1UID, RelTypeUID, PhraseTypeUID, Obj2UID):
        self.UID        = ideaUID
        self.relTypeUID = RelTypeUID
        self.lobjUID    = Obj1UID
        self.robjUID    = Obj2UID
        self.intentUID  = intentUID
        self.phraseTypeUID = PhraseTypeUID
        relation = [self.UID       , self.intentUID    , self.lobjUID,\
                    self.relTypeUID, self.phraseTypeUID, self.robjUID]
        #self.lobjUID.add_relation(relation)
        #self.robjUID.add_relation(relation)

    def add_contextual_fact(self, cont_fact):
        try:
            self.cont_facts.append(cont_fact)
        except AttributeError:
            self.cont_facts = [cont_fact]

    def __repr__(self):
        return("Idea %i %s (%i) %s %s" % (self.UID, self.lobjUID, self.relTypeUID,\
                                              self.phraseTypeUID, self.robjUID))
    
#------------------------------------------------------------------------------------
if __name__ == "__main__":
    import Data.TestDBcontent as Exprs
    lang = FormalLanguage("English")
    for ex in Exprs.expr:
        langUID   = ex[1];   langName   = ex[2] ; commUID = ex[3]       ; commName = ex[4]
        intentUID = ex[6];   intentName = ex[7] ; lhobUID = ex[9]       ; lhobName = ex[10];
        ideaUID   = ex[15];  relTypeUID = ex[17]; relTypePhrase = ex[18]; rhobUID  = ex[23];
        rhobName  = ex[24];  fullDef    = ex[25]
        print("Expression: ",langName, commName, intentName, lhobName, relTypePhrase, rhobName)

        # Interpret an expression and create things, and main relation if they do not yet exist.

        rel = Relation(ideaUID, intentUID, lhobUID, relTypeUID, relTypePhrase, rhobUID)
        rel.descr = ''
        lang.idea_uids.append(rel)
        
        #Id = Idea(ideaUID)
        #Id.descr = "idea-" + str(ideaUID)
        R1 = [0   , "has approval status",790375, "accepted"]
        R2 = [6023, "has as originator",0,"Andries van Renssen"]
        rel.add_contextual_fact(R1)
        rel.add_contextual_fact(R2)
        print('Lang_rel_uids: ', lang.idea_uids)

        O1 = Object(lhobUID, fullDef)
        if O1 not in lang.obj_uids:
            lang.obj_uids.append(O1)
            lhob_name_in_context = [langUID, commUID, lhobName]
            O1.add_name_in_context(lhob_name_in_context)
        print('LH_obj.names_in_contexts: ', O1.names_in_contexts)

        O2 = Object(rhobUID,'')
        if O2 not in lang.obj_uids and O2 not in lang.rh_obj_uids:
            lang.rh_obj_uids.append(O2)
            O2.add_name_in_context(rhobName)
        print('RH+obj.names: ', O2.names_in_contexts)

        RT = RelationType(1260,'bla, bla')
        rt_name_in_context = [langUID, commUID, "composition relation between an individual thing \
and a composed individual thing"]
        RT.add_name_in_context(rt_name_in_context)
        RT.add_base_phrase("is a part of")
        RT.add_inverse_phrase("has as part")

        print(RT)
