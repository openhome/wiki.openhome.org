---
title: "OhNet:What"
permalink: "/wiki/OhNet:What"
redirect_from:
  - "/wiki/OhNet-What"
---

{% raw %}
[What is it?](/wiki/OhNet:What) · [How do I get it?](/wiki/OhNet:How) · [Developers](/wiki/OhNet:Developer)

**ohNet - What is it?** ohNet is a modern, cross platform UPnP stack. ohNet includes both a control point and a device stack that can be used together or independently. It runs on Linux, Windows, Mac, iOS and Android. The public APIs are available for the device and control point stacks in C++, C#, Java, C. There is an JavaScript api for the control point stack.

UPnP services are presented as classes with actions appearing as functions and state variables appearing as member variables. These classes are referred to as proxies for users of the control point stack and providers for users of the device stack.

Proxies and Providers are included for all OpenHome and UPnP AV services. If your application uses other services, ohNet includes a tool (ohNetGen) to generate proxies and/or providers from the service XML in any of the supported languages.

Source code is available under a Simplified BSD license.
{% endraw %}
