---
title: "Av:Developer:Eriskay:StreamingServices"
permalink: "/wiki/Av:Developer:Eriskay:StreamingServices"
redirect_from:
---

{% raw %}
# <span id="Streaming_Services"></span>Streaming Services

## <span id="TIDAL"></span>TIDAL

Tidal's API is private. See Tidal for access to it. Or speak to us for help if you think that your access to the API would benefit OpenHome.

Assuming access to Tidal's API, the [ Credentials](/wiki/Av:Developer:Eriskay:CredentialsService) service can be used to retrieve the following information:

- The `Ids` property variable includes `tidalhifi.com` if Tidal is supported.
- `Data` from `Get` is JSON and contains at least the following fields:

<tt>

`   {`  
`       "country_code": "Tidal country code",`  
`       "user_id": "Tidal user identifier"`  
`       .....`  
`   }`

</tt>

- `Status` from `Get` is blank if `Username` and `Password` are both either blank or set and valid. If `Status` is not blank, it contains either JSON returned from a Tidal API or an error string.
- The token returned from `Login` and `Relogin` is JSON and contains at least the following fields:

<tt>

`   {`  
`       "session_id": "Tidal session id"`  
`       .....`  
`   }`

</tt>

- Tracks can be added to the [ Playlist](/wiki/Av:Developer:Eriskay:PlaylistService) service with urls in the form

<tt>

`   tidal://track?version=1&trackId=[tidal_track_id]`

</tt>

## <span id="Qobuz"></span>Qobuz

Qobuz's [developer API](https://github.com/Qobuz/api-documentation) is published on github.

The [ Credentials](/wiki/Av:Developer:Eriskay:CredentialsService) service can be used to retrieve the following information:

- The `Ids` state variable includes `qobuz.com` if Qobuz is supported.
- `Data` from `Get` is JSON and contains at least the following fields:

<tt>

`   {`  
`       "app_id": "qobuz app id"`  
`       .....`  
`   }`

</tt>

- `Status` from `Get` is blank if `Username` and `Password` are both either blank or set and valid. If `Status` is not blank, it contains either JSON returned from a Qobuz API or an error string.
- The token returned from `Login` and `Relogin` is JSON and contains at least the `user_auth_token` required by some Qobuz calls.

<tt>

`   {`  
`       "user_auth_token": "[token from qobuz]"`  
`       .....`  
`   }`

</tt>

Some Qobuz APIs require an `app_secret` argument. These APIs should not need to be called from control points. Qobuz's standard development agreement prohibits this being shared between device and control point.

Tracks can be added to the [ Playlist](/wiki/Av:Developer:Eriskay:PlaylistService) service with urls in the form <tt>

`   qobuz://track?version=2&trackId=[qobuz_track_id]`

</tt>
{% endraw %}
