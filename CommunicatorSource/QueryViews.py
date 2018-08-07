import os
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, filedialog
from operator import itemgetter

from Bootstrapping import ini_out_path
from Expr_Table_Def import *
from Query import Query
from Display_views import Display_views
from Anything import Anything
from Create_output_file import Create_gellish_expression, Convert_numeric_to_integer, \
     Open_output_file

class Query_view():
    ''' Defines a query window
        for specification of queries in dictionary and models.
    '''
    def __init__(self, gel_net, user_interface):
        #self.main = main
        self.gel_net = gel_net
        self.user_interface = user_interface
        self.views = user_interface.views
        self.query = user_interface.query
        self.unknown_quid = user_interface.unknown_quid
        self.root = user_interface.root
        self.GUI_lang_pref_uids = user_interface.GUI_lang_pref_uids
        self.comm_pref_uids = user_interface.comm_pref_uids

        self.GUI_lang_name = self.user_interface.GUI_lang_name
        self.GUI_lang_uid = self.user_interface.GUI_lang_uid
        self.GUI_lang_index = self.user_interface.GUI_lang_index

        self.lh_options = []
        self.rh_options = []
        self.rel_options = []
        self.unknowns = [] # List of unkown objects that are denoted by an unknown in a query
        self.names_of_unknowns = []
        self.unknown_kind = ['unknown kind' ,'onbekende soort']
        
        # Set default terms for query in user interface
        self.lh_terms = ['elektriciteitskabel', '3 aderige kabel', 'YMvK kabel', 'breedte', \
                         'materiaal','isolatieplaat']
        self.lh_terms.sort()
        self.rel_terms = ['is een soort', \
                          'kan als aspect hebben een', \
                          'moet als aspect hebben een',\
                          'heeft per definitie als aspect een', \
                          'heeft per definitie een schaalwaarde gelijk aan',\
                          'heeft per definitie een schaalwaarde kleiner dan',\
                          'heeft per definitie een schaalwaarde groter dan',\
                          'is per definitie gekwalificeerd als']
        self.rel_terms.sort()
        self.rh_terms = self.lh_terms[:]
        #self.rh_terms.sort() # copy of lh_terms that are already sorted
        self.uoms = ['m', 'mm', 'bar', 'deg C']
        self.uoms.sort()

        self.reply_lang_names = ("English", "Nederlands",  "American",  "Chinese")
        self.reply_language = ['The reply language is', 'De antwoordtaal is']

        self.q_aspects = []
        
    def Query_window(self):
        """ Specify a Search term or UID
            or a Query expression with unknowns and possible multiline conditions.
            Display options for found objects that satisfy the search or query.
            Display definition and aliases and translations of selected option.
            Initiate seach for information about selected option
            by selecting confirmation button.
        """

        if self.user_interface.extended_query:
            query_text = ["Query","Vraag"]
        else:
            query_text = ["Search","Zoek"]
        self.QWindow = Toplevel(self.root)
        self.QWindow.title(query_text[self.GUI_lang_index])
        self.QWindow.columnconfigure(0, weight=1)
        self.QWindow.rowconfigure(0, weight=1)

        # Specify query_frame
        self.query_frame = ttk.Frame(self.QWindow)
        self.query_frame.grid(column=0, row=0, rowspan=30, sticky=NSEW)

        self.query_frame.columnconfigure(0, weight=1)
        self.query_frame.columnconfigure(1, weight=1)
        self.query_frame.columnconfigure(2, weight=1)
        self.query_frame.columnconfigure(3, weight=1)
        self.query_frame.columnconfigure(4, weight=1)
        self.query_frame.columnconfigure(5, weight=1)
        self.query_frame.columnconfigure(6, weight=1)
        self.query_frame.columnconfigure(7, weight=1)
        
        self.query_frame.rowconfigure(0, weight=0)
        self.query_frame.rowconfigure(15, weight=0, minsize=20)
        self.query_frame.rowconfigure(16, weight=1, minsize=300)
