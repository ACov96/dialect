import ply.yacc as yacc
import ply.lex as l
from .lex import tokens, new_lexer
from .util import make_obj
from .error import syntax_error

class ParserError(Exception):
    def __init__(self, msg, tok):
        super().__init__(msg)
        self.tok = tok

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
)

start = 'statement_list'

def p_statement_list(p):
    '''statement_list : statement statement_list
                      | empty'''
    if p[1] is None:
        return []
    if len(p) < 3 or p[2] is None:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_empty(p):
    '''empty :'''
    pass

def p_statement_import(p):
    '''statement : IMPORT STRING SEMICOLON'''
    p[0] = ('import', p[2])

def p_statement_assignment(p):
    '''statement : assignment SEMICOLON'''
    p[0] = p[1]

def p_statement_conditional(p):
    '''statement : conditional'''
    p[0] = p[1]

def p_statement_expr(p):
    '''statement : expr SEMICOLON'''
    p[0] = ('statement_expr', p[1])

def p_statement_macro_def(p):
    '''statement : macro_def'''
    p[0] = p[1]

def p_statement_macro_call(p):
    '''statement : macro_call'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : l_value EQUAL r_value'''
    p[0] = ('assignment', p[1], p[3])

def p_statement_loop(p):
    '''statement : loop'''
    p[0] = p[1]

def p_loop(p):
    '''loop : WHILE LPAREN expr RPAREN LBRACE statement_list RBRACE'''
    p[0] = ('loop', p[3], p[6])

def p_statement_fun_def(p):
    '''statement : fun_def'''
    p[0] = p[1]

def p_fun_def(p):
    '''fun_def : FUN ID LPAREN id_list RPAREN LBRACE statement_list RBRACE'''
    p[0] = ('fun_def', p[2], p[4], p[7])

def p_statement_return(p):
    '''statement : RETURN expr SEMICOLON'''
    p[0] = ('return', p[2])

def p_id_list_single(p):
    '''id_list : ID'''
    p[0] = [p[1]]

def p_id_list_multi(p):
    '''id_list : ID COMMA id_list'''
    p[0] = [p[1]] + p[3]

def p_id_list_empty(p):
    '''id_list : empty'''
    p[0] = []

def p_conditional_full(p):
    '''conditional : IF LPAREN expr RPAREN LBRACE statement_list RBRACE conditional_elif conditional_else'''
    conditions = [(p[3], p[6])] + p[8] + p[9]
    p[0] = ('conditional', conditions)

def p_conditional_elif(p):
    '''conditional_elif : ELIF LPAREN expr RPAREN LBRACE statement_list RBRACE conditional_elif'''
    p[0] = [(p[3], p[6])] + p[8]

def p_conditional_elif_empty(p):
    '''conditional_elif : empty'''
    p[0] = []

def p_conditional_else(p):
    '''conditional_else : ELSE LBRACE statement_list RBRACE'''
    p[0] = [(('bool', True), p[3])]

def p_conditional_else_empty(p):
    '''conditional_else : empty'''
    p[0] = []

def p_r_value(p):
    '''r_value : expr'''
    p[0] = p[1]

def p_l_value_id(p):
    '''l_value : ID'''
    p[0] = ('identifier', p[1])

def p_l_value_record(p):
    '''l_value : ID fields'''
    p[0] = ('record', ('identifier', p[1]), p[2])

def p_l_value_placeholder(p):
    '''l_value : PLACEHOLDER'''
    p[0] = ('placeholder', p[1])

def p_l_value_placeholder_record(p):
    '''l_value : PLACEHOLDER fields'''
    p[0] = ('record', ('placeholder', p[1]), p[2])
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

def p_expr_null(p):
    '''expr : NULL'''
    p[0] = ('null', None)
    
def p_expr_func_call(p):
    '''expr : func_call'''
    p[0] = p[1]

def p_expr_id(p):
    '''expr : ID'''
    p[0] = ('identifier', p[1])

def p_expr_parens(p):
    '''expr : LPAREN expr RPAREN'''
    p[0] = p[2]

def p_expr_anonymous_fun(p):
    '''expr : anonymous_fun'''
    p[0] = p[1]

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
        p[0] = ('subtraction', p[1], p[3])
    if p[2] == '*':
        p[0] = ('multiply', p[1], p[3])
    if p[2] == '/':
        p[0] = ('divide', p[1], p[3])

