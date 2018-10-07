from gw2api import GuildWars2Client  # https://github.com/JuxhinDB/gw2-api-interface
import urllib3.exceptions as U3
import requests.exceptions as REQ
import time
from Objects.Item import Item
from Objects.Recipe import Recipe

TIMEOUT = 10
baseURL = "https://api.guildwars2.com/v2/"
API = None
gw2 = GuildWars2Client(api_key=API)


# region Connection Safety

def connection_safety_wrapper(method_to_run, ids=None, url=None):
    """
    This function is an encapsulating function which protects the code from crashing from connection errors
    or the API being down. If there is an error, it will retry the connection in a predetermined amount of time.

    :param method_to_run: A reference to a function which accesses the particular API endpoint
    :param ids: The ids to be trawled. Can be None, int or list of ints.
    :param url: An override for some of the API endpoints. This effectively
    :return: None if the response is 'empty' or the response.
    """

    def check_response(s):
        """
        :param s: The API response.
        :return: A character which represents the validity of the response.
        """
        a = str(s)
        if a == "":                                 check_char = "U"
        elif a == "{'text': 'no such id'}":         check_char = "U"
        elif a == "[]":                             check_char = "U"
        elif a == "{}":                             check_char = "U"
        elif a == "{'text': 'API not active'}":     check_char = "D"
        elif a == "{'text': 'too many requests'}":  check_char = "S"
        else:                                       check_char = "?"

        return check_char

    check_char = 'E'
    while check_char in "DESU":
        try:
            if url:   s = method_to_run(id=ids, url=url, timeout=TIMEOUT)
            elif ids: s = method_to_run(id=ids, timeout=TIMEOUT)
            else:     s = method_to_run(timeout=TIMEOUT)
        except ConnectionError:
            print("\nConnection Error Handled - VAN", end=" ")
        except U3.ConnectionError:
            print("\nConnection Error Handled - U3", end=" ")
        except REQ.ConnectionError:
            print("\nConnection Error Handled - REQ", end=" ")
        except TimeoutError:
            print("\nTimeout Error Handled", end=" ")
        else:
            check_char = check_response(s)

        if check_char == 'D':
            print("\nAPI is down. Attempting to continue in 10 minutes.\n")
            time.sleep(600)
        elif check_char == 'E':
            print("\nAttempting to continue in 30 seconds.\n")
            time.sleep(30)
        elif check_char == 'S':
            print("\nRequest limit reached. Attempting to continue in 30 seconds.\n")
            time.sleep(30)
        elif check_char == 'U':
            print("\nEmpty info returned. Attempting to continue in 30 seconds.\n")
            time.sleep(30)
        else:
            return s

# endregion


# region API Accessors

def get_recipe_list():
    """
    :return: The list of all in-game recipe IDs
    """
    return connection_safety_wrapper(gw2.recipes.get)


def get_recipe(ids):
    """
    :param ids: The recipe ID
    :return: The object for the Recipe
    """
    return Recipe.from_web(connection_safety_wrapper(gw2.recipes.get, ids=ids))


def searchRecipeByOutput(ids):
    """
    :param ids: The item ID
    :return: The ID for the recipe
    """
    return connection_safety_wrapper(gw2.recipesbyitem.get, ids=ids,
                                     url=baseURL + 'recipes/search?output=' + str(ids))


def searchRecipeByInput(ids):
    """
    :param ids: The item ID
    :return: The ID for the recipe
    """
    return connection_safety_wrapper(gw2.recipessearch.get, ids=ids,
                                     url=baseURL + 'recipes/search?input=' + str(ids))


def get_item_list():
    """
    :return: The list of all in-game item IDs
    """
    return connection_safety_wrapper(gw2.items.get)


def get_item(ids):
    """
    :param ids: The item ID
    :return: The object for the Item
    """
    return Item.from_web(connection_safety_wrapper(gw2.items.get, ids=ids))


def getPrices(ids):
    return connection_safety_wrapper(gw2.commerceprices.get, ids=ids)


def getListings(ids):
    return connection_safety_wrapper(gw2.commercelistings.get, ids=ids)


def getBuys():
    return connection_safety_wrapper(gw2.commercetransactions.history.buys.get)


def getSells():
    return connection_safety_wrapper(gw2.commercetransactions.history.sells.get)


def checkAPI():
    """
    :return: True is the API is active, false otherwise.
    """
    s = connection_safety_wrapper(gw2.tokeninfo.get)
    return not str(s) == "{'text': 'API not active'}"

# endregion

