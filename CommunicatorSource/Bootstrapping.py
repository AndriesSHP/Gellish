# -*- coding: utf-8 -*-

# Base ontology and domain dictionaries directories
dict_dirs = ["../GellishDictionary"]

# Base ontology file
base_onto_file_name = "Formal language definition base-UTF-8-subset.csv"

# Taxonomic Dictionary files
dict_file_names = [
##    "extended language definition-UTF-8.csv",\
    "units of measures & currencies-UTF-8-subset.csv",\
##    "units of measures - Special symbols-UTF-8.csv",\
    "aspects & properties & qualities & laws-UTF-8-subset.csv",\
##    "information & documents & rules & identification & symbols-UTF-8.csv",\
##    "qualitative aspects & qualitative information-UTF-8.csv",\
##    "activities & events & processes-UTF-8.csv",\
##    "buildings & civil & infrastructure & furniture-UTF-8.csv",\
##    "biology & biochemistry & agriculture-UTF-8.csv",\
##    "electrical & instrumentation & control & IT-UTF-8.csv",\
##    "facilities & static eq & process units & piping & protection & connection-UTF-8.csv",\
##    "Chinese - fasteners-UTF-8.csv",\
##    "geography & countries & businesses & persons & organizations-UTF-8.csv",\
##    "mathematics & shapes-UTF-8.csv",\
##    "roles of aspects-UTF-8.csv",\
##    "roles of physical objects-UTF-8.csv",\
##    "rotating equipment & transport & solids handling-UTF-8.csv",\
##    "substances & materials of construction, fluids and solids-UTF-8.csv",\
##    "colors - RAL codes and names - multilingual-UTF-8.csv",\
##    "RDF, RDFS, OWL concepts-UTF-8.csv",\
##    "EN 16323-2010 - Multi lingual Glossary of wastewater terms-UTF-8.csv"
    ]

# Knowledge, Requirements and Product type file paths
model_dirs  = ["../GellishData"]
model_file_names = [
    "Taxonomic Dictionary+Knowledge about Roads-UTF-8.csv",\
##    "Kennisboek WEGEN - v5-UTF-8.csv"]
    ]

# Product & Processes Models file paths
prod_dirs  = ["../GellishData"]
prod_file_names = [
##    "Semantic model of a road network - UTF-8.csv",\
##    "Semantisch model van een Wegennet met Huis - v5.2-UTF-8.csv"
    ]

# Default output path name
ini_out_path = r"../Data"

# Bootstrapping phrases and UIDs
boot_base_phrasesEN    = ["is a kind of", "is a specialization of",\
                          "has by definition as first role a",\
                          "has by definition as second role a",\
                          "is a base phrase for",\
                          "is an inverse phrase for",\
                          "is a synonym of"]
boot_inverse_phrasesEN = ["is by definition a role of a"]
boot_base_phrasesNL    = ["is een soort", "is een specialisatie van",\
                          "heeft per definitie als eerste rol een",\
                          "heeft per definitie als tweede rol een",\
                          "is een basis frase voor",\
                          "is een inverse frase voor",\
                          "is een synoniem van"]
boot_inverse_phrasesNL = ["is per definitie een rol van een"]
base_rel_type_uids     = {'1146':'specialization relation between kinds',\
                          '5944':'by definition being a first role in a relation',\
                          '5945':'by definition being a second role in a relation',\
                          '6066':'base phrase for a term for a kind of relation',\
                          '1986':'inverse phrase as alias for a term for a kind of relation',\
                          '1981':'synonym for a term for something',\
                          '5343':'by definition being a role of an individual thing'}
