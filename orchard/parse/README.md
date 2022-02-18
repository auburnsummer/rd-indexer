This is a modified JSON parser for rdlevels.

Generally speaking, rdlevels are pretty similar to JSON, but with two key differences:

 - newlines do not need to be escaped in strings;

```
{
 "key": "this is a valid
value in an rdlevel
even though it has newlines"
}
```

 - key pairs in objects can be whitespace seperated instead

```
{"key": 2, "key2": 3 "key3": 4}
```


Most code here is auto-generated using ANTLR (see make.sh).

The files that are written by us are:

 - `make.sh`
 - `rdlevel.g4`
 - `myCustomListener.py`
 - `rdlevel.py`
 - `__init__.py`
 - `utils.py`

Everything else is ANTLR-generated.


