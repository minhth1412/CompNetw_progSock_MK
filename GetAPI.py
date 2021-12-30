import requests, json

def getAPIfromWeb():

    APIKey = requests.get("https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate").json()["results"]


    Header = { 
        "Accept": "application/json",
        "Authorization": "Bearer " + APIKey
    }
    URL= "https://vapi.vnappmob.com/api/v2/exchange_rate/vcb"
    urlGetAPI = requests.get(url = URL, headers = Header)
    result = urlGetAPI.json()
    with open("webData.json", "w") as outfile:
        json.dump(result, outfile, indent=4)
            
    return result