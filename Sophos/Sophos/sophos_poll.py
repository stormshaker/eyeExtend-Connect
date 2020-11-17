## Query the list of endpoints and import properties

import requests # Supported in Connect v1.8+

try:
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
	endpoints = []

	logging.debug("Beginning Poll")

	resp = requests.get(url, headers=headers)
	resp.raise_for_status()

	tenant_id = resp.json()['id']
	data_region = resp.json()['apiHosts']['dataRegion']

	## Second request: List endpoints
	headers['X-Tenant-ID'] = tenant_id
	url = data_region + "/endpoint/v1/endpoints"

	resp = requests.get(url, headers=headers)
	resp.raise_for_status()

	## Parse endpoints returned
	for item in resp.json()['items'] :
		new_endpoint = {}

		# Try to put MAC first if available
		if ("macAddresses" in item) :
			new_endpoint["mac"] = item["macAddresses"][0].replace(":", "").lower()

		# IPv4 address should always be available
		new_endpoint["ip"] = item["ipv4Addresses"][0]
		properties = {}

		# Common properties
		#logging.debug("Processing: " + item["hostname"])
		properties["connect_sophos_id"] = item["id"]
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

		new_endpoint["properties"] = properties
		endpoints.append(new_endpoint)
		
except ConnectionError as e:
	logging.debug("Conenction Error: {}".format(str(e)), exc_info=True)
	response["error"] = "Failed to poll. {}".format(str(e))

except Exception as e:
	logging.debug("Error: {}".format(str(e)), exc_info=True)
	response["error"] = "Failed to poll. {}".format(str(e))

finally:
	response['endpoints'] = endpoints

#logging.debug("Returning poll response object to infrastructure. response=[{}]".format(response))

