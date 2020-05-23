import json
from azure.common.client_factory import get_client_from_json_dict
from azure.mgmt.consumption.consumption_management_client import ConsumptionManagementClient

class MyUsage:

    def __init__(self, filePath):        
        with open(filePath) as f:
            credData = json.load(f)
        self.scope = "subscriptions/" + credData['subscriptionId']
        self.consumption_client = get_client_from_json_dict(ConsumptionManagementClient, credData)

    def run_by_date(self, date_filter):
        usages = self.consumption_client.usage_details.list(self.scope, filter=date_filter)
        self.printresults(usages)

    def run_by_billing_period(self, billing_period):
        scope = self.scope + "/providers/Microsoft.Billing/billingPeriods/" + billing_period
        usages = self.consumption_client.usage_details.list(scope);       
        self.printresults(usages)

    def printresults(self, usages):
        output = list(usages)             
        minDate = min(output, key=lambda x: x.date_property).date_property
        maxDate = max(output, key=lambda x: x.date_property).date_property
        print("Minimum Date:", minDate, ", Maximum Date:", maxDate)


def run_example_by_datefilter():
    azure_usage = MyUsage("credentials.json")
    date_filter = "properties/usageStart ge '2020-02-26' AND properties/usageStart lt '2020-02-27'"     
    print("Get data by date range '2020-02-26' and '2020-02-27'")
    azure_usage.run_by_date(date_filter)    
    print("Done")


def run_example_by_billingperiod():
    azure_usage = MyUsage("credentials.json")    
    print("Get data by billing period 202003")
    azure_usage.run_by_billing_period("202003")
    print("Done")


if __name__ == "__main__":
    run_example_by_datefilter()
    run_example_by_billingperiod()

