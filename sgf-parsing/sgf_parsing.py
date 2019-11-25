class SgfTree:
    def __init__(self, properties=None, children=None):
        self.properties = properties or {}
        self.children = children or []

    def __eq__(self, other):
        if not isinstance(other, SgfTree):
            return False
        for k, v in self.properties.items():
            if k not in other.properties:
                return False
            if other.properties[k] != v:
                return False
        for k in other.properties.keys():
            if k not in self.properties:
                return False
        if len(self.children) != len(other.children):
            return False
        for a, b in zip(self.children, other.children):
            if a != b:
                return False
        return True

    def __ne__(self, other):
        return not self == other

import re

def parse(input_string):
    
    error_pattern = r'()'
    if not(input_string[0:2] == '(;' and input_string[-1] == ')'):
        raise ValueError('Entrada Invalida')
    
    input_str = re.split(r'[\(\);]',input_string[2:-1])
    children_str = list(filter(None,input_str[1:]))
    print(input_str, children_str)

    properties = processa_propriedades(input_str[0])
    children = [SgfTree(processa_propriedades(i)) for i in children_str]
    print("P: {}, C: {}".format(properties, children))
    return SgfTree(properties, children)

def processa_propriedades(string):
    properties = {}
    pattern = r'(^[A-Z][A-Z]?)(((?<!\\)\[.*?(?<!\\)\])+)'

    while string:
        prop_1 = re.search(pattern, string, flags=re.DOTALL)
        
        if prop_1 is None:
            raise ValueError('Sintaxe SGF errada!')
        
        prop_2 = re.split(r'(?<!\\)[\[\]]', prop_1.group(2))
        prop_2 = [re.sub(r'\\','',p).expandtabs(1)
                       for p in prop_2 if len(p) > 0]
        
        properties[prop_1.group(1)] = prop_2
        string = re.sub(pattern,'',string,flags=re.DOTALL)
        
    return properties
