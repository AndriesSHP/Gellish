#!/usr/bin/python3

import os
import sqlite3
#from copy import deepcopy
from SystemUsers import *
from DatabaseAPI import Database
from GellishDict import GellishDict
from SemanticNetwork import Semantic_Network
from Bootstrapping import *

def Build_Semantic_Network(gel_cur, net_name):

    # Create and initialize a Semantic Network with name net_name from database gel_cur
    network = Semantic_Network(net_name)
    # Read basic ontology table and build semantic network net_name from DB content
    table = 'base_ontology'
    network.Add_table_content_to_network(gel_cur, table)
    
    # Extent list of relation types, base phrases and inverse phrases
    #analyse = Analyse_base_ontology()
    network.rel_types = network.DetermineSubtypeList(5935)
    for rel in network.rel_types:
        network.rel_type_uids.append(rel.uid)
    print('  Network1: %s; nr of objects = %i; nr of rels = %i; nr of rel_types = %i' % \
          (network.name, len(network.objects), len(network.rels), len(network.rel_types)))

    # Extent network by reading domain dictionaries table from DB content
    table = 'domain_dictionaries'
    network.Add_table_content_to_network(gel_cur, table)
    print('  Network2: %s; nr of objects = %i; nr of rels = %i; nr of rel_types = %i' % \
          (network.name, len(network.objects), len(network.rels), len(network.rel_types)))
    
    # Extent network by reading product and process table from DB content
    table = 'productsANDprocesses'
    network.Add_table_content_to_network(gel_cur, table)
    print('  Network3 : %s; nr of objects = %i; nr of rels = %i; nr of rel_types = %i' % \
          (network.name, len(network.objects), len(network.rels), len(network.rel_types)))
    return network

def Connect_to_database(db_name):
    if db_name == ":memory:":
        dbConnect = sqlite3.connect(db_name)
    else:
        dbConnect = sqlite3.connect("%s.db3"% db_name)
    dbCursor  = dbConnect.cursor()
    return dbCursor

party = input("User name: ")
user = User(party)
users.append(user)
sesam = user.Providing_Access(party)
if sesam == False:
    exit(0)
GUI = GUI_Language(user.GUI_language)

net_name = "Gellish network"
# Select action: 'existing' or 'new'
action = input("\nEnter action: create new db (n), modify existing db (e) \
or query existing db (q) or stop (s): ")
# Enter database name
#db_name = input("Enter database name or memory (FE, m, ...): ")
db_name = "FormalEnglishDB-test"
#db_name = ":memory:"

while action != "s":
##    # Select database type: 'language definition', knowledge/requirements or product/process
##    if action == 'n':
##        db_type = input("Enter database type language (l) or knowledge (k) or requirements (r) or product (p): ")

    # Create new database and load with a language definition
    if action == 'n': # and db_type == 'l':
        # Remove the old database (if present) and create a new database with the same name.
        try:
            os.remove(db_name + ".db3")
        except OSError:
            pass
        Gel_db = Database(db_name)      # create a new database
        Gel_db.CreateTables()           # create empty tables
        print("Database: %s created." % (Gel_db.name))

        # Import a base ontology from file (specified in Bootstrapping)
        Gel_db.Import_Base_Ontology(GUI)
        Base_net = Gel_db.Build_Base_Semantic_Network() # to collect rel_type_uids for validation
        # Import domain dictionaries
        Gel_db.Import_Model_Files(dict_files, dict_dirs, GUI)
        gel_cur = Gel_db.dbCursor
        # Import product and process models
        Gel_db.Import_Model_Files(prod_files, prod_dirs, GUI)
        gel_cur = Gel_db.dbCursor

    # Extent existing database by loading knowledge and/or product files
    elif action == 'e': # and (db_type == 'k' or db_type == 'p'):
        # Connect to existing database
        # Enter database name
        #db_name  = 'FormalEnglishDB'
        #db_name  = 'RoadDB'
        db_name  = ':memory:'
        if db_name != ':memory:':
            dbCursor = Connect_to_database(db_name)
            print("Database: %s connected." % (db_name))
        Gel_db.Import_Model_Files(model_files, model_dirs, GUI)

    # Query the Semantic Network
    elif action == "q":
        # Connect to an existing database
        # Enter database name
        #db_name  = 'FormalEnglishDB'
        #db_name  = ':memory:'
        if db_name != ':memory:':
            dbCursor = Connect_to_database(db_name)
            print("Database: %s connected." % (db_name))
        
        # Build the Semantic Newtork from the database tables
        print("Build semantic network: %s." % (net_name))
        Gel_net = Build_Semantic_Network(dbCursor, net_name)
        
        # Search for data about kinds or individuals and display in various views
        # Query things in network
        string_commonalities = ['case sensitive partially identical', 'case sensitive identical']
        search_string = input("\nEnter a query string or 'quit': ")
        while search_string not in ["q", "quit", "e", "exit"]:
            # string commonalities: ci pi, cs pi, ci i, cs i, ci fi, cs fi ** TO BE DONE
            com = input("\nEnter string commonality (cs pi, cs i): ")
            if com == 'cs i':
                string_commonality = string_commonalities[1]
            else:
                string_commonality = string_commonalities[0]
            candidates = Gel_net.Query_Network(search_string, string_commonality)
            if len(candidates) > 0:
                for candidate in candidates:
                    obj_uid = candidate[1][0]
                    print("  Candidate %s %s" % (obj_uid, candidate[0][2]))
                obj_uid = input('\nEnter UID of selected candidate or "quit":')
                if obj_uid != 'quit':
                    obj = Gel_net.find_object(int(obj_uid))
                    s = obj.show(Gel_net)
            else:
                print("  No candidates found")
            search_string = input("\nEnter a query string or 'quit': ")
                
    action = input("\nEnter action: create new db (n), modify existing db (e) \
or query existing db (q) or stop (s): ")
dbCursor.close()
