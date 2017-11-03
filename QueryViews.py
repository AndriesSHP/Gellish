import os
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, filedialog
from operator import itemgetter
from Bootstrapping import ini_out_path
from Expr_Table_Def import *
#from SemanticNetwork import Semantic_Network
from QueryModule import Query
from ModelViews import Display_views
from Create_output_file import Create_gellish_expression, Convert_numeric_to_integer, Open_output_file

class Query_view():
    ''' Defines a query window for specification of queries in dictionary and models.'''
    def __init__(self, Gel_net, main):
        self.Gel_net = Gel_net
        self.main = main
        self.query = main.query
        self.root = main.root

        self.lang_name  = self.Gel_net.GUI_lang_name
        self.lang_uid   = self.Gel_net.GUI_lang_uid
        self.lang_index = self.Gel_net.GUI_lang_index

        self.views = Display_views(self.Gel_net, self.main)
        self.Gel_net.lh_options  = []
        self.Gel_net.rh_options  = []
        self.Gel_net.rel_options = []
        self.test = False
        self.reply_lang_names = ("English", "Nederlands",  "American",  "Chinese")
        self.reply_language = ['The reply language is', 'De antwoordtaal is']
        
    def Query_window(self):
        """Specify a Query with unknowns and possible multiline conditions."""
        self.test = False

    # Define defaults (initial options) for query
        lhTermListEN  = ['?','Paris', 'Eiffel tower', 'France']
        relTermListEN = ['?','is related to (a)','is related to', 'is classified as a', 'is located in', 'has as part']
        rhTermListEN  = ['?','city', 'tower', 'country']
        uomTermListEN = ['','inch','mi','s', 'degC', 'psi']

        lhTermListNL  = ['?','N51','Groningen','Parijs', 'Eiffeltoren', 'Frankrijk']
        relTermListNL = ['?','is een soort', 'is gerelateerd aan (een)', 'is gerelateerd aan', \
                         'is geclassificeerd als een', 'bevindt zich in', 'heeft als deel']
        rhTermListNL  = ['?','isolatieplaat','weg','dorp','stad','toren','land']
        uomTermListNL = ['','mm','m', 's','°C','bar']

        if self.lang_name == 'Nederlands' or 'Dutch':
            lhTermListD  = lhTermListNL
            relTermListD = relTermListNL
            rhTermListD  = rhTermListNL
            uomTermListD = uomTermListNL
        else:
            lhTermListD  = lhTermListEN
            relTermListD = relTermListEN
            rhTermListD  = rhTermListEN
            uomTermListD = uomTermListEN

        query_text = ["Query","Vraag"]
        self.QWindow = Toplevel(self.root)
        self.QWindow.title(query_text[self.lang_index])
        self.query_frame = ttk.Frame(self.QWindow)
        self.query_frame.grid (column=0,row=0,sticky=NSEW)
        self.query_frame.rowconfigure(35,weight=1)
        
        # Set default values in StringVar's
        self.q_lh_name_str  = StringVar(value=lhTermListD[0])
        self.q_rel_name_str = StringVar(value=relTermListD[0])
        self.q_rh_name_str  = StringVar(value=rhTermListD[0])
        self.q_uom_name_str = StringVar(value=uomTermListD[0])
        self.q_lh_uid_str   = StringVar(value='')
        self.q_rel_uid_str  = StringVar(value='')
        self.q_rh_uid_str   = StringVar(value='')
        self.q_uom_uid_str  = StringVar(value='')
        
        lhCondQStr  = []
        relCondQStr = []
        rhCondQStr  = []
        uomCondQStr = []
        for i in range(0,3):
            lhCondQStr.append (StringVar())
            relCondQStr.append(StringVar())
            rhCondQStr.append (StringVar())
            uomCondQStr.append(StringVar())
        
        lhTerm  = ["Left hand term"      ,"Linker term"]
        relTerm = ["Relation type phrase","Relatietype frase"]
        rhTerm  = ["Right hand term"     ,"Rechter term"]
        uomTerm = ["Unit of measure"     ,"Meeteenheid"]

    # Query variables widgets definition   
        lhNameLbl   = ttk.Label(self.query_frame,text=lhTerm [self.lang_index])
        lhUIDLbl    = ttk.Label(self.query_frame,text='UID:')
        relNameLbl  = ttk.Label(self.query_frame,text=relTerm[self.lang_index])
        rhNameLbl   = ttk.Label(self.query_frame,text=rhTerm [self.lang_index])
        uomNameLbl  = ttk.Label(self.query_frame,text=uomTerm[self.lang_index])
        self.q_lh_name_widget  = ttk.Combobox(self.query_frame,textvariable=self.q_lh_name_str ,\
                                              values=self.Gel_net.lh_terms ,width=30)
        self.q_rel_name_widget = ttk.Combobox(self.query_frame,textvariable=self.q_rel_name_str,\
                                              values=self.Gel_net.rel_terms,width=40)
        self.q_rh_name_widget  = ttk.Combobox(self.query_frame,textvariable=self.q_rh_name_str ,\
                                              values=self.Gel_net.rh_terms ,width=30)
        self.q_uom_name_widget = ttk.Combobox(self.query_frame,textvariable=self.q_uom_name_str,\
                                              values=self.Gel_net.uoms     ,width=10)
        self.q_lh_uid_widget   = ttk.Entry(self.query_frame,textvariable=self.q_lh_uid_str ,width=10)
        self.q_rel_uid_widget  = ttk.Entry(self.query_frame,textvariable=self.q_rel_uid_str,width=10)
        self.q_rh_uid_widget   = ttk.Entry(self.query_frame,textvariable=self.q_rh_uid_str ,width=10)
        self.q_uom_uid_widget  = ttk.Entry(self.query_frame,textvariable=self.q_uom_uid_str,width=10)

    # Bindings
        self.q_lh_uid_widget.bind  ("<KeyRelease>",self.Lh_uid_command)
        self.q_lh_name_widget.bind ("<KeyRelease>",self.LhSearchCmd)
        self.q_rel_name_widget.bind("<KeyRelease>",self.RelSearchCmd)
        self.q_rh_name_widget.bind ("<KeyRelease>",self.RhSearchCmd)
        self.q_lh_name_widget.bind ("<Double-Button-1>"  ,self.LhSearchCmd)
        self.q_rel_name_widget.bind("<Double-Button-1>"  ,self.RelSearchCmd)
        self.q_rh_name_widget.bind ("<Double-Button-1>"  ,self.RhSearchCmd)

        defText = ['Def. of left hand object:','Definitie van linker object:']
        fullDefQLbl = ttk.Label(self.query_frame,text=defText[self.lang_index])
        fullDefQStr = StringVar()
        self.q_full_def_widget = Text(self.query_frame,width=60,height=3,wrap="word")
        
        defQScroll  = ttk.Scrollbar(self.query_frame,orient=VERTICAL,command=self.q_full_def_widget.yview)
        self.q_full_def_widget.config(yscrollcommand=defQScroll.set)
    #
    # String commonality buttons
        #ImmediateSearchVar = BooleanVar()
        self.case_sensitive_var    = BooleanVar()
        self.first_char_match_var  = BooleanVar()
        #ExactMatchVar      = BooleanVar()
        #IncludeDescrVar    = BooleanVar()

        #ImmediateSearchVar.set(True)
        self.case_sensitive_var.set(True)
        self.first_char_match_var.set(True)
        #ExactMatchVar.set(False)
        #IncludeDescrVar.set(False)

        #immText   = ["Immediate Search","Direct zoeken"]
        caseText  = ["Case Sensitive"  ,"Hoofdletter gevoelig"]
        firstText = ["First Char Match","Eerste letter klopt"]
        #exactText = ["Exact Match"     ,"Preciese overeenstemming"]
        #ImmediateSearch = ttk.Checkbutton(self.query_frame, text=immText  [self.lang_index], \
        #                                  variable = ImmediateSearchVar, onvalue = True)
        CaseSensitive   = ttk.Checkbutton(self.query_frame, text=caseText [self.lang_index], \
                                          variable = self.case_sensitive_var,   onvalue = True)
        FirstCharMatch  = ttk.Checkbutton(self.query_frame, text=firstText[self.lang_index], \
                                          variable = self.first_char_match_var,  onvalue = True)
        #ExactMatch      = ttk.Checkbutton(self.query_frame, text=exactText[self.lang_index], \
        #                                  variable = ExactMatchVar,      onvalue = True)
        # Include searching in descriptions
        #IncludeDescr = ttk.Checkbutton(self.query_frame, text="Include Description", \
        #                               variable = IncludeDescrVar, onvalue = True)
        
    # Conditions widgets definition
        condit  = ["Conditions:"         ,"Voorwaarden:"]
        condLbl   = ttk.Label(self.query_frame,text=condit[self.lang_index])
        for i in range(0,3):
            self.query.lhCondVal.append (ttk.Combobox(self.query_frame,textvariable=lhCondQStr[i], \
                                                      values=self.Gel_net.lh_terms ,width=30))
            self.query.relCondVal.append(ttk.Combobox(self.query_frame,textvariable=relCondQStr[i],\
                                                      values=self.Gel_net.rel_terms,width=40))
            self.query.rhCondVal.append (ttk.Combobox(self.query_frame,textvariable=rhCondQStr[i], \
                                                      values=self.Gel_net.rh_terms ,width=30))
            self.query.uomCondVal.append(ttk.Combobox(self.query_frame,textvariable=uomCondQStr[i],\
                                                      values=self.Gel_net.uoms     ,width=10))
        
    # Options for selection Widgets definition
        selectTerm = ["Select one of each of the following options:","Kies één van de volgende opties:"]
        optLbl     = ttk.Label(self.query_frame,text=selectTerm[self.lang_index])

    # lh Options frame in query_frame for lh options Treeview
        lhOptFrame  = ttk.Frame(self.query_frame,borderwidth=3,relief='ridge')
        lhOptFrame.grid (column=0, row=15,columnspan=8,rowspan=5,sticky=NSEW)
        lhOptFrame.columnconfigure(0,minsize=10,weight=1)
        lhOptFrame.rowconfigure   (0,minsize=10,weight=1)

        leftCol = ['Left UID'    ,'Linker UID']
        relaCol = ['Relation UID','Relatie UID']
        righCol = ['Right UID'   ,'Rechter UID']
        nameCol = ['Name'        ,'Naam']
        kindCol = ['Kind'        ,'Soort']
        commCol = ['Community'   ,'Taalgemeenschap']
        langCol = ['Language'    ,'Taal']
        self.lh_options_tree = ttk.Treeview(lhOptFrame,columns=('UID','Name','Kind','Comm','Lang'),\
                                 displaycolumns=('UID','Name','Kind','Comm','Lang'),\
                                 selectmode='browse', height=3)
        self.lh_options_tree.heading('#0'     ,anchor=W)
        self.lh_options_tree.heading('UID'    ,text=leftCol[self.lang_index] ,anchor=W)
        self.lh_options_tree.heading('Name'   ,text=nameCol[self.lang_index] ,anchor=W)
        self.lh_options_tree.heading('Kind'   ,text=kindCol[self.lang_index] ,anchor=W)
        self.lh_options_tree.heading('Comm'   ,text=commCol[self.lang_index] ,anchor=W)
        self.lh_options_tree.heading('Lang'   ,text=langCol[self.lang_index] ,anchor=W)

        self.lh_options_tree.column ('#0'     ,width=10)
        self.lh_options_tree.column ('UID'    ,minwidth=40  ,width=80)
        self.lh_options_tree.column ('Name'   ,minwidth=100 ,width=200)
        self.lh_options_tree.column ('Kind'   ,minwidth=100 ,width=200)
        self.lh_options_tree.column ('Comm'   ,minwidth=80  ,width=160)
        self.lh_options_tree.column ('Lang'   ,minwidth=80  ,width=160)

        self.lh_options_tree.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=NSEW)

        self.lh_options_tree.columnconfigure(0,weight=0)
        self.lh_options_tree.columnconfigure(1,weight=1)
        self.lh_options_tree.columnconfigure(2,weight=1)
        self.lh_options_tree.columnconfigure(3,weight=1)
        self.lh_options_tree.columnconfigure(4,weight=1)
        self.lh_options_tree.columnconfigure(5,weight=1)
        self.lh_options_tree.rowconfigure(0,weight=1)

        lhOptScroll = ttk.Scrollbar(lhOptFrame,orient=VERTICAL,command=self.lh_options_tree.yview)
        lhOptScroll.grid (column=0,row=0,sticky=NS+E)
        self.lh_options_tree.config(yscrollcommand=lhOptScroll.set)

        self.lh_options_tree.bind(sequence='<Double-1>', func=self.Set_selected_q_lh_term)
    # = = = = = = = = =
    # rel Options frame in query_frame for rel options Treeview
        relOptFrame = ttk.Frame(self.query_frame,borderwidth=3,relief='ridge')
        relOptFrame.grid (column=0, row=20,columnspan=8,rowspan=5,sticky=NSEW)
        relOptFrame.columnconfigure(0,minsize=10,weight=1)
        relOptFrame.rowconfigure   (0,minsize=10,weight=1)
        
        #relOptVal = ttk.Combobox(self.query_frame,textvariable=relSelect, values=relOptionList,width=40, postcommand=UpdateRelNames)
        self.rel_options_tree = ttk.Treeview(relOptFrame,columns=('UID','Name','Kind','Comm','Lang'),\
                                displaycolumns='#all', selectmode='browse', height=3)
        self.rel_options_tree.heading('#0'     ,anchor=W)
        self.rel_options_tree.heading('UID'    ,text=relaCol[self.lang_index] ,anchor=W)
        self.rel_options_tree.heading('Name'   ,text=nameCol[self.lang_index] ,anchor=W)
        self.rel_options_tree.heading('Kind'   ,text=kindCol[self.lang_index] ,anchor=W)
        self.rel_options_tree.heading('Comm'   ,text=commCol[self.lang_index] ,anchor=W)
        self.rel_options_tree.heading('Lang'   ,text=langCol[self.lang_index] ,anchor=W)

        self.rel_options_tree.column ('#0'     ,width=10)
        self.rel_options_tree.column ('UID'    ,minwidth=40  ,width=80)
        self.rel_options_tree.column ('Name'   ,minwidth=100 ,width=200)
        self.rel_options_tree.column ('Kind'   ,minwidth=100 ,width=200)
        self.rel_options_tree.column ('Comm'   ,minwidth=80  ,width=160)
        self.rel_options_tree.column ('Lang'   ,minwidth=80  ,width=160)

        #relOptLbl.grid (column=0, row=0,sticky=EW)
        self.rel_options_tree.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=NSEW)

        self.rel_options_tree.columnconfigure(0,weight=0)
        self.rel_options_tree.columnconfigure(1,weight=1)
        self.rel_options_tree.columnconfigure(2,weight=1)
        self.rel_options_tree.columnconfigure(3,weight=1)
        self.rel_options_tree.columnconfigure(4,weight=1)
        self.rel_options_tree.columnconfigure(5,weight=1)
        self.rel_options_tree.rowconfigure(0,weight=1)

        relOptScroll = ttk.Scrollbar(relOptFrame,orient=VERTICAL,command=self.rel_options_tree.yview)
        relOptScroll.grid (column=0,row=0,sticky=NS+E)
        self.rel_options_tree.config(yscrollcommand=relOptScroll.set)

        self.rel_options_tree.bind(sequence='<Double-1>', func=self.Set_selected_q_rel_term)
    # = = = = = = = = =
    # rh Options frame in query_frame for rh options Treeview
        rhOptFrame  = ttk.Frame(self.query_frame,borderwidth=3,relief='ridge')
        rhOptFrame.grid (column=0, row=25,columnspan=8,rowspan=5,sticky=NSEW)
        rhOptFrame.columnconfigure(0,minsize=10,weight=1)
        rhOptFrame.rowconfigure   (0,minsize=10,weight=1)
        
        #rhOptVal  = ttk.Combobox(self.query_frame,textvariable=rhSelect,  values=rhOptionList, width=40, postcommand=UpdateRhNames)
        self.rh_options_tree = ttk.Treeview(rhOptFrame,columns=('UID','Name','Kind','Comm','Lang'),\
                                displaycolumns='#all', selectmode='browse', height=3)
        self.rh_options_tree.heading('#0'     ,anchor=W)
        self.rh_options_tree.heading('UID'    ,text=righCol[self.lang_index] ,anchor=W)
        self.rh_options_tree.heading('Name'   ,text=nameCol[self.lang_index] ,anchor=W)
        self.rh_options_tree.heading('Kind'   ,text=kindCol[self.lang_index] ,anchor=W)
        self.rh_options_tree.heading('Comm'   ,text=commCol[self.lang_index] ,anchor=W)
        self.rh_options_tree.heading('Lang'   ,text=langCol[self.lang_index] ,anchor=W)

        self.rh_options_tree.column ('#0'     ,width=10)
        self.rh_options_tree.column ('UID'    ,minwidth=40  ,width=80)
        self.rh_options_tree.column ('Name'   ,minwidth=100 ,width=200)
        self.rh_options_tree.column ('Kind'   ,minwidth=100 ,width=200)
        self.rh_options_tree.column ('Comm'   ,minwidth=80 ,width=160)
        self.rh_options_tree.column ('Lang'   ,minwidth=80 ,width=160)

        #rhOptLbl.grid (column=0, row=0,sticky=EW)
        self.rh_options_tree.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=NSEW)

        self.rh_options_tree.columnconfigure(0,weight=0)
        self.rh_options_tree.columnconfigure(1,weight=1)
        self.rh_options_tree.columnconfigure(2,weight=1)
        self.rh_options_tree.columnconfigure(3,weight=1)
        self.rh_options_tree.columnconfigure(4,weight=1)
        self.rh_options_tree.columnconfigure(5,weight=1)
        self.rh_options_tree.rowconfigure(0,weight=1)

        rhOptScroll = ttk.Scrollbar(rhOptFrame,orient=VERTICAL,command=self.rh_options_tree.yview)
        rhOptScroll.grid (column=0,row=0,sticky=NS+E)
        self.rh_options_tree.config(yscrollcommand=rhOptScroll.set)

        self.rh_options_tree.bind(sequence='<Double-1>', func=self.Set_selected_q_rh_term)
    # = = = = = = = = = = = = =
    # Buttons definition
        search = ['Search' ,'Zoek']
        close  = ['Close'  ,'Sluit']
        confirm= ['Confirm','Bevestig']
        verify = ['Verify model' ,'Verifieer model']
        #searchBut  = ttk.Button(self.query_frame,text=search[self.lang_index],  command=SearchButCmd)     # then Execute search
        closeBut   = ttk.Button(self.query_frame,text=close[self.lang_index],   command=self.Close_query)
        confirmBut = ttk.Button(self.query_frame,text=confirm[self.lang_index], command=self.Formulate_query_spec)
        verifyBut  = ttk.Button(self.query_frame,text=verify[self.lang_index],  command=self.query.Verify_model)
        
