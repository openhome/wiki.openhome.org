---
title: "Av:Developer:Eriskay:TimeService"
permalink: "/wiki/Av:Developer:Eriskay:TimeService"
redirect_from:
---

{% raw %}
# <span id="Time_Service"></span>Time Service

## <span id="Overview"></span>Overview

The Time service reports the duration of the currently playing track and the number of seconds played so far. It also maintains a count of the total number of tracks played.

If a device's [ Product](/wiki/Av:Developer:Eriskay:ProductService) service reports an attribute `"Time"`, then that device is guaranteed to bear the Time service.

This service is intentionally separated from the [ Transport](/wiki/Av:Developer:Eriskay:TransportService) service. When a track is being played, `Time` delivers an event every second, which can overwhelm some primitive control points. Keeping `Time` separate from the \["TransportServiceEriskay" Transport\] service allows control points to decide whether to subscribe to it independently.

## <span id="Evented_Properties"></span>Evented Properties

### <span id="Track_Count"></span>Track Count

The number of tracks that have been played, including any currently playing one.

`TrackCount` corresponds with the `TrackCount` property reported by the \["TransportServiceEriskay" Transport\] service, but bears no relation to a track or preset `Id` properties reported from the \["PlaylistServiceEriskay" Playlist\] or \["RadioServiceEriskay" Radio\] services.

### <span id="Duration"></span>Duration

The total length of the current track in seconds. Zero for live streams.

### <span id="Seconds"></span>Seconds

The total length of time in seconds for which the current track has been playing.

## <span id="Actions"></span>Actions

### <span id="Time"></span>Time

Return the values of the `TrackCount`, `Duration` and `Seconds` properties.

## <span id="UPnP_Service_Description"></span>UPnP Service Description

For devices supporting the UPnP protocol, the service description is

`name: "Time"`  
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
      <name>Time</name>
      <argumentList>
        <argument>
          <name>TrackCount</name>
          <direction>out</direction>
          <relatedStateVariable>TrackCount</relatedStateVariable>
        </argument>
        <argument>
          <name>Duration</name>
          <direction>out</direction>
          <relatedStateVariable>Duration</relatedStateVariable>
        </argument>
        <argument>
          <name>Seconds</name>
          <direction>out</direction>
          <relatedStateVariable>Seconds</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
  </actionList>
  <serviceStateTable>
    <stateVariable sendEvents="yes">
      <name>TrackCount</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Duration</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Seconds</name>
      <dataType>ui4</dataType>
    </stateVariable>
  </serviceStateTable>
</scpd>
```
{% endraw %}
