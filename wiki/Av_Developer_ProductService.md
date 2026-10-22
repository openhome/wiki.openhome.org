---
title: "Av:Developer:ProductService"
permalink: "/wiki/Av:Developer:ProductService"
redirect_from:
  - "/wiki/Developer:ProductService"
---

{% raw %}
# <span id="Architectural_Overview"></span>Architectural Overview

The Product service contains a summary of a single product’s capabilities. Control points should begin their interaction with an av.openhome device by searching for the `Product` service. Presence of various other services can be inferred from the sources and attributes this reports.

# <span id="State_Variables"></span>State Variables

## <span id="Sources"></span>Sources

### <span id="SourceCount"></span>SourceCount

The number of available sources. Must be greater than 0. Does not vary at run-time.

### <span id="SourceIndex"></span>SourceIndex

The index of the currently active source. This is zero-based so will be in the range `[0..SourceCount-1]`

### <span id="SourceXml"></span>SourceXml

Returns a summary of all sources in the form

``` xml
<SourceList>
    <Source>
        <Name>[user name for source]</Name>
        <Type>[Type of the source.  Read-only. See below for supported types]</Type>
        <Visible>[Boolean.  Whether control points should display source]</Visible>
    </sourcetag>
</SourceList>
```

Supported values for source Type are,

`- Playlist - the av.openhome.org:Playlist:1 service must be available`  
`- Radio - the av.openhome.org:Radio:1 service must be available`  
`- Receiver - the av.openhome.org:Receiver:1 service must be available`  
`- UpnpAv - the upnp.org:MediaRenderer:1 device must be available`  
`- NetAux - Specifies 3rd party, non OpenHome controllable, network protocols such as AirPlay`  
`- Analog - Specifies an analog external input`  
`- Digital - Specifies a digital external input`  
`- Hdmi - Specifies a HDMI external input`

## <span id="Network_Presentation"></span>Network Presentation

### <span id="Attributes"></span>Attributes

Space delimited set of values. Each value guarantees the availability of a service or resource, saving a control point for searching for each of these in turn. Supported values for attributes include

`- Info – the av.openhome.org:``Info:1`` service must be available`  
`- Time – the av.openhome.org:Time:1 service must be available`  
`- Volume – the av.openhome.org:Volume:1 service must be available`  
`- Sender - the av.openhome.org:Sender:1 service must be available`  
`- App:Config=[link] – web UI for device configuration must be available at the url [link]`  
`- Credentials - the av.openhome.org:Credentials:1 service must be available`

### <span id="ManufacturerImageUri"></span>ManufacturerImageUri

Uri for manufacturer’s logo. Does not vary at run-time.

### <span id="ManufacturerInfo"></span>ManufacturerInfo

Manufacturer information. Does not vary at run-time.

### <span id="ManufacturerName"></span>ManufacturerName

Manufacturer name. Does not vary at run-time.

### <span id="ManufacturerUrl"></span>ManufacturerUrl

URL for manufacturer web site. Does not vary at run-time.

### <span id="ModelImageUri"></span>ModelImageUri

Uri for model’s icon. Does not vary at run-time.

### <span id="ModelInfo"></span>ModelInfo

Model information. Does not vary at run-time.

### <span id="ModelName"></span>ModelName

Model name. Does not vary at run-time.

### <span id="ModelUrl"></span>ModelUrl

URL for model web site. Does not vary at run-time.

### <span id="ProductImageUri"></span>ProductImageUri

Uri for product image. Does not vary at run-time.

### <span id="ProductInfo"></span>ProductInfo

Product information. Does not vary at run-time.

### <span id="ProductName"></span>ProductName

User-visible product name. By default this is set to `ModelName`.  
Note that the UPnP friendly name is derived by combining this with Room name in the form `Room : Name`

### <span id="ProductRoom"></span>ProductRoom

The name of the room where the Product is located. Set to “Main Room” by default.  
ProductRoom is used to group the Product with other related Products in the same physical room (e.g. a source with a pre-amp). Products which are physically linked must always share the same `ProductRoom` name.

### <span id="ProductUrl"></span>ProductUrl

URL for product web site. This may be the UPnP presentation page.

## <span id="Standby"></span>Standby

### <span id="Standby_2"></span>Standby

The standby state of a product (true =\> standby enabled)  
Behaviour when `Standby` is enabled is implementation defined. Devices can choose whether to remain network-controllable. If a device is still network-controllable, invoking the `Play` action on any source must disable `Standby`.

# <span id="Actions"></span>Actions

## <span id="Sources_2"></span>Sources

The set of available sources does not vary at run-time (although some source attributes may change). There is always a single source active. Only the active source will play audio or report state updates.

### <span id="SourceCount_2"></span>SourceCount

Query the value of the (read-only) SourceCount state variable.

### <span id="Source"></span>Source

Given the index of a source, query the values of its name, system name, type and visibility.

### <span id="SetSourceIndex"></span>SetSourceIndex

Set the currently active source. The value specified is zero-based and used to index into the source list returned by the `SourceXml` action / state variable.

### <span id="SetSourceIndexByName"></span>SetSourceIndexByName

Set the currently active source. The value specified is matched against the `Name` attributes from the `SourceXml` action / state variable.  
Note that this action is deprecated.

### <span id="SourceXml_2"></span>SourceXml

Query the value of the `SourceXml` state variable.

### <span id="SourceXmlChangeCount"></span>SourceXmlChangeCount

Query how often the `SourceXml` state variable has been updated. This action can be polled by clients that don’t support eventing. Whenever the value returned increases, the `SourceXml` has been updated so should be queried again.

## <span id="Network_Presentation_2"></span>Network Presentation

### <span id="Attributes_2"></span>Attributes