##    # Messages area - text widget definition
##        messText = ["Messages and warnings:","Berichten en foutmeldingen:"]
##        MessagesQLbl = ttk.Label(self.query_frame,text=messText[self.lang_index])
##        self.query.MessagesQ = Text(self.query_frame, width = 40, height = 10, background='#efc')
##        MessQScroll  = ttk.Scrollbar(self.query_frame,orient=VERTICAL,command=self.query.MessagesQ.yview)
##        self.query.MessagesQ.config(yscrollcommand=MessQScroll.set)
        
    # Buttons location in grid
        #ImmediateSearch.grid(column=0, columnspan=2,row=1,sticky=W)
        CaseSensitive.grid  (column=0, columnspan=2,row=1,sticky=W)
        FirstCharMatch.grid (column=0, columnspan=2,row=2,sticky=W)
        #ExactMatch.grid     (column=0, columnspan=2,row=3,sticky=W)
        #IncludeDescr.grid   (column=0,row=4,sticky=W)
    
    # Widget locations in grid
        lhNameLbl.grid  (column=0,row=3,sticky=W)
        lhUIDLbl.grid   (column=0,row=3,sticky=E)
        relNameLbl.grid (column=2,row=3,sticky=EW)
        rhNameLbl.grid  (column=4,row=3,sticky=EW)
        uomNameLbl.grid (column=6,row=3,sticky=EW)
        self.q_lh_name_widget.grid (column=0,row=4,columnspan=2, rowspan=1,sticky=EW)
        self.q_rel_name_widget.grid(column=2,row=4,columnspan=2, rowspan=1,sticky=EW)
        self.q_rh_name_widget.grid (column=4,row=4,columnspan=2, rowspan=1,sticky=EW)
        self.q_uom_name_widget.grid(column=6,row=4,columnspan=2, rowspan=1,sticky=EW)
        self.q_lh_uid_widget.grid  (column=1,row=3,columnspan=1, rowspan=1,sticky=EW)
        #self.q_rel_uid_widget.grid (column=2,row=5,columnspan=1, rowspan=1,sticky=EW)
        #self.q_rh_uid_widget.grid  (column=4,row=5,columnspan=1, rowspan=1,sticky=EW)
        #self.q_uom_uid_widget.grid (column=6,row=5,columnspan=1, rowspan=1,sticky=EW)
        fullDefQLbl.grid(column=0,row=5,rowspan=1,sticky=EW)
        self.q_full_def_widget.grid(column=1,row=5,columnspan=7,rowspan=1,sticky=EW)
        defQScroll.grid (column=7,row=5,rowspan=1,sticky=NS+E)

    # Conditions widgets location
        condLbl.grid  (column=0, row=7, columnspan=1, sticky=W)
        for i in range(0,3):
            rowNr = 11 + i
            self.query.lhCondVal[i].grid (column=0, row=rowNr, columnspan=2, rowspan=1, sticky=EW)
            self.query.relCondVal[i].grid(column=2, row=rowNr, columnspan=2, rowspan=1, sticky=EW)
            self.query.rhCondVal[i].grid (column=4, row=rowNr, columnspan=2, rowspan=1, sticky=EW)
            self.query.uomCondVal[i].grid(column=6, row=rowNr, columnspan=2, rowspan=1, sticky=EW)

    # Option Widgets location
        optLbl.grid    (column=0, row=14, columnspan=3, rowspan=1, sticky=EW)
        #lhOptLbl.grid  (column=0, row=15, columnspan=1, rowspan=1, sticky=EW)
        #relOptLbl.grid (column=0, row=17, columnspan=1, rowspan=1, sticky=EW)
        #rhOptLbl.grid  (column=0, row=19, columnspan=1, rowspan=1, sticky=EW)
        
