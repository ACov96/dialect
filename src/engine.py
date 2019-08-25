class Context:
    def __init__(self):
        self.parent = None
        self._context = {}

    def get(self, key):
        if key in self._context:
            return self._context[key]
        elif self.parent is not None:
            return self.parent.get(key)
        else:
            return ('error', 'No key %s' % key)

    def set(self, key, value):
        self._context[key] = value

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
    if expr[0] == 'string':
        return expr
    elif expr[0] == 'number':
        return expr
    elif expr[0] == 'func_call':
        print(expr)
