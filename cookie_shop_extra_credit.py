import csv

def bake_cookies(filepath):
    cookies = []
    with open(filepath, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cookie = {
                'id': int(row['id']),
                'title': row['title'],
                'description': row['description'],
                'price': float(row['price'].replace('$', '')),
                'sugar_free': row['sugar_free'].lower() == 'yes',
                'gluten_free': row['gluten_free'].lower() == 'yes',
                'contains_nuts': row['contains_nuts'].lower() == 'yes'
            }
            cookies.append(cookie)
    return cookies

def welcome():
    print("Welcome to the Python Cookie Shop!")
    print("We feed each according to their need.\n")

def ask_dietary_restrictions():
    restrictions = {
        'allergic_to_nuts': False,
        'allergic_to_gluten': False,
        'avoiding_sugar': False
    }

    print("We'd hate to trigger an allergic reaction in your body. So please answer the following questions:")

    while True:
        answer = input("Are you allergic to nuts? (yes/no): ").strip().lower()
        if answer in ['yes', 'y', 'no', 'n']:
            restrictions['allergic_to_nuts'] = answer in ['yes', 'y']
            break
        else:
            print("Invalid response. Please answer 'yes' or 'no'.")

    while True:
        answer = input("Are you allergic to gluten? (yes/no): ").strip().lower()
        if answer in ['yes', 'y', 'no', 'n']:
            restrictions['allergic_to_gluten'] = answer in ['yes', 'y']
            break
        else:
            print("Invalid response. Please answer 'yes' or 'no'.")

    while True:
        answer = input("Do you suffer from diabetes? (yes/no): ").strip().lower()
        if answer in ['yes', 'y', 'no', 'n']:
            restrictions['avoiding_sugar'] = answer in ['yes', 'y']
            break
        else:
            print("Invalid response. Please answer 'yes' or 'no'.")

    return restrictions

def display_cookies(cookies, restrictions):
    print("Here are the cookies we have in the shop for you:\n")
    for cookie in cookies:
        if (restrictions['allergic_to_nuts'] and cookie['contains_nuts']) or \
           (restrictions['allergic_to_gluten'] and not cookie['gluten_free']) or \
           (restrictions['avoiding_sugar'] and not cookie['sugar_free']):
            continue
        print(f"#{cookie['id']} - {cookie['title']}")
        print(f"{cookie['description']}")
        print(f"Price: ${cookie['price']:.2f}\n")

def get_cookie_from_dict(id, cookies):
    for cookie in cookies:
        if cookie['id'] == id:
            return cookie
    return None

def solicit_quantity(id, cookies):
    cookie = get_cookie_from_dict(id, cookies)
    while True:
        try:
            quantity = int(input(f"My favorite! How many {cookie['title']} would you like? "))
            if quantity < 0:
                raise ValueError
            subtotal = quantity * cookie['price']
            print(f"Your subtotal for {quantity} {cookie['title']} is ${subtotal:.2f}.")
            return quantity
        except ValueError:
            print("Please enter a valid quantity.")

def solicit_order(cookies):
    order = []
    while True:
        user_input = input("Please enter the number of any cookie you would like to purchase (type 'finished' if finished with your order): ").strip().lower()
        if user_input in ['finished', 'done', 'quit', 'exit']:
            break
        try:
            cookie_id = int(user_input)
            if get_cookie_from_dict(cookie_id, cookies):
                quantity = solicit_quantity(cookie_id, cookies)
                order.append({'id': cookie_id, 'quantity': quantity})
            else:
                print("Invalid cookie ID. Please enter a valid ID.")
        except ValueError:
            print("Invalid input. Please enter a valid ID or 'finished' to complete your order.")
    return order

def display_order_total(order, cookies):
    print("\nThank you for your order. You have ordered:\n")
    total = 0
    for item in order:
        cookie = get_cookie_from_dict(item['id'], cookies)
        quantity = item['quantity']
        subtotal = quantity * cookie['price']
        total += subtotal
        print(f"-{quantity} {cookie['title']}")
    print(f"\nYour total is ${total:.2f}.")
    print("Please pay with Bitcoin before picking-up.\n")
    print("Thank you!\n-The Python Cookie Shop Robot.")

def run_shop(cookies):
    welcome()
    restrictions = ask_dietary_restrictions()
    display_cookies(cookies, restrictions)
    order = solicit_order(cookies)
    display_order_total(order, cookies)
