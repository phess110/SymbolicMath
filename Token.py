'''
    This file defines the Token and Variable classes.
'''

'''
    Token Class

        Contains fields for the text of the token and the 
        type (variable, function, number, symbol, EOF)
        of the token.
'''
class Token:
    __slots__ = ['_text', '_type']
    def __init__(self, text, tokType):
        self._text = text
        self._type = tokType

    @property
    def text(self):
        return self._text

    @property 
    def tokType(self):
        return self._type

    @tokType.setter
    def tokType(self, new_type):
        self._type = new_type

    def IsVariable(self):
        return self._type == "Variable"

    def IsFunction(self):
        return self._type == "Func"
    
    def IsNumber(self):
        return self._type == "Number"
    
    def IsSymbol(self, lst):
        return self._type == "Symbol" and self.text in lst

    def IsEOF(self):
        return self._type == "EOF"

# Global list of variables
VARIABLES = []

'''
    Variable Class

        Stores the name and current value of a user-defined variable.
        All defined variables are stored in the global VARIABLES array.
'''
class Variable:
    __slots__ = ['_name', '_value']
    
    def __init__(self, name):
        self._name = name
        VARIABLES.append(self)
    
    @classmethod
    def is_var(cls, name):
        for v in VARIABLES:
            if v._name == name:
                return True
        return False

    @classmethod
    def get_var(cls, name):
        for v in VARIABLES:
            if v._name == name:
                return v
        return None

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_val):
        self._value = new_val