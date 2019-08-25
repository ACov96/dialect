import ply.lex as l

tokens = (
    'NUMBER',
    'ID',
    'STRING',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'EQUAL',
    'SEMICOLON',
    'LBRACKET',
    'RBRACKET',
    'LPAREN',
    'RPAREN',
    'COMMA',
)

t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_STRING = r'".*"'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_EQUAL = r'='
t_SEMICOLON = r';'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','

def t_NUMBER(t):
    r'[0-9]+(\.[0-9]+)?'
    t.value = float(t.value)
    return t

def t_COMMENT(t):
    r'\#.*'
    pass

t_ignore = ' \t\r\n'

def t_error(t):
    print('Illegal character', t.value[0])
    t.lexer.skip(1)

def lex(file_name):
    with open(file_name, 'r') as f:
        file_content = f.read()
        lexer = l.lex()
        lexer.input(file_content)
        tokens = []
        while True:
            tok = lexer.token()
            if not tok:
                break
            tokens.append(tok)
        return tokens

def new_lexer():
    return l.lex()
