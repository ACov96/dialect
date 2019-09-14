from copy import deepcopy
from context import Context

def _print(ctx, args):
    from engine import eval_expr

    def format_str(x):
        if isinstance(x, float) and x.is_integer():
            return str(int(x))
        elif isinstance(x, float):
            return str(x)
        elif isinstance(x, str):
            return '"{}"'.format(x)
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
        mini = [minify_list(el[1]) if el[0] == 'list' else el for el in l]
        mini = [minify_dict(el[1]) if el[0] == 'object' else el for el in mini]
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
            else:
                d[key] = d[key][1]
        return format_str(d)
                

    evaluated_args = [eval_expr(ctx, arg)[1] for arg in args]
    evaluated_args = [(minify_list(arg),) if isinstance(arg, list) else arg for arg in evaluated_args]
    evaluated_args = [(minify_dict(arg),) if isinstance(arg, dict) else arg for arg in evaluated_args]
    evaluated_args = [format_str(arg) if not isinstance(arg, tuple) else arg[0] for arg in evaluated_args]
    print(' '.join(evaluated_args))
        
STDLIB = {
    'print': _print,
}
