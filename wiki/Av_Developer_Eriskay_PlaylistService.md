---
title: "Av:Developer:Eriskay:PlaylistService"
permalink: "/wiki/Av:Developer:Eriskay:PlaylistService"
redirect_from:
---

{% raw %}
# <span id="Playlist_Service"></span>Playlist Service

## <span id="Overview"></span>Overview

The Playlist service provides access to a list of tracks, which can be played in sequence, starting at any point. ‘Shuffle’ and ‘Repeat’ modes also exist, allowing track order to be randomised and playback to loop.

If a device's [ Product](/wiki/Av:Developer:Eriskay:ProductService) service reports a source of type `"Playlist"`, then that device is guaranteed to bear the Playlist service. If the Playlist service is available, all its properties and actions must be fully implemented.

## <span id="Evented_Properties"></span>Evented Properties

### <span id="Repeat"></span>Repeat

By default a playlist plays each track in sequence then stops after playing the final track. Setting the `Repeat` property changes this behaviour to loop from the last track back to the first, playing it immediately.

By default, `Repeat` is off.

### <span id="Shuffle"></span>Shuffle

Tracks are played in random order if the `Shuffle` property is enabled. As with normal playback, each track is played once then the playlist stops. If `Shuffle` is enabled mid-way through a playlist, each track in the list is shuffled, including any that have just been played.

When combined with `Repeat`, each track is played once before any track is played for a second time.

By default, `Shuffle` is off.

### <span id="Id"></span>Id

The id of the current track (the track currently playing or that would be played if the `Transport.Play` action was invoked while this source was active). Or `0` if the playlist is empty.

### <span id="IdArray"></span>IdArray

A JSON integer array containing the ids of the tracks currently in the playlist.

For example, `[2, 276, 19]` describes a playlist containing track ids 2, 276, and 19 in that order.

Contains `[0..TracksMax]` elements.

### <span id="TracksMax"></span>TracksMax

The maximum number of tracks a playlist can contain. Set on startup and invariant thereafter.

## <span id="Actions"></span>Actions

### <span id="SetRepeat"></span>SetRepeat

`Arguments: (in bool repeat)`  
Enable or disable repeat mode.

### <span id="Repeat_2"></span>Repeat

`Arguments: (out bool repeat)`  
Report whether repeat mode is enabled.

### <span id="SetShuffle"></span>SetShuffle

`Arguments: (out bool shuffle)`  
Enable or disable shuffle mode.

### <span id="Shuffle_2"></span>Shuffle

`Arguments: (in bool shuffle)`  
Report whether shuffle mode is enabled.

### <span id="Id_2"></span>Id

`Arguments: (out uint id)`  
Return the value of the `Id` state variable.

### <span id="ReadList"></span>ReadList

`Arguments: (in string ids, out string json)`  
Given a space separated list of track ids, report their associated uri and metadata in the following JSON form: <tt>

`   [`  
`       {`  
`           "id": integer_id,`  
`           "uri": "track_uri",`  
`           "metadata": "track_metadata"`  
`       },`  
`       {`  
`           "id": integer_id,`  
`           "uri": "track_uri",`  
`           "metadata": "track_metadata"`  
`       }`  
`   ]`

</tt> Any ids not in the playlist are ignored.

### <span id="Insert"></span>Insert

`Arguments: (in uint afterId, in string uri, in string metadata, out uint newId)`  
Adds the given uri and metadata as a new track to the playlist.

Set the `AfterId` argument to `0` to insert a track at the start of the playlist.

Reports a `800` fault code if `AfterId` is not `0` and doesn’t appear in the playlist.  
Reports a `801` fault code if the playlist is full (i.e. already contains `TracksMax` tracks).

### <span id="DeleteList"></span>DeleteList

`Arguments: (int string ids)`  
Given a space separated list of track ids, remove the tracks with these ids from the playlist.

If the id to be deleted is currently playing, the next track becomes current.

Any ids not in the playlist are silently ignored.

### <span id="DeleteAll"></span>DeleteAll

