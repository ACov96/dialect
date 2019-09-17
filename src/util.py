def make_obj(tuples):
    obj = {}
    for key, val in tuples:
        obj[key] = val
    return obj

def minify_macro_args(args):
    if len(args) == 1:
        return [args[0]]
    rest = minify_macro_args(args[1:])
    first, second = args[0], rest[0]
    if first[0] == 'atom' and second[0] == 'atom':
        return [('atom', '{} {}'.format(first[1], second[1]))] + rest[1:]
    return args
