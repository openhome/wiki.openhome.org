---
title: "Av:Developer:Songcast:Ohm"
permalink: "/wiki/Av:Developer:Songcast:Ohm"
redirect_from:
---

{% raw %}
# <span id="Songcast_OHM.2FOHU_Protocol_Specification_.28Version_1.0.29"></span>Songcast OHM/OHU Protocol Specification (Version 1.0)

## <span id="Introduction"></span>Introduction

OHM and OHU, together with [OHZ](/wiki/Av:Developer:Songcast:Ohz), form the Songcast family of OpenHome protocols for transporting audio around a home network.

- OHM provides large scale one to many communication using Multicast UDP.
- OHU provides small scale one to many communication using Unicast UDP.

OHU can be used to deliver Songcast functionality to networks that do not handle Multicast UDP as thoroughly as OHM requires.

## <span id="General"></span>General

### <span id="Message_Format"></span>Message Format

The OHM and OHU protocols share the same message format.

| Bytes | Name | Description |
|----|----|----|
| Header |  |  |
| 4 | Signature | 0x6f, 0x68, 0x6d, 0x20 ('ohm ') |
| 1 | Version | 1 |
| 1 | Type | The type of message |
|  |  | 0 - Join |
|  |  | 1 - Listen |
|  |  | 2 - Leave |
|  |  | 3 - Audio (details below) |
|  |  | 4 - Track (details below) |
|  |  | 5 - Metatext (details below) |
|  |  | 6 - Slave (details below) |
| 2 | Length | The length in bytes of the whole message including this header |
|  | Minimum | 8 |
|  | Maximum | 16392 |
| Audio |  |  |
| 1 | AudioHeaderLength | 50 |
| 1 | Flags | Bit 0 - halt |
|  |  | Bit 1 - lossless |
|  |  | Bit 2 - timestamped |
|  |  | Bit 3 - resent |
|  |  | Bit 4 - 0 |
|  |  | Bit 5 - 0 |
|  |  | Bit 6 - 0 |
|  |  | Bit 7 - 0 |
| 2 | SampleCount | The number of samples in this frame |
| 4 | Frame | The frame number |
| 4 | NetworkTimestamp | The time when the previous frame was sent over the network (if the timestamped flag is on) |
| 4 | MediaLatency | The duration of the Sender's audio buffer |
| 4 | MediaTimestamp | The time when this frame was placed into an audio buffer of duration `MediaLatency` on the Sender (if the timestamped flag is on) |
| 8 | StartSample | The sample number within the current track of the first sample in this frame |
| 8 | TotalSamples | The total number of samples in the current track |
| 4 | SampleRate | The sample rate in samples per second |
| 4 | BitRate | The bit rate in bits per second |
| 2 | VolumeOffset | The volume offset in signed binary milli-dB (+/- 32dB) |
| 1 | BItDepth | The bit depth (8, 16, or 24) |
| 1 | Channels | The number of interleaved audio channels |
| 1 | AudioReserved | 0 |
| 1 | CodecNameLength | The number of bytes in the name of the codec |
| m | CodecName | The codec name (in UTF-8), where m = CodecNameLength |
| n | Pcm | Pcm samples, where n = Channels \* BitDepth \* SampleCount / 8 |
| Track |  |  |
| 4 | TrackSequence | Sequence number for this track. |
| 4 | TrackUriLength | The length in bytes of the track URI |
| 4 | TrackMetadataLength | The length in bytes of the track metadata |
| p | TrackUri | The track URI, where p = TrackUriLength |
| q | TrackMetadata | The track metadata in DIDL-Lite format, where q = TrackMetadataLength |
| Metatext |  |  |
| 4 | MetatextSequence | Sequence number for this metatext. |
| 4 | MetatextLength | The length in bytes of the metatext |
| r | Metatext | The metatext in DIDL-Lite format, where r = MetatextLength |
| Slave |  |  |
| 4 | SlaveCount | The number of slaves |
| s | SlaveList | The list of slave endpoints, where s = 6 \* SlaveCount |

### <span id="Control_Messages"></span>Control Messages

The Join and Listen messages are used by OHM. The Join, Listen, Leave, and Slave messages are used by OHU.

### <span id="Audio_Messages"></span>Audio Messages

Audio is transmitted as a timely and continuous stream of Audio messages.

It is typical to send Audio messages every 5ms - 10ms with the length of each message dependent on the format of the audio being played.

It is also typical at a track boundary to send a shorter Audio message so that a single Audio message does not span two tracks.

If no audio material is to be played because, for instance, the user has told the sender to pause playback, then the sender should not send silence. Rather, the sender should adorn the last Audio message with the 'halt' flag to indicate that this continuous stream of audio has completed and that the next continuous stream of audio will start at an arbitrary time in the future.

