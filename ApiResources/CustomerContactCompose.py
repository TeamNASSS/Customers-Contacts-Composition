import pymysql
from flask import Response
import requests

import os

CUSTOMERS_URI = "http://ec2-54-164-164-254.compute-1.amazonaws.com/api/customers/"
CONTACTS_URI = "http://44.202.82.103:5015/contactInfo/"

class CustomerContactCompose:

    def __int__(self):
        pass

    @staticmethod
    def get_info(cid=None):

        result = None

        if cid is None:
            customers_response = requests.get(CUSTOMERS_URI).json()["content"]
            contacts_response  = requests.get(CONTACTS_URI).json()["items"]
            #result = dict(customers_response["content"].items() | contacts_response.items())

            merged = []
            for customer in customers_response:
                for contact in contacts_response:
                    if customer["cid"] == contact["cid"]:
                        merged.append(dict(customer.items() | contact.items()))
            result = merged

        else:
            customers_response = requests.get(CUSTOMERS_URI + cid).json()
            contacts_response  = requests.get(CONTACTS_URI  + cid).json()
            result = dict(customers_response.items() | contacts_response.items())

        return result
