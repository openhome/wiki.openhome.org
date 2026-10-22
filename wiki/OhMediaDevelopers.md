---
title: "OhMediaDevelopers"
permalink: "/wiki/OhMediaDevelopers"
redirect_from:
---

{% raw %}
# <span id="Network_Services"></span>Network Services

ohMedia defines the following network services:

- [ Product](/wiki/Av:Developer:ProductService). The core of a renderer and the only mandatory service. The state of this service allows control points to infer which other services are present on a device. In more complex installations it allows devices to mapped into a multi-room hi-fi system
- [ Playlist](/wiki/Av:Developer:PlaylistService). An ordered list of tracks to be played.
- [ Radio](/wiki/Av:Developer:RadioService). Browse and select from a list of favourite internet radio, podcast and listen again presets.
- [ Info](/wiki/Av:Developer:InfoService). Report information about currently playing track.
- [ Time](/wiki/Av:Developer:TimeService). Report information about progress through a track.
- [ Volume](/wiki/Av:Developer:VolumeService). Control volume on a renderer or a connected pre-amp.
- [ Transport](/wiki/Av:Developer:TransportService). Source-independent transport controls.
- [ Sender](/wiki/Av:Developer:SenderService). Indicate presence and state of a Songcast sender.
- [ Receiver](/wiki/Av:Developer:ReceiverService). Control a Songcast receiver.
- [ Credentials](/wiki/Av:Developer:CredentialsService). Securely manage login details for external services supported by a device.
- [ Pins](/wiki/Av:Developer:PinsService). Quick access to smart presets, supporting dynamic content.
- NetworkMonitor. Measures network performance.
- [ PlaylistManager](/wiki/Av:Developer:PlaylistManagerService). Included in media servers. Allows playlists to be shared between renderers and saved for future reuse.

The [ Eriskay](/wiki/Av:Developer:EriskayServices) family of services will later replace these. Feedback on Eriskay is welcomed.

# <span id="UPnP"></span>UPnP

All ohMedia products publish and/or consume network services using UPnP. This is enabled by [ ohNet](/wiki/OhNet) - a cross-platform UPnP stack suitable for use in control points and devices. ohNet is open source, liberally licensed and intended for use in external products.

# <span id="ODP"></span>ODP

[ OpenHome Device Protocol](/wiki/Av:Developer:Odp) (ODP) allows control of and evented updates from a device via a single socket. [ohPipeline](https://github.com/openhome/ohPipeline) contains [reference code](https://github.com/openhome/ohPipeline/tree/master/OpenHome/Net/Odp) for control point or device stacks.

All services that are available using over UPnP are also available using ODP. The same auto-generated 'proxies' allow control point authors to invoke an action as a single function call and register callbacks to be informed of evented updates.

# <span id="Songcast"></span>Songcast

The Songcast brand encompasses a range of products and protocols.

## <span id="Desktop_senders"></span>Desktop senders

Virtual audio drivers that send all audio from a Windows or Mac device to a songcast receiver. [Linn](https://www.linn.co.uk/software#songcast) provide a full implementation of these. The bulk of the code required is also available in the [ohSongcast](https://github.com/openhome/ohSongcast) repo.

## <span id="Multi-room"></span>Multi-room

The Songcast protocol enables synchronised playing of audio from an unbounded number of ohMedia renderers.

The [ohSongcast](https://github.com/openhome/ohSongcast) repo provides a cross-platform C++ library offering much of the code needed to write a stand-alone songcast sender. The [ohPipeline](https://github.com/openhome/ohPipeline) repo contains a reference sender and receiver fully integrated to the OpenHome reference audio pipeline.

The Songcast protocols are also documented:

- [ OHM/OHU protocol specification](/wiki/Av:Developer:Songcast:Ohm)
- [ OHZ protocol specification](/wiki/Av:Developer:Songcast:Ohz)

## <span id="Direct"></span>Direct

A specialised protocol, offering simpler integration and potentially higher audio quality, used when there is a single receiver and the sender has control over the rate of streaming (this often means that the sender is responsible for audio decode).

More information, including protocol spec and sample code is available [ here](/wiki/Av:Developer:Scd).

# <span id="Topology"></span>Topology

ohMedia models a home as a number of hi-fi systems, which are located in rooms.

A hi-fi system is modelled as a hierarchical tree of products, where a product is defined as a single physical box that is located in a room, has a unique name within the room, has at least one output and any number of inputs.

A product is modelled through the [ Product](/wiki/Av:Developer:ProductService) service specification.

When a control point wants to construct a model of a user's home they use the Topology algorithm:

- discover all the products in the home that have a Product service
- group the discovered products based on the room they are in
- create a hierarchical tree structure by matching source names to product names \*
- discover source functionality based on source type
- discover additional functionality based on product attributes

Example implementations of the Topology algorithm are available in C# and C++ from the [ohTopology](https://github.com/openhome/ohTopology) github repo.

A more detailed description of the ohTopology software can be found [ here](/wiki/Av:Developer:ohTopologyDescription).

# <span id="Streaming_Services"></span>Streaming Services

Both Linn's DS and [ ohMediaPlayer](/wiki/OhMediaPlayer) include reference implementations for the following streaming services:

- [ Tidal](/wiki/TidalStreamingService)
- [ Qobuz](/wiki/QobuzStreamingService)
- [ Calm Radio](/wiki/CalmRadioInternetRadio)
{% endraw %}
