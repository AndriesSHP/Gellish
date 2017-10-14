class GellishDict(dict):
    ''' A dictionary for names in a context that refer to the denoted concepts.
        The roles of the names are indicated by alias relation_type_UIDs, such as for <is a code for>: 
        key   = name_in_context(tuple) = (languageUID, communityUID, name).
        value = value_triple = (UID, naming_relation_type_UID, description)
    '''
    def __init__(self, name):
        self.name = name
        
    def add_name_in_context(self, name_in_context, value_triple):
        if name_in_context not in self:
            #self.key   = name_in_context(tuple) = (lanuageUID, communityUID, name).
            #self.value = value_triple = (UID, naming_relation_type_UID, description)
            self[name_in_context] = value_triple
            print('add: ',name_in_context, self[name_in_context])
        else:
            value_triple2 = self.find_anything(name_in_context)
            print('Error: Name in context: %s, %s is already known by uid (%s)' % (name_in_context, value_triple, value_triple2))

    def find_anything(self, q_name_in_context):
        if q_name_in_context in self:
            print('Found: ', q_name_in_context, self[q_name_in_context])
            return(self[q_name_in_context])
        else:
            print('Not found: ',q_name_in_context)
            return(None)
        
    def filter_on_key(self, q_string, string_commonality):
        """Search for q-string in the third part of the key of the dictionary,
        where key = term_in_context = (language_uid, community_uid, name).
        Returns a list of items (key, value_triple) that contain q_string as the third part of the key.
        Example item: term_in_context, value_triple = {(910036, 193259, "anything"),(730000, 5117, 'descr'))
        """
        # a list of tuples of [(key0, val0]), (key1, val1), ...]
        items = self.items()
        result_list = []

        # create a filter function that returns true if
        # 0) q_string is equal to the third position of the first(key) field of an item:
        #    case sensitive identical
        # 1) q_string is in that field:
        #    case sensitive partially identical
        # 2) q_string is in that field and starts with that string
        #    case sensitive front end identical
        # 3), 4), 5) idem, but case insensitive
        string_commonalities = ['csi', 'cspi', 'csfi', 'cii', 'cipi', 'cifi']

        if string_commonality   == string_commonalities[0]:
            filt = lambda item: q_string == item[0][2]
        elif string_commonality == string_commonalities[1]:
            filt = lambda item: q_string in item[0][2]
        elif string_commonality == string_commonalities[2]:
            filt = lambda item: item[0][2].startswith(q_string)
        elif string_commonality == string_commonalities[3]:
            filt = lambda item: q_string.lower() == item[0][2].lower()
        elif string_commonality == string_commonalities[4]:
            filt = lambda item: q_string.lower() in item[0][2].lower()
        elif string_commonality == string_commonalities[5]:
            filt = lambda item: item[0][2].lower().startswith(q_string.lower())
        else:
            print('Error: string commonality %s unknown' % (string_commonality))
            filt = ''

        # use the filter to create a *list* of items that match the filter
        result_list = filter(filt, items)
        
        # convert the list to a Gellish dictionary
        #result = GellishDict(result_list)
        
        # and return the resulting list of filtered items
        return(result_list)

class Preferences(dict):
    '''A dictionary for preferences and defaults for the owner of the table of preferences'''
    def __init__(self, dict_name):
        self.name = dict_name

#----------------------------------------------------------------------------      
if __name__ == "__main__":
    d = GellishDict('Dictionary')
    d[1, 4, "anything"] = (730000, 5117, 'what can be thought of')                 
    d[1, 4, "THING"]    = (2,1, 'thing')
    d[1, 5, "pump"]     = (4,1, 'that is intended to ...')
    d[2, 5, "pomp"]     = (4,1, 'die bedoeld is om ...')
    d[3, 5, "Pumpe"]    = (4,2, 'der is geeignet zu ...')
    d[1, 5, "Pump"]     = (4,1, 'synonym of pump') 
    print('Dictionary-0: ',d)
    
    n = (2, 5, "iets")
    v = (730000, 5117, 'waar aan gedacht kan worden.')
    d.add_name_in_context(n,v)
    print('Dictionary-1: ',d)

    n2 = (2, 5, "iets")
    v2 = (1, 1, 'verkeerde UID')
    d.add_name_in_context(n2,v2)
    print('Dictionary-2: ',d)
    
    # print all items that have "pump" as the third field in the key:
    candidates = d.filter_on_key("pump",'csi')
    for candidate in candidates:
        print ("case sensitive identical (pump): ",candidate)

    # print all items that contain "Pu" at the front end of the third field of the key:
    candidates = d.filter_on_key("Pu",'csfi')
    for candidate in candidates:
        print ("case sensitive front end identical (Pu): ",candidate)

    # print all items that contain "ump" as a string somewhere in the third field of the key:
    candidates = d.filter_on_key("ump",'cspi')
    for candidate in candidates:
        print ("case sensitive partially identical (ump): ",candidate)

    # print all items that have "pump" as the third field in the key:
    candidates = d.filter_on_key("pump",'cii')
    for candidate in candidates:
        print ("case insensitive identical (pump): ",candidate)
        
    # print all items that contain "pu" at the front end of the third field of the key:
    candidates = d.filter_on_key("pu",'cifi')
    for candidate in candidates:
        print ("case insensitive front end identical (pu): ",candidate)

    # print all items that contain "i" as a string somewhere in the third field of the key:
    candidates = d.filter_on_key("i",'cipi')
    for candidate in candidates:
        print ("case insensitive partially identical (i): ",candidate)
