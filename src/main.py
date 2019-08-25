import sys
import pprint
from parse import parse

def main(argv):
    ast = parse(argv[0])
    pprint.pprint(ast)

if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print('Missing file')
        exit(1)
    main(sys.argv[1:])
