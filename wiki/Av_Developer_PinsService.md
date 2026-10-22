---
title: "Av:Developer:PinsService"
permalink: "/wiki/Av:Developer:PinsService"
redirect_from:
---

{% raw %}
# <span id="Overview"></span>Overview

A pin is a set of instructions to switch source or play one or more tracks on a device. Some pins will have wholly predictable results (e.g. switch to Analog2, play named playlist); others may be more dynamic (e.g. play the latest podcast from a given feed or a curated playlist of the week from a streaming service).

The Pins service provides access both device-specific and account-wide pins. Both classes of pin can be read from or invoked on a device. Device-specific pins can also be edited; account-wide pins may be editable via a device but should also have edit APIs in the service or location that provides general account support.

# <span id="Supported_Content"></span>Supported Content

Reference code contains support for the following [ pinnable content](/wiki/Av:Developer:PinInvokers).

# <span id="State_Variables"></span>State Variables

## <span id="DeviceMax"></span>DeviceMax

The maximum number of device-specific pins supported

## <span id="AccountMax"></span>AccountMax

The maximum number of account-wide pins supported

## <span id="Modes"></span>Modes

JSON array of strings identifying the different styles of pins supported

## <span id="CloudConnected"></span>CloudConnected

`true` if a connection is available to cloud-backed master copy of account pins (i.e. when account pins are editable); `false` otherwise.

## <span id="IdArray"></span>IdArray

JSON array of identifiers (unsigned integer) for all pins.  
Device pins are listed first, followed by Account pins. i.e. array will always have `DeviceMax` + `AccountMax` entries.  
Identifiers will normally be unique; `0` is a special case which signifies an empty pin.

# <span id="Actions"></span>Actions

## <span id="GetDeviceMax"></span>GetDeviceMax

Read the `DeviceMax` property.

## <span id="GetAccountMax"></span>GetAccountMax

Read the `AccountMax` property.

## <span id="GetModes"></span>GetModes

Read the `Modes` property.

## <span id="GetCloudConnected"></span>GetCloudConnected

Read the `CloudConnected` property.

## <span id="GetIdArray"></span>GetIdArray

Read the `IdArray` property.

## <span id="ReadList"></span>ReadList

Input: JSON integer array, specifying ids of pins to be read.  
Output: JSON array of pins

    [
        {
            "id": {unsigned integer, unique across device & account pins},
            "mode": "where track(s) will be fetched from",
            "type": "instructs the device how to interpret the uri below",
            "uri": "absolute uri",
            "title": "Short text, may be user-visible",
            "description": "Longer text, may be user-visible",
            "artworkUri": "absolute uri to image",
            "shuffle": {boolean}
        },
        { ... }
    ]

## <span id="InvokeIndex"></span>InvokeIndex

Invoke the pin at the specified index in `IdArray`. This will stop anything that is currently playing and may clear any current playlist.

## <span id="InvokeId"></span>InvokeId

Invoke the pin with the specified id. This will stop anything that is currently playing and may clear any current playlist.

## <span id="InvokeUri"></span>InvokeUri

Invoke a pin using data (mode, type, uri, shuffle) from a control point. Should be used by any control point that wants to determine which account to read pins from. (Note however that pins which themselves require cloud support to load cannot be loaded by the device - control points would have to load them directly into a playlist instead.) This will stop anything that is currently playing and may clear any current playlist.

## <span id="SetDevice"></span>SetDevice

Set a device pin, specifying the mode, type, uri, title, description, artworkUri and shuffle plus index into the set of device pins.  
Any pin currently assigned at the specified index will be replaced.  
Any playing content is unaffected (i.e. invoking then replacing a pin leaves the old representation of the pin playing). index must be in the range `[0..DeviceMax)`.  
Some errors are notified in response to this action. Success should only be assumed when an update is evented to IdArray showing a change in id at the specified index.

## <span id="SetAccount"></span>SetAccount

Set an account pin, specifying the mode, type, uri, title, description, artworkUri and shuffle plus index into the set of device pins.  
Any pin currently assigned at the specified index will be replaced.  
Any playing content is unaffected (i.e. invoking then replacing a pin leaves the old representation of the pin playing). index must be in the range `[0..AccountMax)`.  
Requests to update an account pin are proxied to a remote server so are likely to be slower and have greater chance of failure.  
Some errors are notified in response to this action. Success should only be assumed when an update is evented to `IdArray` showing a change in id at `DeviceMax + index`.

## <span id="Clear"></span>Clear

Clear any content in the pin with the specified id.  
As with Set, changes to device pins are implemented locally; changes to account pins are proxied to a remote server.  
Some errors are notified in response to this action. Success should only be assumed when an update is evented to the sequence number for the specified id.

## <span id="Swap"></span>Swap

Swap contents of the 2 pins at the specified indices.  
Pins can only be swapped within either device or account lists.

# <span id="Technical_Details"></span>Technical Details

        Domain  : av.openhome.org
        Name    : Pins
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
      <name>GetDeviceMax</name>
      <argumentList>
        <argument>
          <name>DeviceMax</name>
          <direction>out</direction>
          <relatedStateVariable>DeviceMax</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>GetAccountMax</name>
      <argumentList>
        <argument>
          <name>AccountMax</name>
          <direction>out</direction>
          <relatedStateVariable>AccountMax</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>GetModes</name>
      <argumentList>
        <argument>
          <name>Modes</name>
          <direction>out</direction>
          <relatedStateVariable>Modes</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>GetIdArray</name>
      <argumentList>
        <argument>
          <name>IdArray</name>
          <direction>out</direction>
          <relatedStateVariable>IdArray</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>GetCloudConnected</name>
      <argumentList>
        <argument>
          <name>CloudConnected</name>
          <direction>out</direction>
          <relatedStateVariable>CloudConnected</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>ReadList</name>
      <argumentList>
        <argument>
          <name>Ids</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>List</name>
          <direction>out</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>InvokeId</name>
      <argumentList>
        <argument>
          <name>Id</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_Uint</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>InvokeIndex</name>
      <argumentList>
        <argument>
          <name>Index</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_Uint</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>InvokeUri</name>
      <argumentList>
        <argument>
          <name>Mode</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Type</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Uri</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Shuffle</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_Bool</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SetDevice</name>
      <argumentList>
        <argument>
          <name>Index</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_Uint</relatedStateVariable>
        </argument>
        <argument>
          <name>Mode</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Type</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Uri</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Title</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Description</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>ArtworkUri</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Shuffle</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_Bool</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SetAccount</name>
      <argumentList>
        <argument>
          <name>Index</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_Uint</relatedStateVariable>
        </argument>
        <argument>
          <name>Mode</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Type</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Uri</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Title</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Description</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>ArtworkUri</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Shuffle</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_Bool</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Clear</name>
      <argumentList>
        <argument>
          <name>Id</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_Uint</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Swap</name>
      <argumentList>
        <argument>
          <name>Index1</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_Uint</relatedStateVariable>
        </argument>
        <argument>
          <name>Index2</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_Uint</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
  </actionList>
  <serviceStateTable>
    <stateVariable sendEvents="yes">
      <name>DeviceMax</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>AccountMax</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Modes</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>IdArray</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>CloudConnected</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>A_ARG_TYPE_String</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>A_ARG_TYPE_Uint</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>A_ARG_TYPE_Bool</name>
      <dataType>boolean</dataType>
    </stateVariable>
  </serviceStateTable>
</scpd>
```
{% endraw %}