##        MessagesQLbl.grid (column=0, row=30, columnspan=3, rowspan=1, sticky=EW)
##        self.query.MessagesQ.grid (column=0, row=31, columnspan=9, rowspan=1, sticky=NSEW)
##        MessQScroll.grid  (column=9, row=31, sticky=NS+E)
        
        #searchBut.grid (column=8, row=3 ,sticky=EW)
        closeBut.grid  (column=8, row=5 ,sticky=EW)
        confirmBut.grid(column=8, row=15,sticky=N+EW)
        verifyBut.grid (column=8, row=16 ,sticky=N+EW)

        self.QWindow.columnconfigure(0,weight=1)
        self.QWindow.rowconfigure(0,weight=1)
        
        self.query_frame.columnconfigure(0,weight=1)
        self.query_frame.columnconfigure(1,weight=1)
        self.query_frame.columnconfigure(2,weight=1)
        self.query_frame.columnconfigure(3,weight=1)
        self.query_frame.columnconfigure(4,weight=1)
        self.query_frame.columnconfigure(5,weight=1)
        self.query_frame.columnconfigure(6,weight=1)
        self.query_frame.columnconfigure(7,weight=1)
        self.query_frame.rowconfigure(1,weight=0)
        #self.query_frame.rowconfigure(11,weight=0)
        self.query_frame.rowconfigure(15,weight=1,minsize=25)     # self.lh_options_tree Treeview
        self.query_frame.rowconfigure(16,weight=1,minsize=25)     # lhlOptTree Treeview
        self.query_frame.rowconfigure(17,weight=1,minsize=25)     #  Treeview
        self.query_frame.rowconfigure(18,weight=1,minsize=25)     #  Treeview
        self.query_frame.rowconfigure(19,weight=1,minsize=25)     #  Treeview
        self.query_frame.rowconfigure(20,weight=1,minsize=25)     # self.rel_options_tree Treeview
        self.query_frame.rowconfigure(21,weight=1,minsize=25)     #  Treeview
        self.query_frame.rowconfigure(22,weight=1,minsize=25)     #  Treeview
        self.query_frame.rowconfigure(23,weight=1,minsize=25)     # self.rel_options_tree Treeview
        self.query_frame.rowconfigure(24,weight=1,minsize=25)     # self.rel_options_tree Treeview
        self.query_frame.rowconfigure(25,weight=1,minsize=25)     # self.rh_options_tree Treeview
        self.query_frame.rowconfigure(26,weight=1,minsize=25)     # self.rh_options_tree Treeview
        self.query_frame.rowconfigure(27,weight=1,minsize=25)     #  Treeview
        self.query_frame.rowconfigure(28,weight=1,minsize=25)     #  Treeview
        self.query_frame.rowconfigure(29,weight=1,minsize=25)     #  Treeview
        self.query_frame.rowconfigure(30,weight=1,minsize=25)     #  
        self.query_frame.rowconfigure(31,weight=1,minsize=25)     #  
        self.query_frame.rowconfigure(32,weight=1,minsize=20)

    # Define reply language with language selector
        lang_text = ['Reply language:', 'Antwoordtaal:']
        self.reply_lang_label = Label(self.query_frame, text=lang_text[self.lang_index], width=15)
        self.rep_lang_default = StringVar(value=self.Gel_net.GUI_lang_name)
        self.reply_lang_box   = ttk.Combobox(self.query_frame, textvariable=self.rep_lang_default,\
                                         values=self.reply_lang_names, width=10)
        self.reply_lang_label.grid(column=5, row=1, sticky=W)
        self.reply_lang_box.grid  (column=6, row=1, sticky=W)

        # Binding GUI language choice
        self.reply_lang_box.bind  ("<<ComboboxSelected>>",self.Determine_reply_language)

        # Set the reply language initially identical to the GUI language
        self.Gel_net.Set_reply_language(self.Gel_net.GUI_lang_name)
        print('{} {}'.format(self.reply_language[self.lang_index], self.Gel_net.reply_lang_name))

    def Determine_reply_language(self, event):
        reply_lang_name  = self.reply_lang_box.get()
        self.Gel_net.Set_reply_language(reply_lang_name)
        print('{} {}'.format(self.reply_language[self.lang_index], self.Gel_net.reply_lang_name))

    def Lh_uid_command(self, event):
        """Search for UID in semantic network
        Search in vocabulary for left hand uid.
    == OptionsTable: optionNr,whetherKnown,langUIDres,commUIDres,resultString,resultUID,isCalledUID,kindKnown,kind
    """
        #print('Lh uid entry:',event.char)

        # Delete previous options
        self.Gel_net.lh_options[:]  = []
        x = self.lh_options_tree.get_children()
        for item in x: self.lh_options_tree.delete(item)
        
        # Determine lh_options for lh uid in query
        lh_uid = self.q_lh_uid_widget.get()
