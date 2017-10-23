import os
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, filedialog
from operator import itemgetter
from Bootstrapping import ini_out_path
from Expr_Table_Def import *
from Create_output_file import Create_gellish_expression, Convert_numeric_to_integer, Open_output_file
from Occurrences_diagrams import Occurrences_diagram as occ_diagram

class Main_view():
    def __init__(self, main):
        self.root = main.root
        self.main = main
        self.user = main.user
        self.root.title("Semantic model server")
        max_width, max_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry('1000x600')
        self.root.minsize(width=600,height=300)
        self.root.maxsize(width=max_width, height=max_height) #1000,height=600)
        self.root.myStyle = Style()
        self.root.myStyle.configure("TFrame"   ,background="#dfd")
        self.root.configure(background="#ddf")
        self.root.columnconfigure (0,weight=1)
        self.root.rowconfigure    (0,weight=1)
        #self.root.rowconfigure    (1,weight=1)

        self.GUI_lang_names = ("English", "Nederlands")
        self.lang_uid_dict  = {"English": '910036', "Nederlands": '910037'}

        # Import semantic network from Pickle
        self.main.Load_net()

        # Set GUI language default = English: GUI_lang_names[0]
        self.user.Set_GUI_language(self.GUI_lang_names[0])
        self.lang_index = self.user.GUI_lang_index
        
        # Open main window
        self.Main_window()

        event = 'Button-1'
        self.Determine_GUI_language(event)

#--------------------------------------------------
    def Main_window(self):
        """ Define a MainWindow with select options.
            self.lang_index is the initial index from user.GUI_lang_index
        """

        lprefs = False      # Language preferences are not set yet.
        cprefs = False      # Language community preferences are not set yet.
    #
    # Menu bar   
        self.menubar = Menu(self.root,bg='#fbf')
        self.root['menu'] = self.menubar
    #
        verify  = ['Read file' ,'Lees file']
        query   = ['Query'  ,'Zoek']
        edit    = ['Modify' ,'Wijzig']
        stop    = ['Stop'    ,'Stop']
        admin   = ['DB Admin','DB Admin']
        new_net = ['New network','Nieuw netwerk']
        save_as = ['Save net','Opslaan']
        load_net= ['Load net','Import']
        read_db = ['Net from db', 'Net van db']
        
        self.menubar.add_command(label=verify[self.lang_index], command=self.main.Verify_table)
        self.menubar.add_command(label=query [self.lang_index], command=self.main.Query_net)
        self.menubar.add_command(label=edit  [self.lang_index], command=self.main.Modify_db)
        self.menubar.add_command(label=stop  [self.lang_index], command=self.main.Stop_Quit)
        
        self.DBMenu = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.DBMenu, label=admin[self.lang_index])
        self.DBMenu.add_command (label=new_net [self.lang_index], command=self.main.Create_net)
        self.DBMenu.add_command (label=save_as [self.lang_index], command=self.main.Dump_net)
        self.DBMenu.add_command (label=load_net[self.lang_index], command=self.main.Load_net)
        #self.DBMenu.add_command (label=read_db [self.lang_index], command=self.main.Read_db)

    # Main Frame
        self.main_frame = Frame(self.root)
        self.main_frame.grid   (column=0,row=0,sticky=NSEW)
        self.main_frame.columnconfigure(0,weight=0)
        self.main_frame.columnconfigure(1,weight=1)
        self.main_frame.rowconfigure   (0,weight=0)
        self.main_frame.rowconfigure   (1,weight=1)

        # Define header row with language selector
        lang_text = ['Language:', 'Taal:']
        self.lang_label   = Label(self.main_frame, text=lang_text[self.lang_index], width=10)
        self.lang_default = StringVar(value=self.user.GUI_lang_name)
        self.lang_box     = ttk.Combobox(self.main_frame, textvariable=self.lang_default,\
                                         values=self.GUI_lang_names, width=10)
        self.lang_label.grid(column=0, row=0, sticky=NW)
        self.lang_box.grid  (column=1, row=0, sticky=NW)

        # Binding GUI language choice
        self.lang_box.bind  ("<<ComboboxSelected>>",self.Determine_GUI_language)

    def Determine_GUI_language(self, event):
        GUI_lang_name  = self.lang_box.get()
        self.user.Set_GUI_language(GUI_lang_name)
##        if self.user.GUI_lang_name in self.GUI_lang_names:
##            self.user.GUI_lang_uid   = self.lang_uid_dict[self.user.GUI_lang_name]
##            self.user.GUI_lang_index = self.GUI_lang_names.index(self.user.GUI_lang_name)
##        else:
##            # Set at deafault: English
##            self.user.GUI_lang_name  = 'English'
##            self.user.GUI_lang_uid   = 910036
##            self.user.GUI_lang_index = 0
##            
##        self.lang_index = self.user.GUI_lang_index
        chosen_language = ['The chosen language is', 'De gekozen taal is']
        print('{} {}'.format(chosen_language[self.lang_index], self.user.GUI_lang_name))

#----------------------------------------------------------
class Query_view():
    ''' Defines a query window for specification of queries in dictionary and models.'''
    def __init__(self, Gel_net, main):
        self.Gel_net = Gel_net
        self.main = main
        self.query = main.query
        self.root = main.root
        self.user = main.user

        self.lang_name  = self.user.GUI_lang_name
        self.lang_uid   = self.user.GUI_lang_uid
        self.lang_index = self.user.GUI_lang_index

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
        self.rep_lang_default = StringVar(value=self.user.GUI_lang_name)
        self.reply_lang_box   = ttk.Combobox(self.query_frame, textvariable=self.rep_lang_default,\
                                         values=self.reply_lang_names, width=10)
        self.reply_lang_label.grid(column=5, row=1, sticky=W)
        self.reply_lang_box.grid  (column=6, row=1, sticky=W)

        # Binding GUI language choice
        self.reply_lang_box.bind  ("<<ComboboxSelected>>",self.Determine_reply_language)

        # Set the reply language initially identical to the GUI language
        self.Gel_net.user.Set_reply_language(self.user.GUI_lang_name)
        print('{} {}'.format(self.reply_language[self.lang_index], self.Gel_net.user.reply_lang_name))

    def Determine_reply_language(self, event):
        reply_lang_name  = self.reply_lang_box.get()
        self.Gel_net.user.Set_reply_language(reply_lang_name)
        print('{} {}'.format(self.reply_language[self.lang_index], self.Gel_net.user.reply_lang_name))

    def Lh_uid_command(self, event):
        """Search for UID in semantic network
        Search in vocabulary for left hand uid.
    == OptionsTable: optionNr,whetherKnown,langUIDres,commUIDres,resultString,resultUID,isCalledUID,kindKnown,kind
    """
        #print('Lh uid entry:',event.char)
        
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
                # Build option with preferred name from names_in_contexts
                # Determine the full definition of the obj in the preferred language
                lang_name, comm_name, preferred_name, full_def = \
                           self.Gel_net.Determine_name_in_language_and_community\
                           (lh, self.user.lang_pref_uids)
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
##            full_def = ''
##            int_lh_uid, integer = Convert_numeric_to_integer(lh_uid)
##            if integer == False or int_lh_uid >= 100:
##                obj = self.Gel_net.uid_dict[lh_uid]
##                # Determine the full definition of the obj in the preferred language
##                lang_name, comm_name, preferred_name, full_def = \
##                           self.Gel_net.Determine_name_in_language_and_community(obj, self.user.lang_pref_uids)
##                #print('FullDef:',self.query.q_lh_uid, lhString, self.query.q_lh_category, fullDef)
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
        #print("  Found lh: ", lhString, self.Gel_net.unknown_quid, self.Gel_net.lh_options[0])

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
                       self.Gel_net.Determine_name_in_language_and_community(obj, self.user.lang_pref_uids)
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
                       self.Gel_net.Determine_name_in_language_and_community(obj, self.user.lang_pref_uids)
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
                       self.Gel_net.Determine_name_in_language_and_community\
                       (self.query.q_lh_obj, self.user.lang_pref_uids)
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
class Display_views():
    def __init__(self, Gel_net, main):
        self.Gel_net = Gel_net
        self.main = main
        self.root = main.root
        self.user = main.user
        self.query = main.query
        self.lang_index = self.user.GUI_lang_index

        self.kind_model   = Gel_net.kind_model
        self.prod_model   = Gel_net.prod_model
        self.taxon_model  = Gel_net.taxon_model
        self.summ_model   = Gel_net.summ_model
        self.possibilities_model = Gel_net.possibilities_model
        self.indiv_model  = Gel_net.indiv_model
        self.query_table  = Gel_net.query_table
