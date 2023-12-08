import base64
import logging
import json
from urllib import request, parse
from urllib.error import HTTPError

logging.debug("Debug - SCRIPT is cucm_auth")

credentials = {}
server = {}
response = {"token": ""}
CookieString = {
    "primary": "",
    "additional1": "",
    "additional2": "",
    "additional3": "",
    "additional4": ""
}
logging.debug("Debug - JSON DATA [CookieString] cleared [{}]".format(CookieString))

credentials["username"] = params["connect_cucm_username"]
credentials["password"] = params["connect_cucm_password"]
server["url"] = params["connect_cucm_axl_url"]
additionalservers = params["connect_cucm_additionalservers"]

if additionalservers == "true":
    server["additionalserverurl1"] = params["connect_cucm_additionalserver1"]
    server["additionalserverurl2"] = params["connect_cucm_additionalserver2"]
    server["additionalserverurl3"] = params["connect_cucm_additionalserver3"]
    server["additionalserverurl4"] = params["connect_cucm_additionalserver4"]

logging.debug("Debug - PARAMS [Username] is [{}]".format(credentials["username"]))
logging.debug("Debug - PARAMS [CUCM AXL API Url] is [{}]".format(params["connect_cucm_axl_url"]))
logging.debug("Debug - PARAMS [Additional Servers] is [{}]".format(params["connect_cucm_additionalservers"]))
logging.debug("Debug - PARAMS [Additional Server 1] is [{}]".format(params["connect_cucm_additionalserver1"]))
logging.debug("Debug - PARAMS [Additional Server 2] is [{}]".format(params["connect_cucm_additionalserver2"]))
logging.debug("Debug - PARAMS [Additional Server 3] is [{}]".format(params["connect_cucm_additionalserver3"]))
logging.debug("Debug - PARAMS [Additional Server 4] is [{}]".format(params["connect_cucm_additionalserver4"]))
logging.debug("Debug - VARIABLE [server[url]] is [{}]".format(server["url"]))
logging.debug("Debug - VARIABLE [additionalservers] is [{}]".format(additionalservers))
logging.debug("Debug - VARIABLE [additionalserverurl1] is [{}]".format(server["additionalserverurl1"]))
logging.debug("Debug - VARIABLE [additionalserverurl2] is [{}]".format(server["additionalserverurl2"]))
logging.debug("Debug - VARIABLE [additionalserverurl3] is [{}]".format(server["additionalserverurl3"]))
logging.debug("Debug - VARIABLE [additionalserverurl4] is [{}]".format(server["additionalserverurl4"]))

