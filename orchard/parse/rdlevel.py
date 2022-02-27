import sys
from antlr4 import *
from orchard.parse.rdlevelLexer import rdlevelLexer
from orchard.parse.rdlevelParser import rdlevelParser
from orchard.parse.myCustomListener import MyCustomListener

from pprint import pprint


def parse(s):
    input_stream = InputStream(s)
    lexer = rdlevelLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = rdlevelParser(stream)
    tree = parser.json()
    listener = MyCustomListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    return listener.get_final_result()


def main(argv):
    with open(argv[1], "r", encoding="utf-8-sig") as f:
        pprint(parse(f.read()))


if __name__ == "__main__":
    main(sys.argv)
