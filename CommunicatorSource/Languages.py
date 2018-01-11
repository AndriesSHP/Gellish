#!/usr/bin/python3

lang_uid_dict = {'910036': "English", '910037': "Nederlands", '911689':"American", '589211':"international"}
comm_uid_dict = {'492014': "Gellish", '589830': "Gellish alternative"}
GUI_lang_name_dict = {"English":'910036', "Nederlands":'910037'}

class GUI_language:
    """ The language of the user interface (GUI)
        Defaults = English
    """
    def __init__(self, GUI_lang_name='English'):
        
        self.GUI_lang_name = GUI_lang_name
        # GUI_lang_name == 'Nederlands' then ..., otherwise English (default)
        if GUI_lang_name == lang_dict['910037']:
            self.GUI_lang_uid = '910037'
            self.GUI_lang_index = 1
        else:
            self.GUI_lang_uid = '910036'
            self.GUI_lang_index = 0

    def Set_GUI_language(self, GUI_lang_name):
        '''Set the GUI language of the user'''
        if GUI_lang_name in GUI_lang_name_dict:
            self.GUI_lang_name = GUI_lang_name
            self.GUI_lang_uid  = self.GUI_lang_name_dict[GUI_lang_name]
            if self.GUI_lang_name == 'Nederlands':
                self.GUI_lang_index = 1
            else:
                self.GUI_lang_index = 0
            GUI_lang_set = True
            if self.GUI_lang_uid == '910036':
                # Set default GUI_preferences at international, English, American
                self.GUI_lang_pref_uids = ['589211', '910036', '911689']
            elif self.GUI_lang_uid == '910037':
                # Set default preferences at international, Dutch, English
                self.GUI_lang_pref_uids = ['589211', '910037', '910036']
            else:
                # Set default preferences at international, user_language, English
                self.GUI_lang_pref_uids = ['589211', self.GUI_lang_uid, '910036']
        else:
            print('GUI language {} is unknown. Default = English is used.'.format(GUI_lang_name))
            GUI_lang_set = False
        return GUI_lang_set

class Reply_language:
    ''' The language preferences in which the results are presented,
        in the views as well as in the output files with Gellish expressions
    '''
    def __init__(self, reply_lang_name):
        self.reply_lang_name = reply_lang_name
        
    def Determine_reply_lang_prefs(self):
        pass

#------------------------------------------------------------------------------------
if __name__ == "__main__":
    pass
    
