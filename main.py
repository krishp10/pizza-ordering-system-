"""benvenuto al ristorante krish"""


import re
import sys

gst= 1.15
# maximum number of items in one order
max_items = 5
# delivery charge (in $)
delivery_charge = 10.00
# discount
discount_value = 0
# list of dictionaries (items) with name and price
items_available = (
    {"name": "Hawaiian pizza",             "price": 6},
    {"name": "Meat Lovers pizza",          "price": 6},
    {"name": "Pasta",            "price": 8.5},
    {"name": "Bread Stick",         "price": 4.5},
    {"name": "Classic Cheese pizza",       "price": 5.5},
    {"name": "Veg Hot 'n' Spicy pizza",    "price": 5.5},
    {"name": "Chicken Curry ",         "price": 8.5},
    {"name": "Butter Panner Curry",       "price": 13.5},
    {"name": "Sushi",        "price": 9.5},
    {"name": "Hot Chips", "price": 4.5},
    {"name": "Roast chicken",         "price": 16.5},
    {"name": "Coke 1.5L",             "price": 3.5},
    {"name": "Fanta 1.5L",             "price": 3.5},
    {"name": "Sprite 1.5L",             "price": 3.5},
    {"name": "Noodles",             "price": 7.5},
    {"name": "Cake (10 inch)",             "price": 10.5},
    {"name": "Cupcakes(10 pack)",             "price": 10.5},
)


# defines exception; this is to be raised when an order is cancelled
class CancelOrder(Exception):
    pass


# class with default order details
class Order():
    def __init__(self):
        self.pickup = True

        self.name = ""
        self.address = None
        self.phone = None

        self.number_items = 0
        self.items = []

        self.total_cost = 0


def get_input(regex, input_message=None, error_message=None, ignore_case=True):
    """Gets valid input, validated using regular expressions."""
    # loops until input is valid ("break" is called)
    while True:
        # input to validate, input prompt is as specified
        u_input = input(str(input_message))

        # check if the user wants to quit or cancel the order
        lower = u_input.lower()
        if lower == "qq" or lower == "quit":
            sys.exit()
        elif u_input == "cc" or u_input == "cancel":
            raise CancelOrder()

        # check if the input matches the regex provided
        if ignore_case:
            if re.match(regex, u_input, re.IGNORECASE):
                break
        else:
            if re.match(regex, u_input):
                break

        # if it doesn't match, and an error message has been specified
        if error_message:
            print(str(error_message))

    return u_input


def print_order(order):
    print("| Name: {}".format(order.name))
    print("| Order type: {}".format("Pickup"  if order.pickup else "Delivery"))
    print("")
    print ("| \tDiscount\t\t\t\t\t$ {:>5.2f}".format
            (discount_value))
    order.total_cost -=  discount_value
    print ("| \tG.S.T\t\t\t\t\t$ {:>5.2f}".format
            (gst))
    order.total_cost *=  gst
    
    if not order.pickup:
        print("| Delivery address: {}".format(order.address))
        print("| Customer phone number: {}".format(order.phone))
    print("|\n| Order summary:\t\t\t\tPrice each:\tSubtotal:")
    for item in order.items:
        print("| \t{}x {:<22}\t${:<6.2f}\t\t${:>5.2f}".format(
            item['amount'], item['name'],
            item['price'], item['price']*item['amount']))

    if not order.pickup:
            print("| \tDelivery charge\t\t\t\t\t$ {:>5.2f}".format(
                delivery_charge))

    print("| {:61}--------".format(""))
    print("| {:54} Total: ${:.2f}".format("", order.total_cost))


print("Welcome to ùn rístorantē dí kríśh")
print ("")
print("Enter 'CC' to cancel order, or 'QQ' to exit menu at any time")


# list to hold all completed orders
orders = []

# sorts item list by price, then alphabetically
items_available = sorted(
    items_available,
    key=lambda k: (k["price"], k["name"]))

