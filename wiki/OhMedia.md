---
title: "OhMedia"
permalink: "/wiki/OhMedia"
redirect_from:
---

{% raw %}
# <span id="What_is_ohMedia.3F"></span>What is ohMedia?

OpenHome Media (ohMedia) is an open standard for networked audio devices in the home. Devices can implement ohMedia in place of, or alongside of, the UPnP Forum’s AV standards. It offers a number of advantages over the UPnP Forum's AV standards.

- Easier to program against.
  - UPnP forum services have large numbers of optional features. While this makes it easy for device manufacturers to implement a service, it is hard to write control points and interoperability between devices becomes poor. ohMedia uses options sparingly, typically at a service level. This enables clear, consistent behaviour across devices from different manufacturers.
- Better support for playlists
  - Playlists are stored on the renderer, allowing playback to continue when the control point leaves the network (e.g. your tablet goes to sleep, runs out of battery, or leaves the wifi zone).
  - Multiple control points are supported. A second controller can discover and display a playlist setup by a different device. Edits to the playlist from either controller will be immediately reflected in the other.
  - Storing playlists on the renderer also allows for gapless playback, avoiding gaps between tracks that were intended to merge seamlessly. This is particularly important for live albums and classical music.
- Control the room, not just a device
  - ohMedia topology algorithms allow multi-box systems to be easily managed from a single control point application
- Easy to share music
  - The Songcast protocol allows an ohMedia renderer to share its content with any other ohMedia device or listen to content from another device. Synchronised audio can be played between any number of devices.
  - Desktop songcast applications plus mobile support (Songcast app for Android; Airplay receiver for iOS) allows content from many other devices to be shared.
- Richer set of audio sources
  - In addition to Playlist, Songcast and external digital and analogue inputs, internet radio and a receiver for Apple's AirPlay are also natively supported.

# <span id="Developers"></span>Developers

If you are interested in ohMedia development, [ further information is available](/wiki/OhMediaDevelopers)
{% endraw %}
