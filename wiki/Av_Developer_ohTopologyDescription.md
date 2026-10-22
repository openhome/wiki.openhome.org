---
title: "Av:Developer:ohTopologyDescription"
permalink: "/wiki/Av:Developer:ohTopologyDescription"
redirect_from:
---

{% raw %}
# <span id="ohTopology"></span>ohTopology

## <span id="Overview"></span>Overview

ohTopology is a software stack which provides a means of controlling devices, on a local network, via their UPnP service actions. Devices are grouped based on their Room names and presented as a tree structure based on their interconnectivity. It consists of a number of distinct layers. Each layer focuses on exposing specific properties and actions that are intended to be utilised by the layers above. Clients of ohTopology need only interface directly with the highest layer of the stack to gain access to the properties and actions exposed by the lower layers.

## <span id="Watchable_System"></span>Watchable System

### <span id="Overview_2"></span>Overview

Actions exposed by a layer can be called directly, but property values can only be monitored through a callback notification system (observer pattern). Properties are exposed as "watchable" values that may be monitored by "watcher" clients. When a (watchable) property changes, all of its watchers are automatically notified of the change and the property's new value. Watchers can be added and removed at any time. The IWatchable interface is used to expose single value properties and the IWatchableUnordered and IWatchableOrdered interfaces are used for multivalue property lists. Property client objects must conform to the appropriate Iwatchable/IWatchableUnordered/IWatchableOrdered interface for the property that they wish to observe.

### <span id="Watchable_Thread"></span>Watchable Thread

Although ohTopology is designed to run on multithreaded platforms, actions are executed in a single thread through the use of a thread scheduler class, WatchableThread. Enforcing single threaded execution removes the burden of having to manage thread safety, simplifies debugging and reduces the risk of deadlock. The WatchableThread class provides three methods; Execute, Schedule and Assert.

### <span id="Schedule_Method"></span>Schedule Method

Schedule provides a mechanism for **asynchronous callback**. The specified callback is placed in a queue (FIFO) to be run on the watchable thread, in turn, at some point in the future. Schedule takes a functor, for the callback method, and a generic void\* argument to be passed to the callback.

### <span id="Execute_Method"></span>Execute Method

Execute provides a mechanism for **synchronous callback**. If called from the watchable thread it executes the callback immediately. Otherwise it schedules the callback, for execution on the watchable thread. In either case, it blocks until the callback has completed. Execute takes a functor for the callback method and a generic void\* argument to be passed to the callback.

### <span id="Assert_Method"></span>Assert Method

Assert provides a way of checking if the current thread is the watchable thread.

## <span id="Injector"></span>Injector

## <span id="Network"></span>Network

## <span id="Topology1"></span>Topology1

### <span id="Overview_3"></span>Overview

Topology1 collects a list of **Product Service** devices from Network and exposes a collection of **Products**.

### <span id="Topology1_2"></span>Topology1

Topology1 watches a (Product Service) device list from **Network** and creates a corresponding list of **ProxyProduct** objects that is updated whenever the device list changes. The **Products** method exposes the **ProxyProduct** list as an IWatchableUnordered.

## <span id="Topology2"></span>Topology2

### <span id="Overview_4"></span>Overview

Topology2 collects the list of **Products** from **Topology1** and exposes a collection of **Groups**. Each **Group** exposes a **Sources** collection and pertinent properties and actions of the **Product Service**. Each **Source** exposes the standard set of Source properties.

### <span id="Topology2_2"></span>Topology2

Topology2 watches **Topology1::Products** and creates a corresponding list of **Topology2Group** objects that is updated whenever **Topology1::Products** changes. The **Groups** method exposes the **Topology2Group** list as an IWatchableUnordered.

### <span id="Topology2Source"></span>Topology2Source

Topology2Source exposes the three standard source properties: **Name**, **Visible** and **Type**. The **Index** method exposes the source's position in the source list of **Topology2Group**.

