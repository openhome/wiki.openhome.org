---
title: "Av:Developer:Eriskay:CredentialsService"
permalink: "/wiki/Av:Developer:Eriskay:CredentialsService"
redirect_from:
---

{% raw %}
# <span id="Credentials_Service"></span>Credentials Service

## <span id="Overview"></span>Overview

The Credentials service provides access to username, password and current status of all remote services that require unique logins.

If a device's [ Product](/wiki/Av:Developer:Eriskay:ProductService) service reports an attribute `"Credentials"`, then that device is guaranteed to bear the Credentials service. If the Credentials service is available, all its properties and actions must be fully implemented.

## <span id="Evented_Properties"></span>Evented Properties

### <span id="Ids"></span>Ids

Space separated list of identifiers for services whose credentials can be set.  
Set on startup; does not change at runtime.

### <span id="PublicKey"></span>PublicKey

RSA public key that must be used to encrypt any/all passwords.

When encrypting ensure PKCS1 OAEP padding is used.

May be blank on startup; will not vary once set. With the exception of the `Ids` state variable, the rest of the service cannot usefully be used before this is set.

### <span id="SequenceNumber"></span>SequenceNumber

Increases whenever any aspect of state for any user of credentials listed in `Ids` changes. The client is responsible for polling each Id they are interested in to determine what has changed.

## <span id="Actions"></span>Actions

### <span id="Set"></span>Set

`Arguments: (in string id, in string username, in string password)`  
Set the username and password for a given service. The password must be encrypted using the RSA public key in the `PublicKey` state variable.  
Calling this action automatically enables the service.  
Note that some processing may happen asynchronously. If any of username, password or enabled states are changed for the service, `SequenceNumber` will automatically change.

Returns a `800` fault code if the `Id` argument is invalid.

### <span id="Clear"></span>Clear

`Arguments: (in string id)`  
Remove both username and password for a given service.  
Note that some processing may happen asynchronously. If any of username, password or enabled states are changed for the service, `SequenceNumber` will automatically change.

Returns a `800` fault code if the `Id` argument is invalid.

### <span id="SetEnabled"></span>SetEnabled

`Arguments: (in string id, in bool enabled`  
Set or clear the `Enabled` state of a service. Disabling a service temporarily prevents its use by a device but allows the device to retain the username/password for later use (if the service is re-enabled by calling `SetEnabled()` again).

Returns a `800` fault code if the `Id` argument is invalid.

### <span id="Get"></span>Get

`Arguments: (in string id, out string username, out string encPassword, out bool enabled, out string status, out string data)`  
Retrieve username, password, status and enabled state for a service.

Username, password and enabled will only change in response to invocations of the Credentials service. The password is encrypted so is not suitable for user display. Clients can infer whether a password has been set by checking whether the value returned has non-zero length.

Status may change in response to runtime events. e.g. If an account expires, the status may change to include the error returned by the remote service provider. Status is only set for error cases - a blank status indicates that a service is functioning correctly. The exact format of status content varies between services.

Data contains any other service-specific information. The format of content varies between services.

Returns a `800` fault code if the `Id` argument is invalid.

### <span id="Login"></span>Login

`Arguments: (in string id, out string token)`  
Read a token indicating that a registered user has logged in to a remote service. This allows control points to access data that is specific to a certain user account without requiring access to the (sensitive) password for that account. The data returned may vary between credential-consuming services; the control point is responsible for knowing how to interpret it.

Returns a `800` fault code if the `Id` argument is invalid.  
Returns a `801` fault code if the login was attempted but failed.

### <span id="Relogin"></span>Relogin

`Arguments: (in string id, in string currentToken, out string newToken)`  
Refresh an existing token returned from `Login()`. This should only be called after the remote service has indicated that the current token has expired and is no longer valid.

Returns a `800` fault code if the `Id` argument is invalid.  
Returns a `801` fault code if a new login was attempted but failed.

### <span id="GetIds"></span>GetIds

`Arguments: (out string ids)`  
Read the value of the `Ids` property.

### <span id="GetPublicKey"></span>GetPublicKey

`Arguments: (out string key)`  
Read the value of the `PublicKey` property.

### <span id="GetSequenceNumber"></span>GetSequenceNumber

`Arguments: (out uint seq)`  
Read the value of the `SequenceNumber` property.

## <span id="UPnP_Service_Description"></span>UPnP Service Description

For devices supporting the UPnP protocol, the service description is

`name: "Credentials"`  
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
      <name>Set</name>
      <argumentList>
        <argument>
          <name>Id</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>UserName</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Password</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_Binary</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Clear</name>
      <argumentList>
        <argument>
          <name>Id</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SetEnabled</name>
      <argumentList>
        <argument>
          <name>Id</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Enabled</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_Bool</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Get</name>
      <argumentList>
        <argument>
          <name>Id</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>UserName</name>
          <direction>out</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Password</name>
          <direction>out</direction>
          <relatedStateVariable>A_ARG_TYPE_Binary</relatedStateVariable>
        </argument>
        <argument>
          <name>Enabled</name>
          <direction>out</direction>
          <relatedStateVariable>A_ARG_TYPE_Bool</relatedStateVariable>
        </argument>
        <argument>
          <name>Status</name>
          <direction>out</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Data</name>
          <direction>out</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Login</name>
      <argumentList>
        <argument>
          <name>Id</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>Token</name>
          <direction>out</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Relogin</name>
      <argumentList>
        <argument>
          <name>Id</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>CurrentToken</name>
          <direction>in</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
        <argument>
          <name>NewToken</name>
          <direction>out</direction>
          <relatedStateVariable>A_ARG_TYPE_String</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>GetIds</name>
      <argumentList>
        <argument>
          <name>Ids</name>
          <direction>out</direction>
          <relatedStateVariable>Ids</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>GetPublicKey</name>
      <argumentList>
        <argument>
          <name>PublicKey</name>
          <direction>out</direction>
          <relatedStateVariable>PublicKey</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>GetSequenceNumber</name>
      <argumentList>
        <argument>
          <name>SequenceNumber</name>
          <direction>out</direction>
          <relatedStateVariable>SequenceNumber</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
  </actionList>
  <serviceStateTable>
    <stateVariable sendEvents="yes">
      <name>Ids</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>PublicKey</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>SequenceNumber</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>A_ARG_TYPE_String</name>
      <dataType>string</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>A_ARG_TYPE_Binary</name>
      <dataType>bin.base64</dataType>
    </stateVariable>
    <stateVariable sendEvents="no">
      <name>A_ARG_TYPE_Bool</name>
      <dataType>boolean</dataType>
    </stateVariable>
  </serviceStateTable>
</scpd>
```
{% endraw %}