##        self.hierarchy   = Gel_net.hierarchy

        #self.summ_of_aspect_uids = Gel_net.summ_of_aspect_uids
        self.taxon_column_names  = Gel_net.taxon_column_names
        self.taxon_uom_names     = Gel_net.taxon_uom_names
        self.summ_column_names   = Gel_net.summ_column_names
        self.summ_uom_names      = Gel_net.summ_uom_names
        self.possib_column_names = Gel_net.possib_column_names
        self.possib_uom_names    = Gel_net.possib_uom_names
        self.indiv_column_names  = Gel_net.indiv_column_names
        self.indiv_uom_names     = Gel_net.indiv_uom_names

        self.subsHead    = ['Subtypes'      ,'Subtypen']
        self.compHead    = ['Part hierarchy','Compositie']
        self.involHead   = ['Occurrences'   ,'Gebeurtenissen']
        self.roleHead    = ['Role'          ,'Rol']
        self.otherHead   = ['Involvements'  ,'Betrokkenen']
        self.kindHead    = ['Kind'          ,'Soort']
        self.aspectHead  = ['Aspect'        ,'Aspect']
        self.partOccHead = ['Part occurrence','Deelgebeurtenis']
        self.info_head   = ['Document'      ,'Document']

        self.modification = ''
        
    def Notebook_views(self):
        """ Defines a Notebook with various view layouts and displays view contents.
            Starting in grid on row 1.
        """
        # Define the overall views_notebook
        self.views_noteb  = Notebook(self.main.GUI.main_frame, height=600)  #, height=400, width=1000)
        self.views_noteb.grid(column=0, row=1,sticky=NSEW, columnspan=2) #pack(fill=BOTH, expand=1)
        self.views_noteb.columnconfigure(0,weight=1)
        self.views_noteb.rowconfigure(0,weight=1)
        #self.views_noteb.rowconfigure(1,weight=1)

    # Define and display Taxonomic view sheet for kinds of products = = = =
        if len(self.taxon_model) > 0:
            self.Define_and_display_taxonomy_of_kinds()

    # Define and display Possibilities_view sheet of kind = = = = = = = = = =
        if len(self.possibilities_model) > 0:
            self.Define_and_display_composition_of_kind()

    # Define and display model of a Kind = = = = = = = = = = = = = =
        if len(self.kind_model) > 0:
            self.Define_and_display_kind_view()

    # Define Summary_view sheet for individual products = = = = = = = = = = =
        if len(self.summ_model) > 0:
            # Destroy earlier summary_frame
            try:
                self.summ_frame.destroy()
            except AttributeError:
                pass
            
            self.Define_summary_sheet()

            self.Display_summary_view()

    # Define Individual_view sheet = = = = = = = = = = = = = = = = = = = = =
        if len(self.indiv_model) > 0:
            self.Define_and_display_individual_model()

    # Define Product_model_sheet view = = = = = = = = = = = = = = = =
        if len(self.prod_model) > 0:
            #print('prod_model',self.prod_model)
            # Destroy earlier product_frame
            try:
                self.prod_frame.destroy()
            except AttributeError:
                pass
            
            self.Define_product_model_sheet()
            #print('len prod model', len(self.prod_model))

            # Display prod_model in Composition_sheet view
            self.Display_product_model_view()

    # Define Data_sheet view = = = = = = = = = = = = = = = =
        if len(self.prod_model) > 0:
            # Destroy earlier data sheet
            try:
                self.data_sheet.destroy()
            except AttributeError:
                pass
        
            self.Define_data_sheet()

            # Display prod_model in Data_sheet view
            self.Display_data_sheet_view()
            
    # Activities view = = = = = = = = = = = = = = = = = = = = =
        if len(self.Gel_net.occ_model) > 0:
            # Destroy earlier activity sheet
            try:
                self.act_frame.destroy()
            except AttributeError:
                pass
        
            self.Define_activity_sheet()

            # Display activities and occurrences in self.act_tree
            #if self.test: print('==self.Gel_net.nr_of_occurrencies:',self.Gel_net.nr_of_occurrencies)
            self.act_tree.tag_configure('headTag', option=None, background='#dfd')
            if len(self.Gel_net.occ_model) > 0:
                occText  = ['Occurrence'     ,'Gebeurtenis']
                partText = ['Part occurrence','Deelgebeurtenis']
                strText  = ['Involved'       ,'Betrokkene']
                uidText  = ['UID'            ,'UID']
                kindText = ['Kind'           ,'Soort']
                roleText = ['Role'           ,'Rol']
                uidRText = ['UID of role'    ,'UID van rol']
                space = ''
                # Header line display
                self.act_tree.insert('',index='end',\
                               values=(occText[self.lang_index],partText[self.lang_index],\
                                       strText[self.lang_index],uidText[self.lang_index],kindText[self.lang_index],\
                                       roleText[self.lang_index],uidRText[self.lang_index]),\
                               tags='headTag')                                          
                for occ_line in self.Gel_net.occ_model:
                    if testOcc: print('==OccTree:',occ_line)
                    #wholes = []
                    level  = 0
                    # Display self.act_tree      occName   ,occUID
                    OccurrenceTree(self.act_tree,occ_line[1],occ_line[2],occ_line[3],level) #,wholes

                # IDEF0: Display drawings of occurrences
                occ_diagram.Create_occurrences_diagram()

     # Define and display Documents_view sheet = = = = = = = = = =
        if len(self.Gel_net.info_model) > 0:
            self.Define_and_display_documents()

    # Define Expressions_view sheet = = = = = = = = = = = = = = = = = = =
        # Destroy earlier expression_frame
        try:
            self.expr_frame.destroy()
        except AttributeError:
            pass
        
        self.Define_expressions_sheet()

        # Display expressions from self.query_table in Treeview:
        for query_line in self.query_table:
            self.expr_tree.insert('', index='end', values=query_line, tags='valTag')

    def Define_log_sheet(self):
        ''' Define a frame for error and warnings'''
        self.log_frame = Frame(self.views_noteb)
        self.log_frame.grid (column=0, row=0,sticky=NSEW) 
        self.log_frame.columnconfigure(0, weight=1)
        log_head = ['Messages and warnings','Berichten en foutmeldingen']
        self.views_noteb.add(self.log_frame, text=log_head[self.lang_index], sticky=NSEW)
        self.views_noteb.insert("end", self.log_frame, sticky=NSEW)

        # Messages area - text widget definition
        self.log_messages = Text(self.log_frame, width = 40, background='#efc') # height = 10, 
        log_mess_scroll  = ttk.Scrollbar(self.log_frame,orient=VERTICAL,command=self.log_messages.yview)
        self.log_messages.config(yscrollcommand=log_mess_scroll.set)

        self.log_messages.grid (column=0, row=0, columnspan=1, rowspan=1, sticky=NSEW)
        log_mess_scroll.grid   (column=1, row=0, sticky=NS+E)

    def Define_and_display_taxonomy_of_kinds(self):
        # Destroy earlier taxon_frame
        try:
            self.taxon_frame.destroy()
        except AttributeError:
            pass
        
        self.Define_taxonomy_sheet()

        self.Display_taxonomy_view()

    def Define_taxonomy_sheet(self):
        ''' Define a taxonomy sheet for display of taxon_model (a list of taxon_rows)
            for display in a tab of Notebook
        '''
        self.taxon_frame = Frame(self.views_noteb)
        self.taxon_frame.grid (column=0, row=0, sticky=NSEW, rowspan=2) #pack(fill=BOTH, expand=1)  
        self.taxon_frame.columnconfigure(0, weight=1)
        self.taxon_frame.rowconfigure(0,weight=0)
        self.taxon_frame.rowconfigure(1,weight=1)
        
        taxon_text = ['Taxonomy','Taxonomie']
        self.views_noteb.add(self.taxon_frame, text=taxon_text[self.lang_index], sticky=NSEW)
        #self.views_noteb.insert("end", self.taxon_frame, sticky=NSEW)

        taxon_head = ['Hierarchy of kinds and aspects per object of a particular kind',\
                      'Hiërarchie van soorten en aspecten per object van een bepaalde soort']
        taxon_lbl  = Label(self.taxon_frame,text=taxon_head[self.lang_index])
        
        headings = ['UID','Name', 'Kind','Community','Aspect1','Aspect2','Aspect3','Aspect4','Aspect5'  ,\
                                 'Aspect6','Aspect7','Aspect8','Aspect9','Aspect10']
        nr_of_cols = len(self.taxon_column_names)
        display_cols = headings[3:nr_of_cols]
##        self.taxon_tree = Treeview(self.taxon_frame,columns=('Community','Aspect1','Aspect2','Aspect3','Aspect4'  ,\
##                                                     'Aspect5'  ,'Aspect6','Aspect7','Aspect8','Aspect9','Aspect10'),\
##                                  displaycolumns='#all', selectmode='browse', height=30)
        self.taxon_tree = Treeview(self.taxon_frame,columns=(headings[0:nr_of_cols]),\
                                  displaycolumns=display_cols, selectmode='browse', height=30)
                        
        self.taxon_tree.heading('UID'       ,text='UID'      , anchor=W)
        self.taxon_tree.heading('Name'      ,text='Name'     , anchor=W)
        self.taxon_tree.heading('Kind'      ,text='Kind'     , anchor=W)
        self.taxon_tree.heading('Community' ,text='Community', anchor=W)
        
        self.taxon_tree.column ('#0'        ,minwidth=100    , width=200)
        self.taxon_tree.column ('Community' ,minwidth=20     , width=50)
        asp = 0
        for column in self.taxon_column_names[4:]:
            asp += 1
            Asp_name = 'Aspect' + str(asp)
            self.taxon_tree.heading(Asp_name   ,text=self.taxon_column_names[asp +3]  ,anchor=W)
            self.taxon_tree.column (Asp_name   ,minwidth=20 ,width=50)

##        self.taxon_tree.columnconfigure(0,weight=1)
##        self.taxon_tree.rowconfigure   (0,weight=1)
        
        self.taxon_tree.tag_configure('colTag', option=None, background='#afa')
        self.taxon_tree.tag_configure('uomTag', option=None, background='#ccf')
        self.taxon_tree.tag_configure('sumTag', option=None, background='#cfc')

        taxon_scroll = Scrollbar(self.taxon_frame, orient=VERTICAL, command=self.taxon_tree.yview)
        taxon_lbl.grid       (column=0, row=0,sticky=EW)
        self.taxon_tree.grid (column=0, row=1,sticky=NSEW)
        taxon_scroll.grid    (column=0, row=1,sticky=NS+E)
        self.taxon_tree.config(yscrollcommand=taxon_scroll.set)

        self.taxon_tree.bind(sequence='<Double-1>', func=self.Taxon_detail_view)
        self.taxon_tree.bind(sequence='c'         , func=self.Taxon_detail_view)

    def Display_taxonomy_view(self):
        # Display header row with units of measure
        self.taxon_tree.insert('', index='end', values=self.taxon_uom_names, tags='uomTag')
        # Display self.taxon_model rows in self.taxon_tree
        parents = []
        for taxon_line in self.taxon_model:
            #print('Taxon_line', taxon_line)
            # Verify whether taxon_line[2], being the supertype, is blank or in the list of parents
            if taxon_line[2] == '' or taxon_line[2] in parents:
                # Skip duplicates
                if self.taxon_tree.exists(taxon_line[1]):
                    continue
                else:
                    color_tag = 'sumTag'
                    term = taxon_line[1].partition(' ')
                    if term[0] in ['has', 'heeft', 'classifies', 'classificeert']:
                        color_tag = 'colTag'
                    self.taxon_tree.insert(taxon_line[2],index='end',values=taxon_line,tags=color_tag,\
                                           iid=taxon_line[1],text=taxon_line[1], open=True)
                    parents.append(taxon_line[1])

    def Define_summary_sheet(self):
        ''' Define a summary_sheet for display of summ_model (a list of summary_rows)
            for display in a tab of Notebook
        '''
        self.summ_frame = Frame(self.views_noteb)
        self.summ_frame.grid (column=0, row=0,sticky=NSEW) #pack(fill=BOTH, expand=1)  
        self.summ_frame.columnconfigure(0, weight=1)
        self.summ_frame.rowconfigure(0,weight=1)
        #self.summ_frame.rowconfigure(1,weight=1)
        
        summary = ['Summary','Overzicht']
        self.views_noteb.add(self.summ_frame, text=summary[self.lang_index], sticky=NSEW)
        self.views_noteb.insert("end", self.summ_frame, sticky=NSEW)

        summHead = ['Aspects per object of a particular kind','Aspecten per object van een bepaalde soort']
        summ_lbl = Label(self.summ_frame,text=summHead[self.lang_index])
        
        headings = ['UID','Name', 'Kind','Community','Aspect1','Aspect2','Aspect3','Aspect4','Aspect5'  ,\
                                 'Aspect6','Aspect7','Aspect8','Aspect9','Aspect10']
        nr_of_cols = len(self.summ_column_names)
        display_cols = headings[3:nr_of_cols]
##        self.summ_tree = Treeview(self.summ_frame,columns=('Community','Aspect1','Aspect2','Aspect3','Aspect4'  ,\
##                                                     'Aspect5'  ,'Aspect6','Aspect7','Aspect8','Aspect9','Aspect10'),\
##                                  displaycolumns='#all', selectmode='browse', height=30)
        self.summ_tree = Treeview(self.summ_frame,columns=(headings[0:nr_of_cols]),\
                                  displaycolumns=display_cols, selectmode='browse', height=30)
                        
        self.summ_tree.heading('UID'       ,text='UID'      , anchor=W)
        self.summ_tree.heading('Name'      ,text='Name'     , anchor=W)
        self.summ_tree.heading('Kind'      ,text='Kind'     , anchor=W)
        self.summ_tree.heading('Community' ,text='Community', anchor=W)
        
        self.summ_tree.column ('#0'        ,minwidth=100    , width=200)
        self.summ_tree.column ('Community' ,minwidth=20     , width=50)
        asp = 0
        for column in self.summ_column_names[4:]:
            asp += 1
            Asp_name = 'Aspect' + str(asp)
            self.summ_tree.heading(Asp_name   ,text=self.summ_column_names[asp +3]  ,anchor=W)
            self.summ_tree.column (Asp_name   ,minwidth=20 ,width=50)

        self.summ_tree.columnconfigure(0,weight=1)
        self.summ_tree.rowconfigure   (0,weight=1)
        
        self.summ_tree.tag_configure('colTag', option=None, background='#9f9')
        self.summ_tree.tag_configure('uomTag', option=None, background='#ccf')
        self.summ_tree.tag_configure('sumTag', option=None, background='#cfc')

        summScroll = Scrollbar(self.summ_frame, orient=VERTICAL, command=self.summ_tree.yview)
        summ_lbl.grid      (column=0, row=0,sticky=EW)
        self.summ_tree.grid(column=0, row=1,sticky=NSEW)
        summScroll.grid    (column=1, row=1,sticky=NS+E)
        self.summ_tree.config(yscrollcommand=summScroll.set)

        self.summ_tree.bind(sequence='<Double-1>', func=self.Summ_detail_view)

    def Display_summary_view(self):
        # Display header row with units of measure
        self.summ_tree.insert('', index='end', values=self.summ_uom_names, tags='uomTag')
        # Display self.summ_model rows in self.summ_tree
        parents = []
        for summ_line in self.summ_model:
            if summ_line[2] == '' or summ_line[2] in parents:
                if self.summ_tree.exists(summ_line[1]):
                    continue
                else:
                    self.summ_tree.insert(summ_line[2],index='end',values=summ_line,tags='sumTag',iid=summ_line[1],\
                                          text=summ_line[1], open=True)  # summ_line[2] is the supertype
                    parents.append(summ_line[1])

        # Sorting example
