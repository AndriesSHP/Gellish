import os
from tkinter import *
from tkinter.ttk import *
##from tkinter import messagebox, filedialog
from SemanticNetwork import Semantic_Network

class Main_view():
    def __init__(self, main):
        self.root = main.root
        self.main = main
        self.user = main.user
        self.GUI_lang_names = ['English','Nederlands']
        self.root.title("Gellish Communicator")
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

        self.lang_index = self.main.gel_net.GUI_lang_index

        # Open main window
        self.Main_window()

        event = 'Button-1'
        self.Determine_GUI_language(event)

#--------------------------------------------------
    def Main_window(self):
        """ Define a MainWindow with select options.
        """

        lprefs = False      # Language preferences are not set yet.
        cprefs = False      # Language community preferences are not set yet.
    #
    # Menu bar
        self.menubar = Menu(self.root,bg='#fbf')
        self.root['menu'] = self.menubar
    #
        verify  = ['Read file'  , 'Lees file']
        search  = ['Search'     , 'Zoek']
        query   = ['Query'      , 'Vraag']
##        edit    = ['Modify'     , 'Wijzig']
        stop    = ['Stop'       , 'Stop']
        admin   = ['DB Admin'   , 'DB Admin']
        new_net = ['New network', 'Nieuw netwerk']
        save_as = ['Save net'   , 'Opslaan']
        load_net= ['Load net'   , 'Import']
        read_db = ['Net from db', 'Net van db']

        self.menubar.add_command(label=verify[self.lang_index], command=self.main.read_file)
        self.menubar.add_command(label=search[self.lang_index], command=self.main.search_net)
        self.menubar.add_command(label=query [self.lang_index], command=self.main.query_net)
##        self.menubar.add_command(label=edit  [self.lang_index], command=self.main.Modify_db)
        self.menubar.add_command(label=stop  [self.lang_index], command=self.main.stop_quit)

        self.DBMenu = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.DBMenu, label=admin[self.lang_index])
        self.DBMenu.add_command (label=new_net [self.lang_index], command=self.main.create_net)
        self.DBMenu.add_command (label=save_as [self.lang_index], command=self.main.dump_net)
        #self.DBMenu.add_command (label=load_net[self.lang_index], command=self.main.load_net)
        #self.DBMenu.add_command (label=read_db [self.lang_index], command=self.main.read_db)

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
        # Set default language: GUI_lang_names[0] = English, [1] = Nederlands
        self.lang_default = StringVar(value=self.GUI_lang_names[0])
        self.lang_box     = ttk.Combobox(self.main_frame, textvariable=self.lang_default,\
                                         values=self.GUI_lang_names, width=10)
        self.lang_label.grid(column=0, row=0, sticky=NW)
        self.lang_box.grid  (column=1, row=0, sticky=NW)

        # Binding GUI language choice
        self.lang_box.bind  ("<<ComboboxSelected>>",self.Determine_GUI_language)

    def Determine_GUI_language(self, event):
        GUI_lang_name  = self.lang_box.get()
        self.main.gel_net.Set_GUI_language(GUI_lang_name)

        chosen_language = ['The user interface language is', 'De GUI taal is']
        print('{} {}'.format(chosen_language[self.main.gel_net.GUI_lang_index], self.main.gel_net.GUI_lang_name))

#------------------------------------------------
from tkinter import *
from tkinter.ttk import *

class Semantic_network():
    def __init__(self):
        self.GUI_lang_index = 0
        self.GUI_lang_name = 'English'
        pass

    def Set_GUI_language(self, GUI_lang_name):
        self.GUI_lang_index = 0

class Main():
    def __init__(self):
        self.root = Tk()
        self.user = 'Andries'
        self.gel_net = Semantic_network()

    def read_file(self):
        print('Read file')

    def query_net(self):
        print('Query network')

    def extended_query_net(self):
        print('Extended query network')

    def stop_quit(self):
        print('Stop')

    def create_net(self):
        print('Create network')

    def dump_net(self):
        print('Dump network')

class User():
    def __init__(self):
        pass

if __name__ == "__main__":
    #root = Tk()
    main = Main()
    user = User()
    gel_net = Semantic_network()
    view = Main_view(main)

    view.Main_window()
    mainloop()
