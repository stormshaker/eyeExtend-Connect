## Connect to Sophos Cloud using the auth API and ensure that an access token can be retrieved

import requests # Supported in Connect v1.8+

url = "https://id.sophos.com/api/v2/oauth2/token"

## Setup
payload = "grant_type=client_credentials&client_id=" + params["connect_sophos_client_id"] + "&client_secret=" + params["connect_sophos_client_secret"] + "&scope=token"
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = {}
jwt_token = ""

## Request
try:
	resp = requests.request("POST", url, headers=headers, data = payload)
	resp.raise_for_status()

	jwt_token = resp.json()['access_token']

except ConnectionError as e:
	logging.debug("Conenction Error: {}".format(str(e)), exc_info=True)
	response["error"] = "Failed to authenticate. {}".format(str(e))

except Exception as e:
	logging.debug("Error: {}".format(str(e)), exc_info=True)
	response["error"] = "Failed to authenticate. {}".format(str(e))

## Response back to Forescout
finally:
	if (jwt_token != "") :
		response["succeeded"] = True
		response["result_msg"] = "Successfully connected to Sophos Central."
	else:
		response["succeeded"] = False
		response["result_msg"] = "Could not connect to Sophos Central."