`Arguments: None`  
Delete all tracks from the playlist.

## <span id="Move"></span>Move

`Arguments: (in string ids, in uint afterId)`  
Move a space separated list of ids.

Set `AfterId` to `0` to move the tracks to the start of the playlist.

Any ids not in the playlist are silently ignored.

`AfterId` must not also be in the list to be moved.

### <span id="TracksMax_2"></span>TracksMax

`Arguments: (out uint max)`  
Return the value of the `TracksMax` property.

### <span id="IdArray_2"></span>IdArray

`Arguments: (out uint token, out string json)`  
Return the value of the `IdArray` property. Supports polling implementations by returning a token which can be used with the `IdArrayChanged` action.

### <span id="IdArrayChanged"></span>IdArrayChanged

`Arguments: (in uint token, out bool changed)`  
Check to see if `IdArray` has changed since gathering the specified token. This token must have been previously collected from the `IdArray` action.

This mechanism is provided specifically for any basic control points unable to partake in standard eventing.

## <span id="UPnP_Service_Description"></span>UPnP Service Description

For devices supporting the UPnP protocol, the service description is

`name: "Playlist"`  
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
      <name>Shuffle</name>
      <argumentList>
        <argument>
          <name>Shuffle</name>
          <direction>out</direction>
          <relatedStateVariable>Shuffle</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Id</name>
      <argumentList>
        <argument>
          <name>Id</name>
          <direction>out</direction>
          <relatedStateVariable>Id</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>ReadList</name>
      <argumentList>
        <argument>
          <name>IdList</name>
          <direction>in</direction>
          <relatedStateVariable>IdList</relatedStateVariable>
        </argument>
        <argument>
          <name>TrackList</name>
          <direction>out</direction>
          <relatedStateVariable>TrackList</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Insert</name>
      <argumentList>
        <argument>
          <name>AfterId</name>
          <direction>in</direction>
          <relatedStateVariable>Id</relatedStateVariable>
        </argument>
        <argument>
          <name>Uri</name>
          <direction>in</direction>
          <relatedStateVariable>Uri</relatedStateVariable>
        </argument>
        <argument>
          <name>Metadata</name>
          <direction>in</direction>
          <relatedStateVariable>Metadata</relatedStateVariable>
        </argument>
        <argument>
          <name>NewId</name>
          <direction>out</direction>
          <relatedStateVariable>Id</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Move</name>
      <argumentList>
        <argument>
          <name>AfterId</name>
          <direction>in</direction>
          <relatedStateVariable>Id</relatedStateVariable>
        </argument>
        <argument>
          <name>IdList</name>
          <direction>in</direction>
          <relatedStateVariable>IdList</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>DeleteList</name>
      <argumentList>
        <argument>
          <name>IdList</name>
          <direction>in</direction>
          <relatedStateVariable>IdList</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>DeleteAll</name>
    </action>
    <action>
      <name>TracksMax</name>
      <argumentList>
        <argument>
          <name>TracksMax</name>
          <direction>out</direction>
          <relatedStateVariable>TracksMax</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>IdArray</name>
      <argumentList>
        <argument>
          <name>Token</name>
          <direction>out</direction>
          <relatedStateVariable>IdArrayToken</relatedStateVariable>
        </argument>
        <argument>
          <name>Array</name>
          <direction>out</direction>
          <relatedStateVariable>IdArray</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>IdArrayChanged</name>
      <argumentList>
        <argument>
          <name>Token</name>
          <direction>in</direction>
          <relatedStateVariable>IdArrayToken</relatedStateVariable>
        </argument>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>IdArrayChanged</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
  </actionList>
  <serviceStateTable>
    <stateVariable sendEvents="yes">
      <name>Repeat</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Shuffle</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Id</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>IdArray</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>TracksMax</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>IdList</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>TrackList</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>Uri</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>Metadata</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>IdArrayToken</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>IdArrayChanged</name>
      <dataType>boolean</dataType>
    </stateVariable>
  </serviceStateTable>
</scpd>
```
{% endraw %}