##        if lh_uid_string.isdecimal():
##            lh_uid = lh_uid_string
##        else:
##            print('UID {} should be a whole number'.format(lh_uid_string))
##            return
        try:
            lh = self.Gel_net.uid_dict[lh_uid]
            
            #print("  Found lh: ", lh_uid, lh.name)
            # => lh_options: optionNr, whetherKnown, langUIDres, commUIDres, resultString,\
            #                resultUID, isCalledUID, kindKnown, kind
            if len(lh.names_in_contexts) > 0:
                #print('Lang_prefs:', self.Gel_net.reply_lang_pref_uids)
                #print('Names in contexts:', lh.names_in_contexts)
                # Build option with preferred name from names_in_contexts
                # Determine the full definition of the obj in the preferred language
                lang_name, comm_name, preferred_name, full_def = \
                           self.Gel_net.Determine_name_in_language_and_community(lh)
                option = [1, 'known'] + [lang_name, comm_name, preferred_name] \
                         + [lh.uid, '5117', 'known', lh.kind.name]
                #print('Lh_option', option)
                self.Gel_net.lh_options.append(option)
                opt = [option[5],option[4],option[8],comm_name,lang_name]
                self.lh_options_tree.insert('',index='end',values=opt)

                # Display lh_object uid
                self.query.q_lh_uid = lh_uid
                self.q_lh_uid_str.set(str(lh_uid))
                
            # delete earlier definition text. Then replace by new definition text
            self.q_full_def_widget.delete('1.0', END)
            # Display full definition
            self.q_full_def_widget.insert('1.0',full_def)
        except KeyError:
            pass

    def LhSearchCmd(self, event):
        """ Search or Query in semantic network
        An entry in QueryWindow can be just a name (lhString (for search on UID see Lh_uid_command)
        or a full question with possible condition expressions:
        (lhString,relString,rhString optionally followed by one or more conditions):
       
        lhCommonality = case sensitivity: 'cs/ci'; (partially/front end) identical 'i/pi/fi'
        lhCommonality = input('Lh-commonality (default: csfi-case sensitive, front-end identical): ')

        Search in vocabulary for left hand term as part of building a question.

    == OptionsTable: optionNr,whetherKnown,langUIDres,commUIDres,resultString,resultUID,isCalledUID,kindKnown,kind
    """
        self.test = False
        #print('Lh name entry:',event.char)
        #if event.keysym not in ['Shift_L', 'Shift_R']:
                                    
        case_sens   = self.case_sensitive_var.get()
        if case_sens:
            cs = 'cs'   # case sensitive
        else:
            cs = 'ci'   # case insensitive
        front_end = self.first_char_match_var.get()
        if front_end:
            fe = 'fi'   # front end identical
        else:
            fe = 'pi'   # part identical
        string_commonality = cs + fe

        self.query.q_lh_uid = 0
        self.Gel_net.lh_options[:]  = []
        
        # Remove possible earlier options
        x = self.lh_options_tree.get_children()
        for item in x: self.lh_options_tree.delete(item)
        
        # Determine lh_options for lh term in query
        lhString = self.q_lh_name_widget.get()
        self.found_lh_uid, self.Gel_net.lh_options = self.Gel_net.SolveUnknown(lhString, string_commonality)
        #print("  Found lh: ", lhString, self.Gel_net.unknown_quid, self.Gel_net.lh_options[0:3])

        # => lh_options: optionNr, whetherKnown, langUIDres, commUIDres, resultString,\
        #                resultUID, isCalledUID, kindKnown, kind
        # Sort the list of options alphabetically by name, determine lang_names and display options
        if len(self.Gel_net.lh_options) > 0:
            if len(self.Gel_net.lh_options) > 1:
                # sort by name
                self.Gel_net.lh_options.sort(key=itemgetter(4))
            # Find lang_name and comm_name from uids for option display
            for option in self.Gel_net.lh_options:
                if option[2] == '':
                    lang_name = 'unknown'
                else:
                    if self.lang_index == 1:
                        lang_name = self.Gel_net.lang_dict_NL[option[2]]
                    else:
                        lang_name = self.Gel_net.lang_dict_EN[option[2]]
                if option[3] == '':
                    comm_name = 'unknown'
                else:
                    comm_name = self.Gel_net.community_dict[option[3]]

                # Display option in lh_options_tree
                opt = [option[5],option[4],option[8],comm_name,lang_name]
                self.lh_options_tree.insert('',index='end',values=opt)

            # Display lh_object uid
            self.query.q_lh_uid = self.Gel_net.lh_options[0][5]
            self.q_lh_uid_str.set(str(self.query.q_lh_uid))
            
        # Delete earlier definition text. Then replace by new definition text
        self.q_full_def_widget.delete('1.0', END)
        full_def = ''
        int_q_lh_uid, integer = Convert_numeric_to_integer(self.query.q_lh_uid)
        if integer == False or int_q_lh_uid >= 100:
            # If lh_object is known then determine and display full definition
            self.query.q_lh_category = self.Gel_net.lh_options[0][8]
            obj = self.Gel_net.uid_dict[self.query.q_lh_uid]
            # Determine the full definition of the obj in the preferred language
            lang_name, comm_name, preferred_name, full_def = \
                       self.Gel_net.Determine_name_in_language_and_community(obj)
        # Display full definition
        self.q_full_def_widget.insert('1.0',full_def)
            
