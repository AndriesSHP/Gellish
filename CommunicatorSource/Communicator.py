#!/usr/bin/python3

import os
import sys
import sqlite3
import pickle
from tkinter import *
from tkinter.ttk import *
from SystemUsers import System, User
from MainView import Main_view
from Expression_list import Expression_list
from DatabaseAPI import Database
from GellishDict import GellishDict
from SemanticNetwork import Semantic_Network
from QueryModule import Query
from QueryViews import Query_view
from Bootstrapping import *

#-------------------------------------------------
class Main():
    def __init__(self):
        self.Gel_net_built = False
        self.db_opened = False
        self.net_name  = "Gellish semantic network"
        self.db_name   = "GellishDB"
        self.file_name = "Gellish_net_db"
        self.query_spec = []
        self.extended_query = False

        self.use_GUI = False
        graphic = 'y' #input('GUI (y/n):')
        if graphic == 'y':
            self.use_GUI = True

#-----------------------------------------------------
    def Start_up(self, system):
        party = 'Andries'   #input("User name: ")
        self.user = User(party)
        sesam = self.user.Providing_Access(party, system)
        if sesam == False:
            exit(0)

    def Start_net(self):
        self.GUI_lang_names = ("English", "Nederlands")
        self.lang_uid_dict  = {"English": '910036', "Nederlands": '910037'}

        # Import Gel_net semantic network from Pickle or create new network from files
        self.Load_net()
        if not self.Gel_net_built:
            # Initialize a Semantic Network with a given name
            self.Create_net()
        else:
            # Initialized expression list
            self.exprs = Expression_list(self.Gel_net)
    
    def Create_net(self):
        try:
            del(self.Gel_net)
            Gel_net_built = False
        except AttributeError:
                pass

        # Create (c) means create a new network by
        # initializing a Semantic Network with a given name
        self.Gel_net = Semantic_Network(self.net_name, self.user)

        # Set GUI language default = Dutch: GUI_lang_names[1]
        self.Gel_net.Set_GUI_Language(self.GUI_lang_names[1])

        # Initialized expression list
        self.exprs = Expression_list(self.Gel_net)
        
##        # Create a new database
##        self.Create_new_database()
##        self.db_opened = True
##        # Network is based on database with filename db_name
##        self.Gel_net.db_name = self.db_name
        
        # Create a base dictionary of kinds of relations from bootstrapping
        self.Gel_net.Create_base_reltype_objects()
        
        # Build a new network from files that contain a language definition
        # and store the content of the files in the database
        self.exprs.Build_new_network() #, self.Gel_db)
        self.Gel_net_built = True
        print("Network '{}' is built.".format(self.net_name))

    def Dump_net(self):
        # Dump semantic network as pickle binary file.
        self.Gel_net.Pickle_Dump(self.file_name)
        #self.Pickle_Dump(self.file_name)
        print("Network '{}' is saved in file {}.".format(self.net_name, self.file_name))

    def Load_net(self):
        # Load semantic network from pickle binary file.
        self.Pickle_Load(self.file_name)
        if self.Gel_net_built == True:
            print("Network '{}' is loaded.".format(self.file_name))
        else:
            print("Network '{}' is not loaded. File is not found".format(self.file_name))

    def Pickle_Load(self, fname):
        try:
            f = open(fname, "br")
            try:
                self.Gel_net = pickle.load(f)
                #self = pickle.load(f)
                self.Gel_net_built = True
            except EOFError:
                pass
            f.close()
        except FileNotFoundError:
            pass

    def Read_db(self):
##        self.Verify_presence_db_and_net()
        # Build a network from database content
        # **** to be done ****
        return

    def Modify_db(self):
##        self.Verify_presence_db_and_net()
        # Modify or extent an existing network
        # by loading knowledge and/or product model files
        self.db_cursor.Import_Model_Files(model_files, model_dirs, self.Gel_net, self.user)
        
    def Read_file(self):