### <span id="Topology2Group"></span>Topology2Group

Topology2Group watches the **SourceXml** property of its underlying **ProxyProduct** object. Source information retrieved from **SourceXml** is used to to create and update a list of **Topology2Source** objects. The **Sources** method exposes the **Topology2Source** list as an IWatchableUnordered.

## <span id="Topology3"></span>Topology3

### <span id="Overview_5"></span>Overview

Topology3 collects the list of **Groups** from **Topology2** and exposes a collection of **Groups**. Each **Group** exposes a **Sources** collection, pertinent actions and properties of the **Product Service**, and a **Sender** property.

### <span id="Topology3_2"></span>Topology3

Topology3 watches **Topology2::Groups** to create and maintain a corresponding list of **Topology3Group** objects. A dedicated **SenderWatcher** is created for each **Topology3Group** that has a Sender attribute, to monitor the **Metadata** property of its **Sender Service** . A dedicated **ReceiverWatcher** is created for each **Topology3Group** to monitor both the **Metadata** and **TransportState** properties of its **Receiver Service**.

Topology3 marries receivers and senders by matching their **Uri** properties, reassigning the **Sender** property of each **Topology3Group** when changes are reported by the watchers. The **Groups** method exposes the **Topology3Group** list as an IWatchableUnordered.

### <span id="Topology3Group"></span>Topology3Group

Topology3Group exposes all of the properties and actions of its underlying **Topology2Group** plus a **Sender** property. The Sender property holds a reference to a **Sender** object that reflects the Songcast sender device that the group's receiver source is listening to. The **SenderEmpty** object is used when no sender is selected or the selected sender is inactive.

### <span id="ReceiverWatcher"></span>ReceiverWatcher

ReceiverWatcher watches the **Sources** property of Topology3Group to find a source of type **Receiver** as an indicator of the existence of a **Receiver service**. If it exists, the **Receiver service** is subscribed to and its **TransportState** and **Metadata** properties are watched. When either of these two properties change Topology3 is notified via its **ReceiverChanged** method.

### <span id="SenderWatcher"></span>SenderWatcher

SenderWatcher subscribes to it's group's **Sender service** to watch its **Metadata** property. When this property changes Topology3 is notified via its **SenderChanged** method.

## <span id="Topology4"></span>Topology4

### <span id="Overview_6"></span>Overview

Topology4 collects the list of **Groups** from **Topology3** and exposes a new collection of **Rooms**. Each **Room** in the new collection exposes a collection of **Groups** with matching **RoomName** properties.

### <span id="Topology4_2"></span>Topology4

Topology4 watches **Topology3::Groups** and creates a **Topology4Room** list that is updated whenever there is a change to the **RoomName** property of any **Topology3Group**. A dedicated **Topology4GroupWatcher** is created for each **Topology3Group** to watch its **RoomName** property. The Rooms method exposes the **Topology4Room** list as an IWatchableUnordered.

### <span id="Topology4Room"></span>Topology4Room

Topology4Room maintains a collection of **Topology4Group** objects with matching **RoomName** properties. The collection contains at least one group. Groups are added and removed by the Topology4 class. The **Name** method exposes the **Name** property which reflects the common **RoomName** value shared by all groups in the collection. The **SetStandby** method sets the standby state of all groups. The **Groups** method exposes the collection of groups as an IWatchableUnordered.

### <span id="Topology4GroupWatcher"></span>Topology4GroupWatcher

Topology4GroupWatcher watches the **RoomName** property of a single **Topology3Group** and updates **Topology4**, removing the group from one room and adding it to another, whenever its **RoomName** property changes.

## <span id="Topology5"></span>Topology5

### <span id="Overview_7"></span>Overview

Topology5 collects the list of **Rooms** from **Topology4** and organises the products (**Groups**) in each room, evaluating their interrelationship as a family tree of connected **parents** and **children**. It exposes a list of **Rooms**, with each **Room** exposing a list of parent products (**Roots**) and a list of sources.