Note that CodecName should represent the codec that was used to decode the PCM payload. If no appropriate codec name is available then CodecName should be set to "PCM".

### <span id="Timestamps"></span>Timestamps

Accurate timestamps allow appropriately equipped Songcast Receivers to achieve close audio synchronisation. But timestamps should only be used when high accuracy is achievable. The timestamps and the media latency are measured according to an audio MCLK that is 256 \* 44K1, or 256 \* 48K.

### <span id="Track_Messages"></span>Track Messages

Track messages are transmitted to provide Songcast Receivers with in-band information concerning the currently playing track. They should be sent when a Receiver sends a Join message, and whenever the track changes. The incrementing sequence number can be used by Receivers to distinguish between Track messages sent at the start of a new track (increment) and those sent when a new Receiver joins (no increment).

### <span id="Metatext_Messages"></span>Metatext Messages

Metatext messages are used to convey dynamic textual information concerning the currently playing audio material. This is typically information broadcast by internet radio stations. The incrementing sequence number can be used by Receivers to distinguish between Metatext messages sent when the dynamic information changes (increment) and those sent when a new Receiver joins (no increment).

### <span id="Slave_Messages"></span>Slave Messages

OHU uses Slave messages to deliver one-to-many communication using Unicast UDP. The message contains a list of endpoints arranged as 6-byte ordered pairs of ip-address and port.

## <span id="Multicast"></span>Multicast

### <span id="OHM_Sender_Channel"></span>OHM Sender Channel

OHM is used to stream audio from a single sender to multiple receivers using Multicast UDP.

Each Multicast Sender within a network has a unique 16 bit Multicast Channel, which must be configurable by the user to avoid conflicts. And each Multicast Channel has an equivalent URI as follows:

**Multicast Sender Channel**

|         |                             |
|---------|-----------------------------|
| Channel | Uri                         |
| 0       | ohm://239.253.0.0:51972     |
| 1       | ohm://239.253.0.1:51972     |
| 2       | ohm://239.253.0.2:51972     |
| 3       | ohm://239.253.0.3:51972     |
| ...     | ...                         |
| 65535   | ohm://239.253.255.255:51972 |

A Multicast Sender usually publishes its URI using the OpenHome Sender service over UPnP. However, it is also possible for Multicast Sender to publish its URI by some other mechanism.

A Receiver engages with an Multicast Sender by exchanging messages with the Multicast endpoint indicated by this OHM URI.

### <span id="OHM_NULL_URI"></span>OHM NULL URI

The URI `ohm://0.0.0.0:0` is the OHM NULL URI.

If requested to play this URI, a Receiver should clear any Track Uri, Track Metadata, and Track Metatext, and be silent.

### <span id="OHM_Control"></span>OHM Control

In general a Receiver is required to send a Join message to the Sender when it starts listening and a Listen message every second or so after that. However, when using Multicast UDP it is not necessary for a Receiver to send a Listen message if it has detected that some other Receiver has already sent one. This is because the only purpose of the Listen message is to ensure that the Sender continues sending Audio messages, and any Listen message from any Receiver will serve this purpose.

A Multicast Sender and a listening Receiver implement the following state machines to reduce unnecessary Multicast network traffic.

<figure>
<img src="/mediawiki/images/4/45/Songcast_Sender_Multicast_State_Transition_Diagram.png" title="Songcast_Sender_Multicast_State_Transition_Diagram.png" alt="Songcast_Sender_Multicast_State_Transition_Diagram.png" />
<figcaption aria-hidden="true">Songcast_Sender_Multicast_State_Transition_Diagram.png</figcaption>
</figure>

**MULTICAST SENDER STATE TRANSITION DIAGRAM**

<figure>
<img src="/mediawiki/images/5/54/Songcast_Receiver_Multicast_State_Transition_Diagram.png" title="Songcast_Receiver_Multicast_State_Transition_Diagram.png" alt="Songcast_Receiver_Multicast_State_Transition_Diagram.png" />
<figcaption aria-hidden="true">Songcast_Receiver_Multicast_State_Transition_Diagram.png</figcaption>
</figure>

**MULTICAST RECEIVER STATE TRANSITION DIAGRAM**

Using this scheme one Receiver tends to become the Primary Receiver, which sends Listen messages to keep the Sender producing audio messages. If the Primary Receiver ever stops listening then one of the remaining Secondary Receivers is automatically promoted to the role of Primary Receiver.

The OHM Sender stops producing Audio messages T seconds after the last Receiver has stopped sending Listen messages. Ts and Tp are arranged so that for a Sender to erroneously stop producing Audio messages in the presence of active Receivers it would have to miss 4 consecutive Listen messages.

