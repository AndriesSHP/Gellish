#!/usr/bin/python3
import sys
import os
import csv

from Database import *

class ImportInDatabase():
    """
    Read a file in a Gellish Expression Format.
    Rearrange in expressions and Store expressions in a Gellish database.
    """
    def __init__(self, fname):
        self.row0 = ["", 0,"", 0,"","", 0,"","", 0,\
                     "", 0,"", 0,"", 0,"", 0,"", 0,\
                     0 ,"","", 0,"","","", 0,"", 0,\
                     "", 0,"","","","", 0,"","","",\
                     "", 0,"", 0,"", 0,"","", 0, 0,\
                     "","","","",""]
        self.expIDs = [ 0, 69, 54, 71, 16, 39, 5,  43, 44, 2,\
                       101,72, 73, 19, 18, 1,  42, 60, 3,  85,\
                       74, 75, 45, 15, 201,65, 4,  66, 7,  76,\
                       77, 70, 20, 14, 8,  24, 67, 9,  23, 22,\
                       10, 11, 83, 6,  12, 78, 79, 13, 53, 50,\
                       68, 82, 80, 81, 84]
        try:
            f = open(fname, "r")
        except IOError:
            print("File '%s' does not exist or is not readable." % fname)
            sys.exit()
        
        # determine dialect
        sample = f.read(1024)
        dialect = csv.Sniffer().sniff(sample)
        
        # rewind to start
        f.seek(0)
        
        # initialise csv reading
        reader = csv.reader(f, dialect)
        
        # skip first line
        next(reader)
        
        # read line with field codes and convert them to integers
        sourceIDs = list(map(int, next(reader)))

        destIDs = []
        # For available data columnIDs in reader find the destination columnID
        for ID in sourceIDs:
            if ID in self.expIDs:
                destIDs.append(self.expIDs.index)
            else:
                print('\n Column ID %i is invalid. Column is ignored.' % (ID))
                destIDs.append(0)
        print('DestIDs: ',destIDs)

        # skip third line
        next(reader)

        # Data starts at 4th line
        for fields in reader:
            # put input fields in destination fields on row
            row = self.row0[:]
            for ID in destIDs:
                row[ID] = fields[destIDs.index]
        print('Row: ',row)

        tableName = "expressions"
        FED.InsertRowInTable(tableName, row)

        f.close()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    else:
        fname = os.path.join("Data", "Taxonomic Dictionary of Formal English (core).csv")
    importeer = ImportInDatabase(fname)
    
