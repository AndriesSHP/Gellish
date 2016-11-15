#!/usr/bin/python3

import sys
import BootstrappingRelations as BR

class FormalLanguage:
    """ Determine which formal language will be used
        Defaults = English
        Initialize bootstrapping base relation types,
        base_phrases by bootstrapping base phrases
        and inverse_phrases by bootstrapping inverse phrases
    """
    def __init__(self, language):
        self.languages        = [(910036, "English"), (910037, "Nederlands")]
        self.formal_languages = [(492015, "Formal English"), (492016, "Formeel Nederlands")]
        self.obj_uids        = []
        self.rh_obj_uids     = []
        self.idea_uids       = []
        self.rel_type_uids   = []
        self.base_phrases    = []
        self.inverse_phrases = []

        # language == 'Nederlands' then ..., otherwise English (default)
        if language == self.languages[1][1] or language == self.formal_languages[1][1]:
            self.language  = self.languages[1]
            self.community = self.formal_languages[1]
        else:
            self.language  = self.languages[0]
            self.community = self.formal_languages[0]

        if self.language[0] == 910037:
            self.base_phrases    = BR.base_boot_phrasesNL
            self.inverse_phrases = BR.inverse_boot_phrasesNL
        else:
            self.base_phrases    = BR.base_boot_phrasesEN
            self.inverse_phrases = BR.inverse_boot_phrasesEN
        self.relation_type_UIDs = BR.base_relation_type_UIDs

    def GUILanguage(self, GUI_language):
        """ Determine which user interface language will be used.
            Defaults = English
        """
        self.GUI_languages = [(910036, "English"), (910037, "Nederlands")]
        # if GUI_language == Nederlands then... else English (default)
        if GUI_language == self.GUI_languages[1][1]:
            self.GUI_language = self.GUI_languages[1]
            self.GUI_index = 1
        else:
            self.GUI_language = self.GUI_languages[0]
            self.GUI_index = 0
#------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1:
        formal_language = sys.argv[0]
        GUI_language    = sys.argv[1]
    else:
        formal_language = "English"
        GUI_language    = "English"

    Gellish = FormalLanguage(formal_language)
    print('Language & Comm: ', Gellish.language,Gellish.community)
    print('Base phrases:    ', Gellish.base_phrases)
    print('Inverse phrases: ', Gellish.inverse_phrases)
    print('Relation type UIDs: ',Gellish.relation_type_UIDs)

    GUI = Gellish.GUILanguage(GUI_language)
    print('GUI: ', Gellish.GUI_language)

    
