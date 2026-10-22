---
title: "Av:Developer:Eriskay:VolumeService"
permalink: "/wiki/Av:Developer:Eriskay:VolumeService"
redirect_from:
---

{% raw %}
# <span id="Volume_Service"></span>Volume Service

## <span id="Overview"></span>Overview

The Volume service provides a means of controlling various settings which affect the product's volume (signal amplitude) measured at the output channels. A product may have one or more output channels. Balance or Fade settings may result in different volumes at each output. In the Mute state, all output channels are reduced to zero volume.

If a device's [ Product](/wiki/Av:Developer:Eriskay:ProductService) service reports an attribute `"Volume"`, then that device is guaranteed to bear the Volume service. If the Volume service is available, all its properties and actions must be fully implemented.

`Volume` is an adjustable setting that controls the loudness of the audio at the output channels of the product. It can be set to an absolute value or incremented/decremented in single steps of integrator-defined size. The maximum `Volume` setting is defined by the current value of `VolumeLimit`. The minimum Volume setting is always zero.

`Balance` is an adjustable setting that specifies the bias in volume between left and right output channels. A setting of zero results in neutral balance (i.e. no bias applied) between left and right output channels. Negative values amplify left and attenuate right output channels. Conversely, positive values attenuate left and amplify right output channels. Increasing absolute values result in progressively larger amplification/attenuation being applied to output channels in this asymmetric manner. At or near the maximum settings, the attenuated channels may ended up being effectively reduced to volume zero.

`Fade` is an adjustable setting that specifies the bias in volume between the front and rear output channels.

## <span id="Evented_Properties"></span>Evented Properties

### <span id="Volume"></span>Volume

The current user volume setting, i.e. an integer value in the range `[0..VolumeLimit]`.

### <span id="Mute"></span>Mute

A boolean setting indicating whether all output channels are currently forced to zero volume.

Note that (un)muting a product has no effect on its `TransportState` or it's ability to send audio to other rooms.

### <span id="VolumeLimit"></span>VolumeLimit

User-imposed (soft) maximum volume setting. Must be in the range `[0..VolumeMax]`; other values will be ignored.

### <span id="VolumeMax"></span>VolumeMax

System-imposed (hard) maximum volume setting. Must be exactly divisible by `VolumeSteps`.

### <span id="VolumeUnity"></span>VolumeUnity

System-specific volume setting that results in the input signal amplitude equalling the output signal amplitude (0dB gain), i.e. an integer in the range `[0..VolumeMax]`.

Values in the range `[0..VolumeUnity)` will be attenuated. Values in the range `(VolumeUnity..VolumeLimit]` will be amplified.

### <span id="VolumeSteps"></span>VolumeSteps

System-specific number of user-visible volume steps that would increase the volume from zero to `VolumeMax`.

### <span id="UnityGain"></span>UnityGain

`true` if the active source as reported by the \["ProductServiceEriskay" Product\] service is already volume controlled; `false` otherwise.

Changes to `Volume` will be accepted while `UnityGain` is enabled but will have no immediate effect.

### <span id="Balance"></span>Balance

Current setting of bias between left and right output channels, i.e. an integer value in the range `[-BalanceMax..+BalanceMax]`.

Negative values amplify left and attenuate right output channels. Conversely, positive values attenuate left and amplify right output channels.

A value of zero specifies no bias.

### <span id="BalanceMax"></span>BalanceMax

System-specific balance value for maximum bias between left and right channels.

### <span id="Fade"></span>Fade

Current setting of bias between front and back output channels, i.e. an integer value in the range `[-FadeMax..+FadeMax]`.

A value of zero specifies no bias.

### <span id="FadeMax"></span>FadeMax

System-specific fade value for maximum bias between front and rear between channels.

## <span id="Actions"></span>Actions

### <span id="Characteristics"></span>Characteristics

`Arguments: (out uint volMax, out uint volUnity, out uint volSteps, out uint balanceMax, out uint fadeMax)`  
Return the values of the system-specified properties which do not change at run-time - `VolumeMax`, `VolumeUnity`, `VolumeSteps`, `BalanceMax` and `FadeMax`.

### <span id="Volume_2"></span>Volume

`Arguments: (out uint volume)`  
Return the current value of the `Volume` property.

### <span id="SetVolume"></span>SetVolume

`Arguments: (in uint volume)`  
Set the `Volume` property to an absolute value.

Any attempt to set a value above the `VolumeLimit` must reset `Volume` to `VolumeLimit`.

### <span id="VolumeInc"></span>VolumeInc

`Arguments: None`  
Increase `Volume` by `VolumeMax / VolumeSteps`.

### <span id="Volume_Dec"></span>Volume Dec

