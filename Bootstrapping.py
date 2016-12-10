# Base ontology and domain dictionaries directories
dict_dirs  = ["Data"]

# Base ontology file
base_onto_file = "Base ontology (core).csv"

# Taxonomic Dictionary files
dict_files = ["Taxonomic Dictionary - UoMs & currencies - Subset.csv",\
              "Taxonomic Dictionary about Roads.csv"]

# Knowledge, Requirements and Product file paths
model_dirs  = ["Data",]
model_files = ["Knowledge base ROADS - v5.1.csv"]

# Knowledge, Requirements and Product & Processes Models file paths
prod_dirs  = ["Data",]
prod_files = ["Semantic model of a road network.csv"]

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
                          "is synoniem van"]
boot_inverse_phrasesNL = ["is per definitie een rol van een"]
base_rel_type_uids     = [1146, 5944, 5945, 6066, 1986, 1981, 5343]
boot_alias_uids        = [1981, 1986, 6066]
classifUID       = 1225     # classification relation
classifiedUID    = 3821     # 3821 = classified individual thing
specialUID       = 1146     # subtyping relation
transUID         = 4691     # translation relation
aliasUID         = 1980     # alias relation
binRelUID        = 5935     # binary relation
subtypeRoleUID   = 3818     # UID of 'subtype' (role)
supertypeRoleUID = 3817     # UID of 'supertype' (role)
synUID           = 1981     # synonym relation
basePhraseUID    = 6066     # base phrase for relation
invUID           = 1986     # inverse phrase for relations
qualSubtypeUID   = 4328
indOrMixRelUID   = 6068
indivRelUID      = 4658
kindHierUID      = 5052     # 5052 = hierarchical relation between kinds
kindKindUID      = 1231     # 1231 = binary relation between things of specified kinds
kindRelUID       = 5937     # 5937 = binary relation between kinds
mixedRelUID      = 4719
specialRelUID    = 1146
possAspUID       = 1727     # 1727 = posession of an aspect by an individual thing
possessorUID     = 4290     # 4290 - possessor of an aspect (role)
transRelUID      = 5520     # 5520 - transitive relation
concPossAspUID   = 2069     # conceptual possession of an aspect UID (relation)
concComplRelUID  = 4902     # conceptual compliance UID (relation)
qualSubtypeUID   = 4328     # qualitative subtype UID (role)
qualOptionsUID   = 4848     # qualitative options UID (role)
concComplUID     = 4951     # conceptually compliant UID (role)
concQuantUID     = 1791     # conceptual quantification UID (relation)
qualifUID        = 4703     # qualification relation
quantUID         = 2044
physObjUID       = 730044   # physical object
infoUID          = 970002   # information
informativeUID   = 4173     # role of informative qualitative information about an individual thing
occurrenceUID    = 193671
concComponUID    = 3829     # conceptual component role
involvedUID      = 4546     # 4546 = <involved> being a second role in an <involvement in an occurrence> relation
nextUID          = 5333     # 5333 next element (role)
shallUID         = 5735
roleUID          = 160170
composUID        = 1260
concWholeUID     = 3830
concPosessorUID  = 4705
anythingUID      = 730000
concBinRelKindsUID = 1231
componUID        = 730035   # 730035 = component
propUID          = 551004   # quantification on scale
modelLangUID     = 589296   # 'mixed'

statusses     = ["accepted"           ,"proposed" ,"proposal"                   ,"issue",    "defaults",\
                 "geaccepteerd"        ,"voorstel" ,"voorgesteld","discussiepunt","onzeker",  "defaults"]
ignores       = ["ignore","ignored"   ,"inherited","ignore inherited","history" ,"replaced", "deleted",\
                 "negeer","genegeerd" ,"geërfd"   ,"historie","geschiedenis"    ,"vervangen","vervallen"]
subtypeName   = ['subtype'  ,'subtype']     # English, Dutch
supertypeName = ['supertype','supertype']
# initialize first line of relRolesTable(bin_rel, superRel, etc.
initialRelRow = [5935, 2850, 4729, 'relator', 4824, 'related', 730000, 'anything', 730000, 'anything']
# the following lists should be generated from function DetermineSubtypeList(classUID)
specialRelUIDs  = [1146, 1726, 5277, 6022, 5396, 5683] # UIDs that define a taxonomy: subtypes of 1146.
classifUIDs     = [1225, 1588] # some UIDs that are classification relations, being subtypes of 1225.
uom_def_uids    = [1726, 5708, 1981] # UIDs that imply a new UoM in units and currencies table.
