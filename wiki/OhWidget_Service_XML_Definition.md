---
title: "OhWidget Service XML Definition"
permalink: "/wiki/OhWidget_Service_XML_Definition"
redirect_from:
---

{% raw %}
# <span id="Introduction"></span>Introduction

This document is for Widget manufacturers using OpenHome to define Widget services and properties. The services and properties are defined in XML, following the schema published by OpenHome.

> **Note**
>
> Note The OpenHome SDK contains a copy of the WidgetService.xsd used for validation. OpenHome may occasionally update the XSD definition to include new Widget properties. When these become available, OpenHome will publish the new XSD documents on openhome.org. All new XSD documents will be included in new releases of the SDK.

To help you produce your Widget Service XML file, this document provides descriptions of each element you can use in your own Widget Service XML file. A sample Widget Service XML file is used throughout the document.

## <span id="Prerequisites"></span>Prerequisites

To begin defining your Widget Service XML you must in possession of the following items:

- technical details about the properties your Widget physically provides
- the OpenHome SDK, specifically the WidgetService.xsd file

## <span id="Related_documents"></span>Related documents

The XML you define is used in several areas of Widget development. Refer to the following documents to see how the XML is used:

- [OpenHome Widget Driver Development](/wiki/OhWidget_Driver_Development)

# <span id="Widget_Service_XML"></span>Widget Service XML

The Widget Service XML file is used to define the features that your Widget provides to users.

Each of these features is described as a property in the Widget Service XML. This may be a simple light Widget offering an on/off — or power — property, or a more complicated Widget offering volume, bass, and treble properties.

Your Widget Service XML file can contain as many properties as are necessary to describe the full range of the Widget's feature set. Your Widget Service XML must contain at least one property.

## <span id="Internal_structure"></span>Internal structure

The Widget Service XML file is validated against an XSD. The XSD is included in the OpenHome SDK.

Snippet 1 shows an abstract hierarchy of the elements used in a Widget Service XML file.

`widgetservice`  
`  description`  
`  version`  
`      major`  
`      minor`  
`  propertylist`  
`      property`  
`          name`  
`          description`  
`          dataType`  
`          access`  
`          allowedValueList*`  
`              allowedValue`  
`          allowedValueRange*`  
`              minimum*`  
`              maximum*`  
`              step*`

Snippet 1: An abstract view of a Widget Service XML, showing the structure of the various elements used. Elements marked \* are optional.

The structure of the XML is defined by OpenHome. You cannot change it and expect your Widget to operate on an OpenHome network. However, some of the files you generate from it can be customized.

## <span id="External_document_dependencies"></span>External document dependencies

Your Widget Service XML is used in several areas of Widget development. Several files are automatically generated from this one. Driver authors and UI developers both depend heavily on the code generated from your Widget Service XML. It is therefore essential that you write a well-formed Widget Service XML, conforming to the schema defined in the WidgetService.xsd.

The diagram below shows the significance of the Widget Service XML in relation to the generated files used by other developers to define and publish your Widget on an OpenHome network:

<figure>
<img src="/mediawiki/images/6/69/DriverDevDocHierarchy.png" title="Figure 1: The OpenHome document hierarcy, showing the files you can generate from the Widget Service XML." width="800" alt="DriverDevDocHierarchy.png" />
<figcaption>Figure 1: The OpenHome document hierarcy, showing the files you can generate from the Widget Service XML.</figcaption>
</figure>

The JavaScript proxies and the UI HTML and JavaScript files are used by Web UI developers to style and customize the UI that will run on an OpenHome Node.

The C# Provider is used by Widget driver authors to help them write the code required to operate the Widget.

The C# Proxy is used by developers to produce a C# control point application which can be used in place of the standard Web UI.

# <span id="XML_elements"></span>XML elements

The following tables explain each XML element that can appear in a Widget Service XML file. Descriptions of each element are provided alongside to explain their use. An example of the elements in use is provided in the appendix.

> **Note**
>
> Unless otherwise stated, each of the following elements is mandatory and must appear in your Widget Service XML.

## <span id="widgetService"></span>widgetService

The widgetService element contains the definition of a service available on the Widget.

#### <span id="Table_3.1._widgetService_element_description"></span>Table 3.1. widgetService element description

| \|**Element** | \| **Description** |
|----|----|
| widgetService | Contains the definition of a Widget's service. This element begins and ends a Widget Service XML file. |

The widgetService element has several child elements. They are defined as follows:

#### <span id="Table_3.2._widgetService_child_elements_description"></span>Table 3.2. widgetService child elements description

