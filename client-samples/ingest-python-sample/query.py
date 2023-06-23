
from pydozer.api import ApiClient

api_client = ApiClient("trips", url="localhost:7003")
trips = api_client.query()
if trips and trips.records:
  print(trips.records[0])
else:
  print("No records found")