# keep getting orders, only exits through sys.exit()
while True:
    # try ... except to catch CancelOrder exception
    try:
        print("\nNew Order")
        order = Order()

        # get delivery/pickup type
        user_input = get_input(
            r"$|(?:P|D)",
            "Pickup or delivery? :",
            "Please enter a 'p' (pickup) or a 'd' (delivery)")
        if user_input.lower().startswith("d"):
            order.pickup = False
         # get delivery/pickup type

        def yes_or_no(question):
            answer = input(question + "(y/n): ").lower().strip()
            print("")
            while not(answer == "y" or answer == "yes" or \
            answer == "n" or answer == "no"):
                print("Input yes or no")
                answer = input(question + "(y/n):").lower().strip()
                print("")
            if answer[0] == "y":
                return True
                discount_value = 2
            else:
                return False
                discount_value = 0
        
        if yes_or_no("are you returning customer"):
            print("Welcome back")
            print("We are rewarding you with a discount")
            print("Thank you for your royalty")
            discount_value = 2
           
            
        else:
            print(":(")
            discount_value = 0
            

        # get name info
        order.name = get_input(
            r"[A-Z]+$",
            "Enter customer name:",
            "Name must only contain letters")

        # get address, phone number info (if the customer wants delivery)
        if not order.pickup:
            order.address = get_input(
                r"[ -/\w]+$",
                "Delivery address:",
                "Address must only contain alphanumeric characters")
            order.phone = get_input(
                r"\d+$",
                "Phone number:",
                "Phone number must only contain numbers")



        # print menu (each item is assigned a number)
        print("\nMenu")
        for i, item in enumerate(items_available):
            # each item's number is its index (i) + 1,
            # so the first item is 1
            print("{}: {}".format(str(i+1).zfill(2), item['name']))


        # get number of items to order,
        # make sure it is more than 0,less than max_items
        while True:
            user_input = get_input(
                r"\d$",
                "Number of items to order:",
                "Must be a digit, 5 or less")
            user_input = int(user_input)
            if 0 < user_input <= max_items:
                order.number_items = user_input
                break
            else:
                print("Must be a digit, 5 or less (but more than 0)")
                       
        print("\nEnter your selection number for each item you want to buy")
        for i in range(order.number_items):
            while True:
                string = "item #{} of {}:".format(i+1, order.number_items)
                user_input = get_input(
                    r"\d\d?$",
                    string,
                    "Item selection number must"
                    "correspond to those listed above")
                user_input = int(user_input)
                try:
                    if user_input == 0:
                        raise IndexError
                    # selects the item based on user_input
                    to_add = items_available[user_input-1]

                    # if the item has already been ordered,
                    # increment the amount ordered
                    for ordered in order.items:
                        if to_add["name"] == ordered["name"]:
                            ordered["amount"] += 1
                            break
                    # else add the item to the order list
                    else:
                        order.items.append(to_add)
                        order.items[-1]["amount"] = 1

                    # if there has been no error,
                    # input is valid, break from the while loop
                    break

                except IndexError:
                    print("item selection number must"
                        "correspond to those listed above")
                        
        
        order.total_cost = sum(
            item["price"]*item["amount"]
            for item in order.items)
            
        if not order.pickup:
                order.total_cost += delivery_charge
               # add order to list of orders
        orders.append(order)
        print("\nYour Order Was Saved. Order was:")
        print_order(order)

        user_input = get_input(
            r"$|(?:Y|N|O).*",
            "Would you like to enter another order or view all"
                "previous orders? [Yes]/No/Orders:",
            "Only yes/no or \"orders\" responses allowed")
        if user_input.lower().startswith("o"):
            for i, order in enumerate(orders):
                print("-" * 73)
                print_order(order)
                if i == len(orders) + 1:
                    print("-" * 73)
        elif user_input.lower().startswith("n"):
            sys.exit()

    except CancelOrder:
        try:
            print("\nOrder cancelled")
            user_input = get_input(
                r"$|(?:Y|N).*",
                "Would you like to enter another order? [Yes]/No",
                "Only yes or no responses allowed")
            if user_input.lower().startswith("n"):
                sys.exit()

        except CancelOrder:
            print("Type 'QQ' to exit the program")






