| \|**Element** | \| **Description** |
|----|----|
| description | Contains a plain text description of your Widget, its service and the properties the service provides. It appears as a programmer API comment above the class definitions in both the auto-generated Proxy and Provider files. |
| version | Contains a plain text description of your Widget, its service and the properties the service provides. It appears as a programmer API comment above the class definitions in both the auto-generated Proxy and Provider files. |
| propertylist | Contains the list of properties you want to make available on the Widget. Each entry in this list describes a single property using the property element. |

## <span id="version"></span>version

The version element has the following child elements:

#### <span id="Table_3.3._version_child_elements_description"></span>Table 3.3. version child elements description

| \|**Element** | \| **Description** |
|----|----|
| major | This element must appear once only and must contain the value 1. |
| minor | This element must appear once only and must contain the value 0. |

## <span id="propertylist"></span>propertylist

Use the propertylist element to hold the list of properties you want to make available on the Widget.

> **Note**
>
> Your propertylist should ideally contain a property entry for each feature your Widget provides.
>
> If you choose to exclude a feature from the propertylist, it will not be accessible to the user from any OpenHome UI.

The propertylist element has the following child elements:

#### <span id="Table_3.4._propertylist_child_elements_description"></span>Table 3.4. propertylist child elements description

| \|**Element** | \| **Description** |
|----|----|
| property | Contains a definition of a property available on the Widget, including: the property's name; the data type used to store the property's value; the read and write access for each property. Your Widget Service XML must contain at least one property definition. |

## <span id="property"></span>property

Use the property element to define a single property on the Widget. A property is one part of the service the Widget provides, such as power, volume or any other single feature.

The property element has the following child elements:

#### <span id="Table_3.5._property_child_elements_description"></span>Table 3.5. property child elements description

| \|**Element** | \| **Description** |
|----|----|
| access | Defines the read and write attributes of the property. The access definitions are: readOnly; read- Write; writeOnly. |
| allowedValueList | This only affects properties with the string dataType. Contains the list of acceptable string values the property can have. This element is optional. |
| allowedValueRange | This only affects properties with the integer dataType. Contains the minimum and maximum integer values the property can have and an optional step value which defines the interval between the minimum and maximum values. For example, a minimum of 0, a maximum of 10 and a step of 2 means the property can have the following values: 0, 2, 4, 6, 8, 10. This element is optional. |
| dataType | Contains the name of the data type used to store the value of the property. Data types currently supported are: binary; boolean; color; integer;string. |
| description | Contains the plain-text description of the property. The description is included in the generated files as developer documentation. |
| hint | This element allows you to add special definitions to both the boolean and the string dataType properties. Supported values for boolean are: booleanlockunlock; boolean-onoff; booleanopenclose; boolean-updown. This changes the default text strings used when the control is generated in the UI, rather than just on and off. Note that if you do not specify a hint value (either by leaving the element blank or not including it at all) the control will use the default value of booleanonoff. The supported value for string is uri-image. Any string property whose hint element is defined in this way is assumed to be a URI pointing to an image which will be displayed in the UI. |
| name | Contains the unique name for the property. The name must be unique within the service definition. This ensures the code in the generated files has unique function names for each property. |

## <span id="dataType"></span>dataType

The dataType element specifies the name of the data type used to store the value of the property. The value you specify here determines that type of information the property can process. It also determines which type of control is generated in the UI's HTML.

Choosing the correct value for the dataType element is important as it ensures that the Widget can be properly controlled by users. To help you ensure you are choosing the correct value, each of the supported values are described in more detail in the table below:

#### <span id="Table_3.6._dataType_values_description"></span>Table 3.6. dataType values description

| \|**Value** | \| **Description** |
|----|----|
| binary | Use this datatype when processing raw binary data, such as that used to represent a file or stream of data. |
| boolean | For specifying data that can have only one of two states. Typically used for controls to change a Widget from one of two allowed states to the other. Note that the hint element can be used to further define boolean to make sure the correct labeling is used. See the hint child element under property for more details. |
| color | This generates a color picker control that can be used to select a new RGB value. |
| integer | Used for representing whole numbers that can be used for properties that need a range of values, or need to have their value specified from a list of allowed values. |
| string | Displays plain text, typically as a label on the UI. Note that the hint element can be used to further define string to reference an image. This allows this type of property to display an image instead of text. See the hint child element under property for more details. |

## <span id="allowedValueRange"></span>allowedValueRange

Use the allowedValueRange to restrict the upper and lower values an integer property can have.

