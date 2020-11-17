## Query properties for a single endpoint

import requests # Supported in Connect v1.8+

# Setup
sophos_id = params["connect_sophos_id"]
properties = {}

try:
	## Ensure we have a Sophos Central ID for this endpoint
	assert sophos_id is not None and sophos_id != ''

	## Check if the authorization script has run
	if "connect_authorization_token" in params:
		jwt_token = params["connect_authorization_token"]
		logging.debug("Got access_token from auth script")
	else:
		## Get the access token
		url = "https://id.sophos.com/api/v2/oauth2/token"

		## Setup
		payload = "grant_type=client_credentials&client_id=" + params["connect_sophos_client_id"] + "&client_secret=" + params["connect_sophos_client_secret"] + "&scope=token"
		headers = {
	  		'Content-Type': 'application/x-www-form-urlencoded'
		}
		resp = requests.request("POST", url, headers=headers, data = payload)
		resp.raise_for_status()

		jwt_token = resp.json()['access_token']
		logging.debug("Got access token in poll script")

	## Get tenant ID and data region
	url = "https://api.central.sophos.com/whoami/v1"

	headers = {
	  'Authorization': 'Bearer ' + jwt_token
	}

	response = {}

	logging.debug("Beginning Poll")

	resp = requests.get(url, headers=headers)
	resp.raise_for_status()

	tenant_id = resp.json()['id']
	data_region = resp.json()['apiHosts']['dataRegion']

	## Second request: List endpoints
	headers['X-Tenant-ID'] = tenant_id
	url = data_region + "/endpoint/v1/endpoints/" + sophos_id

	resp = requests.get(url, headers=headers)
	resp.raise_for_status()

	## Parse endpoints returned
	item = resp.json()

	# Common properties
	#logging.debug("Processing: " + item["hostname"])
	properties["connect_sophos_ip4_addresses"] = item["ipv4Addresses"]
	properties["connect_sophos_hostname"] = item["hostname"]
	properties["connect_sophos_is_server"] = item["os"]["isServer"]
	properties["connect_sophos_os_platform"] = item["os"]["platform"]
	properties["connect_sophos_associatedperson_login"] = item["associatedPerson"]["viaLogin"]

	# Optional properties
	if ("macAddresses" in item) :
		macs = []
		for mac in item["macAddresses"] :
			macs.append(mac.replace(":", "").lower())
		properties["connect_sophos_mac_addresses"] = macs

	if ("ipv6Addresses" in item) :
		properties["connect_sophos_ip6_addresses"] = item["ipv6Addresses"]

	if ("name" in item["os"]) :
		properties["connect_sophos_os_name"] = item["os"]["name"]

	if ("name" in item["associatedPerson"]) :
		properties["connect_sophos_associatedperson_name"] = item["associatedPerson"]["name"]

	if ("health" in item) :
		properties["connect_sophos_health_overall"] = item["health"]["overall"]
		properties["connect_sophos_health_service"] = item["health"]["services"]["status"]

	if ("tamperProtectionEnabled" in item) :
		properties["connect_sophos_tamperprotection"] = item["tamperProtectionEnabled"]
		
except ConnectionError as e:
	logging.debug("Conenction Error: {}".format(str(e)), exc_info=True)
	response["error"] = "Failed to resolve. {}".format(str(e))

except AssertionError as e:
	logging.debug("Attempted to resolve with no Sophos ID")
	response["error"] = "Failed to resolve. {}".format(str(e))

except Exception as e:
	logging.debug("Error: {}".format(str(e)), exc_info=True)
	response["error"] = "Failed to resolve. {}".format(str(e))

finally:
	response['properties'] = properties

#logging.debug("Returning resolve response object to infrastructure. response=[{}]".format(response))

