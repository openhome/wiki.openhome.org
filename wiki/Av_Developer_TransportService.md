---
title: "Av:Developer:TransportService"
permalink: "/wiki/Av:Developer:TransportService"
redirect_from:
---

{% raw %}
# <span id="Transport_Service"></span>Transport Service

## <span id="Overview"></span>Overview

The Transport service provides source-independent control of play, pause, stop, skip and seek.

If a device's [ Product](/wiki/Av:Developer:ProductService) service reports an attribute `"Transport"`, then that device is guaranteed to bear the Transport service. If the Transport service is available, all its properties and actions must be fully implemented.

## <span id="Evented_Properties"></span>Evented Properties

### <span id="Modes"></span>Modes

List of available modes (JSON array of strings).

### <span id="CanSkipNext"></span>CanSkipNext

`true` if the `SkipNext` action is currently available; `false` otherwise.

Any mode that is sometimes capable of changing stream as a consequence of `SkipNext` will always report `CanSkipNext` as `true`.

### <span id="CanSkipPrevious"></span>CanSkipPrevious

`true` if the `SkipPrevious` action is currently available; `false` otherwise.

Any mode that is sometimes capable of changing stream as a consequence of `SkipPrevious` will always report `CanSkipPrevious` as `true`.

### <span id="CanRepeat"></span>CanRepeat

`true` if the `SetRepeat` action is currently available; `false` otherwise.

### <span id="CanShuffle"></span>CanShuffle

`true` if the `SetShuffle` action is currently available; `false` otherwise.

### <span id="StreamId"></span>StreamId

Integer id, uniquely identifying the current stream.

### <span id="CanSeek"></span>CanSeek

`true` if the `SeekSecondAbsolute` and `SeekSecondRelative` actions are available for the current stream; `false` otherwise.

### <span id="CanPause"></span>CanPause

`true` if the stream can be paused (so is not being played at a rate determined by a remote sender); `false` otherwise.

### <span id="TransportState"></span>TransportState

One of

- `Playing`
- `Paused`
- `Stopped`
- `Buffering`
- `Waiting`

### <span id="Repeat"></span>Repeat

`true` if repeat mode is currently enabled; `false` otherwise.

### <span id="Shuffle"></span>Shuffle

`true` if shuffle mode is currently enabled; `false` otherwise.

## <span id="Actions"></span>Actions

### <span id="PlayAs"></span>PlayAs

`Arguments: (in string mode, in string command)`  
Start a new stream playing, specifying both a mode (source) to be used and a mode-specific command which describes the track to be played. Common options for [ modes and commands](/wiki/Av:Developer:TransportPlayAsCommands) are documented separately.

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

`Arguments: None`  
Move to the next stream (i.e. skip forwards). Determination of what comes next may vary between sources/modes. If `TransportState` is `Stopped` or `Paused`, try to start playing.

### <span id="Previous"></span>Previous

`Arguments: None`  
Move to the previous stream (i.e. skip backwards). If `TransportState` is `Stopped` or `Paused`, try to start playing.

Returns a `801` fault code if the current channel does not support skipping backwards.

### <span id="SetRepeat"></span>SetRepeat

`Arguments: (in uint repeat)`  
Sets the Repeat state of the device, affecting all sources that are capable of implementing a repeat feature.

### <span id="SetShuffle"></span>SetShuffle

`Arguments: (in uint shuffle)`  
Sets the Shuffle state of the device, affecting all sources that are capable of implementing a randomise feature.

### <span id="SeekSecondAbsolute"></span>SeekSecondAbsolute

`Arguments: (in uint streamId, in uint secondsAbsolute)`  
Seek to an absolute position in the current stream. If `TransportState` is `Stopped` or `Paused`, try to start playing.

Returns a `803` fault code if the seek is not possible.

### <span id="SeekSecondRelative"></span>SeekSecondRelative

`Arguments: (in uint streamId, in int secondsRelative)`  
Seek to a position relative to what's currently playing in the current stream. If `TransportState` is `Stopped` or `Paused`, try to start playing.

Returns a `803` fault code if the seek is not possible.

### <span id="TransportState_2"></span>TransportState

