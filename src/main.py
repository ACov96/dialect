import sys
import pprint
from parse import parse
from engine import Context, eval

def main(argv):
    ast = parse(argv[0])
    ctx = Context()
    eval(ctx, ast)
    print(ctx._context)

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('Missing file')
        exit(1)
    main(sys.argv[1:])
