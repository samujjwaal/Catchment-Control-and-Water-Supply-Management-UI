# import dependencies
import requests
from requests.exceptions import HTTPError

# json data object to be sent to the web service API endpoint
api_data = {
    "Inputs": {
        "Catchment_Input": [
            {
                "LAT": input("LAT : "),
                "LON": input("LON : "),
                "RAINFALL": input("RAINFALL : "),
                "GRDWTR": input("GRDWTR : "),
                "Soil_Score": input("SOIL_SCORE : "),
                "Elevation": input("ELEVATION : "),
            }
        ],
    },
    "GlobalParameters": {},
}

# Replace this with the URI and API Key for different web service
url = "https://ussouthcentral.services.azureml.net/workspaces/e8133a8b3c3e4e70be72cffb0e45a85c/services/95b227a3833042df9afeb7abe8cbd71b/execute?api-version=2.0&format=swagger"
api_key = "LQ0Tb4vX0P7Fbb/zuGmNSauhlKrJv7WcKJps70psDo+8f1vKrV7GyX/XQCD5pJ4CUG/pNeQc/xZX+XK/T5RQkw=="
headers = {"Content-Type": "application/json", "Authorization": ("Bearer " + api_key)}

try:
    # POST request to API
    response = requests.post(url=url, json=api_data, headers=headers)

    # If the response was successful, no Exception will be raised
    response.raise_for_status()

    result = response.json()
    score = result["Results"]["Catchment_Output"][0]["Scored Labels"]
    print(result)

except HTTPError as http_error:
    # Print the headers - they include the request ID and the timestamp, which are useful for debugging the failure
    print(f"The request failed with status code: {http_error.response.status_code}\n")
    print(f"Request Headers: {http_error.response.headers}\n")
    print(f"Error Object: {http_error.response.json()}")
