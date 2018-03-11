class Store(object):
    def __init__(self, location, owner_name):
       self.location = location
       self.owner_name = owner_name
       self.total_products = []

    def add_products(self, *products):
        for product in products:
            self.total_products.append(product)
        return self
    
    def remove_product(self, products):
        self.total_products.remove(products)
        return self

    def show_inventory(self):
        theTotal = self.total_products
        self.total_products = theTotal
        result_string = ""
        for item in self.total_products:
            result_string += item + ", "
            
        print "The " + self.location + " store, which is owned by " + self.owner_name + ", has the following products: " + result_string
        return self

Luckys = Store("San Francisco", "Leslie").add_products("strawberries", "peaches", "apples").show_inventory().remove_product("apples").show_inventory()
Target = Store("San Jose", "Bob").add_products("waffles", "turtles", "bananas", "fishies").show_inventory()

	