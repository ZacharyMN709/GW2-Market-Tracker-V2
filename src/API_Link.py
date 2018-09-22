from gw2api import GuildWars2Client
# https://github.com/JuxhinDB/gw2-api-interface
import urllib3.exceptions as U3
import requests.exceptions as REQ

timeout = 10
baseURL = "https://api.guildwars2.com/v2/"
API = None
gw2 = GuildWars2Client(api_key=API)

####################################
### Connection and Data Safeties ###
####################################
def ConnSafety(methodToRun, ids=None, url=None, retry=True, forceloop=False):
    s = ""
    try:
        if(url): s = methodToRun(id=ids, url=url, timeout=timeout)
        elif(ids): s = methodToRun(id=ids, timeout=timeout)
        else: s = methodToRun(timeout=timeout)
        retry = False
    except ConnectionError: print("\nConnection Error Handled - VAN")
    except U3.ConnectionError: print("\nConnection Error Handled - U3")
    except REQ.ConnectionError: print("\nConnection Error Handled - REQ")
    except ConnectionResetError: print("\nConnection Reset Error Handled")
    except TimeoutError: print("\nTimeout Error Handled")
    finally:
        if(retry):
            if(forceloop):
                s = ConnSafety(methodToRun, ids=ids, url=url, retry=True, forceloop=True)
                print("CAUTION! MAY BE STUCK IN INFINITE LOOP!")
            else: s = ConnSafety(methodToRun, ids=ids, url=url, retry=False)

    # TODO - Work in control structure based on API response
    return VetResponse(s)


def VetResponse(s):
    a = str(s)

    if(a == ""): out = "!"
    elif(a == "{'text': 'no such id'}"): out = "U"
    elif(a == "[]"): out = "U"
    elif(a == "{}"): out = "U"
    elif(a == "{'text': 'API not active'}"): out = "D"
    elif(a == "{'text': 'too many requests'}"): out = "S"
    else: out = "?"

    return out, s

#####################
### API Accessors ###
#####################
def getRecipe(ids=None, forceloop=False):
    return ConnSafety(gw2.recipes.get, ids=ids, forceloop=forceloop)


def searchRecipeByOutput(ids, forceloop=False):
    return ConnSafety(gw2.recipesbyitem.get, ids=ids,
                      url=baseURL + 'recipes/search?output=' + str(ids), forceloop=forceloop)


def searchRecipeByInput(ids, forceloop=False):
    return ConnSafety(gw2.recipessearch.get, ids=ids,
                      url=baseURL + 'recipes/search?input=' + str(ids), forceloop=forceloop)


def getItem(ids=None, forceloop=False):
    return ConnSafety(gw2.items.get, ids=ids, forceloop=forceloop)


def getPrices(ids, forceloop=False):
    return ConnSafety(gw2.commerceprices.get, ids=ids, forceloop=forceloop)


def getListings(ids, forceloop=False):
    return ConnSafety(gw2.commercelistings.get, ids=ids, forceloop=forceloop)


def getBuys():
    return ConnSafety(gw2.commercetransactions.history.buys.get)


def getSells():
    return ConnSafety(gw2.commercetransactions.history.sells.get)


def checkAPI():
    s = ConnSafety(gw2.tokeninfo.get)
    if (str(s) == "{'text': 'API not active'}"):
        return False
    else:
        return True

