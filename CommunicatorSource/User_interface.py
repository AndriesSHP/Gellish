import os
import webbrowser
from tkinter import *
from tkinter.ttk import *

from SemanticNetwork import Semantic_Network
from Query import Query
from QueryViews import Query_view
from Display_views import Display_views
from Create_output_file import Convert_numeric_to_integer

class User_interface():
    ''' The opening window of the Communicator program
        that presents options for execution.
        The options start queries that are executed
        and the resulting models are displayed in model views.
    '''

    def __init__(self, gel_net):
        #self.main = main
        self.gel_net = gel_net
        self.pickle_file_name = "Gellish_net_db"
        self.GUI_lang_name_dict = {"English":'910036', \
                                   "Nederlands":'910037'}
        #self.root = main.root
        self.root = Tk()
        self.GUI_lang_names = ['English', 'Nederlands']
        self.root.title("Gellish Communicator")
        max_width, max_height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry('1000x600')
        self.root.minsize(width=600, height=300)
        self.root.maxsize(width=max_width, height=max_height) #1000,height=600)
        self.root.myStyle = Style()
        self.root.myStyle.configure("TFrame", background="#dfd")
        self.root.configure(background="#ddf")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.option_add('*tearOff', False)

        self.extended_query = False
        self.obj_without_name_in_context = []

        # Set GUI language default = English: GUI_lang_names[0]
        self.Set_GUI_language(self.GUI_lang_names[0])

        self.reply_lang_name_dict = {'English':'910036', \
                                     'Nederlands':'910037', \
                                     'American':'911689', \
                                     'Chinese':'911876', \
                                     'Deutsch':'910038', \
                                     'Francais':'910039'}
        self.comm_pref_uids = ['492014', 'any'] # Default: 492014 = 'Gellish'

        # Define main window
        self.Main_window()

        event = 'Button-1'
        self.Determine_GUI_language(event)

        self.query = None
        #self.query_spec = []
        #self.ex_candids = []
        self.unknown = ['unknown', 'onbekend']
        self.unknown_quid = 0   # start UID for unknowns in queries

        # Create display views object and initialize notebook
        self.views = Display_views(gel_net, self)

        tk.mainloop()

    def Set_GUI_language(self, GUI_lang_name):
        ''' Set the GUI language (name, uid, index and lang_prefs) of the user.
            The preferences defines a list of language uids in a preference sequence.
        '''
        if GUI_lang_name in self.GUI_lang_name_dict:
            self.GUI_lang_name = GUI_lang_name
            self.GUI_lang_uid  = self.GUI_lang_name_dict[GUI_lang_name]
            if GUI_lang_name == 'Nederlands':
                self.GUI_lang_index = 1
            else:
                self.GUI_lang_index = 0
            GUI_set = True
            if self.GUI_lang_uid == '910036':
                # Set default GUI_preferences at international, English, American
                self.GUI_lang_pref_uids = ['589211', '910036', '911689']
            elif self.GUI_lang_uid == '910037':
                # Set default preferences at international, Dutch, English
                self.GUI_lang_pref_uids = ['589211', '910037', '910036']
            else:
                # Set default preferences at international, user_language, English
                self.GUI_lang_pref_uids = ['589211', self.GUI_lang_uid, '910036']
        else:
            self.Message(
                'The GUI language {} is unknown. Default = English.'.format(GUI_lang_name),\
                'De GUI taal {} is onbekend. Default = English.'.format(GUI_lang_name))
            GUI_set = False
        return GUI_set

    def Main_window(self):
        """ Define a MainWindow with select options.
        """

        # Menu bar
        self.menubar = Menu(self.root, bg='#fbf')
        self.root['menu'] = self.menubar

        login = ['Login/Register', 'Login/Registreer']
        verify = ['Read file', 'Lees file']
        search = ['Search', 'Zoek']
        query = ['Query', 'Vraag']
        admin = ['DB Admin', 'DB Admin']
        new_net = ['New network', 'Nieuw netwerk']
        save_as = ['Save net', 'Opslaan']
        manual = ['User manual', 'Handleiding']

        self.menubar.add_command(label=login[self.GUI_lang_index],
                                 command=self.login_reg)
        self.menubar.add_command(label=verify[self.GUI_lang_index],
                                 command=self.read_file)
        self.menubar.add_command(label=search[self.GUI_lang_index],
                                 command=self.search_net)
        self.menubar.add_command(label=query[self.GUI_lang_index],
                                 command=self.query_net)

        self.DBMenu = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.DBMenu,
                                 label=admin[self.GUI_lang_index])
        self.DBMenu.add_command(label=new_net[self.GUI_lang_index],
                                command=self.gel_net.reset_and_build_network)
        self.DBMenu.add_command(label=save_as[self.GUI_lang_index],
                                command=self.dump_net)

        self.menubar.add_command(label=manual[self.GUI_lang_index],
                                 command=self.user_manual)

    # Main Frame
        self.main_frame = Frame(self.root)
        self.main_frame.grid(column=0, row=0, sticky=NSEW)
        self.main_frame.columnconfigure(0,weight=0)
        self.main_frame.columnconfigure(1,weight=1)
        self.main_frame.rowconfigure(0,weight=0)
        self.main_frame.rowconfigure(1,weight=1)

        # Define header row with language selector
        lang_text = ['Language:', 'Taal:']
        self.lang_label = Label(self.main_frame,
                                text=lang_text[self.GUI_lang_index], width=10)
        # Set default language: GUI_lang_names[0] = English, [1] = Nederlands
        self.lang_default = StringVar(value=self.GUI_lang_names[0])
        self.lang_box = Combobox(self.main_frame, textvariable=self.lang_default,
                                 values=self.GUI_lang_names, width=10)
        self.lang_label.grid(column=0, row=0, sticky=NW)
        self.lang_box.grid(column=1, row=0, sticky=NW)

        # Binding GUI language choice
        self.lang_box.bind  ("<<ComboboxSelected>>",self.Determine_GUI_language)

    def Determine_GUI_language(self, event):
        ''' Determine which user interface language is spacified by the user. '''

        GUI_lang_name  = self.lang_box.get()
        self.Set_GUI_language(GUI_lang_name)

        chosen_language = ['The user interface language is', 'De GUI taal is']
        print('{} {}'.format(chosen_language[self.GUI_lang_index], \
                             self.GUI_lang_name))

    def Message(self, mess_text_EN, mess_text_NL):
        if self.GUI_lang_index == 1:
            print(mess_text_NL)
        else:
            print(mess_text_EN)

    def user_manual(self):
        ''' Open the user manual wiki. '''

        url = 'http://wiki.gellish.net/'
        # Open URL in a new tab, if a browser window is already open.
        webbrowser.open_new_tab(url)

    def login_reg(self):
        ''' Enable a user to log in after being recognized as registered
            or register a new user and enable to login after authentication.
        '''
        pass

    def read_file(self):
        ''' Verify file(s) means read one or more files, verify their content
            and extent the semantic network with its content.
        '''
        self.gel_net.read_verify_and_merge_files()

    def dump_net(self):
        ''' Dump semantic network as pickle binary file.'''
        self.gel_net.save_pickle_db(self.pickle_file_name)
        self.Message(
            "Network '{}' is saved in file {}.".\
            format(self.gel_net.name, self.pickle_file_name),
            "Netwerk '{}' is opgeslagen in file {}.".\
            format(self.gel_net.name, self.pickle_file_name))

    def search_net(self):
        ''' Initiate the execution of a simple query as a search for an object.'''
        self.extended_query = False
        self.query_the_network()

    def query_net(self):
        ''' Initiate the execution of a complex query
            with a spec as expression(s) that may include conditions.
        '''
        self.extended_query = True
        self.query_the_network()

    def query_the_network(self):
        ''' Query the semantic network '''
        if self.gel_net is None:
            print('First create a semantic network. Then query again.')
        else:
            # Create a query object
            self.query = Query(self.gel_net, self)

            # Enter and Interpret a query