##        for row in range(16,30):
##            self.query_frame.rowconfigure(row, weight=1, minsize=20)

    # Define reply language with language selector
        lang_text = ['Reply language:', 'Antwoordtaal:']
        self.reply_lang_label = Label(self.query_frame, \
                                      text=lang_text[self.GUI_lang_index], width=15)
        self.rep_lang_default = StringVar(value=self.GUI_lang_name)
        self.reply_lang_box = ttk.Combobox(self.query_frame, \
                                           textvariable=self.rep_lang_default,\
                                           values=self.reply_lang_names, width=15)
        self.reply_lang_label.grid(column=4, row=1, sticky=W)
        self.reply_lang_box.grid(column=5, row=1, sticky=W)

    # String commonality buttons
        #ImmediateSearchVar = BooleanVar()
        self.case_sensitive_var = BooleanVar()
        self.first_char_match_var = BooleanVar()
        #ExactMatchVar = BooleanVar()
        #IncludeDescrVar = BooleanVar()

        #ImmediateSearchVar.set(True)
        self.case_sensitive_var.set(True)
        self.first_char_match_var.set(True)
        #ExactMatchVar.set(False)
        #IncludeDescrVar.set(False)

        #immText = ["Immediate Search", "Direct zoeken"]
        caseText = ["Case Sensitive", "Hoofdletter gevoelig"]
        firstText = ["First Char Match", "Eerste letter klopt"]
        #exactText = ["Exact Match", "Preciese overeenstemming"]
        #ImmediateSearch = ttk.Checkbutton(self.query_frame, text=immText[self.GUI_lang_index], \
        #                                  variable = ImmediateSearchVar, onvalue = True)
        CaseSensitive = ttk.Checkbutton(self.query_frame, text=caseText[self.GUI_lang_index], \
                                        variable = self.case_sensitive_var, onvalue = True)
        FirstCharMatch = ttk.Checkbutton(self.query_frame, text=firstText[self.GUI_lang_index], \
                                         variable = self.first_char_match_var, onvalue = True)
        #ExactMatch = ttk.Checkbutton(self.query_frame, text=exactText[self.GUI_lang_index], \
        #                             variable = ExactMatchVar, onvalue = True)
        # Include searching in descriptions
        #IncludeDescr = ttk.Checkbutton(self.query_frame, text="Include Description", \
        #                               variable = IncludeDescrVar, onvalue = True)

    # Define English and Dutch example values (initial options) for query
        lhTermListEN = ['?','Paris', 'Eiffel tower', 'France']
        relTermListEN = ['?','is related to (a)','is related to', 'is classified as a', \
                         'is located in', 'has as part']
        rhTermListEN = ['?','city', 'tower', 'country']
        uomTermListEN = ['','inch','mi','s', 'degC', 'psi']

        lhTermListNL = ['?','N51','Groningen','Parijs', 'Eiffeltoren', 'Frankrijk']
        relTermListNL = ['?','is een soort', 'is gerelateerd aan (een)', 'is gerelateerd aan', \
                         'is geclassificeerd als een', 'bevindt zich in', 'heeft als deel']
        rhTermListNL = ['?','isolatieplaat','weg','dorp','stad','toren','land']
        uomTermListNL = ['','mm','m', 's','°C','bar']

        if self.GUI_lang_name == 'Nederlands' or 'Dutch':
            lhTermListD = lhTermListNL
            relTermListD = relTermListNL
            rhTermListD = rhTermListNL
            uomTermListD = uomTermListNL
        else:
            lhTermListD = lhTermListEN
            relTermListD = relTermListEN
            rhTermListD = rhTermListEN
            uomTermListD = uomTermListEN
        
        # Set default values in StringVar's
        self.q_lh_name_str = StringVar(value=lhTermListD[0])
        self.q_rel_name_str = StringVar(value=relTermListD[0])
        self.q_rh_name_str = StringVar(value=rhTermListD[0])
        self.q_uom_name_str = StringVar(value=uomTermListD[0])
        self.q_lh_uid_str = StringVar(value='')
        self.q_rel_uid_str = StringVar(value='')
        self.q_rh_uid_str = StringVar(value='')
        self.q_uom_uid_str = StringVar(value='')
        
        lhCondQStr = []
        relCondQStr = []
        rhCondQStr = []
        uomCondQStr = []
        for i in range(0,3):
            lhCondQStr.append (StringVar())
            relCondQStr.append(StringVar())
            rhCondQStr.append (StringVar())
            uomCondQStr.append(StringVar())

        if self.user_interface.extended_query:
            lh_term = ["Left hand term", "Linker term"]
        else: lh_term = ["Search term", "Zoekterm"]
        rel_term = ["Relation type phrase", "Relatietype frase"]
        rh_term = ["Right hand term", "Rechter term"]
        uom_term = ["Unit of measure", "Meeteenheid"]

    # Query variables widgets definition   
        lhNameLbl = ttk.Label(self.query_frame, text=lh_term[self.GUI_lang_index])
        lhUIDLbl = ttk.Label(self.query_frame,text='UID:')
        if self.user_interface.extended_query:
            relNameLbl = ttk.Label(self.query_frame, text=rel_term[self.GUI_lang_index])
            rhNameLbl = ttk.Label(self.query_frame, text=rh_term[self.GUI_lang_index])
            uomNameLbl = ttk.Label(self.query_frame, text=uom_term[self.GUI_lang_index])
        self.q_lh_name_widget = ttk.Combobox(self.query_frame, \
                                             textvariable=self.q_lh_name_str,\
                                             values=self.lh_terms, width=30)
        #if self.user_interface.extended_query:
        self.q_rel_name_widget = ttk.Combobox(self.query_frame, \
                                              textvariable=self.q_rel_name_str,\
                                              values=self.rel_terms, width=40)
        self.q_rh_name_widget = ttk.Combobox(self.query_frame, \
                                             textvariable=self.q_rh_name_str,\
                                             values=self.rh_terms, width=30)
        self.q_uom_name_widget = ttk.Combobox(self.query_frame, \
                                              textvariable=self.q_uom_name_str,\
                                              values=self.uoms, width=10)
        self.q_lh_uid_widget = ttk.Entry(self.query_frame, \
                                         textvariable=self.q_lh_uid_str, width=10)
        #if self.user_interface.extended_query:
        self.q_rel_uid_widget = ttk.Entry(self.query_frame, \
                                          textvariable=self.q_rel_uid_str, width=10)
        self.q_rh_uid_widget = ttk.Entry(self.query_frame, \
                                         textvariable=self.q_rh_uid_str, width=10)
        self.q_uom_uid_widget = ttk.Entry(self.query_frame, \
                                          textvariable=self.q_uom_uid_str, width=10)

    # Bindings for search uid and search string fields and for extended query fields
        self.q_lh_uid_widget.bind("<KeyRelease>", self.Lh_uid_command)
        self.q_lh_name_widget.bind("<KeyRelease>", self.Lh_search_cmd)
        if self.user_interface.extended_query:
            self.q_rel_name_widget.bind("<KeyRelease>", self.Rel_search_cmd)
            self.q_rh_name_widget.bind("<KeyRelease>", self.Rh_search_cmd)
            #self.q_lh_name_widget.bind("<Button-1>", self.Lh_search_cmd)
            #self.q_rel_name_widget.bind("<Button-1>", self.Rel_search_cmd)
            #self.q_rh_name_widget.bind("<Button-1>", self.Rh_search_cmd)

    # Definition display widget
        def_text = ['Def. of left hand object:', 'Definitie van linker object:']
        fullDefQLbl = ttk.Label(self.query_frame, text=def_text[self.GUI_lang_index])
        fullDefQStr = StringVar()
        self.q_full_def_widget = Text(self.query_frame, width=60, height=3, wrap="word")
        
        defQScroll = ttk.Scrollbar(self.query_frame, orient=VERTICAL, \
                                   command=self.q_full_def_widget.yview)
        self.q_full_def_widget.config(yscrollcommand=defQScroll.set)

    # Aliases display widget
        #aliasText = ['Aliases:','Aliases:']
        #alias_label = ttk.Label(self.query_frame, text=aliasText[self.GUI_lang_index])
        self.alias_tree = ttk.Treeview(self.query_frame,\
                                       columns=('Term', 'Alias_type'),\
                                       displaycolumns=('Alias_type'),\
                                       selectmode='none', height=4)
        term_text = ('     Term', '     Term')
        alias_text = ('Alias type', 'Aliastype')
        #lang_text = ('Language', 'Taal')
        self.alias_tree.heading('#0', text=term_text[self.GUI_lang_index], anchor=W)
        self.alias_tree.heading('Alias_type', text=alias_text[self.GUI_lang_index], anchor=W)
        #self.alias_tree.heading('Language', text=lang_text[self.GUI_lang_index], anchor=W)
        alias_scroll = ttk.Scrollbar(self.query_frame, orient=VERTICAL, \
                                     command=self.alias_tree.yview)
        self.alias_tree.config(yscrollcommand=alias_scroll.set)

    # Aspect frame widget
        nr_of_rows = 24
        if self.user_interface.extended_query:
            nr_of_rows = 4
        aspect_frame = ttk.Frame(self.query_frame, borderwidth=3, relief='ridge')
        aspect_frame.grid(column=6, row=6, columnspan=2, rowspan=nr_of_rows, sticky=NSEW)
        aspect_frame.columnconfigure(0, minsize=10, weight=1)
        aspect_frame.rowconfigure(0, minsize=10, weight=1)
        tree_style = ttk.Style()
        #tree_style.configure(".", font=('Helvetica', 8), foreground="white")
        #tree_style.configure("Treeview", foreground='red')
        tree_style.configure("Treeview.Heading", foreground='blue', background='#cfc')

        # Aspects treeview for selection on aspect value(s)
        aspect_col = ['Aspect', 'Aspect']
        eq_col = ['>=<', '>=<']
        value_col = ['Value', 'Waarde']
        uom_col = ['UoM', 'Eenheid']
        self.aspects_tree = ttk.Treeview(aspect_frame,\
                                         columns=('UID','Name','Rel_uid','UID-2','Parent',\
                                                  'Equality','Value','UoM'),\
                                         displaycolumns=('Equality','Value','UoM'),\
                                         selectmode='extended', height=3)
        self.aspects_tree.heading('#0', text=aspect_col[self.GUI_lang_index], anchor=W)
        self.aspects_tree.heading('Equality', text=eq_col[self.GUI_lang_index], anchor=W)
        self.aspects_tree.heading('Value', text=value_col[self.GUI_lang_index], anchor=W)
        self.aspects_tree.heading('UoM', text=uom_col[self.GUI_lang_index], anchor=W)

        self.aspects_tree.column ('#0', width=200)
        self.aspects_tree.column ('Equality', width=30)
        self.aspects_tree.column ('Value', width=80)
        self.aspects_tree.column ('UoM', width=60)
        self.aspects_tree.grid(column=0, row=0, sticky=NSEW)

        aspect_scroll = ttk.Scrollbar(aspect_frame, orient=VERTICAL, \
                                      command=self.aspects_tree.yview)
        aspect_scroll.grid(column=0, row=0, sticky=NS+E)
        self.aspects_tree.config(yscrollcommand=aspect_scroll.set)
        self.aspects_tree.bind(sequence='<ButtonRelease-1>', \
                               func=self.Determine_selected_aspects)

    # Buttons definition
        #search = ['Search' ,'Zoek']
        confirm = ['Confirm','Bevestig']
        close = ['Close'  ,'Sluit']
        #verify = ['Verify model' ,'Verifieer model']
        #searchBut = ttk.Button(self.query_frame,text=search[self.GUI_lang_index], \
        #                       command=SearchButCmd)
        confirm_button = ttk.Button(self.query_frame,text=confirm[self.GUI_lang_index], \
                                    command=self.Formulate_query_spec)
        close_button = ttk.Button(self.query_frame,text=close[self.GUI_lang_index], \
                                  command=self.Close_query)
        #verifyBut = ttk.Button(self.query_frame,text=verify[self.GUI_lang_index], \
        #                       command=self.query.Verify_model)
        
    # Buttons location in grid
        #ImmediateSearch.grid(column=0, columnspan=2, row=1, sticky=W)
        CaseSensitive.grid(column=0, columnspan=2, row=1, sticky=W)
        FirstCharMatch.grid(column=0, columnspan=2, row=2, sticky=W)
        #ExactMatch.grid(column=0, columnspan=2, row=3, sticky=W)
        #IncludeDescr.grid(column=0, row=4, sticky=W)

        #searchBut.grid(column=6, row=2 ,sticky=EW)
        confirm_button.grid(column=6, row=1, sticky=N+EW)
        close_button.grid(column=7, row=1 ,sticky=EW)
        #verifyBut.grid(column=7, row=2 ,sticky=N+EW)
    
    # Widgets locations in grid
        lhNameLbl.grid(column=0, row=3, sticky=W)
        lhUIDLbl.grid(column=0, row=3, sticky=E)
        if self.user_interface.extended_query:
            relNameLbl.grid(column=2, row=3, sticky=EW)
            rhNameLbl.grid(column=4, row=3, sticky=EW)
            uomNameLbl.grid(column=6, row=3, sticky=EW)
        self.q_lh_uid_widget.grid(column=1, row=3, columnspan=1, rowspan=1, sticky=EW)
        if self.user_interface.extended_query:
            self.q_rel_uid_widget.grid(column=3, row=3, columnspan=1, rowspan=1, sticky=EW)
            self.q_rh_uid_widget.grid(column=5, row=3, columnspan=1, rowspan=1, sticky=EW)
            self.q_uom_uid_widget.grid(column=7, row=3, columnspan=1, rowspan=1, sticky=EW)
        self.q_lh_name_widget.grid (column=0, row=4, columnspan=2, rowspan=1, sticky=EW)
        if self.user_interface.extended_query:
            self.q_rel_name_widget.grid(column=2, row=4, columnspan=2, rowspan=1, sticky=EW)
            self.q_rh_name_widget.grid(column=4, row=4, columnspan=2, rowspan=1, sticky=EW)
            self.q_uom_name_widget.grid(column=6, row=4, columnspan=2, rowspan=1, sticky=EW)

        # Definition location in grid
        fullDefQLbl.grid(column=0, row=5, rowspan=1, sticky=EW)
        self.q_full_def_widget.grid(column=1, row=5, columnspan=7, rowspan=1, sticky=EW)
        defQScroll.grid(column=7, row=5, rowspan=1, sticky=NS+E)

        # Alias location in grid
        #alias_label.grid(column=0, row=6, rowspan=1, sticky=EW)
        self.alias_tree.grid(column=0, row=6, columnspan=5, rowspan=1, sticky=EW)
        alias_scroll.grid(column=4, row=6, rowspan=1, sticky=NS+E)
        
    # Conditions widgets definition
        if self.user_interface.extended_query:
            condit = ["Conditions:", "Voorwaarden:"]
            condLbl = ttk.Label(self.query_frame, text=condit[self.GUI_lang_index])
            for i in range(0,3):
                self.query.lhCondVal.append(ttk.Combobox(self.query_frame,\
                                                         textvariable=lhCondQStr[i], \
                                                         values=self.lh_terms,\
                                                         width=30))
                self.query.relCondVal.append(ttk.Combobox(self.query_frame,\
                                                          textvariable=relCondQStr[i],\
                                                          values=self.rel_terms, \
                                                          width=40))
                self.query.rhCondVal.append(ttk.Combobox(self.query_frame,\
                                                         textvariable=rhCondQStr[i], \
                                                         values=self.rh_terms,\
                                                         width=30))
                self.query.uomCondVal.append(ttk.Combobox(self.query_frame,\
                                                          textvariable=uomCondQStr[i],\
                                                          values=self.uoms, \
                                                          width=10))
    # Conditions widgets location
        if self.user_interface.extended_query:
            condLbl.grid  (column=0, row=8, columnspan=1, sticky=W)
            for i in range(0,3):
                rowNr = 12 + i
                self.query.lhCondVal[i].grid(column=0, row=rowNr, \
                                             columnspan=2, rowspan=1, sticky=EW)
                self.query.relCondVal[i].grid(column=2, row=rowNr, \
                                              columnspan=2, rowspan=1, sticky=EW)
                self.query.rhCondVal[i].grid(column=4, row=rowNr, \
                                             columnspan=2, rowspan=1, sticky=EW)
                self.query.uomCondVal[i].grid(column=6, row=rowNr, \
                                              columnspan=2, rowspan=1, sticky=EW)
        
    # Options for selection widgets definition
        select_term = ["Select one of the following options:", \
                       "Kies één van de volgende opties:"]
        opt_label = ttk.Label(self.query_frame, text=select_term[self.GUI_lang_index])
    # Option label widget location
        opt_label.grid(column=0, row=15, columnspan=3, rowspan=1, sticky=EW)

    # lh Options frame in query_frame for lh options Treeview
        nr_cols = 6
        if self.user_interface.extended_query:
            nr_cols = 8
        lh_opt_frame = ttk.Frame(self.query_frame, borderwidth=3, relief='ridge')
        lh_opt_frame.grid(column=0, row=16, columnspan=nr_cols, rowspan=1, sticky=NSEW)
        lh_opt_frame.columnconfigure(0, minsize=10, weight=1)
        lh_opt_frame.rowconfigure(0, minsize=3, weight=1)

        uid_text = ('UID', 'UID')
        left_uid_text = ['Left UID', 'Linker UID']
        if self.user_interface.extended_query:
            uid_col = left_uid_text
        else:
            uid_col = uid_text
        nameCol = ['Name', 'Naam']
        kindCol = ['Kind', 'Soort']
        commCol = ['Community', 'Taalgemeenschap']
        langCol = ['Language', 'Taal']
        relaCol = ['Relation UID', 'Relatie UID']
        righCol = ['Right UID', 'Rechter UID']

        tree_height = 15
        if self.user_interface.extended_query:
            tree_height = 5
        self.lh_options_tree = ttk.Treeview(lh_opt_frame,\
                                            columns=('UID', 'Name','Kind','Comm','Lang'),\
                                            displaycolumns=('Name','Kind','Comm','Lang'),\
                                            selectmode='browse', height=tree_height)
        self.lh_options_tree.heading('#0', text=uid_col[self.GUI_lang_index], anchor=W)
        self.lh_options_tree.heading('Name', text=nameCol[self.GUI_lang_index], anchor=W)
        self.lh_options_tree.heading('Kind', text=kindCol[self.GUI_lang_index], anchor=W)
        self.lh_options_tree.heading('Comm', text=commCol[self.GUI_lang_index], anchor=W)
        self.lh_options_tree.heading('Lang', text=langCol[self.GUI_lang_index], anchor=W)

        self.lh_options_tree.column ('#0', width=80)
        #self.lh_options_tree.column ('UID', minwidth=40, width=80)
        self.lh_options_tree.column ('Name', minwidth=100, width=200)
        self.lh_options_tree.column ('Kind', minwidth=100, width=200)
        self.lh_options_tree.column ('Comm', minwidth=80, width=160)
        self.lh_options_tree.column ('Lang', minwidth=50, width=100)

        self.lh_options_tree.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=NSEW)

        self.lh_options_tree.columnconfigure(0, weight=1)
        self.lh_options_tree.columnconfigure(1, weight=1)
        self.lh_options_tree.columnconfigure(2, weight=1)
        self.lh_options_tree.columnconfigure(3, weight=1)
        self.lh_options_tree.columnconfigure(4, weight=1)
        self.lh_options_tree.rowconfigure(0, weight=1)

        lhOptScroll = ttk.Scrollbar(lh_opt_frame, orient=VERTICAL, \
                                    command=self.lh_options_tree.yview)
        lhOptScroll.grid (column=0, row=0, sticky=NS+E)
        self.lh_options_tree.config(yscrollcommand=lhOptScroll.set)

        self.lh_options_tree.bind(sequence='<ButtonRelease-1>', \
                                  func=self.Set_selected_q_lh_term)

        if self.user_interface.extended_query:
        # rel Options frame in query_frame for rel options Treeview
            rel_opt_frame = ttk.Frame(self.query_frame, borderwidth=3, relief='ridge')
            rel_opt_frame.grid(column=0, row=21, columnspan=8, rowspan=1, sticky=NSEW)
            rel_opt_frame.columnconfigure(0, minsize=10, weight=1)
            rel_opt_frame.rowconfigure(0, minsize=10, weight=1)

            self.rel_options_tree = ttk.Treeview(rel_opt_frame,\
                                                 columns=('UID','Name','Kind','Comm','Lang'),\
                                                 displaycolumns='#all', selectmode='browse', \
                                                 height=tree_height)
            self.rel_options_tree.heading('#0', anchor=W)
            self.rel_options_tree.heading('UID',  text=relaCol[self.GUI_lang_index], anchor=W)
            self.rel_options_tree.heading('Name', text=nameCol[self.GUI_lang_index], anchor=W)
            self.rel_options_tree.heading('Kind', text=kindCol[self.GUI_lang_index], anchor=W)
            self.rel_options_tree.heading('Comm', text=commCol[self.GUI_lang_index], anchor=W)
            self.rel_options_tree.heading('Lang', text=langCol[self.GUI_lang_index], anchor=W)

            self.rel_options_tree.column ('#0', width=10)
            self.rel_options_tree.column ('UID',  minwidth=40 , width=80)
            self.rel_options_tree.column ('Name', minwidth=100, width=200)
            self.rel_options_tree.column ('Kind', minwidth=100, width=200)
            self.rel_options_tree.column ('Comm', minwidth=80 , width=160)
            self.rel_options_tree.column ('Lang', minwidth=50 , width=100)

            #relOptLbl.grid (column=0, row=0,sticky=EW)
            self.rel_options_tree.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=NSEW)

            self.rel_options_tree.columnconfigure(0, weight=0)
            self.rel_options_tree.columnconfigure(1, weight=1)
            self.rel_options_tree.columnconfigure(2, weight=1)
            self.rel_options_tree.columnconfigure(3, weight=1)
            self.rel_options_tree.columnconfigure(4, weight=1)
            #self.rel_options_tree.columnconfigure(5, weight=1)
            self.rel_options_tree.rowconfigure(0, weight=1)

            relOptScroll = ttk.Scrollbar(rel_opt_frame,orient=VERTICAL,\
                                         command=self.rel_options_tree.yview)
            relOptScroll.grid (column=0, row=0, sticky=NS+E)
            self.rel_options_tree.config(yscrollcommand=relOptScroll.set)

            self.rel_options_tree.bind(sequence='<ButtonRelease-1>', \
                                       func=self.Set_selected_q_rel_term)

        # rh Options frame in query_frame for rh options Treeview
            rh_opt_frame = ttk.Frame(self.query_frame, borderwidth=3, relief='ridge')
            rh_opt_frame.grid (column=0, row=26, columnspan=8, rowspan=1, sticky=NSEW)
            rh_opt_frame.columnconfigure(0, minsize=10, weight=1)
            rh_opt_frame.rowconfigure(0, minsize=10, weight=1)
            
            #rhOptVal = ttk.Combobox(self.query_frame,textvariable=rhSelect,\
            #                        values=rhOptionList, width=40, postcommand=UpdateRhNames)
            self.rh_options_tree = ttk.Treeview(rh_opt_frame,\
                                                columns=('UID','Name','Kind','Comm','Lang'),\
                                                displaycolumns='#all', selectmode='browse', \
                                                height=tree_height)
            self.rh_options_tree.heading('#0', anchor=W)
            self.rh_options_tree.heading('UID',  text=righCol[self.GUI_lang_index], anchor=W)
            self.rh_options_tree.heading('Name', text=nameCol[self.GUI_lang_index], anchor=W)
            self.rh_options_tree.heading('Kind', text=kindCol[self.GUI_lang_index], anchor=W)
            self.rh_options_tree.heading('Comm', text=commCol[self.GUI_lang_index], anchor=W)
            self.rh_options_tree.heading('Lang', text=langCol[self.GUI_lang_index], anchor=W)

            self.rh_options_tree.column ('#0'     ,width=10)
            self.rh_options_tree.column ('UID'    ,minwidth=40 , width=80)
            self.rh_options_tree.column ('Name'   ,minwidth=100, width=200)
            self.rh_options_tree.column ('Kind'   ,minwidth=100, width=200)
            self.rh_options_tree.column ('Comm'   ,minwidth=80 , width=160)
            self.rh_options_tree.column ('Lang'   ,minwidth=50 , width=100)

            #rhOptLbl.grid (column=0, row=0,sticky=EW)
            self.rh_options_tree.grid(column=0, row=0, columnspan=1, rowspan=1, sticky=NSEW)

            self.rh_options_tree.columnconfigure(0, weight=0)
            self.rh_options_tree.columnconfigure(1, weight=1)
            self.rh_options_tree.columnconfigure(2, weight=1)
            self.rh_options_tree.columnconfigure(3, weight=1)
            self.rh_options_tree.columnconfigure(4, weight=1)
            #self.rh_options_tree.columnconfigure(5, weight=1)
            self.rh_options_tree.rowconfigure(0, weight=1)

            rhOptScroll = ttk.Scrollbar(rh_opt_frame,orient=VERTICAL,\
                                        command=self.rh_options_tree.yview)
            rhOptScroll.grid (column=0, row=0, sticky=NS+E)
            self.rh_options_tree.config(yscrollcommand=rhOptScroll.set)

            self.rh_options_tree.bind(sequence='<ButtonRelease-1>', \
                                      func=self.Set_selected_q_rh_term)

        # Binding GUI language choice
        self.reply_lang_box.bind("<<ComboboxSelected>>",self.Determine_reply_language)

        # Set the reply language initially identical to the GUI language
        self.user_interface.Set_reply_language(self.GUI_lang_name)
        self.views.Display_message(
                'The reply language is {}'.format(self.user_interface.reply_lang_name),\
                'De antwoordtaal is {}'.format(self.user_interface.reply_lang_name))

    def Determine_reply_language(self, event):
        ''' Get the user specified reply language and report it '''
        
        reply_lang_name = self.reply_lang_box.get()
        self.user_interface.Set_reply_language(reply_lang_name)
        self.views.Display_message(
                'The reply language is {}'.format(self.user_interface.reply_lang_name),\
                'De antwoordtaal is {}'.format(self.user_interface.reply_lang_name))

    def Lh_uid_command(self, event):
        """ Search for UID in semantic network
            Search in vocabulary for left hand uid.
            == OptionsTable: optionNr,whetherKnown,langUIDres,commUIDres,
                             result_string,resultUID,is_called_uid,kindKnown,kind
        """
        #print('Lh uid entry:',event.char)

        # Delete previous options
        self.lh_options[:] = []
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
            lh = self.gel_net.uid_dict[lh_uid]
            
            #print("  Found lh: ", lh_uid, lh.name)
            # => lh_options: optionNr, whetherKnown, langUIDres, commUIDres, result_string,\
            #                resultUID, is_called_uid, kindKnown, kind
            if len(lh.names_in_contexts) > 0:
                #print('Lang_prefs:', self.gel_net.reply_lang_pref_uids)
                #print('Names in contexts:', lh.names_in_contexts)
                # Build option with preferred name from names_in_contexts
                # Determine the full definition of the obj in the preferred language
                lang_name, comm_name, preferred_name, full_def = \
                           self.user_interface.Determine_name_in_context(lh)
                option = [1, 'known'] + [lang_name, comm_name, preferred_name] \
                         + [lh.uid, '5117', 'known', lh.kind.name]
                #print('Lh_option', option)
                self.lh_options.append(option)
                opt = [option[5], option[4], option[8], comm_name, lang_name]
                self.lh_options_tree.insert('', index='end', values=opt, text=opt[0])

                # Display lh_object uid
                self.query.q_lh_uid = lh_uid
                self.q_lh_uid_str.set(str(lh_uid))
                
            # delete earlier definition text. Then replace by new definition text
            self.q_full_def_widget.delete('1.0', END)
            # Display full definition
            self.q_full_def_widget.insert('1.0',full_def)
        except KeyError:
            pass

    def Lh_search_cmd(self, event):
        """ Search or Query in semantic network
            An entry in QueryWindow can be just a name (lhString
            (for search on UID see Lh_uid_command)
            or a full question with possible condition expressions:
            (lhString,relString,rhString optionally followed by one or more conditions):
       
            lhCommonality = case sensitivity: 'cs/ci';
                                  (partially/front end) identical 'i/pi/fi'
            lhCommonality = input('Lh-commonality
                                  (default: csfi-case sensitive, front-end identical): ')

            Search in vocabulary for left hand term as part of building a question.

            == OptionsTable: optionNr,whetherKnown,langUIDres,commUIDres,
                             result_string,resultUID,is_called_uid,kindKnown,kind
        """

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
        self.lh_options[:] = []
        
        # Remove possible earlier options
        x = self.lh_options_tree.get_children()
        for item in x: self.lh_options_tree.delete(item)
        
        # Determine lh_options for lh term in query
        lhString = self.q_lh_name_widget.get()
        self.found_lh_uid, self.lh_options = \
                           self.Solve_unknown(lhString, string_commonality)
        #print("  Found lh: ", lhString, self.unknown_quid, \
        #      self.lh_options[0:3])

        # => lh_options: optionNr, whetherKnown, langUIDres, commUIDres, result_string,\
        #                resultUID, is_called_uid, kindKnown, kind
        # Sort the list of options alphabetically by name,
        # and determine lang_names and display options
        if len(self.lh_options) > 0:
            if len(self.lh_options) > 1:
                # Sort options by name
                self.lh_options.sort(key=itemgetter(4))
            # Find lang_name and comm_name from uids for option display
            for option in self.lh_options:
                if option[2] == '':
                    lang_name = 'unknown'
                else:
                    if self.GUI_lang_index == 1:
                        lang_name = self.gel_net.lang_dict_NL[option[2]]
                    else:
                        lang_name = self.gel_net.lang_dict_EN[option[2]]
                if option[3] == '':
                    comm_name = 'unknown'
                else:
                    comm_name = self.gel_net.community_dict[option[3]]

                # Display option in lh_options_tree
                opt = [option[5], option[4], option[8], comm_name, lang_name]
                self.lh_options_tree.insert('',index='end',values=opt, text=opt[0])

            # Display lh_object uid
            self.query.q_lh_uid = self.lh_options[0][5]
            self.q_lh_uid_str.set(str(self.query.q_lh_uid))
            
        # Delete earlier definition text. Then replace by new definition text
        self.q_full_def_widget.delete('1.0', END)
        full_def = ''
        int_q_lh_uid, integer = Convert_numeric_to_integer(self.query.q_lh_uid)
        if integer is False or int_q_lh_uid >= 100:
            # If lh_object is known then determine and display full definition
            self.query.q_lh_category = self.lh_options[0][8]
            obj = self.gel_net.uid_dict[self.query.q_lh_uid]
            # Determine the full definition of the obj in the preferred language
            lang_name, comm_name, preferred_name, full_def = \
                       self.user_interface.Determine_name_in_context(obj)
        # Display full definition
        self.q_full_def_widget.insert('1.0',full_def)
            
