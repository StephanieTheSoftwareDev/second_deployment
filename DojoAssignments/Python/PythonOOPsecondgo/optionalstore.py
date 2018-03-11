class Store(object):
    def __init__(self, location, owner_name):
       self.location = location
       self.owner_name = owner_name
       self.total_products = []

    def add_products(self, *products):
        self.total_products.append(products)
        return self
    
    def remove_product(self, products):
        self.total_products.remove(products)
        return self

    def inventory(self):
        theTotal = self.total_products
        self.total_products = theTotal
        # print self.total_products
        # if self.total_products:

        for item in range(len(self.total_products)):
            # print len(self.total_products)
            # print item
            for x in item:
                print x
                print item[x]
            # for *products in theTotal:
            #     print *products
                # print b
                # print "The " + self.location + " store, which is owned by " + self.owner_name + ", has the following products: ", a + ", " + b
        return self

store1 = Store("San Francisco", "Leslie").add_products("strawberries", "peaches", "apples").inventory()


	