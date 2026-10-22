---
title: "Av:Developer:IdArray"
permalink: "/wiki/Av:Developer:IdArray"
redirect_from:
---

{% raw %}
# <span id="IdArray"></span>IdArray

Various services require the ability to return a collection of track identifiers. This is achieved using an IdArray.

An IdArray represents an array of big endian 32-bit unsigned integers. For example,

    0x00 0x00 0x00 0x02 0x00 0x00 0x01 0x03 0x00 0x00 0x00 0x13

represents 3 tracks with the id's 2, 259, and 19 in that order.

Since UPnP has no native collection types, an IdArray has binary type in UPnP services.
{% endraw %}
