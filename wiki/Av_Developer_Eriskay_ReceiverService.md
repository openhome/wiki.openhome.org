---
title: "Av:Developer:Eriskay:ReceiverService"
permalink: "/wiki/Av:Developer:Eriskay:ReceiverService"
redirect_from:
---

{% raw %}
# <span id="Receiver_Service"></span>Receiver Service

## <span id="Overview"></span>Overview

A Songcast receiver plays audio broadcast from a [ sender](/wiki/Av:Developer:Eriskay:SenderService). The Receiver service provides the means for controlling a Receiver source.

If a device's [ Product](/wiki/Av:Developer:Eriskay:ProductService) service reports a source of type `Receiver`, then that device is guaranteed to bear the Receiver service. If the Receiver service is available, all its properties and actions must be fully implemented.

## <span id="Evented_Properties"></span>Evented Properties

### <span id="Metadata"></span>Metadata

The metadata of the sender to listen to. In the OpenHome Metadata format provided by the [ Sender](/wiki/Av:Developer:Eriskay:SenderService) service.

### <span id="Uri"></span>Uri

The uri of the [ Sender](/wiki/Av:Developer:Eriskay:SenderService) to listen to.

## <span id="Actions"></span>Actions

## <span id="Sender"></span>Sender

`Arguments: (out string uri, out string metadata)`  
Report the values of the `Uri` and `Metadata` properties.

## <span id="UPnP_Service_Description"></span>UPnP Service Description

For devices supporting the UPnP protocol, the service description is

`name: "Receiver"`  
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
      <name>Sender</name>
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
  </serviceStateTable>
</scpd>
```
{% endraw %}
