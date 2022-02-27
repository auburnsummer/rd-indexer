# Generated from rdlevel.g4 by ANTLR 4.9.3
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys

if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\16")
        buf.write("D\4\2\t\2\4\3\t\3\4\4\t\4\4\5\t\5\4\6\t\6\3\2\3\2\3\3")
        buf.write("\3\3\3\3\5\3\22\n\3\3\3\7\3\25\n\3\f\3\16\3\30\13\3\3")
        buf.write("\3\5\3\33\n\3\3\3\3\3\3\3\3\3\5\3!\n\3\3\4\3\4\3\4\3\4")
        buf.write("\3\5\3\5\3\5\5\5*\n\5\3\5\7\5-\n\5\f\5\16\5\60\13\5\3")
        buf.write("\5\5\5\63\n\5\3\5\3\5\3\5\3\5\5\59\n\5\3\6\3\6\3\6\3\6")
        buf.write("\3\6\3\6\3\6\5\6B\n\6\3\6\2\2\7\2\4\6\b\n\2\2\2L\2\f\3")
        buf.write('\2\2\2\4 \3\2\2\2\6"\3\2\2\2\b8\3\2\2\2\nA\3\2\2\2\f')
        buf.write("\r\5\n\6\2\r\3\3\2\2\2\16\17\7\3\2\2\17\26\5\6\4\2\20")
        buf.write("\22\7\4\2\2\21\20\3\2\2\2\21\22\3\2\2\2\22\23\3\2\2\2")
        buf.write("\23\25\5\6\4\2\24\21\3\2\2\2\25\30\3\2\2\2\26\24\3\2\2")
        buf.write("\2\26\27\3\2\2\2\27\32\3\2\2\2\30\26\3\2\2\2\31\33\7\4")
        buf.write("\2\2\32\31\3\2\2\2\32\33\3\2\2\2\33\34\3\2\2\2\34\35\7")
        buf.write("\5\2\2\35!\3\2\2\2\36\37\7\3\2\2\37!\7\5\2\2 \16\3\2\2")
        buf.write('\2 \36\3\2\2\2!\5\3\2\2\2"#\7\f\2\2#$\7\6\2\2$%\5\n\6')
        buf.write("\2%\7\3\2\2\2&'\7\7\2\2'.\5\n\6\2(*\7\4\2\2)(\3\2\2")
        buf.write("\2)*\3\2\2\2*+\3\2\2\2+-\5\n\6\2,)\3\2\2\2-\60\3\2\2\2")
        buf.write(".,\3\2\2\2./\3\2\2\2/\62\3\2\2\2\60.\3\2\2\2\61\63\7\4")
        buf.write("\2\2\62\61\3\2\2\2\62\63\3\2\2\2\63\64\3\2\2\2\64\65\7")
        buf.write("\b\2\2\659\3\2\2\2\66\67\7\7\2\2\679\7\b\2\28&\3\2\2\2")
        buf.write("8\66\3\2\2\29\t\3\2\2\2:B\7\f\2\2;B\7\r\2\2<B\5\4\3\2")
        buf.write("=B\5\b\5\2>B\7\t\2\2?B\7\n\2\2@B\7\13\2\2A:\3\2\2\2A;")
        buf.write("\3\2\2\2A<\3\2\2\2A=\3\2\2\2A>\3\2\2\2A?\3\2\2\2A@\3\2")
        buf.write("\2\2B\13\3\2\2\2\13\21\26\32 ).\628A")
        return buf.getvalue()


