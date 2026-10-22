---
title: "Av:Developer:Eriskay:DavaarChanges"
permalink: "/wiki/Av:Developer:Eriskay:DavaarChanges"
redirect_from:
---

{% raw %}
# <span id="Changes_between_Davaar_and_Eriskay"></span>Changes between Davaar and Eriskay

This page outlines the API changes between Davaar and Eriskay.

## <span id="Device"></span>Device

New service.

Control points use this service to determine whether a device is using compatible software. The presence of some services below can be inferred from this service.

## <span id="Product"></span>Product

Still the entrypoint for Topology algorithm. Control points no longer need to search for this – its presence can be inferred by checking for the `openhome.org.product` attribute in the versions section of the [ Device](/wiki/Av:Developer:Eriskay:DeviceService) description.

The following actions / properties have changed:

- `SourceXml` is now `SourceArray` and is formatted as JSON
- Similarly, `SourceXmlChangeCount` is now `SourceArrayChangeCount`
- `ProductName` and `ProductRoom` are now simply `Name` and `Room`
- The `Product` action is now `Names`
- `SetSourceIndexByName` and `SetSourceIndex` have been replaced by `SetSource`
- `SourceIndex` has been replaced by `SourceSystemName`

The following actions / properties have been (re)moved:

- `SourceCount` and `SourceIndex` have been removed. Use the `SetSource` action and `SourceSystemName` property instead.
- The `Source` action has been removed. Use `SourceArray`, parsing the JSON returned, to get information about a single source.
- `Standby` has been removed and is now available via the [ Device](/wiki/Av:Developer:Eriskay:DeviceService) service.
- The various `Manufacturer` properties and `Manufacturer` action have been removed and are now available via the [ Device](/wiki/Av:Developer:Eriskay:DeviceService) service.
- The various `Model` properties and `Model` action have been removed and are now available via the [ Device](/wiki/Av:Developer:Eriskay:DeviceService) service.
- The `ProductInfo`, `ProductUri`, `ProductImageUri` properties have been removed and are no longer returned by the `Product` action. These can now be read via the [ Device](/wiki/Av:Developer:Eriskay:DeviceService) service.
- `SetSourceIndexByName` has been removed.

The following actions / properties have been added:

- `Home` provides an identifier for a group of rooms. Traditional control points do not need to use this.

## <span id="Info"></span>Info

Removed. Use the [ Transport](/wiki/Av:Developer:Eriskay:TransportService) service instead.

## <span id="Transport"></span>Transport

New service.

Replaces Info service plus transport commands (`Play`, `Pause`, `Stop`, `Next`, `Prev`, `SeekSecondsAbsolute` and `SeekSecondsRelative`) from source-specific services.

## <span id="Time"></span>Time

No Changes

## <span id="Volume"></span>Volume

Removed the `VolumeMilliDbPerStep` property. Control points which set volume as an absolute decibel level are no longer supported.

One new property – `UnityGain` – which reports whether the current channel is already volume controlled.

## <span id="Credentials"></span>Credentials

`ReLogin` action renamed `Relogin`.

Tokens and data returned for Tidal and Qobuz streaming services are now JSON arrays to allow for additional information to be communicated in future.

## <span id="Sender"></span>Sender

`Attributes` and `PresentationUrl` properties / getters have been removed. These can be published as attributes via the [ Device](/wiki/Av:Developer:Eriskay:DeviceService) service if required.

`Metadata` format has changed from DIDL-Lite to OpenHome Metadata.

Updated list of allowed values for `Status` property (no change in behaviour – Davaar docs were incorrect).

## <span id="Configuration"></span>Configuration

New service.

Developer aid that may be useful from test programs but should not be used in production code.

## <span id="Playlist"></span>Playlist

The following actions have been removed. Use equivalents in [ Transport](/wiki/Av:Developer:Eriskay:TransportService) service instead:

- `Play` / `Pause` / `Stop`
- `Next` / `Prev`
- `SeekSecondsAbsolute` / `SeekSecondsRelative`
- `TransportState`

`Read` and `DeleteId` have been removed. Use `ReadList` and `DeleteList` instead.

`Metadata` passed to `Insert` is expected to now be in OpenHome Metadata format. Whatever format is passed in will be returned from both `Read` and `ReadList`.

The following actions have been added:

- `Move`, which simplifies playlist editing
- `DeleteList`, which simplifies bulk deletion (e.g. an entire album).

The `IdArray` property now has string type and contains a JSON integer array.

The `SeekId` and `SeekIndex` actions have been removed. Equivalent functionality is available via  
`Transport.PlayAs("playlist", "id=[track_id]")`  
or  
`Transport.PlayAs("playlist", "index=[track_index]")`

The `ProtocolInfo` property / getter has been removed. Control points are recommended to just queue any audio content with a player. Any that still want to check audio capabilities can do so via `AVTransport`.

## <span id="Radio"></span>Radio

The following actions have been removed. Use equivalents in [ Transport](/wiki/Av:Developer:Eriskay:TransportService) service instead: U `Play` / `Pause` / `Stop` U `SeekSecondsAbsolute` / `SeekSecondsRelative` U `TransportState`

`Next` / `Prev` are now supported via the [ Transport](/wiki/Av:Developer:Eriskay:TransportService) service

`Metadata` (for the current track and from `Read` / `ReadList`) is now in OpenHome Metadata format

The `IdArray` property now has string type and contains a JSON integer array.

The `SetId` and `SetChannel` actions have been removed. Equivalent functionality is available via  
`Transport.PlayAs("radio", "id=[preset_id]")`  
or  
`Transport.PlayAs("single", "{"url": "[track_url]", "metadata": "{track_metadata]"}")`

The `ProtocolInfo` property / getter has been removed. Control points are recommended to just queue any audio content with a player. Any that still want to check audio capabilities can do so via `AVTransport`.

## <span id="Receiver"></span>Receiver

The `TransportState` property and getter have been removed. Use equivalents in [ Transport](/wiki/Av:Developer:Eriskay:TransportService) service instead.

The `ProtocolInfo` property / getter is now a space-separated list of protocols.

The `SetSender` action has been removed. Equivalent functionality is available via  
`Transport.PlayAs("receiver", "{"url": "[sender_url]", "metadata": "[openhome_sender_metadata]"}")`

## <span id="Exakt"></span>Exakt

Service has been moved to the `linn.co.uk` domain.

There are no guarantees about compatibility so use by third parties is not encouraged.

## <span id="NetworkMonitor"></span>NetworkMonitor

Service has been moved to the `linn.co.uk` domain.

There are no guarantees about compatibility so use by third parties is not encouraged.

## <span id="PlaylistManager"></span>PlaylistManager

Service has been withdrawn.

There is no support for shared playlists in Eriskay media servers.

Equivalent functionality may be supported by a cloud service in future.
{% endraw %}
