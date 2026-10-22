---
title: "Av:Developer:PlaylistManagerService"
permalink: "/wiki/Av:Developer:PlaylistManagerService"
redirect_from:
---

{% raw %}
# <span id="Architectural_Overview"></span>Architectural Overview

The PlaylistManager service provides the ability to create and maintain playlists.

The PlaylistManager service provides access to a list of playlists, which in turn, contain a list of tracks.

Using the PlaylistManager service you can read, insert and delete playlists as well as read, insert and delete tracks in an individual playlist. Each playlist and each track within a playlist is given a unique id.

To insert a playlist, provide the id of the playlist you wish to insert 'after' and the associated metadata, (name, description and image id). An empty playlist is inserted into the correct position and the id of the new playlist is returned. To insert in the first position, insert after the special id of 0.

To insert a track, provide the id of the playlist and the id of the track you wish to insert 'after' and the associated udn and metadata. The track is inserted and the id of the new track is returned. To insert in the first position. insert after the special id of 0. If the track originated from a media server the udn should contain the udn of the media server and the metadata id should contain the metadata for the track. Otherwise the udn should be empty and the metadata id should contain DidlLite describing the track.

There are two ways to read the list of playlists or the list of tracks in a playlist. The first reads a single entry and the second reads a list of entries.

Likewise there are two ways to delete the tracks in a playlist. But you can only delete the playlists themselves individually.

## <span id="IdArray_and_TokenIdArray"></span>IdArray and TokenIdArray

The PlaylistManager service has two evented state variable called IdArray and TokenArray. Both arrays are base64 encoded arrays of 32 bit, big endian unsigned integers. Each Id and Token represents a playlist in the list of playlists. An empty array indicates an empty list if playlists. A Change in Token for a playlist indicates that the playlist contents has changed.

Whether you acquire the IdArray and TokenArray via events or polling, you immediately know the number and order of the ids of the playlists, as well as whether an individual playlist has changed. What you don't necessarily know is the metadata for those ids.

As the metadata for a large number of playlists can easily be several megabytes of xml, blindly fetching all the metadata every time the playlists change is inefficient and will give a poor user experience. In order to quickly display playlists updates and ensure interoperability with other control points on the network, it is strongly recommended that you maintain the following two data structures:

- A copy of the latest IdArray and TokenArray
- A cache mapping id's to their associated metadata.

With this decoupled approach, you only need to fetch the metadata for the ids added to the playlists. Changes to the order of ids in the playlists require no action.

As a further enhancement, when an insert completes successfully, you know both the metadata (as you supplied it), and the new id (returned by the PlaylistManager on completion of the insert action). This information can be directly inserted into the cache, saving subsequent unnecessary retrieval.

## <span id="Playlist_IdArray"></span>Playlist IdArray

The obtain a playlist's IdArray, provide the id of the playlist to the action PlaylistReadArray. The IdArray returned is a base64 encoded array of 32 bit, big endian unsigned integers. Each Id represents a track in the playlist. An empty IdArray indicates an empty playlist.

When you acquire the IdArray, through the action PlaylistReadArray, you immediately know the number and order of the ids in the playlist. What you don't necessarily know is the metadata for those ids.

As the metadata for a large number of playlists can easily be several megabytes of xml, blindly fetching all the metadata every time the playlist changes is inefficient and will give a poor user experience. In order to quickly display playlist updates and ensure interoperability with other control points on the network, it is strongly recommended that you maintain the following two data structures:

- A copy of the latest IdArray
- A cache mapping id's to their associated metadata.

With this decoupled approach, you only need to fetch the metadata for the ids added to the playlist. Changes to the order of ids in the playlist require no action.

As a further enhancement, when an insert completes successfully, you know both the metadata (as you supplied it), and the new id (returned by the PlaylistManager on completion of the insert action). This information can be directly inserted into the cache, saving subsequent unnecessary retrieval.

## <span id="Events"></span>Events

A short while (approx 300ms) after any change to the list of playlists, the PlaylistManager will event all subscribers the current IdArray and TokenArray. The eventing of these state variables is moderated to prevent excessive updates.

A short while (approx 300ms) after any changes to a playlist, the PlaylistManager will event all subscribers the current TokenArray. The eventing of this state variable is moderated to prevent excessive updates.

## <span id="Polling"></span>Polling

For control points that can't subscribe to events, two additional actions are provided. The first, PlaylistArrays, reads the IdArray and TokenArray directly. This action also returns an ArraysToken, which should be saved and periodically passed to a second action, PlaylistArraysChanged, which reports whether or not your copy of IdArray and TokenArray are out of date. If they are, calling PlaylistArrays again will ensure you have up to date versions.

# <span id="Actions"></span>Actions

## <span id="Metadata"></span>Metadata

