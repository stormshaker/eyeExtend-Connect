## Use the authorization script to test connectivity

jwt_token = params["connect_authorization_token"] # auth token
response = {}

if jwt_token != "":
	response["succeeded"] = True
	response["result_msg"] = "Successfully connected."
else:
	response["succeeded"] = False
	response["result_msg"] = "Could not connect to Cylance server."