##        # Add command to heading as follows:
##        tree.heading(column1, text = 'some text', command = foo)
        
##        l = [['a',2], ['a',1], ['b', 2], ['a',3], ['b',1], ['b',3]]
##        l.sort(key=itemgetter(1))
##        l.sort(key=itemgetter(0), reverse=True)
##        # [['b', 1], ['b', 2], ['b', 3], ['a', 1], ['a', 2], ['a', 3]]

    def Define_and_display_composition_of_kind(self):
        # Destroy earlier possib_frame
        try:
            self.possib_frame.destroy()
        except AttributeError:
            pass
        
        self.Define_possibilities_sheet()

        # Display header row with units of measure
        self.possib_tree.insert('', index='end', values=self.possib_uom_names, tags='uomTag')
        # Display self.possibilities_model rows in self.possib_tree
        parents = []
        for possib_line in self.possibilities_model:
            if possib_line[2] == '' or possib_line[2] in parents:
                self.possib_tree.insert(possib_line[2],index='end',values=possib_line,tags='sumTag',iid=possib_line[1],\
                                      text=possib_line[1], open=True)  # possib_line[2] is the whole
                parents.append(possib_line[1])

    def Define_possibilities_sheet(self):
        ''' Define a possibilities_sheet for display of possibilities_model (a list of possib_rows)
            for display in a tab of Notebook
        '''
        self.possib_frame  = Frame(self.views_noteb)
        self.possib_frame.grid (column=0, row=0,sticky=NSEW, rowspan=2) #pack(fill=BOTH, expand=1)  
        self.possib_frame.columnconfigure(0, weight=1)
        self.possib_frame.rowconfigure(0,weight=0)
        self.possib_frame.rowconfigure(1,weight=1)
        
        possib_text = ['Possibilities','Mogelijkheden']
        self.views_noteb.add(self.possib_frame, text=possib_text[self.lang_index], sticky=NSEW)
        self.views_noteb.insert("end", self.possib_frame, sticky=NSEW)

        possib_head  = ['Possible aspects per object of a particular kind','Mogelijke aspecten per object van een bepaalde soort']
        possib_label = Label(self.possib_frame,text=possib_head[self.lang_index])
        headings = ['UID','Name','Parent','Kind','Community','Aspect1','Aspect2','Aspect3','Aspect4','Aspect5'  ,\
                                 'Aspect6','Aspect7','Aspect8','Aspect9','Aspect10']
        nr_of_cols = len(self.possib_column_names)
        display_cols = headings[3:nr_of_cols]
##        self.possib_tree = Treeview(self.possib_frame,columns=('Community','Aspect1','Aspect2','Aspect3','Aspect4'  ,\
##                                                     'Aspect5'  ,'Aspect6','Aspect7','Aspect8','Aspect9','Aspect10'),\
##                                  displaycolumns='#all', selectmode='browse', height=30)
        self.possib_tree = Treeview(self.possib_frame,columns=(headings[0:nr_of_cols]),\
                                  displaycolumns=display_cols, selectmode='browse', height=30)
                        
        self.possib_tree.heading('UID'       ,text='UID'      , anchor=W)
        self.possib_tree.heading('Name'      ,text='Name'     , anchor=W)
        self.possib_tree.heading('Parent'    ,text='Parent'   , anchor=W)
        self.possib_tree.heading('Kind'      ,text='Kind'     , anchor=W)
        self.possib_tree.heading('Community' ,text='Community', anchor=W)
        
        self.possib_tree.column ('#0'        ,minwidth=100    , width=200)
        self.possib_tree.column ('Kind'      ,minwidth=20     , width=50)
        self.possib_tree.column ('Community' ,minwidth=20     , width=50)
        asp = 0
        for column in self.possib_column_names[5:]:
            asp += 1
            Asp_name = 'Aspect' + str(asp)
            self.possib_tree.heading(Asp_name   ,text=self.possib_column_names[asp +4]  ,anchor=W)
            self.possib_tree.column (Asp_name   ,minwidth=20 ,width=50)

        self.possib_tree.columnconfigure(0,weight=1)
        self.possib_tree.columnconfigure(1,weight=1)
        self.possib_tree.rowconfigure   (0,weight=1)
        self.possib_tree.rowconfigure   (1,weight=1)
        
        self.possib_tree.tag_configure('uomTag', option=None, background='#ccf')
        self.possib_tree.tag_configure('sumTag', option=None, background='#cfc')

        possib_Scroll = Scrollbar(self.possib_frame, orient=VERTICAL, command=self.possib_tree.yview)
        possib_label.grid     (column=0, row=0,sticky=EW)
        self.possib_tree.grid (column=0, row=1,sticky=NSEW)
        possib_Scroll.grid    (column=0, row=1,sticky=NS+E)
        self.possib_tree.config(yscrollcommand=possib_Scroll.set)

        self.possib_tree.bind(sequence='<Double-1>', func=self.Possibilities_detail_view)

    def Define_and_display_individual_model(self):
        # Destroy earlier indiv_frame
        try:
            self.indiv_frame.destroy()
        except AttributeError:
            pass
        
        self.Define_composition_sheet()

        # Display composition sheet
        # Display header row with units of measure
        self.indiv_tree.insert('', index='end', values=self.indiv_uom_names, tags='uomTag')
        # Display self.indiv_model rows in self.indiv_tree
        indiv_parents = []
        for indiv_line in self.indiv_model:
            if indiv_line[2] == '' or indiv_line[2] in indiv_parents:
                self.indiv_tree.insert(indiv_line[2],index='end',values=indiv_line,tags='sumTag',iid=indiv_line[1],\
                                      text=indiv_line[1], open=True)  # indiv_line[2] is the whole
                indiv_parents.append(indiv_line[1])
        
    def Define_composition_sheet(self):
        ''' Define a sheet for display of an individual thing (indiv_model, a list of indiv_rows)
            for display in a tab of Notebook
        '''
        self.indiv_frame  = Frame(self.views_noteb)
        self.indiv_frame.grid (column=0, row=0,sticky=NSEW) #pack(fill=BOTH, expand=1)  
        self.indiv_frame.columnconfigure(0, weight=1)
        self.indiv_frame.rowconfigure(0,weight=1)
        self.indiv_frame.rowconfigure(1,weight=1)
        
        indiv_text = ['Composition','Samenstelling']
        self.views_noteb.add(self.indiv_frame, text=indiv_text[self.lang_index], sticky=NSEW)
        self.views_noteb.insert("end", self.indiv_frame, sticky=NSEW)

        indiv_Head = ['Aspects per individual object','Aspecten per individueel object']
        indiv_Lbl  = Label(self.indiv_frame,text=indiv_Head[self.lang_index])
        headings = ['UID','Name','Parent','Kind','Community','Aspect1','Aspect2','Aspect3','Aspect4','Aspect5'  ,\
                                 'Aspect6','Aspect7','Aspect8','Aspect9','Aspect10']
        nr_of_cols = len(self.indiv_column_names)
        display_cols = headings[3:nr_of_cols]
