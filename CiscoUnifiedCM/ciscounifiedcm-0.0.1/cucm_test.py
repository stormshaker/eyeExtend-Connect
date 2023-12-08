import logging

logging.debug("Debug - SCRIPT is cucm_test")

response = {}
storedcookie = params.get("connect_authorization_token")
additionalservers = params["connect_cucm_additionalservers"]
additionalserver1 = params["connect_cucm_additionalserver1"]
additionalserver2 = params["connect_cucm_additionalserver2"]
additionalserver3 = params["connect_cucm_additionalserver3"]
additionalserver4 = params["connect_cucm_additionalserver4"]
cookie = json.loads(storedcookie)

logging.debug("Debug - PARAMS [CUCM AXL API Url] is [{}]".format(params["connect_cucm_axl_url"]))
logging.debug("Debug - PARAMS [connect_authorization_token] is [{}]".format(params.get("connect_authorization_token")))
logging.debug("Debug - VARIABLE [storedcookie] is [{}]".format(storedcookie))
logging.debug("Debug - VARIABLE [cookie] is [{}]".format(cookie))

if cookie:
    if cookie["primary"]:
        message = "DEBUG - Primary Server Token was present"
        response["result_msg"] = message
    else:
        message = "DEBUG - Primary Server Token was NOT present"
        response["result_msg"] = message
        response["troubleshooting"] = message
        response["succeeded"] = False

    if additionalservers == "true":
        if additionalserver1:
            if cookie["additional1"]!="":
                message = "Addtional Server 1 Token was present"
                response["result_msg"] = message
                logging.debug("Debug - TEST [additionalserver1] message is [{}]".format(message))
            else:
                message = "Addtional Server 1 Token was NOT present"
                response["result_msg"] = message
                response["troubleshooting"] = message
                logging.debug("Debug - TEST [additionalserver1] message is [{}]".format(message))
                response["succeeded"] = False
        if additionalserver2!="":
            if cookie["additional2"]!="":
                message = "Addtional Server 2 Token was present"
                response["result_msg"] = message
                logging.debug("Debug - TEST [additionalserver2] message is [{}]".format(message))
            else:
                message = "Addtional Server 2 Token was NOT present"
                response["result_msg"] = message
                response["troubleshooting"] = message
                logging.debug("Debug - TEST [additionalserver2] message is [{}]".format(message))
                response["succeeded"] = False
        if additionalserver3!="":
            if cookie["additional3"]!="":
                message = "Addtional Server 3 Token was present"
                response["result_msg"] = message
                logging.debug("Debug - TEST [additionalserver3] message is [{}]".format(message))
            else:
                message = "Addtional Server 3 Token was NOT present"
                response["result_msg"] = message
                response["troubleshooting"] = message
                logging.debug("Debug - TEST [additionalserver3] message is [{}]".format(message))
                response["succeeded"] = False
        if additionalserver4!="":
            if cookie["additional4"]!="":
                message = "Addtional Server 4 Token was present"
                response["result_msg"] = message
                logging.debug("Debug - TEST [additionalserver4] message is [{}]".format(message))
            else:
                message = "Addtional Server 4 Token was NOT present"
                response["result_msg"] = message
                response["troubleshooting"] = message
                logging.debug("Debug - TEST [additionalserver4] message is [{}]".format(message))
                response["succeeded"] = False
    message = "Test Successful as Authorization Token(s) present"
    logging.debug(message)
    response["result_msg"] = message
    response["succeeded"] = True
else:
    message = "TEST Failed - Authorization Token was not present, try refreshing the Authorization Token"
    response["succeeded"] = False
    response["result_msg"] = message
    response["troubleshooting"] = message