##        self.Verify_presence_db_and_net()
        # Verify file(s) means read one or more files, verify their content
        # and load them in various tables in an in-:memory: database
        # and extent the semantic network with its content
        self.exprs.Read_verify_and_merge_files()

    def Verify_presence_db_and_net(self):
        # Verify presence of database and network, if not present then create them
        self.db_cursor = self.Ensure_db_opened(self.db_name)
        if self.db_opened == False:
            # Create new database and load database with a language definition
            self.Create_new_database()
            self.db_opened = True
            # Network is based on database with filename db_name
            self.Gel_net.db_name = self.db_name
            # Build a new network from files
            self.Gel_net.Create_base_reltype_objects()
            self.exprs.Build_new_network() #, self.Gel_db)
            self.Gel_net_built = True
        if self.Gel_net_built == False:
            # Build a Semantic Network from database content
            self.Ensure_network_built()
            self.Gel_net_built = True

    def Search_net(self):
        self.extended_query = False
        self.Extended_query_net()
        
    def Query_net(self):
        self.extended_query = True
        self.Extended_query_net()
        
    def Extended_query_net(self):
        # Query the semantic network
        if self.Gel_net_built == True:
            # Create a query object
            main.query = Query(self.Gel_net, main)
            # Enter and Interpret query
            if self.use_GUI:
                Q_view = Query_view(self.Gel_net, main)
                # Specify a query via GUI
                Q_view.Query_window()
            else:
                # Specify a query via command line
                main.query.Specify_query_via_command_line()

                # Interpret and execute query
                # Search for data about kinds or about individuals and display in various views
                main.query.Interpret_query_spec()
        else:
            print('First create a semantic network')

    def Stop_Quit(self):
        # Terminate the program
        quit

    #------------------------------------------------
    def Connect_to_database(self, db_name):
        if db_name == ":memory:":
            db_connect = sqlite3.connect(db_name)
        else:
            db_connect = sqlite3.connect("%s.db3"% db_name)
        self.db_cursor  = db_connect.cursor()

    #-----------------------------------------------------------------        
    def Create_new_database(self):
        '''Create new database and load database with a language definition
           and build a semantic network.
        ''' 
        # Remove the old database (if present)
        try:
            os.remove(self.db_name + ".db3")
            print('Database {} removed'.format(self.db_name + ".db3"))
        except OSError:
            pass
        # Create a new database.
        self.Gel_db = Database(self.db_name)    # create a new database
        self.Gel_db.Create_tables()             # create empty tables
        self.db_cursor = self.Gel_db.db_cursor
        # print("Database: %s created." % (name))
                
    def Ensure_db_opened(self, db_name):
        # If not an in_memory_database, then connect to database
##        if db_name != ':memory:':
##            self.db_cursor = self.Connect_to_database(db_name)
##            print("Database: %s connected." % (db_name))
##            self.db_opened = True
        return

    def Ensure_network_built(self):
        # If no network built yet, then    
        # Build the Semantic Newtork from the database tables
        print("Build semantic network: %s." % (self.net_name))
##        self.Gel_net.Build_Base_Semantic_Network(self.db_cursor, self.user) # incl. collecting rel_type_uids for validation
##        self.Gel_net.BuildHierarchies()
##        self.Gel_net.Extent_Semantic_Network(self.db_cursor, self.user)
        
#-----------------------------------------------
##from tkinter import *
##from tkinter.ttk import *
##from GellishDict import GellishDict

sys.setrecursionlimit(100000)

# Initialize system and start up

system = System()
main = Main()
main.Start_up(system)
main.Start_net()
#Expression_list(main.Gel_net)

if main.use_GUI:
    main.root = Tk()
    main.GUI = Main_view(main)
    mainloop()
else:
    # Select one of the following actions
    action = input("\nEnter action \n  Create network     (c) \n  Read database      (r) \
    \n  Modify existing db (m) \n  Verify user table  (v) \n  Query existing db  (q) \
    \n  Dump network db    (d) \n  Load network db    (l) \n  Stop and Exit      (s): ")
    while action != "s":
        if action == 'c':
            main.Gel_net = Semantic_Network(self.net_name, self.user)
            main.Create_net()
        if action == 'r': main.Read_db()
        if action == 'm': main.Modify_db()
        if action == 'v': main.Read_file()
        if action == 'q': main.Query_net()
        if action == 'd': main.Dump_net()
        if action == 'l': main.Load_net()
        if action == 's': main.Stop_Quit()
        
        action = input("\nEnter action \n  Create network     (c) \n  Read database      (r) \
        \n  Modify existing db (m) \n  Verify user table  (v) \n  Query existing db  (q) \
        \n  Dump network db    (d) \n  Load network db    (l) \n  Stop and Exit      (s): ")
#if main.db_opened == True: main.db_cursor.close()
