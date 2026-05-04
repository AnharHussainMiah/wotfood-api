import os
import json
import requests

# BASE_URL = os.getenv("BASE_URL", "https://neo.wotfood.co.uk/")

BASE_URL = "http://localhost:9090/"

def println(s):
    print(s+"\n")


def test_get_shop_details():
    path = "/api/public/shop-details"

    payload = {
        "companyId": 1
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(BASE_URL + path, headers=headers, data=json.dumps(payload))
    println("==> Testing: Get Shop Details...")
    println(response.text)

    assert(response.status_code == 200)


def test_get_opening_times():
    path = "/api/public/opening-times"

    payload = {
        "companyId": 1
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(BASE_URL + path, headers=headers, data=json.dumps(payload))
    println("==> Testing: Get Opening Times...")
    println(response.text)

    assert(response.status_code == 200)

def test_get_menu_data():
    path = "/api/public/menu-data"

    payload = {
        "companyId": 1
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(BASE_URL + path, headers=headers, data=json.dumps(payload))
    println("==> Testing: Get Menu Data...")
    println(response.text)

    assert(response.status_code == 200)

def test_get_item_exta_options():
    path = "/api/public/item-extra-options"

    payload = {
        "productId": 1689
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(BASE_URL + path, headers=headers, data=json.dumps(payload))
    println("==> Testing: Get Item Extra Options...")
    println(response.text)

    assert(response.status_code == 200)