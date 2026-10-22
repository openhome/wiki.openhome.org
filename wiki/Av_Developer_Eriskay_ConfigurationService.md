---
title: "Av:Developer:Eriskay:ConfigurationService"
permalink: "/wiki/Av:Developer:Eriskay:ConfigurationService"
redirect_from:
---

{% raw %}
# <span id="Configuration_Service"></span>Configuration Service

## <span id="Overview"></span>Overview

The Configuration service provides access to all user-configurable values on a product. It is intended as a developer aid only - configuration UIs should use the web app framework instead.

If a device's [ Device](/wiki/Av:Developer:Eriskay:DeviceService) service to reports the attribute `openhome.org.configuration` in its `version` section, that device is guaranteed to bear the Configuration service. If the Configuration service is available, all its properties and actions must be fully implemented.

## <span id="Actions"></span>Actions

### <span id="GetKeys"></span>GetKeys

`Arguments: (out string keys)`  
Read a JSON list of all configuration items for the product.

### <span id="SetValue"></span>SetValue

`Arguments: (in string key, in string value)`  
Update the value of a configuration item.

Returns a `800` fault code if the specified key does not match a configuration item.  
Returns a `801` fault code if the configuration item has integer type but the specified value is not a number.  
Returns a `802` fault code if the configuration item has integer type but the specified value is outside the permitted range.  
Returns a `803` fault code if the configuration item has a list of allowed values and the specified value is not in this allowed list.  
Returns a `804` fault code if the specified value is longer than the maximum storage available for the configuration item.

### <span id="GetValue"></span>GetValue

`Arguments: (in string key, out string value)`  
Read the value of a configuration item.  
The return value is always text; the caller is responsible for converting this to an integer if necessary.

Returns a `800` fault code if the specified key does not match a configuration item.

## <span id="UPnP_Service_Description"></span>UPnP Service Description

For devices supporting the UPnP protocol, the service description is

`name: "Configuration"`  
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
      <name>GetKeys</name>
      <argumentList>
        <argument>
          <name>KeyList</name>
          <direction>out</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SetValue</name>
      <argumentList>
        <argument>
          <name>Key</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Value</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>GetValue</name>
      <argumentList>
        <argument>
          <name>Key</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
  </actionList>
  <serviceStateTable>
    <stateVariable sendEvents="no">
      <name>A_ARG_TYPE_String</name>
      <dataType>string</dataType>
    </stateVariable>
  </serviceStateTable>
</scpd>
```
{% endraw %}