##        self.indiv_tree = Treeview(self.indiv_frame,columns=('Community','Aspect1','Aspect2','Aspect3','Aspect4'  ,\
##                                                     'Aspect5'  ,'Aspect6','Aspect7','Aspect8','Aspect9','Aspect10'),\
##                                  displaycolumns='#all', selectmode='browse', height=30)
        self.indiv_tree = Treeview(self.indiv_frame,columns=(headings[0:nr_of_cols]),\
                                  displaycolumns=display_cols, selectmode='browse', height=30)
                        
        self.indiv_tree.heading('UID'       ,text='UID'      , anchor=W)
        self.indiv_tree.heading('Name'      ,text='Name'     , anchor=W)
        self.indiv_tree.heading('Parent'    ,text='Parent'   , anchor=W)
        self.indiv_tree.heading('Kind'      ,text='Kind'     , anchor=W)
        self.indiv_tree.heading('Community' ,text='Community', anchor=W)
        
        self.indiv_tree.column ('#0'        ,minwidth=100    , width=200)
        self.indiv_tree.column ('Kind'      ,minwidth=20     , width=50)
        self.indiv_tree.column ('Community' ,minwidth=20     , width=50)
        asp = 0
        for column in self.indiv_column_names[5:]:
            asp += 1
            Asp_name = 'Aspect' + str(asp)
            self.indiv_tree.heading(Asp_name   ,text=self.indiv_column_names[asp +4]  ,anchor=W)
            self.indiv_tree.column (Asp_name   ,minwidth=20 ,width=50)

        self.indiv_tree.columnconfigure(0,weight=1)
        self.indiv_tree.columnconfigure(1,weight=1)
        self.indiv_tree.rowconfigure   (0,weight=1)
        self.indiv_tree.rowconfigure   (1,weight=1)
        
        self.indiv_tree.tag_configure('uomTag', option=None, background='#ccf')
        self.indiv_tree.tag_configure('sumTag', option=None, background='#cfc')

        indiv_Scroll = Scrollbar(self.indiv_frame, orient=VERTICAL, command=self.indiv_tree.yview)
        indiv_Lbl.grid       (column=0, row=0,sticky=EW)
        self.indiv_tree.grid(column=0, row=1,sticky=NSEW)
        indiv_Scroll.grid    (column=1, row=1,sticky=NS+E)
        self.indiv_tree.config(yscrollcommand=indiv_Scroll.set)

        self.indiv_tree.bind(sequence='<Double-1>', func=self.Indiv_detail_view)

    def Define_expressions_sheet(self):
        ''' Define expressions view sheet for display of expr_table in Notebook tab
        '''
        self.expr_frame = Frame(self.views_noteb)
        self.expr_frame.grid (column=0, row=0,sticky=NSEW, rowspan=4) #pack(fill=BOTH, expand=1)  
        self.expr_frame.columnconfigure(0,weight=1)
        self.expr_frame.rowconfigure(0,weight=0)
        self.expr_frame.rowconfigure(1,weight=0)
        self.expr_frame.rowconfigure(2,weight=0)
        self.expr_frame.rowconfigure(3,weight=1)
        
        expressions = ['Expressions' ,'Uitdrukkingen']
        save_on_CSV_file  = ['Save on CSV file','Opslaan op CSV file']
        save_on_JSON_file = ['Save on JSON file','Opslaan op JSON file']
        self.views_noteb.add(self.expr_frame, text=expressions[self.lang_index],sticky=NSEW)
        self.views_noteb.insert("end",self.expr_frame,sticky=NSEW)
        # Define button for display of contextual facts
        details_button   = Button(self.expr_frame, text='Context', command=self.Contextual_facts)
        save_CSV_button  = Button(self.expr_frame, text=save_on_CSV_file[self.lang_index], \
                                  command=self.Save_on_CSV_file)
        save_JSON_button = Button(self.expr_frame, text=save_on_JSON_file[self.lang_index], \
                                  command=self.Save_on_JSON_file)

        header = ['Model expressions in Gellish','Uitdrukkingen in Gellish']
        expr_lbl = Label(self.expr_frame, text=header[self.lang_index],justify='left')
        self.expr_tree = Treeview(self.expr_frame,\
                            columns=('seq'       ,'langUID'    ,'langName'  ,'commUID'    ,'commName' ,\
                                     'reality'   ,'intentUID'  ,'intentName','lhCard'     ,'lhUID'    ,\
                                     'lhName'    ,'lhRoleUID'  ,'lhRoleName','validUID'   ,'validName',\
                                     'ideaUID'   ,'ideaDescr'  ,'reltypeUID','reltypeName','phrasetypeUID',\
                                     'rhRoleUID' ,'rhRoleName' ,'rhCard'    ,'rhUID'      ,'rhName'   ,\
                                     'partDef'   ,'fullDef'    ,'uomUID'    ,'uomName'    ,'accUID'   ,\
                                     'accName'   ,'pickUID'    ,'pickName'  ,'remarks'    ,'status'   ,\
                                     'reason'    ,'succUID'    ,'dateStartVal','dateStartAv','dateCC' ,\
                                     'dateLatChE','orignatorUID','originatorName','authorUID','authorName',\
                                     'addrUID'   ,'addrName'   ,'refs'      ,'exprUID'    ,'collUID'  ,\
                                     'collName'  ,'fileName'   ,'lhComm'    ,'rhComm'     ,'relComm' ),\
                            displaycolumns=('langName','commName','ideaUID','lhUID'  ,'lhName','reltypeUID',\
                                            'reltypeName','rhUID','rhName' ,'fullDef','uomUID','uomName',\
                                            'remarks' ,'status') ,\
                            selectmode='browse', height=20)
        
        self.expr_tree.heading('seq'       ,text='Seq'       ,anchor=W)
        self.expr_tree.heading('langUID'   ,text='langUID'   ,anchor=W)
        self.expr_tree.heading('langName'  ,text='Language'  ,anchor=W)
        self.expr_tree.heading('commUID'   ,text='commUID'   ,anchor=W)
        self.expr_tree.heading('commName'  ,text='Community' ,anchor=W)
        self.expr_tree.heading('reality'   ,text='reality'   ,anchor=W)
        self.expr_tree.heading('intentUID' ,text='intentUID' ,anchor=W)
        self.expr_tree.heading('intentName',text='intentName',anchor=W)
        self.expr_tree.heading('lhCard'    ,text='lhCard'    ,anchor=W)
        self.expr_tree.heading('lhUID'     ,text='lhUID'     ,anchor=W)
        self.expr_tree.heading('lhName'    ,text='lhName'    ,anchor=W)
        self.expr_tree.heading('lhRoleUID' ,text='lhRoleUID' ,anchor=W)
        self.expr_tree.heading('lhRoleName',text='lhRoleName',anchor=W)
        self.expr_tree.heading('validUID'  ,text='validUID'  ,anchor=W)
        self.expr_tree.heading('validName' ,text='validName' ,anchor=W)
        self.expr_tree.heading('ideaUID'   ,text='ideaUID'   ,anchor=W)
        self.expr_tree.heading('ideaDescr' ,text='ideaDescr' ,anchor=W)
        self.expr_tree.heading('reltypeUID',text='reltypeUID',anchor=W)
        self.expr_tree.heading('reltypeName',text='relation type',anchor=W)
        self.expr_tree.heading('phrasetypeUID',text='phrase type',anchor=W)
        self.expr_tree.heading('rhRoleUID' ,text='rhRoleUID' ,anchor=W)
        self.expr_tree.heading('rhRoleName',text='rhRoleName',anchor=W)
        self.expr_tree.heading('rhCard'    ,text='rhCard'    ,anchor=W)
        self.expr_tree.heading('rhUID'     ,text='rhUID'     ,anchor=W)
        self.expr_tree.heading('rhName'    ,text='rhName'    ,anchor=W)
        self.expr_tree.heading('partDef'   ,text='partDef'   ,anchor=W)
        self.expr_tree.heading('fullDef'   ,text='Description',anchor=W)
        self.expr_tree.heading('uomUID'    ,text='uomUID'    ,anchor=W)
        self.expr_tree.heading('uomName'   ,text='UoM'       ,anchor=W)
        self.expr_tree.heading('accUID'    ,text='accUID'    ,anchor=W)
        self.expr_tree.heading('accName'   ,text='accName'   ,anchor=W)
        self.expr_tree.heading('pickUID'   ,text='pickUID'   ,anchor=W)
        self.expr_tree.heading('pickName'  ,text='pickName'  ,anchor=W)
        self.expr_tree.heading('remarks'   ,text='Remarks'   ,anchor=W)
        self.expr_tree.heading('status'    ,text='Status'    ,anchor=W)

        self.expr_tree.column ('#0'        ,minwidth=10,width=20)
        self.expr_tree.column ('seq'       ,minwidth=10,width=20)
        self.expr_tree.column ('langUID'   ,minwidth=20,width=55)
        self.expr_tree.column ('langName'  ,minwidth=15,width=80)
        self.expr_tree.column ('commUID'   ,minwidth=15,width=55)
        self.expr_tree.column ('commName'  ,minwidth=15,width=80)
        self.expr_tree.column ('reality'   ,minwidth=15,width=40)
        self.expr_tree.column ('intentUID' ,minwidth=15,width=55)
        self.expr_tree.column ('intentName',minwidth=15,width=80)
        self.expr_tree.column ('lhCard'    ,minwidth=15,width=40)
        self.expr_tree.column ('lhUID'     ,minwidth=15,width=55)
        self.expr_tree.column ('lhName'    ,minwidth=15,width=150)
        self.expr_tree.column ('lhRoleUID' ,minwidth=15,width=55)
        self.expr_tree.column ('lhRoleName',minwidth=15,width=80)
        self.expr_tree.column ('validUID'  ,minwidth=15,width=55)
        self.expr_tree.column ('validName' ,minwidth=15,width=80)
        self.expr_tree.column ('ideaUID'   ,minwidth=15,width=55)
        self.expr_tree.column ('ideaDescr' ,minwidth=15,width=80)
        self.expr_tree.column ('reltypeUID',minwidth=15,width=55)
        self.expr_tree.column ('reltypeName',minwidth=15,width=200)
        self.expr_tree.column ('phrasetypeUID',minwidth=15,width=40)
        self.expr_tree.column ('rhRoleUID' ,minwidth=15,width=55)
        self.expr_tree.column ('rhRoleName',minwidth=15,width=80)
        self.expr_tree.column ('rhCard'    ,minwidth=15,width=40)
        self.expr_tree.column ('rhUID'     ,minwidth=15,width=55)
        self.expr_tree.column ('rhName'    ,minwidth=15,width=150)
        self.expr_tree.column ('partDef'   ,minwidth=15,width=5)
        self.expr_tree.column ('fullDef'   ,minwidth=15,width=120)
        self.expr_tree.column ('uomUID'    ,minwidth=15,width=55)
        self.expr_tree.column ('uomName'   ,minwidth=15,width=60)
        self.expr_tree.column ('accUID'    ,minwidth=15,width=55)
        self.expr_tree.column ('accName'   ,minwidth=15,width=80)
        self.expr_tree.column ('pickUID'   ,minwidth=15,width=55)
        self.expr_tree.column ('pickName'  ,minwidth=15,width=80)
        self.expr_tree.column ('remarks'   ,minwidth=15,width=100)
        self.expr_tree.column ('status'    ,minwidth=15,width=120)

        exprScroll = Scrollbar(self.expr_frame,orient=VERTICAL,command=self.expr_tree.yview)
        expr_lbl.grid         (column=0, row=0, sticky=NSEW)
        self.expr_tree.grid   (column=0, row=1, sticky=NSEW, rowspan=3)
        exprScroll.grid       (column=0, row=1, sticky=NS+E, rowspan=3)
        details_button.grid   (column=1, row=0, sticky=N)
        save_CSV_button.grid  (column=1, row=1, sticky=N)
        save_JSON_button.grid (column=1, row=2, sticky=N)
        
        self.expr_tree.config(yscrollcommand=exprScroll.set)
        self.expr_tree.tag_configure('valTag'  ,background='#cfc')
        
##        self.expr_tree.columnconfigure(0,weight=1)
##        self.expr_tree.columnconfigure(1,weight=1)
##        self.expr_tree.columnconfigure(2,weight=1)
##        self.expr_tree.columnconfigure(3,weight=1)
##        self.expr_tree.columnconfigure(4,weight=1)
##        self.expr_tree.columnconfigure(5,weight=1)
##        self.expr_tree.columnconfigure(6,weight=1)
##        self.expr_tree.columnconfigure(7,weight=1)
##        self.expr_tree.columnconfigure(8,weight=1)
##        self.expr_tree.columnconfigure(9,weight=1)
##        self.expr_tree.columnconfigure(10,weight=1)
##        self.expr_tree.columnconfigure(11,weight=1)
##        self.expr_tree.columnconfigure(12,weight=1)
##        self.expr_tree.rowconfigure(0,weight=1)
##        self.expr_tree.rowconfigure(1,weight=1)
##        self.expr_tree.rowconfigure(2,weight=1)

        self.expr_tree.bind(sequence='<Double-1>', func=self.Expr_detail_view)
    
    def Save_on_CSV_file(self):
        """ Saving query results in a CSV file in Gellish Expression Format."""
        import csv
        import time
        
        date = time.strftime("%x")
        # Create 3 header records of file
        header1 = ['Gellish', 'Nederlands', 'Version', '9.0', date, 'Query results',\
                   'Query results about '+self.Gel_net.object_in_focus.name,'','','','','']
        # header2 = expr_col_ids from initial settings
        # header3 is taken from Expr_Table_Def
        
        # Open an output file for saving the header lines and the query_table
        # Note: the r upfront the string (rawstring) is
        #       to avoid interpretation as a Unicode string (and thus giving an error)
        # ini_out_path from bootstrapping
        outputFile = filedialog.asksaveasfilename(filetypes  = (("CSV files","*.csv"),\
                                                               ("All files","*.*")),\
                                                  title      = "Enter a file name",\
                                                  initialdir = ini_out_path,\
                                                  initialfile= 'QueryResults.csv',\
                                                  parent     = self.expr_frame)
        if outputFile == '':
            if self.lang_index == 1:
                print('De filenaam voor opslaan is blanco of the file selectie is gecancelled. \
    De file is opgeslagen met de naam <QueryResults.csv')
            else:
                print('File name for saving is blank or file selection is cancelled. \
File is saved under name <QueryResults.csv')
            outputFile = 'QueryResults.csv'
        
        queryFile  = open(outputFile,mode='w',newline='')
        fileWriter = csv.writer(queryFile,dialect='excel',delimiter=';') 

        # Save the query_table results in a CSV file, including three header lines
        # Write the three header lines and then the file content from query_table
        fileWriter.writerow(header1)
        fileWriter.writerow(expr_col_ids)
        fileWriter.writerow(header3)
        for expression in self.Gel_net.query_table:
            fileWriter.writerow(expression)
        
        queryFile.close()
        if self.lang_index == 1:
            print('File %s is opgeslagen.' % (outputFile))
        else:
            print('File %s is saved.' % (outputFile))
            
        # Open written file in Excel
        os.startfile(outputFile,'open')

    def Save_on_JSON_file(self):
        """ Saving query results in a JSON file in Gellish Expression Format."""
        subject_name = 'Query results'
        lang_name = 'Nederlands'
        serialization = 'json'
        Open_output_file(self.Gel_net.query_table, subject_name, lang_name, serialization)

    def Define_and_display_kind_view(self):
        # Destroy earlier summary_frame
        try:
            self.kind_frame.destroy()
        except AttributeError:
            pass
        
        self.Define_kind_model_sheet()

        self.Display_kind_model_view()

    def Define_kind_model_sheet(self):
        ''' Kind_model View tab sheet for a kind in Notebook'''
        self.kind_frame  = Frame(self.views_noteb)
        self.kind_frame.grid (column=0, row=0,sticky=NSEW) #pack(fill=BOTH, expand=1)  
        self.kind_frame.columnconfigure(0,weight=1)
        self.kind_frame.rowconfigure(0,weight=1)
        self.kind_frame.rowconfigure(1,weight=1)

        comp = ['Model of a kind','Model van een soort']
        self.views_noteb.add(self.kind_frame, text=comp[self.lang_index],sticky=NSEW)
        self.views_noteb.insert("end",self.kind_frame,sticky=NSEW)

        structure = ['Tree structure','Boomstructuur']

        kind_label = Label(self.kind_frame, text=structure[self.lang_index],justify='left')
        heads = ['uid_1','uid_2','uid-3','inFocus','Level1','Level2','Level3','kind',\
                'aspect','kAspect','>=<','value', 'UoM','status']
        display_heads = heads[3:]
        self.kind_tree = Treeview(self.kind_frame,columns=(heads), displaycolumns=display_heads, \
                                  selectmode='browse', height=30, padding=2)
        self.kind_treeHead = [('LineNr' ,'Object','','' ,'Kind' ,'Aspect','Kind of aspect',\
                               '>=<','Value' ,'UoM'    ,'Status'),\
                              ('RegelNr','Object','','','Soort','Aspect','Soort aspect'  ,\
                               '>=<','Waarde','Eenheid','Status')]
        col = -1
        for head_field in display_heads:
            col += + 1
            self.kind_tree.heading(head_field ,text=self.kind_treeHead[self.lang_index][col],anchor=W)
            
