import pymysql
import json
from flask import jsonify
from flask import Response
import grequests
import requests

import os

CUSTOMERS_URI = "http://ec2-54-164-164-254.compute-1.amazonaws.com/api/customers/"
CONTACTS_URI = "http://44.202.82.103:5015/contactInfo/"


class CustomerContactCompose:

    def __int__(self):
        pass

    # TODO: add pagination here and align it with the other endpoints..
    @staticmethod
    def get_info(cid=None):

        result = None

        if cid is None:
            reqs = [
                grequests.get(CUSTOMERS_URI),
                grequests.get(CONTACTS_URI),
            ]

            async_results = grequests.map(reqs)

            customers_response = json.loads(async_results[0].content)["content"]
            contacts_response = json.loads(async_results[1].content)["items"]

            merged = []
            for customer in customers_response:
                for contact in contacts_response:
                    if customer["cid"] == contact["cid"]:
                        merged.append(dict(customer.items() | contact.items()))
            result = merged

        else:
            reqs = [
                grequests.get(CUSTOMERS_URI + cid),
                grequests.get(CONTACTS_URI + cid),
            ]

            async_results = grequests.map(reqs)

            customers_response = json.loads(async_results[0].content)
            contacts_response = json.loads(async_results[1].content)

            result = dict(customers_response.items() | contacts_response.items())

        return result
