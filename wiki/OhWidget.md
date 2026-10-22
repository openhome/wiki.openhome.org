---
title: "OhWidget"
permalink: "/wiki/OhWidget"
redirect_from:
---

{% raw %}
# <span id="ohWidget"></span>ohWidget

## <span id="What_is_it.3F"></span>What is it?

ohWidget is a home control app which runs on [ohOs](/wiki/OhOs).

It makes it simple get a basic widget, for example a light, thermostat or even a washing machine onto the network, share its data, and make available a graphical user interface representation for its control.

The ohWidget Graphical User Interface framework provides a rich overview of all connected devices in the home, agnostic of their chosen communications protocol. The specific user interface for various widget types is auto-generated. It also presents the user with a number of key features such as;

- Scheduler - set a specific day or time for when a widget needs to change state.

<!-- -->

- Presets/Scenes - group widgets together so their collective state change can be invoked by 1 button press.

<!-- -->

- Triggers - The action of 1 widget invokes an action on 1 or many another widgets.

ohWidget also makes it simple for other apps (external widgets) to plug in to this framework, share their information, and present their UI.

## <span id="How_do_I_get_it.3F"></span>How do I get it?

ohWidget will be available for download soon from [GitHub](https://github.com/Openhome).

For any immediate requirement contact info@openhome.org

## <span id="Documentation"></span>Documentation

### <span id="Overview"></span>Overview

[ohWidget Technical Overview](/wiki/OhWidget_Technical_Overview)

[ohWidget Driver Development](/wiki/OhWidget_Driver_Development)

[ohWidget Service XML Definition](/wiki/OhWidget_Service_XML_Definition)

[ohWidget External Widget Application Development](/wiki/External_Widget_Application_Development) - coming soon

## <span id="Utilities"></span>Utilities

### <span id="ohWidget_Workbench"></span>ohWidget Workbench

ohWidget Workbench is a useful development tool. It allows a widget to be modelled and then appear on a network "virtually". This means any connected control point can see the user interface and observe any change in state reflected in the widget instance running in widget workbench. This saves developers from having to wait until a new physical widget is created before developing and testing the widget driver. ohWidget Workbench can be downloaded from here.
{% endraw %}
