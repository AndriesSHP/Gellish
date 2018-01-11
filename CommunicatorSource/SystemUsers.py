#!/usr/bin/python3

lang_dict = {'910036': "English", '910037': "Nederlands", '911689':"American", '589211':"international"}
comm_dict = {'492014': "Gellish", '589830': "Gellish alternative"}

class UserDb():
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

    def Providing_Access(self, party, user_db):
        # Login: Determine party and preferences
        sesam = False
        known_party = False
        trials = 0
        while known_party != True:
            # Verify password
            if party in user_db.pw_dict:
                known_party = True
                while sesam != True and trials < 5:
                    trials += 1
                    pw = 'pw' #input("Password: ")
                    if user_db.pw_dict[party] == pw:
                        sesam = True
                if sesam is False:
                    print("Password %i times incorrect" % (trials))
                    exit(0)
            else:
                # Register new users
                self.pw    = 'pw' #input("Password: ")
                self.email = 'email' #input("Email address: ")
                user_db.Register_User(party, self.pw)
                sesam = True
        return (sesam)

    def Modify_Preferences(self):
        # Display user preferences
        print("Preferences for user %s " % (self.name))
        print("Preferences     : {} ".format(self.preferences))

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
    if sesam is False:
        exit(0)
    user.Modify_Preferences()
    print('Ready')

