import os
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, filedialog
from operator import itemgetter
from Bootstrapping import ini_out_path
from Expr_Table_Def import *
#from SemanticNetwork import Semantic_Network
from QueryModule import Query
from Create_output_file import Create_gellish_expression, Convert_numeric_to_integer, Open_output_file
from Occurrences_diagrams import Occurrences_diagram

class Display_views():
    def __init__(self, main):
        self.gel_net = main.gel_net
        self.main = main
        self.root = main.root
        self.user = main.user
        self.query = main.query
        self.lang_index = self.gel_net.GUI_lang_index
        self.uid_dict = self.gel_net.uid_dict

        self.kind_model   = self.gel_net.kind_model
        self.prod_model   = self.gel_net.prod_model
        self.taxon_model  = self.gel_net.taxon_model
        self.summ_model   = self.gel_net.summ_model
        self.possibilities_model = self.gel_net.possibilities_model
        self.indiv_model  = self.gel_net.indiv_model
        self.query_table  = self.gel_net.query_table
        self.network_model  = self.gel_net.network_model
        self.occ_model    = self.gel_net.occ_model
        self.involv_table    = self.gel_net.involv_table
        #self.part_whole_occs = self.gel_net.part_whole_occs

        #self.summ_of_aspect_uids = self.gel_net.summ_of_aspect_uids
        self.taxon_column_names  = self.gel_net.taxon_column_names
        self.taxon_uom_names     = self.gel_net.taxon_uom_names
        self.summ_column_names   = self.gel_net.summ_column_names
        self.summ_uom_names      = self.gel_net.summ_uom_names
        self.possib_column_names = self.gel_net.possib_column_names
        self.possib_uom_names    = self.gel_net.possib_uom_names
        self.indiv_column_names  = self.gel_net.indiv_column_names
        self.indiv_uom_names     = self.gel_net.indiv_uom_names

        self.subs_head     = ['Subtypes'      , 'Subtypen']
        self.comp_head     = ['Part hierarchy', 'Compositie']
        self.occ_head      = ['Occurrences'   , 'Gebeurtenissen']
        #self.role_head    = ['Role'          , 'Rol']
        #self.involv_head  = ['Involved'      , 'Betrokkene']
        self.kind_head     = ['Kind'          , 'Soort']
        self.aspect_head   = ['Aspect'        , 'Aspect']
        self.part_occ_head = ['Part occurrence','Deelgebeurtenis']
        self.info_head     = ['Document'      , 'Document']
        self.name_head     = ['Name'          , 'Naam']
        self.parent_head   = ['Upper concept' , 'Hoger concept']
        self.comm_head     = ['Community'     , 'Taalgemeenschap']

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

    # Define and display Network view sheet = = = = = = = = = = = = =
        if len(self.query_table) > 0:
            self.Define_and_display_network()

    # Define and display Taxonomic view sheet for kinds of products = = = =
        if len(self.taxon_model) > 0:
            self.Define_and_display_taxonomy_of_kinds()

    # Define and display Possibilities_view sheet of kind = = = = = = = = = =
        if len(self.possibilities_model) > 0:
            self.Define_and_display_possibilities_of_kind()

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
        if len(self.occ_model) > 0:
            # Destroy earlier activity sheet
            try:
                self.act_frame.destroy()
            except AttributeError:
                pass
        
            self.Define_activity_sheet()

            # Display occ_model in Activity sheet view
            self.Display_occ_model_view()

     # Define and display Documents_view sheet = = = = = = = = = =
        if len(self.gel_net.info_model) > 0:
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

    def Define_and_display_network(self):
        # Destroy earlier network_frame
        try:
            self.network_frame.destroy()
        except AttributeError:
            pass
        
        self.Define_network_sheet()

        self.Display_network_view()

    def Define_network_sheet(self):
        ''' Define a network sheet for display of network_model (a list of network rows)
            for display in a tab of Notebook
        '''
        self.network_frame = Frame(self.views_noteb)
        self.network_frame.grid (column=0, row=0, sticky=NSEW, rowspan=2) #pack(fill=BOTH, expand=1)  
        self.network_frame.columnconfigure(0, weight=1)
        self.network_frame.rowconfigure(0,weight=0)
        self.network_frame.rowconfigure(1,weight=1)
        
        network_text = ['Network','Netwerk']
        self.views_noteb.add(self.network_frame, text=network_text[self.lang_index], sticky=NSEW)
        #self.views_noteb.insert("end", self.network_frame, sticky=NSEW)

        network_head = ['Network of objects and aspects',\
                        'Netwerk van objecten en aspecten']
        network_lbl  = Label(self.network_frame,text=network_head[self.lang_index])
        
        headings = ['UID','Name', 'Parent','Kind','Aspect1','Aspect2','Aspect3','Aspect4','Aspect5'  ,\
                                 'Aspect6','Aspect7','Aspect8','Aspect9','Aspect10']
        nr_of_cols = 4 # len(self.taxon_column_names)
        display_cols = headings[3:nr_of_cols]

        self.network_tree = Treeview(self.network_frame,columns=(headings[0:nr_of_cols]),\
                                  displaycolumns=display_cols, selectmode='browse', height=30)

        self.network_tree.heading('#0'        ,text='Object'   , anchor=W)
        self.network_tree.heading('UID'       ,text='UID'      , anchor=W)
        self.network_tree.heading('Name'      ,text=self.name_head[self.lang_index], anchor=W)
        self.network_tree.heading('Parent'    ,text=self.parent_head[self.lang_index], anchor=W)
        self.network_tree.heading('Kind'      ,text=self.kind_head[self.lang_index], anchor=W)
        
        self.network_tree.column ('#0'        ,minwidth=100    , width=200)
        self.network_tree.column ('Parent'    ,minwidth=20     , width=50)
        self.network_tree.column ('Kind'      ,minwidth=20     , width=50)
