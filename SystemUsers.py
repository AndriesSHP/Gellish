#!/usr/bin/python3

#languages = ['English', 'Nederlands', 'American']
lang_name_dict = {'English':'910036', 'Nederlands':'910037', 'American':'911689', 'Chinese':'911876'}
lang_dict = {'910036': "English", '910037': "Nederlands", '911689':"American", '589211':"international"}
comm_dict = {'492014': "Gellish", '589830': "Gellish alternative"}

class System():
    def __init__(self):
        self.users   = []
        self.pw_dict = {}

    def Register_User(self, new_user, pw):
        self.pw_dict[new_user] = pw
        self.users.append(new_user)
        
class User():
    def __init__(self, name):
        self.name = name
        self.preferences = []
        self.GUI_lang_pref_uids = []
##        self.GUI_lang_name     = 'Nederlands' # default
##        self.GUI_lang_uid      = lang_name_dict['Nederlands'] # default
##        self.GUI_lang_index    = 1            # "Nederlands" (default)
        self.modeling_language = "English"    # default
        # English:910036, American:911689, international:589211, Nederlands:910037
        self.lang_pref_uids = []
        # 492014:"Gellish"
        self.comm_pref_uids = ['492014'] # Default: 'Gellish'
        
    def Providing_Access(self, party, system):
        # Login: Determine party and preferences
        sesam = False
        known_party = False
        trials = 0
        while known_party != True:
            # Verify password
            if party in system.pw_dict:
                known_party = True
                while sesam != True and trials < 5:
                    trials += 1
                    pw = 'pw' #input("Password: ")
                    if system.pw_dict[party] == pw:
                        sesam = True
                if sesam == False:
                    print("Password %i times incorrect" % (trials))
                    exit(0)
            else:
                # Register new users
                self.pw    = 'pw' #input("Password: ")
                self.email = 'email' #input("Email address: ")
                system.Register_User(party, self.pw)
                sesam = True
        return (sesam)

    def Set_GUI_language(self, GUI_lang):
        '''Set the GUI language of the user'''
        if GUI_lang in lang_name_dict:
            self.GUI_lang_name = GUI_lang
            self.GUI_lang_uid  = lang_name_dict[GUI_lang]
            if GUI_lang == 'Nederlands':
                self.GUI_lang_index = 1
            else:
                self.GUI_lang_index = 0
            GUI_set = True
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
            print('GUI language %s unknown. Default = English.' % (GUI_lang))
            GUI_set = False
        return GUI_set

    def Set_reply_language(self, reply_lang_name):
        '''Set the reply language for display of the user views'''
        if reply_lang_name in lang_name_dict:
            self.reply_lang_name = reply_lang_name
            self.reply_lang_uid  = lang_name_dict[reply_lang_name]
            if self.reply_lang_uid == '910036':
                # Set default preferences at international, English, American
                self.lang_pref_uids = ['589211', '910036', '911689']
            elif self.reply_lang_uid == '910037':
                # Set default preferences at international, Dutch, English
                self.lang_pref_uids = ['589211', '910037', '910036']
            else:
                # Set default preferences at international, user_language, English
                self.lang_pref_uids = ['589211', self.reply_lang_uid, '910036']
        else:
            print('Reply language %s unknown. Default = English.' % (reply_lang_name))
            self.reply_lang_name = 'English'
            self.reply_lang_uid  = '910037'

    def Message(self, mess_text_EN, mess_text_NL):
        if self.GUI_lang_index == 1:
            print(mess_text_NL)
        else:
            print(mess_text_EN)

    def Modify_Preferences(self):
        # Display user preferences
        print("Preferences for user %s " % (self.name))
        print("  GUI language     : %s " % (self.GUI_lang_name))
        print("  Modeling language: %s " % (self.modeling_language))
        print("Output languages pref sequence:")
        print(' ', end=" ")
        for lang in self.lang_prefs:
            print(lang_dict[lang],',', sep="", end=" ")
        print("\nLanguage community pref sequence:")
        print(' ', end=" ")
        for comm in self.comm_pref_uids:
            print(comm_dict[comm],',', sep="", end=" ")
        change_prefs = input("\nChange preferences? (y/n): ")
        if change_prefs == 'y':
            # Determine and initialize GUI_lang_name
            out_lang = input("GUI language (EN or NL): ")
            if out_lang in ['NL', 'nl']:
                self.Set_GUI_Language("Nederlands")
            else:
                self.Set_GUI_Language("English")
            print("GUI language: %s " % (self.GUI_lang_name))

class Language:
    """ Determine which modelling language will be used
        Defaults = English
    """
    def __init__(self, language):

        # language == 'Nederlands' then ..., otherwise English (default)
        if language == lang_dict['910037'] or language == comm_dict['492014']:
            self.language  = self.lang_dict['910037']
            self.community = self.comm_dict['492014']
        else:
            self.language  = lang_dict['910036']
            self.community = comm_dict['492014']

#------------------------------------------------------------------------------------
if __name__ == "__main__":
    user_pw_dict = {}
    users = []

    # Create and register first user
    party = "Andries"
    user = User(party)
    users.append(user)
    pw    = 'pw'   #pw    = input("Password: ")
    email = 'andries.vanrenssen@gellish.net' #email = input("Email address: ")
    user.Register_User(party, pw, email)

    # Enter user name, if not registered the register
    party = "Andries"   #input("User name: ")
    if party not in user_pw_dict:
        user = User(party)
        users.append(user)
        pw    = 'pw'    #input("Password: ")
        email = 'a@a'   #input("Email address: ")
        user.Register_User(party, pw, email)
    else:
        if len(users) > 0:
            for obj in users:
                if obj.name == party:
                    user = obj
            
    sesam = user.Providing_Access(party)
    if sesam == False:
        exit(0)
    user.Modify_Preferences()
    print('Ready')
    
