#!/usr/bin/python3
import sys
import os
import csv

import ColNameIndexes as Ci
from Anything import *
from DatabaseAPI import *
from FormalLanguage import Language

class SemanticNetwork():
    """ Build a SemanticNetwork from a Gellish database:
        being a model containing things and their relations.
    """
    def __init__(self, net_name):
        self.name = net_name
        self.idea_uids     = []
        self.rel_type_uids = []
        self.obj_uids      = []
        self.rh_obj_uids   = []
        self.names_in_contexts = []
        
        self.dbConnect = sqlite3.connect("%s.db3"% DB_name)
        self.dbCursor  = self.dbConnect.cursor()
        # read whole database
        self.dbCursor.execute('select * from expressions')
        result = self.dbCursor.fetchall()
        
        for fields in result:
            # read the idea uid and name
            idea_uid = fields[idea_uid_col]
            idea_name = fields[idea_desc_col]
            lang_uid = fields[lang_uid_col]
            comm_uid = fields[comm_uid_col]

            lh_uid, lh_name = fields[lh_uid_col], fields[lh_name_col]
            rh_uid, rh_name = fields[rh_uid_col], fields[rh_name_col]
            rel_type_uid, rel_type_name = fields[rel_type_uid_col], fields[rel_type_name_col]
            phrase_type_uid = fields[phrase_type_uid_col]
            
            # create the idea if it does not exist
            if idea_uid in self.idea_uids:
                idea = self[idea_uid]
                print ("Idea ",idea," already exists, expression ignored.")
                continue
            else:
                idea = Idea(idea_uid)
                self[idea_uid] = idea
                self.idea_uids.append(idea_uid)
            
            # verify whether the relation type UID is defined in the current language definition:
            if rel_type_uid in self.rel_type_uids:
                rel_type = self.relation_types[rel_type_uid]
            else:
                print("Relation type (%i) %s does not exist (yet)" % (rel_type_uid, rel_type_name))
                continue

            # create the left and right objects if they do not exist
            if lh_uid in self.obj_uids or lh_uid in self.rh_obj_uids:
                lh = self[lh_uid]
                    
            else:
                lh = Object(lh_uid)
                self[lh_uid] = lh
                self.obj_uids.append(lh)
                lh_name_in_context = (lang_uid, comm_uid, lh_name)
                self.names_in_contexts.append(lh_name_in_context)

            if rh_uid in self.obj_uids or rh_uid in self.rh_obj_uids:
                rh = self[rh_uid]
            else:
                rh = Object(rh_uid)
                self[rh_uid] = rh
                self.rh_obj_uids.append(rh)
            
            # create the relation
            relation = Relation(idea, reltype, lh, rh)
            print(relation)
            # add the relation to both objects
            lh.add_relation(relation)
            rh.add_relation(relation)
        f.close()
        
    def query(self, qtext):
        results = []
        for k,v in self.items():
            if v.find(qtext) >= 0:
                results.append(k)
        return(results)
    
    def show_item(self, item):
        self[item].show()
        
if __name__ == "__main__":
    Gellish = Language("English", "English")
    net_name = 'Formal English'
    network = SemanticNetwork(net_name)
    
    qtext = input("enter query string: ")
    while qtext != "quit" and qtext != "exit":
        results = network.query(qtext)
        if len(results) > 0:
            for i in range(len(results)):
                print("%i  %s" % (i+1, str(network[results[i]])))
            item = int(input("enter result number: ")) -1
            while item >= 0:
                print("showing item %i" % (item+1))
                network.show_item(results[item])
                item = int(input("enter result number: "))-1
        qtext = input("enter query string: ")
