import logging
import json
import xml.etree.ElementTree as ET
from urllib import request, parse
from urllib.error import HTTPError

logging.debug("Debug - SCRIPT is cucm_resolve")

maclookup = {}
server = {}
response = {}
properties = {}

# Get eyeConnect App PARAMS
maclookup["enabled"] = params["connect_cucm_lookupmac"]
maclookup["prefix"] = params["connect_cucm_macprefix"]
server["description"] = params["connect_cucm_displayname"]
server["url"] = params["connect_cucm_axl_url"]
additionalservers = params["connect_cucm_additionalservers"]
storedcookie = params.get("connect_authorization_token")
cookie = json.loads(params.get("connect_authorization_token"))

# Debug output to console
logging.debug("Debug - PARAMS [CUCM AXL API Url] is [{}]".format(params["connect_cucm_axl_url"]))
logging.debug("Debug - PARAMS [connect_authorization_token] is [{}]".format(params.get("connect_authorization_token")))
logging.debug("Debug - PARAMS [connect_authorization_token] type is [{}]".format(type(params.get("connect_authorization_token"))))
logging.debug("Debug - VARIABLE [storedcookie] is [{}]".format(storedcookie))
logging.debug("Debug - VARIABLE [storedcookie] type is [{}]".format(type(storedcookie)))
logging.debug("Debug - VARIABLE [cookie] is [{}]".format(cookie))
logging.debug("Debug - VARIABLE [cookie] type is [{}]".format(type(cookie)))

# Check if the additionalservers are enabled and if so set the url variables from the app PARAMS
if additionalservers == "true":
    server["additionalserverurl1"] = params["connect_cucm_additionalserver1"]
    server["additionalserverurl2"] = params["connect_cucm_additionalserver2"]
    server["additionalserverurl3"] = params["connect_cucm_additionalserver3"]
    server["additionalserverurl4"] = params["connect_cucm_additionalserver4"]


def cucm_hittheapi(thedevicerequest):
    ####################################
    #### QUERY THE API WITH PAYLOAD ####
    ####################################
    _devices_request = thedevicerequest
    _resp = None

    try:
        _resp = request.urlopen(_devices_request, context=ssl_context)
        logging.debug("Debug - Sent request [{}]".format(_devices_request))

        _current_status_code = _resp.getcode()

        if _resp.getcode() == 200:
            logging.debug("Debug - Success with status code [{}]".format(_current_status_code))
            _request_response = _resp.read().decode("utf-8")
            logging.debug("CUCM API Response: [{}]".format(_request_response))
            return _current_status_code, _request_response

    except HTTPError as e:
        _errorcontent = e.read()
        _errorcode = e.code
        message = "Debug - Unsuccessful with status code [{}] and message [{}].".format(_errorcode, _errorcontent)
        logging.debug(message)
        return _errorcode, _errorcontent


def cucm_additionalservers():
    ###################################
    #### CHECK ADDITIONAL SERVERS  ####
    ###################################
    logging.debug("Debug - FUNCTION is cucm_additionalservers")
    _noresult = ""

    # If starting the function after the primary server is checked, set the server type to Additional1 and run the function again
    if server["type"] == "primary":
        if server["additionalserverurl1"]!="":
            server["type"] = "additional1"
            _code, _props = cucm_getonesystem()
            if _code == 200:
                return _code, _props
            elif _code == 500:
                if server["additionalserverurl2"]!="":
                    server["type"] = "additional2"
                    _code, _props = cucm_getonesystem()
                    if _code == 200:
                        return _code, _props
                    elif _code == 500:
                        if server["additionalserverurl3"]!="":
                            server["type"] = "additional3"
                            _code, _props = cucm_getonesystem()
                            if _code == 200:
                                return _code, _props
                            elif _code == 500:
                                if server["additionalserverurl4"]!="":
                                    server["type"] = "additional4"
                                    _code, _props = cucm_getonesystem()
                                    if _code == 200:
                                        return _code, _props
                                    elif _code == 500:
                                        _noresult = "notfound"
                                    else:
                                        _noresult = "error"
                                else:
                                    _noresult = "notfound"
                            else:
                                _noresult = "error"
                        else:
                            _noresult = "notfound"
                    else:
                        _noresult = "error"
                else:
                    _noresult = "notfound"
            else:
                _noresult = "error"
        else:
            _noresult = "notfound"

    # If _noresult is true then set the phone as registered false and clear the other properties
    if _noresult == "notfound":
        logging.debug("Debug - Phone Lookup Unsuccessful with status code [{}]".format(_code))
        logging.debug("Debug - Attempted Phone Name was [{}]".format(hostname))
        logging.debug("Debug - Server URL was [{}]".format(server["url"]))
        properties["connect_cucm_serverdescription"] = ""
        properties["connect_cucm_serverurl"] = ""
        properties["connect_cucm_serverrole"] = ""
        properties["connect_cucm_querymethod"] = ""
        properties["connect_cucm_registered"] = "false"
        properties["connect_cucm_name"] = ""
        properties["connect_cucm_description"] = ""
        properties["connect_cucm_product"] = ""
        properties["connect_cucm_model"] = ""
        properties["connect_cucm_class"] = ""
        properties["connect_cucm_loadinformation"] = ""
        response["properties"] = properties
        return _code, properties
    elif _noresult == "error":
        logging.debug("Debug - Phone Lookup Unsuccessful with status code [{}]".format(_code))
        logging.debug("Debug - Attempted Phone Name was [{}]".format(hostname))
        logging.debug("Debug - Server URL was [{}]".format(server["url"]))
        return _code, "ERROR"


