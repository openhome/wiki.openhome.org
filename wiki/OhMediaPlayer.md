---
title: "OhMediaPlayer"
permalink: "/wiki/OhMediaPlayer"
redirect_from:
---

{% raw %}
# <span id="ohMediaPlayer"></span>ohMediaPlayer

ohMediaPlayer is a portable software version of the ohMedia and UPnP:AV network services. It is written in C++ and can be deployed to any desktop or mobile platform and many embedded platforms. Its headline features include

- Support for all popular digital formats
  - …including FLAC, MP3, ALAC, WAV, AAC, Vorbis, WMA
  - …for both 44.1kHz and 48kHz family sample rates
  - …supported sample rates from 7.35kHz to 192kHz
  - …at 8/16/24 bit depths
  - …in 1-8 channels
- Playlist source. Store a playlist of hundreds or even thousands of tracks on device, playing these without requiring further interaction from a control point.
- Songcast.
  - Sender. Share your audio stream with an unlimited number of other players
  - Receiver. Listen to the same audio stream as another device, in exact synchronisation with that device and all other receivers.
  - Supports all audio resolutions, up to and including 24-bit / 192kHz
  - "Clock pulling" architecture guarantees that playback starts then remains synchronised between all devices
- Radio. Supports internet radio stations, podcasts and listen again. Includes integration to the popular TuneIn service, allowing users to setup personalised presets from a list of all worldwide internet stations.
- UPnP:AV. Presents the standard UPnP Media Renderer network services for use with basic control points.
- Playback of popular analogue and digital inputs - HDMI, SPDIF, TOS, Analogue, etc.
- Airplay. Receive an audio stream via Apple’s Airplay protocol.

# <span id="Architecture_Overview"></span>Architecture Overview

<figure>
<img src="/mediawiki/images/8/83/MediaPlayer-Integrators.png" title="MediaPlayer-Integrators.png" alt="MediaPlayer-Integrators.png" />
<figcaption aria-hidden="true">MediaPlayer-Integrators.png</figcaption>
</figure>

# <span id="System_Requirements"></span>System Requirements

RAM: 16MB standard; 4MB possible

ROM: 8MB standard; 2.5MB possible (if Radio and Airplay sources are omitted)

# <span id="Integration"></span>Integration

The integrator supplies a small number of components

- Driver. This pulls decoded audio samples from ohMediaPlayer’s audio pipeline and is responsible for feeding them into the host’s audio hardware at the appropriate rate.
- Mutes. Optionally mute audio hardware around changes in audio sample rate or bit depth.
- OS compatibility layer. Threading and socket abstractions. Many standard platforms are available with ohNet, including
  - Linux (x86, x64, ARM)
  - Windows (x86, x64)
  - Mac (x86, x64)
  - Embedded (using [FreeRTOS](http://www.freertos.org/) and [lwIP](http://lwip.wikia.com/wiki/LwIP_Wiki)). Big and little endian ports exist.
- R/W Store. At a minimum, this can simply provide a set of string literals that are determined at design time. If runtime user configuration is supported, this should also provide a means to persist and restore (string) key / (binary) value pairs.
- Application. This can be pretty short - \<100 lines of code - to cover
  - Initialise the UPnP stack
  - Create a UPnP device, adding manufacturer-specific attributes to it
  - Create MediaPlayer object
  - Add desired plug-ins to MediaPlayer object
    - Sources
    - Codecs
    - Protocols
    - Content Processors
    - (Note that a future release may reduce this to selection of sources, with each source enabling appropriate codecs, protocols, etc. automatically.)
  - Create Driver, R/W Store
  - Enable UPnP device

No further code is required. ohMediaPlayer is controlled via [ network APIs](/wiki/OhMediaDevelopers#Network_Services) which will be automatically advertised on the network, ready to be used by any number of controllers in parallel.

# <span id="Configuration"></span>Configuration

APIs are provided for design-time configuration

- Which audio ‘sources’ to include
- Which audio formats to support
- Sizes of various thread and memory pools

Additional software can be provided for run-time configuration, including

- Product name
- Username for externally provided radio presets
- Source naming + visibility to control app
- Delays to apply to different sources (e.g. for lip-sync)

This additional software includes

- On-device UPnP service
- On-device web UI to access these configuration values
- Desktop/mobile app to detect media players and display their configuration page.

# <span id="Software_Updates"></span>Software Updates

Deployments to open systems are assumed to use the host’s existing support for application deployment and update. A highly robust, well proved firmware update mechanism is available for embedded products. This includes

- Additional UPnP services to support reprogramming
- Desktop reprogramming utility
- Optionally, a desktop app which includes the reprogramming utility plus a user interface onto other device configuration options

This functionality is supplied separately from ohMediaPlayer and requires an additional 500KB ROM.

# <span id="Source_Code"></span>Source Code

ohMediaPlayer is provided in binary form (static library + header files) by default. Contact us if you want to discuss a license to access the full source code.  
Note that we use a small number of externally sourced, commercially licensed audio codecs. We could only share the source for these if you negotiate access to them directly with the copyright holders.
{% endraw %}
