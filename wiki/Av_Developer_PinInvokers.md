---
title: "Av:Developer:PinInvokers"
permalink: "/wiki/Av:Developer:PinInvokers"
redirect_from:
---

{% raw %}
# <span id="Overview"></span>Overview

All pins have a uri associated with them which is used by the pins service to interpret one or more playable items and must be in the following form:

\<mode\>`://`\<type\>`?`\<pin specific query parameters\>`&version`\<pin version\>

The `mode` indicates which music provider will provide the playable content. Each has a number of query parameters which are outlined below. The pins service allows you to query which modes the device currently supports.

The `type` describes what the pin is such as an artist, album or playlist.

The current pin version is `1`. The version has been omitted from the examples below.

# <span id=".28Linn.29_Kazoo_Server"></span>(Linn) Kazoo Server

|  |  |  |
|----|----|----|
| mode | openhome.me |  |
| type | album | Requires response type tracks |
|  | artist | Requires response type albums |
|  | playlist | Requires response type tracks |
|  | genre | Requires response type of either albums, playlists or tracks |
|  | container | Only supported in a list pin |
| *Query Parameters* |  |  |
| udn | Server's Udn |  |
| me | Endpoint Id |  |
| response | Response type | See above |
| browse | Item id | Performs a browse query with the given item id. Can't contain list parameter |
| list | Tag id | Performs a list query with given tag id. Can't contain a browse parameter |

Example Uris:

      // Browse pin
      openhome.me://[type]?udn=[device udn]&me=[endpoint id]&browse=[item id]&response=[response type]
      
      // List pin
      openhome.me://[type]?udn=[device udn]&me=[endpoint id]&list=[item id]&response[response type]

# <span id="Tidal"></span>Tidal

## <span id="Tracks"></span>Tracks

|                    |                |
|--------------------|----------------|
| mode               | tidal          |
| type               | track          |
| *Query Parameters* |                |
| trackId            | Tidal track id |

Example Uri:

      tidal://track?trackId=[id]

## <span id="Other_Tidal_Content"></span>Other Tidal Content

For other Tidal content the pin will provide a link to the Tidal API resource and a hint as to what you expect that resource to return.

|  |  |  |
|----|----|----|
| mode | tidal |  |
| type | album | Requires response type tracks |
|  | artist | Requires response type albums |
|  | playlist | Requires response type tracks |
|  | genre | Requires response type of either albums, playlists or tracks |
|  | container | Requires response type of either albums, playlists or tracks |
| *Query Parameters* |  |  |
| path | Tidal API link | Must to be url encoded |
| response | Response type | See above |

Example Uri:

      tidal://[type]?path=[api link]&response=[response type]

# <span id="Qobuz"></span>Qobuz

## <span id="Tracks_2"></span>Tracks

|                    |                |
|--------------------|----------------|
| mode               | qobuz          |
| type               | track          |
| *Query Parameters* |                |
| trackId            | Qobuz track id |

Example Uri:

      qobuz://track?trackId=[id]

## <span id="Other_Qobuz_Content"></span>Other Qobuz Content

For other Qobuz content the pin will provide a link to the Qobuz API resource and a hint as to what you expect that resource to return.

|  |  |  |
|----|----|----|
| mode | qobuz |  |
| type | album | Requires response type tracks |
|  | artist | Requires response type albums |
|  | playlist | Requires response type tracks |
|  | container | Requires response type of either albums, playlists |
| *Query Parameters* |  |  |
| path | Qobuz API link | Must to be url encoded |
| response | Response type | See above |
|  |  |  |

Example Uri:

      qobuz://[type]?path=[api link]&response=[response type]

# <span id="TuneIn"></span>TuneIn

## <span id="Stations"></span>Stations

A TuneIn station pin should play the station from the TuneIn link specified in the pin uri.  
Note that the pin's title and artwork uri will be presented as track metadata by the [ Info](/wiki/Av:Developer:InfoService) service.

|                    |                   |                        |
|--------------------|-------------------|------------------------|
| mode               | tunein            |                        |
| type               | stream            |                        |
| *Query Parameters* |                   |                        |
| path               | Radio stream link | Must to be url encoded |
|                    |                   |                        |

Example Uri:

      tunein://stream?path=[stream]

## <span id="Shows_.2F_Podcasts"></span>Shows / Podcasts

A TuneIn show/podcast pin should play the most recent episode as reported by the TuneIn link specified in the pin uri.

|                    |                   |                        |
|--------------------|-------------------|------------------------|
| mode               | tunein            | Latest episode         |
| mode               | tuneinlist        | All episodes           |
| type               | podcast           |                        |
| *Query Parameters* |                   |                        |
| path               | Show/podcast link | Must to be url encoded |
|                    |                   |                        |

Example Uri:

      tunein://podcast?path=[stream]
      tuneinlist://podcast?path=[stream]

# <span id="Radio_Preset"></span>Radio Preset

Play a radio preset by index:

      radio://preset?id=[index]

# <span id="iTunes_Podcast"></span>iTunes Podcast

Play either the latest episode from a podcast or load a playlist with the last N episodes

|                    |                   |                              |
|--------------------|-------------------|------------------------------|
| mode               | itunes            | Latest episode only          |
| mode               | ituneslist        | Load all of the episode list |
| type               | podcast           |                              |
| *Query Parameters* |                   |                              |
| id                 | iTunes podcast id |                              |
|                    |                   |                              |

      itunes://podcast?id=[identifier]
      ituneslist://podcast?id=[identifier]

# <span id="Sources"></span>Sources

A source pin should switch to the source matching the system name specified in the pin uri.

|                    |                                               |
|--------------------|-----------------------------------------------|
| mode               | transport                                     |
| type               | source                                        |
| *Query Parameters* |                                               |
| id                 | The system name of the source                 |
| udn                | Udn of the device to which the source belongs |
|                    |                                               |

Example Uri:

      transport://source?id=[system name]&udn=[device udn]

# <span id="CalmRadio"></span>CalmRadio

A CalmRadio pin should play the stream specified in the pin uri  
Note that the pin's title and artwork uri will be presented as track metadata by the [ Info](/wiki/Av:Developer:InfoService) service.

|                    |                   |                        |
|--------------------|-------------------|------------------------|
| mode               | calmradio         |                        |
| type               | stream            |                        |
| *Query Parameters* |                   |                        |
| path               | Radio stream link | Must to be url encoded |
|                    |                   |                        |

Example Uri:

      calmradio://stream?path=[stream]

# <span id="Url"></span>Url

Play a hard-coded url.  
Note that the pin's title and artwork uri will be presented as track metadata by the [ Info](/wiki/Av:Developer:InfoService) service.

      url://stream?path=[stream]
{% endraw %}
