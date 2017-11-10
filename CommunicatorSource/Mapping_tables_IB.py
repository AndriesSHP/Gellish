''' This file contains Mapping tables that are required as input for the procedure 
    that reads JSON files with product data that are retrieved from a product supplier database
    and that converts those files into Gellish expressions that can be further processed or exported. 
'''

# Main keys list
#                   IB               Gellish
keys_map       = [('articleId'     ,970047, 'identificatie'),\
                  ('description'   ,5605  , 'synonieme aanduiding'),\
                  ('properties'    ,493676, 'verzameling uitdrukkingen')]

# Attributes of 'properties'
#                   IB                Gellish                 Gellish                                             Gellish    IB      IB
attributes_map = [('ibProductsoort',('identificatie', 5396  , 'is een model'                      , 6066, 730066, 'soort object', '', ''   )),\
                  ('breedteMm'     ,('identificatie', 5527  , 'heeft per definitie als aspect een', 6066, 550464, 'breedte', 'value','unit')),\
                  ('hoogteMm'      ,('identificatie', 5527  , 'heeft per definitie als aspect een', 6066, 550126, 'hoogte' , 'value','unit')),\
                  ('gewichtKg'     ,('identificatie', 5527  , 'heeft per definitie als aspect een', 6066, 550047, 'gewicht', 'value','unit'))]
# Keys for values
#                   IB                Gellish
value_key_map  = [('label'          ,910300, 'label'),\
                  ('name'           ,730066, 'soort'),\
                  ('value'          ,910130, 'naam'),\
                  ('unit'           ,1733  , 'schaal')]

# Allowed values and units
#                  IB                Gellish
values_map     = {'Dakramen|Ramen' :(43769 , 'dakvenster'),\
                  'mm'             :(570423, 'mm'),\
                  'kg'             :(570039, 'kg')}
