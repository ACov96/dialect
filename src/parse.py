import ply.yacc as yacc
import ply.lex as l
from lex import tokens, new_lexer
from util import make_obj

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
)

def p_statement_list(p):
    '''statement_list : statement statement_list
                      | empty'''
    if p[1] is None:
        return
    if len(p) < 3 or p[2] is None:
        p[0] = [p[1]]
    else:
        p[2].append(p[1])
        p[0] = p[2]
    # p[0] = p[2].append(p[1]) if len(p) < 3 else [p[1]]

def p_empty(p):
    '''empty :'''
    pass

def p_statement_assignment(p):
    '''statement : assignment SEMICOLON'''
    p[0] = p[1]

def p_statement_expr(p):
    '''statement : expr SEMICOLON'''
    p[0] = ('statement_expr', p[1])

def p_assignment(p):
    '''assignment : l_value EQUAL r_value'''
    p[0] = ('assignment', p[1], p[3])

def p_r_value(p):
    '''r_value : expr'''
    p[0] = p[1]

def p_l_value_id(p):
    '''l_value : ID'''
    p[0] = ('identifier', p[1])

def p_l_value_record(p):
    '''l_value : ID fields'''
    p[0] = ('record', ('identifier', p[1]), p[2])

def p_fields_single(p):
    '''fields : LBRACKET expr RBRACKET'''
    p[0] = [p[2]]

def p_fields_multi(p):
    '''fields : LBRACKET expr RBRACKET fields'''
    p[0] = [p[2]] + p[4]

def p_expr(p):
    '''expr : alg_op'''
    p[0] = p[1]

def p_expr_string(p):
    '''expr : STRING'''
    p[0] = ('string', p[1])

def p_expr_number(p):
    '''expr : NUMBER'''
    p[0] = ('number', p[1])

def p_expr_bool(p):
    '''expr : BOOL'''
    p[0] = ('bool', p[1])
    
def p_expr_func_call(p):
    '''expr : func_call'''
    p[0] = p[1]

def p_expr_id(p):
    '''expr : ID'''
    p[0] = ('identifier', p[1])

def p_func_call(p):
    ''' func_call : ID LPAREN arg_list RPAREN'''
    p[0] = ('func_call', p[1], p[3])
    
def p_arg_list_empty(p):
    '''arg_list : empty'''
    p[0] = []

def p_arg_list_single(p):
    '''arg_list : expr'''
    p[0] = [p[1]]

def p_arg_list_multi(p):
    '''arg_list : expr COMMA arg_list'''
    if len(p[3]) > 0:
        p[0] = [p[1]] + p[3]
    else:
        p[0] = [p[1]]
       
def p_alg_op(p):
    '''alg_op : expr PLUS expr
               | expr MINUS expr
               | expr MULTIPLY expr
               | expr DIVIDE expr'''
    if p[2] == '+':
        p[0] = ('addition', p[1], p[3])
    elif p[2] == '-':
        p[0] = ('minus', p[1], p[3])
    if p[2] == '*':
        p[0] = ('multiply', p[1], p[3])
    if p[2] == '/':
        p[0] = ('divide', p[1], p[3])

def p_expr_list(p):
    '''expr : LBRACKET arg_list RBRACKET'''
    p[0] = ('list', p[2])

def p_expr_object(p):
    '''expr : LBRACE record_list RBRACE'''
    p[0] = ('object', make_obj(p[2]))

def p_record_list_single(p):
    '''record_list : ID COLON expr'''
    p[0] = [(p[1], p[3])]

def p_record_list_multi(p):
    '''record_list : ID COLON expr COMMA record_list'''
    p[0] = [(p[1], p[3])] + p[5]

def p_record_list_empty(p):
    '''record_list : empty'''
    p[0] = []

def p_expr_access(p):
    '''expr : expr LBRACKET expr RBRACKET'''
    p[0] = ('access', p[1], p[3])

def p_error(p):
    print('Syntax error\n', p)

def parse(file_name):
    with open(file_name, 'r') as f:
        file_content = f.read()
        lexer = new_lexer()
        parser = yacc.yacc()
        statements = parser.parse(file_content)
        statements.reverse()
        return statements