def p_expr_list(p):
    '''expr : LBRACKET arg_list RBRACKET'''
    p[0] = ('list', { 'data': p[2] })

def p_expr_object(p):
    '''expr : LBRACE record_list RBRACE'''
    p[0] = ('object', make_obj(p[2]))

def p_expr_sequence(p):
    '''expr : LPAREN statement_list RPAREN'''
    p[0] = ('sequence', p[2])

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

def p_expr_comp_op(p):
    '''expr : comp_op'''
    p[0] = p[1]

def p_expr_placeholder(p):
    '''expr : PLACEHOLDER'''
    p[0] = ('placeholder', p[1])

def p_comp_op_eq(p):
    '''comp_op : expr EQUAL EQUAL expr'''
    p[0] = ('eq', p[1], p[4])

def p_comp_op_neq(p):
    '''comp_op : expr BANG EQUAL expr'''
    p[0] = ('neq', p[1], p[4])

def p_comp_op_gt(p):
    '''comp_op : expr GT expr'''
    p[0] = ('gt', p[1], p[3])
    
def p_comp_op_gte(p):
    '''comp_op : expr GT EQUAL expr'''
    p[0] = ('gte', p[1], p[4])

def p_comp_op_lt(p):
    '''comp_op : expr LT expr'''
    p[0] = ('lt', p[1], p[3])

def p_comp_op_lte(p):
    '''comp_op : expr LT EQUAL expr'''
    p[0] = ('lte', p[1], p[4])

def p_expr_log_op(p):
    '''expr : log_op'''
    p[0] = p[1]

def p_log_op_and(p):
    '''log_op : expr AND expr'''
    p[0] = ('and', p[1], p[3])

def p_log_op_or(p):
    '''log_op : expr OR expr'''
    p[0] = ('or', p[1], p[3])

def p_log_op_not(p):
    '''log_op : NOT expr'''
    p[0] = ('not', p[2])

def p_macro_def(p):
    '''macro_def : MAC macro_def_arg_list LBRACE statement_list RBRACE'''
    p[0] = ('macro_def', p[2], p[4])

def p_macro_def_arg_list_start_atom(p):
    '''macro_def_arg_list : ATOM macro_def_arg_list_rec'''
    p[0] = [('atom', p[1])] + p[2]

def p_macro_def_arg_list_rec_placeholder(p):
    '''macro_def_arg_list_rec : PLACEHOLDER macro_def_arg_list_rec'''
    p[0] = [('placeholder', p[1])] + p[2]

def p_macro_def_arg_list_rec_atom(p):
    '''macro_def_arg_list_rec : ATOM macro_def_arg_list_rec'''
    p[0] = [('atom', p[1])] + p[2]

def p_macro_def_arg_list_rec_empty(p):
    '''macro_def_arg_list_rec : empty'''
    p[0] = []

def p_macro_call_atom_start(p):
    '''macro_call : ATOM macro_arg_list SEMICOLON'''
    p[0] = ('macro_call', [('atom', p[1])] + p[2])

def p_macro_call_arg_list_atom(p):
    '''macro_arg_list : ATOM macro_arg_list'''
    p[0] = [('atom', p[1])] + p[2]

def p_macro_call_arg_list_expr(p):
    '''macro_arg_list : expr macro_arg_list'''
    p[0] = [p[1]] + p[2]

def p_macro_call_arg_list_empty(p):
    '''macro_arg_list : empty'''
    p[0] = []

def p_anonymous_fun(p):
    '''anonymous_fun : LPAREN id_list RPAREN LBRACE statement_list RBRACE'''
    p[0] = ('fun', p[2], p[5])

def p_error(p):
    raise ParserError('Syntax error', p)

def parse(file_name):
    with open(file_name, 'r') as f:
        file_content = f.read()
        lexer = new_lexer()
        parser = yacc.yacc()
        try:
            statements = parser.parse(file_content,tracking=True)
        except ParserError as err:
            syntax_error(file_name, err.tok.lineno, err.tok.lexpos)
            print(err.tok.lexpos)
            exit(1)
        return statements
