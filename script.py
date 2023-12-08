from asyncio import timeout
import schedule
from schedule import every,repeat
from dataclasses import dataclass
from typing import List
import pymongo
import datetime
import requests
import requests
import time as tm
import get_access_token
import get_temp_creds
import get_catalog_item
import get_amazon_fba_fees
import get_product_price
from sp_api.api import Sales
from sp_api.base import Marketplaces
from sp_api.base import Granularity
import const


@repeat(every(1).hour)
def update_every_one_hour():
    client = pymongo.MongoClient(
        "mongodb+srv://Shaown:qDs5VgNL2FgLSMPN@cluster0.m94phd5.mongodb.net/?retryWrites=true&w=majority")
    db = client["Leads_API_Data"]


    asins = ["B07BF2CD75","B08H1LBQMZ", "B01N0O7QKJ", "B00006IFMO", "B007RAQTSI", "B07PZGSWN9", "B07XLDRB2S", "B0025TUZ8Q",
            "B08YPCDG29", "B004QJU51K", "B097NFV9DM", "B00UJGUBWW", "B01G6RWNH8", "B07PW2DWK2", "B08WF6TM4Q", "B008KQ1Y2Y",
            "B09T619YSF", "B01G6RWTJA", "B09Q3QWCCQ", "B01NAXTMVU", "B09Q4CYJ4S", "B01EVHYXR8", "B09LHXBGXD", "B00CZ21BXG",
            "B0843H7WHX", "B0001WGIBW", "B00000IU6X", "B082QCFBLE"]

    leads_data = {
        "_id": "",
        "ProductImage": "",
        "ProductName": "",
        "AmazonFBAEstimatedFees": "",
        "EstimatedSalesRank": "",
        "AmazonPrice": "",
        "NumberOfSellersOnTheListing": "",
    }

    try:
        temp_credentials = get_temp_creds.get_temp_credentials()
    except Exception as e:
        print(f"Error: {e}")


    try:
        token_data = get_access_token.request_access_token()
    except Exception as e:
        print(f"Error: {e}")


    marketplace_id = "A2EUQ1WTGCTBG2"
    asin = "B01NAXTMVU"
    access_token = token_data["access_token"]
    credentials = temp_credentials
    list_price = -1

    leads_collection = db.leads

    for asin in asins:
        try:
            result = get_catalog_item.get_catalog_item(                #catalog api call here
                marketplace_id, asin, access_token, credentials)
            print(result["asin"])
            leads_data["_id"] = result["asin"]
            leads_data["ProductName"] = result["attributes"]["item_name"][0]["value"]
            leads_data["ProductImage"] = result["images"][0]["images"][0]["link"]
            leads_data["EstimatedSalesRank"] = result["salesRanks"][0]["displayGroupRanks"][0]["rank"]

            if result["attributes"].get("list_price") is not None:
                list_price = result["attributes"]["list_price"][0]["value"]
                leads_data["AmazonPrice"] = result["attributes"]["list_price"][0]["value"]
            else:
                print("list price not available")

        except Exception as e:
            print(f"Error: {e}")

        if (list_price != -1):
            try:
                result = get_amazon_fba_fees.get_amazon_fba_fees(                  # Product fees api call here
                    asin, list_price, access_token, credentials)

                leads_data["AmazonFBAEstimatedFees"] = result["payload"]["FeesEstimateResult"]["FeesEstimate"]["TotalFeesEstimate"]["Amount"]

            except Exception as e:
                print(f"Error")

        try:
            get_price = get_product_price.get_product_price(
                marketplace_id, asin, access_token, credentials)
            leads_data["NumberOfSellersOnTheListing"] = len(
                get_price["payload"]["Offers"])

        except Exception as e:
            print(f"Error:{e}")

        asin_exist = leads_collection .find_one({"_id": leads_data["_id"]})

        if (asin_exist is not None):

            filter_condition = {"_id": leads_data["_id"]}

            update_data = {"$set": {
                "ProductName": leads_data["ProductName"],
                "ProductImage": leads_data["ProductImage"],
                "EstimatedSalesRank": leads_data["EstimatedSalesRank"],
                "AmazonPrice": leads_data["AmazonPrice"],
                "AmazonFBAEstimatedFees": leads_data["AmazonFBAEstimatedFees"],
                "NumberOfSellersOnTheListing": leads_data["NumberOfSellersOnTheListing"]
            }}

            result = leads_collection.update_one(filter_condition, update_data)
        else:
            leads_collection .insert_one(leads_data)


while True:
    schedule.run_pending()
    tm.sleep(1)