`Arguments: (out string state)`  
Read the current value of the TransportState property.

### <span id="Modes_2"></span>Modes

`Arguments: (out string modes)`  
Return the value of the `Modes` property.

### <span id="ModeInfo"></span>ModeInfo

`Arguments: (out string mode, out bool canSkipNext, out bool canSkipPrevious, out bool canRepeat, out bool canShuffle)`  
Reports the values of the `Mode`, `CanSkipNext`, `CanSkipPrev`, `CanRepeat` and `CanShuffle` properties.

### <span id="StreamInfo"></span>StreamInfo

`Arguments:`  
`(out uint streamId, out bool seekable, out bool pausable)`

Reports current stream information:

- `StreamId`
- `Seekable`
- `Pausable`

### <span id="StreamId_2"></span>StreamId

`Arguments: (out uint streamId)`  
Read the current value of the `StreamId` property.

### <span id="Repeat_2"></span>Repeat

`Arguments: (out uint repeat)`  
Read the current value of the `Repeat` property.

### <span id="Shuffle_2"></span>Shuffle

`Arguments: (out uint shuffle)`  
Read the current value of the `Shuffle` property.

## <span id="UPnP_Service_Description"></span>UPnP Service Description

For devices supporting the UPnP protocol, the service description is

`name: "Transport"`  
`domain: "av.openhome.org"`  
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
      <argumentList>
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
      </argumentList>
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
      <name>SkipNext</name>
    </action>
    <action>
      <name>SkipPrevious</name>
    </action>
    <action>
      <name>SetRepeat</name>
      <argumentList>
        <argument>
          <name>Repeat</name>
          <direction>in</direction>
          <relatedStateVariable>Repeat</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SetShuffle</name>
      <argumentList>
        <argument>
          <name>Shuffle</name>
          <direction>in</direction>
          <relatedStateVariable>Shuffle</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SeekSecondAbsolute</name>
      <argumentList>
        <argument>
          <name>StreamId</name>
          <direction>in</direction>
          <relatedStateVariable>StreamId</relatedStateVariable>
        </argument>
        <argument>
          <name>SecondAbsolute</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_uint</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SeekSecondRelative</name>
      <argumentList>
        <argument>
          <name>StreamId</name>
          <direction>in</direction>
          <relatedStateVariable>StreamId</relatedStateVariable>
        </argument>
        <argument>
          <name>SecondRelative</name>
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
      <name>ModeInfo</name>
      <argumentList>
        <argument>
          <name>CanSkipNext</name>
          <direction>out</direction>
          <relatedStateVariable>CanSkipNext</relatedStateVariable>
        </argument>
        <argument>
          <name>CanSkipPrevious</name>
          <direction>out</direction>
          <relatedStateVariable>CanSkipPrevious</relatedStateVariable>
        </argument>
        <argument>
          <name>CanRepeat</name>
          <direction>out</direction>
          <relatedStateVariable>CanRepeat</relatedStateVariable>
        </argument>
        <argument>
          <name>CanShuffle</name>
          <direction>out</direction>
          <relatedStateVariable>CanShuffle</relatedStateVariable>
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
          <name>CanSeek</name>
          <direction>out</direction>
          <relatedStateVariable>CanSeek</relatedStateVariable>
        </argument>
        <argument>
          <name>CanPause</name>
          <direction>out</direction>
          <relatedStateVariable>CanPause</relatedStateVariable>
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
      <name>Repeat</name>
      <argumentList>
        <argument>
          <name>Repeat</name>
          <direction>out</direction>
          <relatedStateVariable>Repeat</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Shuffle</name>
      <argumentList>
        <argument>
          <name>Shuffle</name>
          <direction>out</direction>
          <relatedStateVariable>Shuffle</relatedStateVariable>
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
      <name>CanSkipNext</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>CanSkipPrevious</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>CanRepeat</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>CanShuffle</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>StreamId</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>CanSeek</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>CanPause</name>
      <dataType>boolean</dataType>
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
    <stateVariable sendEvents="yes">
      <name>Repeat</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Shuffle</name>
      <dataType>boolean</dataType>
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
