#!/usr/bin/python3

import sys
import pickle
import tkinter as tk
import SystemUsers as SU
from MainView import Main_view
from Expression_list import Expression_list
from SemanticNetwork import Semantic_Network
from QueryModule import Query
from QueryViews import Query_view

#-------------------------------------------------
class Main():
    def __init__(self):
        self.net_name = "Gellish semantic network"
        self.pickle_file_name = "Gellish_net_db"
        self.query_spec = []
        self.extended_query = False
        self.gel_net = None
        self.user = None
        self.exprs = None
        self.use_GUI = False
        self.GUI_lang_names = ("English", "Nederlands")
        self.lang_uid_dict = {"English": '910036', "Nederlands": '910037'}

        self.root = None
        self.GUI = None

        graphic = 'y' #input('GUI (y/n):')
        if graphic == 'y':
            self.use_GUI = True

#-----------------------------------------------------
    def start_up(self, user_db):
        party = 'Andries'   #input("User name: ")
        self.user = SU.User(party)
        sesam = self.user.Providing_Access(party, user_db)
        if sesam is False:
            sys.exit(0)

    def start_net(self):
        # Import gel_net semantic network from Pickle or create new network from files
        self.load_net()
        if self.gel_net is None:
            # Initialize a Semantic Network with a given name
            self.create_net()
        else:
            # Initialized expression list
            self.exprs = Expression_list(self.gel_net)

    def create_net(self):
        # Create (c) means create a new network by
        # initializing a Semantic Network with a given name
        self.gel_net = Semantic_Network(self.net_name)

        # Set GUI language default = Dutch: GUI_lang_names[1]
        self.gel_net.Set_GUI_language(self.GUI_lang_names[1])

        # Initialized expression list
        self.exprs = Expression_list(self.gel_net)

        # Create a base dictionary of kinds of relations from bootstrapping
        self.gel_net.Create_base_reltype_objects()

        # Build a new network from files that contain a language definition
        # and store the content of the files in the database
        self.exprs.Build_new_network() #, self.Gel_db)
        print("Network '{}' is built.".format(self.net_name))

    def dump_net(self):
        # Dump semantic network as pickle binary file.
        self.gel_net.save_pickle_db(self.pickle_file_name)
        #self.save_pickle_db(self.pickle_file_name)
        print("Network '{}' is saved in file {}.".format(self.net_name, self.pickle_file_name))

    def load_net(self):
        # Load semantic network from pickle binary file.
        self.load_pickle_db(self.pickle_file_name)
        if self.gel_net is None:
            print("Network '{}' is not loaded. File is not found".format(self.pickle_file_name))
        else:
            print("Network '{}' is loaded and is composed of the following files:".format(self.pickle_file_name))
            for file in self.gel_net.Gellish_files:
                print('- {}'.format(file.path_and_name))

    def load_pickle_db(self, fname):
        try:
            infile = open(fname, "br")
        except FileNotFoundError:
            print("Input pickle file could not be found: %s" % fname)
            return()
        try:
            self.gel_net = pickle.load(infile)
            #self = pickle.load(f)
        except EOFError:
            print("Input pickle file could not be read: %s" % fname)
        else:
            infile.close()

    def read_file(self):
        ''' Verify file(s) means read one or more files, verify their content
        # and load them in various tables in an in-:memory: database
        # and extent the semantic network with its content '''
        self.exprs.read_verify_and_merge_files()

    def start_gui(self):
        main.root = tk.Tk()
        main.GUI = Main_view(self)
        tk.mainloop()

    def verify_presence_of_network(self):
        # Verify presence of a semantic network, if not present then create them
        # build a new network from files
        if self.gel_net is None:
            self.gel_net.Create_base_reltype_objects()
            self.exprs.Build_new_network() #, self.Gel_db)

    def search_net(self):
        self.extended_query = False
        self.extended_query_net()

    def query_net(self):
        self.extended_query = True
        self.extended_query_net()

    def extended_query_net(self):
        # Query the semantic network
        if self.gel_net is None:
            print('First create a semantic network')
        else:
            # Create a query object
            # WHAT IS THIS? main is a global instance of Main being used in a method of Main
            self.query = Query(self.gel_net, self)
            # Enter and Interpret query
            if self.use_GUI:
                Q_view = Query_view(self.gel_net, self)
                # Specify a query via GUI
                Q_view.Query_window()
            else:
                # Specify a query via command line
                self.query.Specify_query_via_command_line()

                # Interpret and execute query
                # Search for data about kinds or about individuals and display in various views
                self.query.Interpret_query_spec()

    def stop_quit(self):
        # Terminate the program
        sys.exit()

#-----------------------------------------------
if __name__ == "__main__":
    sys.setrecursionlimit(100000)

    # Initialize user_db and start up

    user_db = SU.UserDb()
    main = Main()
    main.start_up(user_db)
    main.start_net()
    #Expression_list(main.gel_net)

    if main.use_GUI:
        main.start_gui()
    else:
        # Select one of the following actions
        action = input("\nEnter action \n  Create network     (c) \
        \n  Modify existing db (m) \n  Verify user table  (v) \n  Query existing db  (q) \
        \n  Dump network db    (d) \n  Load network db    (l) \n  Stop and Exit      (s): ")
        while action != "s":
            if action == 'c':
                main.gel_net = Semantic_Network(main.net_name)
                main.create_net()
    ##        if action == 'r': main.read_db()
    ##        if action == 'm': main.modify_db()
            if action == 'v': main.read_file()
            if action == 'q': main.query_net()
            if action == 'd': main.dump_net()
            if action == 'l': main.load_net()
            if action == 's': main.stop_quit()

            action = input("\nEnter action \n  Create network     (c) \n  Read database      (r) \
            \n  Modify existing db (m) \n  Verify user table  (v) \n  Query existing db  (q) \
            \n  Dump network db    (d) \n  Load network db    (l) \n  Stop and Exit      (s): ")
