from context import Context

def _print(ctx, args):
    from engine import eval_expr

    def minify_list(l):
        mini = [minify_list(el[1]) if el[0] == 'list' else str(el[1]) for el in l]
        return '[{}]'.format(', '.join(mini))

    evaluated_args = [eval_expr(ctx, arg)[1] for arg in args]
    evaluated_args = [minify_list(arg) if isinstance(arg, list) else str(arg) for arg in evaluated_args]
    print(' '.join(evaluated_args))
        
STDLIB = {
    'print': _print,
}
