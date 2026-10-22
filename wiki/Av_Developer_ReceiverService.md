---
title: "Av:Developer:ReceiverService"
permalink: "/wiki/Av:Developer:ReceiverService"
redirect_from:
  - "/wiki/Developer:ReceiverService"
---

{% raw %}
# <span id="Overview"></span>Overview

A Songcast receiver plays audio broadcast from a [Songcast sender](/wiki/Av:Developer:SenderService).  
The Receiver service provides the means for controlling a Receiver source. If a device's [Product service](/wiki/Av:Developer:ProductService) reports a source of type `Receiver`, then that device is guaranteed to bear the Receiver service.

# <span id="State_Variables"></span>State Variables

## <span id="Metadata"></span>Metadata

The metadata of the sender to listen to. In the DIDL-lite format provided by the [Sender service](/wiki/Av:Developer:SenderService).

## <span id="Uri"></span>Uri

The uri of the [Sender](/wiki/Av:Developer:SenderService) to listen to. This must match the uri from the sender’s metadata.

## <span id="ProtocolInfo"></span>ProtocolInfo

Reports the protocols supported in the normal UPnP forum format – a comma separated list of elements of the form

\<protocol\>`:`\<network\>`:`\<contentFormat\>`:`\<additionalInfo\>

Supported `protocol` elements are \<ohz\>, \<ohm\> and \<ohu\>. Other elements are normally wildcards `*`

## <span id="TransportState"></span>TransportState

Report the current transport state, which can be: `Playing`, `Waiting`, `Stopped` or `Buffering`.  
Note that network conditions may prevent a Receiver from accurately differentiating between `Waiting` and `Buffering` states.

# <span id="Actions"></span>Actions

## <span id="Play"></span>Play

Play audio from the current sender.

## <span id="Stop"></span>Stop

Stop playing audio from the current sender.

## <span id="SetSender"></span>SetSender

Set the `uri` and `metadata` of the sender to listen to.

## <span id="Sender"></span>Sender

Report the values of the `Uri` and `Metadata` state variables.

## <span id="ProtocolInfo_2"></span>ProtocolInfo

Report the value of the `ProtocolInfo` state variable.

## <span id="TransportState_2"></span>TransportState

Report the value of the `TransportState` state variable.

# <span id="Receiver_Service_Description_.28XML.29"></span>Receiver Service Description (XML)

        Domain  : av.openhome.org
        Name    : Receiver
        Version : 1

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
            <name>Stop</name>
        </action>
        <action>
            <name>SetSender</name>
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
                <allowedValue>Waiting</allowedValue>
                <allowedValue>Buffering</allowedValue>
            </allowedValueList>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ProtocolInfo</name>
            <dataType>string</dataType>
        </stateVariable>        
    </serviceStateTable>
</scpd>
```
{% endraw %}
