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

In addition, for about 2 versions of Rhythm Doctor from circa 2018, key pairs in objects
could be seperated via whitespace:

```
{"key": 2, "key2": 3 "key3": 4}
```

There are very few levels that were made in these versions so I'm not supporting this.

# Implementation

This is a modified version of [naya](https://github.com/danielyule/naya) to add the relevant
extra parsing needed.  