##        asp = 0
##        for column in self.taxon_column_names[4:]:
##            asp += 1
##            Asp_name = 'Aspect' + str(asp)
##            self.network_tree.heading(Asp_name   ,text=self.taxon_column_names[asp +3]  ,anchor=W)
##            self.network_tree.column (Asp_name   ,minwidth=20 ,width=50)

##        self.network_tree.columnconfigure(0,weight=1)
##        self.network_tree.rowconfigure   (0,weight=1)
        
        self.network_tree.tag_configure('colTag', option=None, background='#afa')
        self.network_tree.tag_configure('uomTag', option=None, background='#ccf')
        self.network_tree.tag_configure('sumTag', option=None, background='#cfc')

        network_scroll = Scrollbar(self.network_frame, orient=VERTICAL, command=self.network_tree.yview)
        network_lbl.grid       (column=0, row=0,sticky=EW)
        self.network_tree.grid (column=0, row=1,sticky=NSEW)
        network_scroll.grid    (column=0, row=1,sticky=NS+E)
        self.network_tree.config(yscrollcommand=network_scroll.set)

        self.network_tree.bind(sequence='<Double-1>', func=self.Object_detail_view)
        self.network_tree.bind(sequence='i'         , func=self.Object_detail_view)
        self.network_tree.bind(sequence='<Double-3>', func=self.Object_detail_view)

    def Display_network_view(self):
        # Display header row with units of measure
        #self.network_tree.insert('', index='end', values=self.taxon_uom_names, tags='uomTag')
        
        # Display self.network_model rows in self.network_tree
        parents = []
        for network_line in self.network_model:
            # Verify whether network_line[2], being the parent, is blank or in the list of parents
            if network_line[2] == '' or network_line[2] in parents:
                # Skip duplicates
                if self.network_tree.exists(network_line[1]):
                    continue
                else:
                    color_tag = 'sumTag'
                    term = network_line[1].partition(' ')
                    if term[0] in ['has', 'heeft', 'classifies', 'classificeert', \
                                   'is', 'can', 'kan', 'shall', 'moet']:
                        color_tag = 'colTag'
                    self.network_tree.insert(network_line[2],index='end',values=network_line,tags=color_tag,\
                                           iid=network_line[1],text=network_line[1], open=True)
                    parents.append(network_line[1])

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

        self.taxon_tree = Treeview(self.taxon_frame,columns=(headings[0:nr_of_cols]),\
                                  displaycolumns=display_cols, selectmode='browse', height=30)

        self.taxon_tree.heading('#0'        ,text='Object'   , anchor=W)
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

        self.summ_tree.heading('#0'        ,text='Object'   , anchor=W)     
        self.summ_tree.heading('UID'       ,text='UID'      , anchor=W)
        self.summ_tree.heading('Name'      ,text=self.name_head[self.lang_index], anchor=W)
        self.summ_tree.heading('Kind'      ,text=self.kind_head[self.lang_index], anchor=W)
        self.summ_tree.heading('Community' ,text=self.comm_head[self.lang_index], anchor=W)
        
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

    def Define_and_display_possibilities_of_kind(self):
        # Destroy earlier possib_frame
        try:
            self.possib_frame.destroy()
        except AttributeError:
            pass
        
        self.Define_possibilities_sheet()

        # Display possibilities_sheet
        # Display header row with units of measure
        self.possib_tree.insert('', index='end', values=self.possib_uom_names, tags='uomTag')
        # Display self.possibilities_model rows in self.possib_tree
        parents = []
        for possib_line in self.possibilities_model:
            if possib_line[2] == '' or possib_line[2] in parents:
                #print('Possib_line', possib_line)
                self.possib_tree.insert(possib_line[2], index='end', values=possib_line,\
                                        tags='sumTag' , iid=possib_line[1],\
                                        text=possib_line[1], open=True) # possib_line[2] is the whole
                parents.append(possib_line[1])

    def Define_possibilities_sheet(self):
        ''' Define a possibilities_sheet for display of possibilities_model (a list of possib_rows)
            for display in a tab of Notebook
        '''
        self.possib_frame = Frame(self.views_noteb)
        self.possib_frame.grid(column=0, row=0, sticky=NSEW, rowspan=2) #pack(fill=BOTH, expand=1)  
        self.possib_frame.columnconfigure(0, weight=1)
        self.possib_frame.rowconfigure(0, weight=0)
        self.possib_frame.rowconfigure(1, weight=1)
        
        possib_text = ['Possibilities','Mogelijkheden']
        self.views_noteb.add(self.possib_frame, text=possib_text[self.lang_index], sticky=NSEW)
        self.views_noteb.insert("end", self.possib_frame, sticky=NSEW)

        possib_head  = ['Possible aspects per object of a particular kind',\
                        'Mogelijke aspecten per object van een bepaalde soort']
        possib_label = Label(self.possib_frame,text=possib_head[self.lang_index])
        headings = ['UID','Name','Parent','Kind','Community','Aspect1','Aspect2','Aspect3','Aspect4',\
                    'Aspect5'   ,'Aspect6','Aspect7','Aspect8','Aspect9','Aspect10']
        nr_of_cols = len(self.possib_column_names)
        display_cols = headings[3:nr_of_cols]