##        self.kind_tree.heading('inFocus' ,text=self.kind_treeHead[self.lang_index][0],anchor=W)
##        self.kind_tree.heading('Level1'  ,text=self.kind_treeHead[self.lang_index][1],anchor=W)
##        self.kind_tree.heading('Level2'  ,text=self.kind_treeHead[self.lang_index][2],anchor=W)
##        self.kind_tree.heading('Level3'  ,text=self.kind_treeHead[self.lang_index][3],anchor=W)
##        self.kind_tree.heading('kind'    ,text=self.kind_treeHead[self.lang_index][4],anchor=W)
##        self.kind_tree.heading('aspect'  ,text=self.kind_treeHead[self.lang_index][5],anchor=W)
##        self.kind_tree.heading('kAspect' ,text=self.kind_treeHead[self.lang_index][6],anchor=W)
##        self.kind_tree.heading('>=<'     ,text=self.kind_treeHead[self.lang_index][7],anchor=W)
##        self.kind_tree.heading('value'   ,text=self.kind_treeHead[self.lang_index][8],anchor=W)
##        self.kind_tree.heading('UoM'     ,text=self.kind_treeHead[self.lang_index][9],anchor=W)
##        self.kind_tree.heading('status'  ,text=self.kind_treeHead[self.lang_index][10],anchor=W)
        
        self.kind_tree.column ('#0'      ,minwidth=40,width=50)
        self.kind_tree.column ('inFocus' ,minwidth=10,width=10)
        self.kind_tree.column ('Level1'  ,minwidth=20,width=100)
        self.kind_tree.column ('Level2'  ,minwidth=20,width=50)
        self.kind_tree.column ('Level3'  ,minwidth=20,width=50)
        self.kind_tree.column ('kind'    ,minwidth=20,width=100)
        self.kind_tree.column ('aspect'  ,minwidth=20,width=100)
        self.kind_tree.column ('kAspect' ,minwidth=20,width=100)
        self.kind_tree.column ('>=<'     ,minwidth=20,width=20)
        self.kind_tree.column ('value'   ,minwidth=20,width=100)
        self.kind_tree.column ('UoM'     ,minwidth=20,width=50)
        self.kind_tree.column ('status'  ,minwidth=20,width=80)
        
        #self.kind_frame.grid  (column=0, row=3,sticky=EW)
        kind_label.grid       (column=0, row=0,sticky=EW)
        self.kind_tree.grid(column=0, row=1,sticky=NSEW)
        #self.kind_tree.grid(column=0, row=2,sticky=NSEW)
        
        self.kind_tree.columnconfigure(0,weight=1)
        self.kind_tree.columnconfigure(1,weight=1)
        self.kind_tree.columnconfigure(2,weight=1)
        self.kind_tree.columnconfigure(3,weight=1)
        self.kind_tree.columnconfigure(4,weight=1)
        self.kind_tree.columnconfigure(5,weight=1)
        self.kind_tree.columnconfigure(6,weight=1)
        self.kind_tree.columnconfigure(7,weight=1)
        self.kind_tree.columnconfigure(8,weight=1)
        self.kind_tree.columnconfigure(9,weight=1)
        self.kind_tree.columnconfigure(10,weight=1)
        self.kind_tree.columnconfigure(11,weight=1)

        self.kind_tree.columnconfigure(0,weight=1)
        self.kind_tree.rowconfigure(0,weight=1)
        self.kind_tree.rowconfigure(1,weight=1)

        compScroll = Scrollbar(self.kind_frame,orient=VERTICAL,command=self.kind_tree.yview)
        compScroll.grid (column=1,row=1,sticky=NS+E)
        self.kind_tree.config(yscrollcommand=compScroll.set)

        self.kind_tree.tag_configure('focusTag' ,background='#9f9') # hell green
        self.kind_tree.tag_configure('headTag'  ,background='#bfb')
        self.kind_tree.tag_configure('valTag'   ,background='#dfd') # light green
        self.kind_tree.tag_configure('available',background='yellow')
        self.kind_tree.tag_configure('missing'  ,background='#fcc') # red

        self.kind_tree.bind(sequence='<Double-1>', func=self.Kind_detail_view_left)
        self.kind_tree.bind(sequence='<Button-2>', func=self.Kind_detail_view_middle)
        self.kind_tree.bind(sequence='<Button-3>', func=self.Kind_detail_view_right)

    def Display_kind_model_view(self):
        ''' Kind_model Model view of a kind: Display prod_model in self.kind_tree:
            self.kind_tree.insert('',index=0,iid='UIDInFocus',values=[nameInFocus,kindDat],
            tags='focusTag',open=True)
        '''
        unknownVal   = ['unknown value','onbekende waarde']
        unknownKind  = ['unknown kind' ,'onbekende soort']
        for kindLine in self.kind_model:
            head = False
            headLine = []
            #if self.test: print('kindLine:',kindLine)
            # If line_type == 1 then prepare header line for level 0 object
            # Note: line_type == 2 is skipped in this view
            if kindLine[3] == 1:
                headLine = kindLine[0:4]
                headLine.append(kindLine[5])
                headLine.append('')
                headLine.append('')
                headLine.append(kindLine[9])
                nameInFocus = headLine[4]
                level0Part = self.kind_tree.insert('',index='end',values=headLine,tags='focusTag',open=True)
                previusPart = level0Part
            # In kind_tree view line_type 2 to 3 (indicated in kindLine[3]) are not displayed.
            elif kindLine[3] > 3:

                # Set value_tags at 'valTag' or 'headTag' for each field
                value_tags = 11*['valTag']
                # If the line is a header line, then set value_tag to 'headTag'
                if kindLine[4] in self.compHead    or kindLine[4] in self.involHead or \
                   kindLine[4] in self.info_head   or kindLine[8] in self.aspectHead or \
                   kindLine[5] in self.partOccHead or kindLine[4] in self.subsHead:
                    head = True
                    value_tags = 11*['headTag']
                # If the line is a value line (thus not a header line) and there is a name of a part
                # then remember the part as a previous part 
                elif kindLine[4] != '':
                    previusPart = level0Part
                elif kindLine[5] != '':
                    previusPart = level1Part
                elif kindLine[6] != '':
                    previusPart = level2Part

                # Set tag background color depending on value
                # If value is missing then bachgroumd color is yellow
                if kindLine[9] == '' or kindLine[9] in unknownVal:
                    value_tags[9] = 'missing'
                else:
                    value_tags[9] = 'available'
                if kindLine[7] in unknownVal:
                    value_tags[7] = 'missing'
                # Insert line
                #print('Value tags:', value_tags)
                id = self.kind_tree.insert(level0Part,index='end',values=kindLine,tags=value_tags,open=True)

                # If the line is a header line, then continue to next line
                if head == True:
                    continue
                # If the line is a value line and the there is a name of a part
                #    then remember the part as a previous part
                elif kindLine[4] != '':
                    level1Part = id
                    previusPart = level0Part
                elif kindLine[5] != '':
                    level2Part = id
                    previusPart = level1Part
                elif kindLine[6] != '':
                    previusPart = level2Part

    def Define_product_model_sheet(self):
        # Product_model view tab sheet in Notebook
        self.prod_frame  = Frame(self.views_noteb)
        self.prod_frame.grid (column=0, row=0,sticky=NSEW) #pack(fill=BOTH, expand=1)  
        self.prod_frame.columnconfigure(0,weight=1)
        self.prod_frame.rowconfigure(0,weight=1)
        self.prod_frame.rowconfigure(1,weight=1)

        prod_text = ['Product model','Productmodel']
        self.views_noteb.add(self.prod_frame, text=prod_text[self.lang_index],sticky=NSEW)
        self.views_noteb.insert("end",self.prod_frame,sticky=NSEW)

        structure = ['Tree structure','Boomstructuur']

        prod_label = Label(self.prod_frame, text=structure[self.lang_index],justify='left')
        heads = ['uid_1','uid_2','uid-3','inFocus','Level1','Level2','Level3','kind',\
                'aspect','kAspect','>=<','value', 'UoM','status']
        display_heads = heads[3:]
        self.prod_tree = Treeview(self.prod_frame,columns=(heads), displaycolumns=display_heads, \
                                  selectmode='browse', height=30, padding=2)
        self.prod_treeHead = [('LineNr' ,'Object','','' ,'Kind' ,'Aspect','Kind of aspect',\
                               '>=<','Value' ,'UoM'    ,'Status'),\
                              ('RegelNr','Object','','','Soort','Aspect','Soort aspect'  ,\
                               '>=<','Waarde','Eenheid','Status')]
        col = -1
        for head_field in display_heads:
            col += + 1
            self.prod_tree.heading(head_field ,text=self.prod_treeHead[self.lang_index][col],anchor=W)
            