boot_alias_uids        = ['1981', '1986', '6066']
classifUID       = '1225'    # classification relation
classifiedUID    = '3821'    # 3821 = classified individual thing
specialUID       = '1146'    # subtyping relation
transUID         = '4691'    # translation relation
aliasUID         = '1980'    # alias relation
binRelUID        = '5935'    # binary relation
subtypeRoleUID   = '3818'    # UID of 'subtype' (role)
supertypeRoleUID = '3817'    # UID of 'supertype' (role)
synUID           = '1981'    # synonym relation
basePhraseUID    = '6066'    # base phrase for relation
inversePhraseUID = '1986'    # inverse phrase for relations
qualSubtypeUID   = '4328'    #
indOrMixRelUID   = '6068'    #
indivRelUID      = '4658'    #
kindHierUID      = '5052'    # 5052 = hierarchical relation between kinds
kindKindUID      = '1231'    # 1231 = binary relation between things of specified kinds
kindRelUID       = '5937'    # 5937 = binary relation between kinds
mixedRelUID      = '4719'    #
specialRelUID    = '1146'    #
possAspUID       = '1727'    # 1727 = posession of an aspect by an individual thing
possessorUID     = '4290'    # 4290 - possessor of an aspect (role)
transRelUID      = '5520'    # 5520 - transitive relation
concPossAspUID   = '2069'    # conceptual possession of an aspect UID (relation)
concComplRelUID  = '4902'    # conceptual compliance UID (relation)
qualSubtypeUID   = '4328'    # qualitative subtype UID (role)
qualOptionsUID   = '4848'    # qualitative options UID (role)
concComplUID     = '4951'    # conceptually compliant UID (role)
concQuantUID     = '1791'    # conceptual quantification UID (relation)
qualifUID        = '4703'    # qualification relation
quantUID         = '2044'    # quantification of an aspect by a mathematical space
physObjUID       = '730044'  # physical object
infoUID          = '970002'  # information
informativeUID   = '4173'    # role of informative qualitative information about an individual thing
occurrenceUID    = '193671'  #
concComposUID    = '1261'    # conceptual composition relation
concComponUID    = '3829'    # conceptual component role
involvedUID      = '4546'    # 4546 = <involved> being a second role in an <involvement in an occurrence> relation
involvUID        = '4767'    # involvement in an occurrence (relation)
nextUID          = '5333'    # 5333 next element (role)
shallUID         = '5735'    #
roleUID          = '160170'  #
composUID        = '1260'    #
concWholeUID     = '3830'    #
concPosessorUID  = '4705'    #
anythingUID      = '730000'  #
concBinRelKindsUID = '1231'  #
componUID        = '730035'  # 730035 = component
propUID          = '551004'  # quantification on scale
modelLangUID     = '589296'  # 'mixed'
kindAndMixRelUID = '7071'    #
English_uid      = '910036'
Dutch_uid        = '910037'
is_called_uid    = '5117'
first_role_uid   = '5944'    # 'by definition being a first role in a relation',\
second_role_uid  = '5945'    # 'by definition being a second role in a relation',\
by_def_role_of_ind = '5343'  # 'by definition being a role of an individual thing'}
indivUID         = '730067'  # 730067 represents the concept 'individual thing'
                             #        (with as subtypes kinds of phenomena as well as relations)

statusses     = ["accepted"           ,"proposed" ,"proposal"                   ,"issue",    "defaults",\
                 "geaccepteerd"        ,"voorstel" ,"voorgesteld","discussiepunt","onzeker",  "defaults"]
ignores       = ["ignore","ignored"   ,"inherited","ignore inherited","history" ,"replaced", "deleted",\
                 "negeer","genegeerd" ,"geërfd"   ,"historie","geschiedenis"    ,"vervangen","vervallen"]
subtypeName   = ['subtype'  ,'subtype']     # English, Dutch
supertypeName = ['supertype','supertype']
# initialize first line of relRolesTable(bin_rel, superRel, etc.
initialRelRow = ['5935', '2850', '4729', 'relator', '4824', 'related', \
                 '730000', 'anything', '730000', 'anything']
# The following lists should be generated from function Determine_subtype_list(classUID)
# UIDs that define a taxonomy: subtypes of 1146:
specialRelUIDs  = ['1146', '1726', '5277', '6022', '5396', '5683']
# Some UIDs that are classification relations, being subtypes of 1225:
classifUIDs     = ['1225', '1588']
# UIDs that imply a new UoM in units and currencies table.
uom_def_uids    = ['1726', '5708', '1981']

involHead   = ['Occurrences' ,'Gebeurtenissen']
roleHead    = ['Role'        ,'Rol']
otherHead   = ['Involvements','Betrokkenen']
kindHead    = ['Kind'        ,'Soort']
aspectHead  = ['Aspect'      ,'Aspect']
partOccHead = ['Part occurrence','Deelgebeurtenis']
compHead    = ['Part hierarchy' ,'Compositie']
partHead    = ['Part of part'   ,'Deel van deel']
par3Head    = ['Further part'   ,'Verder deel']
subsHead    = ['Subtypes'    ,'Subtypen']
