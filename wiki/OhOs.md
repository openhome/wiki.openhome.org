---
title: "OhOs"
permalink: "/wiki/OhOs"
redirect_from:
---

{% raw %}
# <span id="ohOS"></span>ohOS

## <span id="What_is_it.3F"></span>What is it?

ohOs is designed to be deployed onto a modern Operating System and hosts a number of applications. Each of these applications can automatically run on any host OS. Deployments are maintained for:

- Windows x86/x64 desktop
- Mac x64 desktop
- Linux x86/x64 desktop
- Linux ARM

Linux ARM allows deployment on a [plug computer](http://en.wikipedia.org/wiki/SheevaPlug). The unobtrusive factor and low power requirements of these devices make them very well suited as the hosts for apps which should always be on.

## <span id="Related_projects"></span>Related projects

### <span id="ohWidget"></span>[ohWidget](/wiki/OhWidget)

ohWidget offers a home control framework which runs as an app on ohOs.

### <span id="ohRemote"></span>[ohRemote](/wiki/OhRemote)

ohRemote provides remote access framework and is installed as an app on ohOs.

## <span id="System_architecture"></span>System architecture

System architecture can be summarised as:

<figure>
<img src="/mediawiki/images/4/47/OhOsOverviewArchDiagram.png" title="System architecture" width="400" alt="ohOsOverviewArchDiagram.png" />
<figcaption>System architecture</figcaption>
</figure>

ohOs hosts a number of applications (apps), each of which is always running. All code in ohOs is managed. This has the benefit of making applications portable across all platforms at no cost to the app developer. All code in ohOs is written in C#. Apps can be written in C# or other managed languages.

Each ohOs app runs in its own process. Communication with the app’s user interface or with other apps occurs using service interface calls over the network. Service interfaces are typically presented as standard classes which internally use [ohNet](/wiki/OhNet) to handle the invocation of a service function or notification of a change in a member variable.

ohOs apps contain a web-based user interface, allowing users to access the apps on any control point without installing extra software. Each app is automatically supplied with a rudimentary web server which delivers the web UI. Apps are not required to generate complex html inside ohOs; instead they serve up JavaScript which uses the services exposed by the app to generate its UI client-side.

Web UIs can use HTML5 features to provide an interface as graphically rich as native apps. While there should be no pressing need to write native control points, ohOs does allow this. In addition to C#, proxies for an app’s services can be generated in C or C++ (suitable for Apple’s iOS) or Java (suitable for Google’s Android).

## <span id="How_do_I_get_it.3F"></span>How do I get it?

ohOs is available as a [binary release](http://www.openhome.org/releases/artifacts/ohOs/) and coming soon to the [OpenHome Github account](https://github.com/Openhome)

## <span id="Docs"></span>Docs

Coming soon.
{% endraw %}
