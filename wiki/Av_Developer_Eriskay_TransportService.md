---
title: "Av:Developer:Eriskay:TransportService"
permalink: "/wiki/Av:Developer:Eriskay:TransportService"
redirect_from:
---

{% raw %}
# <span id="Transport_Service"></span>Transport Service

## <span id="Overview"></span>Overview

The Transport service provides both source-independent control of play, pause, stop, skip and seek and information concerning the currently playing media.

Summary information is provided in a number of levels, each of which have a URI and metadata in OpenHome Metadata format. E.g. A (notional) internet radio service that broadcast information about the currently playing track may have a level describing the radio station then another level describing the track. Control points with limited screen estate may choose to display the most derived level(s) of metadata that are available.

In addition to a hierarchy of metadata, detailed information such as bit-rate, sample-rate, bit-depth is available describing what is currently playing.

If a device's [ Product](/wiki/Av:Developer:Eriskay:ProductService) service reports an attribute `"Transport"`, then that device is guaranteed to bear the Transport service. If the Transport service is available, all its properties and actions must be fully implemented.

## <span id="Evented_Properties"></span>Evented Properties

### <span id="Modes"></span>Modes

Space separated list of available modes.

### <span id="LevelCount"></span>LevelCount

The number of levels of information (uri / metadata) provided by this device. Does not vary at run-time.

### <span id="Mode"></span>Mode

The currently active mode

### <span id="SequenceNumbers"></span>SequenceNumbers

A space-separated list of integers that change when their associated uri and/or metadata are updated. A value of `0` implies that both the associated uri and metadata are empty.

### <span id="StreamCount"></span>StreamCount

Changes when each new stream is played.

Indicates a change in one or more stream encoding parameters (`Duration`, `Seekable`, `Pausable`, `BitRate`, `BitDepth`, `SampleRate`, `Lossless`, `CodecName`).

A value of `0` can be assumed to imply empty/`0`/`false` values for all stream-specific data.

### <span id="MetatextCount"></span>MetatextCount

Changes whenever metatext changes.

### <span id="NextAvailable"></span>NextAvailable

`true` if the `Next` (skip forwards) action is currently available; `false` otherwise.

This will only change when `Mode` changes. A mode that is sometimes capable of changing stream as a consequence of `Next` will always report `NextAvailable` as `true`.

### <span id="PrevAvailable"></span>PrevAvailable

`true` if the `Prev` (skip backwards) action is currently available; `false` otherwise.

This will only change when `Mode` changes. A mode that is sometimes capable of changing stream as a consequence of `Prev` will always report `PrevAvailable` as `true`.

### <span id="StreamId"></span>StreamId

Integer id, uniquely identifying the current stream.

### <span id="Duration"></span>Duration

The length of the currently playing stream in seconds.

### <span id="Seekable"></span>Seekable

`true` if the `SeekSecondsAbsolute` and `SeekSecondsRelative` actions are available for the current stream; `false` otherwise.

### <span id="Pausable"></span>Pausable

`true` if the stream can be paused (so is not being played at a rate determined by a remote sender); `false` otherwise.

### <span id="BitRate"></span>BitRate

Dataflow rate in bits per second of the currently playing stream in its encoded representation.

### <span id="BitDepth"></span>BitDepth

Sample (data) resolution in bits per channel sample of the currently playing stream.

### <span id="SampleRate"></span>SampleRate

Time resolution of samples per second in kHz of the currently playing stream.

### <span id="Lossless"></span>Lossless

Indication of whether the currently playing stream can be decoded (decompressed) to a bit-accurate representation of the original audio data (lossless) or merely to a good approximation (lossy encoding).

### <span id="CodecName"></span>CodecName

Shorthand name for the audio encoding and container format used to represent the currently playing stream (e.g. AAC).

### <span id="Metatext"></span>Metatext

Additional textual information (if any) associated with the currently playing stream.

### <span id="TransportState"></span>TransportState

One of

- `Playing`
- `Paused`
- `Stopped`
- `Buffering`
- `Waiting`

## <span id="Actions"></span>Actions

### <span id="PlayAs"></span>PlayAs

`Arguments: (in string mode, in string command)`  
Start a new stream playing, specifying both a mode (source) to be used and a mode-specific command which describes the track to be played. Common options for [ modes and commands](/wiki/Av:Developer:Eriskay:TransportPlayAsCommands) are documented separately.

### <span id="Play"></span>Play

`Arguments: None`  
Start a pending stream playing.

A stream must be ready to play. Possibly via calls to another network service.

Behaviour when a stream is already playing varies depending on the active modes (source).

### <span id="Pause"></span>Pause

`Arguments: None`  
Pause the current stream.

Returns a `801` fault code if the current channel does not support being paused (is being played at a rate determined by a remote sender).

### <span id="Stop"></span>Stop

