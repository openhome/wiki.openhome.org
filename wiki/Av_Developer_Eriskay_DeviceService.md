---
title: "Av:Developer:Eriskay:DeviceService"
permalink: "/wiki/Av:Developer:Eriskay:DeviceService"
redirect_from:
---

{% raw %}
# <span id="Device_Service"></span>Device Service

## <span id="Overview"></span>Overview

The Device service serves as the starting point for retrieving information about an OpenHome device and resolving questions of compatibility between that device and an OpenHome control point.

Before consuming further services, an OpenHome control point MUST engage with the Device service in order to establish whether the device is compatible with the OpenHome client software with which the control point was built.

An OpenHome control point SHOULD indicate to the user the presence of any incompatible device on the network but MUST NOT engage with the device beyond this requirement.

In this situation the device can be identified to the user using the version-independent information provided by the Device service: primarily the name and manufacturer information.

In addition to describing standard OpenHome capabilities, the Device service can be used to publish the presence of vendor-specific enhancements using the version-specific attributes property.

The Device service may also be used to publish the availability of both standard and vendor-specific web applications using the webapps property.

Further free-form vendor-specific information can be included in the JSON document using the extensions property.

The Device publishes read-only information about an OpenHome device using its Description property, which is in JSON format and has the following JSON-Schema. <tt>