##        self.possib_tree = Treeview(self.possib_frame,columns=('Community','Aspect1','Aspect2','Aspect3','Aspect4'  ,\
##                                                     'Aspect5'  ,'Aspect6','Aspect7','Aspect8','Aspect9','Aspect10'),\
##                                  displaycolumns='#all', selectmode='browse', height=30)
        self.possib_tree = Treeview(self.possib_frame, columns=(headings[0:nr_of_cols]),\
                                    displaycolumns=display_cols, selectmode='browse', height=30)

        self.possib_tree.heading('UID'       ,text='UID'      , anchor=W)
        self.possib_tree.heading('Name'      ,text=self.name_head[self.lang_index], anchor=W)
        self.possib_tree.heading('Parent'    ,text=self.parent_head[self.lang_index], anchor=W)
        self.possib_tree.heading('Kind'      ,text=self.kind_head[self.lang_index], anchor=W)
        self.possib_tree.heading('Community' ,text=self.comm_head[self.lang_index], anchor=W)
        
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
        self.Display_composition_view()
        
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

        self.indiv_tree.heading('#0'        ,text='Object'   , anchor=W)
        self.indiv_tree.heading('UID'       ,text='UID'      , anchor=W)
        self.indiv_tree.heading('Name'      ,text=self.name_head[self.lang_index], anchor=W)
        self.indiv_tree.heading('Parent'    ,text=self.parent_head[self.lang_index], anchor=W)
        self.indiv_tree.heading('Kind'      ,text=self.kind_head[self.lang_index], anchor=W)
        self.indiv_tree.heading('Community' ,text=self.comm_head[self.lang_index], anchor=W)
        
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

    def Display_composition_view(self):
        ''' Display rows in indiv_model (composition of individual object)
            in composition sheet view
        '''
        # Display header row with units of measure
        self.indiv_tree.insert('', index='end', values=self.indiv_uom_names, tags='uomTag')
        # Display self.indiv_model rows in self.indiv_tree
        indiv_parents = []
        for indiv_line in self.indiv_model:
            if indiv_line[2] == '' or indiv_line[2] in indiv_parents:
                self.indiv_tree.insert(indiv_line[2], index='end', \
                                       values=indiv_line,tags='sumTag',iid=indiv_line[1],\
                                       text=indiv_line[1], open=True)  # indiv_line[2] is the whole
                indiv_parents.append(indiv_line[1])

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

        exprScrollV = Scrollbar(self.expr_frame, orient=VERTICAL  , command=self.expr_tree.yview)
        exprScrollV.grid       (column=0, row=1, sticky=NS+E, rowspan=3)
        exprScrollH = Scrollbar(self.expr_frame, orient=HORIZONTAL, command=self.expr_tree.xview)
        exprScrollH.grid       (column=0, row=3, sticky=S+EW)
        expr_lbl.grid         (column=0, row=0, sticky=NSEW)
        self.expr_tree.grid   (column=0, row=1, sticky=NSEW, rowspan=3)
        details_button.grid   (column=1, row=0, sticky=N)
        save_CSV_button.grid  (column=1, row=1, sticky=N)
        save_JSON_button.grid (column=1, row=2, sticky=N)
        
        self.expr_tree.config(yscrollcommand=exprScrollV.set)
        self.expr_tree.config(xscrollcommand=exprScrollH.set)
        self.expr_tree.tag_configure('valTag'  ,background='#cfc')
        
        self.expr_tree.columnconfigure(0,weight=1)
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
                   'Query results about '+self.gel_net.object_in_focus.name,'','','','','']
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
        for expression in self.gel_net.query_table:
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
        Open_output_file(self.gel_net.query_table, subject_name, lang_name, serialization)

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
            head_line = []
            #if self.test: print('kindLine:',kindLine)
            # If line_type == 1 then prepare header line for level 0 object
            # Note: line_type == 2 is skipped in this view
            if kindLine[3] == 1:
                head_line = kindLine[0:4]
                head_line.append(kindLine[5])
                head_line.append('')
                head_line.append('')
                head_line.append(kindLine[9])
                nameInFocus = head_line[4]
                level0Part = self.kind_tree.insert('',index='end',values=head_line,tags='focusTag',open=True)
                previusPart = level0Part
            # In kind_tree view line_type 2 to 3 (indicated in kindLine[3]) are not displayed.
            elif kindLine[3] > 3:

                # Set value_tags at 'valTag' or 'headTag' for each field
                value_tags = 11*['valTag']
                # If the line is a header line, then set value_tag to 'headTag'
                if kindLine[4] in self.comp_head    or kindLine[4] in self.occ_head or \
                   kindLine[4] in self.info_head   or kindLine[8] in self.aspect_head or \
                   kindLine[5] in self.part_occ_head or kindLine[4] in self.subs_head:
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
                # If the line is a value line and there is a name of a part
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
        display_heads = heads[5:]
        self.prod_tree = Treeview(self.prod_frame,columns=(heads), displaycolumns=display_heads, \
                                  selectmode='browse', height=30, padding=2)
        self.prod_treeHead = [('','' ,'Kind' ,'Aspect','Kind of aspect',\
                               '>=<','Value' ,'UoM'    ,'Status'),\
                              ('','','Soort','Aspect','Soort aspect'  ,\
                               '>=<','Waarde','Eenheid','Status')]
        self.prod_tree.heading('#0' ,text='Object', anchor=W)
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
        
        self.prod_tree.column ('#0'      ,minwidth=40,width=100)
        #self.prod_tree.column ('inFocus' ,minwidth=10,width=10)
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
        further_part = ['Further part' ,'Verder deel']
        kind_of_part = ['Kind of part', 'Soort deel']
        possible_roles = False # No roles expected
        
        for prod_line_0 in self.prod_model:
            prod_line = prod_line_0[:]
            head = False
            head_line = []
            #print('Prod_line:',prod_line)
            # If line_type (prod_line[3]) == 1 then prepare header line from prod_line for level 0 object
            # Note: line_type == 2 and 3 are skipped in this view
            if prod_line[3] == 1:
                head_line = prod_line[0:4]
                head_line.append(prod_line[5])
                head_line.append('')
                head_line.append('')
                head_line.append(prod_line[9])
                nameInFocus = head_line[4]
                #print('Head_line:',head_line)
                level0Part = self.prod_tree.insert('', index='end', values=head_line,
                                                   text=nameInFocus, tags='focusTag', open=True)
                previusPart = level0Part
            # If line_type (prod_line[3]) == 4 then prepare header line from prod_line for level 0 object
            # Note: line_type == 1, 2 and 3 are skipped in this view
            if prod_line[3] == 4:
                #nameInFocus = prod_line[5]
                prod_name = prod_line[4]
                level0Part = self.prod_tree.insert('', index='end', values=prod_line,\
                                                   text=prod_name, tags='focusTag',open=True)
                previusPart = level0Part
                
            # In prod_tree view line_type 2 to 3 (indicated in prod_line[3]) are not displayed.
            elif prod_line[3] > 4:
                # Set value_tags at 'valTag' or 'headTag' for each field
                value_tags = 11*['valTag']
                    
                # If the line is a header line, then set value_tag to 'headTag'
                if prod_line[4] in self.comp_head    or prod_line[4] in self.occ_head or \
                   prod_line[4] in self.info_head   or prod_line[8] in self.aspect_head or \
                   prod_line[5] in self.part_occ_head or prod_line[4] in self.subs_head:
                    head = True
                    value_tags = 11*['headTag']
                    prod_name = prod_line[4]
                    # Determine whether roles may appear in prod_line[4] in lines following the header line
                    # to avoid that they are included in the indented hierarchy
                    if prod_line[4] in self.occ_head:
                        possible_roles = True
                    elif prod_line[5] in self.part_occ_head:
                        possible_roles = False
                    # Remove header texts 'Further part' and 'Kind of part'
                    if prod_line[6] in further_part:
                        prod_line[6] = ''
                    if prod_line[7] in kind_of_part:
                        continue #prod_line[7] = ''
                    
                # If the line is a value line (thus not a header line) and there is a name of a part
                # then remember the part as a previous part 
                elif prod_line[4] != '':
                    previusPart = level0Part
                    prod_name = prod_line[4]
                elif prod_line[5] != '':
                    previusPart = level1Part
                    prod_name = prod_line[5]
                elif prod_line[6] != '':
                    previusPart = level2Part
                    prod_name = prod_line[6]

                # Set tag background color depending on value
                # If value is missing then bachgroumd color is yellow
                if prod_line[9] == '' or prod_line[9] in unknownVal:
                    value_tags[9] = 'missing'
                else:
                    value_tags[9] = 'available'
                if prod_line[7] in unknownVal:
                    value_tags[7] = 'missing'

                if possible_roles == True and prod_line[4] == '':
                    prod_name = ''
