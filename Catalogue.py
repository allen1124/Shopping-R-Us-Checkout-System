#!/usr/bin/python3

class Catalogue:

    def __init__(self):
        self.catalogue = {}

    def addProduct(self, newProduct):
        """
            newProduct: Dictionary of product details
                e.g. {sku: "ipd", name: "Super iPad", price: 549.99}
        Add newProduct to catalogue dictionary with product sku as key
        """ 
        if newProduct["sku"] in self.catalogue:
            return
        self.catalogue[newProduct["sku"]] = newProduct

    def updatePrice(self, sku, newPrice):
        """
            sku: product sku string
            newPrice: new price number
        Update the product price
        """
        if sku in self.catalogue.keys():
            self.catalogue[sku]["price"] = newPrice
        else:
            print("The product '{}' to be ameneded not exist in catalogue. Please add the product first.".format(sku))

    def getPrice(self, sku):
        """
            sku: product sku string
        Return the product price from catalogue
        """
        return self.catalogue[sku]["price"]

    def __str__(self):
        catStr = "|SKU\t|Name\t\t|Price\t\n"
        for sku, detail in self.catalogue.items():
            catStr += "|"+sku+"\t|"+detail["name"]+"\t|$"+str(detail["price"])+"\t\n"
        return catStr