`Arguments: None`  
Decrease `Volume` by `VolumeMax / VolumeSteps`.

### <span id="VolumeLimit_2"></span>VolumeLimit

`Arguments: (out uint limit)`  
Return the value of the `VolumeLimit` property.

### <span id="UnityGain_2"></span>UnityGain

`Arguments: (out uint unityGain)`  
Return the value of the `UnityGain` property.

### <span id="Balance_2"></span>Balance

`Arguments: (out int balance)`  
Return the value of the `Balance` property.

### <span id="SetBalance"></span>SetBalance

`Arguments: (in int balance)`  
Set the `Balance` property to an absolute value.

### <span id="BalanceInc"></span>BalanceInc

`Arguments: None`  
Increase `Balance` by `1`.

### <span id="BalanceDec"></span>BalanceDec

`Arguments: None`  
Decrease `Balance` by `1`.

### <span id="Fade_2"></span>Fade

`Arguments: (out int fade)`  
Return the value of the `Fade` property.

### <span id="SetFade"></span>SetFade

`Arguments: (in int fade)`  
Set the `Fade` property to an absolute value.

### <span id="FadeInc"></span>FadeInc

`Arguments: None`  
Increase `Fade` by `1`.

### <span id="FadeDec"></span>FadeDec

`Arguments: None`  
Decrease `Fade` by `1`.

### <span id="Mute_2"></span>Mute

`Arguments: (out bool mute)`  
Return the value of the `Mute` property.

### <span id="SetMute.28in_bool_mute.29"></span>SetMute(in bool mute)

`Arguments: (in bool mute)`  
Set the `Mute` property.

## <span id="UPnP_Service_Description"></span>UPnP Service Description

For devices supporting the UPnP protocol, the service description is

`name: "Volume"`  
`domain: "openhome.org.eriskay"`  
`version: "1"`

``` xml
<?xml version="1.0" encoding="utf-8"?>
<scpd xmlns="urn:schemas-upnp-org:service-1-0">
  <specVersion>
    <major>1</major>
    <minor>0</minor>
  </specVersion>
  <actionList>
    <action>
      <name>Characteristics</name>
      <argumentList>
        <argument>
          <name>VolumeMax</name>
          <direction>out</direction>
          <relatedStateVariable>VolumeMax</relatedStateVariable>
        </argument>
        <argument>
          <name>VolumeUnity</name>
          <direction>out</direction>
          <relatedStateVariable>VolumeUnity</relatedStateVariable>
        </argument>
        <argument>
          <name>VolumeSteps</name>
          <direction>out</direction>
          <relatedStateVariable>VolumeSteps</relatedStateVariable>
        </argument>
        <argument>
          <name>BalanceMax</name>
          <direction>out</direction>
          <relatedStateVariable>BalanceMax</relatedStateVariable>
        </argument>
        <argument>
          <name>FadeMax</name>
          <direction>out</direction>
          <relatedStateVariable>FadeMax</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SetVolume</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>in</direction>
          <relatedStateVariable>Volume</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>VolumeInc</name>
    </action>
    <action>
      <name>VolumeDec</name>
    </action>
    <action>
      <name>Volume</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>Volume</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SetBalance</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>in</direction>
          <relatedStateVariable>Balance</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>BalanceInc</name>
    </action>
    <action>
      <name>BalanceDec</name>
    </action>
    <action>
      <name>Balance</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>Balance</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SetFade</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>in</direction>
          <relatedStateVariable>Fade</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>FadeInc</name>
    </action>
    <action>
      <name>FadeDec</name>
    </action>
    <action>
      <name>Fade</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>Fade</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>SetMute</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>in</direction>
          <relatedStateVariable>Mute</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>Mute</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>Mute</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>VolumeLimit</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>VolumeLimit</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
    <action>
      <name>UnityGain</name>
      <argumentList>
        <argument>
          <name>Value</name>
          <direction>out</direction>
          <relatedStateVariable>UnityGain</relatedStateVariable>
        </argument>
      </argumentList>
    </action>
  </actionList>
  <serviceStateTable>
    <stateVariable sendEvents="yes">
      <name>Volume</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Mute</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Balance</name>
      <dataType>i4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>Fade</name>
      <dataType>i4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>VolumeLimit</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>VolumeMax</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>VolumeUnity</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>VolumeSteps</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>UnityGain</name>
      <dataType>boolean</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>BalanceMax</name>
      <dataType>ui4</dataType>
    </stateVariable>
    <stateVariable sendEvents="yes">
      <name>FadeMax</name>
      <dataType>ui4</dataType>
    </stateVariable>
  </serviceStateTable>
</scpd>
```
{% endraw %}
