---
title: "Av:Developer:RadioService"
permalink: "/wiki/Av:Developer:RadioService"
redirect_from:
  - "/wiki/Developer:RadioService"
---

{% raw %}
# <span id="Overview"></span>Overview

The Radio service primarily offers the means for controlling radio presets; it also offers an API to allow arbitrary URLs to be played. If a device’s Product service reports a source of type 'Radio', then the device that bears that Product service is guaranteed to also bear the Radio service.

# <span id="State_Variables"></span>State Variables

## <span id="ChannelsMax"></span>ChannelsMax

The maximum number of presets (and so the number of elements in IdArray). Read-only.

## <span id="Id"></span>Id

The id of the currently selected preset (as set by the last call to SetId). Or 0 if no preset has ever been selected or SetChannel was called more recently than SetId.

## <span id="IdArray"></span>IdArray

Base64-encoded array of 32-bit big endian unsigned integers. Will always be (ChannelsMax \* 4) bytes long. Each id represents a preset id. A value of 0 implies that no preset is set for that slot.

## <span id="Metadata"></span>Metadata

Metadata for the last track to be selected (via a call to either SetChannel or SetId).

## <span id="ProtocolInfo"></span>ProtocolInfo

Audio formats and networking protocols supported by the device. Will be the same as reported by Playlist and AVTransport if these services are present. Read-only.

## <span id="TransportState"></span>TransportState

One of Stopped, Playing, Paused or Buffering.

## <span id="Uri"></span>Uri

The last uri to be set (via a call to either SetChannel or SetId).

# <span id="Actions"></span>Actions

## <span id="Channel"></span>Channel

Return the values of the Uri and Metadata state variables.

## <span id="ChannelsMax_2"></span>ChannelsMax

Return the value of the ChannelsMax state variable.

## <span id="Id_2"></span>Id

Report the value of the Id state variable.

## <span id="IdArray_2"></span>IdArray

Return the value of the IdArray state variable.

## <span id="IdArrayChanged"></span>IdArrayChanged

Check to see if the IdArray state variable has changed since gathering the specified IdArrayToken. This Token must have been previously collected from the IdArray action. This action is provided specifically for clients which do not use UPnP eventing.

## <span id="Pause"></span>Pause

Pause any currently playing radio stream. Should only be called when the Radio source is currently selected.

## <span id="Play"></span>Play

Play any previously selected track (the last uri to be set via either SetChannel or SetId). Switches source to Radio if that wasn’t already selected.

## <span id="ProtocolInfo_2"></span>ProtocolInfo

Return the value of the ProtocolInfo state variable.

## <span id="Read"></span>Read

Given a channel preset Id, return its associated metadata. The metadata will be of the form

``` xml
<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/"
           xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/"
           xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/">
    <item id="" parentID="" restricted="True">
        <dc:title>[title]</dc:title>
        <res protocolInfo="*:*:*:*" bitrate="6000">[track url]</res>
        <upnp:albumArtURI>[image url]</upnp:albumArtURI>
        <upnp:class>object.item.audioItem</upnp:class>
    </item>
</DIDL-Lite>
```

Note that additional elements may be present. The elements listed above are guaranteed to be present. The contents of all elements will be XML escaped.

## <span id="ReadList"></span>ReadList

Given a space separated list of channel preset Ids, return their associated metadata. The metadata will be of the form

``` xml
<ChannelList>
    <Entry>
        <Id>[preset Id]</Id>
        <Metadata>[as for Read]</Metadata>
    </Entry>
    <Entry>
        ....
    </Entry>
</ChannelList>
```

Note that the content of each metadata will be fully xml escaped (so metadata for a given id won't be byte-for-byte identical to that returned by Read).

## <span id="SeekSecondAbsolute"></span>SeekSecondAbsolute

Seek to an absolute (seconds) position in the currently playing stream, retaining the existing TransportState. Note that most radio streams are not seekable so this action is probably only applicable to a subset of tracks played via SetChannel that the Info service reports are seekable.

## <span id="SeekSecondRelative"></span>SeekSecondRelative

Seek to an position (in seconds) in the currently playing stream, relative to its current position, retaining the existing TransportState. Note that most radio streams are not seekable so this action is probably only applicable to a subset of tracks played via SetChannel that the Info service reports are seekable

## <span id="SetChannel"></span>SetChannel

Set the uri and metadata for a new track. Any currently playing track will be stopped. The new track will not play until the Play action is invoked. The Id state variable will be set to 0.

## <span id="SetId"></span>SetId

Set the preset id and uri for a new track. The uri should be parsed from the metadata returned by Read or ReadList. Any currently playing track will be stopped. The new track will not play until the Play action is invoked. The Id state variable will be updated to the newly specified preset id.

## <span id="Stop"></span>Stop

Stop any currently playing radio stream. Should only be called when the Radio source is currently selected

## <span id="TransportState_2"></span>TransportState

Return the value of the TransportState state variable.

# <span id="Technical_Details"></span>Technical Details

        Domain  : av.openhome.org
        Name    : Radio
        Version : 1

## <span id="Radio_Service_Description_.28XML.29"></span>Radio Service Description (XML)

``` xml
<?xml version="1.0"?>
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
            <name>Channel</name>
            <argumentList>
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
            <name>SetChannel</name>
            <argumentList>
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
            <name>SetId</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
                <argument>
                    <name>Uri</name>
                    <direction>in</direction>
                    <relatedStateVariable>Uri</relatedStateVariable>
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
                    <name>ChannelList</name>
                    <direction>out</direction>
                    <relatedStateVariable>ChannelList</relatedStateVariable>
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
            <name>ChannelsMax</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>out</direction>
                    <relatedStateVariable>ChannelsMax</relatedStateVariable>
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
            <name>Uri</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>Metadata</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>TransportState</name>
            <dataType>string</dataType>
            <allowedValueList>
                <allowedValue>Stopped</allowedValue>
                <allowedValue>Playing</allowedValue>
                <allowedValue>Paused</allowedValue>
                <allowedValue>Buffering</allowedValue>
            </allowedValueList>
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
            <name>ChannelsMax</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ProtocolInfo</name>
            <dataType>string</dataType>
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
            <name>IdArrayToken</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>IdArrayChanged</name>
            <dataType>boolean</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>IdList</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>ChannelList</name>
            <dataType>string</dataType>
        </stateVariable>
    </serviceStateTable>
</scpd>
```
{% endraw %}
