---
title: "OhNet:Developer"
permalink: "/wiki/OhNet:Developer"
redirect_from:
  - "/wiki/Ohnet-Av:Developer"
---

{% raw %}
[What is it?](/wiki/OhNet:What) · [How do I get it?](/wiki/OhNet:How) · [Developers](/wiki/OhNet:Developer)

**ohNet - Developers**

### <span id="Overview_docs"></span>Overview docs

- [Control Point stack (PDF)](http://www.openhome.org/releases/ohNet_ControlPointStack.pdf)
- [Device stack (PDF)](http://www.openhome.org/releases/ohNet_DeviceStack.pdf)

### <span id="API_docs"></span>API docs

- [C++](http://www.openhome.org/build/nightly/docs/CppStd/)
- [C#](http://www.openhome.org/build/nightly/docs/Cs/)
- [Java](http://www.openhome.org/build/nightly/docs/Java/)
- [JavaScript](http://www.openhome.org/build/nightly/docs/Js/)
- [C](http://www.openhome.org/build/nightly/docs/C/)

### <span id="Discussion"></span>Discussion

[Developer forum](http://forums.openhome.org/forumdisplay.php?fid=5)

ohNet is written using C++ with std::string replaced by special buffer classes. These buffer classes allow for more efficient use of memory at the cost of a steeper learning curve. Memory use benefits can be especially pronounced for the Device stack. [API docs](http://www.openhome.org/build/nightly/docs/CppCore/) for this version of the stack are available but the buffer classes are intended for internal use of the library and are as such currently undocumented.
{% endraw %}
