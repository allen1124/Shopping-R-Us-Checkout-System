#!/usr/bin/python3
import datetime

class PricingRules:
    
    def __init__(self):
        self.rules = []

    def addBulkDiscount(self, sku, bulkSize, billingPrice, expiredDate):
        """
            sku: product sku string
            bulkSize: number of quantity to be more than considered as bulk
            billingPrice: new billing price with bulk discount
            expiredDate: expired date, Date object
        Append a new bulk discount rule into the list of pricing rules
            e.g ("ipd", 4, 499.99, datetime.datetime.(2020, 3, 11)))
            if customer buy more that 4 ipd, the price of ipd will drop to $499.99
        """
        rule = {
            "type": "BULK",
            "sku": sku,
            "bulkSize": bulkSize,
            "billingPrice": billingPrice,
            "expiredDate": expiredDate
        }
        if expiredDate < datetime.datetime.now().date():
            print("The pricing rule is outdated. Please add with a new expired date.")
        else:
            self.rules.append(rule)
    
    def addXforYDiscount(self, xSku, xSize, ySku, ySize, expiredDate):
        """
            xSku: product sku string which product required for XforY discount
            xSize: number of quantity of xSku product required
            ySku: free product sku
            ySize: number of quantity of ySku product given
            expiredDate: expired date, Date object
        Add a new XforY discount into the list of pricing rules.
            e.g. ("atv", 3, "atv", 1, datetime.datetime.(2020, 3, 11)))
            for every 3 atv in cart, customer can have 1 atv as free, i.e. 3 for 2 deal on atv
        """
        rule = {
            "type": "XforY",
            "xSku": xSku,
            "xSize": xSize,
            "ySku": ySku,
            "ySize": ySize,
            "expiredDate": expiredDate
        }
        if expiredDate < datetime.datetime.now().date():
            print("The pricing rule is outdated. Please add with a new expired date.")
        else:
            self.rules.append(rule)

    def refreshRules(self):
        """
        Remove the pricing rule(s) which is expired now
        """
        self.rules = [rule for rule in self.rules if rule["expiredDate"] >= datetime.datetime.now().date()]
                