Return the value of the `Attributes` state variable.

### <span id="Manufacturer"></span>Manufacturer

Return the values of the `ManufacturerName`, `ManufacturerInfo`, `ManufacturerUrl`, `ManufacturerImageUri` state variables. All are read-only so the values returned will not vary at runtime.

### <span id="Model"></span>Model

Return the values of the `ModelName`, `ModelInfo`, `ModelUrl`, `ModelImageUri` state variables. All are read-only so the values returned will not vary at runtime.

### <span id="Product"></span>Product

Return the values of the `ProductRoom`, `ProductName`, `ProductInfo`, `ProductUrl`, `ProductImageUri` state variables.

## <span id="Standby_3"></span>Standby

### <span id="Standby_4"></span>Standby

Return the value of the `Standby` state variable.

### <span id="SetStandby"></span>SetStandby

Set the value of the `Standby` state variable. The SetStandby action provides a means of setting the current standby state of the product.

# <span id="Product_Service_Description_.28XML.29"></span>Product Service Description (XML)

``` xml
<?xml version="1.0" encoding="utf-8"?>
<scpd xmlns="urn:schemas-upnp-org:service-1-0">
    <specVersion>
        <major>1</major>
        <minor>0</minor>
    </specVersion>
    <actionList>
        <action>
            <name>Manufacturer</name>
            <argumentList>
                <argument>
                    <name>Name</name>
                    <direction>out</direction>
                    <relatedStateVariable>ManufacturerName</relatedStateVariable>
                </argument>
                <argument>
                    <name>Info</name>
                    <direction>out</direction>
                    <relatedStateVariable>ManufacturerInfo</relatedStateVariable>
                </argument>
                <argument>
                    <name>Url</name>
                    <direction>out</direction>
                    <relatedStateVariable>ManufacturerUrl</relatedStateVariable>
                </argument>
                <argument>
                    <name>ImageUri</name>
                    <direction>out</direction>
                    <relatedStateVariable>ManufacturerImageUri</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>Model</name>
            <argumentList>
                <argument>
                    <name>Name</name>
                    <direction>out</direction>
                    <relatedStateVariable>ModelName</relatedStateVariable>
                </argument>
                <argument>
                    <name>Info</name>
                    <direction>out</direction>
                    <relatedStateVariable>ModelInfo</relatedStateVariable>
                </argument>
                <argument>
                    <name>Url</name>
                    <direction>out</direction>
                    <relatedStateVariable>ModelUrl</relatedStateVariable>
                </argument>
                <argument>
                    <name>ImageUri</name>
                    <direction>out</direction>
                    <relatedStateVariable>ModelImageUri</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>Product</name>
            <argumentList>
                <argument>
                    <name>Room</name>
                    <direction>out</direction>
                    <relatedStateVariable>ProductRoom</relatedStateVariable>
                </argument>
                <argument>
                    <name>Name</name>
                    <direction>out</direction>
                    <relatedStateVariable>ProductName</relatedStateVariable>
                </argument>
                <argument>
                    <name>Info</name>
                    <direction>out</direction>
                    <relatedStateVariable>ProductInfo</relatedStateVariable>
                </argument>
                <argument>
                    <name>Url</name>
                    <direction>out</direction>
                    <relatedStateVariable>ProductUrl</relatedStateVariable>
                </argument>
                <argument>
                    <name>ImageUri</name>
                    <direction>out</direction>
                    <relatedStateVariable>ProductImageUri</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>Standby</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>out</direction>
                    <relatedStateVariable>Standby</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>SetStandby</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>in</direction>
                    <relatedStateVariable>Standby</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>SourceCount</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>out</direction>
                    <relatedStateVariable>SourceCount</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>SourceXml</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>out</direction>
                    <relatedStateVariable>SourceXml</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>SourceIndex</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>out</direction>
                    <relatedStateVariable>SourceIndex</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>SetSourceIndex</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>in</direction>
                    <relatedStateVariable>SourceIndex</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>SetSourceIndexByName</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>in</direction>
                    <relatedStateVariable>SourceName</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>Source</name>
            <argumentList>
                <argument>
                    <name>Index</name>
                    <direction>in</direction>
                    <relatedStateVariable>SourceIndex</relatedStateVariable>
                </argument>
                <argument>
                    <name>SystemName</name>
                    <direction>out</direction>
                    <relatedStateVariable>SourceName</relatedStateVariable>
                </argument>
                <argument>
                    <name>Type</name>
                    <direction>out</direction>
                    <relatedStateVariable>SourceType</relatedStateVariable>
                </argument>
                <argument>
                    <name>Name</name>
                    <direction>out</direction>
                    <relatedStateVariable>SourceName</relatedStateVariable>
                </argument>
                <argument>
                    <name>Visible</name>
                    <direction>out</direction>
                    <relatedStateVariable>SourceVisible</relatedStateVariable>
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
        <action>
            <name>SourceXmlChangeCount</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>out</direction>
                    <relatedStateVariable>SourceXmlChangeCount</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
    </actionList>
    <serviceStateTable>
        <stateVariable sendEvents="yes">
            <name>ManufacturerName</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ManufacturerInfo</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ManufacturerUrl</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ManufacturerImageUri</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ModelName</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ModelInfo</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ModelUrl</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ModelImageUri</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ProductRoom</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ProductName</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ProductInfo</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ProductUrl</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>ProductImageUri</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>Standby</name>
            <dataType>boolean</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>SourceIndex</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>SourceCount</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>SourceXml</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>Attributes</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>SourceXmlChangeCount</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>SourceType</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>SourceName</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="no">
            <name>SourceVisible</name>
            <dataType>boolean</dataType>
        </stateVariable>
    </serviceStateTable>
</scpd>
```
{% endraw %}