#### <span id="Roots"></span>Roots

Products in a room can be daisychained by connecting the outputs of one product to the inputs of another, creating a tree of devices. In such a setup, the **Root** (parent) of the tree (the product at the end of the chain) is the output for all the products in the room. Typically there should only be one **Root** in each room, whose outputs are connected to the speakers. A **Root** is thus defined as a product whose outputs are **not** connected to the inputs of any other product.

#### <span id="Source_Naming"></span>Source Naming

It is not possible for a product to detect if other products are connected to its inputs. Topology, therefore, can only imply this through source naming configured by the user, as follows. If a **source name** on a product "ProductA" matches the **device name** of another product "ProductB", in the same room, it implies that the outputs of ProductB are connected to the inputs of that source on ProductA. In the family tree of products in a room, ProductA is the **parent** of ProductB and ProductB is a **child** of ProductA.

### <span id="Topology5_2"></span>Topology5

Topology5 watches **Topology4::Rooms** to create and maintain a corresponding collection of **Topology5Room** objects. The **Rooms** method exposes the collection of rooms as an IWatchableUnordered.

### <span id="Topology5Room"></span>Topology5Room

Topology5Room maintains a Topology3Group list of by watching the Groups list of its underlying Topology4Room. A dedicated Topology5GroupWatcher is created for each group to watch its **Name** and **Sources** properties. Since all groups in the room may not share the same standby state, an additional "**mixed**" state is introduced to create a **tristate Standby** property. The **Topology3Group** list is used to maintain a corresponding **Topology5Group** list which is then filtered to obtain a **Roots** list. A super list of sources (Topology5Source) is then created by gathering all the sources of each Root replacing each source with its child group's sources where appropriate. The **Roots** method exposes the Roots list as an IWatchableUnordered. The **Sources** method exposes the Roots list as an IWatchableUnordered. The **Standby** method exposes the standby state of the room. The **SetStandby** method sets the standby state of all groups in the room. The **Name** method exposes the common room name shared by all groups in the room.

### <span id="Topology5Group"></span>Topology5Group

Topology5Group keeps track of it's **parent** and **children** groups, its currently active source, a list of its currently visible sources (expanded to include the sources of any child groups), a list of groups (from my group upwards) with the Volume service, a list of all child groups that have the Sender service.

### <span id="Topology5GroupWatcher"></span>Topology5GroupWatcher

Monitors the **Name** and **Sources** properties of a specific **Topology3Group**, updating **Topology5Room** whenever a change occurs.

### <span id="Topology5Source"></span>Topology5Source

Topology5Source provides a number of methods that expose the standard source parameters, flags to the presence of the Info and Time services, the source's parent group, the group's device and a list of parent groups with the Volume service. Also provided is a method to reset the list of volume service groups, a method select the source and a factory method, **CreatePreset**, that returns a **MediaPresetExternal** object.

### <span id="MediaPresetExternal"></span>MediaPresetExternal

MediaPresetExternal is an object that provides access to a single **Topology5Source** object via the standard **IMediaPreset** interface. It monitors the transport state of the Source by watching the **Source** property of the its parent **Topology5Group**. The state is exposed via the three IWatchable properties **Playing**, **Buffering** and **Selected**. The **Play** method selects the source in its parent group.

## <span id="Services"></span>Services

### <span id="Overview_8"></span>Overview

### <span id="Service"></span>Service

### <span id="ServicePlaylist"></span>ServicePlaylist

### <span id="ServiceRadio"></span>ServiceRadio

### <span id="ServiceSender"></span>ServiceSender

### <span id="ServiceReceiver"></span>ServiceReceiver

### <span id="ServiceVolume"></span>ServiceVolume

### <span id="ServiceInfo"></span>ServiceInfo

### <span id="ServiceProduct"></span>ServiceProduct
{% endraw %}