#----------------------------------------------------------------------
    def RelSearchCmd(self, event):
        """Search or Query in Ontology and Model
         Entry in QueryWindow is a question with possible condition expressions (lhString,relString,rhString):
       
           lhCommonality = 'csfi'
           lhCommonality = input('Lh-commonality (default: csfi-case sensitive, front-end identical): ')

         Search in vocabulary for left hand, relation type and right hand terms 
         and build a question

        == Options: optionNr,whetherKnown,langUIDres,commUIDres,resultString,resultUID,isCalledUID,kindKnown,kind
        """
        self.test = False

        if self.test: print('Rel Entry:',event.char)
        if event.keysym not in ['Shift_L', 'Shift_R']:

            front_end = self.first_char_match_var.get()
            case_sens = self.case_sensitive_var.get()

            # Delete previous list of rel_options in tree
            self.Gel_net.rel_options[:] = []
            x = self.rel_options_tree.get_children()
            for item in x: self.rel_options_tree.delete(item)
            
            # Get relation type name (relString) from user interface
            relString    = self.q_rel_name_widget.get()
            #if event != '': relString = relString # + event.char
            if relString == 'any':
                if self.lang_index == 1:
                    relString = 'binaire relatie'
                else:
                    relString = 'binary relation'
                self.q_rel_name_widget.set(relString)
            if relString == '':
                relString = 'binary relation'
            string_commonality = 'csfi'
            self.foundRel, self.Gel_net.rel_options = self.Gel_net.SolveUnknown(relString, string_commonality)
            #print('  OptRel:',self.Gel_net.rel_options)
            
            # == rel_opions: optionNr,whetherKnown,langUIDres,commUIDres,resultString,resultUID,isCalledUID,kindKnown,kind 
            # If rel_options are available, then sort the list and display in rel_options tree
            if len(self.Gel_net.rel_options) > 0:
                self.query.q_rel_uid = self.Gel_net.rel_options[0][5]
                int_q_rel_uid, integer = Convert_numeric_to_integer(self.query.q_rel_uid)
                if integer == False or self.query.q_rel_uid > 100:
                    obj = self.Gel_net.uid_dict[self.query.q_rel_uid]
                    self.q_rel_uid_str.set(str(self.query.q_rel_uid))
                if len(self.Gel_net.rel_options) > 1:
                    # Sort the list of options alphabetically by name
                    self.Gel_net.rel_options.sort(key=itemgetter(4))
                for option in self.Gel_net.rel_options:
                    if option[2] == 0:
                        lang_name = 'unknown'
                    else:
                        lang_name = self.Gel_net.lang_uid_dict[option[2]]
                    if option[3] == 0:
                        comm_name = 'unknown'
                    else:
                        comm_name = self.Gel_net.community_dict[option[3]]
                    opt = [option[5],option[4],option[8],comm_name,lang_name]
                    self.rel_options_tree.insert('',index='end',values=opt)        
