---
title: "Developer:IdArray"
permalink: "/wiki/Developer:IdArray"
redirect_from:
---

{% raw %}
An `IdArray` is an array of 32 bit, big endian unsigned integers. Each Id typically represents a track. An empty `IdArray` indicates an rray with no elements i.e. no tracks are available.

For example the `IdArray` of:

``` cpp
0x00 0x00 0x00 0x02 0x00 0x00 0x01 0x14 0x00 0x00 0x00 0x13
```

contains 3 ids with the values of 2, 276, and 19 in that order.
{% endraw %}