Returns the Metadata describing the PlaylistManager.

## <span id="ImagesXml"></span>ImagesXml

Returns a list of artwork images a control point can associate with a playlist.

``` xml

  <ImageList>
    <Entry>
      <Id></Id>
      <Uri></Uri>
    </Entry>
  </ImageList>
```

## <span id="PlaylistReadArray"></span>PlaylistReadArray

Report the current id array for the specified playlist.

The IdArray is an ordered array of ids that represent each track in the playlist.

## <span id="PlaylistReadList"></span>PlaylistReadList

Given a list of playlist ids, report their associated Name, Description and ImageId in the following XML form:

``` xml

  <PlaylistList>
    <Entry>
      <Id></Id>
      <Name></Name>
      <Description></Description>
      <ImageId></ImageId>
    </Entry>
  </PlaylistList>
```

## <span id="PlaylistRead"></span>PlaylistRead

Given a playlist id, report its associated Name, Description and ImageId.

## <span id="PlaylistSetName"></span>PlaylistSetName

Sets the Name of the specified playlist.

## <span id="PlaylistSetDescription"></span>PlaylistSetDescription

Sets the Description of the specified playlist.

## <span id="PlaylistSetImageId"></span>PlaylistSetImageId

Sets the ImageId of the specified playlist.

## <span id="PlaylistInsert"></span>PlaylistInsert

Inserts an empty playlist with the specified Name, Description and ImageId after the specified playlist id. To insert at the beginning of the list use the special playlist id of 0.

## <span id="PlaylistDeleteId"></span>PlaylistDeleteId

Delete from the list of playlists the playlist with the specified Id.

## <span id="PlaylistsMax"></span>PlaylistsMax

Report the maximum number of playlists in the playlists id array. This remains constant while a particular OpenHome device remains registerted on the network, but may vary between different models of OpenHome device from different manufacturers. A value of 0 indicates no limit.

## <span id="TracksMax"></span>TracksMax

Report the maximum number of tracks in a playlist id array. This remains constant while a particular OpenHome device remains registerted on the network, but may vary between different models of OpenHome device from different manufacturers. A value of 0 indicates no limit.

## <span id="PlaylistArrays"></span>PlaylistArrays

Report the current id array and token array.

The IdArray is an ordered array of ids that represent each playlist in the list of playlists.

This action also reports a Token, which can be used to quickly detect if the id array or token array has changed since it was last read (see PlaylistArraysChanged).

## <span id="PlaylistArraysChanged"></span>PlaylistArraysChanged

Check to see if the id array or token array has changed since gathering the specified Token. This Token must have been previously collected from the PlaylistArrays action.

This mechanism is provided specifically for clients unable to partake in UPnP eventing.

## <span id="Read"></span>Read

Given a playlist id and a track Id, report its associated Metadata.

## <span id="ReadList"></span>ReadList

Given a playlist id and a space separated list of track Id's, report their associated Metadata in the following xml form:

``` xml

  <Playlist>
    <Track>
      <Udn></Udn>
      <Metadata></Metadata>
    </Track>
  </Playlist>
```

## <span id="Insert"></span>Insert

Insert a track after the specified track id. To insert at the beginning of the list use the special track id of 0.

## <span id="DeleteId"></span>DeleteId

Delete from the specified playlist the track with the specified Id.

## <span id="DeleteAll"></span>DeleteAll

Clears the specified playlist.

# <span id="Technical_Details"></span>Technical Details

        Domain  : av.openhome.org
        Name    : PlaylistManager
        Version : 1

## <span id="PlaylistManager_Service_Description_.28XML.29"></span>PlaylistManager Service Description (XML)

