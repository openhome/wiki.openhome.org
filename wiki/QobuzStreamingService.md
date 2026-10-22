---
title: "QobuzStreamingService"
permalink: "/wiki/QobuzStreamingService"
redirect_from:
---

{% raw %}
Qobuz's [developer API](https://github.com/Qobuz/api-documentation) is published on github.

The [ Credentials](/wiki/Av:Developer:CredentialsService) service can be used to retrieve the following information:

- The `Ids` state variable includes `qobuz.com` if Qobuz is supported.
- `Data` from `Get` contains the `app_id` used by many Qobuz API calls.
- `Status` from `Get` is blank if Username and Password are both either blank or set and valid. If `Status` is not blank, it contains either json returned from a Qobuz API or an error string.
- The token returned from `Login` and `ReLogin` is a Qobuz `user_auth_token`.

Some Qobuz APIs require an `app_secret` argument. These APIs should not need to be called from control points.

Tracks can be added to the [ Playlist](/wiki/Av:Developer:PlaylistService) service with urls in the form  
`qobuz://track?version=2&trackId=[insert_qobuz_track_id]`
{% endraw %}
