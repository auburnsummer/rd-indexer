from orchard.parse.rdlevelListener import rdlevelListener
from orchard.parse.rdlevelParser import rdlevelParser
from orchard.parse.utils import update

from codecs import escape_decode


class MyCustomListener(rdlevelListener):
    def __init__(self):
        self.accum = None
        self.currentPath = []  # indicates root.

    def set(self, value):
        self.accum = update(self.accum, self.currentPath, value)

    def enterEmptyObject(self, ctx: rdlevelParser.EmptyObjectContext):
        self.set({})

    def enterEmptyArray(self, ctx: rdlevelParser.EmptyArrayContext):
        self.set([])

    def enterAnArray(self, ctx: rdlevelParser.AnArrayContext):
        self.set([])
        self.currentPath.append(-1)  # indicator we're in an array.

    def exitAnArray(self, ctx: rdlevelParser.AnArrayContext):
        self.currentPath.pop()

    def enterPair(self, ctx: rdlevelParser.PairContext):
        key = str(ctx.STRING()).strip('"')
        self.currentPath[-1] = key

    def enterAnObject(self, ctx: rdlevelParser.AnObjectContext):
        self.set({})
        self.currentPath.append(
            ""
        )  # current object key. will be replaced in enterPair.

    def exitAnObject(self, ctx: rdlevelParser.AnObjectContext):
        self.currentPath.pop()

    def enterBooleanValue(self, ctx: rdlevelParser.BooleanValueContext):
        value = ctx.getText() == "true"
        self.set(value)

    def enterNumberValue(self, ctx: rdlevelParser.NumberValueContext):
        s = ctx.getText()
        try:
            value = int(s)
        except ValueError:
            value = float(s)
        self.set(value)

    def enterStringValue(self, ctx: rdlevelParser.StringValueContext):
        # strip leading and ending "'s
        s1 = ctx.getText()[1:-1]
        # magical bullshit python function
        s2 = escape_decode(s1.encode('utf-8'))[0].decode('utf-8')
        self.set(s2)

    def enterNullValue(self, ctx: rdlevelParser.NullValueContext):
        self.set(None)

    def get_final_result(self):
        return self.accum