`Arguments: None` Stop the current stream.

### <span id="Next"></span>Next

`Arguments: (in uint streamId)`  
Move to the next stream (i.e. skip forwards). Determination of what comes next may vary between sources/modes. If `TransportState` is `Stopped` or `Paused`, try to start playing.

Returns a `801` fault code if the current channel does not support skipping forwards.

### <span id="Prev"></span>Prev

`Arguments: (in uint streamId)`  
Move to the previous stream (i.e. skip backwards). If `TransportState` is `Stopped` or `Paused`, try to start playing.

Returns a `801` fault code if the current channel does not support skipping backwards.

### <span id="SeekSecondsAbsolute"></span>SeekSecondsAbsolute

`Arguments: (in uint streamId, in uint secondsAbsolute)`  
Seek to an absolute position in the current stream. If `TransportState` is `Stopped` or `Paused`, try to start playing.

Returns a `801` fault code if the current stream does not support seek.  
Returns a `803` fault code if the seek position is beyond the end of the stream.

### <span id="SeekSecondsRelative"></span>SeekSecondsRelative

`Arguments: (in uint streamId, in int secondsRelative)`  
Seek to a position relative to what's currently playing in the current stream. If `TransportState` is `Stopped` or `Paused`, try to start playing.

Returns a `801` fault code if the current stream does not support seek.  
Returns a `803` fault code if the seek position is beyond the end of the stream.

### <span id="TransportState_2"></span>TransportState

`Arguments: (out string state)`  
Read the current value of the TransportState property.

### <span id="Modes_2"></span>Modes

`Arguments: (out string modes)`  
Return the value of the `Modes` property.

### <span id="Counters"></span>Counters

`Arguments: (out string seq, out uint stream, out uint metatext)`  
Read the values of the sequence numbers associated with each level of information plus the counters for current stream details.

### <span id="ModeInfo"></span>ModeInfo

`Arguments: (out string mode, out bool nextAvailable, out bool prevAvailable)`  
Reports the values of the `Mode`, `NextAvailable` and `PrevAvailable` properties.

### <span id="LevelInfo"></span>LevelInfo

`Arguments: (in uint index, out string uri, out string metadata)`  
Reports uri & metadata for the specified level (a zero-based index into the `SequenceNumbers` array).

### <span id="StreamInfo"></span>StreamInfo

`Arguments:`  
`(out uint streamId, out string uri, out bool seekable, out bool pausable, out uint durationSecs, out uint bitRate, out uint bitDepth, out uint SampleRate, out bool lossless, out string codec)`

Reports current stream information:

- `StreamId`
- `Uri`
- `Seekable`
- `Pausable`
- `Duration`
- `BitRate`
- `BitDepth`
- `SampleRate`
- `Lossless`
- `CodecName`

### <span id="StreamId_2"></span>StreamId

`Arguments: (out uint streamId)`  
Read the current value of the `StreamId` property.

### <span id="Metatext_2"></span>Metatext

`Arguments: (out string text)`  
Read the current value of the `Metatext` property.

## <span id="UPnP_Service_Description"></span>UPnP Service Description

For devices supporting the UPnP protocol, the service description is

`name: "Transport"`  
`domain: "openhome.org.eriskay"`  
`version: "1"`