##            if self.use_GUI:
            q_view = Query_view(self.gel_net, self)
            # Specify a query via GUI
            q_view.Query_window()
##            else:
##                # Specify a query via command line
##                self.query.Specify_query_via_command_line()
##
##                # Interpret and execute query
##                # Search for data about kinds or about individuals and display in various views
##                self.query.Interpret_query_spec()

    def Set_reply_language(self, reply_lang_name):
        ''' Set the reply language (name, uid, reply_lang_pref_uids)
            for display of the user views.
        '''
        if reply_lang_name in self.reply_lang_name_dict:
            self.reply_lang_name = reply_lang_name
            self.reply_lang_uid  = self.reply_lang_name_dict[reply_lang_name]
            if self.reply_lang_uid == '910036':
                # Set default preferences at international, English, American
                self.reply_lang_pref_uids = ['589211', '910036', '911689']
            elif self.reply_lang_uid == '910037':
                # Set default preferences at international, Dutch, English
                self.reply_lang_pref_uids = ['589211', '910037', '910036']
            else:
                # Set default preferences at international, user_language, English
                self.reply_lang_pref_uids = ['589211', self.reply_lang_uid, '910036']
        else:
            self.Message(
                'The reply language {} is unknown. Default = English is used.'.\
                format(reply_lang_name),\
                'De antwoordtaal {} is onbekend. Default = English wordt gebruikt.'.\
                format(reply_lang_name))
            self.reply_lang_name = 'English'
            self.reply_lang_uid  = '910037'

    def Determine_name_in_context(self, obj, base_or_inverse = 'normal'):
        ''' Given an object and preferred language sequence uids and community sequence uids,
            determine lang_name, comm_name, preferred obj_name for user interface.
            base_or_inverse denotes whether the preferred name should be found
            in the attribute list
            names_in_contexts, base_phrases_in_contexts or inverse_phrases_in_contexts
            name_in_context = (lang_uid, comm_uid, name, naming_uid, description)
        '''
        if base_or_inverse == 'base':
            names_in_contexts = obj.base_phrases_in_contexts
        elif base_or_inverse == 'inverse':
            names_in_contexts = obj.inverse_phrases_in_contexts
        else:
            names_in_contexts = obj.names_in_contexts

        obj_name = None
        if len(names_in_contexts) > 0:
            # For language_prefs and community preferences search for name
            for lang_uid in self.reply_lang_pref_uids:
                for comm_pref_uid in self.comm_pref_uids:
                    for name_in_context in names_in_contexts:
                        # Verify if language uid corresponds with required reply language uid
                        if name_in_context[0] == lang_uid \
                           and (name_in_context[1] == comm_pref_uid or comm_pref_uid == 'any'):
                            obj_name = name_in_context[2]
                            lang_name = self.gel_net.lang_uid_dict[name_in_context[0]]
                            comm_name = self.gel_net.community_dict[name_in_context[1]] # community uid
