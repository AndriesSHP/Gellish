#Column name   Col_index, type, ID      Obligatory IDs: [2, 1, 60, 15]
#IDs of UIDs: [69, 71, 5, 2, 72, 19, 1, 60, 85, 74, 15, 66, 76, 70, 67, 11, 6, 78, 53, 50]
pres_seq_col         = 0 #text,   0     
lang_uid_col         = 1 #integer,69      UID of the language of a left hand object name
lang_name_col        = 2 #text,   54      Name of the language of a left hand object name
comm_uid_col         = 3 #integer,71      UID of the language community of a left hand object name
comm_name_col        = 4 #text,   16      Name of the language community of a left hand object name
reality_col          = 5 #text,   39      
intent_uid_col       = 6 #integer,5       UID of an intention with which the expression of an idea is communicated
intent_name_col      = 7 #text,   43      Description of an intention
lh_card_col          = 8 #text,   44      Left hand simultaneous cardinalities
lh_uid_col           = 9 #integer, 2      UID of a left hand object
lh_name_col          = 10 #text,   101    Name of a left hand object
lh_role_uid_col      = 11 #integer,72
lh_role_name_col     = 12 #text,   73
valCont_uid_col      = 13 #integer,19     UID of a validity context
valCont_name_col     = 14 #text,   18     Name of a validity context
idea_uid_col         = 15 #integer primary key, 1 UID of an idea
idea_desc_col        = 16 #text,   42     Description of an idea
rel_type_uid_col     = 17 #integer,60     UID of a kind of relation
rel_type_name_col    = 18 #text,   3      Name of a kind of relation (relation type)
phrase_type_uid_col  = 19 #integer,85     UID of a phrase type: base phrase = 6066, inverse phrase = 1986.
rh_role_uid_col      = 20 #integer,74
rh_role_name_col     = 21 #text,   75
rh_card_col          = 22 #text,   45     Right hand simultaneous cardinalities
rh_uid_col           = 23 #text,   15     UID of a right hand object
rh_name_col          = 24 #text,   201    Name of a right hand object
# not yet: exponent UID and name (34,35)
part_def_col         = 25 #text,   65     Partial definition (excluding supertype)
full_def_col         = 26 #text,   4      Full definition
# not yet: extent and probability UID and name (30,31,32,33)
uom_uid_col          = 27 #integer,66     UID of a unit of measure
uom_name_col         = 28 #text,   7      Name of a unit of measure (type of scale)
acc_uid_col          = 29 #integer,76
acc_name_col         = 30 #text,   77
pick_list_uid_col    = 31 #integer,70   
pick_list_name_col   = 32 #text,   20
remarks_col          = 33 #text,   14     Remarks on the expression
status_col           = 34 #text,   8      Status of the expression
reason_col           = 35 #text,   24     
succ_uid_col         = 36 #integer,67     Successor UID of an idea UID
date_start_app_col   = 37 #text,   9      Date of begin of existence of idea
date_start_avail_col = 38 #text,   23
date_crea_copy_col   = 39 #text,   22
date_lat_ch_col      = 40 #text,   10     Date of latest change of expression
originator_uid_col   = 41 #integer,11
originator_name_col  = 42 #text,   83
auth_lat_ch_uid_col  = 43 #integer,6
auth_lat_ch_name_col = 44 #text,   12     Author of latest change of expression
addr_uid_col         = 45 #integer,78
addr_name_col        = 46 #text,   79
refs_col             = 47 #text,   13     References
expr_uid_col         = 48 #integer,53
coll_uid_col         = 49 #integer,50     UID of a collection of ideas
coll_name_col        = 50 #text,   68     Name of a collection of ideas
file_name_col        = 51 #text,   82
lh_string_comm_col   = 52 #text,   80
rh_string_comm_col   = 53 #text,   81
rel_string_comm_col  = 54 #text,   84
multiplier_col       = 55 #float,  40
offset_col           = 56 #float,  41

expr_col_ids= [ 0, 69, 54, 71, 16, 39,  5, 43, 44,  2,\
               101,72, 73, 19, 18,  1, 42, 60,  3, 85,\
               74, 75, 45, 15, 201,65,  4, 66,  7, 76,\
               77, 70, 20, 14,  8, 24, 67,  9, 23, 22,\
               10, 11, 83,  6, 12, 78, 79, 13, 53, 50,\
               68, 82, 80, 81, 84, 40, 41]
default_row = 57*[""]
##              ["",  0, "",  0, "", "",491285,"statement", "",  0,\
##               "",  0, "",  0, "",  0, "",  0, "",  0,\
##               0 , "", "",  0, "", "", "",  0, "",  0,\
##               "",  0, "", "", "", "",  0, "", "", "",\
##               "",  0, "",  0, "",  0, "", "",  0,  0,\
##               "", "", "", "", "", "", ""]
# list of integer column ids
##int_col_ids = []
##              [     1,      3,          6,            \
##                   11,     13,     15,     17,     19,\
##               20,                         27,     29,\
##                   31,                 36,\
##                   41,     43,     45,         48, 49]  

# Define 3rd header record for output file
header3 = [
    'PresSeq',      'LangUID',      'LangName',     'CommUID',       'CommName',     \
    'Reality',      'IntentUID',    'IntentName',   'LhCard',        'LhUID',        \
    'LhName',       'LhRoleUID',    'LhRoleName',   'ValidityUID',   'ValidityName', \
    'IdeaUID',      'IdeaDescr',    'RelUID',       'RelName',       'PhraseTypeUID',\
    'RhRoleUID',    'RhRoleName',   'RhCard',       'RhUID',         'RhName',       \
    'PartDef',      'FullDef',      'UomUID',       'UomName',       'AccuracyUID',  \
    'AccuracyName', 'PickListUID',  'PickListName', 'Remarks',       'Status',       \
    'Reason',       'SuccessorUID', 'DateStartVal', 'DateStartAvail','DateCreaCopy', \
    'DateLatCh',    'OrigUID',      'OrigName',     'AuthorUID',     'AuthorName',   \
    'AddresseeUID', 'AddresseeName','References',   'ExpressionUID', 'CollUID',      \
    'CollName',     'FileName',     'LhStringComm', 'RhStringComm',  'RelStringComm',\
    'Multiplier',   'Offset']