> **Note**
>
> If you do not set an allowedValueRange, the generated code will bound the values to the range of a 32-bit signed integer. Typically this range is too large to provide useful upper and lower limits for a property such as a light dimmer or a volume control.
>
> Setting your own limits means you get to determine what the boundaries for your Widget's properties are. This also has a direct effect on the sensitivity of the HTML controls generated for the UI.

The allowedValueRange element has the following child elements:

#### <span id="Table_3.7._allowedValueRange_child_elements_description"></span>Table 3.7. allowedValueRange child elements description

| \|**Element** | \| **Description** |
|----|----|
| minimum | Contains the lowest integer value this property can have. |
| maximum | Contains the highest integer value this property can have. The maximum value must be greater than or equal to the minimum value. |
| step | Contains a non-negative integer to define the increment between each change in value. The value you specify here must be exactly divisible into the difference between the maximum and minimum values. For example, if your minimum and maximum values are 0 and 50 respectively, your step value must be one of the following: 1, 2, 5, 10, 25 or 50. |

**HTML controls** The use of allowedValueRange in an integer property affects whether a text box or slider control is generated.

A text box is displayed in the Web UI if you do not provide an allowedValueRange.

A text box is also displayed if you do provide an allowedValueRange, but the difference between the maximum and minimum values is too great.

A slider control is displayed only if the difference between maximum and minimum is a small enough value. This value is set by OpenHome and is currently undefined.

## <span id="allowedValueList"></span>allowedValueList

Use the allowedValueList to restrict the values a string property can have.

The allowedValueList element has the following child elements:

#### <span id="Table_3.8._allowedValueList_child_elements_description"></span>Table 3.8. allowedValueList child elements description

| \|**Element** | \| **Description** |
|----|----|
| allowedValue | Contains a plain text string defining one of the allowed values. You must define a new allowedValue for each new value you want the control to be able to accept. |

**HTML controls** The use of allowedValueList affects how the control for a string property is generated.

If you provide an allowedValueList, a drop-down list is displayed in the Web UI with your defined entries in it. Users can select the value from this list.

If you do not provide an allowedValueList, a text box is displayed in the Web UI. Users can manually enter the desired value.

# <span id="Primary_property"></span>Primary property

A Widget's primary property is the property that users will want to access most often.

Once defined, the primary property is automatically displayed in the Web UI's summary view, along with the name of the Widget.

<figure>
<img src="/mediawiki/images/d/d6/SummaryViewAbstract.png" title="Figure 2. An abstract view of several Widgets&#39; summary views, aggregated in the Node UI." width="800" alt="SummaryViewAbstract.png" />
<figcaption>Figure 2. An abstract view of several Widgets' summary views, aggregated in the Node UI.</figcaption>
</figure>

For some simple Widgets the primary property is often the power property. For a more complicated Widget you will need to consider which property you want to assign as primary.

The details of the primary property are stored in the auto-generated Provider. This means the Node has direct access to these details and can provide the summary view UI at run-time.

## <span id="Assigning_the_primary_property"></span>Assigning the primary property

You assign the primary property by adding an attribute to the chosen property in the XML. For example, if we take the On property from a Basic Light Widget we can define it as the primary property by inserting primary="true". For example:

\<property primary="true"\>  
`    `\<description\>`Indicates whether the light is currently`  
`        illuminated`\</description\>  
`    `\<name\>`On`\</name\>  
`    `\<dataType\>`boolean`\</dataType\>  
`    `\<access\>`readWrite`\</access\>  
\</property\>

You must assign at most one primary property. Defining more than one property as the primary property will leave your XML unable to generate the other files used in Widget development.

> **Note**
>
> - Defining a primary property is not mandatory.
> - You do not need to indicate which properties are NOT the primary property. You use the primary attribute only once in your Widget Service XML as shown in the example above.

For more details about the Provider, see the [OpenHome Widget Driver Development](/wiki/OhWidget_Driver_Development) document.

# <span id="Naming_rules"></span>Naming rules

The contents of some elements in the Widget Service XML directly affect the output in the generated files.

These details are important for the developers who will use your Widget Service XML file to write drivers and UIs for the Widget.

The following sections explain how the XML you define affects the auto-generated output.

> **Note**
>
> The following sections are provided for information. You are not expected to learn any of this information to be able to write a Widget Service XML.

## <span id="Summary_view_UI"></span>Summary view UI

The details for the summary view UI are defined by the primary property in the XML.

Those details are stored in the Provider so that the Node can always access them and generate the summary view UI at run-time.

## <span id="Details_view_UI"></span>Details view UI

### <span id="HTML_and_UI_JavaScript"></span>HTML and UI JavaScript