##                elif possible_roles == False and prod_line[5] != '':
##                    prod_line[5] = ''
                    
                # Insert line
                #print('Values:', prod_line[1], type(prod_line[1]))
                id = self.prod_tree.insert(previusPart, index='end', values=prod_line,\
                                           text=prod_name, tags=value_tags, open=True)

                # If the line is a header line, then continue to next line
                if head == True:
                    continue
                # If the line is a value line and the there is a name of a part
                #   then remember the part as a previous part
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
                    if (column_nr == 1 and (field_value in self.comp_head or field_value in self.occ_head or\
                                            field_value in self.info_head)) or \
                       (column_nr == 2 and (field_value in self.part_occ_head)):
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
        headings = ['OccUID', 'OccName' , 'WholeOccName', 'InvolvUID', 'KindOccUID',
                    'OccName','PartName', 'Involved'    , 'Kind'     , 'Role']
        display_cols = headings[7:]
        self.act_tree = Treeview(self.act_frame, columns=(headings),\
                               displaycolumns=display_cols,
                               selectmode='browse',height=30)

        occText  = ['Occurrence'     ,'Gebeurtenis']
        partText = ['Part occurrence','Deelgebeurtenis']
        strText  = ['Involved object','Betrokken object']
        kindText = ['Kind'           ,'Soort']
        roleText = ['Role'           ,'Rol']
        self.act_tree.heading('#0'      ,text=occText[self.lang_index] ,anchor=W)
        self.act_tree.heading('OccName' ,text=occText[self.lang_index] ,anchor=W)
        self.act_tree.heading('PartName',text=partText[self.lang_index],anchor=W)
        self.act_tree.heading('Involved',text=strText[self.lang_index] ,anchor=W)
        self.act_tree.heading('Kind'    ,text=kindText[self.lang_index],anchor=W)
        self.act_tree.heading('Role'    ,text=roleText[self.lang_index],anchor=W)
        
        self.act_tree.column('#0'       ,minwidth=20,width=20)
        self.act_tree.column('OccName'  ,minwidth=20,width=120)
        self.act_tree.column('PartName' ,minwidth=20,width=80)
        self.act_tree.column('Involved' ,minwidth=20,width=80)
        self.act_tree.column('Kind'     ,minwidth=20,width=60)
        self.act_tree.column('Role'     ,minwidth=20,width=60)

        #actLbl.grid (column=0,row=0,sticky=EW)
        self.act_tree.grid(column=0,row=0,sticky=NSEW)

        self.act_tree.columnconfigure(0,weight=0)
        self.act_tree.columnconfigure(1,weight=1)
        self.act_tree.columnconfigure(2,weight=1)
        self.act_tree.columnconfigure(3,weight=1)
        self.act_tree.columnconfigure(4,weight=1)
        self.act_tree.columnconfigure(5,weight=1)