`   {`  
`       "title": "OpenHome Device Description",`  
`       "$schema": "`[`http://json-schema.org/draft-04/schema#`](http://json-schema.org/draft-04/schema#)`",`  
`       "properties": {`  
`           "name": {`  
`               "type": "string"`  
`           },`  
`           "domain": {`  
`               "type": "string"`  
`           },`  
`           "id": {`  
`               "type": "string"`  
`           },`  
`           "manufacturer" : {`  
`               "type": "object",`  
`               "properties": {`  
`                   "name": {`  
`                       "type": "string"`  
`                   },`  
`                   "info": {`  
`                       "type": "string"`  
`                   },`  
`                   "url": {`  
`                       "type": "string"`  
`                   },`  
`                   "image": {`  
`                       "type": "string"`  
`                   }`  
`               },`  
`               "required": ["name"]`  
`           },`  
`           "model" : {`  
`               "type": "object",`  
`               "properties": {`  
`                   "name": {`  
`                       "type": "string"`  
`                   },`  
`                   "info": {`  
`                       "type": "string"`  
`                   },`  
`                   "url": {`  
`                       "type": "string"`  
`                   },`  
`                   "image": {`  
`                       "type": "string"`  
`                   }`  
`               },`  
`               "required": ["name"]`  
`           },`  
`           "webapps" : {`  
`               "type": "array",`  
`               "items": {`  
`                   "type": "object",`  
`                   "properties": {`  
`                       "id" : {`  
`                           "type": "string",`  
`                       },`  
`                       "url": {`  
`                           "type": "string",`  
`                       }`  
`                   },`  
`                   "required": ["id", "url"]`  
`               },`  
`               "minItems": 1,`  
`               "uniqueItems": true`  
`           },`  
`           "versions" : {`  
`               "type": "array",`  
`               "items": {`  
`                   "type": "object",`  
`                   "properties": {`  
`                       "version" : {`  
`                           "type": "integer",`  
`                           "minimum" : 5`  
`                       },`  
`                       "attributes": {`  
`                           "type": "array",`  
`                           "items": {`  
`                               "type": "string"`  
`                           },`  
`                           "minItems": 1,`  
`                           "uniqueItems": true`  
`                       }`  
`                   },`  
`                   "required": ["version"]`  
`               },`  
`               "minItems": 1,`  
`               "uniqueItems": true`  
`           },`  
`           "extensions" : {`  
`           }`  
`       },`  
`       "required": [`  
`         "name",`  
`         "domain",`  
`         "id",`  
`         "manufacturer",`  
`         "model",`  
`         "versions"`  
`       ],`  
`       "additionalProperties": false`  
`   }`

</tt>

### <span id="Examples"></span>Examples

A typical device supporting Eriskay (OpenHome Version 5) <tt>

`   {`  
`       "name": "Kitchen:Sneaky DS",`  
`       "domain": "linn.co.uk",`  
`       "id": "1203431",`  
`       "manufacturer" : {`  
`         "name": "Linn",`  
`         "info": "just listen"`  
`         "url": "`[`http://www.linn.co.uk`](http://www.linn.co.uk)`",`  
`         "image": "/images/logo.png"`  
`       },`  
`       "model" : {`  
`         "name": "Sneaky DS",`  
`         "url": "`[`http://www.linn.co.uk//wiki/index.php/sneaky`](http://www.linn.co.uk//wiki/index.php/sneaky)`",`  
`         "image": "/images/icon.png"`  
`       },`  
`       "webapps": [`  
`           {`  
`             "id": "openhome.org.presentation",`  
`             "url": "/index.html"`  
`           },`  
`           {`  
`             "id": "openhome.org.configuration",`  
`             "url": "/Config/Layouts/Default/index.html?service=Ds"`  
`           },`  
`           {`  
`             "id": "openhome.org.control",`  
`             "url": "Control/Layouts/Default/index.html?service=Ds"`  
`           }`  
`       ],`  
`       "versions": [`  
`           {`  
`               "version": 5`  
`           }`  
`       ],`  
`       "extensions": {`  
`           "bsp": "magma",`  
`             "mac": "00:26:0f:21:82:e9",`  
`           "software": "4.25.1134",`  
`           "boards" : [`  
`             {`  
`               "pcb": 723,`  
`               "type": "PCAS723L2R3",`  
`               "id": "070000041bdec314",`  
`                 "description": ""`  
`             }`  
`           ]`  
`       }`  
`   }`

</tt>

A device that supports Eriskay (OpenHome Version 5) and Fetlar (OpenHome Version 6). The device implements the Linn Exakt extension in Version 5 and 6, and the Linn Exakt v2 extension in version 6. <tt>

`   {`  
`       "name": "Bedroom:Akurate DSM",`  
`       "domain": "linn.co.uk",`  
`       "id": "1286201",`  
`       "manufacturer" : {`  
`         "name": "Linn",`  
`         "url": "`[`http://www.linn.co.uk`](http://www.linn.co.uk)`",`  
`         "image": "/images/logo.png"`  
`       },`  
`       "model" : {`  
`         "name": "Akurate DSM",`  
`         "url": "`[`http://www.linn.co.uk//wiki/index.php/akurate-dsm`](http://www.linn.co.uk//wiki/index.php/akurate-dsm)`",`  
`         "image": "/images/icon.png"`  
`       },`  
`       "webapps": [`  
`           {`  
`             "id": "openhome.org.presentation",`  
`             "url": "/index.html"`  
`           },`  
`           {`  
`             "id": "openhome.org.configuration",`  
`             "url": "/Config/Layouts/Default/index.html?service=Ds"`  
`           },`  
`           {`  
`             "id": "openhome.org.control",`  
`             "url": "/Control/Layouts/Default/index.html?service=Ds"`  
`           }`  
`       ],`  
`       "versions": [`  
`           {`  
`               "version": 5,`  
`               "attributes": [`  
`                   "openhome.org.topology",`  
`                   "linn.co.uk.exakt"`  
`               ]`  
`           },`  
`           {`  
`               "version": 6,`  
`               "attributes": [`  
`                   "openhome.org.topology",`  
`                   "linn.co.uk.exakt",`  
`                   "linn.co.uk.exakt2"`  
`               ]`  
`           }`  
`       ],`  
`       "extensions": {`  
`           "bsp": "magma",`  
`             "mac": "00:26:0f:21:b1:18",`  
`           "software": "4.24.1066",`  
`           "boards" : [`  
`               {`  
`                 "pcb": 797,`  
`                 "type": "PCAS797L1R1",`  
`                 "id": "db000004d775f014",`  
`                 "description": "2011 variant"`  
`                 },`  
`               {`  
`                 "pcb": 802,`  
`                 "type": "PCAS802L3R1",`  
`                 "id": "9f00000505929814",`  
`                 "description": ""`  
`                 },`  
`               {`  
`                 "pcb": 611,`  
`                 "type": "PCAS611L1R2",`  
`                 "id": "45000004d7a73414",`  
`                 "description": "Moving Coil"`  
`                 },`  
`               {`  
`                 "pcb": 799,`  
`                 "type": "PCAS799L2R1",`  
`                 "id": "5f000004d7757214",`  
`                 "description": ""`  
`                 }`  
`           ]`  
`       }`  
`   }`

</tt>

### <span id="Difference_Between_Device_Service_Attributes_and_Product_Service_Attributes"></span>Difference Between Device Service Attributes and Product Service Attributes

Those attributes that are necessary for the operation of OpenHome Topology remain in the Product service. These include `Info`, `Time`, `Volume`, `Credentials`, and `Sender`.

The `Exakt` attribute is now more sensibly expressed in the Device service. And the functionality of the `App:Config` attribute is now delivered, not as an attribute, but using the `webapps` property of the Device service.

## <span id="Evented_Properties"></span>Evented Properties

### <span id="Description"></span>Description

A device description in the format outlined above.  
Does not change at run-time.

## <span id="Actions"></span>Actions

### <span id="Description_2"></span>Description

Read the value of the `Description` property.

## <span id="UPnP_Service_Description"></span>UPnP Service Description

For devices supporting the UPnP protocol, the service description is

`name: "Device"`  
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
      <name>Description</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>Description</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
  </actionList>
  <serviceStateTable>
    <stateVariable sendEvents="yes">
      <name>Description</name>
      <dataType>string</dataType>
    </stateVariable>
  </serviceStateTable>
</scpd>
```
{% endraw %}
