---
title: "Av:Developer:CloudServer"
permalink: "/wiki/Av:Developer:CloudServer"
redirect_from:
---

{% raw %}
**UPnP in the Cloud – Control Point Discovery Technical Document**

Draft 1 (26th July 2011)

Current control points rely on SSDP discovery for a UPnP server to make its presence known, obviously this cannot function through the Internet so a way of specifying the server has to be provided by the user into the control point, at the same time the user can enter their credentials to ensure that they only have access to their content.

To keep it as simple as possible the user should type as little as possible, 3 pieces of information are required:

Server Address User ID Password

The user ID should only allow characters a-z and numbers 0-9, and be case independent.

The control point would take this information and put it into a standard device discovery URL, for example the following information is supplied:

- Sever Address: a.cloudupnp.com
- User ID: user1234
- Password: tuesday

For sake of preserving the security of passwords (which might be used elsewhere), the password is hashed through sha1 taking a hex representation of the result (in uppercase). The salt for the password is the username.

For the given user ID & password above: sha1(“user1234tuesday”) giving a result: 6A6B4062BB3289F4624343C5D0EA88493FB77A98

Constructed URL: <http://a.cloudupnp.com/user1234/6A6B4062BB3289F4624343C5D0EA88493FB77A98> /

From here the server returns a standard Device Descriptor XML (using port 80) with a special exception: returned SCPDURL / controlURL cannot be relative as required by the UPnP specification, instead an absolute URL is returned which uses an IP address (for renderers which cannot perform a DNS lookup).

An example returned SCPDURL might be:

100.1.23.56:33333/ContentDirectory/e48c8f12-64bd-1-2-123456789abc/scpd.xml?un=user1234&pwd=6A6B4062BB3289F4624343C5D0EA88493FB77A98

Where 100.1.23.56 is the IP address of the server (most likely a different IP address from a.cloudupnp.com), 33333 is the port that should be used and the URL contains a query embedded User ID and Password. If at a later date the user were to change their password, the URL given out by the Device Descriptor would change.

eventSubURL are blank (\<eventSubURL\>\</eventSubURL\>) as there is no eventing from the Internet.

Ideally a control point would list the cloud based service under available servers, once selected allowing for credentials to be entered. The control point must allow multiple servers to be added, each cloud based server might offer a different package. The icon for each service should be retrieved from the Device Descriptor XML, however when signing up a generic cloud icon could be used.
{% endraw %}
