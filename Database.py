import sqlite3

class Database:
    def __init__(self, DBName):
        self.dbConnect = sqlite3.connect("%s.db3" % DBName)
        self.dbCursor  = self.dbConnect.cursor()

    def CreateExprTable(self, expressions):
        """ Create a generic Gellish SQL expression table in 'database' (cursor).
        The tableName is 'expressions'.
        """

        # Wat is hier het nut van? Je doet niets met tablename
        tableName = expressions

        self.dbCursor.execute('''CREATE TABLE expressions (
            presSeq        text,
            langUID        integer,
            langName       text,
            commUID        integer,
            commName       text,
            reality        text,
            lhUID          integer,
            lhCard         text,
            lhName         text,
            lhRoleUID      integer,
            lhRoleName     text,
            intentUID      integer,
            intentName     text,
            validUID       integer,
            validName      text,
            factUID        integer primary key,
            descFact       text,
            relUID         integer,
            relName        text,
            rhRoleUID      integer,
            rhRoleName     text,
            rhUID          integer,
            rhCard         text,
            rhName         text,
            partDef        text,
            fullDef        text,
            uomUID         integer,
            uomName        text,
            accUID         integer,
            accName        text,
            pickListUID    integer,
            pickListName   text,
            remarks        text,
            status         text,
            reason         text,
            succUID        integer,
            dateStartVal   text,
            dateStartAvail text,
            dateCreaCopy   text,
            dateLatCh      text,
            creatorUID     integer,
            creatorName    text,
            authLatChUID   integer,
            authLatChName  text,
            addrUID        integer,
            addrName       text,
            refs           text,
            exprUID        integer,
            collUID        integer,
            collName       text,
            fileName       text,
            lhStringComm   text,
            rhStringComm   text,
            relStringComm  text,
            inverseCode    integer,
            lhKindRoleUID  integer,
            lhKindRoleName text,
            rhKindRoleUID  integer,
            rhKindRoleName text)
            ''')                    # 59 columns (id 0..58)
        self.dbConnect.commit()

        # overbodig als je niets
        # return
#-------------------------------------------------------------
    def InsertRowInDB(self, row):
        """Insert one row of data in exprTable into Gellish DB with name 'databaseName'."""

        #dbConnect = sqlite3.connect(databaseName)

        # Insert row of data
        try:
            #self.dbCursor.execute("INSERT INTO expressions VALUES (?,?,?,?,?,?,?,?,?,?,\
            #                 ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
            #                 ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",row)
            # Dit is leesbaarder, bovendien klopte het aantal wildmarks niet:
            self.dbCursor.execute("INSERT INTO expressions VALUES (?%s)" % (58*",?"), row)
        except sqlite3.IntegrityError:
            print('ERROR: FactUID %i already exists' % (row[factUIDExC]))

        # Save (commit) the addition
        self.dbConnect.commit()

        return
#-------------------------------------------------------------
    def InsertRowsInDB(self, exprTable):
        """Insert a number of rows of data in exprTable into Gellish DB with name 'databaseName'."""

        #dbConnect = sqlite3.connect(databaseName)

        # Insert rows of data
        #self.dbCursor.executemany("INSERT INTO expressions VALUES (?,?,?,?,?,?,?,?,?,?,\
        #                     ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,\
        #                     ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",exprTable)
        # Dit is leesbaarder, bovendien klopte het aantal wildmarks niet:
        self.dbCursor.executemany("INSERT INTO expressions VALUES (?%s)" % (58*",?"), exprTable)

        # Save (commit) the additions
        self.dbConnect.commit()

        # overbodig
        # return
#-------------------------------------------------------------
    def SearchRowsInDB(self, criteria):
        """Search for rows in databaseName where criteria
        specifies a list of triples (colName,' and '/' or ',value) for matching.
        """

        #dbConnect = sqlite3.connect(databaseName)

        values = []
        first = True
        for crit in criteria:
            if first == True:
                query = 'select * from expressions where ' + crit[0] + '=?'
                values.append(crit[2])
                first = False
            else:
                query = query + crit[1] + crit[0] + '=?'
                values.append(crit[2])
        #print(query)
        #print(values)
        resultTable = []
        #for row in dbConnect.execute('select * from expressions where lhName=? and rhName=?',(values)):
        #for row in dbConnect.execute(query,(values)):
        #    resultTable.append(row)
        self.dbCursor.execute(query,(values))
        resultTable = self.dbCursor.fetchall()
        #print('resultTable:',resultTable)
        return(resultTable)
#-------------------------------------------------------------

if __name__ == "__main__":
    import os
    from copy import deepcopy
    # gooi de oude database weg omdat we anders geen table met de naam expressions kunnen maken:
    os.remove("FormalEnglish.db3")
    FED = Database("FormalEnglish")
    expressions = "expressions"
    FED.CreateExprTable(expressions)

    if True:
        row1 = []
        for i,c in enumerate("titittittititititititittttititittttittttititittiitttttiitit"):
            if c == "i":
                row1.append(i+1)
            else:
                row1.append(str(i+1))
        row1[33] = "34s1"
        # row 2,3 is twee keer row, op een paar velden na
        # make deep copy to create new rows instead of a new reference to row1
        row2 = deepcopy(row1)
        row2[0] = 2
        row2[15] = 116
        row2[33] = "34s2"
        row3 = deepcopy(row1)
        row3[0] = 3
        row3[15] = 216
        row3[33] = "34s3"
        rows = [row2, row3]
    else:
        # Dit is saai typen. En er zit nog een foutje in ook. Er zijn 59 velden.
        row = [1, "2", 3, "4","5",6,"7","8",9,"10",\
               11,"12",13,"14",15,"16",17,"18",19,"20",21,"22","23","24","25",26,"27",28,"29",30,\
               "31","32","33","34s1",35,"36","37","38","39",40,"41",42,"43",44,"45","46",47,48,"49","50",\
               "51","52","53",54,55,"56",57,"58"]
        rows = [(2, "2", 3, "4","5",6,"7","8",9,"10",\
               11,"12",13,"14",15,"116",17,"18",19,"20",21,"22","23","24","25",26,"27",28,"29",30,\
               "31","32","33","34s2",35,"36","37","38","39",40,"41",42,"43",44,"45","46",47,48,"49","50",\
               "51","52","53",54,55,"56",57,"58"),\
                (3, "2", 3, "4","5",6,"7","8",9,"10",\
               11,"12",13,"14",15,"216",17,"18",19,"20",21,"22","23","24","25",26,"27",28,"29",30,\
               "31","32","33","34s3",35,"36","37","38","39",40,"41",42,"43",44,"45","46",47,48,"49","50",\
               "51","52","53",54,55,"56",57,"58")]


    FED.InsertRowInDB(row1)
    FED.InsertRowsInDB(rows)
    # Dit doe je al in de Databasemethods. Die zijn juist bedoeld dit soort details weg te abstraheren
    # dbConnect.commit()
    criteria = [('lhName', ' and ', 9),('status',' and ', "34s2")]
    resultTable = FED.SearchRowsInDB(criteria)
    print(resultTable)



