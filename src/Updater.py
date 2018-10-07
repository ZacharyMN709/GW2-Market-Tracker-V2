import time
import src.API_Link as API
import src.Database_Link as DB
from Objects.Item import MalformedItemError
from Objects.Recipe import MalformedRecipeError

# region Printing & Time

def check_char_print(out, count):
    if(count % 25 == 0): out += " "
    if(count % 50 == 0): out += str(count) + '\n'
    print(out, end="")
    return out


def get_time():
    return time.asctime(time.localtime(time.time()))

# endregion

# region Updaters

def update_item_table(start=None, end=None):
    count = 0
    direc = "../Logs/"
    lst = API.get_item_list()
    if start:
        lst = lst[start - 1:]
        count = start - 1
    if end:
        lst = lst[:end]

    print("Items in list: " + str(len(lst)))
    market = DB.DatabaseLink()

    # Update the logs with the most recent run time.
    with open(direc + 'ErrantItems.txt', 'w') as e:
        e.write(get_time() + '\n')
    with open(direc + 'ItemsMasterList.txt', 'w') as i:
        i.write(get_time() + '\n')

        # Get every item in the list, and attempt to create and save it
        for x in lst:
            count += 1
            try:
                item = API.get_item(x)
                item.set_craftable()
                check_char = item.save_item_to_db()
            except MalformedItemError as err:
                check_char = '!'
                with open(direc + 'ErrantItems.txt', 'a') as e:
                    e.write("Ct: {}  -  {}\n".format(count, err))
            i.write(check_char_print(check_char, count))

    market.close()


def update_recipe_table(start=None, end=None):
    count = 0
    direc = "../Logs/"
    lst = API.get_recipe_list()
    if start:
        lst = lst[start -1:]
        count = start -1
    if end:
        lst = lst[:end]

    print("Recipes in list: " + str(len(lst)))
    market = DB.DatabaseLink()

    # Update the logs with the most recent run time.
    with open(direc + 'ErrantRecipes.txt', 'w') as e:
        e.write(get_time() + '\n')
    with open(direc + 'RecipeMasterList.txt', 'w') as i:
        i.write(get_time() + '\n')

        # Get every recipe in the list, and attempt to create and save it
        for x in lst:
            count += 1
            try:
                recipe = API.get_recipe(x)
                check_char = recipe.save_recipe_to_db(market)
            except MalformedRecipeError:
                check_char = "!"
                with open(direc + 'ErrantRecipes.txt', 'a') as err:
                    e.write("Ct: {}  -  {}\n".format(count, err))
            i.write(check_char_print(check_char, count))

    market.close()

# endregion


if __name__ == '__main__':
    update_recipe_table()
    #update_item_table()