def cucm_getonesystem():
    #########################
    #### GET ONE SYSTEM  ####
    #########################
    logging.debug("Debug - FUNCTION is cucm_getonesystem")

    #_serverurl = "%s/" % server["url"]
    _servertype = server["type"]
    logging.debug("Debug - VARIABLE [_servertype] is [{}]".format(_servertype))

    if _servertype == "primary":
        _serverurl = '{}/'.format(server["url"])
    elif _servertype == "additional1":
        _serverurl = '{}/'.format(server["additionalserverurl1"])
    elif _servertype == "additional2":
        _serverurl = '{}/'.format(server["additionalserverurl2"])
    elif _servertype == "additional3":
        _serverurl = '{}/'.format(server["additionalserverurl3"])
    elif _servertype == "additional4":
        _serverurl = '{}/'.format(server["additionalserverurl4"])

    logging.debug("Debug - VARIABLE [_serverurl] is [{}]".format(_serverurl))

    _storedcookie = cookie[_servertype]
    logging.debug("Debug - VARIABLE [_storedcookie] is [{}]".format(_storedcookie))
    logging.debug("Debug - VARIABLE [_storedcookie] type is [{}]".format(type(_storedcookie)))
    #_split_cookie1 = _storedcookie[0].split(';')
    #_split_cookie2 = _storedcookie[1].split(';')
    #_cookie = _split_cookie1[0] + "; " + _split_cookie2[0]
    _cookie = _storedcookie[0]
    logging.debug("Debug - VARIABLE [_cookie] is [{}]".format(_cookie))
    logging.debug("Debug - VARIABLE [_cookie] type is [{}]".format(type(_cookie)))

    _headers = {
        'Content-Type': "text/xml",
        'charset': 'utf-8',
        'User-Agent': "FSCT/9.16.2020",
        'Accept': "*/*",
        'SOAPAction': 'CUCM:DB ver=10.5 getPhone',
        'Cookie': _cookie
        }
    logging.debug("Debug - VARIABLE [headers] is [{}]".format(_headers))

    _payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/10.5">
                    <soapenv:Header/>
                    <soapenv:Body>
                        <ns:getPhone>
                            <name>""" + hostname + """</name>
                        </ns:getPhone>
                    </soapenv:Body>
                </soapenv:Envelope>"""

    logging.debug("Debug - VARIABLE [payload] is [{}]".format(_payload))

    _devices_request = request.Request(_serverurl, headers=_headers, data=bytes(_payload, encoding="utf-8"))

    logging.debug("Debug - Attempting to send request [{}] to URL [{}]".format(_devices_request, _serverurl))
    _code, _req_response = cucm_hittheapi(_devices_request)

    if _code == 200:
        _xml_response = ET.fromstring(_req_response)
        logging.debug("Debug - VARIABLE [xml_response] is [{}]".format(_xml_response))

        logging.debug("Debug - CUCM Get Phone Result:")
        for child in _xml_response[0][0][0]:
            if child is not None:
                    logging.debug("Debug - Server Description is [{}]".format(server['description']))
                    logging.debug("Debug - Server URL is [{}]".format(_serverurl))
                    logging.debug("Debug - Server Role is [{}]".format(_servertype))
                    logging.debug("Debug - Query Method is [{}]".format(server['querymethod']))
                    logging.debug("Debug - Phone Name is [{}]".format(child[0].text))
                    logging.debug("Debug - Description is [{}]".format(child[1].text))
                    logging.debug("Debug - Product is [{}]".format(child[2].text))
                    logging.debug("Debug - Model is [{}]".format(child[3].text))
                    logging.debug("Debug - Class is [{}]".format(child[4].text))
                    logging.debug("Debug - Load Information is [{}]".format(child[18].text))
                    properties["connect_cucm_serverdescription"] = server['description']
                    properties["connect_cucm_serverurl"] = _serverurl
                    properties["connect_cucm_serverrole"] = _servertype
                    properties["connect_cucm_querymethod"] = server['querymethod']
                    properties["connect_cucm_registered"] = "true"
                    properties["connect_cucm_name"] = child[0].text
                    properties["connect_cucm_description"] = child[1].text
                    properties["connect_cucm_product"] = child[2].text
                    properties["connect_cucm_model"] = child[3].text
                    properties["connect_cucm_class"] = child[4].text
                    properties["connect_cucm_loadinformation"] = child[18].text
                    return _code, properties
    elif _code == 401 or _code == 500:
        if additionalservers == "true":
            if _servertype == "primary":
                logging.debug("Debug - Additonal Servers is set to True, will attempt lookup with the Additional Servers")
                _code_, _props_ = cucm_additionalservers()
                return _code_, _props_
            else:
                return _code, _req_response
        else:
            if _code == 500:
                logging.debug("Debug - Phone Lookup Unsuccessful with status code [{}] and error [{}]".format(_code, _req_response))
                logging.debug("Debug - Attempted Phone Name was [{}]".format(hostname))
                logging.debug("Debug - Server URL was [{}]".format(_serverurl))
                properties["connect_cucm_serverdescription"] = ""
                properties["connect_cucm_serverurl"] = ""
                properties["connect_cucm_serverrole"] = ""
                properties["connect_cucm_querymethod"] = ""
                properties["connect_cucm_registered"] = "false"
                properties["connect_cucm_name"] = ""
                properties["connect_cucm_description"] = ""
                properties["connect_cucm_product"] = ""
                properties["connect_cucm_model"] = ""
                properties["connect_cucm_class"] = ""
                properties["connect_cucm_loadinformation"] = ""
                return _code, properties
            else:
                logging.debug("Debug - Phone Lookup Unsuccessful with status code [{}] and error [{}]".format(_code, _req_response))
                return _code, _req_response
    else:
        logging.debug("Debug - Phone Lookup Unsuccessful with status code [{}] and error [{}]".format(_code, _req_response))
        return _code, _req_response


#####################################
# Resolution process kicks off here #
#####################################

#Check if dhcp_hostname_v2 is present for the phone
if "dhcp_hostname_v2" in params and params["dhcp_hostname_v2"]!="":
    hostname = params["dhcp_hostname_v2"]
    logging.debug("Debug - PARAMS [host_name] is using dhcp_hostname_v2 [{}]".format(hostname))
    server["querymethod"] = "DHCP Hostname"
    server["type"] = "primary"
    code, props = cucm_getonesystem()
    if code == 200:
        response["properties"] = props
        response["succeeded"] = True
    elif code == 500:
        response["properties"] = props
        response["succeeded"] = True
    else:
        message = "Debug - Failed to process the request and got code [{}] and error [{}]".format(code, props)
        logging.debug(message)
        response["troubleshooting"] = message
        response["succeeded"] = False
# If dhcp_hostname_v2 is Null and MAC Lookup is enabled then use the MAC Address to search for the phone
elif maclookup["enabled"] == "true":
    mac = params["mac"]
    uppermac = mac.upper()
    hostname = '{}{}'.format(maclookup["prefix"], uppermac)
    logging.debug("Debug - PARAMS [host_name] is using MAC [{}]".format(hostname))
    server["querymethod"] = "MAC Address"
    server["type"] = "primary"
    code, props = cucm_getonesystem()
    if code == 200:
        response["properties"] = props
        response["succeeded"] = True
    elif code == 500:
        response["properties"] = props
        response["succeeded"] = True
# If dhcp_hostname_v2 is Null and MAC Lookup is disabled then we cannot lookup the phone
else:
    message = "Debug - DHCP Hostname is Null and MAC Lookup is Disabled so PARAMS [host_name] is blank - we cannot lookup the phone"
    logging.debug(message)
    response["troubleshooting"] = message
    response["succeeded"] = False
