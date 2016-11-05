from FormalLanguage import Language

class Anything:
        def __init__(self, UID):
                self.ID = UID
                self.names = []
                self.relations = []

        def add_name(self, name):
                self.names.append(name)

        def add_relation(self, relation):
                self.relations.append(relation)

        def find(self, qstring):
                return(self.name.find(qstring))

        def show(self):
                output = str(self) + "\n"
                for rel in self.relations:
                        output += "\t%s\n" % str(rel)
                print(output)

        def __repr__(self):
                return(" (%i) %s" % (self.ID, self.names))

class Idea(Anything):
        # cont_fact= [idea_UID, name of relation type, related_object_UID, related_object_name]         
        def add_contextual_fact(self, cont_fact):
                try:
                        self.cont_facts.append(cont_fact)
                except AttributeError:
                        self.cont_facts = [cont_fact]

class Object(Anything):
	#def __init__(self):
        def nothing():
                return

class RelationType(Anything):
	#def __init__(self):
        def add_base_phrase(self, phrase):
                Gellish.basePhrases.append(phrase)

        def add_inverse_phrase(self, phrase):
                Gellish.inversePhrases.append(phrase)

class Expression(Anything):
        def __init__(self, UID, RelTypeUID, RelTypeName, Obj1, Obj2):
                self.ID   = UID
                self.relTypeID   = RelTypeUID
                self.relTypeName = RelTypePhrase  # UID and phrase
                self.lobj = Obj1        # UID and name
                self.robj = Obj2        # UID and name
                if RelTypePhrase in basePhrases:
                        self.phraseType = 6066
                elif RelTypePhrase in invesePhrases:
                        self.phraseType = 1986

        def __repr__(self):
                return("Idea %i %s (%i) %s %s" % (self.ID, self.lobj, self.relTypeID,\
                                           self.relTypeName, self.robj))

if __name__ == "__main__":

        Id = Idea(1)
        R1 = [0   , "has approval status",790375, "accepted"]
        R2 = [6023, "has as originator",0,"Andries van Renssen"]
        Id.add_contextual_fact(R1)
        Id.add_contextual_fact(R2)
        print(Id)

        O1 = Object(100)
        O1.add_name("N51")
        O1.add_name("Amsterdam road")
        print(O1.names)

        O2 = Object(101)
        O2.add_name("Road network-1")
        print(O2.names)

        FormalLanguage = "English"
        GUILanguage    = "English"
        Gellish = Language(FormalLanguage,GUILanguage)

        RT = RelationType(1260)
        RT.add_name("composition relation between an individual thing \
and a composed individual thing")
        RT.add_base_phrase("is a part of")
        RT.add_inverse_phrase("has as part")

        E = Expression(201, 1260, "is a part of",O1,O2)
        print(E)