def cucm_auth(credentials, server, role):
    ##########################
    ##### AUTHENTICATION #####
    ##########################
    logging.debug("Debug - FUNCTION is CUCM Authentication")

    _current_status_code = None
    if role == "primary":
        _server = server["url"]
    elif role == "additional1":
        _server = server["additionalserverurl1"]
    elif role == "additional2":
        _server = server["additionalserverurl2"]
    elif role == "additional3":
        _server = server["additionalserverurl3"]
    elif role == "additional4":
        _server = server["additionalserverurl4"]
        
    _serverurl = _server
    logging.debug("Debug - VARIABLE [_serverurl] is [{}]".format(_serverurl))

    _username = credentials["username"]
    _password = credentials["password"]
    logging.debug("Debug - VARIABLE [_username] is [{}]".format(_username))

    _role = role
    logging.debug("Debug - VARIABLE [_role] is [{}]".format(_role))

    _creds = "%s:%s" % (_username, _password)
    _encoded_creds = base64.b64encode(_creds.encode()).decode()
    logging.debug("Debug - VARIABLE [encoded_creds] is [Basic {}]".format(_encoded_creds))

    _headers = {
        'Content-Type': "text/xml",
        'charset': 'utf-8',
        'User-Agent': "FSCT/9.16.2020",
        'Accept': "*/*",
        'Authorization': "Basic %s" % _encoded_creds
        }

    _auth_request = request.Request(_serverurl, headers=_headers)

    logging.debug("Debug - Attemping to send CUCM Auth request to URL [{}]".format(_serverurl))
    _resp = request.urlopen(_auth_request, context=ssl_context)
    logging.debug("Debug - Sent request [{}] to URL [{}]".format(_auth_request, _serverurl))

    _request_response = _resp.read()
    _current_status_code = _resp.getcode()
    logging.debug("Debug - Response is [{}] with status code [{}]".format(_request_response, _current_status_code))

    if _resp.getcode() == 200:
        message = "Debug - Authorization with CUCM server using URL [{}] is successful. ".format(_serverurl)
        _set_cookie = _resp.info().get_all('Set-Cookie')
        logging.debug("Debug - VARIABLE [set_cookie] is [{}]".format(_set_cookie))
        #split_cookie1 = set_cookie[0].split(';')
        #split_cookie2 = set_cookie[1].split(';')
        #_cookie = split_cookie1[0] + "; " + split_cookie2[0]
        #logging.debug("Debug - VARIABLE [_cookie] is [{}]".format(_cookie))

        if _role == "primary":
            CookieString.update(primary=_set_cookie)
            logging.debug("Debug - JSON VALUE [CookieString[primary]] is [{}]".format(CookieString["primary"]))
        elif _role == "additional1":
            CookieString.update(additional1=_set_cookie)
            logging.debug("Debug - JSON VALUE [CookieString[additional1]] is [{}]".format(CookieString["additional1"]))
        elif _role == "additional2":
            CookieString.update(additional2=_set_cookie)
            logging.debug("Debug - JSON VALUE [CookieString[additional2]] is [{}]".format(CookieString["additional2"]))
        elif _role == "additional3":
            CookieString.update(additional3=_set_cookie)
            logging.debug("Debug - JSON VALUE [CookieString[additional3]] is [{}]".format(CookieString["additional3"]))
        elif _role == "additional4":
            CookieString.update(additional4=_set_cookie)
            logging.debug("Debug - JSON VALUE [CookieString[additional4]] is [{}]".format(CookieString["additional4"]))

        _Cookie_String = json.dumps(CookieString)
        logging.debug("Debug - JSON DATA [_CookieString] is [{}]".format(_Cookie_String))
        logging.debug("Debug - JSON DATA [_CookieString] type is [{}]".format(type(_Cookie_String)))

        response["token"] = _Cookie_String
        logging.debug("Debug - VARIABLE [response[token]] is [{}]".format(_Cookie_String))
        response["succeeded"] = True
        logging.debug("Debug - Success with status code [{}] and created Cookie".format(_current_status_code))
        return 200
    else:
        message = "Debug - Authorization with CUCM server using URL [{}] was NOT successful returning code [{}]".format(server["url"], client_code)
        response["succeeded"] = False
        response["troubleshooting"] = message


if additionalservers == "false":
    logging.debug("Debug - Going to try auth with Primary Server [{}]".format(server["url"]))
    cucm_auth(credentials, server, "primary")
    logging.debug("Debug - Additonal Servers is False, no other servers to auth with.")
elif additionalservers == "true":
    logging.debug("Debug - Going to try auth with Primary Server [{}]".format(server["url"]))
    cucm_auth(credentials, server, "primary")
    logging.debug("Debug - Additonal Servers is True, will try attempt auth with Additional Servers")
    if server["additionalserverurl1"]!="":
        logging.debug("Debug - Will try to auth with Additional Server 1 [{}]".format(server["additionalserverurl1"]))
        cucm_auth(credentials, server, "additional1")
    if server["additionalserverurl2"]!="":
        logging.debug("Debug - Will try to auth with Additional Server 2 [{}]".format(server["additionalserverurl2"]))
        cucm_auth(credentials, server, "additional2")
    if server["additionalserverurl3"]!="":
        logging.debug("Debug - Will try to auth with Additional Server 3 [{}]".format(server["additionalserverurl3"]))
        cucm_auth(credentials, server, "additional3")
    if server["additionalserverurl4"]!="":
        logging.debug("Debug - Will try to auth with Additional Server 4 [{}]".format(server["additionalserverurl4"]))
        cucm_auth(credentials, server, "additional4")