The generated code used in the UI JavaScript and the HTML is based on the content of each of the elements you define in the XML.

## <span id="Provider"></span>Provider

The code generated in the C# provider presents the driver developers with a series of abstract functions they can implement. Those functions are generated using the values you provide in each property's name, dataType and access elements.

For example, the following property in the XML:

\<property primary="true"\>  
`    `\<description\>`Indicates whether the light is currently`  
`        illuminated `\</description\>  
`    `\<name\>`On`\</name\>  
`    `\<dataType\>`boolean`\</dataType\>  
`    `\<access\>`readWrite`\</access\>  
`    `\</property\>

will produce the following auto-generated code in the Provider:

`public bool SetPropertyOn(bool aValue)`  
`{`  
`   ...`  
`}`  
  
`public bool PropertyOn()`  
`{`  
`   ...`  
`}`  
`...`  
`protected abstract void SetOn(uint aVersion, bool aValue);`

Here we see two accessor functions and one abstract function have been created. The accessor functions allow the property's value to be read and written. The abstract function is for Widget driver writers to implement in the code they write.

Let's examine how each of the XML elements affects them.

### <span id="name"></span>name

The XML defines the property's \<name\> as On:

\<name\>`On`\</name\>

The generated code includes the property name in the names of each of the generated functions: Set- PropertyOn, PropertyOn and SetOn.

SetOn is the abstract function used in the Widget driver. This means that Widget driver writers will consistently use the same names throughout the code they write.

### <span id="access"></span>access

The XML defines the property's access as readWrite:

\<access\>`readWrite`\</access\>

The generated code provides two functions that meet this access setting. The first, SetPropertyOn, provides a way to write the property's value. The second, PropertyOn, provides a way to read the property's value.

If the access was defined as writeOnly, only the abstract SetOn function would be generated.

> **Important**
>
> If the access was defined as readOnly, a SetPropertyOn function is still generated, but is not accessible from the UI. The function remains in the auto-generated code so that the Widget can update the Node with the property's new state when it changes.

### <span id="dataType_2"></span>dataType

The XML defines the property's dataType as boolean:

\<dataType\>`boolean`\</dataType\>

The SetPropertyOn function automatically takes a bool as the parameter to use to set the new value of the property.

The PropertyOn function automatically returns a bool to report the value of the property.

The abstract SetOn function automatically takes a bool as the parameter used to set the new value of the property.

# <span id="Appendix_A"></span>Appendix A

\<widgetService\>  
`    `\<description\>\</description\>  
`    `\<version\>  
`        `\<major\>`1`\</major\>  
`        `\<minor\>`0`\</minor\>  
`    `\</version\>  
`    `\<propertylist\>  
`        <propertyprimary="true">`  
`            `\<description\>`Indicates whether the light is currently`  
`                illuminated`\</description\>  
`            `\<name\>`On`\</name\>  
`            `\<dataType\>`boolean`\</dataType\>  
`            `\<access\>`readWrite`\</access\>  
`            `\<hint\>`boolean-onoff`\</hint\>  
`        `\</property\>  
`    `\</propertylist\>  
\</widgetService\>

# <span id="Glossary"></span>Glossary

Control Point - The device that displays the user interface which makes use of services on the network to control a UPnP device.

CPNW - Control Point, Node, Widget. The model of devices used in Openhome environments.

Node - The communications bridge between the Control Point and the Widget. Also the target for deployment of ohApps.

Node communication protocol - The custom UPnP protocol provided by Openhome to allow Nodes to communicate with each other.

Node mesh A - collection of Nodes that intercommunicate.

ohApp - An application that runs inside ohOS.

[ohNet](/wiki/OhNet) - Library for discovering, eventing and controlling services on a network. Includes a full implementation of the UPnP stack.

[ohOs](/wiki/OhOs) - The Openhome Operating System. Core software for Openhome systems that runs on Nodes.

PDLP - Proxy Device List Provider. The pattern used to represent the layers of UPnP in the Openhome code. All layers except the Presentation layer are represented in this pattern.

UPnP - Universal Plug and Play. The network protocols set out by the UPnP Forum to allow networked devices to seamlessly establish connections and services.

Widget - The physical device installed in the user's home to provide them with a service. Typical Widgets are lights, speakers, temperature controls.

Widget communication protocol - The protocol used by the Widget to advertise its availability and services to the Nodes. Widget manufacturers are responsible for choosing which protocols each Widget supports. A typical Widget supports only one Widget communication protocol.

Widget driver - The software used by the Node to communicate with the Widget.
{% endraw %}
