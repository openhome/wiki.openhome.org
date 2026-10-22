---
title: "Av:Developer:InfoService"
permalink: "/wiki/Av:Developer:InfoService"
redirect_from:
  - "/wiki/Developer:InfoService"
---

{% raw %}
# <span id="Overview"></span>Overview

The Info service provides information concerning the currently playing media. The information provided is based on the concept of a track, which has a URI and metadata in DIDL-Lite format. Some time after the track changes further information becomes available such as the bit-rate, sample-rate, bit-depth, etc. Optionally a track may contain dynamic textual information (known as metatext) that is updated as the track is played. Metatext is typically used to convey broadcast information from Internet radio stations.

# <span id="Actions"></span>Actions

## <span id="Counters"></span>Counters

Counters are used to version Track, Details, and Metatext information in the face of dynamic changes.

The Counters action can be used by clients that are unable to partake in UPnP eventing in order to track changes in the information provided by the Info Service.

When a track changes, the Track Count is incremented, the URI and Metadata are set, the Details Count is set to zero, the Details are defaulted to blank and zero values, the Metatext Count is set to zero, and the Metatext is set to blank.

Subsequent updates to the Details and Metatext are accompanied by increments in their respective Counters.

## <span id="Track"></span>Track

Reports current track information concerning the current media:

- URI
- Metadata

## <span id="Details"></span>Details

Reports details concerning the current media:

- Duration
- Bit Rate
- Bit Depth
- Sample Rate
- Lossless
- Codec Name

## <span id="Metatext"></span>Metatext

Reports dynamic textual information concerning the current media.

This currently amounts to broadcast information from Internet radio stations, but the same mechanism could be used for other purposes in the future.

# <span id="State_Variables"></span>State Variables

## <span id="TrackCount"></span>TrackCount

the strictly monotonically increasing integer number of tracks played (incl. current one)

## <span id="DetailsCount"></span>DetailsCount

the strictly monotonically increasing integer number versioning changes in track encoding parameters (duration, bitrate, bitdepth, samplerate, lossy compression, codec); reset to zero on each track change

## <span id="MetatextCount"></span>MetatextCount

the strictly monotonicallyl increasing integer number versioning changes in any text associated with the currently playing track; reset to zero on each track change

## <span id="Uri"></span>Uri

the Universal Resource Indicator, indicating the currently playing track; initially empty string

## <span id="Metadata"></span>Metadata

the DIDL-Lite encoded string of information about the currently playing track (e.g. artist, album, year, etc.); initially empty string

## <span id="Duration"></span>Duration

the length of the currently playing track in seconds

## <span id="BitRate"></span>BitRate

the dataflow rate in bits per second of the currently playing track in its encoded representation(XXX) XXX MP3: CBR vs. VBR

## <span id="BitDepth"></span>BitDepth

the sample (data) resolution in bits per channel sample of the currently playing track

## <span id="SampleRate"></span>SampleRate

the time resolution of samples per second in kHz of the currently playing track

## <span id="Lossless"></span>Lossless

the indication of whether the currently playing track can be decoded (decompressed) to a bit-accurate representation of the original audio data (lossless) or merely to a good approximation (lossy encoding)

## <span id="CodecName"></span>CodecName

the shorthand name for the audio encoding and container format used to represent the currently playing track (e.g. AAC); initially empty string

## <span id="Metatext_2"></span>Metatext

the additional textual information (if any) associated with the currently playing track

# <span id="Technical_Details"></span>Technical Details

        Domain  : av.openhome.org
        Name    : Info
        Version : 1

## <span id="Info_Service_Description_.28XML.29"></span>Info Service Description (XML)

``` xml
<?xml version="1.0" encoding="utf-8"?>
<scpd xmlns="urn:schemas-upnp-org:service-1-0">
    <specVersion>
        <major>1</major>
        <minor>0</minor>
    </specVersion>
    <actionList>
        <action>
            <name>Counters</name>
            <argumentList>
                <argument>
                    <name>TrackCount</name>
                    <direction>out</direction>
                    <relatedStateVariable>TrackCount</relatedStateVariable>
                </argument>
                <argument>
                    <name>DetailsCount</name>
                    <direction>out</direction>
                    <relatedStateVariable>DetailsCount</relatedStateVariable>
                </argument>
                <argument>
                    <name>MetatextCount</name>
                    <direction>out</direction>
                    <relatedStateVariable>MetatextCount</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>Track</name>
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
            <name>Details</name>
            <argumentList>
                <argument>
                    <name>Duration</name>
                    <direction>out</direction>
                    <relatedStateVariable>Duration</relatedStateVariable>
                </argument>
                <argument>
                    <name>BitRate</name>
                    <direction>out</direction>
                    <relatedStateVariable>BitRate</relatedStateVariable>
                </argument>
                <argument>
                    <name>BitDepth</name>
                    <direction>out</direction>
                    <relatedStateVariable>BitDepth</relatedStateVariable>
                </argument>
                <argument>
                    <name>SampleRate</name>
                    <direction>out</direction>
                    <relatedStateVariable>SampleRate</relatedStateVariable>
                </argument>
                <argument>
                    <name>Lossless</name>
                    <direction>out</direction>
                    <relatedStateVariable>Lossless</relatedStateVariable>
                </argument>
                <argument>
                    <name>CodecName</name>
                    <direction>out</direction>
                    <relatedStateVariable>CodecName</relatedStateVariable>
                </argument>
            </argumentList>
        </action>
        <action>
            <name>Metatext</name>
            <argumentList>
                <argument>
                    <name>Value</name>
                    <direction>out</direction>
                    <relatedStateVariable>Metatext</relatedStateVariable>
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
            <name>DetailsCount</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>MetatextCount</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
          <name>Uri</name>
          <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
          <name>Metadata</name>
          <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>Duration</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>BitRate</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>BitDepth</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>SampleRate</name>
            <dataType>ui4</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>Lossless</name>
            <dataType>boolean</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
            <name>CodecName</name>
            <dataType>string</dataType>
        </stateVariable>
        <stateVariable sendEvents="yes">
          <name>Metatext</name>
          <dataType>string</dataType>
        </stateVariable>
   </serviceStateTable>
</scpd>
```
{% endraw %}
