
/** Taken from "The Definitive ANTLR 4 Reference" by Terence Parr */

// Derived from http://json.org
grammar rdlevel;

json
   : value
   ;

// allow trailing comma, and commas between pairs are optional.
obj
   : '{' pair (','? pair)* ','? '}'  # AnObject
   | '{' '}'                   # EmptyObject
   ;

pair
   : STRING ':' value         
   ;

// same as object.
arr
   : '[' value (','? value)* ','? ']'  #AnArray
   | '[' ']'                     #EmptyArray
   ;

value
   : STRING    # StringValue
   | NUMBER    # NumberValue
   | obj       # ObjectValue
   | arr       # ArrayValue
   | 'true'    # BooleanValue
   | 'false'   # BooleanValue
   | 'null'    # NullValue
   ;

// allow non-escaped whitespace.
STRING
   : '"' (ESC | SAFECODEPOINT | WS)* '"'
   ;


fragment ESC
   : '\\' (["\\/bfnrt] | UNICODE)
   ;
fragment UNICODE
   : 'u' HEX HEX HEX HEX
   ;
fragment HEX
   : [0-9a-fA-F]
   ;
fragment SAFECODEPOINT
   : ~ ["\\\u0000-\u001F]
   ;


NUMBER
   : '-'? INT ('.' [0-9] +)? EXP?
   ;


fragment INT
   : '0' | [1-9] [0-9]*
   ;

// no leading zeros

fragment EXP
   : [Ee] [+\-]? INT
   ;

// \- since - means "range" inside [...]

WS
   : [ \t\n\r] + -> skip
   ;