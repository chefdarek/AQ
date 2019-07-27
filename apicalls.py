import openaq
api = openaq.OpenAQ()
status, body = api.measurements(city='Los Angeles', parameter='pm25')
