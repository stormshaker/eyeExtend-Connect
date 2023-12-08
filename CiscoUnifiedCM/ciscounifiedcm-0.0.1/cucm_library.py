import ssl
import base64
import logging
import json
import xml.etree.ElementTree as ET
from urllib import request, parse
from urllib.error import HTTPError

def cucm_auth(credentials, server):
    ##########################
    ##### AUTHENTICATION #####
    ##########################
    logging.debug("Debug - FUNCTION is CUCM Authentication")

    _current_status_code = None
    _cookie = None
    _server = server["url"]
    _serverurl = _server
    logging.debug("Debug - VARIABLE [_serverurl] is [{}]".format(_serverurl))

    _username = credentials["username"]
    _password = credentials["password"]
    logging.debug("Debug - VARIABLE [_username] is [{}]".format(_username))

    creds = "%s:%s" % (_username, _password)
    encoded_creds = base64.b64encode(creds.encode()).decode()
    logging.debug("Debug - VARIABLE [encoded_creds] is [Basic {}]".format(encoded_creds))

    response = {}
    headers = {
        'Content-Type': "text/xml",
        'charset': 'utf-8',
        'User-Agent': "FSCT/9.16.2020",
        'Accept': "*/*",
        'Authorization': "Basic %s" % encoded_creds
        }

    auth_request = request.Request(_serverurl, headers=headers)

    logging.debug("Debug - Attemping to send CUCM Auth request to URL [{}]".format(_serverurl))
    context=ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context=ssl._create_unverified_context()

    resp = request.urlopen(auth_request, context=context)
    logging.debug("Debug - Sent request [{}] to URL [{}]".format(auth_request, _serverurl))

    request_response = resp.read()
    _current_status_code = resp.getcode()
    logging.debug("Debug - Response is [{}] with status code [{}]".format(request_response, _current_status_code))

    if resp.getcode() == 200:
        set_cookie = resp.info().get_all('Set-Cookie')
        logging.debug("Debug - Set-Cookie is [{}]".format(set_cookie))
        split_cookie1 = set_cookie[0].split(';')
        split_cookie2 = set_cookie[1].split(';')
        _cookie = split_cookie1[0] + "; " + split_cookie2[0]
        logging.debug("Debug - VARIABLE [_cookie] is [{}]".format(_cookie))

        logging.debug("Debug - Success with status code [{}] and created Cookie".format(_current_status_code))
    else:
        logging.debug("Debug - Unsuccessful with status code [{}]".format(_current_status_code))

    return _current_status_code, _cookie

