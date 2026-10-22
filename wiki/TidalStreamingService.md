---
title: "TidalStreamingService"
permalink: "/wiki/TidalStreamingService"
redirect_from:
---

{% raw %}
Tidal's API is private. See Tidal for access to it. Or speak to us for help if you think that your access to the API would benefit OpenHome.

Assuming access to Tidal's API, the [ Credentials](/wiki/Av:Developer:CredentialsService) service can be used to retrieve the following information:

- The `Ids` state variable includes `tidalhifi.com` if Tidal is supported.
- `Data` from `Get` contains the country code used for many Tidal API calls.
- `Status` from `Get` is blank if Username and Password are both either blank or set and valid. If `Status` is not blank, it contains either json returned from a Tidal API or an error string.
- The token returned from `Login` and `ReLogin` is a Tidal session id.

Tracks can be added to the [ Playlist](/wiki/Av:Developer:PlaylistService) service with urls in the form  
`tidal://track?version=1&trackId=[insert_tidal_track_id]`
{% endraw %}
