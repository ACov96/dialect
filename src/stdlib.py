from context import Context

def _print(ctx, args):
    from engine import eval_expr

    def minify_list(l):
        return str([minify_list(el) if type(el) == 'list' else el for el in l])
    evaluated_args = [eval_expr(ctx, arg)[1] for arg in args]
    evaluated_args = [minify_list(arg) if type(arg) == 'list' else arg for arg in evaluated_args]
    print(evaluated_args)
    print(' '.join(evaluated_args))
        
STDLIB = {
    'print': _print,
}
