# parse

Rhythm Doctor's JSON dialect has a few pecularities:

**Newlines do not need to be escaped in strings**

```
{
 "key": "this is a valid
value in an rdlevel
even though it has newlines"
}
```

**Objects and arrays can have trailing commas, including the root object**

```
{
 "key": "aewfawefwae",
 "array": [1, 2, 3, 4, 5],
},
```

Key pairs in objects can be seperated by whitespace:

```
{"key": 2, "key2": 3 "key3": 4}
```


# Implementation

This is a modified version of [naya](https://github.com/danielyule/naya) to add the relevant
extra parsing needed.  

