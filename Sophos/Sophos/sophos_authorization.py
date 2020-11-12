## Use the newly-supported requests library
import requests

url = "https://id.sophos.com/api/v2/oauth2/token"

## Setup
payload = "grant_type=client_credentials&client_id=" + params["connect_sophos_client_id"] + "&client_secret=" + params["connect_sophos_client_secret"] + "&scope=token"
headers = {
  'Content-Type': 'application/x-www-form-urlencoded'
}

response = {}

## Request
try:
	resp = requests.request("POST", url, headers=headers, data = payload)

	if (resp.getcode() == 200) :
		jwt_token = resp.json()['access_token']
		response["token"] = jwt_token
	else:
		response["token"] = ""
		
except HTTPError as e:
	logging.debug("HTTPError: {}".format(str(e)))
	response["error"] = "Failed to authenticate. Response code: {}".format(e.code)
except URLError as e:
	logging.debug("URLError: {}".format(str(e)))
	response["error"] = "Failed to poll. {}".format(e.reason)
except Exception as e:
	logging.debug("Error: {}".format(str(e)), exc_info=True)
	response["error"] = "Failed to authenticate. {}".format(str(e))