##        self.act_tree.columnconfigure(6,weight=1)
##        self.act_tree.columnconfigure(7,weight=1)
##        self.act_tree.columnconfigure(8,weight=1)
        self.act_tree.rowconfigure(0,weight=0)
        self.act_tree.rowconfigure(1,weight=1)

        self.act_tree.tag_configure('uomTag', option=None, background='#ccf')
        self.act_tree.tag_configure('actTag', option=None, background='#dfd')

        actScroll = Scrollbar(self.act_frame,orient=VERTICAL,command=self.act_tree.yview)
        actScroll.grid (column=0,row=0,sticky=NS+E)
        self.act_tree.config(yscrollcommand=actScroll.set)

    
    def Display_occ_model_view(self):
        ''' Display activities and occurrences in self.act_tree
            Followed by a display of IDEF0 diagram(s)
        '''
        
        self.act_tree.tag_configure('headTag', option=None, background='#dfd')
        if len(self.occ_model) > 0:
            self.top_occurrences = []
            for occ_line in self.occ_model:
                #print('==OccTree:',occ_line)
                # If higher part (occ_linen[2]) is blank then occ_line[0] contains top occ_UID
                if occ_line[2] == '':
                    top_occ = self.uid_dict[occ_line[0]]
                    self.top_occurrences.append(top_occ)
                level  = 0
                # Display self.act_tree line
                self.Display_occurrence_tree(occ_line, level) #,wholes

            # IDEF0: Display drawings of occurrences
            diagram = Occurrences_diagram(self.root, self.gel_net)
            diagram.Create_occurrences_diagram(self.top_occurrences)

    def Display_occurrence_tree(self, occ_line, level):
        """ Display occurrences compositions with inputs and outputs and roles.
            occ_line = line in occ_model
            occ_model.append([occ.uid, occ.name, higher.name, involv.uid, kind_occ.uid,\
                              occ.name, part_occ.name, involv.name, \
                              kind_part_occ.name, role_of_involved])
            involv_table: occ, involved, inv_role_kind, inv_kind_name
        """
        #print('Occ_line:', occ_line)
        
        self.act_tree.tag_configure('occTag', option=None, background='#ddf')
        self.act_tree.tag_configure('ioTag' , option=None, background='#eef')
        space = ''

        # Display the occurrence
        id = self.act_tree.insert(occ_line[2], index='end', values=(occ_line),
                                  iid=occ_line[1], text=occ_line[1], tags='occTag' , open=True)
            
        # Find and display its inputs and outputs
        # involv_table = occ, involved_obj, inv_role_kind, inv_kind_name
        for io_objects in self.involv_table:
            io_line = ['','','','','','','', io_objects[1].name, io_objects[3], io_objects[2].name]
            #print('involv_table-line:', occ_line[1], io_objects[0].uid, io_objects[1].uid, io_line)
            # If uid of occurrence == uid of object that has inputs or outputs then display io_line
            if occ_line[0] == io_objects[0].uid:
                self.act_tree.insert(id, index='end', values=(io_line), tags='ioTag' , open=True)
        level = 1
