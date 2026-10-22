---
title: "Av:Developer:Scd"
permalink: "/wiki/Av:Developer:Scd"
redirect_from:
---

{% raw %}
# <span id="Songcast_Direct"></span>Songcast Direct

## <span id="Overview"></span>Overview

Songcast Direct (SCD) can be used to send decoded audio from any computing device to an OpenHome device. The Sender device is responsible for decoding audio to PCM, framing this in a simple protocol and making it available via a simple TCP server. The Receiver pulls data from this server, giving the Receiver complete control of the audio clock.

A Songcast Direct sender performs a broadly similar role to a Songcast sender. Applications that perform their own decoding to PCM will find SCD is easier to integrate and offers higher audio performance:

- There is a constant TCP connection between sender and receiver, avoiding the need for application-level resend support
- It uses the clock of the receiver, allowing for higher quality playback if the sender is on a desktop computer
- It offers the receiver limited control over the stream – initially Transport (play / pause / stop) and Volume. While the primary control UI may reside on the sender device, this allows for basic integration with any Ir handset for the receiver.

## <span id="Sample_Code"></span>Sample Code

[ohPipeline](https://github.com/openhome/ohPipeline/tree/master/OpenHome/Av/Scd) contains sample code.

`WavSender` contains an example of a trivial SCD Sender, scanning a single directory and decoding then sending any WAV files it finds. (Note that compilation of this is currently disabled. `DirScanner::Run()` contains code from an experimental precursor to C++17's `std::``filesystem::directory_iterator`. Current code is compatible with VS2013; it should only require a couple of lines of change to make this compile against any more recent compiler.)

Code in the [Scd](https://github.com/openhome/ohPipeline/tree/master/OpenHome/Av/Scd) and [Sender](https://github.com/openhome/ohPipeline/tree/master/OpenHome/Av/Scd/Sender) directories should be usable without any change. It will be possible to write a commercial quality sender using the `ScdSender` library, passing audio into `IScdSupply` and relying on the configuration of `ScdMsgFactory` to determine how much audio is buffered by the Sender.

Sample code demonstrating how a Sender can control a Receiver via ODP is coming soon. For now, see [ODP tests](https://github.com/openhome/ohPipeline/blob/master/OpenHome/Net/Odp/Tests/TestDvOdp.cpp) for a basic example.

## <span id="Discovery"></span>Discovery

### <span id="SSDP"></span>SSDP

First search for `av-openhome-org:``service:Product:2` then either

- Check `Attributes` on `Product` service for `"Transport"`
- Check `Modes` on `Transport` service for `"scd"`

or

- Check `SourceXml` on `Product` for a source with `Type` of `"scd"`

### <span id="mDNS"></span>mDNS

Search for `_openhome._odp` service to identify ODP endpoint

## <span id="Control"></span>Control

Control of the Receiver is out of band, via the standard [ OpenHome network APIs](/wiki/OhMediaDevelopers#Network_Services). These are available over UPnP or [ ODP](/wiki/OhMediaDevelopers#ODP) (a single connected socket).

## <span id="Protocol"></span>Protocol

The protocol used for communication between Sender and Receiver contains the following message types:

<table>
<thead>
<tr>
<th><p><strong>Type</strong></p></th>
<th><p><strong>Description</strong></p></th>
<th><p><strong>Sent by</strong></p></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>Ready</p></td>
<td><p>Signals availability and version support to other party</p></td>
<td><p>Receiver &amp; Sender</p></td>
</tr>
<tr>
<td><p>MetadataDidl</p></td>
<td><p>Metadata relevant until the end of the next track.<br />
Will cause the receiver to reset its reported time indicator for the audio stream.<br />
Should be sent after all Audio for any preceding track.<br />
Uses DIDL-Lite.</p></td>
<td><p>Sender</p></td>
</tr>
<tr>
<td><p>MetadataOh</p></td>
<td><p>Metadata relevant until the end of the next track.<br />
Will cause the receiver to reset its reported time indicator for the audio stream.<br />
Should be sent after all Audio for any preceding track.<br />
Uses <a href="/wiki/Av::OhMetadata"> OpenHome Metadata format</a>.</p></td>
<td><p>Sender</p></td>
</tr>
<tr>
<td><p>Format</p></td>
<td><p>Format for the following (PCM) audio. Must be sent before any audio.</p></td>
<td><p>Sender</p></td>
</tr>
<tr>
<td><p>FormatDsd</p></td>
<td><p>Format for the following (DSD) audio. Must be sent before any audio.</p></td>
<td><p>Sender</p></td>
</tr>
<tr>
<td><p>Audio</p></td>
<td><p>Decoded audio. Can only be sent after a <code>Format</code> message describing its sample rate etc.</p></td>
<td><p>Sender</p></td>
</tr>
<tr>
<td><p>MetatextDidl</p></td>
<td><p>Metadata relevant to a portion of a track.<br />
May be sent [0..n] times during a track.<br />
Uses DIDL-Lite.</p></td>
<td><p>Sender</p></td>
</tr>
<tr>
<td><p>MetatextOh</p></td>
<td><p>Metadata relevant to a portion of a track.<br />
May be sent [0..n] times during a track.<br />
Uses <a href="/wiki/Av::OhMetadata"> OpenHome Metadata format</a>. Note that a uri does not need to be specified.</p></td>
<td><p>Sender</p></td>
</tr>
<tr>
<td><p>Halt</p></td>
<td><p>Indicates that a break in audio follows. E.g. at the end of a track with no further tracks to be played, or when the Sender has paused.</p></td>
<td><p>Sender</p></td>
</tr>
<tr>
<td><p>Disconnect</p></td>
<td><p>Indicates that the originator of the message is closing its SCD session. No further audio will be available. The message receiver should disconnect its socket.</p></td>
<td><p>Receiver &amp; Sender</p></td>
</tr>
<tr>
<td><p>Seek</p></td>
<td><p>Indicates that the Receiver wants to jump to a different point in the current track.<br />
Is only sent for tracks that the Sender has indicated support seeking.</p></td>
<td><p>Receiver</p></td>
</tr>
<tr>
<td><p>Skip</p></td>
<td><p>Indicates that the Receiver wants to immediately jump to the next or previous track.</p></td>
<td><p>Receiver</p></td>
</tr>
</tbody>
</table>

A SCD session is initiated by the Sender. It instantiates a simple TCP server then instructs the Receiver to start playing from it.

The Receiver connects to the Sender and sends a `Ready` message, indicating the protocol version it supports. If the Sender is compatible with this version, it responds with a `Ready` message stating the same version. Otherwise, the Sender sends a `Ready` message stating the version it supports. If the Receiver cannot support this version, it must close the connection.

After sending a `Ready` message, the Sender should send either `Halt` (if it has nothing to send yet) or one of `MetadataDidl` or `MetadataOh` plus `Format`. The order of `Format` versus `Metadata*` is not important.

After this, the Sender should then send `Audio`. Any number of `Audio` messages can be sent until the end of the stream is reached. `Metatext` messages (either `Didl` or `Oh`) may be interleaved with `Audio`.

A `Halt` message implies that a break in audio may follow. If this break is during a stream, the Sender must have applied attenuation to samples immediately before this to avoid any audio artifacts at the break in transmission. Senders which cannot do this should implement pausing of streams using the Transport.Pause control API instead.

The details of the wire protocol are shown below. Note that all multi-byte integer values are big endian.

<table>
<thead>
<tr>
<th><p><strong>Bytes</strong></p></th>
<th><p><strong>Name</strong></p></th>
<th><p><strong>Description</strong></p></th>
</tr>
</thead>
<tbody>
<tr>
<td><p><strong>Header</strong></p></td>
<td></td>
<td><p>Prefixes to all messages below</p></td>
</tr>
<tr>
<td><p>4</p></td>
<td><p>Signature</p></td>
<td><p>0x73, 0x63, 0x64,0x20 ('scd ')</p></td>
</tr>
<tr>
<td><p>1</p></td>
<td><p>Type</p></td>
<td><p>The type of message:</p>
<ul>
<li>0 – Ready</li>
<li>1 – MetadataDidl</li>
<li>2 - MetaDataOh</li>
<li>3 – Format</li>
<li>4 – FormatDsd</li>
<li>5 – Audio</li>
<li>7 – MetatextDidl</li>
<li>8 – MetatextOh</li>
<li>9 – Halt</li>
<li>10 – Disconnect</li>
<li>11 – Seek</li>
<li>12 – Skip</li>
</ul></td>
</tr>
<tr>
<td><p>2</p></td>
<td><p>Length</p></td>
<td><p>Length in bytes of the whole message including this header</p></td>
</tr>
<tr>
<td><p>4</p></td>
<td><p>Reserved</p></td>
<td><p>Unused, reserved for future use</p></td>
</tr>
<tr>
<td><p><strong>Ready</strong></p></td>
<td></td>
<td></td>
</tr>
<tr>
<td><p>2</p></td>
<td><p>Major Version</p></td>
<td><p>1</p></td>
</tr>
<tr>
<td><p>2</p></td>
<td><p>Minor Version</p></td>
<td><p>0</p></td>
</tr>
<tr>
<td><p><strong>MetadataDidl</strong></p></td>
<td></td>
<td></td>
</tr>
<tr>
<td><p>2</p></td>
<td><p>TrackUriLength</p></td>
<td><p>Length, in bytes, of the track URI</p></td>
</tr>
<tr>
<td><p>m</p></td>
<td><p>TrackUri</p></td>
<td><p>The track URI, where m = TrackUriLength</p></td>
</tr>
<tr>
<td><p>2</p></td>
<td><p>MetadataLength</p></td>
<td><p>Length, in bytes, of the track metadata, in DIDL-Lite format</p></td>
</tr>
<tr>
<td><p>n</p></td>
<td><p>Metadata</p></td>
<td><p>The track metadata, where n = MetadataLength</p></td>
</tr>
<tr>
<td><p><strong>MetadataOh</strong></p></td>
<td></td>
<td></td>
</tr>
<tr>
<td><p>1</p></td>
<td><p>Count</p></td>
<td><p>Number of key-value pairs that follow</p></td>
</tr>
<tr>
<td><p>1</p></td>
<td><p>KeyLength</p></td>
<td><p>Length, in bytes, of the key</p></td>
</tr>
<tr>
<td><p>p</p></td>
<td><p>Key</p></td>
<td><p>Key for the metadata element, where p = KeyLength</p></td>
</tr>
<tr>
<td><p>2</p></td>
<td><p>ValueLength</p></td>
<td><p>Length, in bytes, of the value</p></td>
</tr>
<tr>
<td><p>q</p></td>
<td><p>Value</p></td>
<td><p>Value for the metadata element, where q = ValueLength</p></td>
</tr>
<tr>
<td><p>...</p></td>
<td><p>...</p></td>
<td><p>Repeat key-value pairs for all Count metadata elements</p></td>
</tr>
<tr>
<td><p><strong>Format</strong></p></td>
<td></td>
<td></td>
</tr>
<tr>
<td><p>1</p></td>
<td><p>BitDepth</p></td>
<td><p>Bit depth of the following audio</p></td>
</tr>
<tr>
<td><p>4</p></td>
<td><p>SampleRate</p></td>
<td><p>Sample rate of the following audio</p></td>
</tr>
<tr>
<td><p>1</p></td>
<td><p>Channels</p></td>
<td><p>Number of channels of the following audio</p></td>
</tr>
<tr>
<td><p>4</p></td>
<td><p>BitRate</p></td>
<td><p>Bit rate of the following audio</p></td>
</tr>
<tr>
<td><p>8</p></td>
<td><p>SampleStart</p></td>
<td><p>Sample position of the first sample in the next <code>Audio</code> message</p></td>
</tr>
<tr>
<td><p>8</p></td>
<td><p>SamplesTotal</p></td>
<td><p>Total number of samples in the following audio (requirement for this to be confirmed)</p></td>
</tr>
<tr>
<td><p>1</p></td>
<td><p>Flags</p></td>
<td><ul>
<li>Bit 0 - Seekable</li>
<li>Bit 1 - Lossless</li>
<li>Bit 2 - Live (content generated upstream of the Sender, e.g. internet radio)</li>
<li>Bit 3 - Broadcastable (whether the Receiver is allowed to offer the following audio via any multi-room protocols</li>
<li>Bits 4-7 - Reserved. Must be zero.</li>
</ul></td>
</tr>
<tr>
<td><p>1</p></td>
<td><p>CodecNameLength</p></td>
<td><p>Length, in bytes, of the codec name</p></td>
</tr>
<tr>
<td><p>r</p></td>
<td><p>CodecName</p></td>
<td><p>The codec name, where r = CodecNameLength</p></td>
</tr>
<tr>
<td><p><strong>FormatDsd</strong></p></td>
<td></td>
<td></td>
</tr>
<tr>
<td><p>4</p></td>
<td><p>SampleRate</p></td>
<td><p>Sample rate of the following audio</p></td>
</tr>
<tr>
<td><p>1</p></td>
<td><p>Channels</p></td>
<td><p>Number of channels of the following audio</p></td>
</tr>
<tr>
<td><p>2</p></td>
<td><p>SampleBlockBits</p></td>
<td><p>Block size (in bits) of DSD data. 2 for stereo where left/right channels are interleaved, 16 for stereo with one byte of left subsamples followed by one byte of right subsamples, etc.</p></td>
</tr>
<tr>
<td><p>8</p></td>
<td><p>SampleStart</p></td>
<td><p>Sample position of the first sample in the next <code>Audio</code> message</p></td>
</tr>
<tr>
<td><p>8</p></td>
<td><p>SamplesTotal</p></td>
<td><p>Total number of samples in the following audio (requirement for this to be confirmed)</p></td>
</tr>
<tr>
<td><p>1</p></td>
<td><p>Flags</p></td>
<td><ul>
<li>Bit 0 - Seekable</li>
<li>Bit 1-2 - Reserved. Must be zero.</li>
<li>Bit 3 - Broadcastable (whether the Receiver is allowed to offer the following audio via any multi-room protocols</li>
<li>Bits 4-7 - Reserved. Must be zero.</li>
</ul></td>
</tr>
<tr>
<td><p>1</p></td>
<td><p>CodecNameLength</p></td>
<td><p>Length, in bytes, of the codec name</p></td>
</tr>
<tr>
<td><p>r</p></td>
<td><p>CodecName</p></td>
<td><p>The codec name, where r = CodecNameLength</p></td>
</tr>
<tr>
<td><p><strong>Audio</strong></p></td>
<td></td>
<td></td>
</tr>
<tr>
<td><p>2</p></td>
<td><p>NumSamples</p></td>
<td><p>The number of audio samples in this message</p></td>
</tr>
<tr>
<td><p>s</p></td>
<td><p>AudioData</p></td>
<td><p>Audio data. Where s = NumSamples * (BitDepth/8) * NumChannels.<br />
Multi-channel audio must supply data sample at a time, with left channel first. Audio is packed (i.e. no padding bytes rounding samples up to 32-bit boundaries) and big endian.</p></td>
</tr>
<tr>
<td><p><strong>MetatextDidl</strong></p></td>
<td></td>
<td></td>
</tr>
<tr>
<td><p>2</p></td>
<td><p>Metatext Length</p></td>
<td><p>Length, in bytes, of the metatext, in DIDL-Lite format</p></td>
</tr>
<tr>
<td><p>n</p></td>
<td><p>Metatext</p></td>
<td><p>The metatext, where n = MetatextLength</p></td>
</tr>
<tr>
<td><p><strong>MetatextOh</strong></p></td>
<td></td>
<td></td>
</tr>
<tr>
<td><p>1</p></td>
<td><p>Count</p></td>
<td><p>Number of key-value pairs that follow</p></td>
</tr>
<tr>
<td><p>1</p></td>
<td><p>KeyLength</p></td>
<td><p>Length, in bytes, of the key</p></td>
</tr>
<tr>
<td><p>p</p></td>
<td><p>Key</p></td>
<td><p>Key for the metatext element, where p = KeyLength</p></td>
</tr>
<tr>
<td><p>2</p></td>
<td><p>ValueLength</p></td>
<td><p>Length, in bytes, of the value</p></td>
</tr>
<tr>
<td><p>q</p></td>
<td><p>Value</p></td>
<td><p>Value for the metatext element, where q = ValueLength</p></td>
</tr>
<tr>
<td><p>...</p></td>
<td><p>...</p></td>
<td><p>Repeat key-value pairs for all Count metatext elements</p></td>
</tr>
<tr>
<td><p><strong>Halt</strong></p></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td><p>No message body (only header required)</p></td>
</tr>
<tr>
<td><p><strong>Disconnect</strong></p></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td><p>No message body (only header required)</p></td>
</tr>
<tr>
<td><p><strong>Seek</strong></p></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td><p>To be confirmed</p></td>
</tr>
<tr>
<td><p><strong>Skip</strong></p></td>
<td></td>
<td></td>
</tr>
<tr>
<td></td>
<td></td>
<td><p>To be confirmed</p></td>
</tr>
</tbody>
</table>
{% endraw %}
