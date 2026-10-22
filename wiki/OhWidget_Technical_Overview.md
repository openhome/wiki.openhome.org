---
title: "OhWidget Technical Overview"
permalink: "/wiki/OhWidget_Technical_Overview"
redirect_from:
---

{% raw %}
# <span id="Introduction"></span>Introduction

This document provides a technical overview of the [ohWidget](/wiki/OhWidget) home automation system and details about the physical architecture it uses. It introduces the concepts, terminology and interactions of each component of an ohWidget system.

This document does not provide low-level technical information such as hardware specifications of the Nodes nor code examples from the ohWidget API.

## <span id="ohWidget"></span>[ohWidget](/wiki/OhWidget)

[ohWidget](/wiki/OhWidget) makes use of three distinct components: Widgets, Control Points and Nodes. This document uses these three terms heavily throughout and are defined simply as follows:

### <span id="Widget"></span>Widget

Any device in an end-user's home that can be remotely controlled. Widgets can range in complexity from simple single-service lights to multi-service audio/visual devices.

### <span id="Control_Point"></span>Control Point

A device used by the end-user to access the services provided by each Widget.

### <span id="Node"></span>Node

The device used to aggregate devices and services published by Widgets, for quick and easy access by Control Points.

Together these three classes of device can be used in any number to create an [ohWidget](/wiki/OhWidget) home automation system.

## <span id="Node_manufacturer_benefits"></span>Node manufacturer benefits

[ohWidget](/wiki/OhWidget) supports Node manufacturers by:

- providing a protocol-independent framework from which to build the communications hardware most suited to each manufacturer
- removing the tightly coupled nature of Control Points and devices that appears in other home automation systems
- allowing Widget vendors to specify the Widget requirements
- not tying Nodes directly to Widgets, and vice-versa
- providing a customizable user interface design to allow for smart and intuitive user experiences

## <span id="Widget_vendor_benefits"></span>Widget vendor benefits

Widget vendors using [ohWidget](/wiki/OhWidget) benefit from how little the need to do to make their Widgets [ohWidget](/wiki/OhWidget) compatible.

[ohWidget](/wiki/OhWidget) supports Widget vendors by:

- allowing the easy integration of Widgets to a connected home with the addition of a tiny amount of intelligence on the Widget itself, without the necessity for a large-scale redesign of the products
- supporting managed code for driver writing in C# allowing for faster development across multiple hardware implementations
- auto-generating several essential files from one central configuration file
- defining the configuration details of the device in simple XML which is easily created and maintained

## <span id="User_benefits"></span>User benefits

The goal of [ohWidget](/wiki/OhWidget) is to place the user at the center of their own home services by providing them an aggregated view of all the devices in their home, irrespective of the vendor.

[ohWidget](/wiki/OhWidget) puts the focus on the user in their home by:

- giving users complete freedom of choice of which devices are used in their own home
- allowing existing, familiar devices to be used as the Control Point, including a choice from among smartphones and tablet PCs
- providing a system backbone that persists when in the home (removing the Control Point doesn't remove the system)
- providing a minimum set up system for home users by applying the benefits of Universal Plug and Play to all devices, independently of the communications protocol used by each device
- aggregating all Widgets in the home, regardless of vendor or protocol
- providing a truly scalable solution allowing the user to build their own smart home network as they wish

# <span id="Technical_Overview"></span>Technical Overview

A very simple view of an ohWidget connected home is shown in Figure 1 below. One Control Point accesses a single Widget by interacting with the Node:

<figure>
<img src="/mediawiki/images/5/5a/CPNW.jpg" title="Figure 1: An abstract view of a Control Point, Node and Widget using a home network to communicate." width="800" alt="CPNW.jpg" />
<figcaption>Figure 1: An abstract view of a Control Point, Node and Widget using a home network to communicate.</figcaption>
</figure>

Key:

- WAP: Wireless Access Point. A network point allowing the Control Point and Nodes to access the 802.11a/b/g/n protocol.
- PLC: Power Line Communications. Can be used to help extend ethernet connections around the home.
- LEC: Low Energy Communications. The module installed on the Node used to communicate with compatible Widgets. Examples are [6LowPan](http://www.6lowpan.org/), [ZigBee](http://www.zigbee.org/), [Z-wave](http://www.sigmadesigns.com/solutions_subcat.php?id=24) or [Bluetooth LE](http://www.bluetooth.com).
- Home network: A representation of any number of routers, switches and wireless access points in the home. This also includes wired Ethernet connections, indicated in the diagram by the thick lines between the Control Point, Home network and Node.
- Wireless comms: The protocol used by the Node and Widget to communicate with each other.

> **Note**
>
> The Node is shown with a broken line through it to represent the possibility of a second Node being contacted to pass the message on to the Widget. At most a message will travel from Control Point \> Node \> Node \> Widget (this is discussed in more detail in the Node chapter). In this case, the first Node will continue to use ethernet comms (potentially augmented by [PLC](http://en.wikipedia.org/wiki/Power_line_communication)) to contact the second Node, and the second Node will use the LEC protocol to contact the Widget.

An ohWidget network grows with no maintenance burden on the user when new Widgets are introduced. Communication between the Control Point and the Widget is key to ensuring a smart home functions efficiently as possible for users.

The view shown in the diagram above places the emphasis for this scalability and openness on the Node. Nodes treat both Widget and Control Point as abstract concepts and operate, for the most part, independently of the requirements of both. This is what stands ohWidget apart from other smart home systems.

# <span id="Widgets"></span>Widgets

Widgets are any device that offer a service that can be interacted with from a Control Point. The Widget can be as complicated as an integrated audio streaming center or as simple as a light.

To be an ohWidget compatible device, a Widget needs to have the following knowledge about itself:

- State — the current status of the Widget, such as On or Off
- Service — the list of actions and options the Widget offers over the network
- Unique identifier (UID) — the value used to identify the Widget from all others

These details must be present on the Widget. This small requirement means that almost any device can be compatible with ohWidget.

The intelligence and mechanisms required to access and use these details is not stored on the Widget. ohWidget loads the intelligence on the Nodes rather than demand Widget vendors make their Widgets more complicated than they have to be.

## <span id="Classifying_Widgets"></span>Classifying Widgets

Some devices will already be complex in the range of function that they offer, whilst others will remain simple devices offering one or two functions at most. The simpler devices, Widgets, are supported by ohWidget's property list. These devices can have their functionality easily defined within the ohWidget framework, producing both auto-generated code for developers and intuitive user interfaces to present the Widget to the user.

## <span id="Widgets_in_more_detail"></span>Widgets in more detail

A Widget is a simple hardware device such as a light or thermometer. Widgets communicate with the Node using a low-energy communications protocol, such as [Zigbee](http://www.zigbee.org) or [Z-Wave](http://www.z-wave.com/modules/ZwaveStart/). They are controlled using a device- and protocol-specific driver. Widget drivers are installed on the Node and used as required.

For example, two Widgets providing an identical service over the same communications protocol will both use the same copy of the device driver. A new Widget providing the same service as the first two but over a different communications protocol will need a new device driver. A fourth Widget offering a different service, but using the same protocol as the first two, will also need its own device driver.

A more advanced device might not have its full range of functionality supported in the set of ohWidget properties alone. These devices are called External Widgets. Their more complicated functions must be defined externally of the ohWidget properties. However, ohWidget will fully integrate an External Widget definition so that it can be presented seamlessly alongside other Widgets.

<figure>
<img src="/mediawiki/images/d/df/MultipleDriverExplanation.png" title="Figure 2: Four Widgets shown using three drivers installed on the Node" width="800" alt="MultipleDriverExplanation.png" />
<figcaption>Figure 2: Four Widgets shown using three drivers installed on the Node</figcaption>
</figure>

> **Note**
>
> For more information on writing a Widget driver, see the [ohWidget Driver Development](/wiki/OhWidget_Driver_Development) document

If we examine the list of compatibility requirements again, we see that Widgets automatically meet each one:

- State — Widgets will typically offer one state variable that can be changed (such as a light being able to turn on or off), so their state is readily and easily available.
- Service — As above, most Widgets will offer a single service that can be controlled which Widget vendors will write and publish in an XML description file.
- Unique Identifier (UID) — By providing the Widget with a communications protocol (such as a light that communicates over the [Zigbee](http://www.zigbee.org) protocol) you also give it a MAC address. The Widget's MAC address can easily be used as the UID.

> **Note**
>
> Widgets can be provided with a communications protocol either internally by including the protocol hardware in the body of the device itself, or externally by converting the device using a commercially available adapter. Either way, the Widget becomes network accessible and is assigned a MAC address.

Widget vendors are responsible for providing sufficient information about their Widgets in a Widget class driver. The information provided in the driver is written by the Widget vendor and released at the same time as the Widget. This does not mean, however, that it is necessarily packaged with the Widget. Some drivers will be deployed via an automatic download to the Node, or manually installed using a USB stick. This allows any Widget from any vendor to be added to the network (assuming that the Widget and the Node share a compatible communications protocol) and provides instant access to the Widget's services. No IP address or other complex TCP/IP stack requirements are placed on the Widget, keeping it simple and focused on its primary function.

ohWidget allows Widgets to remain:

- low in power consumption
- unhindered by the extra hardware and software expense that would have been required to maintain multiple communications protocols on a single device
- dedicated to providing the service it was designed for

## <span id="External_Widgets_in_more_detail"></span>External Widgets in more detail

An External Widget is a complex hardware or software device that cannot have its controls and interface easily presented as a Widget. An External Widget will typically communicate over a network using TCP/IP, but can also use the same protocols as a Simple Widget (such as [Zigbee](http://www.zigbee.org) or [Z-Wave](http://www.z-wave.com/modules/ZwaveStart/)). External widgets are hosted in separate apps. These apps have the ability of being displayed and controlled through the ohwidget user interface. For more details refer to the [External Widget Application Development](/wiki/External_Widget_Application_Development) document.

## <span id="User_Interface"></span>User Interface

The responsibility for hosting the user interface (UI) to control Widgets is given to the Node. This ensures the Widget remains dedicated to providing the service it was originally designed for. By default, ohWidget will provide a full UI to allow users to control each function available on the Widget.

> **Note**
>
> For more details of UI hosting and Node UI design, see the User interface section in the Nodes chapter.

The Widget vendor must provide the details of how to control each device they manufacture for use in the smart home. This information is provided in the Widget Service XML file which is used to generate the UI.

Each Widget UI provides both a summary and a details view. The summary view allows users quick access to a Widget's single basic function, such as a simple on/off command. The details view provides users access to the full range of functionality that the Widget offers. This allows vendors to be as specific as they like for each Widget they produce.

The summary view is automatically displayed when the Widget has been detected on the network. The UI aggregates all of the available Widgets' summary views into a single list for the user.

The details view can be auto-generated from the information provided in the service XML. Vendors can then customize the look of the details view UI with custom CSS and JavaScript.

ohWidget does not restrict vendors in how they present their Widgets to the end-user. To assist Widget vendors in getting their product integrated into an ohWidget system as quickly and easily as possible, the details view can be generated automatically from the service XML Widget vendors write when releasing a new Widget.

There is a list of supported controls that the auto-generation process generates from the XML into HTML, complete with CSS and associated JavaScript. Any other controls the vendor needs to have displayed can be provided in custom-written HTML alongside the auto-generated content.

> **Note**
>
> The CSS is hosted on the Node and the auto-generated HTML will default to using this. If Widget vendors want to customize the look and feel of their UI they must provide their own custom CSS and ship it along with their HTML.

This operation is carried out at compile time, before the Widget is shipped.

See the [External Widget Application Development](/wiki/External_Widget_Application_Development) document for more information on writing custom details view UIs for External Widgets.

# <span id="Control_Points"></span>Control Points

## <span id="Control_Points_2"></span>Control Points

A Control Point is used by the end-user to control each of the Widgets in their smart home. A Control Point is itself a device, but isn't considered a Widget in the ohWidget system.

The UI provided by ohWidget for Control Points to use is web-based. It is hosted on the Node and developed in two parts by Node manufacturers and Widget vendors, with auto-generation tools and support provided in the ohWidget software to assist this process. ohWidget provides support for the development of native Control Point applications to be developed, but the development of native applications is a manual process. ohWidget provides no auto-generation tools for native Control Point applications.

## <span id="Familiar_Devices"></span>Familiar Devices

A typical Control Point already exists in the modern-day home in the form of:

- tablet PC
- smart phone
- personal computer
- laptop

A typical modern home has at least one of these devices (and in a lot of cases often more than one of each type) readily available to perform the function of Control Point in a smart home.

Users are already comfortable using these devices and ohWidget is designed to leverage that comfort zone and minimize further costs to the user.

This leaves the user free to focus on choosing which Widgets they want to install in their home.

## <span id="Flexible_network_architecture"></span>Flexible network architecture

ohWidget provides a network architecture that allows the relationship between the Control Point and the user's smart home to remain flexible at the hardware level, yet tightly bound at the software level.

Other attempts at home automation use proprietary hardware for the Control Point, loading it with the intelligence needed to run the devices in your home meaning that it must remain in the home as a part of the network solution. In a way, it could be said that in those solutions the Control Point is the smart home network.

ohWidget actively encourages users to use devices they already familiar with as their Control Point. Furthermore, the intelligence of the network is not placed on those devices, but on the Nodes connected to the Widgets. This reduces the learning curve for users, ensures their Widgets are always accessible and opens up the possibility to give users remote access to their home.

Removing the Control Point from the home does not remove the ohWidget network. It persists as long as the Nodes and Widgets remain connected. Devices such as tablet PCs, smart phones and laptop computers are all readily usable as Control Points — both inside and out of the user's home.

> **Important**
>
> Control Point hardware is not delivered as part of the ohWidget home automation system, though the ability to present the services that Widgets provide is.
>
> The model provides a simple Web server to run on the Node which is given the responsibility of serving the user interface to the Control Point.

# <span id="Nodes"></span>Nodes

## <span id="Nodes_2"></span>Nodes

A Node is a device used to bridge communications between a Control Point and the Widgets connected to the network.

The ohWidget software for Nodes is designed to be hardware independent and isn't tied to any particular protocol when communicating with Widgets. The choice of hardware configuration used by Node manufacturers is not defined by OpenHome, and is not constrained by the ohWidget software.

However, the use of the Universal Plug and Play (UPnP) protocol is mandatory for communications between the Nodes. This is built in to the ohWidget software.

OpenHome recommend and support a small form-factor to easily introduce Nodes into the home of the end-user who might not have the technical ability of a modern smart home hobbyist, enthusiast or custom installer. Depending on the manufacturer's choice a Node may take the form of a plugcomputer or something more ubiquitous such as a light wall switch.

## <span id="Self_management"></span>Self management

When several Nodes are introduced to the same network they will negotiate with each other to arrange themselves into a robust network backbone within the home. The network enables Control Points to be able to connect to, and access the services on the Widgets connected to the network.

Each Node maintains a list of the Widgets it controls, called the Widget registry. The Node publishes its Widget registry across the Node network. Every Node on the network aggregates the published Widget registries from other Nodes into one list. This means that every Node knows which is the controlling Node for each Widget on the network.

Interconnected Nodes pass messages from one Node to another ensuring that the Control Point contacts the destination Widget via the correct controlling Node. At maximum the communication path will be no more than Control Point \> presentation Node \> controlling Node \> Widget, with allowances for network routing in between.

> **Note**
>
> The Node contacted after the presentation Node will always be the Node that controls the destination Widget. If the presentation Node is also the controlling Node, the communication path is reduced by one step.

A presentation Node is the Node the Control Point is connected to when accessing the user interface. A Node can only be regarded as a presentation Node when a Control Point is connected to it. Otherwise it is equal in status among the other Nodes.

Nodes are equal in their responsibilities when presenting the UI to a Control Point. Any Node is capable of presenting the UI to a Control Point. A Node may present the UI to any number of Control Points currently connected to it. There is no 1-to-1 mapping of Control Points to presentation Nodes.

### <span id="Widget_aggregator"></span>Widget aggregator

When a Control Point connects to any Node, the full list of available Widgets is immediately available in the UI. Any further filtering or arranging of the Widgets must be handled by the Control Point.

Widgets are registered with the Nodes when they are added to the network. This occurs either automatically using automatic discovery or manually using the pairing mechanism provided by the specific communication protocol. No matter the method, all Widgets are maintained in the same list on the Node so that the Nodes have a single aggregation point to manage the entire list of available Widgets. Giving this function over to the Nodes removes the extra complexity from both the Control Point and the Widgets that would otherwise be required to ensure services are kept available to the end-user.

## <span id="Protocol_independent_Nodes"></span>Protocol independent Nodes

### <span id="Node_to_Node_communication"></span>Node to Node communication

Nodes communicate with each other over Ethernet.

### <span id="Node_to_Widget_communication"></span>Node to Widget communication

It is not expected that Widgets should be stacked with the complex UPnP software and necessary extra hardware to support UPnP communications. Node to Widget communication is expected to use a lighter protocol.

However, OpenHome recognizes the requirement for Widget vendors to select their own protocols for their Widgets, and provides an independent framework to allow the freedom of protocol choice.

#### <span id="Protocol_independent_communication"></span>Protocol independent communication

The hardware limitations implicit in a small form factor Node mean that not every wireless communications protocol can be supported. Attempting to support several standards on a single Node has several consequences, including:

- increasing the manufacturing costs of the Nodes
- power consumption increases with each new piece of hardware added to the Node
- practical issues such as shielding one protocol from another in a single Node

However, minimizing the list of supported protocols by preventing communications by one or more of the available methods is against the goal of OpenHome. Rather than attempt to support some at the risk of alienating others, OpenHome provides Node software that is completely protocol independent with software to support whatever hardware is implemented in the Nodes.

The manufacturing choices will, ultimately, make that choice explicit. For example, a Node built with Bluetooth LE transceiver hardware will only be able to communicate with Widgets that are also Bluetooth LE enabled.

Nodes built to support multiple protocols will likewise be constrained to communicate with only those Widgets that use those same protocols.

OpenHome support both of these scenarios by not limiting the choices for manufacturers.

> **Note**
>
> Practically speaking it is not expected that Widget vendors will stack their devices with a range of communications protocols to ensure many types of Node can communicate with them. Rather, it is expected that Widget vendors will choose a Node manufacturer with whom they want to interoperate and design their Widgets to support the chosen Node manufacturer's implemented protocol.
>
> Cooperation between Node manufacturers and Widget vendors will ensure each vendor's devices can communicate with each other.

#### <span id="Widget_service_access"></span>Widget service access

ohOS places no constraint on the classes of Widgets that Nodes can communicate with. In fact, ohWidget Nodes will never need to ship with specific details about Widgets and the services or actions they provide.

Instead, the Widget manufacturers are given the responsibility of providing the details required for the Node to communicate with their Widgets.

This keeps the Nodes open and able to communicate with any Widget it can see on the home network, and also means that Node manufacturers are not spending their time concerned with a large amount of Widget implementation detail.

The details that Nodes do require are stored in separate Widget drivers. The Node operates independently of the content of each Widget driver and, therefore, independently of the function of each Widget. See Widget class driver below for more details of drivers.

Widget vendors have direct control over how much functionality each Widget exposes entirely independently of any conventions, consortium or forum. See the [ohWidget Driver Development](/wiki/OhWidget_Driver_Development) document for more details about writing Widget drivers.

This clear separation of responsibility allows Node manufacturers to be concerned only with the communications protocol they want to use, and the hardware implications of that choice. Widget vendors are solely responsible for providing the required details to allow Nodes access to the Widget.

## <span id="Widget_independent_Nodes"></span>Widget independent Nodes

A Node is never fully aware of the services each Widget it has access to provides. The complexity of the Widget is an unimportant detail for Nodes. Instead each Node is provided with the necessary drivers it needs to communicate with the Widget. The driver is used when a message is passed between the Node and the Control Point.

When the Node does not have access to the necessary driver, it will attempt to automatically retrieve it from an online resource. This can be either directly from the Widget vendor or from a database of drivers hosted elsewhere.

Alternatively the driver can be loaded manually by the user, using whatever means are made available by the hardware in the Node (such as USB stick or SD card). Both automatic and manual resolutions involve low levels of interaction by the user.

### <span id="Widget_class_driver"></span>Widget class driver

Each class of Widget, and each Widget using a different communications protocol within that class (i.e. two Widgets, both in the binary light class, one of which communicates with [Bluetooth LE](http://www.bluetooth.com) and the other with [Zigbee](http://www.zigbee.org)), has its own driver. Widget drivers are installed on the Node. Each driver contains code to allow the Widget to accept actions and report events.

An action is a message sent from the Control Point to the Widget, instructing the Widget to change its state in a particular way. Actions are initiated by the user from the UI, such as someone pressing the on button. An event is a message sent to the Control Point from the Widget, updating the Control Point about a change in the Widget's state. Events are initiated at the Widget, such as someone physically turning a light off.

Many previous attempts at home automation solutions relied on the Widget coming stacked with the necessary protocols and other networking interface information, such as a TCP/IP stack. ohWidget moves this responsibility away from the vendors by placing the information on the Nodes, leaving them fully capable of communicating with any Widget that needs to connect to the network.

To allow for the inclusion of more Widgets at any time the Nodes are designed to have no immediate knowledge of the Widgets in their vicinity. Beyond discovering the class of the Widget the Node remains functionally ignorant of each Widget, whether it be a light, a sprinkler or a thermostat.

It is left to Widget vendors as the experts of their own device to provide the specific details in Widget class drivers about each service a Widget provides. Widget drivers are written using the API provided by ohWidget and augmented by the vendor as required to suit a specific Widget's needs (such as specific communication protocol requirements).

Drivers must be written using managed code but can otherwise contain as much or as little code as the Widget vendors decide. ohWidget does not prescribe which services or actions Widget vendors can expose in their Widgets, leaving the Widget vendors free to implement their drivers with no compromise to any specific standard.

## <span id="User_interface_2"></span>User interface

### <span id="UI_host"></span>UI host

The Nodes are provided with a simple Web server. It hosts the user interface and gives the user access to the Widget's services.

OpenHome recommends the use of plug computers for Nodes due to both their small form factor and their processing power. The processing power of a plug computer is more than enough to serve the UI to the end-user.

Using the Node as the UI host means that Widgets do not have extra responsibility added to them. It also allows Node manufacturers to customize the look and feel of the UI.

Widget vendors can instead focus on the two most important aspects:

- ensuring the Widget provides the best possible service it was designed for
- focusing the vendor's own developers on building clean, usable interfaces that are specific to a particular Widget

### <span id="UI_design"></span>UI design

The Node manufacturer has complete control over how the user interface looks and feels.

> **Important**
>
> A reference UI is provided with the ohWidget software to display a list of aggregated services. Node manufacturers are entirely responsible for the design of the user interface beyond that.

The HTML, JavaScript and CSS files provided with the UI SDK can be customized to suit the design specifications of the Node manufacturer.

ohWidget provides an API for manufacturers to develop UIs for their own Nodes. Presented as a Web-based API, it offers the simplest and easiest method to access the Widget's functionality. Using a Web-based presentation means that most end-users will be able to access the Widget's UI with no extra hardware costs. Most modern homes already have one or more Web-enabled devices already installed, whether it be a personal computer or a smartphone.

The Web UI is capable of running on both types of device and the range of devices in between.

# <span id="Glossary"></span>Glossary

Control Point - The device that displays the user interface which makes use of services on the network to control a UPnP device.

Node - The communications bridge between the Control Point and the Widget. Also the target for deployment of ohApps.

Node communication protocol - The custom UPnP protocol provided by Openhome to allow Nodes to communicate with each other.

Node mesh - A collection of Nodes that intercommunicate.

ohApp - An application that runs inside ohOS.

[ohNet](/wiki/OhNet) - Library for discovering, eventing and controlling services on a network. Includes a full implementation of the UPnP stack.

[ohOs](/wiki/OhOs) - The Openhome Operating System. Core software for ohWidget systems that runs on Nodes.

Widget - The physical device installed in the user's home to provide them with a service. Typical Widgets are lights, speakers, temperature controls.

Widget communication protocol - The protocol used by the Widget to advertise its availability and services to the Nodes. Widget manufacturers are responsible for choosing which protocols each Widget supports. A typical Widget supports only one Widget communication protocol.

Widget driver - The software used by the Node to communicate with the Widget.
{% endraw %}
