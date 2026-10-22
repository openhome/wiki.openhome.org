---
title: "Av:Developer:TransportPlayAsCommands"
permalink: "/wiki/Av:Developer:TransportPlayAsCommands"
redirect_from:
---

{% raw %}
# <span id="Transport_PlayAs_Options"></span>Transport PlayAs Options

The [ Transport](/wiki/Av:Developer:TransportService) service’s `PlayAs` action takes arguments for `mode` (source or group of related sources) and a mode-specific `command`. Some standard modes and commands are listed below; other manufacturer-specific options are possible.

### <span id="Playlist"></span>Playlist

The `"playlist"` mode supports the following commands:

- `id=[track_id]` - Halt playback of any current track and switch to the track with the specified id. Returns a `800` fault code if `[track_id]` is not valid.
- `index=[playlist_index]` - Halt playback of the current track and switch to the track with the specified index. Returns a `802` fault code if the index is beyond the end of the playlist.
- `track={"uri":"track_uri","metadata":"didl_lite"}` - load the specified track at the end of the current Playlist and play it next.

### <span id="Radio"></span>Radio

The `"radio"` mode supports the following command:

- `id=[preset_id]` – Start playing the specified preset. Returns a `800` fault code if `[preset_id]` does not match a current preset

The `"Radio-Single"` mode supports the following command:

- `track={"uri":"track_uri","metadata":"didl_lite"}` - load the specified track.
{% endraw %}
