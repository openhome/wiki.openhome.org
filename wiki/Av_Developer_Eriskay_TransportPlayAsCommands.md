---
title: "Av:Developer:Eriskay:TransportPlayAsCommands"
permalink: "/wiki/Av:Developer:Eriskay:TransportPlayAsCommands"
redirect_from:
---

{% raw %}
# <span id="Transport_PlayAs_Options"></span>Transport PlayAs Options

The [ Transport](/wiki/Av:Developer:Eriskay:TransportService) service’s `PlayAs` action takes arguments for `mode` (source or group of related sources) and a mode-specific `command`. Some standard modes and commands are listed below; other manufacturer-specific options are possible.

### <span id="Playlist"></span>Playlist

The `"playlist"` mode supports the following commands:

- `id=[track_id]` - Halt playback of any current track and switch to the track with the specified id. Returns a `800` fault code if `[track_id]` is not valid.
- `index=[playlist_index]` - Halt playback of the current track and switch to the track with the specified index. Returns a `802` fault code if the index is beyond the end of the playlist.

### <span id="Radio"></span>Radio

The `"radio"` mode supports the following command:

- `id=[preset_id]` – Start playing the specified preset. Returns a `800` fault code if `[preset_id]` does not match a current preset

### <span id="Receiver"></span>Receiver

The `"receiver"` mode supports the following command: <tt>

`   {`  
`       "url": "[sender_url]",`  
`       "metadata": "[openhome_sender_metadata]"`  
`   }`

</tt> and will start playing the same content as the device that either hosts the `ohu` or `ohm` sender or matches the zone in the `ohz` url.

### <span id="Single"></span>Single

The `"single"` mode supports the following command <tt>

`   {`  
`       "url": "[track_url]",`  
`       "metadata": "[openhome_metadata]"`  
`   }`

</tt> and will start playing `[track_url]`, reporting the specified metadata. When the track completes, it will be queued again then `TransportState` will change to `Stopped`.

### <span id="External"></span>External

The `"external"` mode supports the following command:

- `[system_name]` – activate the source with whose system name matches `[system_name]` and start playing.

### <span id="UpnpAv"></span>UpnpAv

The `"upnpav"` mode supports the following command:

- `[blank]` – Start playing the last uri set via `AVTransport.SetAVTransportUri`. Activates the source but leaves transport state as `STOPPED` if no uri is set.
{% endraw %}
