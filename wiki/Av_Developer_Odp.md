---
title: "Av:Developer:Odp"
permalink: "/wiki/Av:Developer:Odp"
redirect_from:
---

{% raw %}
# <span id="OpenHome_Device_Protocol"></span>OpenHome Device Protocol

## <span id="Overview"></span>Overview

OpenHome Device Protocl (ODP) allows a control point to control and receive evented updates from an OpenHome device using a single TCP socket. This has some advantages over UPnP:

- No need to define error handling policy for cases where evented updates cannot be delivered.  
  If the socket connection is open, it'll be possible to deliver an evented update.  
  If the socket connection is broken, the device can automatically clean up all subscriptions from that control point.
- No need to define additional protocol to allow control points to infer removal of a device.  
  If the socket connection is open, a control point can assume the device is available.  
  If the socket connection is broken, the control point is immediately prompted to retry connection; if this fails, it can quickly update its state to show that the device is no longer available.
- No danger of TIME_WAIT socket errors when control points invoke very large numbers of actions and/or devices are rebooted.

## <span id="Discovery"></span>Discovery

Using mDNS, search for `_openhome._odp` to identify an ODP endpoint.

## <span id="Sample_Code"></span>Sample Code

[ohPipeline](https://github.com/openhome/ohPipeline) contains [reference code](https://github.com/openhome/ohPipeline/tree/master/OpenHome/Net/Odp) for control point or device stacks.

Control point authors can instantiate [CpiDeviceOdp](https://github.com/openhome/ohPipeline/blob/master/OpenHome/Net/Odp/Tests/CpiDeviceOdp.h) then use standard ohNet proxy classes to access all OpenHome network services. Proxies can be generated from UPnP service XML; pre-generated versions are available in [ohNetGenerated](https://github.com/openhome/ohNetGenerated).

See [ODP test code](https://github.com/openhome/ohPipeline/blob/master/OpenHome/Net/Odp/Tests/TestDvOdp.cpp) for a simple example of a control point invoking actions and receiving evented updates over ODP.

Sample code for mDNS discovery of ODP devices is coming soon.

## <span id="Protocol"></span>Protocol

### <span id="Framing"></span>Framing

Each message, in either direction, is a JSON object followed by a newline (`'\n'`)

### <span id="Announcement"></span>Announcement

When a client connects, a device announces its capabilities:

`   {`  
`       "type":"announcement",`  
`       "protocolVersion":3,`  
`       "devices": [`  
`           {`  
`               "id":"udn",`  
`               "type":"one of Ds, MediaRenderer, ZoneSetup, ZoneSource, ZoneReceiver",`  
`               "services": [`  
`                   { "domain": "abc.org", "name":"service1", "version":1 },`  
`                   { "domain": "abc.org", "name":"service2", "version":2 },`  
`                   { "domain": "xyz.com", "name":"service3", "version":1 }`  
`               ]`  
`           },`  
`           {`  
`               "id": "udn",`  
`               "type":"one of Ds, MediaRenderer, ZoneSetup, ZoneSource, ZoneReceiver",`  
`               "services": [`  
`                   { "domain": "abc.org", "name":"service4", "version":1 },`  
`                   { "domain": "xyz.com", "name":"service5", "version":1 }`  
`               ]`  
`           }`  
`       ]`  
`   }`

### <span id="Control"></span>Control

The control point can invoke an action on a device as follows. This will block until a response is sent. Note that it is possible that the control point may receive other messages (e.g. `notify` - see below) before the action response.  
The name for each input argument will match the `name` element for that argument in the service description XML. All values are strings.

`   {`  
`       "type": "action",`  
`       "id": "udn",`  
`       "device": "type",`  
`       "service": { "domain": "xyz.com", "name": "service_name", "version": 1 },`  
`       "action": "action_name",`  
`       "arguments": [`  
`           { "name": "input_arg_str", "value":"json_escaped_str" },`  
`           { "name": "input_arg_bin", "value":"base64_encoded_str" },`  
`           { "name": "input_arg_bool", "value":"true" },`  
`           { "name": "input_arg_int", "value":"-1" },`  
`           { "name": "input_arg_uint", "value":"3" }`  
`           ],`  
`       "correlationId":"optional request identifier",`  
`       "userAgent":"optional client identifier"`  
`   }`

Response when action invocation is successful.  
The name for each output argument will match the `name` element for that argument in the service description XML. All values are strings.

`   {`  
`       "type": "actionResponse",`  
`       "error": null,`  
`       "arguments": [`  
`           { "name": "output_arg_str", "value":"json_escaped_str" },`  
`           { "name": "output_arg_bin", "value":"base64_encoded_str" },`  
`           { "name": "output_arg_bool", "value":"true" },`  
`           { "name": "output_arg_int", "value":"-1" },`  
`           { "name": "output_arg_uint", "value":"3" }`  
`       ],`  
`       "correlationId":"echoed from request"`  
`   }`

Response when action invocation fails:

`   {`  
`       "type": "actionResponse",`  
`       "error": { "code": 123, "description": "error msg" },`  
`       "arguments": null,`  
`       "correlationId":"echoed from request"`  
`   }`

### <span id="Eventing"></span>Eventing

Subscribe to a particular service. On successful completion, the device will send out unsolicited messages (with type `notify`) whenever one or more evented properties of a service change.

`   {`  
`       "type": "subscribe",`  
`       "id", "udn",`  
`       "device": "type",`  
`       "service": { "domain": "abc.org", "name": "service_name", "version": 2 },`  
`       "correlationId":"optional request identifier"`  
`   }`

Response when a subscribe request succeeds. The subscription id (sid) will be included in all later evented updates for this subscription.

`   {`  
`       "type": "subscribeResponse",`  
`       "device": "type",`  
`       "service": { "name": "service_name", "version": 2 }`  
`       "error": null,`  
`       "correlationId":"echoed from request",`  
`       "sid": "subscription_id"`  
`   }`

Response when a subscribe request fails. No later evented updates will be sent.

`   {`  
`       "type": "subscribeResponse",`  
`       "id", "udn",`  
`       "device": "type",`  
`       "service": { "domain": "abc.org", "name": "service_name", "version": 2 }`  
`       "error": { "code": 123, "description": "error msg" },`  
`       "correlationId":"echoed from request",`  
`       "sid": null`  
`   }`

Unsubscribe (halt a particular stream of evented updates).

`   {`  
`       "type": "unsubscribe",`  
`       "correlationId":"optional request identifier",`  
`       "sid": "subscription_id"`  
`   }`

Response when an unsubscribe completes. No evented updates for this subscription will be sent after this.

`   {`  
`       "type": "unsubscribeResponse",`  
`       "correlationId":"echoed from request"`  
`   }`

A device will send the following whenever one or more evented properties change on a service with an active subscription.  
The name for each property will match the `name` element for the associated `stateVariable` in the service description XML. All values are strings.

`   {`  
`       "type": "notify",`  
`       "sid": "subscription_id",`  
`       "properties": [`  
`           { "name": "property_str", "value":"json_escaped_str" },`  
`           { "name": "property_bin", "value":"base64_encoded_str" },`  
`           { "name": "property_bool", "value":"true" },`  
`           { "name": "property_int", "value":"-1" },`  
`           { "name": "property_uint", "value":"3" }`  
`       ]`  
`   }`
{% endraw %}