##        for whole_occ, part_occ, part_kind_occ in self.part_whole_occs:
##            # For each part of occurrence call Display_occurrence_tree recursively
##            # If uid of occurrence == uid whole then there is a part
##            if occ_line[0] == whole_part[0].uid:
##                print('part in part_whole_occs:', whole_occ.name, part_occ.name, part_kind_occ.name)
##                #self.act_tree.insert(id,index='end',values=(wholePart[3],wholePart[2]),tags='actTag')
##                self.Display_occurrence_tree(whole_part, level)

    def Define_and_display_documents(self):
        # Destroy earlier documents sheet
        try:
            self.doc_frame.destroy()
        except AttributeError:
            pass
    
        self.Define_documents_sheet()

        # Documents: Display documents and files for selection for display
        for info_line in self.gel_net.info_model:
            self.doc_tree.insert('',index='end',values=info_line,tags='docTag')

    def Define_documents_sheet(self):
        documents = ['Documents','Documenten']
        self.doc_frame = Frame(self.views_noteb)
        self.doc_frame.grid (column=0, row=0,sticky=NSEW) #pack(fill=BOTH, expand=1)  
        self.doc_frame.columnconfigure(0,weight=1)
        self.doc_frame.rowconfigure(0,weight=0)
        self.views_noteb.add(self.doc_frame, text=documents[self.lang_index], sticky=NSEW)
        self.views_noteb.insert("end",self.doc_frame,sticky=NSEW)
        headings = ['info','obj','carrier','directory','infoName','infoKind', 'dirName',\
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
        self.doc_tree.heading('dirName'  ,text='Directory'  ,anchor=W)
        self.doc_tree.heading('objName'  ,text='about Object' ,anchor=W)
        self.doc_tree.heading('fileName' ,text='File name' ,anchor=W)
        self.doc_tree.heading('fileKind' ,text='File type' ,anchor=W)
        
        self.doc_tree.column('#0'        ,minwidth=10,width=10)
        self.doc_tree.column('infoName'  ,minwidth=100,width=150)
        self.doc_tree.column('infoKind'  ,minwidth=100,width=150)
        self.doc_tree.column('dirName'   ,minwidth=100,width=150)
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
        self.doc_tree.bind(sequence='<Button-3>', func=self.Doc_detail_view)

#------------------------------------------------------------------------
    def Expr_detail_view(self, sel):
        """ Find the selected object from a user selection
            in the query_table that is displayed in the expr_tree view."""
        
        cur_item = self.expr_tree.focus()
        item_dict = self.expr_tree.item(cur_item)
        values = list(item_dict['values'])

        selected_object = self.gel_net.uid_dict[str(values[lh_uid_col])]
        print('Display product details of:', selected_object.name)
        if selected_object.category in ['kind', 'kind of physical object', \
                                        'kind of occurrence', 'kind of aspect', \
                                        'kind of role', 'kind of relation']:
            self.Define_and_display_kind_detail_view(selected_object)
        else:
            self.Define_and_display_individual_detail_view(selected_object)

#------------------------------------------------------------------------
    def Object_detail_view(self, sel):
        """ Find the selected left hand object from a user selection with left button
            in the network_model that is displayed in the network_tree view."""
        description_text = ['description', 'beschrijving']
        obj_descr_title  = ['Information about ', 'Informatie over ']
        
        cur_item = self.network_tree.focus()
        item_dict = self.network_tree.item(cur_item)
        values = list(item_dict['values'])
        #print('Network object_detail_view:', cur_item, values)
        if len(values) > 0:
            if sel.num == 1:
                chosen_object_uid = values[0]
            else:
                chosen_object_uid = values[4]
            if chosen_object_uid != '':
                selected_object   = self.gel_net.uid_dict[str(chosen_object_uid)]

                # If info_kind is a description then display the destription in messagebox
                if values[8] in description_text:
                    print('Information {} is not presented on a carrier but is as follows:\n   {}'.\
                          format(values[5], selected_object.description))
                    messagebox.showinfo(obj_descr_title[self.lang_index] + selected_object.name, \
                                        selected_object.description)
                else:
                    print('Display object details of: {}'.format(selected_object.name))
                    if selected_object.category in self.gel_net.categories_of_kinds:
                        self.Define_and_display_kind_detail_view(selected_object)
                    else:
                        self.Define_and_display_individual_detail_view(selected_object)
                
                if len(self.gel_net.info_model) > 0:
                    self.Define_and_display_documents()

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
        selected_object   = self.gel_net.uid_dict[str(values[0])]

        # If info_kind is a description then display the destription in messagebox
        if values[7] in description_text:
            print('Information {} is not presented on a carrier but is as follows:\n   {}'.\
                  format(values[4], selected_object.description))
            messagebox.showinfo(obj_descr_title[self.lang_index] + selected_object.name, \
                                selected_object.description)
        else:                                       
            print('Display kind details of: {}'.format(selected_object.name))
            self.Define_and_display_kind_detail_view(selected_object)
            if len(self.gel_net.info_model) > 0:
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
                selected_object   = self.gel_net.uid_dict[str(values[1])]
                
                # Save sel.type being either 'ButtonPress' or 'KeyPress' with sel.keysym = 'c'
                self.sel_type = sel.type
                
                print('Display taxonomy of: {}'.format(selected_object.name))
                obj_list = []
                obj_list.append(selected_object)
                self.gel_net.Build_product_views(obj_list)
                # Display taxonomy of selected kind
                self.Define_and_display_taxonomy_of_kinds()
                if len(self.gel_net.info_model) > 0:
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
        """ Find the selected left hand individual object from a user selection with left button
            in the prod_table that is displayed in the prod_tree view."""
        description_text = ['description', 'beschrijving']
        obj_descr_title  = ['Information about ', 'Informatie over ']
        cur_item = self.prod_tree.focus()
        item_dict = self.prod_tree.item(cur_item)
        values = list(item_dict['values'])
        print('Prod_detail_left:', cur_item, values)
        if len(values) > 0:
            if values[0] != '':
                selected_object   = self.gel_net.uid_dict[str(values[0])]

                # If info_kind is a description then display the destription in messagebox
                if values[7] in description_text:
                    print('Information {} is not presented on a carrier but is as follows:\n   {}'.\
                          format(values[4], selected_object.description))
                    messagebox.showinfo(obj_descr_title[self.lang_index] + selected_object.name, \
                                        selected_object.description)
                else:                                       
                    print('Display product details of: {}'.format(selected_object.name))
                    self.Define_and_display_individual_detail_view(selected_object)
                
                if len(self.gel_net.info_model) > 0:
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
                selected_object   = self.gel_net.uid_dict[str(values[1])]
                #print('sel.type', sel.type, sel.keysym, sel.char)
                # Verify sel.type being either 'ButtonPress' for display of taxonomy
                # or 'KeyPress' with sel.keysym = 'c' (for display for classification by selection of subtype)
                if sel.keysym == 'c':
                    self.modification = 'classification started'
                    self.gel_net.modified_object = self.gel_net.uid_dict[str(values[0])]
                    print('Present taxonomy of kind: {} that classifies {} for selection of a subtype'.\
                          format(selected_object.name, self.gel_net.modified_object.name))
                    
                    # Formulate query_spec including conditions from aspects of individual, if any
                    self.query.Formulate_query_spec_for_individual(selected_object)
                    self.query.Create_query_file()
                    self.query.Interpret_query_spec()
                else:
                    # Mouse ButtonPress: Build views for selected object (kind) and display views
                    print('Display taxonomy of kind: {}'.format(selected_object.name))
                obj_list = []
                obj_list.append(selected_object)
                self.gel_net.Build_product_views(obj_list)
                # Display taxonomy in taxon view
                self.Define_and_display_taxonomy_of_kinds()
                # Display possibilities of kind in possibilities view
                self.Define_and_display_possibilities_of_kind()

                if len(self.gel_net.info_model) > 0:
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
                if str(values[2]) == '':
                    print('There is no right hand object to be displayed')
                else:
                    print('Name of right hand object {} does not contain a file extension. It is interpreted as an aspect.'.\
                          format(values[8]))
                    selected_object = self.gel_net.uid_dict[str(values[2])]
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
        
        classifier = ['classifies', 'classificeert']
        cur_item = self.taxon_tree.focus()
        item_dict = self.taxon_tree.item(cur_item)
        #print('Detail view item:', item_dict['values'])
        values = list(item_dict['values'])
        #print('Taxon values, sel.', values)
        selected_object = self.gel_net.uid_dict[str(values[0])]

        if sel.num == 1:
            # If mousebutton-1 is used, then Create a detail view
            # Verify whether object is an individual thing due to being classified
            parts = str(values[2]).partition(' ')
            if parts[0] in classifier:
                print('Display details of individual:',values[0], selected_object.name)
                self.Define_and_display_individual_detail_view(selected_object)
            else:
                print('Display details of kind:',values[0], selected_object.name)
                self.Define_and_display_kind_detail_view(selected_object)
        elif self.modification == 'classification started':
            # if sel.type = 'KeyPress' with sel.keysym = 'c' then 
            # Append selected classifier to modified_object, and add classification relation
            self.gel_net.Add_classification_relation(self.gel_net.modified_object, selected_object)

            # Display modified product view
            self.modification = 'classification completed'
            self.Define_and_display_individual_detail_view(self.gel_net.modified_object)
            print('Classification of {} by classifier {} is added to the network'.\
                  format(self.gel_net.modified_object.name, selected_object.name))

#-------------------------------------------------------------------------        
    def Summ_detail_view(self, sel):
        """ Find the selected object from a user selection that is made
            in the summ_model that is displayed in the summ_tree view."""
        
        #item_dict = self.summ_tree.selection()
        cur_item = self.summ_tree.focus()
        item_dict = self.summ_tree.item(cur_item)
        #print('Detail view item:', item_dict['values'])
        values = list(item_dict['values'])
        
        selected_object = self.gel_net.uid_dict[str(values[0])]
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
        
        selected_object = self.gel_net.uid_dict[str(values[0])]
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
        
        selected_object = self.gel_net.uid_dict[str(values[0])]
        #print('Display product details of:',values[0], selected_object.name)
        # Create a detail view 
        self.Define_and_display_individual_detail_view(selected_object)

    def Define_and_display_kind_detail_view(self, selected_object):
        """ Create a detail view of a kind from a user selection
            and display the view in the kind_model view."""
        self.gel_net.kind_model[:]  = []
        self.gel_net.query_table[:] = []
        self.gel_net.Build_single_product_view(selected_object)

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
        self.gel_net.prod_model[:]  = []
        self.gel_net.query_table[:] = []
        self.gel_net.Build_single_product_view(selected_object)

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
        print('Doc_detail_view:', cur_item, info_row)

        # If right hand mouse button is pressed (sel.num == 3),
        # then determine and display a product view of the object about which the document provides info
        if sel.num == 3:
            if len(info_row) > 1:
                if info_row[1] != '':
                    selected_object   = self.gel_net.uid_dict[str(info_row[1])]
                    print('Display product details of: {}'.format(selected_object.name))
                    self.Define_and_display_kind_detail_view(selected_object)
                    
                    if len(self.gel_net.info_model) > 0:
                        self.Define_and_display_documents()
        else:
            # Left hand mouse button is pressed
            # If info_kind is a description then display the destription
            description_text  = ['description', 'beschrijving']
            description_title = ['Information about ', 'Informatie over ']
            if info_row[5] in description_text:
                #print('Information {} is not presented on a carrier but is as follows:\n   {}'.\
                #      format(info_row[4], info_row[2]))
                messagebox.showinfo(description_title[self.lang_index] + info_row[6], info_row[2])

            # Verify whether file name (info_row[7]) is presented on a file
            # And verify whether the file name has a file extension (indicated by a dot (.)) 
            parts = info_row[8].rsplit('.', maxsplit=1)
            if len(parts) == 1:
                print('== Error: File name {} does not have a file extension'.format(info_row[7]))
            else:
                # Open the file in the file format that is defined by its file extension
                print('Open file {} about {}'.format(info_row[8], info_row[7]))
                directory_name = info_row[3]
                if directory_name != '':
                    file_path = os.path.join(directory_name, info_row[8])
                    normalized_path = os.path.normpath(file_path)
                    os.startfile(normalized_path,'open')

    def Contextual_facts(self):
        print('Contextual_facts')
        
#------------------------------------------------
class Main():
    def __init__(self):
        pass
    def Read_file(self):
        print('Read_file')
        
    def Query_net(self):
        print('Query_net')
        
    def Stop_Quit(self):
        print('Stop_Quit')
        
    def Create_net(self):
        print('Create_net')
        
    def Dump_net(self):
        print('Dump_net')
        
##    def Load_net(self):
##        print('Load_net')
##        
##    def Read_db(self):
##        print('Read_db')

class User():
    def __init__(self):
        self.GUI_lang_name = 'Nederlands'
        self.GUI_lang_index = 1
        
    
if __name__ == "__main__":
    root = Tk()
    main = Main()
    main.gel_net = Semantic_network()
    views = Display_views(main)
    views.lang_index = 0
    views.lang_name = 'English'
    views.categoryInFocus = 'kind'
    
    views.Notebook_views()
    root.mainloop()
