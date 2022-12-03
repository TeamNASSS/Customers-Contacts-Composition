from smartystreets_python_sdk import StaticCredentials, exceptions, ClientBuilder
from smartystreets_python_sdk.us_street import Lookup as StreetLookup

def is_valid_address(data):
    auth_id = "f035080f-c8fb-2860-a856-a2d7cf3537fb"
    auth_token = "gH1PRVsGnUuY3VEzLd0y"

    credentials = StaticCredentials(auth_id, auth_token)
    client = ClientBuilder(credentials).build_us_street_api_client()
    lookup = StreetLookup()

    lookup.street = data['address_line1']
    # apartment number fails as it may not be in smarty's database
    #lookup.secondary = data['address_line2']
    lookup.city = data['address_city']
    lookup.state = data['address_state']
    lookup.zipcode = data['address_zipcode']

    try:
       client.send_lookup(lookup)
    except exceptions.SmartyException as err:
       return False

    if not lookup.result:
       return False

    return True
