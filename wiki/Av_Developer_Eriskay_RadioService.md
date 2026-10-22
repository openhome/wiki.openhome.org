---
title: "Av:Developer:Eriskay:RadioService"
permalink: "/wiki/Av:Developer:Eriskay:RadioService"
redirect_from:
---

{% raw %}
# <span id="Radio_Service"></span>Radio Service

## <span id="Overview"></span>Overview

The Radio service offers a means for controlling radio presets.

If a device's [ Product](/wiki/Av:Developer:Eriskay:ProductService) service reports a source of type `"Radio"`, then that device is guaranteed to also bear the Radio service. If the Radio service is available, all its properties and actions must be fully implemented.

## <span id="Evented_Properties"></span>Evented Properties

### <span id="ChannelsMax"></span>ChannelsMax

The maximum number of presets (and so the number of elements in `IdArray`). Does not vary at run-time.

### <span id="Id"></span>Id

The id of the currently selected preset. Or `0` if no preset has ever been selected.

### <span id="IdArray"></span>IdArray

A JSON integer array containing preset ids. Will always have `ChannelsMax` elements. A value of `0` implies that no preset is set for that slot.

### <span id="Metadata"></span>Metadata

Metadata for the last preset to be selected.

### <span id="Uri"></span>Uri

Uri for the last preset to be selected.

## <span id="Actions"></span>Actions

### <span id="Channel"></span>Channel

`Arguments: (out string uri, out string metadata)`  
Return the values of the `Uri` and `Metadata` properties.

### <span id="ChannelsMax_2"></span>ChannelsMax

`Arguments: (out uint max)`  
Return the value of the `ChannelsMax` property.

### <span id="Id_2"></span>Id

`Arguments: (out uint id)`  
Return the value of the `Id` property.

### <span id="IdArray_2"></span>IdArray

`Arguments: (out uint token, out string idArray)`  
Return the value of the `IdArray` property.

### <span id="IdArrayChanged"></span>IdArrayChanged

`Arguments: (in uint token, out bool changed)`  
Check to see if the `IdArray` state variable has changed since gathering the specified `IdArrayToken`. This Token must have been previously collected from the `IdArray` action. This action is provided specifically for clients which cannot consume standard evented updates of properties.

### <span id="Read"></span>Read

`Arguments: (in uint id, out string metadata)`  
Given a channel preset id, return its associated metadata. The metadata will be of the form <tt>

`   {`  
`       "Title": "[title]"`  
`       "Origin": "[id of origin of metadata]"`  
`       "Uri": "[preset uri]"`  
`       "Artwork": "[image url]"`  
`   }`

</tt> The elements listed above are guaranteed to be present; additional elements may also be included.

### <span id="ReadList"></span>ReadList

`Arguments: (in string ids, out string json)`  
Given a space separated list of channel preset ids, return their associated metadata. The metadata will be of the form <tt>

`   {`  
`       "channels": [`  
`           {`  
`               "id": [preset_id_1],`  
`               "metadata": {`  
`                   "Title": "[title]"`  
`                   "Origin": "[id of origin of metadata]"`  
`                   "Uri": "[preset uri]"`  
`                   "Artwork": "[image url]"`  
`               }`  
`           },`  
`           {`  
`               "id": [preset_id_1],`  
`               "metadata": {`  
`                   "Title": "[title]"`  
`                   "Origin": "[id of origin of metadata]"`  
`                   "Uri": "[preset uri]"`  
`                   "Artwork": "[image url]"`  
`               }`  
`           },`  
`           ........    `  
`       ]`  
`   }`

</tt>

## <span id="UPnP_Service_Description"></span>UPnP Service Description

For devices supporting the UPnP protocol, the service description is

`name: "Radio"`  
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
      <name>Id</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>IdArray</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>ChannelsMax</name>
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