##        self.prod_tree.heading('inFocus' ,text=self.prod_treeHead[self.lang_index][0],anchor=W)
##        self.prod_tree.heading('Level1'  ,text=self.prod_treeHead[self.lang_index][1],anchor=W)
##        self.prod_tree.heading('Level2'  ,text=self.prod_treeHead[self.lang_index][2],anchor=W)
##        self.prod_tree.heading('Level3'  ,text=self.prod_treeHead[self.lang_index][3],anchor=W)
##        self.prod_tree.heading('kind'    ,text=self.prod_treeHead[self.lang_index][4],anchor=W)
##        self.prod_tree.heading('aspect'  ,text=self.prod_treeHead[self.lang_index][5],anchor=W)
##        self.prod_tree.heading('kAspect' ,text=self.prod_treeHead[self.lang_index][6],anchor=W)
##        self.prod_tree.heading('>=<'     ,text=self.prod_treeHead[self.lang_index][7],anchor=W)
##        self.prod_tree.heading('value'   ,text=self.prod_treeHead[self.lang_index][8],anchor=W)
##        self.prod_tree.heading('UoM'     ,text=self.prod_treeHead[self.lang_index][9],anchor=W)
##        self.prod_tree.heading('status'  ,text=self.prod_treeHead[self.lang_index][10],anchor=W)
        
        self.prod_tree.column ('#0'      ,minwidth=40,width=50)
        self.prod_tree.column ('inFocus' ,minwidth=10,width=10)
        self.prod_tree.column ('Level1'  ,minwidth=20,width=100)
        self.prod_tree.column ('Level2'  ,minwidth=20,width=50)
        self.prod_tree.column ('Level3'  ,minwidth=20,width=50)
        self.prod_tree.column ('kind'    ,minwidth=20,width=100)
        self.prod_tree.column ('aspect'  ,minwidth=20,width=100)
        self.prod_tree.column ('kAspect' ,minwidth=20,width=100)
        self.prod_tree.column ('>=<'     ,minwidth=20,width=20)
        self.prod_tree.column ('value'   ,minwidth=20,width=100)
        self.prod_tree.column ('UoM'     ,minwidth=20,width=50)
        self.prod_tree.column ('status'  ,minwidth=20,width=80)
        
        #self.prod_frame.grid  (column=0, row=3,sticky=EW)
        prod_label.grid       (column=0, row=0,sticky=EW)
        self.prod_tree.grid(column=0, row=1,sticky=NSEW)
        #self.prod_tree.grid(column=0, row=2,sticky=NSEW)
        
        self.prod_tree.columnconfigure(0,weight=1)
        self.prod_tree.columnconfigure(1,weight=1)
        self.prod_tree.columnconfigure(2,weight=1)
        self.prod_tree.columnconfigure(3,weight=1)
        self.prod_tree.columnconfigure(4,weight=1)
        self.prod_tree.columnconfigure(5,weight=1)
        self.prod_tree.columnconfigure(6,weight=1)
        self.prod_tree.columnconfigure(7,weight=1)
        self.prod_tree.columnconfigure(8,weight=1)
        self.prod_tree.columnconfigure(9,weight=1)
        self.prod_tree.columnconfigure(10,weight=1)
        self.prod_tree.columnconfigure(11,weight=1)

        self.prod_tree.columnconfigure(0,weight=1)
        self.prod_tree.rowconfigure(0,weight=1)
        self.prod_tree.rowconfigure(1,weight=1)

        compScroll = Scrollbar(self.prod_frame,orient=VERTICAL,command=self.prod_tree.yview)
        compScroll.grid (column=1,row=1,sticky=NS+E)
        self.prod_tree.config(yscrollcommand=compScroll.set)

        self.prod_tree.tag_configure('focusTag' ,background='#9f9') # hell green
        self.prod_tree.tag_configure('headTag'  ,background='#bfb')
        self.prod_tree.tag_configure('valTag'   ,background='#dfd') # light green
        self.prod_tree.tag_configure('available',background='yellow')
        self.prod_tree.tag_configure('missing'  ,background='#fcc') # red

        self.prod_tree.bind(sequence='<Double-1>', func=self.Prod_detail_view_left)
        self.prod_tree.bind(sequence='<Button-2>', func=self.Prod_detail_view_middle)
        self.prod_tree.bind(sequence='<Button-3>', func=self.Prod_detail_view_right)
        self.prod_tree.bind(sequence='c'         , func=self.Prod_detail_view_middle)

    def Display_product_model_view(self):
        ''' Product Model view: Display prod_model in self.prod_tree:
            self.prod_tree.insert('',index=0,iid='UIDInFocus',values=[nameInFocus,kindDat],
            tags='focusTag',open=True)
        '''
        unknownVal   = ['unknown value','onbekende waarde']
        unknownKind  = ['unknown kind' ,'onbekende soort']
        for prod_line in self.prod_model:
            head = False
            headLine = []
            #if self.test: print('prod_line:',prod_line)
            # If line_type (prod_line[3]) == 1 then prepare header line from prod_line for level 0 object
            # Note: line_type == 2 is skipped in this view
            if prod_line[3] == 1:
                headLine = prod_line[0:4]
                headLine.append(prod_line[5])
                headLine.append('')
                headLine.append('')
                headLine.append(prod_line[9])
                nameInFocus = headLine[4]
                level0Part = self.prod_tree.insert('',index='end',values=headLine,tags='focusTag',open=True)
                previusPart = level0Part
                
            # In prod_tree view line_type 2 to 3 (indicated in prod_line[3]) are not displayed.
            elif prod_line[3] > 3:
                # Set value_tags at 'valTag' or 'headTag' for each field
                value_tags = 11*['valTag']
                # If the line is a header line, then set value_tag to 'headTag'
                if prod_line[4] in self.compHead    or prod_line[4] in self.involHead or \
                   prod_line[4] in self.info_head   or prod_line[8] in self.aspectHead or \
                   prod_line[5] in self.partOccHead or prod_line[4] in self.subsHead:
                    head = True
                    value_tags = 11*['headTag']
                # If the line is a value line (thus not a header line) and there is a name of a part
                # then remember the part as a previous part 
                elif prod_line[4] != '':
                    previusPart = level0Part
                elif prod_line[5] != '':
                    previusPart = level1Part
                elif prod_line[6] != '':
                    previusPart = level2Part

                # Set tag background color depending on value
                # If value is missing then bachgroumd color is yellow
                if prod_line[9] == '' or prod_line[9] in unknownVal:
                    value_tags[9] = 'missing'
                else:
                    value_tags[9] = 'available'
                if prod_line[7] in unknownVal:
                    value_tags[7] = 'missing'
                # Insert line
                #print('Values:', prod_line[1], type(prod_line[1]))
                id = self.prod_tree.insert(level0Part,index='end',values=prod_line,tags=value_tags,open=True)

                # If the line is a header line, then continue to next line
                if head == True:
                    continue
                # If the line is a value line and the there is a name of a part
                # # then remember the part as a previous part
                elif prod_line[4] != '':
                    level1Part = id
                    previusPart = level0Part
                elif prod_line[5] != '':
                    level2Part = id
                    previusPart = level1Part
                elif prod_line[6] != '':
                    previusPart = level2Part

    def Define_data_sheet(self):
        # Define ProductView tab in Notebook = = = = = = = = = = = = = = = = = = =    
        # Product_sheet is canvas for scrollbar 
        self.data_sheet = Frame(self.views_noteb)
        self.data_sheet.grid (column=0, row=0,sticky=NSEW) #pack(fill=BOTH, expand=1)  
        self.data_sheet.columnconfigure(0,weight=1)
        self.data_sheet.rowconfigure(0,weight=0)
        #self.data_sheet.rowconfigure(1,weight=0)
        prodText = ['Data sheet', 'Data sheet']
        self.views_noteb.add(self.data_sheet, text=prodText[self.lang_index], sticky=NSEW)
        self.views_noteb.insert("end",self.data_sheet,sticky=NSEW)

        data_canvas = Canvas(self.data_sheet, background='#ddf') 
        #data_canvas.pack()
        data_canvas.grid(column=0,row=0,sticky=NSEW)
        #data_canvas.bind('<Button-2>', RightMouseButton)
        data_canvas.columnconfigure(0,weight=1)
        data_canvas.rowconfigure(0,weight=0)

        self.data_frame = Frame(data_canvas)
        self.data_frame.grid(column=0,row=0,sticky=NSEW) 

        self.data_frame.columnconfigure(0,weight=1)
        self.data_frame.columnconfigure(1,weight=1)
        self.data_frame.columnconfigure(2,weight=1)
        self.data_frame.columnconfigure(3,weight=1)
        self.data_frame.columnconfigure(4,weight=1)
        self.data_frame.columnconfigure(5,weight=1)
        self.data_frame.columnconfigure(6,weight=1)
        self.data_frame.columnconfigure(7,weight=1)
        self.data_frame.columnconfigure(8,weight=1)
        self.data_frame.columnconfigure(9,weight=1)
        self.data_frame.columnconfigure(10,weight=1)
        self.data_frame.rowconfigure(0,weight=0)
        self.data_frame.rowconfigure(1,weight=0)

        prodScroll = Scrollbar(self.data_sheet,orient=VERTICAL,command=data_canvas.yview)
        prodScroll.grid (column=1, row=0, sticky=NS+E)
        data_canvas.config(yscrollcommand=prodScroll.set)

    def Display_data_sheet_view(self):
        ''' Produce a view of a product model in the form of a datasheet'''
        unknownVal   = ['unknown value','onbekende waarde']
        unknownKind  = ['unknown kind' ,'onbekende soort', 'anything', 'iets']
        
        # Set column widths in data sheet
        col_width = [4,20,10,10,20,15,20,4,10,5,10]
        line_nr = -1
        for prod_row in self.prod_model:
            line = prod_row[3:]
            line_nr += + 1
            column_nr  = -1
            head = False
            header1 = False
            header2 = False
            header3 = False
            body    = False
            back = 'white'
            fore = 'black'
            for field_value in line:
                column_nr += + 1
                fieldStr = StringVar()
                span = 1
                column_width = col_width[column_nr]
                
                # Detect start of header line 1: Field_value 1 in column 0 means line_type_1 and header_1
                if column_nr == 0 and field_value == 1:
                    header1 = True
                if header1 == True:
                    if column_nr == 2: span=3
                    elif column_nr == 6: span=5

                # Display on line 1 the line nr, 'Product form' label and the 'kind' label
                if header1 == True and column_nr in [0, 1, 5]:
                    back = '#dfb' # light green
                    fd = ttk.Label(self.data_frame, text=field_value, width=column_width, justify='left',\
                                   background=back, foreground=fore)\
                                   .grid(row=line_nr, column=column_nr, columnspan=span, sticky=EW)

                # Display on line 1 the product_name and kind_name (with another background color)
                if header1 == True and column_nr in [2, 6]:
                    back = 'white'
                    fore = 'black'
                    fd = ttk.Label(self.data_frame, text=field_value, width=column_width, background=back,\
                                   foreground=fore, borderwidth=0)\
                                   .grid(row=line_nr, column=column_nr, columnspan=span, sticky=EW)

                # Detect start of header line 2: Value 2 in column 0 means line_type2 and header2
                if column_nr == 0 and field_value == 2:
                    header2 = True

                # Display on line 2 the description text 
                if header2 == True and column_nr == 3:
                    span = 8
                    back = 'white'
                    fore = 'black'
                    fd = ttk.Label(self.data_frame, text=field_value, width=column_width, justify='left',\
                                   background=back, foreground=fore)\
                                   .grid(row=line_nr, column=column_nr, columnspan=span, rowspan=2, sticky=EW)
                # Display on line 2 the description label
                if header2 == True and column_nr in range(0,3):
                    back = '#dfb'
                    fd = ttk.Label(self.data_frame, text=field_value, width=column_width, justify='left',\
                                   background=back, foreground=fore)\
                                   .grid(row=line_nr, column=column_nr, columnspan=span, rowspan=2, sticky=EW)

                # Detect start of header line 3: Value 3 in column 0 means line_type3 and header3
                if column_nr == 0 and field_value == 3:
                    header3 = True
                    line_nr += + 1
                    
                # Display the line 3 subsequent values
                if header3 == True:
                    back = '#dfb'
                    fd = ttk.Label(self.data_frame, text=field_value, width=column_width, justify="center", \
                                   background=back, foreground=fore)\
                                   .grid(row=line_nr, column=column_nr, columnspan=span, sticky=EW)

                # Detect start of body values: Value >3 in column 0 means body of values
                if column_nr == 0 and field_value > 3:
                    body = True
                # Display the subsequent body values on line type > 3
                if body == True:
                    # Set background color depending on either header, value present of 'unknown'
                    if (column_nr == 1 and (field_value in self.compHead or field_value in self.involHead or\
                                            field_value in self.info_head)) or \
                       (column_nr == 2 and (field_value in self.partOccHead)):
                        # Header line detected; set background color accordingly
                        head = True
                        back = '#dfb'
                    if column_nr == 8 and field_value != '':        #(back == 'white' or back == '#fcc'):
                        back = 'yellow'
                    elif head != True:                 #back == 'yellow' or back == '#fcc':
                        back = 'white'
                    if field_value in unknownVal:
                        field_value = unknownVal[self.lang_index]
                        back = '#fcc'
                    elif field_value in unknownKind:
                        field_value = unknownKind[self.lang_index]
                        back = '#fcc'
                    # Display subsequent body values
                    fd = ttk.Label(self.data_frame, text=field_value, width=column_width, background=back, foreground=fore,\
                                   wraplength=200, borderwidth=0, relief='ridge')\
                                   .grid(row=line_nr, column=column_nr, columnspan=span, sticky=EW)

    def Define_activity_sheet(self):
        activity = ['Activities','Activiteiten']
        self.act_frame = Frame(self.views_noteb)
        self.act_frame.grid (column=0, row=0,sticky=NSEW) #pack(fill=BOTH, expand=1)  
        self.act_frame.columnconfigure(0,weight=1)
        self.act_frame.rowconfigure(0,weight=0)
        self.views_noteb.add(self.act_frame, text=activity[self.lang_index], sticky=NSEW)
        self.views_noteb.insert("end",self.act_frame,sticky=NSEW)
        acts = ['Activity tree', 'Activiteitenboom']
        actLbl = Label(self.act_frame,text=acts[self.lang_index])
        
        self.act_tree = Treeview(self.act_frame,columns=('ActName','PartName','Involved','UID','Kind','Role','RoleUID'),\
                               displaycolumns  =('ActName','PartName','Involved','UID','Kind','Role','RoleUID'),
                               selectmode='browse',height=30)

        #self.act_tree.heading('actName' ,text=q_rh_name     ,anchor=W)
        #self.act_tree.heading('actUID'  ,text='UID'       ,anchor=W)
        #self.act_tree.heading('actKind' ,text='Soort'     ,anchor=W)
        #self.act_tree.heading('aspect1' ,text=occKinds[4] ,anchor=W)
        #self.act_tree.heading('aspect2' ,text=occKinds[5] ,anchor=W)
        #self.act_tree.heading('aspect3' ,text=occKinds[6] ,anchor=W)
        
        self.act_tree.column('#0'       ,minwidth=20,width=20)
        self.act_tree.column('ActName'  ,minwidth=20,width=120)
        self.act_tree.column('PartName' ,minwidth=20,width=80)
        self.act_tree.column('Involved' ,minwidth=20,width=80)
        self.act_tree.column('UID'      ,minwidth=20,width=40)
        self.act_tree.column('Kind'     ,minwidth=20,width=60)
        self.act_tree.column('Role'     ,minwidth=20,width=60)
        self.act_tree.column('RoleUID'  ,minwidth=20,width=40)

        #actLbl.grid (column=0,row=0,sticky=EW)
        self.act_tree.grid(column=0,row=0,sticky=NSEW)

        self.act_tree.columnconfigure(0,weight=0)
        self.act_tree.columnconfigure(1,weight=1)
        self.act_tree.columnconfigure(2,weight=1)
        self.act_tree.columnconfigure(3,weight=1)
        self.act_tree.columnconfigure(4,weight=1)
        self.act_tree.columnconfigure(5,weight=1)
        self.act_tree.columnconfigure(6,weight=1)
        self.act_tree.columnconfigure(7,weight=1)
        self.act_tree.columnconfigure(8,weight=1)
        self.act_tree.rowconfigure(0,weight=0)
        self.act_tree.rowconfigure(1,weight=1)

        self.act_tree.tag_configure('uomTag', option=None, background='#ccf')
        self.act_tree.tag_configure('actTag', option=None, background='#dfd')

        actScroll = Scrollbar(self.act_frame,orient=VERTICAL,command=self.act_tree.yview)
        actScroll.grid (column=0,row=0,sticky=NS+E)
        self.act_tree.config(yscrollcommand=actScroll.set)

    def Define_and_display_documents(self):
        # Destroy earlier documents sheet
        try:
            self.doc_frame.destroy()
        except AttributeError:
            pass
    
        self.Define_documents_sheet()

        # Documents: Display documents and files for selection for display
        for info_line in self.Gel_net.info_model:
            self.doc_tree.insert('',index='end',values=info_line,tags='docTag')

    def Define_documents_sheet(self):
        documents = ['Documents','Documenten']
        self.doc_frame = Frame(self.views_noteb)
        self.doc_frame.grid (column=0, row=0,sticky=NSEW) #pack(fill=BOTH, expand=1)  
        self.doc_frame.columnconfigure(0,weight=1)
        self.doc_frame.rowconfigure(0,weight=0)
        self.views_noteb.add(self.doc_frame, text=documents[self.lang_index], sticky=NSEW)
        self.views_noteb.insert("end",self.doc_frame,sticky=NSEW)
        headings = ['info','obj','carrier','directory','infoName','infoKind',\
                    'objName','fileName','fileKind']
        display_cols = headings[4:]
        self.doc_tree = Treeview(self.doc_frame, columns=(headings),\
                                 displaycolumns=display_cols, selectmode='browse', height=30)
        self.doc_tree.heading('info' ,text='info'    ,anchor=W)
        self.doc_tree.heading('obj'  ,text='obj'     ,anchor=W)
        self.doc_tree.heading('carrier'  ,text='carrier'   ,anchor=W)
        self.doc_tree.heading('directory',text='directory' ,anchor=W)
        self.doc_tree.heading('infoName' ,text='Document'  ,anchor=W)
        self.doc_tree.heading('infoKind' ,text='Doc type'  ,anchor=W)
        self.doc_tree.heading('objName'  ,text='about Object' ,anchor=W)
        self.doc_tree.heading('fileName' ,text='File name' ,anchor=W)
        self.doc_tree.heading('fileKind' ,text='File type' ,anchor=W)
        
        self.doc_tree.column('#0'        ,minwidth=10,width=10)
        self.doc_tree.column('infoName'  ,minwidth=100,width=150)
        self.doc_tree.column('infoKind'  ,minwidth=100,width=150)
        self.doc_tree.column('objName'   ,minwidth=100,width=150)
        self.doc_tree.column('fileName'  ,minwidth=100,width=150)
        self.doc_tree.column('fileKind'  ,minwidth=100,width=150)

        self.doc_tree.grid(column=0,row=0,sticky=NSEW)

        self.doc_tree.columnconfigure(0,weight=1)
        self.doc_tree.rowconfigure(0,weight=0)

        self.doc_tree.tag_configure('docTag', option=None, background='#cfc')

        docScroll = Scrollbar(self.doc_frame,orient=VERTICAL,command=self.doc_tree.yview)
        docScroll.grid (column=0,row=0,sticky=NS+E)
        self.doc_tree.config(yscrollcommand=docScroll.set)

        self.doc_tree.bind(sequence='<Double-1>', func=self.Doc_detail_view)

