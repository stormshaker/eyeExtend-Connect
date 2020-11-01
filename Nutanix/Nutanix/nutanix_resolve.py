'''
Copyright © 2020 Forescout Technologies, Inc.
 
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from urllib.request import HTTPError, URLError
import base64

# Mapping between Nutanix API response fields to CounterACT properties
nutanix_to_forescout_props_map = {
    "description": "connect_nutanix_description",
    "name": "connect_nutanix_name",
    "power_state": "connect_nutanix_power_state"
}

# Config
nu_url = "https://" + params["connect_nutanix_cluster"] + ":9440/api/nutanix/v3/vms/" + params["connect_nutanix_uuid"]
nu_user = params["connect_nutanix_admin_user"] 
nu_pass = params["connect_nutanix_admin_password"]

## Setup request
request = urllib.request.Request(nu_url)
request.add_header("Content-Type", "application/json")

## Add auth
# TODO: move this to an auth script?
credentials = ('%s:%s' % (nu_user, nu_pass))
encoded_credentials = base64.b64encode(credentials.encode('ascii'))
request.add_header('Authorization', 'Basic %s' % encoded_credentials.decode("ascii"))

## Request
try:
	resp = urllib.request.urlopen(request, context=ssl_context)
	json_resp = json.loads(resp.read())
	logging.debug("Request: {}".format(str(nu_url)))

	## Process the response
	logging.debug("Response: {}".format(str(json_resp)))
	properties = {}
	response["properties"] = properties

except HTTPError as e:
	logging.debug("HTTPError: {}".format(str(e)))
	response["error"] = "Failed to poll. Response code: {}".format(e.code)
except URLError as e:
	logging.debug("URLError: {}".format(str(e)))
	response["error"] = "Failed to poll. {}".format(e.reason)
except Exception as e:
	logging.debug("Error: {}".format(str(e)), exc_info=True)
	response["error"] = "Failed to poll. {}".format(str(e))

logging.debug("Returning response object to infrastructure. response=[{}]".format(response))