class rdlevelParser(Parser):

    grammarFileName = "rdlevel.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [DFA(ds, i) for i, ds in enumerate(atn.decisionToState)]

    sharedContextCache = PredictionContextCache()

    literalNames = [
        "<INVALID>",
        "'{'",
        "','",
        "'}'",
        "':'",
        "'['",
        "']'",
        "'true'",
        "'false'",
        "'null'",
    ]

    symbolicNames = [
        "<INVALID>",
        "<INVALID>",
        "<INVALID>",
        "<INVALID>",
        "<INVALID>",
        "<INVALID>",
        "<INVALID>",
        "<INVALID>",
        "<INVALID>",
        "<INVALID>",
        "STRING",
        "NUMBER",
        "WS",
    ]

    RULE_json = 0
    RULE_obj = 1
    RULE_pair = 2
    RULE_arr = 3
    RULE_value = 4

    ruleNames = ["json", "obj", "pair", "arr", "value"]

    EOF = Token.EOF
    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    STRING = 10
    NUMBER = 11
    WS = 12

    def __init__(self, input: TokenStream, output: TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.3")
        self._interp = ParserATNSimulator(
            self, self.atn, self.decisionsToDFA, self.sharedContextCache
        )
        self._predicates = None

    class JsonContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(
            self, parser, parent: ParserRuleContext = None, invokingState: int = -1
        ):
            super().__init__(parent, invokingState)
            self.parser = parser

        def value(self):
            return self.getTypedRuleContext(rdlevelParser.ValueContext, 0)

        def getRuleIndex(self):
            return rdlevelParser.RULE_json

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterJson"):
                listener.enterJson(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitJson"):
                listener.exitJson(self)

    def json(self):

        localctx = rdlevelParser.JsonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_json)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ObjContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(
            self, parser, parent: ParserRuleContext = None, invokingState: int = -1
        ):
            super().__init__(parent, invokingState)
            self.parser = parser

        def getRuleIndex(self):
            return rdlevelParser.RULE_obj

        def copyFrom(self, ctx: ParserRuleContext):
            super().copyFrom(ctx)

    class AnObjectContext(ObjContext):
        def __init__(
            self, parser, ctx: ParserRuleContext
        ):  # actually a rdlevelParser.ObjContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def pair(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(rdlevelParser.PairContext)
            else:
                return self.getTypedRuleContext(rdlevelParser.PairContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterAnObject"):
                listener.enterAnObject(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitAnObject"):
                listener.exitAnObject(self)

    class EmptyObjectContext(ObjContext):
        def __init__(
            self, parser, ctx: ParserRuleContext
        ):  # actually a rdlevelParser.ObjContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterEmptyObject"):
                listener.enterEmptyObject(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitEmptyObject"):
                listener.exitEmptyObject(self)

    def obj(self):

        localctx = rdlevelParser.ObjContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_obj)
        self._la = 0  # Token type
        try:
            self.state = 30
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 3, self._ctx)
            if la_ == 1:
                localctx = rdlevelParser.AnObjectContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 12
                self.match(rdlevelParser.T__0)
                self.state = 13
                self.pair()
                self.state = 20
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 1, self._ctx)
                while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 15
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == rdlevelParser.T__1:
                            self.state = 14
                            self.match(rdlevelParser.T__1)

                        self.state = 17
                        self.pair()
                    self.state = 22
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input, 1, self._ctx)

                self.state = 24
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == rdlevelParser.T__1:
                    self.state = 23
                    self.match(rdlevelParser.T__1)

                self.state = 26
                self.match(rdlevelParser.T__2)
                pass

            elif la_ == 2:
                localctx = rdlevelParser.EmptyObjectContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 28
                self.match(rdlevelParser.T__0)
                self.state = 29
                self.match(rdlevelParser.T__2)
                pass

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class PairContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(
            self, parser, parent: ParserRuleContext = None, invokingState: int = -1
        ):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(rdlevelParser.STRING, 0)

        def value(self):
            return self.getTypedRuleContext(rdlevelParser.ValueContext, 0)

        def getRuleIndex(self):
            return rdlevelParser.RULE_pair

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterPair"):
                listener.enterPair(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitPair"):
                listener.exitPair(self)

    def pair(self):

        localctx = rdlevelParser.PairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_pair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 32
            self.match(rdlevelParser.STRING)
            self.state = 33
            self.match(rdlevelParser.T__3)
            self.state = 34
            self.value()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ArrContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(
            self, parser, parent: ParserRuleContext = None, invokingState: int = -1
        ):
            super().__init__(parent, invokingState)
            self.parser = parser

        def getRuleIndex(self):
            return rdlevelParser.RULE_arr

        def copyFrom(self, ctx: ParserRuleContext):
            super().copyFrom(ctx)

    class EmptyArrayContext(ArrContext):
        def __init__(
            self, parser, ctx: ParserRuleContext
        ):  # actually a rdlevelParser.ArrContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterEmptyArray"):
                listener.enterEmptyArray(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitEmptyArray"):
                listener.exitEmptyArray(self)

    class AnArrayContext(ArrContext):
        def __init__(
            self, parser, ctx: ParserRuleContext
        ):  # actually a rdlevelParser.ArrContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def value(self, i: int = None):
            if i is None:
                return self.getTypedRuleContexts(rdlevelParser.ValueContext)
            else:
                return self.getTypedRuleContext(rdlevelParser.ValueContext, i)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterAnArray"):
                listener.enterAnArray(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitAnArray"):
                listener.exitAnArray(self)

    def arr(self):

        localctx = rdlevelParser.ArrContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_arr)
        self._la = 0  # Token type
        try:
            self.state = 54
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input, 7, self._ctx)
            if la_ == 1:
                localctx = rdlevelParser.AnArrayContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 36
                self.match(rdlevelParser.T__4)
                self.state = 37
                self.value()
                self.state = 44
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input, 5, self._ctx)
                while _alt != 2 and _alt != ATN.INVALID_ALT_NUMBER:
                    if _alt == 1:
                        self.state = 39
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la == rdlevelParser.T__1:
                            self.state = 38
                            self.match(rdlevelParser.T__1)

                        self.state = 41
                        self.value()
                    self.state = 46
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input, 5, self._ctx)

                self.state = 48
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la == rdlevelParser.T__1:
                    self.state = 47
                    self.match(rdlevelParser.T__1)

                self.state = 50
                self.match(rdlevelParser.T__5)
                pass

            elif la_ == 2:
                localctx = rdlevelParser.EmptyArrayContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 52
                self.match(rdlevelParser.T__4)
                self.state = 53
                self.match(rdlevelParser.T__5)
                pass

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    class ValueContext(ParserRuleContext):
        __slots__ = "parser"

        def __init__(
            self, parser, parent: ParserRuleContext = None, invokingState: int = -1
        ):
            super().__init__(parent, invokingState)
            self.parser = parser

        def getRuleIndex(self):
            return rdlevelParser.RULE_value

        def copyFrom(self, ctx: ParserRuleContext):
            super().copyFrom(ctx)

    class ObjectValueContext(ValueContext):
        def __init__(
            self, parser, ctx: ParserRuleContext
        ):  # actually a rdlevelParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def obj(self):
            return self.getTypedRuleContext(rdlevelParser.ObjContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterObjectValue"):
                listener.enterObjectValue(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitObjectValue"):
                listener.exitObjectValue(self)

    class NullValueContext(ValueContext):
        def __init__(
            self, parser, ctx: ParserRuleContext
        ):  # actually a rdlevelParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterNullValue"):
                listener.enterNullValue(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitNullValue"):
                listener.exitNullValue(self)

    class NumberValueContext(ValueContext):
        def __init__(
            self, parser, ctx: ParserRuleContext
        ):  # actually a rdlevelParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NUMBER(self):
            return self.getToken(rdlevelParser.NUMBER, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterNumberValue"):
                listener.enterNumberValue(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitNumberValue"):
                listener.exitNumberValue(self)

    class BooleanValueContext(ValueContext):
        def __init__(
            self, parser, ctx: ParserRuleContext
        ):  # actually a rdlevelParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterBooleanValue"):
                listener.enterBooleanValue(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitBooleanValue"):
                listener.exitBooleanValue(self)

    class StringValueContext(ValueContext):
        def __init__(
            self, parser, ctx: ParserRuleContext
        ):  # actually a rdlevelParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(rdlevelParser.STRING, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterStringValue"):
                listener.enterStringValue(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitStringValue"):
                listener.exitStringValue(self)

    class ArrayValueContext(ValueContext):
        def __init__(
            self, parser, ctx: ParserRuleContext
        ):  # actually a rdlevelParser.ValueContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def arr(self):
            return self.getTypedRuleContext(rdlevelParser.ArrContext, 0)

        def enterRule(self, listener: ParseTreeListener):
            if hasattr(listener, "enterArrayValue"):
                listener.enterArrayValue(self)

        def exitRule(self, listener: ParseTreeListener):
            if hasattr(listener, "exitArrayValue"):
                listener.exitArrayValue(self)

    def value(self):

        localctx = rdlevelParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_value)
        try:
            self.state = 63
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [rdlevelParser.STRING]:
                localctx = rdlevelParser.StringValueContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 56
                self.match(rdlevelParser.STRING)
                pass
            elif token in [rdlevelParser.NUMBER]:
                localctx = rdlevelParser.NumberValueContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 57
                self.match(rdlevelParser.NUMBER)
                pass
            elif token in [rdlevelParser.T__0]:
                localctx = rdlevelParser.ObjectValueContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 58
                self.obj()
                pass
            elif token in [rdlevelParser.T__4]:
                localctx = rdlevelParser.ArrayValueContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 59
                self.arr()
                pass
            elif token in [rdlevelParser.T__6]:
                localctx = rdlevelParser.BooleanValueContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 60
                self.match(rdlevelParser.T__6)
                pass
            elif token in [rdlevelParser.T__7]:
                localctx = rdlevelParser.BooleanValueContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 61
                self.match(rdlevelParser.T__7)
                pass
            elif token in [rdlevelParser.T__8]:
                localctx = rdlevelParser.NullValueContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 62
                self.match(rdlevelParser.T__8)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