#----------------------------------------------------------------------
    def Rel_search_cmd(self, event):
        """ Search or Query in Ontology and Model
            Entry in QueryWindow is a question with possible condition expressions
            (lhString,relString,rhString):
       
            lhCommonality = 'csfi'
            lhCommonality = input('Lh-commonality
                                  (default: csfi-case sensitive, front-end identical): ')

            Search in vocabulary for left hand, relation type and right hand terms 
            and build a question

            == Options: optionNr,whetherKnown,langUIDres,commUIDres,
                        result_string,resultUID,is_called_uid,kindKnown,kind
        """

        #print('Rel Entry:',event.char)
        if event.keysym not in ['Shift_L', 'Shift_R']:

            front_end = self.first_char_match_var.get()
            case_sens = self.case_sensitive_var.get()

            # Delete previous list of rel_options in tree
            self.rel_options[:] = []
            x = self.rel_options_tree.get_children()
            for item in x: self.rel_options_tree.delete(item)
            
            # Get relation type name (relString) from user interface
            relString = self.q_rel_name_widget.get()
            #if event != '': relString = relString # + event.char
            if relString == 'any':
                if self.GUI_lang_index == 1:
                    relString = 'binaire relatie'
                else:
                    relString = 'binary relation'
                self.q_rel_name_widget.set(relString)
            if relString == '':
                relString = 'binary relation'
            string_commonality = 'csfi'
            self.foundRel, self.rel_options = \
                           self.Solve_unknown(relString, string_commonality)
            #print('  OptRel:',self.rel_options)
            
            # == rel_opions: optionNr,whetherKnown,langUIDres,commUIDres,
            #                result_string,resultUID,is_called_uid,kindKnown,kind 
            # If rel_options are available, then sort the list and display in rel_options tree
            if len(self.rel_options) > 0:
                self.query.q_rel_uid = self.rel_options[0][5]
                int_q_rel_uid, integer = Convert_numeric_to_integer(self.query.q_rel_uid)
                if integer is False or int_q_rel_uid > 100:
                    obj = self.gel_net.uid_dict[self.query.q_rel_uid]
                    self.q_rel_uid_str.set(str(self.query.q_rel_uid))
                if len(self.rel_options) > 1:
                    # Sort the list of options alphabetically by name
                    self.rel_options.sort(key=itemgetter(4))
                for option in self.rel_options:
                    if option[2] == 0:
                        lang_name = 'unknown'
                    else:
                        lang_name = self.gel_net.lang_uid_dict[option[2]]
                    if option[3] == 0:
                        comm_name = 'unknown'
                    else:
                        comm_name = self.gel_net.community_dict[option[3]]
                    opt = [option[5], option[4], option[8], comm_name, lang_name]
                    self.rel_options_tree.insert('', index='end', values=opt)        
