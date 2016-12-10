#!/usr/bin/python3

from Anything import GUI_Language

GUI_languages = ['English', 'Nederlands']
lang_dict = {910036: "English", 910037: "Nederlands", 911689:"American", 589211:"international"}
comm_dict = {492015: "Formal English", 492016: "Formeel Nederlands"}

# Existing users to be read from database (** TO BE DONE **)
user_pw_dict = {}
users = [] 

class User():
    def __init__(self, name):
        self.name = name
        self.preferences = []
        self.GUI_language      = "English"    # default
        self.modeling_language = "English"    # default
        # English:910036, American:911689, international:589211, Nederlands:910037
        self.lang_prefs = [910036, 911689, 589211, 910037] # Default
        # 492015:"Formal English", 492016:"Formeel Nederlands"
        self.comm_prefs = [492015, 492016] # Default
        self.Set_GUI_Language(self.GUI_language)
        
    def Providing_Access(self, party):
        # Login: Determine party and preferences
        sesam = False
        known_party = False
        trials = 0
        while known_party != True:
            # Verify password
            if party in user_pw_dict:
                known_party = True
                while sesam != True and trials < 5:
                    trials += 1
                    pw = input("Password: ")
                    if user_pw_dict[party] == pw:
                        sesam = True
                if sesam == False:
                    print("Password %i times incorrect" % (trials))
                    exit(0)
            else:
                # Register new users
                pw    = input("Password: ")
                email = input("Email address: ")
                self.Register_User(party, pw, email)
                sesam = True
        return (sesam)

    def Register_User(self, new_user, pw, email):
        user_pw_dict[new_user] = pw
        self.email = email

    def Set_GUI_Language(self, GUI_lang):
        if GUI_lang in GUI_languages:
            self.GUI_language = GUI_lang
            self.GUI_index = GUI_languages.index
        else:
            print('GUI language %s unknown. Default = English.' % (GUI_lang))
            self.GUI_language = GUI_languages[0]
            self.GUI_index = 0

    def Display_Preferences(self):
        # Display preferences
        print("Preferences for %s " % (self.name))
        print("  GUI language     : %s " % (self.GUI_language))
        print("  Modeling language: %s " % (self.modeling_language))
        print("Output languages pref sequence:")
        print(' ', end=" ")
        for lang in self.lang_prefs:
            print(lang_dict[lang],',', sep="", end=" ")
        print("\nLanguage community pref sequence:")
        print(' ', end=" ")
        for comm in self.comm_prefs:
            print(comm_dict[comm],',', sep="", end=" ")
        change_prefs = input("\nChange preferences? (y/n): ")
        if change_prefs == 'y':
            # Determine and initialize GUI_language
            out_lang = input("GUI language (EN or NL): ")
            if out_lang in ['NL', 'nl']:
                self.Set_GUI_Language("Nederlands")
            else:
                self.Set_GUI_Language("English")
            print("GUI language: %s " % (self.GUI_language))

#------------------------------------------------------------------------------------
if __name__ == "__main__":
    user_pw_dict = {}
    users = []

    # Create and register first user
    party = "a"
    user = User(party)
    users.append(user)
    pw    = 'a'   #pw    = input("Password: ")
    email = 'andries.vanrenssen@gellish.net' #email = input("Email address: ")
    user.Register_User(party, pw, email)

    # Enter user name, if not registered the register
    party = input("User name: ")
    if party not in user_pw_dict:
        user = User(party)
        users.append(user)
        pw    = input("Password: ")
        email = input("Email address: ")
        user.Register_User(party, pw, email)
    else:
        if len(users) > 0:
            for obj in users:
                if obj.name == party:
                    user = obj
            
    sesam = user.Providing_Access(party)
    if sesam == False:
        exit(0)
    user.Display_Preferences()
    print('Ready')
    
