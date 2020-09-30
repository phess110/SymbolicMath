import string
import Token

'''
    This file defines a state machine for parsing arithmetic expressions 
'''

# List of available unary functions
RESERVED = ['sin', 'cos', 'tan', 'log', 'ln', 'lg', 'csc', 'sec', 'cot', 'exp']
# Available binary functions
''' POW ADD SUBTRACT TIMES DIVIDE '''

# Lists for defining transitions
LETTERS = list(string.ascii_lowercase + string.ascii_uppercase)
DIGIT = list(string.digits)
WHITESPACE = [' ', '\t']
SYMBOLS = ['+', '-', '*', '/', '^', '(', ')']
DOT = ['.']
END = ['$'] # special ending symbol
E = ['E', 'e']
SYM_SPACE_LETTER = SYMBOLS + WHITESPACE + LETTERS

# STATE MACHINE SET UP 
TRANSITIONS = {}
INPUT = ""
POSITION = 0
STATE = 0
ACCEPTING = [2, 3, 6]
CURR_TOKEN = 0

def addTransition(fromState, toState, onChars):
    for c in onChars:
        TRANSITIONS[(fromState, c)] = toState

# Scan for variables/reserved functions
addTransition(0, 0, WHITESPACE)
addTransition(0, 0, END)
addTransition(0, 1, LETTERS)
addTransition(1, 1, LETTERS)
addTransition(1, 2, SYMBOLS)
addTransition(1, 2, WHITESPACE)
addTransition(1, 2, END)

# Scan for symbols 
addTransition(0, 3, SYMBOLS)

# Scan for numbers
addTransition(0, 4, DOT)
addTransition(4, 5, DIGIT)
addTransition(5, 5, DIGIT)
addTransition(5, 6, SYM_SPACE_LETTER)
addTransition(5, 9, E)
addTransition(0, 7, DIGIT)
addTransition(7, 7, DIGIT)
addTransition(7, 6, SYM_SPACE_LETTER)
addTransition(7, 8, DOT)
addTransition(7, 9, E) # this must occur after 7 -> 6 transition to override action of 'e'
addTransition(8, 8, DIGIT)
addTransition(8, 6, SYM_SPACE_LETTER)
addTransition(8, 9, E)
addTransition(9, 4, DOT)
addTransition(9, 7, DIGIT)
addTransition(9, 10, ['+','-'])
addTransition(10, 4, DOT)
addTransition(10, 7, DIGIT)

addTransition(5, 6, END)
addTransition(7, 6, END)
addTransition(8, 6, END)

# Transition into error state on unexpected end
addTransition(4, -1, END)
addTransition(9, -1, END)

'''
    Initialize the scanner with the given string
    Resets state machine and performs minor input manipulation
'''
def Initialize(text):
    global INPUT, POSITION, STATE
    if '$' in text:
        raise ValueError("Illegal character: $")
    INPUT = text.lower().strip() + "$"
    POSITION = 0
    STATE = 0

'''
    Returns the token type of the given text based on the 
    the current accepting state of the machine
'''
def GetType(text):
    if STATE == 2:
        if (text in RESERVED):
            return "Func"
        elif (Token.Variable.is_var(text)):
            return "Variable"
        else:
            print(f"ERROR: Variable {text} is not defined.")
            return "VarError"
    elif STATE == 3:
        return "Symbol"
    elif STATE == 6:
        return "Number"
    else: 
        return "Error" # unreachable?

'''
    Prints out all the tokens within the string
    MUST call initialize beforehand.
'''
def Tokenize():
    t = Token.Token("", "START")
    while(t.tokType != "EOF" and t.tokType != "Error"):
        t = PeakToken()
        Consume()
        print(f"Text: \"{t.text}\".  Type: {t.tokType}")

'''
    Runs the state machine until an accepting state is reached
    Stores the token which was read in CURR_TOKEN
'''
def RunStateMachine():
    global STATE, POSITION, CURR_TOKEN
    init_pos = POSITION
    n = len(INPUT)
    while(not(STATE in ACCEPTING)):
        try:
            STATE = TRANSITIONS[(STATE, INPUT[POSITION])]
            POSITION = POSITION + 1
        except:
            print(f"ERROR: Unexpected character {INPUT[POSITION]} at position {POSITION} in input.")
            CURR_TOKEN = Token.Token("", "Error")
            return
        if STATE == -1 or POSITION > n:
            print("ERROR: Input ended unexpectedly.")
            CURR_TOKEN = Token.Token("", "Error")
            return
    # All accepting states except state 3 consume the
    # next character which we have to undo
    if STATE != 3:
        POSITION = POSITION-1
    tokText = INPUT[init_pos:POSITION].strip()
    CURR_TOKEN = Token.Token(tokText, GetType(tokText))

'''
    Returns the value of CURR_TOKEN
'''
def PeakToken():
    if POSITION >= len(INPUT):
        return Token.Token("","EOF")
    elif STATE == 0:
        RunStateMachine()
    return CURR_TOKEN

'''
    Move the state machine back to the starting state 
    to prepare to extract next token.

    After we call PeakToken(), we must call Consume() in order to 
    continue tokenizing. Otherwise, PeakToken will just keep 
    returning the same token.
'''
def Consume():
    global STATE
    STATE = 0