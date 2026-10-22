---
title: "CalmRadioInternetRadio"
permalink: "/wiki/CalmRadioInternetRadio"
redirect_from:
---

{% raw %}
Calm Radio's API is private. See Calm Radio for access to it. Or speak to us for help if you think that your access to the API would benefit OpenHome.

Assuming access to Calm Radio's API, the [ Credentials](/wiki/Av:Developer:CredentialsService) service can be used to retrieve the following information:

- The `Ids` state variable includes `calmradio.com` if Calm Radio is supported.
- `Data` from `Get` contains the json object returned from login (so includes both a login token and a note on membership level).
- `Status` from `Get` is blank if Username and Password are both either blank or set and valid. If `Status` is not blank, it contains either json returned from a Calm Radio API or an error string.
- The token returned from `Login` and `ReLogin` is a Calm Radio token. No streams can be played if this is empty.

Tracks can be added to either [ Playlist](/wiki/Av:Developer:PlaylistService) or [ Radio](/wiki/Av:Developer:RadioService) services with urls in the form  
`calmradio://stream?[url encoded full url to calm radio stream]`
{% endraw %}
