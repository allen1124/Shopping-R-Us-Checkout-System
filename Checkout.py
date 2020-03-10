#!/usr/bin/python3
from PricingRules import PricingRules
from Catalogue import Catalogue
import datetime

class Checkout():
    def __init__(self, catalogue, pricingRules):
        """
            catalogue: Catalogue object from Catalogue.py
            pricingRules: PricingRules object from PricingRules.py
        """
        super(Checkout, self).__init__()
        self.cart = []
        self.catalogue = catalogue
        self.pricingRules = pricingRules
        
    def scan(self, item):
        """
            item: scanned product sku string
        Add scanned product into cart
        """
        if item in self.catalogue.catalogue:
            self.cart.append({"sku": item, "billingPrice": self.catalogue.getPrice(item)})
        else:
            raise KeyError("The item '{}' is not exist in the Catalogue".format(item))

    def countItem(self, sku):
        """
            item: product sku string
        Return number of the product in cart
        """
        count = 0
        for item in self.cart:
            if item["sku"] == sku:
                count += 1
        return count

    def applyRules(self):
        """
        Apply the pricing rules to the current cart
        """
        self.pricingRules.refreshRules()
        for rule in self.pricingRules.rules:
            if rule["type"] == "BULK":
                if self.countItem(rule["sku"]) > rule["bulkSize"]:
                    for item in self.cart:
                        if item["sku"] == rule["sku"]:
                            if item["billingPrice"] > rule["billingPrice"]:
                                item["billingPrice"] = rule["billingPrice"]
            elif rule["type"] == "XforY":
                count = int(self.countItem(rule["xSku"])/rule["xSize"])*rule["ySize"]
                for item in self.cart:
                    if count > 0 and item["sku"] == rule["ySku"]:
                        item["billingPrice"] = 0
                        count -= 1

    def total(self):
        """
        Return the total price of the current cart, which pricing rules applied
        """
        totalPrice = 0
        self.applyRules()
        for item in self.cart:
            totalPrice += item["billingPrice"]
        return totalPrice

    def clearCart(self):
        self.cart = []
    
    def __str__(self):
        skuScanned = "SKUs scanned: "
        for item in self.cart[:-1]:
            skuScanned += item["sku"]+", "
        skuScanned += self.cart[-1]["sku"]
        expectedTotal = "Total expected: ${0:.2f}".format(self.total())
        return skuScanned+"\n"+expectedTotal
        

if __name__ == '__main__':
    cat = Catalogue()
    cat.addProduct({"sku": "ipd", "name": "Super iPad", "price": 549.99})
    cat.addProduct({"sku": "mbp", "name": "Macbook Pro", "price": 1399.99})
    cat.addProduct({"sku": "atv", "name": "Apple TV", "price": 109.50})
    cat.addProduct({"sku": "vga", "name": "VGA Adapter", "price": 30.00})
    print(cat)

    pl = PricingRules()
    pl.addXforYDiscount("atv", 3, "atv", 1, datetime.datetime.now().date())
    pl.addBulkDiscount("ipd", 4, 499.99, datetime.datetime.now().date())
    pl.addXforYDiscount("mbp", 1, "vga", 1 , datetime.datetime.now().date())

    co = Checkout(cat, pl)

    # Case 1: {atv, atv, atv, vga}
    co.scan("atv")
    co.scan("atv")
    co.scan("atv")
    co.scan("vga")
    print(co)
    co.clearCart()

    # Case 2: {atv, ipd, ipd, atv, ipd, ipd, ipd}
    co.scan("atv")
    co.scan("ipd")
    co.scan("ipd")
    co.scan("atv")
    co.scan("ipd")
    co.scan("ipd")
    co.scan("ipd")
    print(co)
    co.clearCart()

    # Case 3: {mbp, vga, ipd}
    co.scan("mbp")
    co.scan("vga")
    co.scan("ipd")
    print(co)
    co.clearCart()