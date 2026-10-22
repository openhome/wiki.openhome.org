---
title: "OhWidget Driver Development"
permalink: "/wiki/OhWidget_Driver_Development"
redirect_from:
---

{% raw %}
# <span id="Introduction"></span>Introduction

This document is for developers using the OpenHome SDK to integrate a Widget into an OpenHome system. Each Widget must have its own driver to allow it to communicate with the OpenHome Nodes.

To help you write your driver, this document provides high level descriptions of the core responsibilities of a Widget driver and gives a detailed walk-through using example code.

Full versions of each file used in the development of the example driver are available in the Appendix.

## <span id="Prerequisites"></span>Prerequisites

To begin development of your Widget driver you must be in possession of the following items:

- your Widget Service XML that describes the properties on your Widget.

> **Note**
>
> This document does not contain advice on how to write Widget Service XML. Refer to the OpenHome Widget Service XML definition document for more details.

- the OpenHome SDK
- your chosen communication protocol's API

The protocol you choose for your Widgets must be the same protocol used on your choice of Node.

> **Note**
>
> This document focuses on the development of the Widget driver. Details about the communications protocol used are beyond the scope of this document. This document assumes you are familiar with your chosen protocol's code libraries and are able to use them in the driver code you write.

## <span id="Related_Documents"></span>Related Documents

The following related OpenHome documentation may be of interest to you:

- [ohWidget Technical Overview](/wiki/OhWidget_Technical_Overview)
- OpenHome Widget Service XML definition
- [OpenHome ohNet Device Stack](http://www.openhome.org/releases/ohNet_DeviceStack.pdf)

> **Note**
>
> None of the related documents listed above is mandatory reading for Widget driver development.

# <span id="Widget_Service_XML"></span>Widget Service XML

## <span id="Widget_Service_XML_2"></span>Widget Service XML

OpenHome Widget driver writing relies heavily on the use of code generated from a single source — the Widget Service XML.

The service and actions your Widget provides are represented in code in a file called a Provider. The Provider is automatically generated from the Widget Service XML and produces an abstract class for you to inherit when you write your concrete class driver.

To aid in the explanation of how the Provider is created and put to use we will follow the development of a driver for a simple light Widget; taking the defined Widget Service XML and stepping through how it is used to generate the other files. Examples of code are used throughout this document to show you how each one is created and used in an OpenHome system.

It is essential that you start with a well-formed Widget Service XML, conforming to the schema defined in the WidgetService.xsd. The following diagram shows the significance of the Widget Service XML in relation to the generated files you will use when writing your driver:

<figure>
<img src="/mediawiki/images/6/69/DriverDevDocHierarchy.png" title="Figure 1: The OpenHome document hierarchy, highlighting the areas specifically used in driver development" width="800" alt="DriverDevDocHierarchy.png" />
<figcaption>Figure 1: The OpenHome document hierarchy, highlighting the areas specifically used in driver development</figcaption>
</figure>

> **Note**
>
> - The grayed-out files are not relevant to Widget driver development but can also be generated from the Widget Service XML.
> - The Provider is generated in C#, meaning your driver must be written in C# as well. The use of managed code is mandatory for driver writing in the OpenHome framework.

## <span id="Code_sample_used_in_this_document"></span>Code sample used in this document

Our examples in this document use a Widget Service XML definition for a light Widget called BasicLight.xml.

> **Note**
>
> Full versions of all the example files used in this document are available in the Appendix.

We will see how the Provider is generated from this XML and how it is used to aid the driver writing process. The examples also show how your chosen communication protocol should be used in the body of the driver code.

Implementation details of specific protocols you choose to use are beyond the scope of this document. However, the samples used in this document show the use of the SimpleUPnP protocol to aid you in your development process.

The SimpleUPnP protocol was developed as a test protocol during the early stages of the OpenHome project. It is included in the OpenHome SDK and can be used as a public resource.

The use of SimpleUPnP in the example files and the code snippets within the following sections is highlighted by the ![Warning.png](/mediawiki/images/c/cb/Warning.png "Warning.png") icon. The lines of code marked by ![Warning.png](/mediawiki/images/c/cb/Warning.png "Warning.png") must be changed to code from your chosen communication protocol's library. SimpleUPnP is left in to help you understand how a protocol is used in a working example.

The sample code provided attempts to show best-practice coding standards. There are several sections of code that have a mandatory layout or that call specifically named methods and functions. These areas of the code are highlighted where required.

Where the examples do not explicitly state that the code shown is mandatory, you are free to implement it in a different way according to your own coding style and practices.

# <span id="Driver_responsibilities"></span>Driver responsibilities

## <span id="Driver_responsibilities_2"></span>Driver responsibilities

An OpenHome Widget driver has several responsibilities which must be met before it can be used on an OpenHome Node.

These responsibilities are listed R1 to R7 and are defined here, explaining what each one must do.

### <span id="R1_Specifying_the_type_of_Widget_the_driver_controls"></span>R1 Specifying the type of Widget the driver controls

A driver must know which type of Widget it can communicate with and be able to provide that information to the Discovery Module. A driver will normally communicate with one specific type of Widget and will only ever use one communications protocol.

### <span id="R2_Reacting_to_a_discovered_Widget_on_the_network"></span>R2 Reacting to a discovered Widget on the network

A driver must create a new IWidgetRegistryEntry object to represent the Widget and use it to listen to changes in the physical Widget's state.

### <span id="R3_Setting_the_initial_values_for_the_Widget.27s_properties"></span>R3 Setting the initial values for the Widget's properties

A driver must set the Widget object's initial properties.

### <span id="R4_Publishing_discovered_Widgets_in_the_Local_Widget_Registry_on_the_Node"></span>R4 Publishing discovered Widgets in the Local Widget Registry on the Node

Publishing Widgets advertises their presence on the network. This allows Nodes to access the Widgets and present their services for use. A driver must be able to enable and publish a Widget object.

### <span id="R5_Reacting_to_an_event_reported_from_the_Widget"></span>R5 Reacting to an event reported from the Widget

A driver must update the Node with the state of the Widget's properties when the Widget reports a change.

### <span id="R6_Reacting_to_actions_sent_to_the_Widget"></span>R6 Reacting to actions sent to the Widget

A driver must update a specified property to a new value when instructed to do so by the Node.

### <span id="R7_Reacting_to_a_Widget.27s_departure"></span>R7 Reacting to a Widget's departure

A driver must properly handle the IWidgetRegistryEntry object when the physical Widget is no longer available.

The sections of example code that follow show you how to write a driver from beginning to end. The accompanying text explaining the example code highlights when a responsibility, or part of a responsibility, has been met.

# <span id="Driver_Architecture"></span>Driver Architecture

## <span id="Driver_Architecture_2"></span>Driver Architecture

Drivers are installed on the Node and used when the Node needs to communicate with the Widget. Drivers use several objects to communicate with Widgets over the Widget's lifetime. Figure 2 shows the objects used by the driver and how the responsibilities listed above relate to each one:

<figure>
<img src="/mediawiki/images/3/3b/DriverNodeArchitecture.png" title="Figure 2: The architecture of a driver, showing the driver&#39;s relationship to the objects used to communicate with a Widget. Lines between objects show message flow." width="800" alt="DriverNodeArchitecture.png" />
<figcaption>Figure 2: The architecture of a driver, showing the driver's relationship to the objects used to communicate with a Widget. Lines between objects show message flow.</figcaption>
</figure>

The objects contained in the dotted boundary must appear in the code you write to define your driver. The Driver, Provider and IWidgetRegistryEntry objects are all contained in the same driver file. We begin discussing this on page 12.

The other objects are provided by the OpenHome SDK or as installed components on the Node.

The Discovery Module informs the driver of the presence of an available Widget.

Each Node has a Protocol Module which contains the protocol's API. Widgets can communicate with OpenHome Nodes using any one of the set of communications protocols the Node supports. The driver uses your chosen protocol's Protocol Module to communicate with the Widget.

Both the Protocol Module and the Discovery Module are installed on the Node. When you write your driver you will use your Protocol Module to allow the driver to communicate with the Widget.

IWidgetPublisher, IPublishedWidget and DvDevice are objects provided in the OpenHome API. You can read about them in the APIs.

# <span id="Generating_the_Provider"></span>Generating the Provider

## <span id="Generating_the_Provider_2"></span>Generating the Provider

You must generate your provider before you can begin writing your Widget driver. You use your provider as a guide to implement the functions your Widget needs to set the values of its properties.

The current provider generation process is a manual one involving the use of a text transform tool.

Speak to your OpenHome contact who will help you generate your provider.

Future releases of the OpenHome SDK will include a tool to help you generate the provider.

## <span id="Prerequisites_2"></span>Prerequisites

You must be in possession of:

- the OpenHome SDK, unpacked on your computer
- your Widget Service XML file

# <span id="Writing_a_SimpleUPnP_driver"></span>Writing a SimpleUPnP driver

## <span id="Introduction_to_the_SimpleUPnP_protocol"></span>Introduction to the SimpleUPnP protocol

The SimpleUPnP protocol was developed as a test protocol used to control emulated Widgets over a custom UPnP service.

This chapter shows how a driver is written using the SimpleUPnP communications protocol. The aim is to show the code using as generic a protocol as possible so that you can see where your own protocol specific code needs to go.

The use of code specific to the SimpleUPnP implementation is highlighted by the use of the ![Warning.png](/mediawiki/images/c/cb/Warning.png "Warning.png") icon. The lines of code are marked by this icon to make it easier for you to see where the protocol-specific code must go and what parts of the code are generic.

### <span id="Register_model"></span>Register model

SimpleUPnP is modeled on 8 physical registers available on the Widget. Each register is 32-bits wide. They are indexed from 0 to 7 and the last register (register 7) is reserved for storing the Widget's class.

This detail is used by the Protocol Module on the Node to determine which driver is needed to run the new Widget when it has been discovered.

The remaining 7 registers (registers 0 to 6) are free for Widget engineers to assign to the Widget's functions.

Registers 0, 1, 2 and 3 are available as read/write registers. Registers 4, 5 and 6 are readonly registers.

Only the emulated hardware (running on the Node) can change the values held in registers 4, 5 and 6.

### <span id="Register_use_in_drivers"></span>Register use in drivers

In the example that follows we have a Basic Light Widget with a very simple function: it can be turned on and turned off. The on/off value is stored in register 0, with values 0=OFF and 1=ON. Register 0 is a read/write register. This means we can change the value stored there using messages passed to the Widget from the Node, and by reacting to physical interactions at the Widget (such as someone manually switching the light on or off).

The mapping of registers to properties on the Widget is decided by the engineers who manufacture the device. You must be provided with the mapping before you begin developing your driver.

## <span id="Starting_the_driver"></span>Starting the driver

<figure>
<img src="/mediawiki/images/f/f0/DriverNodeArchitecture-BoxHighlight.png" title="Figure 3 The driver architecture highlighting the Widget driver and its component parts." width="800" alt="DriverNodeArchitecture-BoxHighlight.png" />
<figcaption>Figure 3 The driver architecture highlighting the Widget driver and its component parts.</figcaption>
</figure>

When you have generated the abstract provider you can put it to use in the Widget driver. A Widget driver has three distinct components:

- an implementation of your abstract provider
- a definition of the Widget driver
- an implementation of the IWidgetRegistryEntry interface

> **Important**
>
> You must manually write the code for your Widget driver. The differences in implementation of Widget properties and communication protocols means that the driver code cannot be autogenerated.

This section takes you through how to write a Widget driver by implementing the auto-generated provider, starting from a new blank file and finishing with a working driver for the Basic Light Widget.

> **Note**
>
> No assumptions have been made about the type of editor you use to write your code. Shortcuts or macros that you use as standard will not appear in the instructions below. A full example BinaryLightDriver.cs is available to review in Appendix C.

### <span id="Writing_the_code"></span>Writing the code

Create a new C# file in your IDE. Ensure the following libraries are used:

`using System;`  
`using System.Collections.Generic;`  
`using OpenHome.Net.Device;`  
`using OpenHome.Widget.Nodes.Local;`  
`using OpenHome.Widget.Nodes.Local.Providers;`  
![`Warning.png`](/mediawiki/images/c/cb/Warning.png "Warning.png")`using OpenHome.Widget.Protocols.SimpleUpnp;`  
`namespace OpenHome.Widget.Drivers.SimpleUpnp`  
`{`

> **Important**
>
> You must use the libraries listed above for this specific example.
>
> In general, drivers require the following libraries:
>
> - System\*
> - System.Collections.Generic\*
> - OpenHome.Widget.Nodes.Local.Providers
>
> Your driver will fail to compile if you miss any of these listed libraries. Libraries marked \* are typically added by default by most modern IDEs.
>
> The OpenHome.Widget.Protocols.SimpleUpnp library is required only in this SimpleUPnP example. Drivers using a different protocol will use their own protocol library.

## <span id="Implementing_the_provider"></span>Implementing the provider

<figure>
<img src="/mediawiki/images/2/22/DriverNodeArchitecture-ProviderHighlight.png" title="Figure 4 The driver architecture highlighting the Provider&#39;s place" width="800" alt="DriverNodeArchitecture-ProviderHighlight.png" />
<figcaption>Figure 4 The driver architecture highlighting the Provider's place</figcaption>
</figure>

You use your auto-generated abstract provider by writing an implementation of it in the driver file. Responsibilities met by implementing your auto-generated provider are:

**R3 Setting the initial values for the Widget's properties**

A driver must set the Widget object's initial properties.

**R6 Reacting to actions sent to the Widget**

A driver must update a specified property to a new value when instructed to do so by the Node.

### <span id="Writing_the_code_2"></span>Writing the code

Begin by creating a new class. It will subclass the abstract auto-generated provider:

`class BinaryLightProvider : DvProviderOpenhomeOrgTestBinaryLight1`  
`{`

The Protocol Module will provide an API for the Provider to use to communicate with the Widget. In SimpleUPnP we are provided with an interface called ISimpleUpnpWidget. The provider is supplied with the required instance of the interface by the Discovery Module on the Node.

The mechanisms for registering providers with specific Protocol Modules, and for the way the module gives each provider its required interface are covered later when writing the discovery method.

For now, we need to give the Provider a place to store the interface that it will later use to communicate with the Widget:

![`Warning.png`](/mediawiki/images/c/cb/Warning.png "Warning.png")` private ISimpleUpnpWidget iProtocol;`

The interface from the Protocol Module is passed in as a parameter in the Provider's constructor and then assigned to the variable we just created:

`public BinaryLightProvider(DvDevice aDevice,`  
![`Warning.png`](/mediawiki/images/c/cb/Warning.png "Warning.png")`         ISimpleUpnpWidget aProtocol) : base(aDevice)`  
`{`  
`      iProtocol = aProtocol;`  
`}`

> **Note**
>
> To satisfy R3 we would normally set the Widget's properties here, giving them an initial value. However, in this specific example we cannot set the value of Basic Light's only property because we will never know, in advance, what the state of the light will be (either on or off) when we create the DiscoveredWidget.
>
> When you cannot set the properties ahead of time, and you are using an eventing protocol like SimpleUPnP, you can instead set them in the HandleRegisterEvent method in the driver class. This also satisfies the requirements for R3. You must set the Widget's properties before you enable it using SetEnabled().

The abstract provider includes an abstract method called SetOn. This method is invoked by the Node when passing a message to the Widget, specifically to set the on property of the Widget to either 0 or 1. The implementation of this method will meet the requirements for R6.

We must override this method and provide the protocol module a way of passing a message on to the Widget to perform the required action, in this case turn the light on or off:

`         protected override void SetOn(uint aVersion, bool aValue)`  
`         {`  
`    `![`Warning.png`](/mediawiki/images/c/cb/Warning.png "Warning.png")`        iProtocol.Registers[0] = aValue ? (uint)1 : 0;`  
`         }`  
`    }`

In this example the Basic Light's SetOn property (the boolean property that controls whether the light is on or off) is represented in the physical Widget by the register that has an index of 0.

> **Note**
>
> - This method is an example of an action on a Widget. Actions are messages sent from the Node to the Widget. We will see later how to handle events that need to be passed back from the Widget
>
> to the Node.
>
> - Your own Widget will likely provide more than a single property. Your auto-generated provider will contain one abstract method to represent each writable property. Read-only properties are not provided an abstract method.
>
> You must implement each abstract method in your driver to ensure the relevant property on the Widget can be set.

We have now finished implementing the provider. The next step is to implement the driver.

## <span id="Implementing_the_driver"></span>Implementing the driver

<figure>
<img src="/mediawiki/images/a/af/DriverNodeArchitecture-DriverHighlight.png" title="Figure 4: The driver architecture highlighting the implemented driver&#39;s place." width="800" alt="DriverNodeArchitecture-DriverHighlight.png" />
<figcaption>Figure 4: The driver architecture highlighting the implemented driver's place.</figcaption>
</figure>

The code for your Widget driver must provide an implementation of the IWidgetRegistryInterface, including the following tasks:

- methods to expose identifying details about the Widget for the Node to access
- providing methods to handle events reported by the Widget

The driver is implemented as a public class within the same file as the provider code. Each driver must use the interface for the protocol you are using. For the SimpleUPnP protocol the interface is ISimple-UpnpWidgetDriver.

### <span id="Writing_code"></span>Writing code

Create your new driver class and subclass the ISimpleUpnpWidgetDriver interface:

`public class BinaryLightDriver : ISimpleUpnpWidgetDriver`  
`{`

### <span id="Implementing_IWidgetRegistryEntry"></span>Implementing IWidgetRegistryEntry

IWidgetRegistryEntry is the interface you use to represent physical Widgets. It is implemented as a subclass of your driver class. We are going to implement this interface in a class called **DiscoveredWidget**.

Let's return to our driver architecture diagram for a moment:

<figure>
<img src="/mediawiki/images/f/f7/DriverNodeArchitecture-IRegistryEntryHighlight.png" title="Figure 5 The driver architecture highlighting the IWidgetRegistryEntry object you will now implement" width="800" alt="DriverNodeArchitecture-IRegistryEntryHighlight.png" />
<figcaption>Figure 5 The driver architecture highlighting the IWidgetRegistryEntry object you will now implement</figcaption>
</figure>

IWidgetRegistryEntry uses several other objects to help create it and respond to messages sent to and from it. These objects will be created in our implementation of DiscoveredWidget.

When successfully created and published, the DiscoveredWidget objects are stored in a list on the Node called the Local Widget Registry. The Local Widget Registry is used by Nodes to maintain contact with the Widgets they control.

The Local Widget Registry is shown at the top of Figure 5, marked plainly as (Registry). The path to the Local Widget Registry goes through several layers of Node architecture which are not relevant to Widget driver writing, so are not shown in the diagrams.

#### <span id="Writing_code_2"></span>Writing code

Start by subclassing the IWidgetRegistryEntry interface in your new class:

`     private class DiscoveredWidget : IWidgetRegistryEntry`  
`     {`

A DiscoveredWidget must provide the driver with the objects required to present the Widget and its properties to the Node:

`          private readonly IDvDeviceFactory iDeviceFactory;`  
`          private readonly IWidgetPublisher iPublisher;`  
`          private readonly ISimpleUpnpWidget iProtocol;`  
`          private readonly BinaryLightProvider iProvider;`  
`          private readonly DvDevice iDvDevice;`  
`          private IPublishedWidget iPublishedWidget;`

Each of the attributes in the example above are defined as follows:

iDeviceFactory — used by the driver to create a single instance of DvDevice to represent a single Widget

iPublisher — used by the driver to publish the Widget to the Node

iProtocol — the object used by the Widget to communicate with the Protocol Module on the Node

iProvider — an instantiated provider of the type you defined earlier

iDvDevice — a representation of a Widget to which the provider is attached, created using iDevice-Factory above

iPublishedWidget — used to contain the returned object from a successful publishing of the Widget If we look again at the driver architecture diagram, we ca highlight the objects we've just defined:

<figure>
<img src="/mediawiki/images/0/09/DriverNodeArchitecture-Highlight.png" title="Figure 6: The driver architecture highlighting the objects used by the IWidgetRegistryEntry implementation" width="800" alt="DriverNodeArchitecture-Highlight.png" />
<figcaption>Figure 6: The driver architecture highlighting the objects used by the IWidgetRegistryEntry implementation</figcaption>
</figure>

> **Note**
>
> The DeviceFactory, defined above in the member variable iDeviceFactory, is used to create new DvDevice objects. The DeviceFactory is only ever used to do this once. It is not shown in the driver architecture diagrams due to its minimal role in the operation of a driver, but it would normally appear between the IWidgetRegistryEntry and DvDevice objects.

A driver requires methods to expose identifying details about the Widget. We must provide access to two of the attributes we just defined above:

`public DvDevice DvDevice`  
`{`  
`    get { return iDvDevice; }`  
`}`  
`public string WidgetClass`  
`{`  
`    get { return "openhome.org:BinaryLight"; }`  
`}`

The WidgetClass string is formed using a combination of the vendor name and the Widget's name in the format:

`[vendor_domain]:[widget_name]`

The Local Widget Registry can now query both the DvDevice object representing the Widget, and the specific class of Widget this driver represents. The other member variables we defined do not need their own accessor methods.

Now we must write a constructor for DiscoveredWidget and assign the parameters accordingly:

`public DiscoveredWidget(IDvDeviceFactory aDeviceFactory,`  
`                           string aUdn,`  
`                           ISimpleUpnpWidget aProxy,`  
`                           IWidgetPublisher aPublisher)`  
`{`  
`     iDeviceFactory = aDeviceFactory;`  
`     iProtocol = aProtocol;`  
`     iPublisher = aPublisher;`  
`     iDvDevice = iDeviceFactory.CreateDevice(aUdn);`  
`     iProvider = new BinaryLightProvider(iDvDevice,`  
`     iProtocol);`  
`}`

### <span id="Event_handling"></span>Event handling

A Widget's state can change in one of three significant ways:

- when the Widget needs to be published on the Node
- when the Widget disappears from the network (by losing power or similar)
- when a property's state changes and must be updated to a new value

We now need methods to handle these changes.

> **Important**
>
> The methods we define here will be used as callbacks, rather than invoked as method calls. We define the methods here first and then use them later on. We will use the Protocol Module to listen for changes in the Widget's state and register these methods as callbacks there. See Writing the SimpleUPnP Widget discovery method for more details.

Responsibilities met in this section of the driver are:

**R3 Setting the initial values for the Widget's properties**

A driver must set the Widget object's initial properties.

**R4 Publishing discovered Widgets in the Local Widget Registry on the Node**

Publishing Widgets advertises their presence on the network. This allows Nodes to access the Widgets and present their services for use. A driver must be able to enable and publish a Widget object.

**R5 Reacting to an event reported from the Widget**

A driver must update the Node with the state of the Widget's properties when the Widget reports a change.

**R7 Reacting to a Widget's departure**

A driver must properly handle the IWidgetRegistryEntry object when the physical Widget is no longer available.

#### <span id="Enabling_and_publishing_a_discovered_Widget"></span>Enabling and publishing a discovered Widget

The first method initializes the Widget by enabling the device and then using the IWidgetPublisher to make it available on the Node:

`public void HandleInitialEvent()`  
`{`  
`     iDvDevice.SetEnabled();`  
`     iPublisher.TryPublishWidget(iDvDevice.iUdn(),`  
`                             this,`  
`                             out iPublishedWidget);`  
`}`

This method meets the requirements for R4.

The call to TryPublishWidget returns an iPublishedWidget object. We use this object later to satisfy the requirements of R7.

> **Important**
>
> The ordering of the calls to SetEnabled and TryPublishWidget is vitally important. You must enable the device before you attempt to publish it. Your Widget will not be available to the Nodes unless SetEnabled is called first. Nodes will not be able to access a published device that has not been enabled.

> **Note**
>
> R3 requires that you set the Widget's properties before you enable and publish the device. We discussed on page 14 how some properties can only be set after the Widget reports what their state is. We do this in HandleRegisterEvent.
>
> We rely on the SimpleUPnP Protocol Module guaranteeing a call to HandleRegisterEvent first before HandleInitialEvent. This is informed by guarantees made by the Control Point stack that the calls will be made in that order.

#### <span id="Removing_a_Widget"></span>Removing a Widget

Removing a Widget involves unpublishing it from the Node. The IPublishedWidget interface provides us with a method we can call to manage that for us:

`public void HandleDisappearance(bool aGoneFromNetwork)`  
`{`  
`    if (iPublishedWidget != null)`  
`    { iPublishedWidget.Unpublish(); }`

Assuming that the Widget was successfully published earlier, it is removed from the Node's Local Widget Registry.

We must also properly handle the resources we used to create and maintain the Widget object while it was published:

`     iProvider.Dispose();`  
`     iDvDevice.Dispose();`  
`}`

The calls to Dispose are made regardless of the Widget's published state, ensuring that any created device and associated provider are properly disposed. This implementation satisfies R7.

#### <span id="Event_handling_2"></span>Event handling

We need a method to handle changes to the state of the Widget's properties.

If the property changes at the Widget, it needs to pass the new state back to the Node so that it is kept up-to-date on the Widget's status. This is called an event. An example in the case of our Basic Light is someone manually switching the light from on to off. This is in contrast to actions, which are passed from the Node to the Widget.

> **Note**
>
> Other examples of events involve no human interaction, such as a thermometer Widget updating its current temperature based on environmental changes.

Our Basic Light Widget has only one property that needs to be handled:

`public void HandleRegisterEvent(uint aIndex, uint aValue)`  
`{`  
`    if (aIndex == 0)`  
`    {`  
`        iProvider.SetPropertyOn(aValue != 0);`  
`    }`  
`}`

We use our instance of the provider to update the register on the Widget that is mapped to the On property. This in turn updates the Node with the new state of the Widget.

This method provides implementations to satisfy two driver responsibilities:

- R3 is now completely satisfied, as we can now set the values of all the previously unknown properties here.
- R5 is also satisfied as this method allows us to update the Widget's status on the Node when a property is changed on the Widget.

> **Note**
>
> Not all protocols pass messages back to the Node in this manner. The way we have satisfied R3 and R5 here only applies to protocols and Widgets that support this behavior.
>
> Widgets that do not use an eventing protocol need to have their properties set in the provider's constructor to satisfy R3.
>
> To satisfy R5, the over-ridden method SetOn in the provider must include the call to SetPropertyOn. Non-eventing protocols do not require a HandleRegisterEvent method.

### <span id="Constructor"></span>Constructor

The final requirement for the driver is the constructor so that new DiscoveredWidget objects can be created.

Responsibilities met in this area of code are:

**R1 Specifying the type of Widget the driver controls**

A driver must know which type of Widget that it can communicate with and be able to provide that information to the Discovery Module. A driver will normally communicate with one specific type of Widget and will only ever use one communications protocol.

#### <span id="Writing_the_code_3"></span>Writing the code

We begin by defining the variables we will use to store the objects used by the driver:

`private readonly string iName;`  
`private readonly IDvDeviceFactory iDeviceFactory;`  
`private readonly IWidgetPublisher iWidgetPublisher;`

We can now write the constructor for the driver and assign the passed in parameters appropriately:

`public BinaryLightDriver(string aName,`  
`               IWidgetPublisher aPublisher,`  
`               IDvDeviceFactory aDeviceFactory)`  
`{`  
`    iWidgetPublisher = aPublisher;`  
`    iName = aName;`  
`    iDeviceFactory = aDeviceFactory;`  
`}`

Finally we need to provide the driver a way to publish the class of Widget it controls. This information is requested by the Discovery Module and is used to ensure the Node uses the correct driver when a new Widget appears.

The implementation for this details will be different for each protocol. The SimpleUPnP protocol library provides a file that contains the SimpleUPnP definitions as integers. Each integer represents a particular class of identified Widget.

The SimpleUPnP implementation of that method is as follows:

`public IEnumerable`\<uint\>` WidgetClasses`  
`{`  
![`Warning.png`](/mediawiki/images/c/cb/Warning.png "Warning.png")`        get { yield return (uint)WidgetKind.BinaryLight; }`  
`}`

The body of this method is specifically written for the Widget class we are defining (in this case a binary light). This method completes the driver's requirements for R1.

## <span id="Writing_the_SimpleUPnP_Widget_discovery_method"></span>Writing the SimpleUPnP Widget discovery method

Every driver must contain a method which creates new objects to represent newly discovered Widgets. The Discovery Module invokes this method to begin the process of creating the objects required to allow the Node to access the Widget.

The name of this method is dictated by your chosen protocol's API. The SimpleUPnP protocol requires a method called WidgetDiscovered.

> **Note**
>
> The method's name will not always be the same for each protocol. Your protocol's documentation will contain the details of what this method must be called.

This method and its implementation will meet the following driver responsibilities:

**R2 Reacting to a discovered Widget on the network**

A driver must create a new IWidgetRegistryEntry object to represent the Widget and use it to listen to changes in the physical Widget's state.

Our implementation of the WidgetDiscovered method will create a new DiscoveredWidget object and use the Protocol Module to listen for changes to the Widget's state.

### <span id="Writing_the_code_4"></span>Writing the code

The method uses the Protocol Module and two ways to identify the Widget. We must pass these in as parameters:

`public void WidgetDiscovered(string aWidgetUdn,`  
`                             uint aWidgetClass,`  
`                             ISimpleUpnpWidget`  
`                                 aSimpleUpnpWidget)`  
`{`

Every Widget that uses this driver must be uniquely identifiable:

![`Warning.png`](/mediawiki/images/c/cb/Warning.png "Warning.png")`    string newUdn = aWidgetUdn;`

Each new Widget is represented by a DiscoveredWidget object. Create the new DiscoveredWidget and pass in the required parameters we created earlier:

`    DiscoveredWidget discoveredWidget =`  
`                new DiscoveredWidget(iDeviceFactory,`  
`                                     newUdn,`  
` `  
![`Warning.png`](/mediawiki/images/c/cb/Warning.png "Warning.png")`                                    aSimpleUpnpWidget,`

### <span id="Registering_the_callbacks"></span>Registering the callbacks

Finally, we ask the Widget's protocol interface to listen for calls to the handler methods we defined earlier in DiscoveredWidget. We do this by registering those methods as callbacks for the Protocol Module to listen for:

![`Warning.png`](/mediawiki/images/c/cb/Warning.png "Warning.png")`             aSimpleUpnpWidget.Listen(`  
`                       discoveredWidget.HandleInitialEvent,`  
`                       discoveredWidget.HandleRegisterEvent,`  
`                       discoveredWidget.HandleDisappearance);`  
`        }`  
`    }`  
`} //End of file`

You have now met 100% of the driver responsibility requirements and have a working driver to use with your SimpleUPnP Widget.

# <span id="Appendix_A._Sample_XML"></span>Appendix A. Sample XML

## <span id="Binary_Light.xml"></span>Binary Light.xml

\<widgetService\>  
` `\<description\>\</description\>  
` `\<version\>  
`  `\<major\>`1`\</major\>  
`  `\<minor\>`0`\</minor\>  
` `\</version\>  
` `\<propertylist\>  
`  `\<property primary="true"\>  
`   `\<description\>`Indicates whether the light is currently`  
`      illuminated`\</description\>  
`   `\<name\>`On`\</name\>  
`   `\<dataType\>`boolean`\</dataType\>  
`   `\<access\>`readWrite`\</access\>  
`  `\</property\>  
` `\</propertylist\>  
\</widgetService\>

# <span id="Appendix_B._Sample_Provider"></span>Appendix B. Sample Provider

## <span id="DvWidgetOpenhomeOrgBasicLight1.cs"></span>DvWidgetOpenhomeOrgBasicLight1.cs

`using System;`  
`using System.Runtime.InteropServices;`  
`using System.Collections.Generic;`  
`using OpenHome.Net.Core;`  
`using OpenHome.Net.Device;`  
`using OpenHome.Widget.Utils.Binary;`  
  
`namespace OpenHome.Widget.Nodes.Local.Providers`  
`{`  
`   public interface IDvProviderOpenhomeOrgBinaryLight1 :`  
`       IDisposable`  
`   {`  
`       /// `

\<summary\>

`       /// Set the value of the On property`  
`       /// `

\</summary\>

`       /// `\<param name="aValue"\>`New value for the property`\</param\>  
`       /// `\<returns\>`true if the value has been updated;`  
`       /// false if aValue was the same as the previous value`  
`       /// `\</returns\>  
`       bool SetPropertyOn(bool aValue);`  
` `  
`       /// `

\<summary\>

`       /// Get a copy of the value of the On property`  
`       /// `

\</summary\>

`       /// `\<param name="aValue"\>`Property's value will be copied`  
`       /// here`\</param\>  
`       bool PropertyOn();`  
`   }`  
`   /// < summary>`  
`   /// Provider for the openhome.org:BinaryLight:1 UPnP service`  
`   /// `

\</summary\>

`   public abstract class DvProviderOpenhomeOrgBinaryLight1 :`  
`              DvProvider,`  
`              IDisposable,`  
`              IDvProviderOpenhomeOrgBinaryLight1`  
`   {`  
`       private GCHandle iGch;`  
`       private PropertyBool iPropertyOn;`  
`       private PropertyUint iPropertyPrimarySeq;`  
`       private PropertyUint iPropertySecondarySeq;`  
`       private ActionDelegate iDelegateSetProperty;`  
`       private ActionDelegate iDelegateGetProperty;`  
`       private ActionDelegate iDelegateGetPrimaryProperty;`  
` `  
`       /// `

\<summary\>

`       /// Constructor`  
`       /// `

\</summary\>

`       /// `\<param name="aDevice"\>`Device which owns this`  
`       /// provider`\</param\>  
`       protected DvProviderOpenhomeOrgBinaryLight1(DvDevice aDevice)`  
`           : base(aDevice, "openhome.org", "GenericWidget", 1)`  
`       {`  
`           iGch = GCHandle.Alloc(this);`  
`           List`\<String\>` allowedValues = new List`\<String\>`();`  
`           iPropertyOn = new PropertyBool(new ParameterBool("On"));`  
`           iPropertyPrimarySeq = new PropertyUint`  
`               (new ParameterUint("PrimarySeq"));`  
`           AddProperty(iPropertyPrimarySeq);`  
`           iPropertySecondarySeq = new PropertyUint`  
`               (new ParameterUint("SecondarySeq"));`  
`           AddProperty(iPropertySecondarySeq);`  
`           SetPropertyUint(iPropertyPrimarySeq, 0);`  
`           SetPropertyUint(iPropertySecondarySeq, 0);`  
` `  
`           Zapp.Core.Action action = new Zapp.Core.Action`  
`               ("SetProperty");`  
`           allowedValues.Add("PropInt");`  
`           allowedValues.Add("PropBool");`  
`           allowedValues.Add("PropStr");`  
`           allowedValues.Add("PropBin");`  
`           allowedValues.Add("FireAndForget");`  
`           action.AddInputParameter(new ParameterString`  
`               ("Name", allowedValues));`  
`           allowedValues.Clear();`  
`           action.AddInputParameter(new ParameterBinary("Value"));`  
`           iDelegateSetProperty = new ActionDelegate(DoSetProperty);`  
`           EnableAction(action, iDelegateSetProperty,`  
`               GCHandle.ToIntPtr(iGch));`  
` `  
`           action = new Zapp.Core.Action("GetProperty");`  
`           allowedValues.Add("PropInt");`  
`           allowedValues.Add("PropBool");`  
`           allowedValues.Add("PropStr");`  
`           allowedValues.Add("PropBin");`  
`           allowedValues.Add("UpdateCount");`  
`           action.AddInputParameter(new ParameterString`  
`               ("Name", allowedValues));`  
`           allowedValues.Clear();`  
`           action.AddOutputParameter(new ParameterBinary("Value"));`  
`           iDelegateGetProperty = new ActionDelegate(DoGetProperty);`  
`           EnableAction(action, iDelegateGetProperty,`  
`               GCHandle.ToIntPtr(iGch));`  
` `  
`           action = new Zapp.Core.Action("GetPrimaryProperty");`  
`           allowedValues.Add("");`  
`           allowedValues.Add("PropInt");`  
`           allowedValues.Add("PropBool");`  
`           allowedValues.Add("PropStr");`  
`           allowedValues.Add("PropBin");`  
`           allowedValues.Add("UpdateCount");`  
`           action.AddOutputParameter(new ParameterString`  
`                ("Name", allowedValues));`  
`           allowedValues.Clear();`  
`           allowedValues.Add("");`  
`           allowedValues.Add("integer");`  
`           allowedValues.Add("boolean");`  
`           allowedValues.Add("string");`  
`           allowedValues.Add("binary");`  
`           action.AddOutputParameter(new ParameterString`  
`               ("Type", allowedValues));`  
`           allowedValues.Clear();`  
`           action.AddOutputParameter(new ParameterBinary("Value"));`  
`           allowedValues.Add("");`  
`           allowedValues.Add("readWrite");allowedValues.Add`  
`               ("readOnly");`  
`           allowedValues.Add("writeOnly");`  
`           action.AddOutputParameter(new ParameterString("Access",`  
`               allowedValues));`  
`           allowedValues.Clear();`  
`           iDelegateGetPrimaryProperty = new`  
`           ActionDelegate(DoGetPrimaryProperty);`  
`           EnableAction(action, iDelegateGetPrimaryProperty,`  
`           GCHandle.ToIntPtr(iGch));`  
`       }`  
  
`       /// `

\<summary\>

`       /// Set the value of the On property`  
`       /// `

\</summary\>

`       /// `\<param name="aValue"\>`New value for the property`\</param\>  
`       /// `\<returns\>`true if the value has been updated;`  
`       /// false if aValue was the same as the previous`  
`       /// value`\</returns\>  
`       public bool SetPropertyOn(bool aValue)`  
`       {`  
`           if (iPropertyOn.SetValue(aValue))`  
`           {`  
`               lock (iPropertyPrimarySeq)`  
`               {`  
`                   SetPropertyUint(iPropertyPrimarySeq,`  
`                       iPropertyPrimarySeq.Value() + 1);`  
`               } return true;`  
`           } return false;`  
`       }`  
` `  
`       /// `

\<summary\>

`       /// Get a copy of the value of the On property`  
`       /// `

\</summary\>

`       /// `\<returns\>`The value of the property`\</returns\>  
`       public bool PropertyOn()`  
`       {`  
`           return iPropertyOn.Value();`  
`       }`  
` `  
`       /// `

\<summary\>

`       /// Set the On property.`  
`       /// `

\</summary\>

`       /// `\<param name="aVersion"\>`Version of the service being`  
`       /// requested (will be <= the version advertised)`\</param\>` `  
`       /// `\<param name="aValue"\>`New value for the On property.`  
`       /// `\</param\>  
`       protected abstract void SetOn(uint aVersion, bool aValue);`  
` `  
`       private static int DoSetProperty(IntPtr aPtr,`  
`                       IntPtr aInvocation,`  
`                       uint aVersion)`  
`       {`  
`           GCHandle gch = GCHandle.FromIntPtr(aPtr);`  
`           DvProviderOpenhomeOrgBinaryLight1 self =`  
`               (DvProviderOpenhomeOrgBinaryLight1)gch.Target;`  
`           DvInvocation invocation = new DvInvocation(aInvocation);`  
`           try`  
`           {`  
`               invocation.ReadStart();`  
`               string name = invocation.ReadString("Name");`  
`               byte[] valBin = invocation.ReadBinary("Value");`  
`               invocation.ReadEnd();`  
`               switch (name)`  
`               {`  
`                   case "On":`  
`                       self.SetOn(aVersion, Converter.`  
`                           BinaryToBoolean(valBin));`  
`                       break;`  
`                   default:`  
`                       throw new ActionError();`  
`               }`  
`               invocation.WriteStart();`  
`               invocation.WriteEnd();`  
`           }`  
`           catch (ActionError)`  
`           {`  
`               invocation.ReportError(501, "Invalid XML"); ;`  
`               return -1;`  
`           }`  
`           catch (PropertyUpdateError)`  
`           {`  
`               invocation.ReportError(501, "Invalid XML"); ;`  
`               return -1;`  
`           }`  
`       return 0;`  
`       }`  
` `  
`       private static int DoGetProperty(IntPtr aPtr,`  
`                       IntPtr aInvocation,`  
`                       uint aVersion)`  
`       {`  
`           GCHandle gch = GCHandle.FromIntPtr(aPtr);`  
`           DvProviderOpenhomeOrgBinaryLight1 self =`  
`               (DvProviderOpenhomeOrgBinaryLight1)gch.Target;`  
`           DvInvocation invocation = new DvInvocation(aInvocation);`  
`           try`  
`           {`  
`               invocation.ReadStart();`  
`               string name = invocation.ReadString("Name");`  
`               invocation.ReadEnd();`  
`               invocation.WriteStart();`  
`           switch (name)`  
`           {`  
`               case "On":`  
`               invocation.WriteBinary("Value",`  
`                   Converter.BooleanToBinary(self.iPropertyOn.`  
`                       Value()));`  
`               break;`  
`               default:`  
`               throw new ActionError();`  
`           }`  
`           invocation.WriteEnd();`  
`       }`  
`       catch (ActionError)`  
`       {`  
`           invocation.ReportError(501, "Invalid XML"); ;`  
`           return -1;`  
`       }`  
`       catch (PropertyUpdateError)`  
`       {`  
`           invocation.ReportError(501, "Invalid XML"); ;`  
`           return -1;`  
`       }`  
`       return 0;`  
`   }`  
`   private static int DoGetPrimaryProperty(IntPtr aPtr,`  
`                   IntPtr aInvocation,`  
`                   uint aVersion)`  
`   {`  
`       GCHandle gch = GCHandle.FromIntPtr(aPtr);`  
`       DvProviderOpenhomeOrgBinaryLight1 self =`  
`           (DvProviderOpenhomeOrgBinaryLight1)gch.Target;`  
`       DvInvocation invocation = new DvInvocation(aInvocation);`  
` `  
`       try`  
`       {`  
`           invocation.ReadStart();`  
`           invocation.ReadEnd();`  
`           invocation.WriteStart();`  
`           invocation.WriteString("Name", "On");`  
`           invocation.WriteString("Type", "boolean");`  
`           invocation.WriteBinary("Value",`  
`               Converter.BooleanToBinary(self.iPropertyOn.Value()));`  
`           invocation.WriteString("Access", "readWrite");`  
`           invocation.WriteEnd();`  
`       }`  
`       catch (ActionError)`  
`       {`  
`           invocation.ReportError(501, "Invalid XML"); ;`  
`           return -1;`  
`       }`  
`       catch (PropertyUpdateError)`  
`       {`  
`           invocation.ReportError(501, "Invalid XML"); ;`  
`           return -1;`  
`       }`  
`       return 0;`  
`   }`  
`   /// `

\<summary\>

`   /// Must be called for each class instance. Must be called before`  
`   /// Core.Library.Close().`  
`   /// `

\</summary\>

`   public void Dispose()`  
`   {`  
`       DoDispose();`  
`       GC.SuppressFinalize(this);`  
`   }`  
` `  
`   ~DvProviderOpenhomeOrgBinaryLight1()`  
`   {`  
`       DoDispose();`  
`   }`  
` `  
`       private void DoDispose()`  
`       {`  
`           lock (this)`  
`           {`  
`               if (iHandle == IntPtr.Zero)`  
`           {`  
`                   return;`  
`           }`  
`           DisposeProvider();`  
`           iPropertyOn.Dispose();`  
`           iHandle = IntPtr.Zero;`  
`           }`  
`           iGch.Free();`  
`       }`  
`   }`  
`}`

# <span id="Appendix_C._Sample_Driver"></span>Appendix C. Sample Driver

## <span id="BasicLightDriver.cs"></span>BasicLightDriver.cs

`using System.Collections.Generic;`  
`using OpenHome.Net.Device;`  
`using OpenHome.Widget.Nodes.Local;`  
`using OpenHome.Widget.Nodes.Local.Providers;`  
`using OpenHome.Widget.Protocols.SimpleUpnp;`  
  
`namespace OpenHome.hWidget.Drivers.SimpleUpnp`  
`{`  
`    class BinaryLightProvider : DvProviderOpenhomeOrgTestBinaryLight1`  
`    {`  
`        private ISimpleUpnpWidget iProtocol;`  
`        public BinaryLightProvider(DvDevice aDevice, `  
`            ISimpleUpnpWidget aProtocol) : base(aDevice)`  
`        {`  
`            iProtocol = aProtocol;`  
`        }  `  
  
`        protected override void SetOn(uint aVersion, bool aValue)`  
`        {`  
`            iProtocol.Registers[0] = aValue ? (uint)1 : 0;`  
`        }`  
`    }`  
  
`    public class BinaryLightDriver : ISimpleUpnpWidgetDriver`  
`    {`  
`        private class DiscoveredWidget : IWidgetRegistryEntry`  
`        {`  
`            private readonly IDvDeviceFactory iDeviceFactory;`  
`            private readonly IWidgetPublisher iPublisher;`  
`            private readonly ISimpleUpnpWidget iProtocol; `  
  
`            private readonly BinaryLightProvider iProvider;`  
`            private readonly DvDevice iDvDevice;`  
`            private IPublishedWidget iPublishedWidget; `  
  
`            public DvDevice DvDevice`  
`            {`  
`                get { return iDvDevice; }`  
`            }`  
`            `  
`            public string WidgetClass`  
`            {`  
`                get { return "openhome.org:BinaryLight"; }`  
`            } `  
  
`            public DiscoveredWidget(`  
`                IDvDeviceFactory aDeviceFactory,`  
`                string aUdn,`  
`                ISimpleUpnpWidget aProxy,`  
`                IWidgetPublisher aPublisher)`  
`            {`  
`                iDeviceFactory = aDeviceFactory;`  
`                iProtocol = aProtocol;`  
  
`                iPublisher = aPublisher;`  
`                iDvDevice = iDeviceFactory.CreateDevice(aUdn);  `  
`                iProvider = new BinaryLightProvider(iDvDevice, `  
`                                                    iProtocol);`  
`            }`  
  
`            public void HandleInitialEvent()`  
`            {`  
`                iDvDevice.SetEnabled();`  
`                iPublisher.TryPublishWidget(iDvDevice.iUdn(), this,`  
`                    out iPublishedWidget);`  
`            } `  
  
`            public void HandleDisappearance(bool aGoneFromNetwork)`  
`            {`  
`                if (iPublishedWidget != null)`  
`                {`  
`                    iPublishedWidget.Unpublish();`  
`                } `  
`                iProvider.Dispose();`  
`                iDvDevice.Dispose();`  
`            }  `  
  
`            public void HandleRegisterEvent(uint aIndex, uint aValue)`  
`            {`  
`                if (aIndex == 0)`  
`                {`  
`                    iProvider.SetPropertyOn(aValue != 0);`  
`                }`  
`            }`  
`        }`  
`        `  
`        private readonly string iName;`  
`        private readonly IDvDeviceFactory aDeviceFactory;`  
`        private readonly IWidgetPublisher iWidgetPublisher;`  
`        `  
`        public BinaryLightDriver(`  
`            string aName,`  
`            IWidgetPublisher aPublisher,`  
`            iDeviceFactory aDeviceFactory)`  
`        {`  
`            iWidgetPublisher = aPublisher;`  
`            iName = aName;`  
`            iDeviceFactory = aDeviceFactory;`  
`        } `  
  
`        public IEnumerable<uint> WidgetClasses`  
`        {`  
`            get { yield return (uint)WidgetKind.BinaryLight; }`  
`        }  `  
  
`        public void WidgetDiscovered(`  
`            string aWidgetUdn,`  
`            uint aWidgetClass,`  
`            ISimpleUpnpWidget aSimpleUpnpWidget)`  
`        {`  
`            string newUdn = aWidgetUdn;`  
`            DiscoveredWidget discoveredWidget = new DiscoveredWidget`  
`                (iDeviceFactory,`  
`                 newUdn,`  
`                 aSimpleUpnpWidget,`  
`                 iWidgetPublisher);`  
  
`            aSimpleUpnpWidget.Listen(`  
`                discoveredWidget.HandleInitialEvent,`  
`                discoveredWidget.HandleRegisterEvent,`  
`                discoveredWidget.HandleDisappearance);`  
`        }`  
`    }`  
`} //End of file`

# <span id="Glossary"></span>Glossary

Control Point - The device that displays the user interface which makes use of services on the network to control a UPnP device.

CPNW - Control Point, Node, Widget. The model of devices used in OpenHome environments.

Node - The communications bridge between the Control Point and the Widget. Also the target for deployment of ohApps.

Node communication protocol - The custom UPnP protocol provided by OpenHome to allow Nodes to communicate with each other.

Node mesh - A collection of Nodes that intercommunicate.

ohApp - An application that runs on ohOS.

[ohNet](/wiki/OhNet) - Library for discovering, eventing and controlling services on a network. Includes a full implementation of the UPnP stack.

[ohOs](/wiki/OhOs) - The OpenHome Operating System. Core software for OpenHome systems that runs on Nodes.

UPnP - Universal Plug and Play. The network protocols set out by the UPnP Forum to allow networked devices to seamlessly establish connections and services.

Widget - The physical device installed in the user's home to provide them with a service.

Widget communication protocol - The protocol used by the Widget to advertise its availability and services to the Nodes. A typical Widget supports only one protocol.

Widget driver - The software used by the Node to communicate with the Widget.
{% endraw %}
