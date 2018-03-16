#!/usr/bin/python3

import sys
import pickle
#import tkinter as tk

import SystemUsers as SU
from User_interface import User_interface
from SemanticNetwork import Semantic_Network
#from Display_views import Display_views
#from Query import Query
#from QueryViews import Query_view

#-------------------------------------------------
class Main():
    def __init__(self):
        self.net_name = "Gellish semantic network"
        self.pickle_file_name = "Gellish_net_db"
##        self.query = None
##        self.query_spec = []
        self.gel_net = None
        self.user = None
##        self.views = None
##        self.use_GUI = False
        #self.GUI_lang_names = ("English", "Nederlands")
        #self.lang_uid_dict = {"English": '910036', "Nederlands": '910037'}

        #self.root = None
        self.user_interface = None

##        graphic = 'y' #input('GUI (y/n):')
##        if graphic == 'y':
##            self.use_GUI = True

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

##    def start_gui(self):
##        self.root = tk.Tk()
##        self.user_interface = User_interface(self)
##        # Create a query object
##        self.query = Query(self.gel_net, self)
##        # Create display views objects and initialize notebook
##        self.views = Display_views(main)
##        tk.mainloop()

##    def read_file(self):
##        ''' Verify file(s) means read one or more files, verify their content
##            and extent the semantic network with its content
##        '''
##        self.gel_net.read_verify_and_merge_files()

##    def verify_presence_of_network(self):
##        # Verify presence of a semantic network,
##        #   if not present then create them
##        # build a new network from files
##        if self.gel_net is None:
##            self.gel_net.Create_base_reltype_objects()
##            self.gel_net.Build_new_network()

#-----------------------------------------------
if __name__ == "__main__":
    sys.setrecursionlimit(100000)

    # Initialize user_db and start up

    user_db = SU.UserDb()
    main = Main()
    main.start_up(user_db)
    main.start_net()

##    if main.use_GUI:
##        main.start_gui()
##    else:
##        # Select one of the following actions
##        action = input('\nEnter action '
##                       '\n  Create network     (c) '
##                       '\n  Modify existing db (m) '
##                       '\n  Verify user table  (v) '
##                       '\n  Query existing db  (q) '
##                       '\n  Dump network db    (d) '
##                       '\n  Load network db    (l) '
##                       '\n  Stop and Exit      (s): ')
##        while action != "s":
##            if action == 'c':
##                main.gel_net = Semantic_Network(main.net_name)
##                main.gel_net.build_network()
##    ##        if action == 'r': main.read_db()
##    ##        if action == 'm': main.modify_db()
##            if action == 'v': main.read_file()
##            if action == 'q': main.query_net()
##            if action == 'd': main.dump_net()
##            if action == 'l': main.load_net()
##            if action == 's': main.stop_quit()
##
##            action = input('\nEnter action '
##                           '\n  Create network     (c) '
##                           '\n  Read database      (r) '
##                           '\n  Modify existing db (m) '
##                           '\n  Verify user table  (v) '
##                           '\n  Query existing db  (q) '
##                           '\n  Dump network db    (d) '
##                           '\n  Load network db    (l) '
##                           '\n  Stop and Exit      (s): ')
