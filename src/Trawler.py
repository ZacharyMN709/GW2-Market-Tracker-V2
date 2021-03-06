import src.API_Link as API
import time
from Objects.Item import Item
from Objects.Recipe import Recipe
from src.Database_Link import DatabaseLink as DB
import threading


TRAWL_TIME = 300.0
START_TIME = time.time()
PATH = 'C:\\Users\\Zachary\\Documents\\GitHub\\GW2-Market-Tracker-V2\\Logs\\'
SAVE_PRICE_QUERY = "INSERT INTO Market VALUES (?, ?, ?, ?, ?, ?);"
TRAWL_COUNTER = 0
TRAWL_MAX = 10


def get_display_time():
    return time.asctime(time.localtime(time.time()))


def get_timestamp_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


class Trawler:

    # TODO - Better implement instances of objects.
    def __init__(self, itmID):
        self._instance = TRAWL_COUNTER
        self._start = START_TIME + ((TRAWL_TIME / TRAWL_MAX) * TRAWL_COUNTER) % TRAWL_TIME
        self.itmID = itmID
        self.items = dict()
        self.recipes = dict()
        self.craft_tree = str()
        self._travel_crafting_tree(self.itmID)
        self._filename = PATH + 'Item Trawl Log - {}.txt'.format(self.itmID)
        with open(self._filename, 'a') as file:
            file.write('\nTrawler {} Initialized at {}\n'.format(self._instance, get_display_time()))
        self.db = DB()

    def __str__(self):
        return self.craft_tree

    def __enter__(self):
        global TRAWL_COUNTER
        TRAWL_COUNTER += 1

    def __exit__(self, exc_type, exc_val, exc_tb):
        global TRAWL_COUNTER
        TRAWL_COUNTER -= 1
        self.db.close()

    def _travel_crafting_tree(self, item_id, spaces=0):
        # Get the item by ID and add to the dictionary
        item = Item.by_item_id(item_id)
        self.items[item.itmID] = item

        # Crate a tree shaped string for __str__ method.
        if spaces:
            '╠ ╚ ═ ║ ╬'
            self.craft_tree += "{}╚{}\n".format(" " * (spaces-1), item.itmID)
        else:
            self.craft_tree += "Crafting tree for: {}\n{}\n".format(self.itmID, item.itmID)

        # Get the recipes related to the item and add to the dictionary
        recipes = tuple(Recipe.by_item_id(item_id))

        if recipes:
            self.recipes[item.itmID] = recipes
            # For each recipe get the item ID from each component set, and recur
            for recipe in recipes:
                if len(recipes) > 1:
                    self.craft_tree += (' '*spaces) + '----------'
                for component_pair in recipe.components:
                    self._travel_crafting_tree(component_pair[0], spaces=spaces+1)
                if len(recipes) > 1:
                    self.craft_tree += (' ' * spaces) + '----------'

    def trawl(self, count='Manual'):
        with open(self._filename, 'a') as file:
            file.write("{}: Loop #{} - Starting Trawl...\n".format(get_display_time(), count))
            timestamp = (get_timestamp_time(),)
            internal_count = 0
            for i in self.items:
                price_tuple = API.get_prices(i)
                if price_tuple:
                    self.db.conn.execute(SAVE_PRICE_QUERY, timestamp + price_tuple)
                    file.write("{}: .    ".format(i))
                else:
                    file.write("{}: !    ".format(i))
                internal_count += 1
                if internal_count % 6 == 0: file.write("\n")
            self.db.commit()
            file.write("{}: Loop #{} - Trawl Complete\n\n".format(get_display_time(), count))

    def async_loop(self):
        def loop():
            count = 0
            while True:
                self.trawl(count)
                count += 1
                time.sleep(TRAWL_TIME - ((time.time() - self._start) % TRAWL_TIME))
        threading.Thread(target=loop()).start()


if __name__ == '__main__':
    damask = Trawler(71334)
    cloth = Trawler(46741)
    square = Trawler(46739)
    damask.async_loop()
