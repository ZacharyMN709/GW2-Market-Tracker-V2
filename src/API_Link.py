from gw2api import GuildWars2Client
# https://github.com/JuxhinDB/gw2-api-interface
import urllib3.exceptions as U3
import requests.exceptions as REQ
import time
from Objects.Item import Item

TIMEOUT = 10
baseURL = "https://api.guildwars2.com/v2/"
API = None
gw2 = GuildWars2Client(api_key=API)

####################################
### Connection and Data Safeties ###
####################################
def connection_safety_wrapper(methodToRun, ids=None, url=None):
    s = ""
    try:
        if(url): s = methodToRun(id=ids, url=url, timeout=TIMEOUT)
        elif(ids): s = methodToRun(id=ids, timeout=TIMEOUT)
        else: s = methodToRun(timeout=TIMEOUT)
    except ConnectionError: print("\nConnection Error Handled - VAN")
    except U3.ConnectionError: print("\nConnection Error Handled - U3")
    except REQ.ConnectionError: print("\nConnection Error Handled - REQ")
    except TimeoutError: print("\nTimeout Error Handled")

    check_char = check_response(s)

    if check_char == 'D':
        time.sleep(600)
        print("API is down. Attempting to continue in 10 minutes.\n")
        return connection_safety_wrapper(methodToRun, ids, url)
    elif check_char == 'S':
        time.sleep(30)
        print("Request limit reached. Attempting to continue in 30 seconds.\n")
        return connection_safety_wrapper(methodToRun, ids, url)
    elif check_char == 'U':
        return None
    else:
        return s


def check_response(s):
    a = str(s)

    if a == "": check_char = "!"
    elif a == "{'text': 'no such id'}": check_char = "U"
    elif a == "[]": check_char = "U"
    elif a == "{}": check_char = "U"
    elif a == "{'text': 'API not active'}": check_char = "D"
    elif a == "{'text': 'too many requests'}": check_char = "S"
    else: check_char = "?"

    return check_char

#####################
### API Accessors ###
#####################
def getRecipe(ids=None):
    return connection_safety_wrapper(gw2.recipes.get, ids=ids)


def searchRecipeByOutput(ids):
    return connection_safety_wrapper(gw2.recipesbyitem.get, ids=ids,
                                     url=baseURL + 'recipes/search?output=' + str(ids))


def searchRecipeByInput(ids):
    return connection_safety_wrapper(gw2.recipessearch.get, ids=ids,
                                     url=baseURL + 'recipes/search?input=' + str(ids))


def get_item(ids=None):
    s = connection_safety_wrapper(gw2.items.get, ids=ids)
    item = Item.from_web(ids, s.get('name'), s.get('icon'), 'NoSell' not in s.get('flags'))
    return item


def getPrices(ids):
    return connection_safety_wrapper(gw2.commerceprices.get, ids=ids)


def getListings(ids):
    return connection_safety_wrapper(gw2.commercelistings.get, ids=ids)


def getBuys():
    return connection_safety_wrapper(gw2.commercetransactions.history.buys.get)


def getSells():
    return connection_safety_wrapper(gw2.commercetransactions.history.sells.get)


def checkAPI():
    s = connection_safety_wrapper(gw2.tokeninfo.get)
    if str(s) == "{'text': 'API not active'}":
        return False
    else:
        return True

