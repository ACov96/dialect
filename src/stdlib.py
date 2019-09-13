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
        return x

    def minify_list(l):
        mini = [minify_list(el[1]) if el[0] == 'list' else format_str(el[1]) for el in l]
        return '[{}]'.format(', '.join(mini))

    evaluated_args = [eval_expr(ctx, arg)[1] for arg in args]
    evaluated_args = [minify_list(arg) if isinstance(arg, list) else format_str(arg) for arg in evaluated_args]
    print(' '.join(evaluated_args))
        
STDLIB = {
    'print': _print,
}
