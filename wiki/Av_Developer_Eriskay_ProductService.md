---
title: "Av:Developer:Eriskay:ProductService"
permalink: "/wiki/Av:Developer:Eriskay:ProductService"
redirect_from:
---

{% raw %}
# <span id="Product_Service"></span>Product Service

## <span id="Overview"></span>Overview

The Product service contains a summary of a single product’s capabilities. After using the [ Device](/wiki/Av:Developer:Eriskay:DeviceService) service to confirm both compatibility and the presence of the `openhome.org.product` attribute, control points should begin their interaction with an OpenHome device by using the Product service. Presence of various other services can be inferred from the sources and attributes this reports.

If the Product service is available, all its properties and actions must be fully implemented.

## <span id="Evented_Properties"></span>Evented Properties

### <span id="SourceArray"></span>SourceArray

Returns a summary of all sources as a JSON array: <tt>

`   [`  
`       {`  
`           "name": "user name for source"`  
`           "type": "type of source"`  
`           "visible": "Boolean.  Whether control points should display source"`  
`           "systemName": "default name for source"`  
`       }`  
`   ]`

</tt> Source `type` may have any implementation-defined value. The following values have a commonly understood meaning:

- `Playlist` - the `openhome.org.eriskay:Playlist:1` service must be available
- `Radio` - the `openhome.org.eriskay:Radio:1` service must be available
- `Receiver` - the `openhome.org.eriskay:Receiver:1` service must be available
- `UpnpAv` - the `upnp.org:MediaRenderer:1` device must be available
- `Single` - software source that plays a single track
- `NetAux` - Specifies 3rd party, non OpenHome controllable, network protocols such as AirPlay
- `Analog` - Specifies an analog external input
- `Digital` - Specifies a digital external input
- `Hdmi` - Specifies a HDMI external input

Other implementation-defined values are possible. Control points that have not been developed to support them should treat such sources as comparable to external inputs.

Each `systemName` is guaranteed to be unique within the array.

### <span id="SourceSystemName"></span>SourceSystemName

The `systemName` of the currently active source.

### <span id="Attributes"></span>Attributes

Space delimited set of values. Each value guarantees the availability of a service or resource, saving a control point from searching for each of these in turn. Supported values for attributes include

- `Transport` – the `openhome.org.eriskay:Transport:1` service must be available
- `Time` – the `openhome.org.eriskay:Time:1` service must be available
- `Volume` – the `openhome.org.eriskay:Volume:1` service must be available
- `Sender` - the `openhome.org.eriskay:Sender:1` service must be available
- `Credentials` - the `openhome.org.eriskay:Credentials:1` service must be available

### <span id="Name"></span>Name

User-visible product name. By default this is set to the model name as reported by the Device service. Note that the UPnP friendly name is derived by combining this with Room name in the form `Room : Name`.

### <span id="Room"></span>Room

The name of the room where the Product is located. `Room` is used to group the Product with other related Products in the same physical room (e.g. a source with a pre-amp). Products which are physically linked must always share the same `Room` name.

### <span id="Home"></span>Home

User-visible name for a home (a collection of rooms). Reserved for future use.

## <span id="Actions"></span>Actions

### <span id="SourceArray_2"></span>SourceArray

`Arguments: (out string array)`  
Return the value of the `SourceArray` property.

### <span id="SourceArrayChangeCount"></span>SourceArrayChangeCount

`Arguments: (out uint count)`  
Query how often the `SourceArray` property has been updated. This action can be polled by clients that don’t support eventing. Whenever the value returned increases, `SourceArray` has been updated so should be queried again.

### <span id="SourceSystemName_2"></span>SourceSystemName

`Arguments: (out string systemName)`  
Return the value of the `SourceSystemName` property.

### <span id="SetSource"></span>SetSource

`Arguments: (in string systemName)`  
Set the currently active source to the one with the specified system name.

### <span id="Attributes_2"></span>Attributes

`Arguments: (out string attributes)`  
Return the value of the `Attributes` property.

### <span id="Names"></span>Names

`Arguments: (out string room, out string name, out string home)`  
Return the values of the `Room`, `Name` and `Home` properties.

## <span id="UPnP_Service_Description"></span>UPnP Service Description

For devices supporting the UPnP protocol, the service description is

`name: "Product"`  
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
      <name>Names</name>
      <argumentList>
        <argument>
          <name>Room</name>
          <direction>out</direction>
          <relatedStateVariable>Room</relatedStateVariable>
        </argument>
        <argument>
          <name>Name</name>
          <direction>out</direction>
          <relatedStateVariable>Name</relatedStateVariable>
        </argument>
        <argument>
          <name>Home</name>
          <direction>out</direction>
          <relatedStateVariable>Home</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SourceArray</name>
      <argumentList>
        <argument>
          <name>Array</name>
          <direction>out</direction>
          <relatedStateVariable>SourceArray</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SetSource</name>
      <argumentList>
        <argument>
          <name>Index</name>
          <direction>in</direction>
          <relatedStateVariable>SourceSystemName</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Attributes</name>
      <argumentList>
        <argument>
          <name>Attributes</name>
          <direction>out</direction>
          <relatedStateVariable>Attributes</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SourceSystemName</name>
      <argumentList>
        <argument>
          <name>SourceSystemName</name>
          <direction>out</direction>
          <relatedStateVariable>Attributes</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SourceArrayChangeCount</name>
      <argumentList>
        <argument>
          <name>Count</name>
          <direction>out</direction>
          <relatedStateVariable>SourceArrayChangeCount</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
  </actionList>
  <serviceStateTable>
    <stateVariable sendEvents="yes">
      <name>Room</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Name</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Home</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>SourceSystemName</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>SourceArray</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Attributes</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>SourceArrayChangeCount</name>
      <dataType>ui4</dataType>
    </stateVariable>
  </serviceStateTable>
</scpd>
```
{% endraw %}
