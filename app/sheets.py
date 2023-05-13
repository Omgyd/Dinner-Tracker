import gspread


gc = gspread.service_account(filename="app/static/creds.json")


def get_dish_list():
    sh = gc.open("Dinner List")
    dinner_list = sh.sheet1.get_all_values()
    dish_list = []

    for i in range(2, len(dinner_list)):
        dish_list.append(dinner_list[i])

    return dish_list