#------------------------------------------------------------------
    def RhSearchCmd(self, event):
        """ Search or Query in Ontology and Model
            An entry in QueryWindow (lhString,relString,rhString)
            is a question with possible condition expressions:
       
            rhCommonality = input('Rh-commonality (default: csfi-case sensitive, front-end identical): ')

            Search for string in vocabulary for candidates for right hand term 
            and build a question

        == Options: optionNr,whetherKnown,langUIDres,commUIDres,resultString,resultUID,isCalledUID,kindKnown,kind
        """
        #print('Rh Entry:',event.char)
        if event.keysym not in ['Shift_L', 'Shift_R']:

            case_sens = self.case_sensitive_var.get()
            front_end = self.first_char_match_var.get()
            if case_sens:
                cs = 'cs'   # case sensitive
            else:
                cs = 'ci'   # case insensitive
            if front_end:
                fe = 'fi'   # front end identical
            else:
                fe = 'pi'   # part identical
            string_commonality = cs + fe

            # Delete previous items in the rh_options in tree
            self.Gel_net.rh_options[:]  = []
            x = self.rh_options_tree.get_children()
            for item in x: self.rh_options_tree.delete(item)

            # Get the rh_string and search for options in the dictionary
            rhString = self.q_rh_name_widget.get()
            self.foundRh, self.Gel_net.rh_options = self.Gel_net.SolveUnknown(rhString, string_commonality)
            #print('  OptRh:',self.Gel_net.rh_options);

            # == rh_options: optionNr,whetherKnown,langUIDres,commUIDres,resultString,resultUID,isCalledUID,kindKnown,kind
            # If rh_options are available, sort the list and display them in the rh_options tree
            if len(self.Gel_net.rh_options) > 0:
                self.query.q_rh_uid = self.Gel_net.rh_options[0][5]
                #obj = self.Gel_net.uid_dict[self.query.q_rh_uid]
                self.q_rh_uid_str.set(str(self.query.q_rh_uid))            
                self.query.q_rh_category = self.Gel_net.rh_options[0][8]
                if len(self.Gel_net.rh_options) > 1:
                    # Sort the list of options alphabetically by name
                    self.Gel_net.rh_options.sort(key=itemgetter(4))   # sort by name
                for option in self.Gel_net.rh_options:
                    if option[2] == 0:
                        lang_name = 'unknown'
                    else:
                        lang_name = self.Gel_net.lang_uid_dict[option[2]]
                    if option[3] == 0:
                        comm_name = 'unknown'
                    else:
                        comm_name = self.Gel_net.community_dict[option[3]]
                    opt = [option[5],option[4],option[8],comm_name,lang_name]
                    self.rh_options_tree.insert('',index='end',values=opt)