def cucm_getallsystems(server, cookie):
    #########################
    #### GET ALL SYSTEMS ####
    #########################
    logging.debug("Debug - FUNCTION is CUCM Get All Systems")

    _cookie = cookie
    logging.debug("Debug - VARIABLE [_cookie] is [{}]".format(_cookie))

    _server = server["url"]
    _serverurl = "%s/" % _server
    logging.debug("Debug - VARIABLE [_serverurl] is [{}]".format(_serverurl))

    response = {}
    headers = {
        'Content-Type': "text/xml",
        'charset': 'utf-8',
        'User-Agent': "FSCT/9.16.2020",
        'Accept': "*/*",
        'SOAPAction': 'CUCM:DB ver=10.5 listPhone',
        'Cookie': "%s" % _cookie
        }

    payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/10.5">
                   <soapenv:Header/>
                   <soapenv:Body>
                      <ns:listPhone>
                         <searchCriteria>
                            <!--Optional:-->
                            <!--<name>SEP%</name>-->
                            <devicePoolName>Default</devicePoolName>
                         </searchCriteria>
                         <returnedTags>
                           <name></name>
                            <model></model>
                            <ownerUserName></ownerUserName>
                         </returnedTags>
                      </ns:listPhone>
                   </soapenv:Body>
                </soapenv:Envelope>"""
    logging.debug("Debug - VARIABLE [payload] is [{}]".format(payload))

    devices_request = request.Request(_serverurl, headers=headers, data=bytes(payload, encoding="utf-8"))

    context=ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context=ssl._create_unverified_context()

    logging.debug("Debug - Attempting to send request [{}] to URL [{}]".format(devices_request, _serverurl))
    resp = request.urlopen(devices_request, context=context)
    logging.debug("Debug - Sent request [{}] to URL [{}]".format(devices_request, _serverurl))

    _current_status_code = resp.getcode()

    if resp.getcode() == 200:
        logging.debug("Debug - Success with status code [{}]".format(_current_status_code))
        request_response = resp.read().decode("utf-8")
        logging.debug("Debug - CUCM API Response: [{}]".format(request_response))

        xml_response = ET.fromstring(request_response)
        logging.debug("Debug - VARIABLE [xml_response] is [{}]".format(xml_response))

        logging.debug("Debug - CUCM List Phones Result:")
        for child in xml_response[0][0][0]:
            if child is not None:
                    logging.debug("Debug - Name is [{}] with Description [{}]".format(child[0].text, child[1].text))

        _current_status_code = resp.getcode()
    else:
        logging.debug("Debug - Unsuccessful with status code [{}]".format(_current_status_code))

    return _current_status_code, request_response

def cucm_getonesystem(server, cookie, name):
    #########################
    #### GET ONE SYSTEM  ####
    #########################
    logging.debug("Debug - FUCTION is CUCM Get One System")

    _cookie = cookie
    logging.debug("Debug - VARIABLE [_cookie] is [{}]".format(_cookie))

    _server = server["url"]
    _serverurl = "%s/" % _server
    logging.debug("Debug - VARIABLE [_serverurl] is [{}]".format(_serverurl))

    _hostname = name
    logging.debug("Debug - VARIABLE [_name] is [{}]".format(_hostname))

    systemdetails = {}
    response = {}
    headers = {
        'Content-Type': "text/xml",
        'charset': 'utf-8',
        'User-Agent': "FSCT/9.16.2020",
        'Accept': "*/*",
        'SOAPAction': 'CUCM:DB ver=10.5 getPhone',
        'Cookie': "%s" % _cookie
        }

    payload = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://www.cisco.com/AXL/API/10.5">
                    <soapenv:Header/>
                    <soapenv:Body>
                        <ns:getPhone>
                            <name>""" + _hostname + """</name>
                        </ns:getPhone>
                    </soapenv:Body>
                </soapenv:Envelope>"""

    logging.debug("Debug - VARIABLE [payload] is [{}]".format(payload))

    devices_request = request.Request(_serverurl, headers=headers, data=bytes(payload, encoding="utf-8"))

    context=ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    context=ssl._create_unverified_context()

    logging.debug("Debug - Attempting to send request [{}] to URL [{}]".format(devices_request, _serverurl))

    try:
        resp = request.urlopen(devices_request, context=context)
        logging.debug("Debug - Sent request [{}] to URL [{}]".format(devices_request, _serverurl))

        _current_status_code = resp.getcode()

        if resp.getcode() == 200:
            logging.debug("Debug - Success with status code [{}]".format(_current_status_code))
            request_response = resp.read().decode("utf-8")
            logging.debug("CUCM API Response: [{}]".format(request_response))

            xml_response = ET.fromstring(request_response)
            logging.debug("Debug - VARIABLE [xml_response] is [{}]".format(xml_response))

            logging.debug("Debug - CUCM Get Phone Result:")
            for child in xml_response[0][0][0]:
                if child is not None:
                        logging.debug("Debug - Server URL is [{}]".format(_serverurl))
                        logging.debug("Debug - Phone Name is [{}]".format(child[0].text))
                        logging.debug("Debug - Description is [{}]".format(child[1].text))
                        logging.debug("Debug - Product is [{}]".format(child[2].text))
                        logging.debug("Debug - Model is [{}]".format(child[3].text))
                        logging.debug("Debug - Class is [{}]".format(child[4].text))
                        logging.debug("Debug - Load Information is [{}]".format(child[18].text))
                        systemdetails['registered'] = "true"
                        systemdetails['serverurl'] = _serverurl
                        systemdetails['name'] = child[0].text
                        systemdetails['description'] = child[1].text
                        systemdetails['product'] = child[2].text
                        systemdetails['model'] = child[3].text
                        systemdetails['class'] = child[4].text
                        systemdetails['loadinformation'] = child[18].text

        return _current_status_code, systemdetails

    except HTTPError as e:
        _errorcontent = e.read()
        _errorcode = e.code
        logging.debug("Debug - Error Content is [{}]".format(_errorcontent))
        if _errorcode == 500:
            logging.debug("Debug - Phone Lookup Unsuccessful with status code [{}]".format(_errorcode))
            logging.debug("Debug - Attempted Phone Name was [{}]".format(_hostname))
            logging.debug("Debug - Server URL was [{}]".format(_serverurl))
            systemdetails['registered'] = "false"
            systemdetails['serverurl'] = ""
            systemdetails['name'] = ""
            systemdetails['description'] = ""
            systemdetails['product'] = ""
            systemdetails['model'] = ""
            systemdetails['class'] = ""
            systemdetails['loadinformation'] = ""
            return _errorcode, systemdetails
        else:
            logging.debug("Debug - Unsuccessful with status code [{}]".format(_errorcode))
            logging.debug("Debug - Exiting Script [{}]".format(_errorcode))
