---
title: "Av:Developer:VolumeService"
permalink: "/wiki/Av:Developer:VolumeService"
redirect_from:
  - "/wiki/Developer:VolumeService"
---

{% raw %}
# <span id="Architecture_Overview"></span>Architecture Overview

The Volume Service provides a means of controlling various settings which affect the product's volume (signal amplitude) measured at the output channels. A product may have one or more output channels. Balance or Fade settings may result in different volumes at each output. In the Mute state, all output channels are reduced to zero volume.

## <span id="Volume"></span>Volume

Volume is an adjustable setting that controls the loudness of the audio at the output channels of the product. Volume can be set to an absolute value or incremented/decremented in single steps. The maximum Volume setting is defined by the current value of **VolumeLimit**. The minimum Volume setting is zero. If an attempt is made to set the Volume above VolumeLimit, the Volume will be set to the **VolumLimit**. If an attempt is made to set the Volume above **VolumeMax**, an error will be reported.

## <span id="Volume_Limit"></span>Volume Limit

VolumeLimit specifies the upper limit of the Volume. Any attempt to set Volume above the VolumeLimit will reset Volume to the value of VolumeLimit. If VolumeLimit is changed, Volume is checked and automatically reduced if necessary. The maximum VolumeLimit setting is defined by the **VolumeMax** Characteristic.

## <span id="Balance"></span>Balance

Balance is an adjustable setting that specifies the **bias** in volume between the **left and right** output channels of the product. Balance can be set to an absolute value or incremented/decremented in single steps. The maximum Balance setting is defined by the **BalanceMax** Characteristic. The minimum Balance setting is defined by (**-BalanceMax**).

A setting of zero results in neutral balance (i.e. no bias applied) between left and right output channels. Negative values amplify left and attenuate right output channels. Conversely, positive values attenuate left and amplify right output channels. Increasing absolute values result in progressively larger amplification/attenuation being applied to output channels in this asymmetric manner. At or near the maximum settings, the attenuated channels may ended up being effectively reduced to volume zero.

## <span id="Fade"></span>Fade

Fade is an adjustable setting that specifies the **bias** in volume between the **front and rear** output channels of the products. Fade can be set to an absolute value or incremented/decremented in single steps. The maximum Fade setting is defined by the **FadeMax** Characteristic. The minimum Fade setting is defined by (**-FadeMax**) .

## <span id="Mute"></span>Mute

Mute is an adjustable state that determines if the output channels of the product are muted or not. When muted, all output channels of the product are silent.

## <span id="Characteristics"></span>Characteristics

Each product has six read-only values that define value ranges and their granularity -- as well as notable values within these ranges -- for volume, balance, and fade.

#### <span id="VolumeMax"></span>VolumeMax

VolumeMax defines the absolute maximum Volume setting.

#### <span id="VolumeUnity"></span>VolumeUnity

VolumeUnity defines the value of Volume that will result in unity system gain (i.e. *output amplitude* = *input amplitude*).

#### <span id="VolumeSteps"></span>VolumeSteps

VolumeSteps defines the number of step increments required to increase the Volume from zero to VolumeMax.

#### <span id="VolumeMilliDbPerStep"></span>VolumeMilliDbPerStep

VolumeMilliDbPerStep defines the size of each volume step in **binary milli decibels** (mibi dB). \[*1024mibi dB = 1dB*\]

#### <span id="BalanceMax"></span>BalanceMax

BalanceMax defines the maximum Balance setting. The minimum Balance setting is (-BalanceMax).

#### <span id="FadeMax"></span>FadeMax

FadeMax defines the maximum Fade setting. The minimum Fade setting is (-FadeMax).

# <span id="Actions"></span>Actions

### <span id="Volume_2"></span>Volume

The Volume action reports the current Volume setting.

### <span id="SetVolume"></span>SetVolume

The SetVolume action provides a means of setting the Volume to an absolute value.

### <span id="Volume_Inc"></span>Volume Inc

The VolumeInc action provides a means of increasing the Volume by 1.

### <span id="Volume_Dec"></span>Volume Dec

The VolumeDec action provides a means of decreasing the Volume by 1.

### <span id="VolumeLimit"></span>VolumeLimit

The VolumeLimit action reports the current VolumeLimit setting.

### <span id="Balance_2"></span>Balance

The Balance action reports the current Balance setting.

### <span id="SetBalance"></span>SetBalance

The SetBalance action provides a means of setting the Balance to a specific value.

### <span id="BalanceInc"></span>BalanceInc

The BalanceInc action provides a means of increasing the Balance by 1.

### <span id="BalanceDec"></span>BalanceDec

The BalanceDec action provides a means of decreasing the Balance by 1.

### <span id="Fade_2"></span>Fade

The Fade action reports the current Fade setting of the product.

### <span id="SetFade"></span>SetFade

The SetFade action provides a means of setting the Fade to a specific value.

### <span id="FadeInc"></span>FadeInc

The FadeInc action provides a means of increasing the Fade by 1.

### <span id="FadeDec"></span>FadeDec

The FadeDec action provides a means of decreasing the Fade by 1.

### <span id="Mute_2"></span>Mute

The Mute action reports the current Mute state of the product.

### <span id="SetMute"></span>SetMute

The SetMute action provides a means of setting the Mute state.

### <span id="Characteristics_2"></span>Characteristics

The Characteristics action returns all six characteristic values of the product.

# <span id="State_Variables"></span>State Variables

## <span id="Volume_3"></span>Volume

the current user volume setting, i.e. an integer value in the range \[0..VolumeLimit\]

## <span id="Mute_3"></span>Mute

the boolean setting indicating whether all output channels are currently forced to zero volume

## <span id="Balance_3"></span>Balance

the current setting of bias between left and right output channels, i.e. an integer value in the range \[-BalanceMax..+BalanceMax\]

## <span id="Fade_3"></span>Fade

the current setting of bias between front and back output channels, i.e. an integer value in the range \[-FadeMax..+FadeMax\]

## <span id="VolumeLimit_2"></span>VolumeLimit

the user-imposed (soft) maximum volume setting, i.e. an integer in the range \[0..VolumeMax\]; read-only

## <span id="VolumeMax_2"></span>VolumeMax

the system-imposed (hard) maximum volume setting; read-only

## <span id="VolumeUnity_2"></span>VolumeUnity

the system-specific volume setting that results in the input signal amplitude equalling the output signal amplitude (0dB gain), i.e. an integer in the range \[0..VolumeMax\]; read-only

## <span id="VolumeSteps_2"></span>VolumeSteps

the system-specific number of user-visible volume steps that would increase the volume from zero to VolumeMax; read-only

## <span id="VolumeMilliDbPerStep_2"></span>VolumeMilliDbPerStep

the system-specific gain increase with each volume step in binary milli decibel (mibi dB); read-only

## <span id="BalanceMax_2"></span>BalanceMax

the system-specific balance value that leads to maximum bias towards the right between output channels; read-only

## <span id="FadeMax_2"></span>FadeMax

the system-specific fade value that leads to maximum bias towards the rear between output channels; read-only

# <span id="Technical_Details"></span>Technical Details

        Domain  : av.openhome.org
        Name    : Volume
        Version : 1

## <span id="Volume_Service_Description_.28XML.29"></span>Volume Service Description (XML)

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
                    <name>VolumeMilliDbPerStep</name>
                    <direction>out</direction>
                    <relatedStateVariable>VolumeMilliDbPerStep</relatedStateVariable>
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
         <name>VolumeMilliDbPerStep</name>
         <dataType>ui4</dataType>
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
