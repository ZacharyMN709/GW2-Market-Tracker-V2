import time
import os
import sqlite3
import src.Trawler as Trawler
import src.API_Link as API

market, inventory = None, None


#####################
### Database Code ###
#####################
def connect_db():
    """
    Connect to the database and return the connection.

    Keyword arguments:
    test -- boolean flag to indicate whether or not to use the testing database (default False)
    """

    ## __enter__, __exit__
    market = sqlite3.connect(os.path.join(os.curdir, 'gw2_market_data.db'), check_same_thread=False)
    market.row_factory = sqlite3.Row

    inventory = sqlite3.connect(os.path.join(os.curdir, 'gw2_personal_inventory.db'), check_same_thread=False)
    inventory.row_factory = sqlite3.Row
    return market, inventory


def close_db():
    """Close the connection to the database."""
    market.close()
    inventory.close()


def init_db():
    """Initialize a database from the schema file."""
    market, inventory = connect_db()
    with open('market_data_schema.sql', mode='r') as a:
        market.cursor().executescript(a.read())
        market.commit()
    with open('inventory_data_schema', mode='r') as b:
        inventory.cursor().executescript(b.read())
        inventory.commit()

    print('Initialized the database.')


###############################
### Formatting and Printing ###
###############################
def LinePrint(s, c, m=4):
    space = "   "
    if(c % m == 0): space = "\n"
    print(s, end=space)

def IterPrint(out, count):
    if(count % 25 == 0): out += " "
    if(count % 50 == 0): out += str(count) + '\n'
    print(out, end="")
    return out

def printSleep(count):
    # TODO - Use .format to print
    print("\n" + getTime() + "\nRequest Limit Reached at Count: " + str(count))
    print("Sleeping thread. Attempting to continue in 30 seconds.\n")
    mod = (count - 1) % 50
    spacer = (" " * mod) + (" " * (mod > 25))
    print(spacer, end='')
    time.sleep(30)

def getTime(): return time.asctime( time.localtime(time.time()) )
def getTimestamp(): return '"' + getTime() + '",'
##############################################



####################
### Master Lists ###
####################

def TrawlAllItems(start=None, end=None):
    ## Convert file to utf-8
    def AttemptItemTrawl(ids, count):
        out, item = Trawler.TrawlItem(ids, forceloop=True)
        if(out == "O"):
            out = "."
        elif(out == "S"):
            printSleep(count)
            return AttemptItemTrawl(ids, count)
        elif(out in "U12"):
            out = "!"

        return out, item

    count = 0
    direc = "../Logs/"
    check, lst = API.getItem()
    if check != '?':
        return
    if start:
        lst = lst[start - 1:]
        count = start - 1
    if end:
        lst = lst[:end]

    print("Items in list: " + str(len(lst)))

    with open(direc + 'ItemsMasterList.txt', 'w') as i:
        i.write(getTime() + '\n')
    with open(direc + 'ErrantItems.txt', 'w') as e:
        e.write(getTime() + '\n')

    conn, _ = connect_db()
    query = "INSERT INTO Items VALUES (?, ?, ?, ?, ?);"
    craftable_query = "SELECT recID FROM Recipes WHERE itmID = ?"

    for x in lst:
        count += 1
        out, item = AttemptItemTrawl(x, count)
        if out == ".":
            craftable = conn.execute(craftable_query, (x,)).fetchall()
            conn.execute(query, (x, item[0], item[1], item[2], len(craftable) > 0))
        else:
            with open(direc + 'ErrantItems.txt', 'a') as e:
                e.write(str(count) + "-" + str(x) + ": " + str(item) + "\n")
        with open(direc + 'ItemsMasterList.txt', 'a') as i:
            i.write(IterPrint(out, count))
    conn.commit()
    conn.close()


def TrawlAllRecipes(start=None, end=None):
    def AttemptRecipeTrawl(ids, count):
        out, recipe = Trawler.TrawlRecipe(ids, prt=False, forceloop=True)
        if(out in "OU"):
            out = "."
        elif(out == "S"):
            printSleep(count)
            return AttemptRecipeTrawl(ids, count)
        elif(out in "12"):
            out = "!"
        else:
            out = "."

        return out, recipe

    count = 0
    direc = "../Logs"
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

    conn, _ = connect_db()
    query = "INSERT INTO Recipes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
    classes = ['Artificer', 'Armorsmith', 'Chef', 'Huntsman', 'Jeweler', 'Leatherworker', 'Tailor', 'Weaponsmith', 'Scribe']

    for x in lst:
        count += 1
        out, recipe = AttemptRecipeTrawl(x, count)
        if out == "." and 'upgrade_id' not in recipe:
            conn.execute(query, [x, recipe['itmID'], recipe['count'], str([(a['item_id'], a['count']) for a in recipe['components']]), recipe['count']] + [c in recipe['crafter_class'] for c in classes])
        else:
            with open(direc + 'ErrantRecipes.txt', 'a') as e:
                e.write(str(count) + "-" + str(x) + ": " + str(recipe) + "\n")
        with open(direc + 'RecipeMasterList.txt', 'a') as l:
            l.write(IterPrint(out, count))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    ## TODO - Add in more robust handling of trawling.
    ## Skip entries already found, and give the option to wipe and start over.
    #TrawlAllRecipes()
    TrawlAllItems(start=20000+1)