#------------------------------------------------------------------
    def Rh_search_cmd(self, event):
        """ Search or Query in Ontology and Model
            An entry in QueryWindow (lhString,relString,rhString)
            is a question with possible condition expressions:
       
            rhCommonality = input('Rh-commonality
                                  (default: csfi-case sensitive, front-end identical): ')

            Search for string in vocabulary for candidates for right hand term 
            and build a question

            == Options: optionNr,whetherKnown,langUIDres,commUIDres,
                        result_string,resultUID,is_called_uid,kindKnown,kind
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
            self.rh_options[:]  = []
            x = self.rh_options_tree.get_children()
            for item in x: self.rh_options_tree.delete(item)

            # Get the rh_string and search for options in the dictionary
            rhString = self.q_rh_name_widget.get()
            self.foundRh, self.rh_options = \
                          self.Solve_unknown(rhString, string_commonality)
            #print('  OptRh:',self.rh_options);

            # == rh_options: optionNr,whetherKnown,langUIDres,commUIDres,
            #                result_string,resultUID,is_called_uid,kindKnown,kind
            # If rh_options are available,
            # then sort the list and display them in the rh_options tree
            if len(self.rh_options) > 0:
                self.query.q_rh_uid = self.rh_options[0][5]
                #obj = self.gel_net.uid_dict[self.query.q_rh_uid]
                self.q_rh_uid_str.set(str(self.query.q_rh_uid))            
                self.query.q_rh_category = self.rh_options[0][8]
                if len(self.rh_options) > 1:
                    # Sort the list of options alphabetically by name
                    self.rh_options.sort(key=itemgetter(4))
                for option in self.rh_options:
                    if option[2] == 0:
                        lang_name = 'unknown'
                    else:
                        lang_name = self.gel_net.lang_uid_dict[option[2]]
                    if option[3] == 0:
                        comm_name = 'unknown'
                    else:
                        comm_name = self.gel_net.community_dict[option[3]]
                    opt = [option[5],option[4],option[8],comm_name,lang_name]
                    self.rh_options_tree.insert('', index='end', values=opt)

    def Determine_selected_aspects(self, event):
        ''' Determine one or more selected aspects and their values
            and add them to the query.
            Note: values for the same aspects are alternative options (or)
                  values for different aspects are additional requirements (and)
        '''
        self.query.aspect_values = []
        selected_aspects = self.aspects_tree.selection()
        #print('Selected aspects:', selected_aspects)
        if len(selected_aspects) > 0:
            for aspect in selected_aspects:
                aspect_dict = self.aspects_tree.item(aspect)
                aspect_values = list(aspect_dict['values'])
                print('Query aspects:', aspect_values)
                self.query.aspect_values.append(aspect_values)

    def Solve_unknown(self, search_string, string_commonality):
        """ Determine the available options (UIDs and names) in the dictionary
            that match the search_string.
            Collect options in lh, rel and rh optionsTables for display and selection.

            - search_string = the string to be found in Gel_dict
              with corresponding lang_uid and comm_uid.
            - string_commonality is one of:
              cipi, cspi, cii, csi, cifi, csfi
              (case (in)sensitive partial/front end identical

            Returnparameters:
            == options (Lh, Rel or Rh):
               optionNr, whetherKnown, langUIDres, commUIDres, result_string,
               resultUID, isCalled, objectTypeKnown, kind (of resultUID).
               OptionTables have basically the same table structure
                 as the namingTable, but is extended with extra columns.

            == Gel_dict columns: [lang_uid, comm_uid, term], [UID, naming_uid, part_def]
         
            Process: Determine whether search_string equals 'what' etc. or whether it occurs one or more times in vocabulary Gel_dict.
            Collect options in OptionTables, for selecting a preferred option.
        """
        # Initialize indicator whether the search string is an unknown (UID 1-99) or not.
        whetherKnown = 'unknown'
        objectTypeKnown = 'unknown'
        option = []
        options = []
        unknown_terms = ['', '?', 'any', 'what', 'which', 'who', 'where', \
                         'wat', 'welke', 'wie', 'waar']
        found_uid = ''
        is_called_uid = '5117'

        # If search string denotes an unknown from the list unknown_terms
        # then add unknown to the list of options
        if search_string in unknown_terms:
            if search_string == '':
                result_string = 'blank';
                return found_uid, options
            else:
                result_string = search_string
            if result_string not in self.names_of_unknowns:
                # Create an object for the (list of) unknown(s)
                self.unknown_quid += 1
                unknown = Anything(str(self.unknown_quid), result_string)
                self.unknowns.append(unknown)
                self.names_of_unknowns.append(result_string)
                optionNr = 1
                option.append(optionNr) 
                option.append(whetherKnown)
                option.append(self.GUI_lang_pref_uids[1])
                option.append(self.comm_pref_uids[0])
                option.append(result_string)
                option.append(str(self.unknown_quid))
                option.append(is_called_uid)
                option.append(objectTypeKnown)
                option.append(self.unknown_kind[self.GUI_lang_index])

                options.append(option)
                found_uid = str(self.unknown_quid)
            else:
                # Search in earlier collected list of unknowns
                # for object with name search_string
                for unknown in self.unknowns:
                    if unknown.name == search_string:
                        found_uid = unknown.uid
                        continue
            if found_uid == '':
                self.user_interface.Message_UI(
                    'No uid found.',
                    'Er is geen uid gevonden.')
            return found_uid, options
        
        # Search for full search_string in GellishDict
        candidates = self.gel_net.Query_network_dict(search_string, string_commonality)

        # Collect found option in 'options' list for display and selection
        if len(candidates) > 0:
            #print ("nr of candidates:",len(candidates), self.GUI_lang_pref_uids)
            optionNr = 0
            for candidate in candidates:
                # Only add the candidate if uid of language
                # corresponds with uid from GUI_lang_pref_uids
                # because the query is in the GUI_language
                if candidate[0][0] not in self.GUI_lang_pref_uids:
                    continue
                whetherKnown = 'known'
                option = []
                optionNr = optionNr + 1
                option.append(optionNr)
                option.append(whetherKnown)
                # Add candidate fields to option (in column (2,3,4),(5,6,7)
                for part in candidate:
                    for field in part:
                        option.append(field)
                #print ("option:",len(candidates), option)

                #== option: optionNr, whetherKnown, langUID, commUID, result_string, \
                #           resultUID, objectTypeKnown, kind_name (of resultUID).

                # If result_uid is a known uid (being alphanumeric or >= 100) then
                # then find the object and its supertype or classifier
                # and add the object to the list of options
                
                result_uid, integer = Convert_numeric_to_integer(option[5])
                if integer is False or result_uid >= 100:
                    # UID is of a known object (alpha or in range above unknowns (1-100))
                    # then identify the object.
                    obj = self.gel_net.uid_dict[str(result_uid)]
                    
                    # Find and append the name of the kind
                    # (the supertype or classifier of the option)
                    if len(obj.supertypes) > 0:
                        pref_kind_name = obj.supertypes[0].name
                        # Find the first name in the preferred language
                        # of the first supertype in the GUI_language
                        if len(obj.supertypes[0].names_in_contexts) > 0:
                            lang_name, comm_name_supertype, pref_kind_name, descr_of_super = \
                                self.user_interface.Determine_name_in_context(obj.supertypes[0])
                    elif len(obj.classifiers) > 0:
                        pref_kind_name = obj.classifiers[0].name
                        # Find the first name in the preferred language
                        # of the first classifier in the GUI_language
                        if len(obj.classifiers[0].names_in_contexts) > 0:
                            lang_name, comm_name_supertype, pref_kind_name, descr_of_super = \
                                self.user_interface.Determine_name_in_context(obj.classifiers[0])
##                        for name_in_context in obj.classifiers[0].names_in_contexts:
##                            if name_in_context[0] == self.GUI_lang_uid:
##                                pref_kind_name = name_in_context[2]
##                                continue
                    else:
                        pref_kind_name = obj.category
                    option.append(pref_kind_name)
                    
##                    # Determine the direct supertype(s), if any    
##                    supers = obj.supertypes
##                    option.append(obj.name) #names_in_contexts[0][2])
                else:
                    #option.append('unknown')       # objectType
                    option.append(self.unknown_kind[self.GUI_lang_index])

                # Add the option to the list of options 
                options.append(option)
                found_uid = option[5]
                
        # If not found in vocabulary, return with name of search_string
        # (being the unknown) and next UID.
        else:   # nrOfFounds == 0:
            if search_string not in self.names_of_unknowns:
                # Create an object for the (list of) unknown(s)
                self.unknown_quid += 1
                unknown = Anything(str(self.unknown_quid), search_string)
                self.unknowns.append(unknown)
                whetherKnown = 'unknown'
                self.names_of_unknowns.append(search_string)
                optionNr = 1
                option.append(optionNr)
                option.append(whetherKnown)
                option.append(self.GUI_lang_pref_uids[1])
                option.append(self.comm_pref_uids[0])
                option.append(search_string)
                option.append(str(self.unknown_quid))
                option.append(is_called_uid)
                option.append(objectTypeKnown)
                option.append(self.unknown_kind[self.GUI_lang_index])

                options.append(option)
                    
                self.user_interface.Message_UI(
                    'String <{}> not found in the dictionary. UID = {}. '.\
                    format(search_string, self.unknown_quid),\
                    'Term <{}> is niet gevonden in het woordenboek. UID = {}. '.\
                    format(search_string, self.unknown_quid))
                found_uid = self.unknown_quid
            else:
                # Search in unknowns for object with name search_string
                for obj in self.unknowns:
                    if obj.name == search_string:
                        found_uid = obj.uid
                        break
            if found_uid == '':
                self.user_interface.Message_UI(
                    'The found UID is blank, which is incorrect.',\
                    'De gevonden UID is blanco, hetgeen niet correct is.')
                 
        return found_uid, options

    def Set_selected_q_lh_term(self, ind):
        """ Put the lh_object that is selected from lh_options
            in the query (q_lh_name_str and q_lh_uid_str)
            and display its textual definition.
            Then determine the kinds of relations
            that relate to that lh_object or its subtypes
            for display their phrases in dropdown listbox and selection.
            And determine the synonyms and translations of lh_object name.
        """
        item = self.lh_options_tree.selection()
        ind = self.lh_options_tree.index(item) 
        if len(self.lh_options) == 0:
            self.user_interface.Message_UI(
                'Warning: No option is selected yet. Please try again.',
                'Waarschuwing: Er is nog geen optie geselecteerd. Probeer nogmaals.')
            return
        self.query.lhSel = self.lh_options[ind]
        # Determine UID and Name of selected option
        self.query.q_lh_uid = self.query.lhSel[5]
        self.query.q_lh_name = self.query.lhSel[4]
        self.q_lh_uid_str.set(str(self.query.q_lh_uid))
        self.q_lh_name_str.set(self.query.q_lh_name)
        self.q_full_def_widget.delete('1.0',END)
        
        full_def = ''
        # Determine the selected object via its uid
        int_q_lh_uid, integer = Convert_numeric_to_integer(self.query.q_lh_uid)
        # If not unknown
        if integer is False or int_q_lh_uid >= 100:
            self.query.q_lh_category = self.query.lhSel[8]
            obj = self.gel_net.uid_dict[self.query.q_lh_uid]
            
            # Determine the full definition of the selected object in the preferred language
            lang_name, comm_name, preferred_name, full_def = \
                       self.user_interface.Determine_name_in_context(obj)
            #print('FullDef:',self.query.q_lh_uid, self.query.q_lh_name,\
            #      self.query.q_lh_category,full_def)
        # Display full definition
        self.q_full_def_widget.insert('1.0', full_def)

        self.q_aspects[:] = []
        # If the lh_object is known,
        # then determine the kinds of relations that relate to that lh_object
        #is_called_uid = '5117'
        if integer is False or int_q_lh_uid >= 100:
            rel_options = []
            #opt_nr = 0
            lh_object = self.gel_net.uid_dict[self.query.q_lh_uid]
            # Determine list of subtypes of the lh_object
            sub_types, sub_type_uids = self.gel_net.Determine_subtypes(lh_object)
            sub_types.append(lh_object)
            for lh_obj_sub in sub_types:
                # Determine rel types and store results in self.lh_obj_relation_types
                self.Determine_rel_types_for_lh_object(lh_obj_sub)
                
                # Create option list for each found kind of relation
                for rel_type in self.lh_obj_relation_types:
                    if len(rel_type.base_phrases_in_contexts) > 0:
                        for phrase_in_context in rel_type.base_phrases_in_contexts:
                            # If language of phrase is as requested and phrase matches
                            # then add phrase to options (if not yet present)
                            if phrase_in_context[0] == self.GUI_lang_uid:
                                rel_option = phrase_in_context[2]
                                if rel_option not in rel_options:
                                    rel_options.append(rel_option)
                                    #print('Rel type option:', rel_option)
                    elif len(rel_type.inverse_phrases_in_contexts) > 0:
                        # The same for an inverse phrase
                        for phrase_in_context in rel_type.inverse_phrases_in_contexts:
                            if phrase_in_context[0] == self.GUI_lang_uid:
                                rel_option = phrase_in_context[2]
                                if rel_option not in rel_options:   
                                    rel_options.append(rel_option)
                                    #print('Rel type option:', rel_option)

                self.Determine_aspect_and_value_options(lh_obj_sub)

            # Delete previous characteristics
            x = self.aspects_tree.get_children()
            for item in x: self.aspects_tree.delete(item)
            # Insert new list of characteristics in aspects_tree
            if len(self.q_aspects) > 0:
                # Sort aspect values by kind of aspect name and by value
                self.q_aspects.sort(key=itemgetter(4,6))
                for asp in self.q_aspects:
                    #print('Asp:', asp)
                    if asp[1] == '':
                        self.aspects_tree.insert(asp[4], index='end',
                                                 values=asp,
                                                 text=asp[1], open=False)
                    else:
                        self.aspects_tree.insert(asp[4], index='end',
                                                 iid=asp[1],
                                                 values=asp,
                                                 text=asp[1], open=False)
                        
            rel_options.sort()
            self.gel_net.rel_terms = rel_options
            self.q_rel_name_widget.config(values=self.gel_net.rel_terms)

            # Delete previous aliases
            x = self.alias_tree.get_children()
            for item in x: self.alias_tree.delete(item)
            
            # Determine synonyms and translations of lh_object name in various languages        
            languages, alias_table = self.Determine_aliases(lh_object)
            for language in languages:
                self.alias_tree.insert('', index='end',
                                       values=language,
                                       iid=language,
                                       text=language, open=True)
            for alias_row in alias_table:
                self.alias_tree.insert(alias_row[0], index='end',
                                       values=alias_row[1:],
                                       #iid=alias_row[1],
                                       text=alias_row[1], open=True)
                
    def Determine_aspect_and_value_options(self, lh_obj_sub):
        ''' Determine in a search the characteristics of lh_object and its subtypes
            and determine the available values for those characteristics.
            These are options for conditions that reduce the selection in a query.
        '''
        equality = '='
        for rel_obj in lh_obj_sub.relations:
            expr = rel_obj.expression
            if expr[rel_type_uid_col] in self.gel_net.subConcPossAspUIDs \
               and not expr[rel_type_uid_col] in self.gel_net.conc_playing_uids:
                # An aspect is found
                asp_opt = [expr[rh_uid_col], expr[rh_name_col], '', '', '', '', '']
                role_uid = expr[rh_role_uid_col]
                if asp_opt not in self.q_aspects:
                    self.q_aspects.append(asp_opt)
                    #print('Aspect:', asp_opt)
                    
                # Determine the value(s) for a found kind of aspect
                # Therefore, find a rh_role object (intrinsic aspect)
                # of a <can have as aspect a> relation or its subtypes.
                if role_uid != '':
                    role = self.gel_net.uid_dict[role_uid]
                    
                    # Find criterion, constraints or value for intrinsic aspect, if any.
                    for rel_obj2 in role.relations:
                        expr2 = rel_obj2.expression
                        values = []
                        # Find compliancy criterion or constraint (4951)
                        # Find conceptual quantification (1791) value (on a scale)
                        # Find conceptual compliance criterion/qualif (4902)
                        # or def qualification
                        if role_uid == expr2[lh_uid_col] \
                             and (expr2[lh_role_uid_col] in self.gel_net.concComplUIDs \
                                  or expr2[rel_type_uid_col] in self.gel_net.concQuantUIDs \
                                  or expr2[rel_type_uid_col] in self.gel_net.subConcComplRelUIDs):
                            values = [expr2[rh_uid_col], '', expr2[rel_type_uid_col], \
                                      expr[rh_uid_col], expr[rh_name_col], \
                                      equality, expr2[rh_name_col], expr2[uom_name_col]]
                        # Find compliancy criterion or constraint (inverse)
                        # Find conceptual quantification (1791) value (inverse)
                        # Find conceptual compliance criterion (inverse)
                        elif role_uid == expr2[rh_uid_col] \
                             and (expr2[rh_role_uid_col] in self.gel_net.concComplUIDs \
                                  or expr2[rel_type_uid_col] in self.gel_net.concQuantUIDs \
                                  or expr2[rel_type_uid_col] in self.gel_net.subConcComplRelUIDs):
                            values = [expr2[lh_uid_col], '', expr2[rel_type_uid_col], \
                                      expr[rh_uid_col], expr[rh_name_col], \
                                      equality, expr2[lh_name_col], expr2[uom_name_col]]
                        if len(values) > 0:
                            if values not in self.q_aspects:
                                self.q_aspects.append(values)
                                #print('Values:', values)

    def Determine_rel_types_for_lh_object(self, lh_object):
        ''' With given selected lh_object determine which kinds of relations are known
            and store results in self.lh_obj_relation_types
        '''
        self.lh_obj_relation_types = []
        for lh_obj_rel in lh_object.relations:
                expr = lh_obj_rel.expression
                rel_type = self.gel_net.uid_dict[expr[rel_type_uid_col]]
                if rel_type == None:
                    self.user_interface.Message_UI(
                        'The kind of relation {} is not found.'.format(rel_type_uid),\
                        'De soort relatie {} is niet gevonden.'.format(rel_type_uid))
                else:
                    if rel_type not in self.lh_obj_relation_types:
                        self.lh_obj_relation_types.append(rel_type)
                        
                        # Determine_subtypes of the relation type
                        sub_rel_types, sub_rel_type_uids = self.gel_net.Determine_subtypes(rel_type)
                        for sub_rel_type in sub_rel_types:
                            if sub_rel_type not in self.lh_obj_relation_types:
                                self.lh_obj_relation_types.append(sub_rel_type)

    def Determine_aliases(self, obj):
        ''' Collect the names and translation that are known for obj
            in the alias_table for display in alias_tree treeview.
            name_in_context = (lang_uid, comm_uid, name, naming_uid, description)
            alias_row = (language, term, alias_type)
        '''
        alias_table = []
        languages = []
        for name_in_context in obj.names_in_contexts:
            alias_type = self.gel_net.uid_dict[name_in_context[3]]
            # Determine preferred name of alias_type
            lang_name, comm_name, alias_name, full_def = \
                       self.user_interface.Determine_name_in_context(\
                           alias_type, base_or_inverse = 'base')

            language = self.gel_net.lang_uid_dict[name_in_context[0]]
            if language not in languages:
                languages.append(language)

            alias_row = (language, name_in_context[2], alias_name)
            if alias_row not in alias_table:
                alias_table.append(alias_row)
        return languages, alias_table

    def Set_selected_q_rel_term(self, ind):
        """ Put the selected relObject name and uid from relOptions
            in query (self.q_rel_name_str and self.q_rel_uid_str).
            Then determine the rh_objects
            that are related to the lh_object by such a relation or its subtypes
        """
        item   = self.rel_options_tree.selection()
        ind    = self.rel_options_tree.index(item)
        self.query.relSel = self.rel_options[ind]
        # Determine UID and Name of selected option
        self.query.q_rel_uid  = self.query.relSel[5]
        self.query.q_rel_name = self.query.relSel[4]
        self.q_rel_uid_str.set(str(self.query.q_rel_uid))
        self.q_rel_name_str.set(self.query.q_rel_name)
        if self.query.q_rel_name in self.gel_net.total_base_phrases:
            self.query.q_phrase_type_uid = '6066'

        # Determine the rh_objects in the query
        # that are related by selected rel_object type or its subtypes
        # to the lh_object or its subtypes in the query
        int_q_lh_uid, integer = Convert_numeric_to_integer(self.query.q_lh_uid)
        if integer is False or int_q_lh_uid >= 100:
            rh_options = []
            # Determine list of subtypes of the rel_object
            q_rel_object = self.gel_net.uid_dict[self.query.q_rel_uid]
            q_rel_sub_types, q_rel_sub_type_uids = self.gel_net.Determine_subtypes(q_rel_object)
            q_rel_sub_types.append(q_rel_object)
            # Determine list of subtypes of the lh_object
            q_lh_obj = self.gel_net.uid_dict[self.query.q_lh_uid]
            q_lh_sub_types, q_lh_sub_type_uids = self.gel_net.Determine_subtypes(q_lh_obj)
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
                            # If the base relation corresponds the collect the rh name,
                            # if not yet present
                            if expr[lh_uid_col] == lh_sub.uid:
                                if expr[rh_name_col] not in rh_options:
                                    rh_options.append(expr[rh_name_col])
                            # If the inverse corresponds
                            elif expr[rh_uid_col] == lh_sub.uid:
                                if expr[lh_name_col] not in rh_options:
                                    rh_options.append(expr[lh_name_col])
                            #print('lh_name, rh_name', expr[lh_name_col], expr[rh_name_col])
            rh_options.sort()
            self.gel_net.rh_terms = rh_options
            self.q_rh_name_widget.config(values=self.gel_net.rh_terms)

    #--------------------------------------------------------------------------------
    def Set_selected_q_rh_term(self, ind):
        """Put the selection of rhObject in self.q_rh_name_str and self.q_rh_uid_str"""
        
        item  = self.rh_options_tree.selection()
        ind   = self.rh_options_tree.index(item)
        self.query.rhSel = self.rh_options[ind]
        # Determine UID and Name of selected option
        self.query.q_rh_uid  = self.query.rhSel[5]
        self.query.q_rh_name = self.query.rhSel[4]
        self.q_rh_uid_str.set(str(self.query.q_rh_uid))
        self.q_rh_name_str.set(self.query.q_rh_name)

    def Formulate_query_spec(self):
        """Formulte a query_spec on the network for the relation type and its subtypes.
           Store resulting query expressions in candids table with the same table definition.
        """
        # Make query_spec empty
        self.query.query_spec[:] = []
        self.query.ex_candids[:] = []
        
        # LH: Get selected option (textString)
        # from the presented list of options (lh_options_tree) in QueryWindow
        lh_uid_init = self.q_lh_uid_widget.get()
        if lh_uid_init == '':
            #print('Warning: Left hand option not yet selected. Please try again.')
            self.user_interface.Message_UI(
                'Left hand option is not yet selected. Please try again.',
                'Linker optie is nog niet geselecteerd. Probeer nogmaals.')
            return
        item = self.lh_options_tree.selection()
        ind = self.lh_options_tree.index(item)
        # => lh_options: optionNr, whetherKnown, langUIDres, commUIDres, result_string,\
        #                resultUID, is_called_uid, kindKnown, kind
        if len(self.lh_options) == 0:
            self.user_interface.Message_UI(
                'No option is selected. Please try again.',
                'Er is geen optie geselecteerd. Probeer nogmaals.')
            return
        self.query.lhSel = self.lh_options[ind]
        #print('Selected option:',item, ind, self.query.lhSel)

        # Determine UID and Name of selected lh option
        # and formulate query expression (query_expr)
        self.query.q_lh_uid = self.query.lhSel[5]
        self.query.q_lh_name = self.query.lhSel[4]
        self.q_lh_uid_str.set(str(self.query.q_lh_uid))
        self.q_lh_name_str.set(self.query.q_lh_name)
        self.query.query_expr = [self.query.q_lh_uid, self.query.q_lh_name]

        # Delete earlier definition text in query_window.
        self.q_full_def_widget.delete('1.0', END)
        
        # If lh_object is known then determine and display its full definition
        int_q_lh_uid, integer = Convert_numeric_to_integer(self.query.q_lh_uid)
        if integer is False or int_q_lh_uid >= 100:
            self.query.q_lh_obj = self.gel_net.uid_dict[self.query.q_lh_uid]
            self.query.q_lh_category = self.lh_options[0][8]

            # Determine the full definition of the selected object in the preferred language
            lang_name, comm_name, preferred_name, full_def = \
                       self.user_interface.Determine_name_in_context(self.query.q_lh_obj)
            #print('Full def:', self.query.q_lh_uid, lhString, self.query.q_lh_category, full_def)
            # Display full definition
            self.q_full_def_widget.insert('1.0',full_def)
            
        # Rel: Selected relation type option
        # Verify whether kind of relation is specified or only lh option is selected.
        #   If yes then formulate query, else determine rel and rh part of query expression 
        rel_uid_init = self.q_rel_uid_widget.get()
        if rel_uid_init != '':
            # There is a kind of relation specified. Identify its uid and name
            item = self.rel_options_tree.selection()
            ind = self.rel_options_tree.index(item)
            print('rel_ind', ind, self.rel_options)
            self.query.relSel = self.rel_options[ind]
            
            self.query.q_rel_uid = self.query.relSel[5]
            self.query.q_rel_name = self.query.relSel[4]
            self.q_rel_uid_str.set(str(self.query.q_rel_uid))
            self.q_rel_name_str.set(self.query.q_rel_name)

            int_q_rel_uid, integer = Convert_numeric_to_integer(self.query.q_rel_uid)
            if integer is False or int_q_rel_uid >= 100:
                self.query.q_rel_obj = self.gel_net.uid_dict[self.query.q_rel_uid]
            
                # Determine phraseTypeUID of self.query.q_rel_name
                self.query.q_phrase_type_uid = 0
                if self.query.q_rel_name in self.gel_net.total_base_phrases:
                    self.query.q_phrase_type_uid = '6066'   # base phrase
                else:
                    self.query.q_phrase_type_uid = '1986'   # inverse phrase
                
                # Determine role_players_types because of q_rel_type
                self.query.rolePlayersQTypes = self.query.q_rel_obj.role_players_types
                self.query.rolePlayerQTypeLH = self.query.q_rel_obj.role_player_type_lh
                self.query.rolePlayerQTypeRH = self.query.q_rel_obj.role_player_type_rh
                # 6068 = binary relation between an individual thing and any (kind or individual)
                if self.query.rolePlayersQTypes == 'individualsOrMixed':  # is related to (a)
                    if self.query.q_rel_name in self.gel_net.total_base_phrases:
                        self.query.rolePlayersQTypes = 'individualAndMixed'
                        self.query.rolePlayerQTypeLH = 'individual'
                        self.query.rolePlayerQTypeRH = 'mixed'
                    else:
                        self.query.rolePlayersQTypes = 'mixedAndIndividual'
                        self.query.rolePlayerQTypeLH = 'mixed'
                        self.query.rolePlayerQTypeRH = 'individual'
                # Binary relation between an individual thing and a kind
                elif self.query.rolePlayersQTypes == 'mixed':
                    if self.query.q_rel_name in self.gel_net.total_base_phrases:
                        self.query.rolePlayersQTypes = 'individualAndKind'
                        self.query.rolePlayerQTypeLH = 'individual'
                        self.query.rolePlayerQTypeRH = 'kind'
                    else:
                        self.query.rolePlayersQTypes = 'kindAndIndividual'
                        self.query.rolePlayerQTypeLH = 'kind'
                        self.query.rolePlayerQTypeRH = 'individual'
                # 7071 = binary relation between a kind and any (kind or individual)
                elif self.query.rolePlayersQTypes == 'kindsOrMixed':  # can be related to (a)
                    if self.query.q_rel_name in self.gel_net.total_base_phrases:
                        self.query.rolePlayersQTypes = 'kindsAndMixed' # can be related to (a)
                        self.query.rolePlayerQTypeLH = 'kind'
                        self.query.rolePlayerQTypeRH = 'mixed'
                    else:
                        self.query.rolePlayersQTypes = 'mixedAndKind' # is or can be related to a
                        self.query.rolePlayerQTypeLH = 'mixed'
                        self.query.rolePlayerQTypeRH = 'kind'
                else:
                    pass

            # RH: Selected right hand option
            # Verify whether a rh name is specified
            rh_uid_init = self.q_rh_uid_widget.get()
            if rh_uid_init == '':
                print('Right hand option is not (yet) selected.')
                self.user_interface.Message_UI(
                    'Right hand option ís not (yet) selected.',
                    'Rechter optie is nog niet geselecteerd.')
            else:
                # There is a rh name specified. Determine its name and uid and identity
                item = self.rh_options_tree.selection()
                ind = self.rh_options_tree.index(item)
                self.query.rhSel = self.rh_options[ind]
                
                self.query.q_rh_uid = self.query.rhSel[5]
                self.query.q_rh_name = self.query.rhSel[4]
                self.q_rh_uid_str.set(str(self.query.q_rh_uid))
                self.q_rh_name_str.set(self.query.q_rh_name)

                int_q_rh_uid, integer = Convert_numeric_to_integer(self.query.q_rh_uid)
                if integer is False or int_q_rh_uid >= 100:
                    self.query.q_rh_obj = self.gel_net.uid_dict[self.query.q_rh_uid]
                    
                # Report final query
                queryText = ['Query ','Vraag   ']
                self.views.log_messages.insert('end','\n\n{}: {} ({}) {} ({}) {} ({})'.\
                    format(queryText[self.GUI_lang_index], \
                           self.query.q_lh_name, self.query.q_lh_uid,\
                           self.query.q_rel_name, self.query.q_rel_uid,\
                           self.query.q_rh_name, self.query.q_rh_uid))
                self.query.query_expr = [self.query.q_lh_uid, self.query.q_lh_name, \
                                         self.query.q_rel_uid, self.query.q_rel_name,\
                                         self.query.q_rh_uid, self.query.q_rh_name, \
                                         self.query.q_phrase_type_uid]
##        else:
##            # Option for relation type is blank
##            self.user_interface.Message_UI(
##              'Relation type option is not (yet) selected.',\
##              'Optie voor soort relatie is (noch) niet geselecteerd.')
                
        # Append query expression as first line in query_spec
        # query_expr = lh_uid, lh_name, rel_uid, rel_name, rh_uid_rh_name, phrase_type_uid
        self.query.query_spec.append(self.query.query_expr)

        # Formulate coditions as are specified in the GUI 
        self.query.Formulate_conditions_from_gui()

        # Prepare query for execution and execute query
        self.query.Interpret_query_spec()
        # Display query results in notebook sheets
        self.views.Display_notebook_views()

    def Close_query(self):
        self.QWindow.destroy()
        
#------------------------------------------------------
class User_interface():
    def __init__(self):
        self.root = Tk()
        
if __name__ == "__main__":
    
    main = Main()
    user_interface = User_interface()
    gel_net = Semantic_network()
    main_view = Query_views(gel_net, user_interface)
    
    root.mainloop()
