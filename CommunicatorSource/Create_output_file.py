import os
import csv
import datetime
import json
from tkinter import filedialog
from Bootstrapping import ini_out_path
from Expr_Table_Def import *
from Expr_Table_Def import expr_col_ids, header3, default_row
from utils import open_file


def Create_gellish_expression(lang_comm, idea_uid, intent_uid_name, \
                              lh_uid_name, rel_uid_phrase_type,\
                              rh_role_uid_name, rh_uid_name, uom_uid_name, full_description):
    ''' Create a Gellish expression from default_row in Expr_Table_Def'''
    gellish_expr = default_row[:]
    gellish_expr[lang_uid_col]  = lang_comm[0]
    gellish_expr[lang_name_col] = lang_comm[1]
    gellish_expr[comm_uid_col]  = lang_comm[2]
    gellish_expr[comm_name_col] = lang_comm[3]
    gellish_expr[intent_uid_col]  = intent_uid_name[0]
    gellish_expr[intent_name_col] = intent_uid_name[1]
    gellish_expr[idea_uid_col]  = idea_uid
    gellish_expr[lh_uid_col]    = lh_uid_name[0]
    gellish_expr[lh_name_col]   = lh_uid_name[1]
    gellish_expr[rel_type_uid_col]    = rel_uid_phrase_type[0]
    gellish_expr[rel_type_name_col]   = rel_uid_phrase_type[1]
    gellish_expr[phrase_type_uid_col] = rel_uid_phrase_type[2]
    gellish_expr[rh_role_uid_col]     = rh_role_uid_name[0]
    gellish_expr[rh_role_name_col]    = rh_role_uid_name[1]
    gellish_expr[full_def_col] = full_description
    gellish_expr[rh_uid_col]   = rh_uid_name[0]
    gellish_expr[rh_name_col]  = rh_uid_name[1]
    gellish_expr[uom_uid_col]  = uom_uid_name[0]
    gellish_expr[uom_name_col] = uom_uid_name[1]
    gellish_expr[status_col]   = 'geaccepteerd'
    return gellish_expr

def Open_output_file(expressions, subject_name, lang_name, serialization):
    """ Open a file for saving expressions in some format
        such as the CSV in Gellish Expression Format:
        Serialization is either 'csv', 'xml', 'n3' or 'json'.
    """

    date = datetime.date.today()
    # Create header line 1 and an initial file name
    if lang_name == 'Nederlands':
        header1 = ['Gellish','Nederlands','Versie','9.0',date,'Resultaten',\
                   'over '+subject_name]  # ,'',46*(0,), 0]
        res = 'Resultaten-'
    else:
        header1 = ['Gellish','English','Version','9.0',date,'Results',\
                   'about '+subject_name]  # ,'',46*(0,), 0]
        res = 'Results-'
    if serialization == 'csv':
        ini_file_name = res + subject_name + '.csv.csv'
    if serialization == 'xml':
        ini_file_name = res + subject_name + '.xml.xml'
    if serialization == 'n3':
        ini_file_name = res + subject_name + '.n3.n3'
    if serialization == 'json':
        ini_file_name = res + subject_name + '.json.json'

    #header2 = expr_col_ids  # from Bootstrapping

    # Select file name and directory
    # Ini_out_path from Bootstrapping
    title = serialization + ' files'
    extension = '*.' + serialization
    output_file = filedialog.asksaveasfilename(filetypes  = ((title, extension),\
                                                           ("All files","*.*")),\
                                               title      = "Enter a file name",\
                                               initialdir = ini_out_path,\
                                               initialfile= ini_file_name) #,\
                                               # parent     = exprFrame)
    if output_file == '':
        output_file = 'Results.' + serialization
        if lang_name == 'Nederlands':
            print('***De filenaam voor opslaan is blanco of the file selectie is gecancelled. '
                  'De file is opgeslagen met de naam ' + output_file)
        else:
            print('***File name for saving is blank or file selection is cancelled. '
                  'The file is saved under name ' + output_file)
    Save_expressions_in_file(expressions, output_file, header1, serialization)
#---------------------------------------------------------
def Save_expressions_in_file(expressions, output_file, header1, serialization):
    '''Write expressions to an output file in an CSV or RDF serialization'''
    from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef, RDFS

    if serialization == 'csv':
        # Save the result_expr expressions in a CSV file, preceeded by three header lines.
        try:
            f = open(output_file, mode='w',newline='', encoding='utf-8')
            fileWriter = csv.writer(f, dialect='excel', delimiter=';')

            # Write header rows and expressions
            fileWriter.writerow(header1)
            fileWriter.writerow(expr_col_ids)
            fileWriter.writerow(header3)
            for expression in expressions:
                fileWriter.writerow(expression)

            f.close()

            open_file(output_file)     # Open written file in CSV viewer (e.g. Excel)
        except PermissionError:
            print('File {} cannot be opened. Probably already in use'.format(output_file))
            return

    elif serialization in ['xml', 'n3']:
        g1 = Graph()

        uri = "http://www.formalenglish.net/dictionary" #"
        gel = Namespace("http://www.formalenglish.net/dictionary") #")
        g1.bind('gel',"http://www.formalenglish.net/dictionary") #")

        #rdfs = {1146: 'subClassOf'}

        for expr in expressions:
            rel_name = str(expr[3]).replace(" ", "_")
            if expr[2] == 1146:
                rel = RDFS.subClassOf
            else:
                rel = URIRef(uri+rel_name)

        ##    lh = gel.lh_101
        ##    rh = gel.lh_102

            lh = URIRef(uri+str(expr[1]))
            rh = URIRef(uri+str(expr[5]))
            g1.add((lh, rel, rh))

        if serialization == 'n3':
            s = g1.serialize(format='n3')
            f = open(output_file, 'w')
            f.write(str(s))
        elif serialization == 'xml':
            s = g1.serialize(format='xml')
            f = open(output_file, 'w')
            f.write(str(s))
    else:
        f = open(output_file, 'w', encoding='utf-8')
        json.dump(expressions, f)

    f.close()
    print('Saved file: {}'.format(output_file))
    # Open written file in a viewer
    open_file(output_file)

def Convert_numeric_to_integer(numeric_text):
    ''' Convert a numeric string into integer value removing dots(.), commas (,) and spaces ( )
        If string is not numeric, return string and integer = False
    '''
    integer = True
    try:
        int_val = int(numeric_text)
    except ValueError:
        commas_removed = numeric_text.replace(',', '')
        dots_removed   = commas_removed.replace('.', '')
        spaces_removed = dots_removed.replace(' ', '')
        if spaces_removed.isdecimal():
            return int(spaces_removed), integer
        else:
            integer = False
            return numeric_text, integer
    return int_val, integer


def Message(GUI_lang_index, mess_text_EN, mess_text_NL):
    if GUI_lang_index == 1:
        print(mess_text_NL)
    else:
        print(mess_text_EN)
