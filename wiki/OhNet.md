---
title: "OhNet"
permalink: "/wiki/OhNet"
redirect_from:
---

{% raw %}
# <span id="ohNet"></span>ohNet

## <span id="What_is_it.3F"></span>What is it?

OpenHome Networking (ohNet) is a modern, cross platform UPnP stack. ohNet includes both a control point and a device stack that can be used together or independently. It runs on Linux, Windows, Mac, iOS and Android. The public APIs are available for the device and control point stacks in C++, C#, Java and C. JavaScript and Python APIs are also provided for the control point stack.

UPnP services are presented as classes with actions appearing as functions and state variables appearing as member variables. These classes are referred to as proxies for users of the control point stack and providers for users of the device stack.

Proxies and Providers are included for all OpenHome and UPnP AV services. If your application uses other services, ohNet includes a tool (ohNetGen) to generate proxies and/or providers from the service XML in any of the supported languages.

Source code is available under a [MIT license](https://opensource.org/licenses/MIT).

## <span id="How_do_I_get_it.3F"></span>How do I get it?

ohNet is available as [source code](https://github.com/openhome/ohNet). Setup a (free) github account then

` git clone git@github.com:openhome/ohNet.git ohnet`

build using

` cd ohnet`  
` make`

There are also [binaries available](https://s3-eu-west-1.amazonaws.com/linn-artifacts-public/index.html#artifacts/ohNet/) for certain popular platforms/architectures.

## <span id="Documentation"></span>Documentation

### <span id="Overview_docs"></span>Overview docs

- [Control Point stack (PDF)](http://builds.openhome.org/releases/ohNet_ControlPointStack.pdf)
- [Device stack (PDF)](http://builds.openhome.org/releases/ohNet_DeviceStack.pdf)

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
