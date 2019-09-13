from stdlib import STDLIB

def eval(ctx, statements):
    for statement in statements:
        eval_statement(ctx, statement)
            
def eval_statement(ctx, statement):
    if statement[0] == 'assignment':
        eval_assignment(ctx, statement)
    elif statement[0] == 'statement_expr':
        eval_expr(ctx, statement[1])

def eval_assignment(ctx, assignment):
    ctx.set(assignment[1], eval_expr(ctx, assignment[2]))

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
    elif expr[0] == 'access':
        return eval_access(ctx, expr)

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

def init_obj_fields(ctx, obj):
    for key in obj:
        obj[key] = eval_expr(ctx, obj[key])
    return obj
