import pymysql
import json
from flask import jsonify
from flask import Response
import grequests
import requests

import os

CUSTOMERS_URI = "http://ec2-54-164-164-254.compute-1.amazonaws.com/api/customers"
CONTACTS_URI = "http://44.202.82.103:5015/contactInfo"


class CustomerContactCompose:

    def __int__(self):
        pass

    # TODO: add pagination here and align it with the other endpoints..
    @staticmethod
    def get_info(cid=None):
        print("Inside get_info")

        result = None

        if cid is None:
            print("cid is None")
            reqs = [
                grequests.get(CUSTOMERS_URI),
                grequests.get(CONTACTS_URI),
            ]

            customers_req_response, contacts_req_response = gre_responses(reqs)

            customers_response = json.loads(customers_req_response.content)["content"]
            contacts_response = json.loads(contacts_req_response.content)["items"]

            merged = []
            for customer in customers_response:
                for contact in contacts_response:
                    if str(customer["cid"]) == str(contact["cid"]):
                        element = dict(customer.items() | contact.items())
                        element["links"] = [
                            {
                            "href": "/beta/itemsservice/items/cid/{}".format(customer["cid"]),
                            "rel": "items"
                            },
                            {
                            "href": "/beta/composeservice/api/customercontactcompose/{}".format(customer["cid"]),
                            "rel": "self"
                            }
                        ]
                        merged.append(element)
            print("result 54 : ", result)
            result = merged

        else:
            print("result 58 : ", result)
            reqs = [
                grequests.get(CUSTOMERS_URI + '/' + cid),
                grequests.get(CONTACTS_URI + '/' + cid),
            ]

            customers_req_response, contacts_req_response = gre_responses(reqs)

            # Customers MS returns 500 if user doesn't exist, so I only check contacts
            if contacts_req_response.status_code == 404:
                return None

            print("!!!! customers_req_response !!!", customers_req_response)
            print("!!!! contacts_req_response !!!", contacts_req_response)

            customers_response = json.loads(customers_req_response.content)
            contacts_response = json.loads(contacts_req_response.content)

            result = dict(customers_response.items() | contacts_response.items())

            if "cid" in customers_response.keys():
                result["links"] = [
                    {
                       "href": "/beta/itemsservice/items/{}".format(customers_response["cid"]),
                       "rel": "items"
                    },
                    {
                       "href": "/beta/composeservice/api/customercontactcompose/{}".format(customers_response["cid"]),
                       "rel": "self"
                    }
                ]
        print("!!!! result 89 !!!", result)

        return result

    def add_info(data):
        dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
        contact_post = dictfilt(data, ("cid", "email", "phone", "address_line1", "address_line2", "address_state", "address_city", "address_zipcode"))
        customer_post = dictfilt(data, ("cid", "firstName", "middleName", "lastName", "doj"))

        headers = {'Content-Type': 'application/json', 'authCID': contact_post['cid']}

        reqs = [
            grequests.post(CUSTOMERS_URI, data=json.dumps(customer_post), headers=headers),
            grequests.post(CONTACTS_URI, data=json.dumps(contact_post), headers=headers)
        ]

        customers_req_response, contacts_req_response = gre_responses(reqs)

        customers_response = {"customers_status_code" : customers_req_response.status_code}
        contacts_response = {"contacts_status_code" : contacts_req_response.status_code}

        result = dict(customers_response.items() | contacts_response.items())

        return result

    def update_info(data):
        dictfilt = lambda x, y: dict([ (i,x[i]) for i in x if i in set(y) ])
        contact_put = dictfilt(data, ("cid", "email", "phone", "address_line1", "address_line2", "address_state", "address_city", "address_zipcode"))
        customer_put = dictfilt(data, ("cid", "firstName", "middleName", "lastName", "doj"))

        headers = {'Content-Type': 'application/json', 'authCID': contact_put['cid']}

        reqs = [
            grequests.put(CUSTOMERS_URI + "/{}".format(data["cid"]), data=json.dumps(customer_put), headers=headers),
            grequests.put(CONTACTS_URI + "/{}".format(data["cid"]), data=json.dumps(contact_put), headers=headers)
        ]

        customers_req_response, contacts_req_response = gre_responses(reqs)

        customers_response = {"customers_status_code" : customers_req_response.status_code}
        contacts_response = {"contacts_status_code" : contacts_req_response.status_code}

        result = dict(customers_response.items() | contacts_response.items())

        return result

def gre_responses(reqs):
    async_results = grequests.map(reqs)

    contacts_req_response = None
    customers_req_response = None

    for response in async_results:
        if "customers" in response.request.url:
            customers_req_response = response
        else:
            contacts_req_response = response

    return customers_req_response, contacts_req_response