#------------------------------------------------------------------------
    def Expr_detail_view(self, sel):
        """ Find the selected object from a user selection
            in the query_table that is displayed in the expr_tree view."""
        
        cur_item = self.expr_tree.focus()
        item_dict = self.expr_tree.item(cur_item)
        values = list(item_dict['values'])

        selected_object = self.Gel_net.uid_dict[values[lh_uid_col]]
        print('Display product details of:', selected_object.name)
        if selected_object.category in ['kind', 'kind of physical object', \
                                        'kind of occurrence', 'kind of aspect', \
                                        'kind of role', 'kind of relation']:
            self.Define_and_display_kind_detail_view(selected_object)
        else:
            self.Define_and_display_individual_detail_view(selected_object)

#------------------------------------------------------------------------
    def Kind_detail_view_left(self, sel):
        """ Find the selected left hand object from a user selection with left button
            in the kind_table that is displayed in the kind_tree view."""
        description_text = ['description', 'beschrijving']
        obj_descr_title  = ['Information about ', 'Informatie over ']
        cur_item = self.kind_tree.focus()
        item_dict = self.kind_tree.item(cur_item)
        values = list(item_dict['values'])
        #print('Kind_detail_left:', cur_item, values) #[0], values[1], values[2:]
        selected_object   = self.Gel_net.uid_dict[str(values[0])]

        # If info_kind is a description then display the destription in messagebox
        if values[7] in description_text:
            print('Information {} is not presented on a carrier but is as follows:\n   {}'.\
                  format(values[4], selected_object.description))
            messagebox.showinfo(obj_descr_title[self.lang_index] + selected_object.name, \
                                selected_object.description)
        else:                                       
            print('Display kind details of: {}'.format(selected_object.name))
            self.Define_and_display_kind_detail_view(selected_object)
            if len(self.Gel_net.info_model) > 0:
                self.Define_and_display_documents()

#------------------------------------------------------------------------
    def Kind_detail_view_middle(self, sel):
        """ Find the selected left supertype object from a user selection with middle button
            in the kind_table that is displayed in the kind_tree view.
            Then display its taxonomy
        """

        cur_item = self.kind_tree.focus()
        item_dict = self.kind_tree.item(cur_item)
        values = list(item_dict['values'])
        #print('Comp_detail_middle:', sel.type, sel.keysym, cur_item, values) #[1], values[1], values[2:]
        
        if len(values) > 0:
            if values[1] > 0:
                selected_object   = self.Gel_net.uid_dict[str(values[1])]
                
                # Save sel.type being either 'ButtonPress' or 'KeyPress' with sel.keysym = 'c'
                self.sel_type = sel.type
                
                print('Display taxonomy of: {}'.format(selected_object.name))
                obj_list = []
                obj_list.append(selected_object)
                self.Gel_net.Build_product_views(obj_list)
                # Display taxonomy of selected kind
                self.Define_and_display_taxonomy_of_kinds()
                if len(self.Gel_net.info_model) > 0:
                    self.Define_and_display_documents()
            else:
                print('Kind of object is unknown.')
        else:
            print('Select an item before clicking second mouse button.')
        
#------------------------------------------------------------------------        
    def Kind_detail_view_right(self, sel):
        """ Find the selected kind of aspect or file from a user selection with right button
            in the kind_table that is displayed in the kind_tree view."""
        
        cur_item  = self.kind_tree.focus()
        if cur_item == '':
            print('No item selected. First select item with single left button click, \
then click right button')
            return
        item_dict = self.kind_tree.item(cur_item)
        values = list(item_dict['values'])
        #print('Kind_detail_right:',cur_item, values)

        if len(values) > 8:
            # If values[8] contains a dot (.) then it is interpreted as a file.name with file extension,
            # else it is interpreted as a selected kind of aspect name       
            parts = values[8].rsplit('.', maxsplit=1)
            if len(parts) == 1:
                print('Name {} does not contain a file extension. It is interpreted as a kind of aspect.'.\
                      format(values[8]))
                selected_object = values[2]
                print('Display aspect details of: {}'.format(selected_object.name))
                # Display taxonomy of selected kind
                self.Define_and_display_taxonomy_of_kinds()
            else:
                # Open the file in the file format that is defined by its file extension
                # from directory+file_name
                file_path = os.path.join(values[5], values[8])
                normalized_path = os.path.normpath(file_path)
                os.startfile(normalized_path,'open')
        else:
            print('There is no right hand object to be displayed')
