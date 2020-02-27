import json
from azure.common.client_factory import get_client_from_json_dict
from azure.mgmt.consumption.consumption_management_client import ConsumptionManagementClient

class MyUsage:

    def __init__(self, filePath):        
        with open(filePath) as f:
            credData = json.load(f)
        self.scope = "subscriptions/" + credData['subscriptionId']                 
        self.consumption_client = get_client_from_json_dict(ConsumptionManagementClient, credData)

    def run(self, date_filter):
        usages = self.consumption_client.usage_details.list(self.scope, filter=date_filter);   
        output = list(usages)             
        minDate = min(output, key=lambda x: x.date_property).date_property
        maxDate = max(output, key=lambda x: x.date_property).date_property
        print("Minimum Date:", minDate, ", Maximum Date:", maxDate)


def run_example():
    azure_usage = MyUsage("C:\SDK\Python\credentials.json")
    date_filter = "properties/usageStart ge '2020-02-25' AND properties/usageStart lt '2020-02-27'"     
    azure_usage.run(date_filter)    


if __name__ == "__main__":
    run_example()