``` xml
<?xml version="1.0" encoding="utf-8"?>
<scpd xmlns="urn:schemas-upnp-org:service-1-0">
  <specVersion>
    <major>1</major>
    <minor>0</minor>
  </specVersion>

  <actionList>
    <action>
      <name>PlayAs</name>
      <argument>
        <name>Mode</name>
        <direction>in</direction>
        <relatedStateVariable>A_ARG_TYPE_string</relatedStateVariable>
      </argument>
      <argument>
        <name>Command</name>
        <direction>in</direction>
        <relatedStateVariable>A_ARG_TYPE_string</relatedStateVariable>
      </argument>
    </action>
    <action>
      <name>Play</name>
    </action>
    <action>
      <name>Pause</name>
    </action>
    <action>
      <name>Stop</name>
    </action>
    <action>
      <name>Next</name>
      <argumentList>
        <argument>
          <name>StreamId</name>
          <direction>in</direction>
          <relatedStateVariable>StreamId</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Prev</name>
      <argumentList>
        <argument>
          <name>StreamId</name>
          <direction>in</direction>
          <relatedStateVariable>StreamId</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SeekSecondsAbsolute</name>
      <argumentList>
        <argument>
          <name>StreamId</name>
          <direction>in</direction>
          <relatedStateVariable>StreamId</relatedStateVariable>
        </argument>
        <argument>
          <name>SecondsAbsolute</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_uint</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SeekSecondsRelative</name>
      <argumentList>
        <argument>
          <name>StreamId</name>
          <direction>in</direction>
          <relatedStateVariable>StreamId</relatedStateVariable>
        </argument>
        <argument>
          <name>SecondsRelative</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_int</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>TransportState</name>
      <argumentList>
        <argument>
          <name>State</name>
          <direction>out</direction>
          <relatedStateVariable>TransportState</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Modes</name>
      <argumentList>
        <argument>
          <name>Modes</name>
          <direction>out</direction>
          <relatedStateVariable>Modes</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Counters</name>
      <argumentList>
        <argument>
          <name>SequenceNumbers</name>
          <direction>out</direction>
          <relatedStateVariable>SequenceNumbers</relatedStateVariable>
        </argument>
        <argument>
          <name>StreamCount</name>
          <direction>out</direction>
          <relatedStateVariable>StreamCount</relatedStateVariable>
        </argument>
        <argument>
          <name>MetatextCount</name>
          <direction>out</direction>
          <relatedStateVariable>MetatextCount</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>LevelInfo</name>
      <argumentList>
        <argument>
          <name>Index</name>
          <direction>out</direction>
          <relatedStateVariable>A_ARG_TYPE_uint</relatedStateVariable>
        </argument>
        <argument>
          <name>Uri</name>
          <direction>out</direction>
          <relatedStateVariable>A_ARG_TYPE_string</relatedStateVariable>
        </argument>
        <argument>
          <name>Metadata</name>
          <direction>out</direction>
          <relatedStateVariable>A_ARG_TYPE_string</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>ModeInfo</name>
      <argumentList>
        <argument>
          <name>Mode</name>
          <direction>out</direction>
          <relatedStateVariable>Mode</relatedStateVariable>
        </argument>
        <argument>
          <name>NextAvailable</name>
          <direction>out</direction>
          <relatedStateVariable>NextAvailable</relatedStateVariable>
        </argument>
        <argument>
          <name>PrevAvailable</name>
          <direction>out</direction>
          <relatedStateVariable>PrevAvailable</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>StreamInfo</name>
      <argumentList>
        <argument>
          <name>StreamId</name>
          <direction>out</direction>
          <relatedStateVariable>StreamId</relatedStateVariable>
        </argument>
        <argument>
          <name>Uri</name>
          <direction>out</direction>
          <relatedStateVariable>A_ARG_TYPE_string</relatedStateVariable>
        </argument>
        <argument>
          <name>Seekable</name>
          <direction>out</direction>
          <relatedStateVariable>Seekable</relatedStateVariable>
        </argument>
        <argument>
          <name>Pausable</name>
          <direction>out</direction>
          <relatedStateVariable>Pausable</relatedStateVariable>
        </argument>
        <argument>
          <name>Duration</name>
          <direction>out</direction>
          <relatedStateVariable>Duration</relatedStateVariable>
        </argument>
        <argument>
          <name>BitRate</name>
          <direction>out</direction>
          <relatedStateVariable>BitRate</relatedStateVariable>
        </argument>
        <argument>
          <name>BitDepth</name>
          <direction>out</direction>
          <relatedStateVariable>BitDepth</relatedStateVariable>
        </argument>
        <argument>
          <name>SampleRate</name>
          <direction>out</direction>
          <relatedStateVariable>SampleRate</relatedStateVariable>
        </argument>
        <argument>
          <name>Lossless</name>
          <direction>out</direction>
          <relatedStateVariable>Lossless</relatedStateVariable>
        </argument>
        <argument>
          <name>CodecName</name>
          <direction>out</direction>
          <relatedStateVariable>CodecName</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>StreamId</name>
      <argumentList>
        <argument>
          <name>StreamId</name>
          <direction>out</direction>
          <relatedStateVariable>StreamId</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Metatext</name>
      <argumentList>
        <argument>
          <name>Metatext</name>
          <direction>out</direction>
          <relatedStateVariable>Metatext</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
  </actionList>

  <serviceStateTable>
    <stateVariable sendEvents="yes">
      <name>Modes</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>LevelCount</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Mode</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>SequenceNumbers</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>StreamCount</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>MetatextCount</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>NextAvailable</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>PrevAvailable</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>StreamId</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Duration</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Seekable</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Pausable</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>BitRate</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>BitDepth</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>SampleRate</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Lossless</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>CodecName</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Metatext</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>TransportState</name>
      <dataType>string</dataType>
      <allowedValueList>
        <allowedValue>Playing</allowedValue>
        <allowedValue>Paused</allowedValue>
        <allowedValue>Stopped</allowedValue>
        <allowedValue>Buffering</allowedValue>
        <allowedValue>Waiting</allowedValue>
      </allowedValueList>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>A_ARG_TYPE_uint</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>A_ARG_TYPE_int</name>
      <dataType>i4</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>A_ARG_TYPE_string</name>
      <dataType>string</dataType>
    </stateVariable>
  </serviceStateTable>
</scpd>
```
{% endraw %}
