---
title: "Av:Developer:TimeService"
permalink: "/wiki/Av:Developer:TimeService"
redirect_from:
  - "/wiki/Developer:TimeService"
---

{% raw %}
# <span id="Overview"></span>Overview

The Time service reports the duration of the currently playing track and the number of seconds played so far. It also maintains a count of the total number of tracks played.

This service is intentionally separated from the [Info](/wiki/Av:Developer:InfoService) service. When a track is being played, this service delivers an event every second, which can overwhelm some primitive control points. The `Time` service is kept separate from the [Info](/wiki/Av:Developer:InfoService) service so that control points can decide to subscribe to it independently.

# <span id="State_Variables"></span>State Variables

## <span id="Track_Count"></span>Track Count

The number of tracks that have been played, including any currently playing one.

## <span id="Duration"></span>Duration

The total length of the current track in seconds. Zero for live streams.

## <span id="Seconds"></span>Seconds

The total length of time in seconds for which the current track has been playing.

# <span id="Actions"></span>Actions

## <span id="Time"></span>Time

This reports `TrackCount`, which increments each time a new track is played; `Duration`, which is the duration of the current track in seconds; and `Seconds`, which is the number of seconds so far played.

`TrackCount` corresponds with `TrackCount` reported in the [Info](/wiki/Av:Developer:InfoService) service, but bears no relation to a Track Id or Preset Id reported from the Playlist or Radio services.

# <span id="Technical_Details"></span>Technical Details

        Domain  : av.openhome.org
        Name    : Time
        Version : 1

## <span id="Time_Service_Description_.28XML.29"></span>Time Service Description (XML)

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
