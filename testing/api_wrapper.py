import requests, json

import settings

SERVER_URL = "http://{}:{}".format(settings.HOST, settings.PORT)

"""
    These are some quick and dirty wrappers for calling the api endpoints to give them a test
"""

def print_response(resp):
    print("URL called: {}".format(resp.url))
    print("HTTP response code: {}".format(resp.status_code))
    print("Content: {}".format(resp.text))


def get_node_name():
    print_response(requests.get(SERVER_URL))


def mine():
    url = "{}/mine".format(SERVER_URL)
    print_response(requests.get(url))


def current_transactions():
    url = "{}/transactions/current".format(SERVER_URL)
    print_response(requests.get(url))


def new_transaction(sender, recipient, amount):
    url = "{}/transactions/new".format(SERVER_URL)
    data = {
        'sender': sender, 
        'recipient': recipient, 
        'amount': amount
    }
    json_str = json.dumps(data)
    print_response(requests.post(url, headers={'Content-Type': 'application/json'}, data=json_str))
    

def chain():
    url = "{}/chain".format(SERVER_URL)
    print_response(requests.get(url))