import Tokenizer
import Token

'''
    This file defines the ParseTree class
    and implements a parser for the provided LL(1) arithmetic
    expression grammar. The parser returns the corresponding
    ParseTree.

    ParseTree has a value field.

    ConstantFunction, UnaryFunction, and BinaryFunction are
    the derived classes of ParseTree. 

    ConstantFunction simply stores a value (such as a variable or number).

    UnaryFunction stores the function name and the ParseTree of its argument.

    BinaryFunction stores the function name and the ParseTrees of its arguments.

    The parser will raise a ValueError if the input expression is misformed.
'''

class ParseTree():
    __slots__ = ['_value']
    # A parse tree is a node with 0, 1, 2 children:
    #   node with 0 children = constant function (Number or Variable)
    #   node with 1 child = unary function
    #   node with 2 childern = binary function

class ConstantFunction(ParseTree):
    # value will store a number or variable ref
    def __init__(self, val):
        self._value = val

    @property
    def value(self):
        return self._value

class UnaryFunction(ParseTree):
    # value will store a unary function name
    __slots__ = ['_name','_child']
    def __init__(self, name):
        self._value = name

    @child.setter
    def child(self, parseTree):
        self._child = parseTree

    @property
    def name(self)
        return self._value

class BinaryFunction(ParseTree):
    # value will store a binary function name
    __slots__ = ['_lchild', "_rchild"]
    def __init__(self, name):
        self._value = name

    @property
    def name(self)
        return self._value

    @lchild.setter
    def lchild(self, parseTree):
        self._lchild = parseTree
    
    @rchild.setter
    def rchild(self, parseTree):
        self._rchild = parseTree

'''
    Parse a given arithmetic expression string
    Return a parse tree
'''
def Parse():
    return Expression()

''' Parses an end parenthesis '''
def EndParens():
    token = Tokenizer.PeakToken()
    if token.IsSymbol(')'):
        Tokenizer.Consume()
    else:
        raise ValueError("Unmatched parenthesis")

'''
    Parse an Expression
'''
def Expression():
    token = Tokenizer.PeakToken()
    if (token.IsNumber() or \
        token.IsFunc() or \
        token.IsVariable() or \
        token.IsSymbol(['+', '-', '('])):

        parseTree = Term()
        return TermTail(parseTree)
    else:
        raise ValueError("Expression")

'''
    Parse a Term
'''
def Term():
    token = Tokenizer.PeakToken()
    if (token.IsNumber() or \
        token.IsFunc() or \
        token.IsVariable() or \
        token.IsSymbol(['+', '-', '('])):

        parseTree = Factor()
        return FactorTail(parseTree)
    else:
        raise ValueError("Term")

'''
    Parse a Term Tail
'''
def TermTail(leftParseTree):
    token = Tokenizer.PeakToken()
    if token.IsSymbol(['+','-']):

        Tokenizer.Consume()

        parseTree = BinaryFunction(token.text)
        parseTree.lchild(leftParseTree)
        parseTree.rchild(Term())

        return TermTail(parseTree)

    elif token.IsEOF() or \
            token.IsSymbol(')'):

        return leftParseTree

    else:
        raise ValueError("Term Tail")

'''
    Parse a Factor
'''
def Factor():
    token = Tokenizer.PeakToken()

    if token.IsVariable():

        Tokenizer.Consume()
        return ConstantFunction(Token.Variable.get_var(token.text))

    elif token.IsSymbol('('):

        Tokenizer.Consume()
        parseTree = Expression() 
        EndParens()
        return parseTree

    elif token.IsNumber() or \
            token.IsSymbol(['+','-']):

        return Number()

    elif token.IsFunc():

        Tokenizer.Consume()
        parseTree = UnaryFunction(token.text)
        parseTree.child(Factor())
        return parseTree

    else:
        raise ValueError("Factor")

'''
    Parse a Factor Tail
'''
def FactorTail(leftParseTree):
    token = Tokenizer.PeakToken()
    if token.IsSymbol(['*','/','^']):

        Tokenizer.Consume()
        parseTree = BinaryFunction(token.text)
        parseTree.lchild(leftParseTree)
        parseTree.rchild(Factor())

        return FactorTail(parseTree)

    elif token.IsFunc():
        # implicit multiply
        Tokenizer.Consume()
        parseTree = BinaryFunction('*')
        rightParseTree = UnaryFunction(token.text)
        rightParseTree.child(Factor())

        parseTree.lchild(leftParseTree)
        parseTree.rchild(rightParseTree)

        return FactorTail(parseTree)

    elif token.IsEOF() or \
        token.IsSymbol(['+','-',')']):

        return leftParseTree

    else:
        raise ValueError("Factor Tail")        

'''
    Parse a Number
'''
def Number():
    token = Tokenizer.PeakToken()
    negate = token.IsSymbol(['-'])
    if token.IsSymbol(['+','-']):
        # ignore unary +
        # use negate for unary -
        Tokenizer.Consume()
        token = Tokenizer.PeakToken()

    if token.IsNumber():

        Tokenizer.Consume()
        text = ('-' if negate else '') + token.text
        val = float(text) if '.' in text else int(text)
        return ConstantFunction(val)

    else:
        raise ValueError("Invalid Number")