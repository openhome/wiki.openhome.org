---
title: "OhMedia:Developer"
permalink: "/wiki/OhMedia:Developer"
redirect_from:
  - "/wiki/Av:Developer"
  - "/wiki/Developer"
---

{% raw %}
[What is it?](/wiki/OhMedia:What) · [How do I get it?](/wiki/OhMedia:How) · [Developers](/wiki/OhMedia:Developer)

**OpenHome Media - Developers**

# <span id="Introduction"></span>Introduction

OpenHome Media is an independent standard for networked audio visual devices. OpenHome Media products all have a standard way of presenting themselves to the network. This makes it possible to write generic Control Point software that is able to control those products independent of manufacturer or specific features.

The technologies associated with making this possible are grouped under the term OpenHome Media Topology.

If a developer wishes to write generic software that participates in the aims described above, then they should write that software in a way that conforms to the strategies and algorithms of OpenHome Media Topology, which is described below

# <span id="Topology"></span>Topology

## <span id="Products"></span>Products

An OpenHome installation consists of products from a variety of manufacturers each bearing the [Product service](/wiki/Av:Developer:ProductService).

Amongst other information, each product has:

- Room (user configurable, defaults to 'Main Room')

<!-- -->

- Name (user configurable, defaults to the model name)

<!-- -->

- Source Count (fixed according to the capabilities of the product)

<!-- -->

- List of Sources, each with its own Type, Name, and Visibility

<!-- -->

- Attributes, identifying additional functionality offered by the product

## <span id="Proper_Configuration"></span>Proper Configuration

The name of each product represents its audio output.

The name of each source represents an audio input (either internal or external).

In a properly configured system, if one product is connected to another using an audio cable, then the name of the product sending the audio should match the name of the source receiving the audio. It is by matching these names that a Control Point is able to select the correct input on, for instance, a preamp when a particular source is selected.

## <span id="Discovering_An_OpenHome_Media_System"></span>Discovering An OpenHome Media System

The correct way to discover an OpenHome Media system is to:

- search for all units bearing the Product service

<!-- -->

- subscribe to each Product service

<!-- -->

- group these products according to their Room.

<!-- -->

- collect the name of all the sources in each product

<!-- -->

- match the names of the sources to the names of the products to create a set of tree structures in each room.

## <span id="Source_Functionality"></span>Source Functionality

To determine the kind of functionality available on each source, inspect its type.

If it has type Playlist, it additionally contains the [Playlist service](/wiki/Av:Developer:PlaylistService)

If it has type Radio, it additionally contains the [Radio service](/wiki/Av:Developer:RadioService)

If it has type Receiver, it additionally contains the [Receiver service](/wiki/Av:Developer:ReceiverService)

## <span id="Volume_Control"></span>Volume Control

Products that offer volume control include the Volume attribute and the [Volume service](/wiki/Av:Developer:VolumeService)

## <span id="Now_Playing_Information"></span>Now Playing Information

Products that provide information concerning the currently playing media include the [Info service](/wiki/Av:Developer:InfoService)

Products that report the current time within the currently playing track include the [Time service](/wiki/Av:Developer:TimeService)

## <span id="Multiroom_Functionality"></span>Multiroom Functionality

An OpenHome Media Sender broadcasts music onto a network in a way that is playable by an OpenHome Media Receiver.

An OpenHome Media Sender includes the [Sender service](/wiki/Av:Developer:SenderService).

An OpenHome Media Receiver includes a Receiver source (as part of of its topology) and an associated [Receiver service](/wiki/Av:Developer:ReceiverService).

# <span id="Services"></span>Services

- [Product service](/wiki/Av:Developer:ProductService)
- [Playlist service](/wiki/Av:Developer:PlaylistService)
- [Radio service](/wiki/Av:Developer:RadioService)
- [Info service](/wiki/Av:Developer:InfoService)
- [Time service](/wiki/Av:Developer:TimeService)
- [Volume service](/wiki/Av:Developer:VolumeService)
- [Sender service](/wiki/Av:Developer:SenderService)
- [Receiver service](/wiki/Av:Developer:ReceiverService)

# <span id="Songcast_Specifications"></span>Songcast Specifications

- [Songcast OHM/OHU Protocol Specification](/wiki/Av:Developer:Songcast:Ohm)
- [Songcast OHZ Protocol Specification](/wiki/Av:Developer:Songcast:Ohz)
{% endraw %}