#----------------------------------------------------
    def Set_selected_q_lh_term(self, ind):
        """ Put the lhObject that is selected from lhOptions
            in the query (self.q_lh_name_str and self.q_lh_uid_str) and display its textual definition.
            Then determine the kinds of relations that relate to that lh_object or its subtypes
        """
        item  = self.lh_options_tree.selection()
        ind   = self.lh_options_tree.index(item)
        self.query.lhSel = self.Gel_net.lh_options[ind]
        self.query.q_lh_uid  = self.query.lhSel[5]    # Determine UID and Name of selected option
        self.query.q_lh_name = self.query.lhSel[4]
        self.q_lh_uid_str.set(str(self.query.q_lh_uid))
        self.q_lh_name_str.set(self.query.q_lh_name)
        self.q_full_def_widget.delete('1.0',END)
        
        full_def = ''
        # Determine the selected object via its uid
        int_q_lh_uid, integer = Convert_numeric_to_integer(self.query.q_lh_uid)
        if integer == False or int_q_lh_uid >= 100:                 # if not unknown
            self.query.q_lh_category = self.query.lhSel[8]
            obj = self.Gel_net.uid_dict[self.query.q_lh_uid]
            
            # Determine the full definition of the selected object in the preferred language
            lang_name, comm_name, preferred_name, full_def = \
                       self.Gel_net.Determine_name_in_language_and_community(obj)
            #print('FullDef:',self.query.q_lh_uid, self.query.q_lh_name,self.query.q_lh_category,full_def)
        # Display full definition
        self.q_full_def_widget.insert('1.0',full_def)

        # If the lh_object is known, then determine the kinds of relations that relate to that lh_object
        is_called_uid = '5117'
        if integer == False or int_q_lh_uid >= 100:
            rel_options = []
            #opt_nr = 0
            lh_object = self.Gel_net.uid_dict[self.query.q_lh_uid]
            # Determine list of subtypes of the lh_object
            sub_types, sub_type_uids = self.Gel_net.Determine_subtypes(lh_object)
            sub_types.append(lh_object)
            for lh_obj_sub in sub_types:
                # Determine rel types and store results in self.lh_obj_relation_types
                self.Gel_net.Determine_rel_types_for_lh_object(lh_obj_sub)
                
                # Create option list for each found kind of relation
                for rel_type in self.Gel_net.lh_obj_relation_types:
                    if len(rel_type.basePhrases_in_context) > 0:
                        for phrase_in_context in rel_type.basePhrases_in_context:
                            # If language of phrase is as requested
                            if phrase_in_context[0] == self.lang_uid:
                                rel_option = phrase_in_context[2]
        ##                        opt_nr += + 1
        ##                        #rel_option: optionNr, whetherKnown, lang_uid, comm_uid, resultString,\
        ##                        #            resultUID, is_called_uid, kindKnown, kind
        ##                        rel_option = [opt_nr, 'known', lang_uid, comm_uid, phrase_in_context[2], \
        ##                                      lh_object.uid, is_called_uid, '', '']
                                if rel_option not in rel_options:
                                    rel_options.append(rel_option)
                                    #print('Rel type option:', rel_option)
                    elif len(rel_type.inversePhrases_in_context) > 0:
                        for phrase_in_context in rel_type.inversePhrases_in_context:
                            if phrase_in_context[0] == self.lang_uid:
                                rel_option = phrase_in_context[2]
        ##                        opt_nr += + 1
        ##                        #rel_option: optionNr, whetherKnown, lang_uid, comm_uid, resultString,\
        ##                        #            resultUID, is_called_uid, kindKnown, kind
        ##                        rel_option = [opt_nr, 'known', lang_uid, comm_uid, phrase_in_context[2], \
        ##                                      lh_object.uid, is_called_uid, '', '']
                                if rel_option not in rel_options:
                                    rel_options.append(rel_option)
                                    print('Rel type option:', rel_option)
            rel_options.sort()
            self.Gel_net.rel_terms = rel_options
            self.q_rel_name_widget.config(values=self.Gel_net.rel_terms)

    #--------------------------------------------------------------------------------
    def Set_selected_q_rel_term(self, ind):
        """ Put the selected relObject name and uid from relOptions
            in query (self.q_rel_name_str and self.q_rel_uid_str).
            Then determine the rh_objects that are related to the lh_object by such a relation or its subtypes
        """
        item   = self.rel_options_tree.selection()
        ind    = self.rel_options_tree.index(item)
        self.query.relSel = self.Gel_net.rel_options[ind]
        # Determine UID and Name of selected option
        self.query.q_rel_uid  = self.query.relSel[5]
        self.query.q_rel_name = self.query.relSel[4]
        self.q_rel_uid_str.set(str(self.query.q_rel_uid))
        self.q_rel_name_str.set(self.query.q_rel_name)
        if self.query.q_rel_name in self.Gel_net.base_phrases:
            self.query.q_phrase_type_uid = '6066'

        # Determine the rh_objects in the query that are related by selected rel_object type or its subtypes
        # to the lh_object or its subtypes in the query
        int_q_lh_uid, integer = Convert_numeric_to_integer(self.query.q_lh_uid)
        if integer == False or int_q_lh_uid >= 100:
            rh_options = []
            # Determine list of subtypes of the rel_object
            q_rel_object = self.Gel_net.uid_dict[self.query.q_rel_uid]
            q_rel_sub_types, q_rel_sub_type_uids = self.Gel_net.Determine_subtypes(q_rel_object)
            q_rel_sub_types.append(q_rel_object)
            # Determine list of subtypes of the lh_object
            q_lh_obj = self.Gel_net.uid_dict[self.query.q_lh_uid]
            q_lh_sub_types, q_lh_sub_type_uids = self.Gel_net.Determine_subtypes(q_lh_obj)
            q_lh_sub_types.append(q_lh_obj)
            # For each relation of an lh_subtype verify if the relation type (rel_type_uid)
            # corresponds with the relation type of the query or one of its rel_subtypes.
            # If yes, then collect the rh_name in the list of rh_options.
            for lh_sub in q_lh_sub_types:
                for lh_sub_rel in lh_sub.relations:
                    expr = lh_sub_rel.expression
                    for rel_sub in q_rel_sub_types:
                        # Check if the relation types correspond
                        if expr[rel_type_uid_col] == rel_sub.uid:
                            # If the base relation corresponds the collect the rh name, if not yet present
                            if expr[lh_uid_col] == lh_sub.uid:
                                if expr[rh_name_col] not in rh_options:
                                    rh_options.append(expr[rh_name_col])
                            # If the inverse corresponds
                            elif expr[rh_uid_col] == lh_sub.uid:
                                if expr[lh_name_col] not in rh_options:
                                    rh_options.append(expr[lh_name_col])
                            print('expr[lh_name_col], expr[rh_name_col]', expr[lh_name_col], expr[rh_name_col])
            rh_options.sort()
            self.Gel_net.rh_terms = rh_options
            self.q_rh_name_widget.config(values=self.Gel_net.rh_terms)

    #--------------------------------------------------------------------------------
    def Set_selected_q_rh_term(self, ind):
        """Put the selection of rhObject in self.q_rh_name_str and self.q_rh_uid_str"""
        
        item  = self.rh_options_tree.selection()
        ind   = self.rh_options_tree.index(item)
        self.query.rhSel = self.Gel_net.rh_options[ind]
        self.query.q_rh_uid  = self.query.rhSel[5]    # Determine UID and Name of selected option
        self.query.q_rh_name = self.query.rhSel[4]
        self.q_rh_uid_str.set(str(self.query.q_rh_uid))
        self.q_rh_name_str.set(self.query.q_rh_name)

    def Formulate_query_spec(self):
        """Formulte a query_spec on the network for the relation type and its subtypes.
           Store resulting query expressions in candids table with the same table definition.
        """
        # Make query_spec empty
        self.main.query_spec[:]    = []
        self.Gel_net.ex_candids[:] = []
        
        # LH: Get selected option (textString) from the presented list of options (lh_options_tree) in QueryWindow
        lhUIDInit = self.q_lh_uid_widget.get()
        if lhUIDInit == '':
            print('Warning: Left hand option not yet selected. Please try again.')
            #self.query.MessagesQ.insert('end','\nLeft hand option not yet selected. Please try again.')
            return
        item  = self.lh_options_tree.selection()
        ind   = self.lh_options_tree.index(item)
        # => lh_options: optionNr, whetherKnown, langUIDres, commUIDres, resultString,\
        #                resultUID, isCalledUID, kindKnown, kind
        self.query.lhSel = self.Gel_net.lh_options[ind]
        #print('Selected option:',item, ind, self.query.lhSel)

        # Determine UID and Name of selected lh option and formulate query expression (query_expr)
        self.query.q_lh_uid  = self.query.lhSel[5]
        self.query.q_lh_name = self.query.lhSel[4]
        self.q_lh_uid_str.set(str(self.query.q_lh_uid))
        self.q_lh_name_str.set(self.query.q_lh_name)
        self.query.query_expr = [self.query.q_lh_uid, self.query.q_lh_name]

        # Delete earlier definition text in query_window.
        self.q_full_def_widget.delete('1.0', END)
        
        # If lh_object is known then determine and display its full definition
        int_q_lh_uid, integer = Convert_numeric_to_integer(self.query.q_lh_uid)
        if integer == False or int_q_lh_uid >= 100:
            self.query.q_lh_obj = self.Gel_net.uid_dict[self.query.q_lh_uid]
            self.query.q_lh_category = self.Gel_net.lh_options[0][8]

            # Determine the full definition of the selected object in the preferred language
            lang_name, comm_name, preferred_name, full_def = \
                       self.Gel_net.Determine_name_in_language_and_community(self.query.q_lh_obj)
            #print('Full def:', self.query.q_lh_uid, lhString, self.query.q_lh_category, full_def)
            # Display full definition
            self.q_full_def_widget.insert('1.0',full_def)
            
        # Rel: Selected relation type option
        # Verify whether only lh is selected.
        #   If yes then formulate query, else determine rel and rh part of query expression 
        relUIDInit = self.q_rel_uid_widget.get()
        #print('relUIDInit', relUIDInit)
        if relUIDInit == '':
            print('Relation type option is not (yet) selected.')
            #self.query.MessagesQ.insert('end','\nRelation type option is not (yet) selected.')
        else:
            # There is a kind of relation specified. Identify its uid and name
            item   = self.rel_options_tree.selection()
            ind    = self.rel_options_tree.index(item)
            print('rel_ind', ind, self.Gel_net.rel_options)
            self.query.relSel = self.Gel_net.rel_options[ind]
            
            self.query.q_rel_uid  = self.query.relSel[5]
            self.query.q_rel_name = self.query.relSel[4]
            self.q_rel_uid_str.set(str(self.query.q_rel_uid))
            self.q_rel_name_str.set(self.query.q_rel_name)

            int_q_rel_uid, integer = Convert_numeric_to_integer(self.query.q_rel_uid)
            if integer == False or int_q_rel_uid >= 100:
                self.query.q_rel_obj = self.Gel_net.uid_dict[self.query.q_rel_uid]
            
                # Determine phraseTypeUID of self.query.q_rel_name
                self.query.q_phrase_type_uid = 0
                if self.query.q_rel_name in self.Gel_net.base_phrases:
                    self.query.q_phrase_type_uid = '6066'   # base phrase
                else:
                    self.query.q_phrase_type_uid = '1986'   # inverse phrase
                
                # Determine role_players_types because of q_rel_type
                self.query.rolePlayersQTypes = self.query.q_rel_obj.role_players_types
                self.query.rolePlayerQTypeLH = self.query.q_rel_obj.role_player_type_lh
                self.query.rolePlayerQTypeRH = self.query.q_rel_obj.role_player_type_rh
                # 6068 = binary relation between an individual thing and any (kind or individual)
                if self.query.rolePlayersQTypes == 'individualsOrMixed':  # is related to (a)
                    #print('self.query.rolePlayers-IndividualsOrMixed:',self.query.rolePlayersQTypes,self.query.q_rel_name,self.Gel_net.base_phrases)
                    if self.query.q_rel_name in self.Gel_net.base_phrases:
                        self.query.rolePlayersQTypes = 'individualAndMixed'
                        self.query.rolePlayerQTypeLH = 'individual'
                        self.query.rolePlayerQTypeRH = 'mixed'
                    else:
                        self.query.rolePlayersQTypes = 'mixedAndIndividual'
                        self.query.rolePlayerQTypeLH = 'mixed'
                        self.query.rolePlayerQTypeRH = 'individual'
                # Binary relation between an individual thing and a kind
                elif self.query.rolePlayersQTypes == 'mixed':
                    if self.query.q_rel_name in self.Gel_net.base_phrases:
                        self.query.rolePlayersQTypes = 'individualAndKind'
                        self.query.rolePlayerQTypeLH = 'individual'
                        self.query.rolePlayerQTypeRH = 'kind'
                    else:
                        self.query.rolePlayersQTypes = 'kindAndIndividual'
                        self.query.rolePlayerQTypeLH = 'kind'
                        self.query.rolePlayerQTypeRH = 'individual'
                # 7071 = binary relation between a kind and any (kind or individual)
                elif self.query.rolePlayersQTypes == 'kindsOrMixed':  # can be related to (a)
                    if self.query.q_rel_name in self.Gel_net.base_phrases:
                        self.query.rolePlayersQTypes = 'kindsAndMixed'  # can be related to (a)
                        self.query.rolePlayerQTypeLH = 'kind'
                        self.query.rolePlayerQTypeRH = 'mixed'
                    else:
                        self.query.rolePlayersQTypes = 'mixedAndKind'  # is or can be related to a
                        self.query.rolePlayerQTypeLH = 'mixed'
                        self.query.rolePlayerQTypeRH = 'kind'
                else:
                    pass

            # RH: Selected right hand option
            rhUIDInit = self.q_rh_uid_widget.get()
            if rhUIDInit == '':
                print('Right hand option not (yet) selected.')
                #self.query.MessagesQ.insert('end','\nRight hand option not (yet) selected.')
            else:
                # There is a rh name specified. Determine its name and uid and identity
                item  = self.rh_options_tree.selection()
                ind   = self.rh_options_tree.index(item)
                self.query.rhSel = self.Gel_net.rh_options[ind]
                
                self.query.q_rh_uid  = self.query.rhSel[5]
                self.query.q_rh_name = self.query.rhSel[4]
                self.q_rh_uid_str.set(str(self.query.q_rh_uid))
                self.q_rh_name_str.set(self.query.q_rh_name)

                int_q_rh_uid, integer = Convert_numeric_to_integer(self.query.q_rh_uid)
                if integer == False or int_q_rh_uid >= 100:
                    self.query.q_rh_obj = self.Gel_net.uid_dict[self.query.q_rh_uid]
                    
                # Report final query
                queryText = ['Query ','Vraag   ']
                self.views.log_messages.insert('end','\n\n{}: {} ({}) {} ({}) {} ({})'.format\
                                        (queryText[self.lang_index], \
                                         self.query.q_lh_name , self.query.q_lh_uid,\
                                         self.query.q_rel_name, self.query.q_rel_uid,\
                                         self.query.q_rh_name , self.query.q_rh_uid))
                self.query.query_expr = [self.query.q_lh_uid , self.query.q_lh_name, \
                                         self.query.q_rel_uid, self.query.q_rel_name,\
                                         self.query.q_rh_uid , self.query.q_rh_name, self.query.q_phrase_type_uid]
                
        # Append query expression as first line in query_spec
        # query_expr = lh_uid, lh_name, rel_uid, rel_name, rh_uid_rh_name, phrase_type_uid
        self.main.query_spec.append(self.query.query_expr)

        # Formulate coditions as are specified in the GUI 
        self.query.Formulate_conditions_from_gui()

        # Prepare query for execution and execute query
        self.query.Interpret_query_spec()
        # Display query results in notebook sheets
        self.views.Notebook_views()

    def Close_query(self):
        self.QWindow.destroy()
        return
#------------------------------------------------------
    
if __name__ == "__main__":
    root = Tk()
    main = Main()
    Gel_net = Semantic_network()
    GUI = Query_views(Gel_net, main)
    
    root.mainloop()
