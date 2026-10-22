---
title: "Av:Developer:PlaylistService"
permalink: "/wiki/Av:Developer:PlaylistService"
redirect_from:
  - "/wiki/Developer:PlaylistService"
---

{% raw %}
# <span id="Overview"></span>Overview

The Playlist service provides access to a list of tracks, which can be played in sequence, starting at any point. ‘Shuffle’ and ‘Repeat’ modes also exist, allowing track order to be randomised and playback to loop.  
If a device's [Product](/wiki/Av:Developer:ProductService) service reports a source of type 'Playlist', then that device is guaranteed to bear the Playlist service.

# <span id="State_Variables"></span>State Variables

## <span id="TransportState"></span>TransportState

One of `Stopped`, `Playing`, `Paused` or `Buffering`.

## <span id="Repeat"></span>Repeat

By default a playlist plays each track in sequence then stops after playing the final track. Setting the `Repeat` property changes this behaviour to loop from the last track back to the first, playing it immediately. The `Next` and `Previous` actions also vary their behaviour according to this property at the ends of a playlist.  
By default, `Repeat` is off.

## <span id="Shuffle"></span>Shuffle

Tracks are played in random order if the `Shuffle` property is enabled. As with normal playback, each track is played once then the playlist stops. If `Shuffle` is enabled mid-way through a playlist, each track in the list is shuffled, including any that have just been played.  
When combined with `Repeat`, each track is played once before any track is played for a second time.  
By default, `Shuffle` is off.

## <span id="Id"></span>Id

The id of the current track (the track currently playing or that would be played if the `Play` action was invoked). Or `0` if the playlist is empty.

## <span id="IdArray"></span>IdArray

An [IdArray](/wiki/Developer:IdArray) containing the ids of the tracks currently in the playlist. Contains `[0.. TracksMax]` elements.

## <span id="TracksMax"></span>TracksMax

The maximum number of tracks a playlist can contain. Set on startup and invariant thereafter.

## <span id="ProtocolInfo"></span>ProtocolInfo

Audio formats and networking protocols supported by the device. Will be the same as reported by [Radio](/wiki/Av:Developer:RadioService) and `AVTransport` if these services are present. Set on startup and invariant thereafter.

# <span id="Actions"></span>Actions

## <span id="Play"></span>Play

If `TransportState` is `Stopped` or `Paused`, start playing the track indicated by the `Id` state variable.  
If `TransportState` is `Playing` or `Buffering`, re-start playing the current track from the beginning.  
If the Playlist source is not active, deactivates the current source and activates Playlist.  
Disables `Standby` in the [Product](/wiki/Av:Developer:ProductService) service if that was enabled (and if the product is controllable over the network in this mode).

## <span id="Pause"></span>Pause

Pause the current track. The `TransportState` will change to `Paused`, possibly after a short delay allowing the volume to be ramped down.  
This will be converted to `Stop` if the track cannot be paused e.g. for internet radio.

## <span id="Stop"></span>Stop

Stop the current track and move the current position to the start of this track. The `TransportState` will change to `Stopped`, possibly after a short delay allowing the volume to be ramped down.

## <span id="Next"></span>Next

Halt playback of the current track and start playing the next item in the playlist.  
If the last track in a playlist is being played and `Repeat` is off, the playlist will pause. The first track in the playlist will be played from the beginning if the `Play` action is invoked.  
If the last track in a playlist is being played and `Repeat` is on, the first last track in the playlist is played.

## <span id="Previous"></span>Previous

Halt playback of the current track and start playing the previous item in the playlist.  
If the first track in a playlist is being played and `Repeat` is off, the playlist will pause. The first track will be played from the beginning if the `Play` action is invoked.  
If the first track in a playlist is being played and `Repeat` is on, the last track in the playlist is played.  
Behaviour when `Shuffle` is enabled is implementation defined.

## <span id="SetRepeat"></span>SetRepeat

Enable or disable repeat mode.

## <span id="Repeat_2"></span>Repeat

Return the value of the `Repeat` state variable.

## <span id="SetShuffle"></span>SetShuffle

Enable or disable shuffle mode.

## <span id="Shuffle_2"></span>Shuffle

Return the value of the `Shuffle` state variable.

## <span id="SeekSecondAbsolute"></span>SeekSecondAbsolute

Seek to an absolute second within the current track. This is only available if the current track has a finite length.

## <span id="SeekSecondRelative"></span>SeekSecondRelative

Seek to a relative second within the current track. This is only available if the current track has a finite length.

## <span id="SeekId"></span>SeekId

Halt playback of the current track and switch to the track with the specified id.  
Should return a `800` fault code if the id is invalid.

## <span id="SeekIndex"></span>SeekIndex

