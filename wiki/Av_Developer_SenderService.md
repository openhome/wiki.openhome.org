---
title: "Av:Developer:SenderService"
permalink: "/wiki/Av:Developer:SenderService"
redirect_from:
  - "/wiki/Developer:SenderService"
---

{% raw %}
# <span id="Overview"></span>Overview

The Sender service indicates the presence of a Songcast sender and provides information concerning that sender.

A Songcast sender broadcasts music on a network in a way that is playable by a Songcast [receiver](/wiki/Av:Developer:ReceiverService).

If a device's Product service reports an attribute source of type 'Sender', then that device is guaranteed to bear the Sender service. Alternatively, Songcast senders can be discovered independently of the Product service by simply searching for devices bearing the Sender service.

# <span id="State_Variables"></span>State Variables

## <span id="Attributes"></span>Attributes

Reserved for future use.

## <span id="Audio"></span>Audio

`true` if audio is currently available from this Sender; `false` otherwise.

## <span id="Metadata"></span>Metadata

Provides basic information about the sender in DIDL-Lite format.

``` xml
<DIDL-Lite xmlns:dc="http://purl.org/dc/elements/1.1/"
           xmlns:upnp="urn:schemas-upnp-org:metadata-1-0/upnp/"
           xmlns="urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/">
    <item id="0" restricted="True">
        <dc:title>[sender_name]</dc:title>"
        <res protocolInfo="ohz:*:*:[m|u]">ohz://239.255.255.250:51972/[device_udn]</res>
        <upnp:albumArtURI>[full_uri]</upnp:albumArtURI>
        <upnp:class>object.item.audioItem</upnp:class>
    </item>
</DIDL-Lite>
```

Note that protocolInfo takes the form `ohz:*:*:m` or `ohz:*:*:u` depending on whether multicast or unicast mode is enabled

## <span id="PresentationUrl"></span>PresentationUrl

Reports the url of a presentation page for further information concerning the sender, or for controlling the sender in some application-specific way. If the sender has no presentation page, `PresentationUrl` is empty.

## <span id="Status"></span>Status

Deprecated. Use `Status2` instead.

- Enabled - sender enabled by user configuration and not blocked
- Blocked - audio from another sender detected on the same channel (mis-configuration)
- Disabled - sender disabled by user configuration

## <span id="Status2"></span>Status2

Reports the status of the sender (normally only for debugging purposes):

- Sending - currently sending audio over the network
- Ready - capable of sending audio but no listeners. Use `Audio` to determine whether audio would be sent immediately a listener joins.
- Blocked - audio from another sender detected on the same channel (mis-configuration)
- Inactive - sender device is playing content which cannot be broadcast
- Disabled - sender disabled by user configuration

## <span id="Enabled"></span>Enabled

`true` if the device bearing this service is capable of acting as a Songcast sender (i.e. Songcast sending is enabled and the sender is not blocked due to a multicast port clash); `false` otherwise.

# <span id="Actions"></span>Actions

## <span id="Attributes_2"></span>Attributes

Return the value of the `Attributes` state variable

## <span id="Audio_2"></span>Audio

Return the value of the `Audio` state variable

## <span id="Metadata_2"></span>Metadata

Return the value of the `Metadata` state variable

## <span id="PresentationUrl_2"></span>PresentationUrl

Return the value of the `PresentationUrl` state variable

## <span id="Status_2"></span>Status

Return the value of the `Status` state variable

# <span id="Sender_Service_Description_.28XML.29"></span>Sender Service Description (XML)

        Domain  : av.openhome.org
        Name    : Sender
        Version : 2

``` xml
<?xml version="1.0"?>
<scpd xmlns="urn:schemas-upnp-org:service-1-0">
  <specVersion>
    <major>1</major>
    <minor>0</minor>
  </specVersion>

  <actionList>
    <action>
      <name>PresentationUrl</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>PresentationUrl</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Metadata</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>Metadata</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Audio</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>Audio</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Status</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>Status</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Status2</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>Status2</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Enabled</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>Enabled</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Attributes</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>Attributes</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
  </actionList>

  <serviceStateTable>
    <stateVariable sendEvents="yes">
      <name>PresentationUrl</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Metadata</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Audio</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Status</name>
      <dataType>string</dataType>
      <allowedValueList>
        <allowedValue>Enabled</allowedValue>
        <allowedValue>Disabled</allowedValue>
        <allowedValue>Blocked</allowedValue>
      </allowedValueList>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Status2</name>
      <dataType>string</dataType>
      <allowedValueList>
        <allowedValue>Sending</allowedValue>
        <allowedValue>Ready</allowedValue>
        <allowedValue>Blocked</allowedValue>
        <allowedValue>Inactive</allowedValue>
        <allowedValue>Disabled</allowedValue>
      </allowedValueList>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Enabled</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Attributes</name>
      <dataType>string</dataType>
    </stateVariable>
  </serviceStateTable>
</scpd>
```
{% endraw %}
