import os
from context import Context
from macro import Macro
from stdlib import STDLIB
from util import minify_macro_args
from parse import parse

ALG_OPS = {'addition', 'subtraction', 'multiply', 'divide'}
COMP_OPS = {'eq', 'neq', 'gt', 'gte', 'lt', 'lte'}
LOGIC_OPS = {'and', 'or', 'not'}

def eval_file(ctx, path):
    new_path = ctx.__path__ + '/' + path
    ctx = Context(__path__=os.path.dirname(os.path.realpath(new_path)))
    ast = parse(new_path)
    eval(ctx, ast)
    return ctx

def eval(ctx, statements):
    for statement in statements:
        if statement[0] == 'return':
            ret = eval_expr(ctx, statement[1])
            ctx.flag_return(ret)
            return ret
        else:
            eval_statement(ctx, statement)
            if ctx.ret_val is not None:
                ret = ctx.ret_val
                ctx.flag_return(None)
                return ret

def eval_statement(ctx, statement):
    if statement[0] == 'assignment':
        return eval_assignment(ctx, statement)
    elif statement[0] == 'conditional':
        return eval_conditional(ctx, statement)
    elif statement[0] == 'loop':
        return eval_loop(ctx, statement)
    elif statement[0] == 'fun_def':
        return eval_fun_def(ctx, statement)
    elif statement[0] == 'statement_expr':
        return eval_expr(ctx, statement[1])
    elif statement[0] == 'macro_def':
        return eval_macro_def(ctx, (statement[1], statement[2]))
    elif statement[0] == 'macro_call':
        return eval_macro_call(ctx, statement[1])
    elif statement[0] == 'import':
        return eval_import(ctx, statement[1])

def eval_assignment(ctx, assignment):
    data = eval_expr(ctx, assignment[2])
    if assignment[1][0] == 'identifier':
        ctx.set(assignment[1], data)
    elif assignment[1][0] == 'record':
        all_fields = [eval_expr(ctx, arg)[1] for arg in assignment[1][2]]
        def _recreate(cur_target, fields):
            if len(fields) == 1:
                if cur_target[0] == 'list':
                    cur_target[1]['data'][int(fields[0])] = data
                else:
                    cur_target[1][fields[0]] = data
            else:
                if cur_target[0] == 'list':
                    cur_target[1]['data'][int(fields[0])] = _recreate(cur_target[1]['data'][int(fields[0])], fields[1:])
                else:
                    cur_target[1][fields[0]] = _recreate(cur_target[1][fields[0]], fields[1:])
            return cur_target
        ctx.set(assignment[1][1], _recreate(ctx.get(assignment[1][1][1]), all_fields))

def eval_expr(ctx, expr):
    # print('EVALUATING EXPRESSION', expr)
    if expr[0] == 'string':
        return expr
    elif expr[0] == 'number':
        return expr
    elif expr[0] == 'list':
        return ('list', { 'data': [eval_expr(ctx, el) for el in expr[1]['data']] })
    elif expr[0] == 'object':
        return ('object', init_obj_fields(ctx, expr[1]))
    elif expr[0] == 'func_call':
        return eval_func_call(ctx, expr)
    elif expr[0] == 'identifier':
        return eval_expr(ctx, ctx.get(expr[1]))
    elif expr[0] == 'bool':
        return expr
    elif expr[0] == 'null':
        return expr
    elif expr[0] == 'fun':
        return expr
    elif expr[0] == 'access':
        return eval_access(ctx, expr)
    elif expr[0] == 'sequence':
        return expr
    elif expr[0] in ALG_OPS:
        return eval_alg_op(ctx, expr)
    elif expr[0] in COMP_OPS:
        return eval_comp_op(ctx, expr)
    elif expr[0] in LOGIC_OPS:
        return eval_logic_op(ctx, expr)

def eval_access(ctx, expr):
    target = eval_expr(ctx, expr[1])
    key = eval_expr(ctx, expr[2])
    if target[0] == 'list':
        target = target[1]['data']
        key = int(key[1])
    else:
        target = target[1]
        key = key[1]
    return target[key]
    
def eval_func_call(ctx, expr):
    if expr[1] in STDLIB:
        return STDLIB[expr[1]](ctx, expr[2])
    else:
        new_ctx = Context(parent=ctx)
        _, fun_id, args = expr
        fun = ctx.get(fun_id)
        _, targets, body = fun
        args = [eval_expr(ctx, arg) for arg in args]
        if len(targets) > len(args):
            args += [('null', None)] * (len(targets) - len(args))
        for target, arg in zip(targets, args):
            new_ctx.set(('identifier', target), arg)
        ret = eval(new_ctx, body)
        return ret

def init_obj_fields(ctx, obj):
    for key in obj:
        obj[key] = eval_expr(ctx, obj[key])
    return obj

def eval_conditional(ctx, conditional):
    evaluated = False
    statements = conditional[1]
    for condition, branch in statements:
        condition = eval_expr(ctx, condition)
        if condition[1]:
            return eval(ctx, branch)

def eval_loop(ctx, loop):
    condition = loop[1]
    statements = loop[2]
    while eval_expr(ctx, condition)[1]:
        eval(ctx, statements)
        if ctx.ret_val is not None:
            ret = ctx.ret_val
            ctx.flag_return(None)
            return ret

def eval_fun_def(ctx, definition):
    _, fun_id, args, body = definition
    eval_assignment(ctx, ('assignment', ('identifier', fun_id), ('fun', args, body)))

def eval_alg_op(ctx, expr):
    left = eval_expr(ctx, expr[1])[1]
    right = eval_expr(ctx, expr[2])[1]
    if expr[0] == 'addition':
        data = left + right
    elif expr[0] == 'subtraction':
        data = left - right
    elif expr[0] == 'multiply':
        data = left * right
    elif expr[0] == 'divide':
        data = left / right
    
    if isinstance(data, str):
        return ('string', data)
    elif isinstance(data, float):
        return ('number', data)
    else:
        return ('null', None)

def eval_comp_op(ctx, expr):
    left = eval_expr(ctx, expr[1])[1]
    right = eval_expr(ctx, expr[2])[1]
    if expr[0] == 'eq':
        data = left == right
    elif expr[0] == 'neq':
        data = left != right
    elif expr[0] == 'gt':
        data = left > right
    elif expr[0] == 'lt':
        data = left < right
    elif expr[0] == 'gte':
        data = left >= right
    elif expr[0] == 'lte':
        data = left <= right
    return ('bool', data)

def eval_logic_op(ctx, expr):
    if expr[0] == 'and':
        return ('bool', eval_expr(ctx, expr[1]) and eval_expr(ctx, expr[2]))
    elif expr[0] == 'or':
        return ('bool', eval_expr(ctx, expr[1]) or eval_expr(ctx, expr[2]))
    else:
        return ('bool', not eval_expr(ctx, expr[1])[1])

def eval_macro_def(ctx, macro_def):
    args = minify_macro_args(macro_def[0])
    ctx.macro.register_macro(args, macro_def[1])

def eval_macro_call(ctx, macro_call):
    call = minify_macro_args(macro_call)
    if ctx.macro.has_macro(call):
        statements = ctx.macro.render_statements(call)
        return eval(ctx, statements)

def eval_import(ctx, import_statement):
    imported_ctx = eval_file(ctx, import_statement)
    ctx.macro.macros += imported_ctx.macro.macros
    for key in imported_ctx._context:
        ctx.set(('identifier', key), imported_ctx.get(key))
