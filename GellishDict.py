class GellishDict(dict):
    ''' A dictionary for names in a context that refer to the denoted concepts.
        The roles of the names is indicated by alias relation_type_UIDs, such as for <is a code for>: 
        key   = name_in_context(tuple) = (lanuageUID, communityUID, name).
        value = value_pair = (UID, naming_relation_type_UID)
    '''
    def add_name_in_context(self, name_in_context, value_pair):
        if name_in_context not in self:
            #self.key   = name_in_context
            #self.value = value_pair
            self[name_in_context] = value_pair
            print('add: ',name_in_context, self[name_in_context])
        else:
            value_pair = self.find_anything(name_in_context)
            print('Name in context: %s already known by uid (%s)' % (name_in_context, value_pair))

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
        Returns a list of items (key, value_pair) that contain q_string as the third part of the key.
        Example item: term_in_context, value_triple = {(910036, 193259, "anything"),(730000, 5117, 'descr'))
        """
        # a list of tuples of [(key0, val0]), (key1, val1), ...]
        items = self.items()

        # create a filter function that returns true if
        # 1) q_string is equal to the third position of the first(key) field of an item <or>
        # 2) q_string is in that field
        # 3) q_string is in that field and starts with that string
        identical       = ['case sensitive identical', 'case insensitive identical']
        part_identical  = ['case sensitive partially identical', 'case insensitive partially identical']
        front_identical = ['case sensitive front end identical', 'case insensitive front end identical']
        if string_commonality in identical:
            filt = lambda item: q_string == item[0][2]
        elif string_commonality in part_identical:
            filt = lambda item: q_string in item[0][2] ### TO BE DONE: first split q_string in 'words'
        elif string_commonality in front_identical:
            filt = lambda item: q_string in item[0][2] ### TO BE IMPROVED and extended
        else:
            print('string commonality %s unknown' % (string_commonality))

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
        
if __name__ == "__main__":
    d = GellishDict({
        (1, 4, "anything"): (1,1),
        (1, 4, "thing")   : (2,1),
        (1, 5, "pump")    : (4,1),
        (3, 5, "Pumpe")   : (4,2),
        (2, 5, "pump")    : (4,1) })

    print(d)
    n = (2, 5, "ïets")
    v = (730000, 5117)
    d.add_name_in_context(n,v)
    print(d)

    n2 = (2, 5, "iets")
    v2 = (1, 1)
    d.add_name_in_context(n2,v2)
    print(d)
    
    # print all items that have "pump" as the third field in the key:
    candidates = d.filter_on_key("pump",'case sensitive identical')
    for candidate in candidates:
        print ("case sensitive identical",candidate)

    # print all items that contain "Pu" at the front end of the third field of the key:
    candidates = d.filter_on_key("Pu",'case insensitive front end identical')
    for candidate in candidates:
        print ("case insensitive front end identical",candidate)

    # print all items that contain "ump" as a string somewhere in the third field of the key:
    candidates = d.filter_on_key("ump",'case sensitive partially identical')
    for candidate in candidates:
        print ("case sensitive front end identical",candidate)

    # print all items that contain "i" as a string somewhere in the third field of the key:
    candidates = d.filter_on_key("i",'case insensitive partially identical')
    for candidate in candidates:
        print ("case insensitive front end identical",candidate)
