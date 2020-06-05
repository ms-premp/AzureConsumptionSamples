import json
import adal
import requests


class MyUsage:

    def __init__(self, filePath):        
        with open(filePath) as f:
            credData = json.load(f)
        scope = "subscriptions/" + credData['subscriptionId']
        self.costmanagementUrl = "https://management.azure.com/" + scope + "/providers/Microsoft.CostManagement/query?api-version=2019-11-01&$top=4000"
        authority_uri = credData['activeDirectoryEndpointUrl'] + "/" + credData['tenantId']
        context = adal.AuthenticationContext(authority_uri)
        token = context.acquire_token_with_client_credentials(
                    credData["resourceManagerEndpointUrl"],
                    credData['clientId'],
                    credData['clientSecret'])
        bearer = "bearer " + token.get("accessToken")
        self.headers = { "Authorization" : bearer, "Content-Type": "application/json" }
        self.usagedata = []          


    def run(self, startdate, enddate, grain = "Monthly", groupby = None):

        payload = {
                "type": "ActualCost",
                "dataSet": {
                    "granularity": grain,
                    "aggregation": {
                        "totalCost": {
                            "name": "PreTaxCost",
                            "function": "Sum"
                        },
                        "totalCostUSD": {
                            "name": "PreTaxCostUSD",
                            "function": "Sum"
                        }
                    }
                },
                "timeframe": "Custom",
                "timePeriod": {
                    "from": startdate,
                    "to": enddate
                }
            }
        
        if groupby != None:
            payload['dataSet']['grouping'] =[{
                            "type": "Dimension",
                            "name": groupby
                        }]
        
        payloadjson = json.dumps(payload)        
        self.usagedata = []
        response = requests.post(self.costmanagementUrl, data=payloadjson, headers = self.headers)
        if response.status_code == 200:
            self.transform(payloadjson, response.text)
            print(*self.usagedata, sep = "\n")
        else:
            print("error")   
            print("error " + response.text)


    def transform(self, payloadjson, response):
        result = json.loads(response)
        for record in result["properties"]["rows"]:
            usageRecord = {}
            for index, val in enumerate(record):
                columnName = result["properties"]["columns"][index]
                if columnName["type"] == "number":
                    usageRecord[columnName["name"]] = float(val)
                else:
                    usageRecord[columnName["name"]] = val

            self.usagedata.append(usageRecord)

        nextLink = result["properties"]["nextLink"]
        if nextLink != None:
            nextLinkResponse = requests.post(nextLink, data=payloadjson, headers = self.headers)
            if nextLinkResponse.status_code == 200:
                self.transform(payloadjson, nextLinkResponse.text)
            else:
                print("error in fetching next page " + nextLink)
                print("error " + nextLinkResponse.text)




def run_example():
    azure_usage = MyUsage("credentials.json")
    azure_usage.run("2020-04-01", "2020-06-30")
    # azure_usage.run("2020-04-01", "2020-06-30", groupby="ServiceName")
    print("Done")


if __name__ == "__main__":
    run_example()


