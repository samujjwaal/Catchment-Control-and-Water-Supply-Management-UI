import urllib.request
import json

data = {
        "Inputs": {
                "Catchment_Input":
                [
                    {
                            'LAT': input("LAT : "),   
                            'LON': input("LON : "),   
                            'RAINFALL': input("RAINFALL : "),   
                            'GRDWTR': input("GRDWTR : "),   
                            'Soil_Score': input("SOIL_SCORE : "),   
                            'Elevation': input("ELEVATION : "),   
                    }
                ],
        },
    "GlobalParameters":  {
    }
}

body = str.encode(json.dumps(data))

url = 'https://ussouthcentral.services.azureml.net/workspaces/e8133a8b3c3e4e70be72cffb0e45a85c/services/95b227a3833042df9afeb7abe8cbd71b/execute?api-version=2.0&format=swagger'
api_key = 'LQ0Tb4vX0P7Fbb/zuGmNSauhlKrJv7WcKJps70psDo+8f1vKrV7GyX/XQCD5pJ4CUG/pNeQc/xZX+XK/T5RQkw==' # Replace this with the API key for the web service
headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

req = urllib.request.Request(url, body, headers)

try:
    response = urllib.request.urlopen(req)

    result = response.read()
##    op = response.json()
##    print(op["Results"]["Catchment_Output"][0]["Scored Labels"])
    print(result)
except urllib.error.HTTPError as error:
    print("The request failed with status code: " + str(error.code))

    # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
    print(error.info())
    print(json.loads(error.read().decode("utf8", 'ignore')))
