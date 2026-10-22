---
title: "Av:Developer:Eriskay:SenderService"
permalink: "/wiki/Av:Developer:Eriskay:SenderService"
redirect_from:
---

{% raw %}
# <span id="Sender_Service"></span>Sender Service

## <span id="Overview"></span>Overview

The Sender service indicates the presence of a Songcast sender and provides information concerning that sender.

A Songcast sender broadcasts music on a network in a way that is playable by a Songcast [ receiver](/wiki/Av:Developer:Eriskay:ReceiverService).

If a device's [ Product](/wiki/Av:Developer:Eriskay:ProductService) service reports an attribute `"Sender"`, then that device is guaranteed to bear the Sender service. Alternatively, Songcast senders can be discovered independently of the Product service by checking for the `openhome.org.sender` attribute on the [ Device](/wiki/Av:Developer:Eriskay:DeviceService) service.

If the Sender service is available, all its properties and actions must be fully implemented.

## <span id="Evented_Properties"></span>Evented Properties

### <span id="Audio"></span>Audio

`true` if audio is currently available from this Sender; `false` otherwise.

### <span id="Metadata"></span>Metadata

Provides basic information about the sender in OpenHome Metadata format. <tt>

`   {`  
`       "Title"   : "[sender name]",`  
`       "Origin"  : "openhome.org.sender",`  
`       "Uri"     : "[ohz uri.  ohu/ohm if ohz is not supported]",`  
`       "Artwork" : "[uri to icon for sender]",`  
`       "Channel" : "Songcast"`  
`   }`

</tt>

### <span id="Status"></span>Status

Reports the status of the sender:

- `Enabled` - sender enabled by user configuration (default)
- `Disabled` - sender disabled by user configuration
- `Blocked` - audio from another sender detected on the same channel (mis-configuration)

## <span id="Actions"></span>Actions

### <span id="Audio_2"></span>Audio

`Arguments: (out bool audio)`  
Return the value of the `Audio` property.

### <span id="Metadata_2"></span>Metadata

`Arguments: (out string metadata)`  
Return the value of the `Metadata` property.

### <span id="Status_2"></span>Status

`Arguments: (out string status)`  
Return the value of the `Status` property.

## <span id="UPnP_Service_Description"></span>UPnP Service Description

For devices supporting the UPnP protocol, the service description is

`name: "Sender"`  
`domain: "openhome.org.eriskay"`  
`version: "1"`

``` xml
<?xml version="1.0"?>
<scpd xmlns="urn:schemas-upnp-org:service-1-0">
  <specVersion>
    <major>1</major>
    <minor>0</minor>
  </specVersion>

  <actionList>
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
      <name>Status</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>Status</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
  </actionList>

  <serviceStateTable>
    <stateVariable sendEvents="yes">
      <name>Audio</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Metadata</name>
      <dataType>string</dataType>
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
  </serviceStateTable>
</scpd>
```
{% endraw %}
