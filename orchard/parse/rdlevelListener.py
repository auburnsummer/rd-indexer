# Generated from rdlevel.g4 by ANTLR 4.9.3
from antlr4 import *

if __name__ is not None and "." in __name__:
    from .rdlevelParser import rdlevelParser
else:
    from rdlevelParser import rdlevelParser

# This class defines a complete listener for a parse tree produced by rdlevelParser.
class rdlevelListener(ParseTreeListener):

    # Enter a parse tree produced by rdlevelParser#json.
    def enterJson(self, ctx: rdlevelParser.JsonContext):
        pass

    # Exit a parse tree produced by rdlevelParser#json.
    def exitJson(self, ctx: rdlevelParser.JsonContext):
        pass

    # Enter a parse tree produced by rdlevelParser#AnObject.
    def enterAnObject(self, ctx: rdlevelParser.AnObjectContext):
        pass

    # Exit a parse tree produced by rdlevelParser#AnObject.
    def exitAnObject(self, ctx: rdlevelParser.AnObjectContext):
        pass

    # Enter a parse tree produced by rdlevelParser#EmptyObject.
    def enterEmptyObject(self, ctx: rdlevelParser.EmptyObjectContext):
        pass

    # Exit a parse tree produced by rdlevelParser#EmptyObject.
    def exitEmptyObject(self, ctx: rdlevelParser.EmptyObjectContext):
        pass

    # Enter a parse tree produced by rdlevelParser#pair.
    def enterPair(self, ctx: rdlevelParser.PairContext):
        pass

    # Exit a parse tree produced by rdlevelParser#pair.
    def exitPair(self, ctx: rdlevelParser.PairContext):
        pass

    # Enter a parse tree produced by rdlevelParser#AnArray.
    def enterAnArray(self, ctx: rdlevelParser.AnArrayContext):
        pass

    # Exit a parse tree produced by rdlevelParser#AnArray.
    def exitAnArray(self, ctx: rdlevelParser.AnArrayContext):
        pass

    # Enter a parse tree produced by rdlevelParser#EmptyArray.
    def enterEmptyArray(self, ctx: rdlevelParser.EmptyArrayContext):
        pass

    # Exit a parse tree produced by rdlevelParser#EmptyArray.
    def exitEmptyArray(self, ctx: rdlevelParser.EmptyArrayContext):
        pass

    # Enter a parse tree produced by rdlevelParser#StringValue.
    def enterStringValue(self, ctx: rdlevelParser.StringValueContext):
        pass

    # Exit a parse tree produced by rdlevelParser#StringValue.
    def exitStringValue(self, ctx: rdlevelParser.StringValueContext):
        pass

    # Enter a parse tree produced by rdlevelParser#NumberValue.
    def enterNumberValue(self, ctx: rdlevelParser.NumberValueContext):
        pass

    # Exit a parse tree produced by rdlevelParser#NumberValue.
    def exitNumberValue(self, ctx: rdlevelParser.NumberValueContext):
        pass

    # Enter a parse tree produced by rdlevelParser#ObjectValue.
    def enterObjectValue(self, ctx: rdlevelParser.ObjectValueContext):
        pass

    # Exit a parse tree produced by rdlevelParser#ObjectValue.
    def exitObjectValue(self, ctx: rdlevelParser.ObjectValueContext):
        pass

    # Enter a parse tree produced by rdlevelParser#ArrayValue.
    def enterArrayValue(self, ctx: rdlevelParser.ArrayValueContext):
        pass

    # Exit a parse tree produced by rdlevelParser#ArrayValue.
    def exitArrayValue(self, ctx: rdlevelParser.ArrayValueContext):
        pass

    # Enter a parse tree produced by rdlevelParser#BooleanValue.
    def enterBooleanValue(self, ctx: rdlevelParser.BooleanValueContext):
        pass

    # Exit a parse tree produced by rdlevelParser#BooleanValue.
    def exitBooleanValue(self, ctx: rdlevelParser.BooleanValueContext):
        pass

    # Enter a parse tree produced by rdlevelParser#NullValue.
    def enterNullValue(self, ctx: rdlevelParser.NullValueContext):
        pass

    # Exit a parse tree produced by rdlevelParser#NullValue.
    def exitNullValue(self, ctx: rdlevelParser.NullValueContext):
        pass


del rdlevelParser
