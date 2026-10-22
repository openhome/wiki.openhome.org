---
title: "OhRemote"
permalink: "/wiki/OhRemote"
redirect_from:
---

{% raw %}
# <span id="ohRemote"></span>ohRemote

ohRemote provides the set of server components used to access ohOs apps from outside the home.

#### <span id="Simple_for_an_end_user_to_set_up_and_use"></span>Simple for an end user to set up and use

It has been designed to be trivial for end users to setup and use. All communications are routed through a central server, avoiding any requirement for users to learn about port forwarding, static external IP addresses, or setup firewall rules to allow incoming http connections etc.

#### <span id="Cheap_to_host"></span>Cheap to host

Secondly, it has been designed so that the central server can be inexpensive for Node manufacturers to host. It is intended that tens of thousands of clients (homes) can be accommodated by a single server. When user numbers grow beyond this or the geographical spread of users makes a single server a bottleneck, minimal work will allow any number of additional servers to be deployed.

In addition to the software in ohRemote, remote access requires some additional features in [ohOs](/wiki/OhOs). These are also described below.

## <span id="How_do_I_get_it.3F"></span>How do I get it?

[Source code](https://github.com/openhome/ohremote) is available to selected partners. OpenHome also maintain a demo server. Contact info@openhome.org if you require access to either.

## <span id="System_Architecture"></span>System Architecture

<figure>
<img src="/mediawiki/images/3/32/RemoteAccessOverview.png" title="RemoteAccessOverview.png" width="800" alt="RemoteAccessOverview.png" />
<figcaption aria-hidden="true">RemoteAccessOverview.png</figcaption>
</figure>

The server contains the following components:

- [Stunnel](http://www.stunnel.org/) – a SSL tunnel which allows secure communications between user/node and the server without server components having to understand SSL.
- A reverse proxy server – [HaProxy](http://haproxy.1wt.eu/). This directs web requests to the correct server component.
- Web server, provided by [Node.js](http://nodejs.org/)
- Web services, implemented using [Node.js](http://nodejs.org/)
- SSH server, provided by [dropbear](http://matt.ucc.asn.au/dropbear/dropbear.html)
- Client authentication – a [pluggable authentication module](http://en.wikipedia.org/wiki/Pluggable_authentication_module) used by the ssh server when deciding whether to accept a connection request from a Node.
- Databases, provided by [MySQL](http://www.mysql.com)

The Node contains the following components:

- Standard node software
- Provider for RemoteAccess UPnP service
- Remote access settings registry (currently combined with provider). This stores username, password, user-facing control url & node-facing web services url
- Proxy server. This connects to the remote access server’s ssh server and listens for requests, forwarding them to the appropriate locations on the standard node web server. The proxy server uses standard .NET classes – `HttpListener` for the server and `HttpWebRequest` to forward requests.

The remote client contains the following components:

- Any web browser supported by the Node UI.

## <span id="Use_cases"></span>Use cases

To aid understanding of the architecture diagram, key use cases for the system are described below.

### <span id="Register_new_Node"></span>Register new Node

- User brings up their Node UI inside the home
- User enters desired username & password
- Provider for RemoteAccess service is called for `SetUserName` action
- Provider calls `register` web service
- Registration web service on remote access server is called (via Stunnel then HaProxy)
- If requested username is available, registration service adds a record to the Login Database. Otherwise, it generates a list of similar usernames which are still available and returns this as part of an error.
- Assuming registration succeeded, Username is added to remote access registry. `SetUserName` action returns success.
- UI calls `SetPassword` action. Password is added to remote access registry and action returns success.
- UI calls `SetEnable` action. Enabled state is set in remote access registry. Enabling remote access is then covered by the next use case...

### <span id="Connect_a_registered_Node"></span>Connect a registered Node

- Happens either when `SetEnable` action is called or ohOs starts when remote access was previously enabled.
- Provider for RemoteAccess service calls `getaddress` on Node Login service (via Stunnel then HaProxy)
- Node Login service checks that node has been previously registered (by checking for node’s udn in Login Database). If the node is unregistered, an error is returned.
- Node Login service calls Port Finder service to determine which port of the ssh server the node should connect to.
- Port Finder service determines a free port. Node Login service writes node udn, ssh server address & port, plus status (pending) to the Session Database.
- Node Login service checks config file to determine ssh server host name & port (used for connecting to the ssh server) plus the IP address to bind to for remote port forwarding. These 3 details plus the port determined above are returned to the home node.
- Home node now has approx 1 minute to connect to the ssh server. The Node Login service periodically checks the Session Database and removes records that have been pending for longer than 1 minute.
- Home node starts its proxy server. This is currently hard-coded to listen on port 55170.
- Home node connects to ssh server. Server uses PAM SQL Lookup to validate ssh key used in connection request against key in Login Database. Server then changes status of node’s record in Session Database to ‘connected’.
- Home node sets up remote port forwarding for the port its proxy server is listening on.

### <span id="User_connects_remotely"></span>User connects remotely

- User enters the url returned by the node registration process into their web browser.
- This reaches the Login web service (via Stunnel and HaProxy).
- The url path is the user name that was selected during registration. Login service looks this up in Login Database and redirects the request to HaProxy with the path changed to the node udn which matches the username.
- HaProxy uses the node udn to look up ssh server address/port in the Session Database.
- HaProxy forwards the request to the appropriate address/port on the ssh server.
- Ssh server forwards the request to the appropriate proxy server on a home node.
- Home node checks for the presence of a login cookie in the request. If this is missing, the request is redirected to a login page hosted by the home node.
- When the first request completes, HaProxy sets a session cookie noting the udn for this user.
- The user’s web browser displays the login page prompting for username and password. The results from this are sent to the home node’s proxy server which checks them against the data in its remote access registry. If the login is valid, another session cookie is set and the user is redirected to the root of the home node’s proxy server.
- The user’s web browser issues a GET request for ‘/’. HaProxy uses its cookie to find the correct ssh server address/port. (This may come from either the session database or an in-memory cache.) The home node’s proxy server manually forwards the request to the web server home UIs are available from, applying minor rewrites (such as compression) to the response.

## <span id="Deployment"></span>Deployment

### <span id="Server"></span>Server

All configuration options are contained in the file `ohremote/scripts/config`.  
Hosting the server on a box with 2 IP addresses is recommended. This allows both the ssh server and web services to operate on port 443. This port is used by https so is likely to be open for outbound requests on most firewalls. (An argument could be made for port 80 – as used by http. This is at least as likely to be open on firewalls but is more likely to be subject to packet inspection and blocked as our use here will appear different to traditional web access.)

### <span id="Node"></span>Node

The location of the remote access server must be set in the `remote-access-server` tag of `ohos.ohconfig.xml`. This file is generated from `ohOs/src/Host/Host.ohconfig.xml.template` during a build or the generated file can be edited and ohOs restarted to apply changes.  
The Node must be capable of generating a RSA format SSH key. This is currently only supported on Linux; other platforms need to manually generate the keys and move them (named key.priv & key.pub) to the remote directory in ohWidget’s store.

## <span id="Monitoring"></span>Monitoring

### <span id="Server_2"></span>Server

Every 3 seconds, checks status of each component, restarting server if any component does not respond correctly. See `ohremote/scripts/ohmonitor` for details.

### <span id="Node_2"></span>Node

Every 5 minutes, issues a `HEAD` request to the user-facing uri returned by register web service (and then stored in registry). If this fails, disconnects from ssh server, stops (local) proxy server then repeats “Connect a registered node” use case. If connection fails, it is retried at randomised (but increasing) intervals thereafter.

## <span id="APIs"></span>APIs

### <span id="Server_Web_Services"></span>Server Web Services

**1. To register for remote access, including selecting a username**

`URL:  [server_url]/register`  
`Body:`  
`   `\<register\>  
`       `\<username\>`[Proposed username]`\</username\>  
`       `\<uidnode\>`[Node’s UDN]`\</uidnode\>  
`       `\<sshkey\>`[Contents of public key]`\</sshkey\>  
`   `\</register\>

Returns (success):

`   `\<result\>  
`       `\<success\>`[Proposed username]`\</success\>  
`   `\</result\>

Returns (failure):

`   `\<result\>  
`       `\<error\>`Username exists`\</error\>  
`       `\<suggestionlist\>  
`           `\<suggestion\>`First suggested free name`\</suggestion\>  
`           `\<suggestion\>`Second suggested free name`\</suggestion\>  
`           `\<suggestion\>`etc.`\</suggestion\>  
`       `\</suggestionlist\>  
`   `\</result\>

**2. To clear an account - (deregister interest in remote access, remove username)**

`URL:  [server_url]/remove`  
`Body:`  
`   `\<remove\>  
`       `\<uidnode\>`[Node’s UDN]`\</uidnode\>  
`   `\</remove\>

Returns (success):

`   `\<result\>  
`       `\<success\>`[Node’s UDN]`\</success\>  
`   `\</result\>

Returns (failure):

`   `\<result\>  
`       `\<error\>`[Error Message]`\</error\>  
`   `\</result\>

**3. To get connection details for the ssh tunnel**

`URL:  [server_url]/getaddress`  
`Body:`  
`   `\<getaddress\>  
`       `\<uidnode\>`[Node’s UDN]`\</uidnode\>  
`   `\</getaddress\>

Returns (success):

`   `\<result\>  
`       `\<success\>  
`           `\<sshserver\>  
`               `

\<address\>

\[Ssh server host (or address)\]

\</address\>

`               `\<port\>`[Ssh server port to connect to]`\</port\>  
`           `\</sshserver\>  
`           `\<portforward\>  
`               `

\<address\>

\[Address for remote port forwarding\]

\</address\>

`               `\<port\>`[Port for remote port forwarding]`\</port\>  
`           `\</portforward\>  
`       `\</success\>  
`   `\</result\>

Returns (failure):

`   `\<result\>  
`       `\<error\>`[Error Message]`\</error\>  
`   `\</result\>

### <span id="Node_web_service"></span>Node web service

As with other Node features, this is available as a UPnP service - openhome-org:service:RemoteAccess:1.

#### <span id="State_variables"></span>State variables

- `Enabled`  
  `true` if remote access is currently enabled; `false` otherwise.
- `PasswordSet`  
  `true` if a password is currently set; `false` otherwise. (Note that the password itself cannot be queried.)
- `PublicUri`  
  The url used for remote access. This is set once a Node has registered for remote access. The value does not change when `Enabled` changes.
- `UserName`  
  The username selected during registration; or `""` if the Node is not registered for remote access.

#### <span id="Actions"></span>Actions

- `SetUserName(in uint Handle, in string UserName, out bool Succeeded, out string AlternativeNames)`  
  Register a Node for remote access, selecting its unique username. Arguments are:
  - *`Handle`*`:`Reserved for future compatability. Must be 0.
  - *`UserName`*`:`Proposed username.
  - *`Succeeded`*`:``true` if `UserName` was available; `false` otherwise.
  - *`AlternativeNames`*`:`XML block in the same form as `suggestionlist` block from `register` web service.
- `SetPassword(int uint Handle, in string Password)`  
  Set a password used to authenticate remote connection requests. Arguments are:
  - *`Handle`*`:`Reserved for future compatability. Must be 0.
  - *`Password`*`:`Password. This is held locally on the Node so is guaranteed to be valid.
- `Enable(bool Enable)`  
  Enable remote access. This can only be called when a valid username and password are set. i.e. When the `UserName` state variable is non-empty and the `PasswordSet` state variable is `true`. Arguments are:
  - *`Enable`*`:``True` if remote access should be enabled; `false` if it is currently enabled and should be disabled.
- `Reset(uint Handle)`  
  Disable remote access, remove registration with remote access server and clear local username and password.
- `ClearAuthenticatedClients()`  
  Force any active remote access sessions to re-authenticate.
{% endraw %}
