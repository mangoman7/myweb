from pattern_functions import *
def patterns():
    patterns = [{
            'Title':'All Extractor',
            'id':'extract_1',
            'recode':'^https://.*$',
            'function':extract_1
    }]
    return patterns