##                            # base and inverse phrases have no description (name_in_context[4])
##                            if len(name_in_context) < 5:
##                                part_def = ''
##                            else:
##                                part_def = name_in_context[4]
##                            name_known = True
                            break
                            #return lang_name, comm_name, obj_name, part_def
                    if obj_name:
                        break
                if obj_name:
                    break

            # Search for partial definition in specialization relation in pref_languages
            # thus in a name_in_context[3] where 'is called' (5117) is used
            if obj_name:
                part_def = None
                for lang_uid in self.reply_lang_pref_uids:
                    for name_in_context in obj.names_in_contexts:
                        if name_in_context[0] == lang_uid \
                           and name_in_context[3] == '5117':
                            part_def = name_in_context[4]
                            break
                    if part_def:
                        break
                if not part_def:
                    # No definition found,
                    # then search for def in any name in context in pref_languages
                    for lang_uid in self.reply_lang_pref_uids:
                       for name_in_context in obj.names_in_contexts:
                           if name_in_context[0] == lang_uid \
                              and name_in_context[4] != '':
                               part_def = name_in_context[4]
                               break
                       if part_def:
                           break
            else:
                # No name is available in the preferred language,
                # then use the first available name and its definition
                obj_name = names_in_contexts[0][2]
                lang_name = self.gel_net.lang_uid_dict[names_in_contexts[0][0]]
                comm_name = self.gel_net.community_dict[names_in_contexts[0][1]]
                if base_or_inverse == 'normal':
                    part_def = names_in_contexts[0][4]
                else:
                    part_def = ''
        # No names in contexts available for obj
        else:
            if obj not in self.obj_without_name_in_context:
                self.obj_without_name_in_context.append(obj)
                numeric_uid, integer = Convert_numeric_to_integer(obj.uid)
                if integer is False or numeric_uid not in range(1000000000, 3000000000):
                    self.Message(
                        'There is no name in context known for {}'.format(obj.name),\
                        'Er is geen naam in context bekend voor {}'.format(obj.name))
            obj_name = obj.name
            lang_name = self.unknown[self.GUI_lang_index]
            comm_name = self.unknown[self.GUI_lang_index]
            part_def = ''

        # Determine full_def by determining supertype name in the preferred language
        # and concatenate with part_def
        super_name = None
        if len(obj.supertypes) > 0 and len(obj.supertypes[0].names_in_contexts) > 0:
            for lang_uid in self.reply_lang_pref_uids:
                for name_in_context in obj.supertypes[0].names_in_contexts:
                    # Verify if language uid corresponds with required reply language uid
                    if name_in_context[0] == lang_uid \
                       and name_in_context[3] == '5117':
                        super_name = name_in_context[2]
                        break
                if super_name:
                    break
        if super_name:
            full_def = super_name + ' ' + part_def
        else:
            full_def = part_def

        return lang_name, comm_name, obj_name, full_def

    def stop_quit(self):
        ''' Terminate the program.'''
        sys.exit()

#------------------------------------------------
import tkinter as tk
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
        self.gel_net = Semantic_network()

    def build_network(self):
        print('Build network')

if __name__ == "__main__":
    #root = Tk()
    main = Main()
    user_interface = User_interface(main.gel_net)
