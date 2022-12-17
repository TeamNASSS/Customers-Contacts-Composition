from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup

auth_id = "f035080f-c8fb-2860-a856-a2d7cf3537fb"
auth_token = "gH1PRVsGnUuY3VEzLd0y"

credentials = StaticCredentials(auth_id, auth_token)
client = ClientBuilder(credentials).build_us_street_api_client()
lookup = StreetLookup()

lookup.street = "318W 121St"
lookup.street2 = "5C"
#lookup.secondary = "APT 2"
lookup.city = "New York"
lookup.state = "NY"
lookup.zipcode = 10027

try:
   client.send_lookup(lookup)
except exceptions.SmartyException as err:
   print(False)

if not lookup.result:
   print(False)

print(True)