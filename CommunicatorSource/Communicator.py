#!/usr/bin/python3

import sys
import pickle

import SystemUsers as SU
from User_interface import User_interface
from SemanticNetwork import Semantic_Network

#-------------------------------------------------
class Main():
    def __init__(self):
        self.net_name = "Gellish semantic network"
        self.pickle_file_name = "Gellish_net_db"

        self.gel_net = None
        self.user = None
        self.user_interface = None

#-----------------------------------------------------
    def start_up(self, user_db):
        party = 'Andries'   #input("User name: ")
        self.user = SU.User(party)
        sesam = self.user.Providing_Access(party, user_db)
        if sesam is False:
            sys.exit(0)

    def start_net(self):
        ''' Start user interaction and
            Import gel_net semantic network from Pickle
            or create new network from files
        '''
        # Load the semantic network from pickle, if available
        self.load_net()
        if self.gel_net is None:
            # Create a Semantic Network with a given name
            # from bootstrapping and from files
            self.gel_net = Semantic_Network(self.net_name)
            # Build the semantic network
            self.gel_net.build_network()
        # Create and open a user interface
        self.user_interface = User_interface(self.gel_net)

    def load_net(self):
        # Load semantic network from pickle binary file.
        self.load_pickle_db(self.pickle_file_name)
        if self.gel_net is None:
            print("Network '{}' is not loaded. File is not found".\
                  format(self.pickle_file_name))
        else:
            print("Network '{}' is loaded "
                  "and is composed of the following files:".\
                  format(self.pickle_file_name))
            for file in self.gel_net.Gellish_files:
                print('- {}'.format(file.path_and_name))

    def load_pickle_db(self, fname):
        try:
            infile = open(fname, "br")
        except FileNotFoundError:
            print("Input pickle file could not be found: {}". \
                  format(fname))
            return()
        try:
            self.gel_net = pickle.load(infile)
            #self = pickle.load(f)
        except EOFError:
            print("Input pickle file could not be read: {}". \
                  format(fname))
        else:
            infile.close()

#-----------------------------------------------
if __name__ == "__main__":
    sys.setrecursionlimit(100000)

    # Initialize user_db and start up

    user_db = SU.UserDb()
    main = Main()
    main.start_up(user_db)
    main.start_net()
