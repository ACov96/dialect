from context import Context
from stdlib import STDLIB

ALG_OPS = {'addition', 'subtraction', 'multiply', 'divide'}
COMP_OPS = {'eq', 'neq', 'gt', 'gte', 'lt', 'lte'}
LOGIC_OPS = {'and', 'or', 'not'}

def eval(ctx, statements):
    for statement in statements:
        eval_statement(ctx, statement)

def eval_statement(ctx, statement):
    if statement[0] == 'assignment':
        eval_assignment(ctx, statement)
    elif statement[0] == 'conditional':
        eval_conditional(ctx, statement)
    elif statement[0] == 'loop':
        eval_loop(ctx, statement)
    elif statement[0] == 'fun_def':
        eval_fun_def(ctx, statement)
    elif statement[0] == 'statement_expr':
        eval_expr(ctx, statement[1])

def eval_assignment(ctx, assignment):
    if assignment[1][0] == 'identifier':
        ctx.set(assignment[1], eval_expr(ctx, assignment[2]))
    elif assignment[1][0] == 'record':
        target = eval_expr(ctx, assignment[1][1])
        fields = [eval_expr(ctx, field)[1] for field in assignment[1][2]]
        for i in range(len(fields)):
            if i == len(fields) - 1:
                # We are on the last field
                target[1][int(fields[i]) if isinstance(fields[i], float) else fields[i]] = eval_expr(ctx, assignment[2])
            else:
                target = target[1][int(fields[i]) if isinstance(fields[i], float) else fields[i]]
        print('TARGET', target[1], hex(id(target[1])))

def eval_expr(ctx, expr):
    # print('EVALUATING EXPRESSION', expr)
    if expr[0] == 'string':
        return expr
    elif expr[0] == 'number':
        return expr
    elif expr[0] == 'list':
        return ('list', [eval_expr(ctx, el) for el in expr[1]])
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
        target = target[1]
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
        return eval(new_ctx, body)

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
            new_ctx = Context(parent=ctx)
            return eval(new_ctx, branch)

def eval_loop(ctx, loop):
    looping = True
    statements = loop[1]
    new_ctx = Context(parent=ctx)
    while looping:
        for statement in statements:
            if statement[0] == 'break':
                looping = False
            else:
                eval_statement(new_ctx, statement)

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
        return ('bool', not eval_expr(ctx, expr[1]))
