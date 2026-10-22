---
title: "Av:Developer:Songcast:Ohz"
permalink: "/wiki/Av:Developer:Songcast:Ohz"
redirect_from:
---

{% raw %}
# <span id="Songcast_OHZ_Protocol_Specification_.28Version_1.0.29"></span>Songcast OHZ Protocol Specification (Version 1.0)

## <span id="Introduction"></span>Introduction

OHZ, together with [OHM and OHU](/wiki/Av:Developer:Songcast:Ohm), form the Songcast family of OpenHome protocols for transporting audio around a home network.

OHZ provides the ability for a uniquely identified Songcast Sender to redirect its Receivers to different OHM or OHU URIs.

### <span id="How_does_a_Songcast_Sender_use_OHZ.3F"></span>How does a Songcast Sender use OHZ?

In order to use OHZ, a Songcast Sender must:

- Publish an OHZ URI instead of an OHM or OHU URI
- Broadcast the OHM or OHU URI associated with this OHZ URI whenever it is requested by a Receiver (solicited broadcast)
- Broadcast the OHM or OHU URI associated with this OHZ URI whenever it changes (unsolicited broadcast)

### <span id="Why_would_a_Songcast_Sender_use_OHZ.3F"></span>Why would a Songcast Sender use OHZ?

There are two known reasons for the use of OHZ.

- To allow devices that are both Senders and Receivers to manage complicated patterns of one-to-many communication, such as a Receiver listening to a Sender that is itself listening to another Sender. In this instance, the intermediate Sender can redirect its Receivers to the root Sender rather than rebroadcast Audio messages, which would accumulate network delays.

<!-- -->

- In order to allow a Receiver to continue listening to a Sender even though the configuration of the Sender has changed from Unicast to Multicast, or vice versa. Or when the Multicast channel is changed while the Sender is in Multicast mode.

## <span id="Message_Format"></span>Message Format

The OHZ protocol has the following message format.

| Bytes | Name | Description |
|----|----|----|
| Header |  |  |
| 4 | Signature | 0x6f, 0x68, 0x7a, 0x20 ('ohz ') |
| 1 | Version | 1 |
| 1 | Type | The type of message |
|  |  | 0 - Zone Query |
|  |  | 1 - Zone Uri |
|  |  | 2 - Preset Query |
|  |  | 3 - Preset Info |
| 2 | Length | The length in bytes of the whole message including this header \[8..5000\] |
| Zone Query |  |  |
| 4 | QueryZoneLength | The length in bytes of the zone |
| n | QueryZone | The queried Zone Id, where n = QueryZoneLength |
| Zone Uri |  |  |
| 4 | ZoneLength | The length in bytes of the Zone Id |
| 4 | UriLength | The length in bytes of the URI |
| p | Zone | The Zone Id, where p = ZoneLength |
| q | Uri | The URI, where q = UriLength |
| Preset Query |  |  |
| 4 | QueryPreset | The queried preset number |
| Preset Info |  |  |
| 4 | Preset | The preset number |
| 4 | MetadataLength | The length in bytes of the metadata |
| r | Metadata | The metadata in DIDL-Lite format, where r = MetadataLength |

## <span id="Zone_Handling"></span>Zone Handling

Each participating Sender must have a unique Zone Id. This Id is often derived from the Sender's MAC address, but any other network-unique Id is acceptable.

The OHZ URI for a Sender is: `ohz://239.255.255.250:51972/ZoneId`

### <span id="From_The_Receiver.27s_Perspective"></span>From The Receiver's Perspective

In order to listen to `ohz://239.255.255.250:51972/ZoneId`, a Receiver should send a Zone Query message to the Multicast endpoint `239.255.255.250:51972` and listen for an equivalent Zone Uri message.

If no Zone Uri message is received within 100mS, then the process should be repeated.

Once a matching Zone Uri message has been received, the contained OHM or OHU URI is used to establish an audio connection to the Sender.

The OHZ handler should continue listening for Zone Uri messages that match the Zone Id. If a different URI is published by the Sender, then audio playback should be terminated and a new audio connection established using the new OHM or OHU URI.

### <span id="From_The_Sender.27s_Perspective"></span>From The Sender's Perspective

A Sender should listen on the Multicast endpoint `239.255.255.250:51972` for Zone Query messages that match its Zone Id, and should respond with a single Zone Uri message.

Whenever the Sender's OHM or OHU URI changes, it should send 3 consecutive Zone Uri messages with the new URI.

## <span id="Presets"></span>Presets

A Sender can optionally participate in the OHZ Preset system. This allows for a Sender to be configured with a network-unique preset number that can be used by a primitive control points, such as an IR handset.

To participate in this system, a Sender must listen for Preset Query messages and send Preset Info messages accordingly.

The metadata for the Preset Info message is the same DIDL-Lite metadata that is published using the [Sender service](/wiki/Av:Developer:SenderService).
{% endraw %}
