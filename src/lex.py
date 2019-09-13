import ply.lex as l

tokens = (
    'NUMBER',
    'ID',
    'STRING',
    'BOOL',
    'NULL',
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
    'LBRACE',
    'RBRACE',
    'COMMA',
    'FUN',
    'COLON',
)

t_FUN = r'fun'
t_NULL = r'null'
t_ID = r'[a-z_][a-z_0-9]*'
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
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COLON = r':'

def t_NUMBER(t):
    r'[0-9]+(\.[0-9]+)?'
    t.value = float(t.value)
    return t

def t_STRING(t):
    r'\"(\\.|[^"\\])*\"'
    t.value = t.value.replace('"', '')
    return t

def t_BOOL(t):
    r'(true|false)'
    if t.value == 'true':
        t.value = True
    else:
        t.value = False

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
