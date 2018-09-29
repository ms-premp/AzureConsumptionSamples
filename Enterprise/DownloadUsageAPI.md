# Usage Details download API



Usage details download APIs from Microsoft consumption has two variants.

- Synchronous 
- Asynchronous

To know more about them please visit [here](https://docs.microsoft.com/en-us/rest/api/billing/enterprise/billing-enterprise-api-usage-detail).



### Synchronous call

In this sample, we will be showing how to use synchronous call to download the usage data in CSV format.

I am writing a simple C# function to get the job done. 

``` 
     
/// <param name="enrollmentNumber">Enrollment Number</param>
/// <param name="apiKey">API key for making the request</param>
/// <param name="billingPeriod">billing period for usage data</param>
/// <param name="destinationFilePath">path to file, where the data will be downloaded</param>
public void DownloadUsage(string enrollmentNumber, string apiKey, string billingPeriod, string destinationFilePath)
{
	try
	{
		var apiUrl = $"https://consumption.azure.com/v3/enrollments/{enrollmentNumber}/usagedetails/download?billingPeriod={billingPeriod}";
		var request = System.Net.WebRequest.CreateHttp(apiUrl);
		request.Headers.Add("authorization", "bearer " + apiKey);
		request.Method = "GET";
		using (var response = (System.Net.HttpWebResponse)request.GetResponse())
		{
			var responseStream = response.GetResponseStream();
			if (responseStream == null)
			{
				Console.WriteLine("No Response");
			}
			else
			{
				//// feel free to change buffer size as needed.
				const int BufferSize = 64 * 1024 * 1024;
				using (var reader = new System.IO.StreamReader(responseStream, System.Text.Encoding.UTF8))
				using (var writer = new System.IO.StreamWriter(destinationFilePath))
				{
					var buffer = new char[BufferSize];
					int bytesRead;
					while ((bytesRead = reader.Read(buffer, 0, BufferSize)) != 0)
					{
						writer.Write(buffer);
					}
				}
			}
		}
	}
	catch (Exception ex)
	{
		Console.WriteLine(ex);
	}

}
```



That's it.

In my test, I was able to download 1 GB of file in around 8 minutes. 

Please feel free to try other variants of reading and writing to file for better performance.

