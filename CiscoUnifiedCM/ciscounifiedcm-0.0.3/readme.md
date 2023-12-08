# CUCM 0.0.3

eyeExtend Connect App for Cisco Unified Call Manager (CUCM) - Check for registered endpoints and gather properties from the CUCM AXL API.


## About the eyeExtend Connect App for Cisco Unified Call Manager (CUCM)
---
This app provides the following information from a registered endpoint (voip) in CUCM:

- Class
- Description
- Load Information
- Model
- Name
- Product


## Customer Support
---
The Connect Plugin is supported by Forescout Customer Support. See https://forescout.force.com/support/s/.

Connect Apps, including those provided by Forescout, are not supported by Forescout.


## Requirements
---
The app has been developed and tested with the following versions (it may work on others but testing has not been conducted):

- Forescout 8.2.2.x
- eyeExtend Connect Plugin 2.0.1
- Cisco Unified Call Manager (CUCM) 10.5

The app is likely to work on other versions (especially later releases) however it has not been tested and verified.


## Versions
---
- 0.0.1:
	- Initial Version
- 0.0.2:
	- Added app configuration setting to allow MAC Lookup if the DHCP Hostname is not available
 	- Added app configuration setting to set the prefix for MAC Lookup if it is enabled (eg, SEPxxxxxxxxxxxx)
- 0.0.3:
 	- Added additional endpoint property "Registered"
	- Added additional endpoint property "Server Description"
	- Added additional endpoint property "Server URL"
	- Added additional endpoint property "Server Role"
	- Added additional endpoint property "Query Method"
 	- Updated Policy Template to check for "CUCM - Registered" matches "true" for sub-rule "Registered"
	- Updated Policy Template to check for "CUCM - Registered" matches "false" for sub-rule "NOT Registered"
	- Updated Policy Template to include Scope for Member of Group "P-VoIP Devices"
	- Added app configuration setting "Enable Additional Servers" to allow lookup of an endpoint on other servers that share the same credentials as the "primary" server
	- Added app configuration setting "Additional Server 1" 
	- Added app configuration setting "Additional Server 2" 
	- Added app configuration setting "Additional Server 3" 
	- Added app configuration setting "Additional Server 4" 
	- Added app configuration setting "Rauth every x mins) which uses the Authentication script to reauth every x mins and save cookies (to be used when lookup occurs rather than reauthenticate every time)
	- Added app configuration setting to check for SSL Certificate Verification
	- Added ability to authenticate with primary and additional servers using the same credentials and store cookies for each
	- Added ability to store the cookie for the primary server in the Connect PARAM "token" 
	- Added ability to store the cookies for additional servers in the Connect PARAM "token"
	- Added code to check for HTTP 500 and set "CUCM - Registered" to "false" if not found
	- Added script cucm_auth.py to use integrated functions of eyeExtend Connect that allow Authentication Refresh on an interval
	- Added script cucm_resolve.py to use integrated functions of eyeExtend Connect that allow query of endpoint properties when the endpoint property is referenced in a policy or action
	- Moved all code from cucm_auth function in cucm_library to script cucm_auth.py
	- Moved all code from cucm_getonesystem function in cucm_library to script cucm_resolve.py
	- Removed cucm_library from the app as it was no longer required
	- Added icons to the Right Click Actions for Action Group "CUCM"
	- Added additional error handling for when a device is not found and/or an unexpected response is received from the server
	- Added process to blank out "CUCM - xxx" properties if the endpoint is not found on the primary or any additional servers
	

## App Configuration
---
The following sections outline the configuration required when setting up the app:

### Server URL
The URL of the CUCM AXL API is required (eg, https://servername.fqdn:8443/axl)

### Username/Password
Username and Password configured in the API is required.

### Authorization Refresh interval
How often we want to authentication with the server(s) and refresh the cookies.

### Verify server certificate
Verify the SSL Certificate of the server provided or not.

### Additional Servers
If additional servers are provided the same username/password will be used to authenticate with these servers. If an endpoint is not found on the primary server during lookup, the additional servers will be checked one-by-one until a result is found.


## Actions
---
One action is provided (as below) which can used used with manual right Click actions or by adding as an Action to a policy. Both are available under the Action Group titled "CUCM".

- Get System Details


## Policy Templates
---
A policy template is provided with the app titled "Get CUCM System Details" and is scoped to Member of Group (P-VoIP Devices) by default.

The policy will use the check the value CUCM - Registered on each endpoint and will fall into the sub-rules in according with the below values:

- true = Registered
- false = NOT Registered
- Null or Irresolvable = Unable to Obtain


## New Features Still To Be Added
---
Thw following features will be added in coming versions:

- Remove any blank properties rather than having them set to ""
- Add Policy Template statement about the additional properties (those not collected from the API) but rather created by the script for information purposes about the server the endpoint was found on
- Add app setting for Query Rate Limit