#------------------------------------------------------------------------
    def Prod_detail_view_left(self, sel):
        """ Find the selected left hand object from a user selection with left button
            in the prod_table that is displayed in the prod_tree view."""
        description_text = ['description', 'beschrijving']
        obj_descr_title  = ['Information about ', 'Informatie over ']
        cur_item = self.prod_tree.focus()
        item_dict = self.prod_tree.item(cur_item)
        values = list(item_dict['values'])
        print('Prod_detail_left:', cur_item, values)
        if len(values) > 0:
            if values[0] != '':
                selected_object   = self.Gel_net.uid_dict[str(values[0])]

                # If info_kind is a description then display the destription in messagebox
                if values[7] in description_text:
                    print('Information {} is not presented on a carrier but is as follows:\n   {}'.\
                          format(values[4], selected_object.description))
                    messagebox.showinfo(obj_descr_title[self.lang_index] + selected_object.name, \
                                        selected_object.description)
            else:                                       
                print('Display product details of: {}'.format(selected_object.name))
                self.Define_and_display_individual_detail_view(selected_object)
                
                if len(self.Gel_net.info_model) > 0:
                    self.Define_and_display_documents()

#------------------------------------------------------------------------
    def Prod_detail_view_middle(self, sel):
        """ Find the selected left classifier object from a user selection
            in the prod_table that is displayed in the prod_tree view.
            When the middle mouse button was used the taxonomy of the selected kind is displayed.
            When the 'c' key was used a search for a second classifier in the taxonomy
            (the subtype hierarchy of the selected kind) is started.
            The aspects of the individual object are used to create selection criteria for the
            subtypes in the hierarchy.
            The taxonomy of the selected kind is displayed for selection of the classifier.
        """

        cur_item = self.prod_tree.focus()
        item_dict = self.prod_tree.item(cur_item)
        values = list(item_dict['values'])
        #print('Prod_detail_middle:', sel.type, sel.keysym, cur_item, values, type(values[1])) #[1], values[1], values[2:]
        
        if len(values) > 0:
            if values[1] != '':
                selected_object   = self.Gel_net.uid_dict[str(values[1])]
                #print('sel.type', sel.type, sel.keysym, sel.char)
                # Verify sel.type being either 'ButtonPress' for display of taxonomy
                # or 'KeyPress' with sel.keysym = 'c' (for display for classification by selection of subtype)
                if sel.keysym == 'c':
                    self.modification = 'classification started'
                    self.Gel_net.modified_object = self.Gel_net.uid_dict[str(values[0])]
                    print('Present taxonomy of kind: {} that classifies {} for selection of a subtype'.\
                          format(selected_object.name, self.Gel_net.modified_object.name))
                    
                    # Formulate query_spec including conditions from aspects of individual, if any
                    self.query.Formulate_query_spec_for_individual(selected_object)
                    self.query.Create_query_file()
                    self.query.Interpret_query_spec()
                else:
                    # Mouse ButtonPress: Build views for selected object (kind) and display views
                    print('Display taxonomy of kind: {}'.format(selected_object.name))
                obj_list = []
                obj_list.append(selected_object)
                self.Gel_net.Build_product_views(obj_list)
                # Display taxonomy in taxon view
                self.Define_and_display_taxonomy_of_kinds()

                if len(self.Gel_net.info_model) > 0:
                    self.Define_and_display_documents()
            else:
                print('Kind of object is unknown.')
        else:
            print("Select an item, then click the second mouse button or press 'c' key \
for classying the object.")
        
#------------------------------------------------------------------------        
    def Prod_detail_view_right(self, sel):
        """ Find the selected aspect or file from a user selection with right button
            in the prod_table that is displayed in the prod_tree view."""
        
        cur_item  = self.prod_tree.focus()
        if cur_item == '':
            print('No item selected. First select item with single left button click, \
then click right button')
            return
        item_dict = self.prod_tree.item(cur_item)
        values = list(item_dict['values'])
        print('Prod_detail_right:',cur_item, values)

        if len(values) > 8:
            # If values[8] contains a dot (.) then it is interpreted as a file.name with file extension,
            # else it is interpreted as an selected aspect        
            parts = values[8].rsplit('.', maxsplit=1)
            if len(parts) == 1:
                print('Name {} does not contain a file extension. It is interpreted as an aspect.'.\
                      format(values[8]))
                selected_object = self.Gel_net.uid_dict[str(values[2])]
                print('Display aspect details of: {}'.format(selected_object.name))
                self.Define_and_display_individual_detail_view(selected_object)
            else:
                # Open the file in the file format that is defined by its file extension
                # from directory+file_name
                file_path = os.path.join(values[5], values[8])
                normalized_path = os.path.normpath(file_path)
                os.startfile(normalized_path,'open')
        else:
            print('There is no right hand object to be displayed')

#-------------------------------------------------------------------------        
    def Taxon_detail_view(self, sel):
        """ Find the selected object from a user selection that is made
            in the taxon_model that is displayed in the taxon_tree view."""
        
        #item_dict = self.summ_tree.selection()
        cur_item = self.taxon_tree.focus()
        item_dict = self.taxon_tree.item(cur_item)
        #print('Detail view item:', item_dict['values'])
        values = list(item_dict['values'])
        #print('Taxon values, sel.', values)
        selected_object = self.Gel_net.uid_dict[str(values[0])]

        if sel.num == 1:
            # If mousebutton-1 is used, then Create a detail view 
            print('Display kind details of:',values[0], selected_object.name)
            self.Define_and_display_kind_detail_view(selected_object)
        elif self.modification == 'classification started':
            # if sel.type = 'KeyPress' with sel.keysym = 'c' then 
            # Append selected classifier to modified_object, and add classification relation
            self.Gel_net.Add_classification_relation(self.Gel_net.modified_object, selected_object)

            # Display modified product view
            self.modification = 'classification completed'
            self.Define_and_display_individual_detail_view(self.Gel_net.modified_object)
            print('Classification of {} by classifier {} is added to the network'.\
                  format(self.Gel_net.modified_object.name, selected_object.name))

#-------------------------------------------------------------------------        
    def Summ_detail_view(self, sel):
        """ Find the selected object from a user selection that is made
            in the summ_model that is displayed in the summ_tree view."""
        
        #item_dict = self.summ_tree.selection()
        cur_item = self.summ_tree.focus()
        item_dict = self.summ_tree.item(cur_item)
        #print('Detail view item:', item_dict['values'])
        values = list(item_dict['values'])
        
        selected_object = self.Gel_net.uid_dict[str(values[0])]
        print('Display product details of:',values[0], selected_object.name)
        # Create a detail view 
        self.Define_and_display_individual_detail_view(selected_object)

    def Possibilities_detail_view(self, sel):
        """ Find the selected object from a user selection that is made
            in the possibilities_model that is displayed in the possib_tree view."""
        
        #item_dict = self.possib_tree.selection()
        cur_item = self.possib_tree.focus()
        item_dict = self.possib_tree.item(cur_item)
        #print('Detail view item:', item_dict['values'])
        values = list(item_dict['values'])
        
        selected_object = self.Gel_net.uid_dict[str(values[0])]
        #print('Display product details of:',values[0], selected_object.name)
        # Create a detail view 
        self.Define_and_display_kind_detail_view(selected_object)

    def Indiv_detail_view(self, sel):
        """ Find the selected object from a user selection that is made
            in the indiv_model that is displayed in the indiv_tree view."""
        
        #item_dict = self.indiv_tree.selection()
        cur_item = self.indiv_tree.focus()
        item_dict = self.indiv_tree.item(cur_item)
        #print('Detail view item:', item_dict['values'])
        values = list(item_dict['values'])
        
        selected_object = self.Gel_net.uid_dict[str(values[0])]
        #print('Display product details of:',values[0], selected_object.name)
        # Create a detail view 
        self.Define_and_display_individual_detail_view(selected_object)

    def Define_and_display_kind_detail_view(self, selected_object):
        """ Create a detail view of a kind from a user selection
            and display the view in the kind_model view."""
        self.Gel_net.kind_model[:]  = []
        self.Gel_net.query_table[:] = []
        self.Gel_net.Build_single_product_view(selected_object)

        try:
            self.kind_frame.destroy()
        except AttributeError:
            pass
        
        self.Define_kind_model_sheet()
        self.Display_kind_model_view()

        try:
            self.expr_frame.destroy()
        except AttributeError:
            pass
        
        # Define Expressions view sheet = = = = = = = = = = = = = = = = = = =
        self.Define_expressions_sheet()

        # Expressions view: Display expressions from self.query_table in Treeview:
        for queryLine in self.query_table:
            self.expr_tree.insert('',index='end',values=queryLine,tags='valTag')

    def Define_and_display_individual_detail_view(self, selected_object):
        """ Create a detail view of a product from a user selection
            and display the view in the prod_model view."""
        self.Gel_net.prod_model[:]  = []
        self.Gel_net.query_table[:] = []
        self.Gel_net.Build_single_product_view(selected_object)

        try:
            self.prod_frame.destroy()
        except AttributeError:
            pass
        self.Define_product_model_sheet()
        self.Display_product_model_view()

        try:
            self.data_sheet.destroy()
        except AttributeError:
            pass
        self.Define_data_sheet()
        self.Display_data_sheet_view()

        try:
            self.expr_frame.destroy()
        except AttributeError:
            pass
        # Define Expressions view sheet = = = = = = = = = = = = = = = = = = =
        self.Define_expressions_sheet()

        # Expressions view: Display expressions from self.query_table in Treeview:
        for queryLine in self.query_table:
            self.expr_tree.insert('',index='end',values=queryLine,tags='valTag')

#----------------------------------------------------------
    def Doc_detail_view(self, sel):
        """ Find the selected object from a user selection
            in the info_model that is displayed in the doc_tree view.
            - info_row ('values') = [info.uid, obj.uid, carrier.uid, directory_name,\
                                    info.name, super_info_name, obj.name, \
                                    carrier.name, carrier_kind_name]
        """
        
        cur_item = self.doc_tree.focus()
        item_dict = self.doc_tree.item(cur_item)
        info_row = list(item_dict['values'])

        # If info_kind is a description then display the destription
        description_text  = ['description', 'beschrijving']
        description_title = ['Information about ', 'Informatie over ']
        if info_row[5] in description_text:
            #print('Information {} is not presented on a carrier but is as follows:\n   {}'.\
            #      format(info_row[4], info_row[2]))
            messagebox.showinfo(description_title[self.lang_index] + info_row[6], info_row[2])

        # Verify whether file name (info_row[7]) is presented on a file
        # And verify whether the file name has a file extension (indicated by a dot (.)) 
        parts = info_row[7].rsplit('.', maxsplit=1)
        if len(parts) == 1:
            print('== Error: File name {} does not have a file extension'.format(info_row[7]))
        else:
            # Open the file in the file format that is defined by its file extension
            print('Open file {} about {}'.format(info_row[7], info_row[6]))
            directory_name = info_row[3]
            if directory_name != '':
                file_path = os.path.join(directory_name, info_row[7])
                normalized_path = os.path.normpath(file_path)
                os.startfile(normalized_path,'open')

    def Contextual_facts(self):
        print('Contextual_facts')
        

#------------------------------------------------
class Main():
    def __init__(self):
        pass
    def Verify_table(self):
        print('Verify_table')
        
    def Query_net(self):
        print('Query_net')
        
    def Modify_db(self):
        print('Modify_db')
        
    def Stop_Quit(self):
        print('Stop_Quit')
        
    def Create_net(self):
        print('Create_net')
        
    def Dump_net(self):
        print('Dump_net')
        
    def Load_net(self):
        print('Load_net')
        
    def Read_db(self):
        print('Read_db')

class User():
    def __init__(self):
        self.GUI_lang_name = 'Nederlands'
        self.GUI_lang_index = 1
        
    
if __name__ == "__main__":
    root = Tk()
    main = Main()
    user = User()
    GUI = GUI_views(root, main, user)
    GUI.lang_index = 0
    GUI.lang_name = 'English'
    GUI.categoryInFocus = 'kind'
    
    GUI.Notebook_views()
    root.mainloop()
