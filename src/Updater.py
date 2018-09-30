import time
import src.Trawler as Trawler
import src.API_Link as API
import src.Database_Link as DB
from sqlite3 import IntegrityError
from Objects.Item import MalformedItemError



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
    check, lst = API.get_item()
    if check != '?':
        return
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
    def AttemptRecipeTrawl(ids, count):
        out, recipe = Trawler.TrawlRecipe(ids, prt=False)
        if(out in "OU"):
            out = "."
        elif(out == "S"):
            return AttemptRecipeTrawl(ids, count)
        elif(out in "12"):
            out = "!"
        else:
            out = "."

        return out, recipe

    count = 0
    direc = "../Logs/"
    check, lst = API.getRecipe()
    if check != '?':
        return
    if start:
        lst = lst[start -1:]
        count = start -1
    if end:
        lst = lst[:end]
    print("Recipes in list: " + str(len(lst)))

    with open(direc + 'ErrantRecipes.txt', 'w') as e:
        e.write(getTime() + '\n')
    with open(direc + 'RecipeMasterList.txt', 'w') as l:
        l.write(getTime() + '\n')

    market = DB.DatabaseLink('gw2_market_data')
    query = "INSERT INTO Recipes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
    classes = ['Artificer', 'Armorsmith', 'Chef', 'Huntsman', 'Jeweler', 'Leatherworker', 'Tailor', 'Weaponsmith', 'Scribe']

    for x in lst:
        count += 1
        out, recipe = AttemptRecipeTrawl(x, count)
        if out == "." and 'upgrade_id' not in recipe:
            market.conn.execute(query, [x, recipe['itmID'], recipe['count'], str([(a['item_id'], a['count']) for a in recipe['components']]), recipe['count']] + [c in recipe['crafter_class'] for c in classes])
        else:
            with open(direc + 'ErrantRecipes.txt', 'a') as e:
                e.write(str(count) + "-" + str(x) + ": " + str(recipe) + "\n")
        with open(direc + 'RecipeMasterList.txt', 'a') as l:
            l.write(IterPrint(out, count))
    market.commit()
    market.close()


if __name__ == '__main__':
    ## TODO - Add in more robust handling of trawling.
    ## Skip entries already found, and give the option to wipe and start over.
    #TrawlAllRecipes()
    TrawlAllItems()