The Sender Blocked states should only occur in a misconfigured system with more than one Sender on the same channel.

## <span id="Unicast"></span>Unicast

### <span id="OHU_Basics"></span>OHU Basics

The OHU protocol is arranged so that the OHU Sender need send audio to only one OHU Receiver. This is to reduce the processing overhead on those OHU Senders that have constrained processing resources.

If the OHU Sender is using this feature of the OHU protocol then it nominates one of its OHU Receivers to be the Primary OHU Receiver and sends it a Slave message, which contains a list of Slave OHU Receiver endpoints. The Primary OHU Receiver must forward any subsequent Audio, Track, or Metatext messages to this list.

As OHU Receivers come and go, the OHU Sender is responsible for nominating its OHU Primary Receiver and updating the list of OHU Slave Receivers appropriately.

If an OHU Sender has the processing power necessary to send to multiple OHU Receivers it may ignore the Slave feature or may adopt a hybrid approach, which would multiply the maximum number of OHU Receivers that that OHU Sender could support.

### <span id="OHU_Sender_Uri"></span>OHU Sender Uri

An OHU Sender URI, such as ohu://192.168.1.23:51973, represents an ip endpoint.

An OHU Sender usually publishes its URI using the OpenHome Sender service over UPnP. However, it is also possible for an OHU Sender to publish its URI by some other mechanism.

An OHU Receiver engages with an OHU Sender by exchanging UDP messages with the Unicast endpoint indicated by the OHU Sender's URI.

### <span id="OHU_Control"></span>OHU Control

As well as the Join and Listen messages, OHU also uses the Leave message. This gives the OHU Sender instantaneous information concerning its OHU Listeners and enables it to quickly reorganise its OHU Primary Receiver and OHU Slave Receivers in a way that ensures uninterrupted audio.

The periodic Listen message from all receivers is still present as a fallback mechanism for detecting OHU Receivers that become disconnected in a way that prevents them from successfully informing the OHU Sender with a Leave message.

The Unicast Sender is difficult to express in a traditional State Transition Diagram. But the following description should serve as a reasonable specification.

- When a Join message is received
  - If this is the first Receiver, set the Primary Receiver and move to the Alive state
  - If this is not the first Receiver, add to the Slave Receiver list and send a Slave message with this updated list to the Primary Receiver
  - In all cases send a Track and Metatext message to the Primary Receiver

<!-- -->

- When a Listen message is received
  - Identify the sending Primary or Slave Receiver and refresh their Alive timer
  - Check for expired Alive timers and modify the Primary or Slave list accordingly, possibly sending a Slave message with this updated list to the Primary Receiver

<!-- -->

- When a Leave message is received
  - Identify the sending Primary or Slave Receiver modify the Primary or Slave list accordingly, possibly sending a Slave message with this updated list to the Primary Receiver

<!-- -->

- If no more Receivers are listening, return the Waiting state

<!-- -->

- In the Alive state send all necessary Audio, Track, and Metatext messages to the Primary Receiver

A Receiver connected to a Unicast Sender implements the following state machine. It contains a mechanism for synchronizing the sending of a Leave message with the reception of an Audio message. This mechanism is designed to give the OHU Sender as much time as possible to reorganise its Slaves.

<figure>
<img src="/mediawiki/images/4/4b/Songcast_Receiver_Unicast_State_Transition_Diagram.png" title="Songcast_Receiver_Unicast_State_Transition_Diagram.png" alt="Songcast_Receiver_Unicast_State_Transition_Diagram.png" />
<figcaption aria-hidden="true">Songcast_Receiver_Unicast_State_Transition_Diagram.png</figcaption>
</figure>

**UNICAST RECEIVER STATE TRANSITION DIAGRAM**

## <span id="UPnP_Services"></span>UPnP Services

The usual way of publishing a Songcast Sender Uri is through the Metadata state variable in the [Sender service](/wiki/Av:Developer:SenderService). This should cause a Songcast Sender to be listed by those Control Points compliant with the OpenHome AV standard.

A Songcast Receiver should publish itself using the [Receiver service](/wiki/Av:Developer:ReceiverService) in conjunction with the [Product service](/wiki/Av:Developer:ReceiverService)

## <span id="Source_Code"></span>Source Code

A reference implementation of a Songcast Sender and Songcast Receiver will shortly be published, together with a complete open source UPnP stack.

## <span id="Glossary"></span>Glossary

- Binary milli-dB - 1/1024 dB
- Endpoint - an ip-address and port combination that specifies a particular application running on a networked machine.
- Multicast - one-to-many ip-based networking using a specially reserved set of addresses
- Unicast - basic point-to-point ip-based networking
{% endraw %}
