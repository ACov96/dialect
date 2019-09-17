import sys
import os
from pprint import pprint
from parse import parse
from engine import eval
from context import Context

def main(argv):
    ast = parse(argv[0])
    # print(ast)
    dir_path = os.path.dirname(os.path.realpath(argv[0]))
    ctx = Context(__path__=dir_path)
    eval(ctx, ast)
    # pprint(ctx._context)
    # x = ctx._context['l'][1]
    # print(x, hex(id(x)))
    # pprint(hex(id(ctx._context['l'][1][2][1][0])))

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('Missing file')
        exit(1)
    main(sys.argv[1:])
