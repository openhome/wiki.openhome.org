---
title: "Av::OhMetadata"
permalink: "/wiki/Av::OhMetadata"
redirect_from:
---

{% raw %}
# <span id="OpenHome_Metadata_Format"></span>OpenHome Metadata Format

OpenHome Metadata format describes metadata for an audio track as a series of key-value pairs.

The list of supported keys, their mapping into DIDL-Lite and the number of instances that may be used are listed below:

<table>
<thead>
<tr>
<th><p><strong>Key</strong></p></th>
<th><p><strong>DIDL-Lite mapping</strong></p></th>
<th><p><strong>Instances</strong></p></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>uri</p></td>
<td><p>res</p></td>
<td><p>1</p></td>
</tr>
<tr>
<td><p>id</p></td>
<td><p>@id in item</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>type</p></td>
<td><ul>
<li>track -&gt; object.item.audioItem.musicTrack</li>
</ul></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>provider</p></td>
<td><p>oh:provider</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>title</p></td>
<td><p>dc:title</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>artwork</p></td>
<td><p>oh:artwork</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>artist</p></td>
<td><p>upnp:artist</p></td>
<td><p>[0..n]</p></td>
</tr>
<tr>
<td><p>composer</p></td>
<td><p>upnp:artist @role=composer</p></td>
<td><p>[0..n]</p></td>
</tr>
<tr>
<td><p>conductor</p></td>
<td><p>upnp:artist @role=conductor</p></td>
<td><p>[0..n]</p></td>
</tr>
<tr>
<td><p>genre</p></td>
<td><p>upnp:genre</p></td>
<td><p>[0..n]</p></td>
</tr>
<tr>
<td><p>albumTitle</p></td>
<td><p>upnp:album</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>albumArtwork</p></td>
<td><p>upnp:albumArtURI</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>albumArtist</p></td>
<td><p>upnp:artist @role=AlbumArtist</p></td>
<td><p>[0..n]</p></td>
</tr>
<tr>
<td><p>albumGenre</p></td>
<td><p>upnp:genre</p></td>
<td><p>[0..n]</p></td>
</tr>
<tr>
<td><p>year</p></td>
<td><p>dc:date</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>disc</p></td>
<td><p>oh:originalDiscNumber</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>discs</p></td>
<td><p>oh:originalDiscCount</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>track</p></td>
<td><p>upnp:originalTrackNumber</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>tracks</p></td>
<td><p>oh:originalTrackCount</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>channels</p></td>
<td><p>res @nrAudioChannels</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>bitDepth</p></td>
<td><p>res @bitsPerSample</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>sampleRate</p></td>
<td><p>res @sampleFrequency</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>bitRate</p></td>
<td><p>res @bitrate (integer / string of digits)</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>duration</p></td>
<td><p>res @duration (seconds - string of digits, zero = live/eternal)</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>mimeType</p></td>
<td><p>res @protocolInfo</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>work</p></td>
<td><p>oh:work</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>movement</p></td>
<td><p>oh:movement</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>show</p></td>
<td><p>oh:show</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>episode</p></td>
<td><p>oh:episodeNumber</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>episodes</p></td>
<td><p>oh:episodeCount</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>author</p></td>
<td><p>dc:author</p></td>
<td><p>[0..n]</p></td>
</tr>
<tr>
<td><p>narrator</p></td>
<td><p>upnp:artist @role=narrator</p></td>
<td><p>[0..n]</p></td>
</tr>
<tr>
<td><p>performer</p></td>
<td><p>upnp:artist @role=performer</p></td>
<td><p>[0..n]</p></td>
</tr>
<tr>
<td><p>publisher</p></td>
<td><p>dc:publisher</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>published</p></td>
<td><p>oh:published (ISO 8601)</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>website</p></td>
<td><p>oh:website</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>location</p></td>
<td><p>oh:location (ISO 6709)</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>details</p></td>
<td><p>oh:details</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>description</p></td>
<td><p>dc:description</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>rating</p></td>
<td><p>upnp:rating</p></td>
<td><p>[0..1]</p></td>
</tr>
<tr>
<td><p>extensions</p></td>
<td><p>oh:extensions</p></td>
<td><p>[0..1]</p></td>
</tr>
</tbody>
</table>
{% endraw %}