Halt playback of the current track and switch to the track with the specified index.  
Use of this function is discouraged as it results in an unpredictable track being played in the presence of multiple control points. Try to use `SeekId` in preference to this.  
May return a `800` fault code if the index is beyond the end of the playlist.

## <span id="TransportState_2"></span>TransportState

Return the value of the `TransportState` state variable.

## <span id="Id_2"></span>Id

Return the value of the `Id` state variable.

## <span id="Read"></span>Read

Report the uri and metadata for a given track id.  
Returns a `800` fault code if the given id is not in the playlist.

## <span id="ReadList"></span>ReadList

Given a space separated list of track Id's, report their associated uri and metadata in the following xml form:

``` xml
  <TrackList>
    <Entry>
      <Id></Id>
      <Uri></Uri>
      <Metadata></Metadata>
    </Entry>
  </TrackList>
```

Any ids not in the playlist are ignored.

## <span id="Insert"></span>Insert

Adds the given uri and metadata as a new track to the playlist.  
Set the `AfterId` argument to `0` to insert a track at the start of the playlist.  
Reports a `800` fault code if `AfterId` is not `0` and doesn’t appear in the playlist.  
Reports a `801` fault code if the playlist is full (i.e. already contains `TracksMax` tracks).

## <span id="DeleteId"></span>DeleteId

Delete the track with a given id from the playlist.  
If the id to be deleted is currently playing, the next track becomes current.  
Returns a `800` fault code if the given id is not in the playlist.

## <span id="DeleteAll"></span>DeleteAll

Delete all tracks from the playlist.

## <span id="TracksMax_2"></span>TracksMax

Return the value of the `TracksMax` state variable.

## <span id="IdArray_2"></span>IdArray

Return the value of the `IdArray` state variable. Also returns a token which can be used with the IdArrayChanged action.

## <span id="IdArrayChanged"></span>IdArrayChanged

Check to see if the id array has changed since gathering the specified `Token`. This `Token` must have been previously collected from the `IdArray` action.  
This mechanism is provided specifically for clients unable to partake in UPnP eventing.

## <span id="ProtocolInfo_2"></span>ProtocolInfo

Return the value of the `ProtocolInfo` state variable.

# <span id="Technical_Details"></span>Technical Details

        Domain  : av.openhome.org
        Name    : Playlist
        Version : 1

## <span id="Service_Description_.28XML.29"></span>Service Description (XML)

``` xml

<?xml version="1.0" encoding="utf-8"?>

<scpd xmlns="urn:schemas-upnp-org:service-1-0">
    
    <specVersion>
        <major>1</major>
        <minor>0</minor>
    </specVersion>

    <actionList>
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
        </action>
        <action>
            <name>Previous</name>
        </action>
        <action>
            <name>SetRepeat</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>in</direction>
                    <relatedStateVariable>Repeat</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>Repeat</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>out</direction>
                    <relatedStateVariable>Repeat</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>SetShuffle</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>in</direction>
                    <relatedStateVariable>Shuffle</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>Shuffle</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>out</direction>
                    <relatedStateVariable>Shuffle</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>SeekSecondAbsolute</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>in</direction>
                    <relatedStateVariable>Absolute</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>SeekSecondRelative</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>in</direction>
                    <relatedStateVariable>Relative</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>SeekId</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>SeekIndex</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>in</direction>
                    <relatedStateVariable>Index</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>TransportState</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>out</direction>
                    <relatedStateVariable>TransportState</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>Id</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>out</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>Read</name>
            <argumentList>
                <argument>
                    <name>Id</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
                <argument>
                    <name>Uri</name>
                    <direction>out</direction>
                    <relatedStateVariable>Uri</relatedStateVariable>
                </argument>
                <argument>
                    <name>Metadata</name>
                    <direction>out</direction>
                    <relatedStateVariable>Metadata</relatedStateVariable>
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
            <name>DeleteId</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
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
                    <name>Value</name>
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
        <action>
            <name>ProtocolInfo</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>out</direction>
                    <relatedStateVariable>ProtocolInfo</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
    </actionList>

    <serviceStateTable>
        <stateVariable sendEvents="yes">
            <name>TransportState</name>
            <dataType>string</dataType>
            <allowedValueList>
                <allowedValue>Playing</allowedValue>
                <allowedValue>Paused</allowedValue>
                <allowedValue>Stopped</allowedValue>
                <allowedValue>Buffering</allowedValue>
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
        <stateVariable sendEvents="yes">
            <name>Id</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>IdArray</name>
            <dataType>bin.base64</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>TracksMax</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ProtocolInfo</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>Index</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>Relative</name>
            <dataType>i4</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>Absolute</name>
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