``` xml

<?xml version="1.0" encoding="utf-8"?>

<scpd xmlns="urn:schemas-upnp-org:service-1-0">
    
    <specVersion>
        <major>1</major>
        <minor>0</minor>
    </specVersion>

    <actionList>
        <action>
            <name>Metadata</name>
            <argumentList>
                <argument>
                    <name>Metadata</name>
                    <direction>out</direction>
                    <relatedStateVariable>Metadata</relatedStateVariable>
                </argument>
            </argumentList>
        </action>

        <action>
            <name>ImagesXml</name>
            <argumentList>
                <argument>
                    <name>ImagesXml</name>
                    <direction>out</direction>
                    <relatedStateVariable>ImagesXml</relatedStateVariable>
                </argument>
            </argumentList>
        </action>

        <action>
            <name>PlaylistReadArray</name>
            <argumentList>
                <argument>
                    <name>Id</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
                <argument>
                    <name>Array</name>
                    <direction>out</direction>
                    <relatedStateVariable>IdArray</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>PlaylistReadList</name>
            <argumentList>
                <argument>
                    <name>IdList</name>
                    <direction>in</direction>
                    <relatedStateVariable>IdList</relatedStateVariable>
                </argument>
                <argument>
                    <name>PlaylistList</name>
                    <direction>out</direction>
                    <relatedStateVariable>PlaylistList</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>PlaylistRead</name>
            <argumentList>
                <argument>
                    <name>Id</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
                <argument>
                    <name>Name</name>
                    <direction>out</direction>
                    <relatedStateVariable>Name</relatedStateVariable>
                </argument>
                <argument>
                    <name>Description</name>
                    <direction>out</direction>
                    <relatedStateVariable>Description</relatedStateVariable>
                </argument>
                <argument>
                    <name>ImageId</name>
                    <direction>out</direction>
                    <relatedStateVariable>ImageId</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>PlaylistSetName</name>
            <argumentList>
                <argument>
                    <name>Id</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
                <argument>
                    <name>Name</name>
                    <direction>in</direction>
                    <relatedStateVariable>Name</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>PlaylistSetDescription</name>
            <argumentList>
                <argument>
                    <name>Id</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
                <argument>
                    <name>Description</name>
                    <direction>in</direction>
                    <relatedStateVariable>Description</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>PlaylistSetImageId</name>
            <argumentList>
                <argument>
                    <name>Id</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
                <argument>
                    <name>ImageId</name>
                    <direction>in</direction>
                    <relatedStateVariable>ImageId</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>PlaylistInsert</name>
            <argumentList>
                <argument>
                    <name>AfterId</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
                <argument>
                    <name>Name</name>
                    <direction>in</direction>
                    <relatedStateVariable>Name</relatedStateVariable>
                </argument>
                <argument>
                    <name>Description</name>
                    <direction>in</direction>
                    <relatedStateVariable>Description</relatedStateVariable>
                </argument>
                <argument>
                    <name>ImageId</name>
                    <direction>in</direction>
                    <relatedStateVariable>ImageId</relatedStateVariable>
                </argument>
                <argument>
                    <name>NewId</name>
                    <direction>out</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>PlaylistDeleteId</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>PlaylistMove</name>
            <argumentList>
                <argument>
                    <name>Id</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
                <argument>
                    <name>AfterId</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>PlaylistsMax</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>out</direction>
                    <relatedStateVariable>PlaylistsMax</relatedStateVariable>
                </argument>
            </argumentList>
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
            <name>PlaylistArrays</name>
            <argumentList>
                <argument>
                    <name>Token</name>
                    <direction>out</direction>
                    <relatedStateVariable>ArraysToken</relatedStateVariable>
                </argument>
                <argument>
                    <name>IdArray</name>
                    <direction>out</direction>
                    <relatedStateVariable>IdArray</relatedStateVariable>
                </argument>
                <argument>
                    <name>TokenArray</name>
                    <direction>out</direction>
                    <relatedStateVariable>TokenArray</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>PlaylistArraysChanged</name>
            <argumentList>
                <argument>
                    <name>Token</name>
                    <direction>in</direction>
                    <relatedStateVariable>ArraysToken</relatedStateVariable>
                </argument>
                <argument>
                    <name>Value</name>
                    <direction>out</direction>
                    <relatedStateVariable>IdArrayChanged</relatedStateVariable>
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
                    <name>TrackId</name>
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
                    <name>Id</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
                <argument>
                    <name>TrackIdList</name>
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
                    <name>Id</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
                <argument>
                    <name>AfterTrackId</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
                <argument>
                    <name>Udn</name>
                    <direction>in</direction>
                    <relatedStateVariable>Udn</relatedStateVariable>
                </argument>
                <argument>
                    <name>MetadataId</name>
                    <direction>in</direction>
                    <relatedStateVariable>MetadataId</relatedStateVariable>
                </argument>
                <argument>
                    <name>NewTrackId</name>
                    <direction>out</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>DeleteId</name>
            <argumentList>
                <argument>
                    <name>TrackId</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
                <argument>
                    <name>Value</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>DeleteAll</name>
            <argumentList>
                <argument>
                    <name>TrackId</name>
                    <direction>in</direction>
                    <relatedStateVariable>Id</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
    </actionList>

    <serviceStateTable>

        <stateVariable sendEvents="yes">
            <name>Metadata</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ImagesXml</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>IdArray</name>
            <dataType>bin.base64</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>TokenArray</name>
            <dataType>bin.base64</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>PlaylistsMax</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>TracksMax</name>
            <dataType>ui4</dataType>
        </stateVariable>

        <stateVariable sendEvents="no">
            <name>PlaylistList</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>Id</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>IdList</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>Name</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>Description</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>ImageId</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>TrackList</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>Udn</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>MetadataId</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>ArraysToken</name>
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
