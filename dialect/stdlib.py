import re
from copy import deepcopy
from .context import Context

def _print(ctx, args):
    from .engine import eval_expr

    def format_str(x):
        if isinstance(x, float) and x.is_integer():
            return str(int(x))
        elif isinstance(x, float):
            return str(x)
        elif isinstance(x, str):
            return x
        elif isinstance(x, bool):
            return 'true' if x else 'false'
        elif x is None:
            return 'null'
        elif isinstance(x, dict):
            key_vals = ['{} : {}'.format(key, x[key]) for key in x]
            return '{{ {} }}'.format(', '.join(key_vals))
        return x

    def minify_list(l):
        l = deepcopy(l)
        mini = [minify_list(el[1]['data']) if el[0] == 'list' else el for el in l]
        mini = [minify_dict(el[1]) if el[0] == 'object' else el for el in mini]
        mini = ['[function]' if el[0] == 'fun' else el for el in mini]
        mini = [format_str(el[1]) if isinstance(el, tuple) else el for el in mini]
        return '[{}]'.format(', '.join(mini))

    def minify_dict(d):
        d = deepcopy(d)
        for key in d:
            if d[key][0] == 'object':
                d[key] = minify_dict(d[key][1])
            elif d[key][0] == 'list':
                d[key] = minify_list(d[key][1])
            elif d[key][0] == 'number' and d[key][1].is_integer():
                d[key] = int(d[key][1])
            elif d[key][0] == 'fun':
                d[key] = '[function]'
            else:
                d[key] = d[key][1]
        return format_str(d)
                
    print(eval_expr(ctx, args[0]))
    evaluated_args = [eval_expr(ctx, arg)[1] if eval_expr(ctx, arg)[0] != 'list' and eval_expr(ctx, arg)[0] != 'fun' else eval_expr(ctx, arg)[1]['data'] if eval_expr(ctx, arg)[0] != 'fun' else eval_expr(ctx, arg) for arg in args]
    evaluated_args = [(minify_list(arg),) if isinstance(arg, list) else arg for arg in evaluated_args]
    evaluated_args = [(minify_dict(arg),) if isinstance(arg, dict) else arg for arg in evaluated_args]
    evaluated_args = ['[function]' if isinstance(arg, tuple) and arg[0] == 'fun' else arg for arg in evaluated_args]
    evaluated_args = [format_str(arg) if not isinstance(arg, tuple) else arg[0] for arg in evaluated_args]
    print(' '.join(evaluated_args))
        

def run_sequence(ctx, args):
    from .engine import eval, eval_expr
    sequence = args[0]
    if sequence[0] != 'sequence':
        sequence = eval_expr(ctx, sequence)
    return eval(ctx, sequence[1])

def length(ctx, args):
    from .engine import eval_expr
    expr = eval_expr(ctx, args[0])
    if expr[0] == 'list':
        return ('number', float(len(expr[1]['data'])))
    return ('number', float(len(expr[1])))

def _type(ctx, args):
    from .engine import eval_expr
    expr = eval_expr(ctx, args[0])
    return ('string', expr[0])

def _copy(ctx, args):
    from .engine import eval_expr
    expr = eval_expr(ctx, args[0])
    return deepcopy(expr)

def exists(ctx, args):
    return ctx.check(args[0])

def delete(ctx, args):
    return ctx.delete(args[0])

def keys(ctx, args):
    from .engine import eval_expr
    expr = eval_expr(ctx, args[0])
    obj_keys = [('string', k) for k in list(expr[1].keys())]
    return ('list', { 'data': obj_keys})

def _list(ctx, args):
    from .engine import eval_expr
    expr = eval_expr(ctx, args[0])
    return ('list', { 'data': [('null', None)] * int(expr[1])})

def symbol_to_string(ctx, args):
    return ('string', args[0][1])

def string_to_symbol(ctx, args):
    match = re.match('[a-z_][a-z_0-9]*', args[0][1])
    if match:
        return ('identifier', args[0][1])
    else:
        return ('null', None)

STDLIB = {
    'print': _print,
    'run': run_sequence,
    'length': length,
    'type': _type,
    'copy': _copy,
    'exists': exists,
    'delete': delete,
    'keys': keys,
    'list': _list,
    'symbol_to_string': symbol_to_string,
    'string_to_symbol': string_to_symbol,
}
