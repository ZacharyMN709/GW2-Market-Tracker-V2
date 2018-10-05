import time
import src.Trawler as Trawler
import src.API_Link as API
import src.Database_Link as DB
from sqlite3 import IntegrityError
from Objects.Item import MalformedItemError
from Objects.Recipe import MalformedRecipeError



###############################
### Formatting and Printing ###
###############################
def IterPrint(out, count):
    if(count % 25 == 0): out += " "
    if(count % 50 == 0): out += str(count) + '\n'
    print(out, end="")
    return out

def getTime(): return time.asctime(time.localtime(time.time()))
def getTimestamp(): return '"' + getTime() + '",'
##############################################



####################
### Master Lists ###
####################

def TrawlAllItems(start=None, end=None):
    count = 0
    direc = "../Logs/"
    lst = API.get_item_list()
    if start:
        lst = lst[start - 1:]
        count = start - 1
    if end:
        lst = lst[:end]

    print("Items in list: " + str(len(lst)))

    market = DB.DatabaseLink('gw2_market_data')

    with open(direc + 'ItemsMasterList.txt', 'w') as i:
        # Update the log time with the most recent run.
        i.write(getTime() + '\n')
        with open(direc + 'ErrantItems.txt', 'w') as e:
            # Update the log time with the most recent run.
            e.write(getTime() + '\n')

        for x in lst:
            count += 1
            check_char = "."
            if not market.conn.execute("SELECT itmID FROM Items WHERE itmID = ?", (x,)).fetchall():
                try:
                    item = API.get_item(x)
                    item.set_craftable(market)
                    item.save_item_to_db(market)
                except MalformedItemError as err:
                    check_char = '!'
                    with open(direc + 'ErrantItems.txt', 'a') as e:
                        e.write("Ct: {}  -  {}\n".format(count, err))
            i.write(IterPrint(check_char, count))
    market.close()


def TrawlAllRecipes(start=None, end=None):
    count = 0
    direc = "../Logs/"
    lst = API.get_recipe_list()
    if start:
        lst = lst[start -1:]
        count = start -1
    if end:
        lst = lst[:end]

    print("Recipes in list: " + str(len(lst)))

    market = DB.DatabaseLink('gw2_market_data')

    with open(direc + 'RecipeMasterList.txt', 'w') as l:
        l.write(getTime() + '\n')
        with open(direc + 'ErrantRecipes.txt', 'w') as e:
            e.write(getTime() + '\n')

        for x in lst:
            count += 1
            check_char = "."
            try:
                recipe = API.get_recipe(x)
                recipe.save_item_to_db(market)
            except MalformedRecipeError:
                check_char = "!"
                with open(direc + 'ErrantRecipes.txt', 'a') as err:
                    e.write("Ct: {}  -  {}\n".format(count, err))
            with open(direc + 'RecipeMasterList.txt', 'a') as l:
                l.write(IterPrint(check_char, count))
    market.close()


if __name__ == '__main__':
    ## TODO - Add in more robust handling of trawling.
    ## Skip entries already found, and give the option to wipe and start over.
    #TrawlAllRecipes()
    TrawlAllItems()
