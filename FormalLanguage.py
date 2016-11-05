#!/usr/bin/python3

import BootstrappingRelations as BR
#!/usr/bin/python3
import sys

class Language:
	""" Determine which formal language will be used
		and which user interface language will be used.
		Defaults for both = English
		Specify bootstrapping base relation types, base phrases and inverse phrases
	"""
	def __init__(self, language, GUIlanguage):
		self.languages       = [(910036, "English"), (910037, "Nederlands")]
		self.formalLanguages = [(492015, "Formal English"), (492016, "Formeel Nederlands")]
		# if language of GUIlanguage == Nederlands dan... anders Engels (default)
		if language == self.languages[1][1]:
			self.formalLanguage = self.formalLanguages[1]
			self.community      = self.formalLanguages[1]
		else:
			self.formalLanguage = self.formalLanguages[1]
			self.community      = self.formalLanguages[1]
		if GUIlanguage == self.languages[1][1]:
			self.GUIlanguage = self.languages[1]
		else:
			self.GUIlanguage = self.languages[0]

		if self.formalLanguage[0] == 910037:
			self.basePhrases    = BR.baseBootPhrasesNL
			self.inversePhrases = BR.inverseBootPhrasesNL
		else:
			self.basePhrases    = BR.baseBootPhrasesEN
			self.inversePhrases = BR.inverseBootPhrasesEN
		self.relation_types = BR.base_relation_types
		self.kinds = []         # UIDs of kinds
		self.individuals = []   # UIDs of individual things
		

if __name__ == "__main__":
        if len(sys.argv) > 1:
                FormalLanguage = sys.argv[1]
                GUILanguage    = sys.argv[2]
        else:
                FormalLanguage = "English"
                GUILanguage    = "English"

        Gellish = Language(FormalLanguage,GUILanguage)
        print(FormalLanguage,GUILanguage,Gellish.basePhrases)
