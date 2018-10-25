import src.Database_Link as DB
from Objects.Recipe import Recipe


class MalformedItemError(Exception):
    def __init__(self, message):
        super().__init__(message)

# TODO - Implement Memoization


MAX_COST = 99999999
SAVE_ITEM_QUERY = "INSERT INTO Items VALUES (?, ?, ?, ?, ?);"
IS_CRAFTABLE_QUERY = "SELECT recID FROM Recipes WHERE itmID = ?"
ITEM_IN_DATABSE = "SELECT * FROM Items WHERE itmID = ?"


class Item:
    items = {}

    def __new__(cls, itmID, name, icon, sellable, craftable):
        """
        Memoizes the object, so recursion is both quicker and updates objects globally
        """
        if itmID in Item.items:
            return Item.items[itmID]
        else:
            self = Item.items[itmID] = super(Item, cls).__new__(cls)
            return self

    def __init__(self, itmID, name, icon, sellable, craftable):
        # Static Properties
        self.itmID = itmID
        self.name = name
        self.icon = icon
        self.sellable = sellable
        self.craftable = craftable
        self.db_link = DB.DatabaseLink()

        # Dynamic Properties
        self.merchant_price = None
        self.optimal_recipe = None
        self.optimal_price = None

        # Function Calls
        self.get_merchant_price()
        self.get_optimals()

    def __str__(self):
        return "ItemID: {}\n"\
               "Name: {}\n"\
               "Sellable: {}\n"\
               "Craftable: {}\n"\
               "Icon: {}".format(
                self.itmID,
                self.name,
                "True" if self.sellable else "False",
                "True" if self.craftable else "False",
                self.icon
                )

    def get_merchant_price(self):
        # TODO - Fill out and retrieve from database
        self.merchant_price = MAX_COST

    def get_optimals(self, time=None):
        # Recursively travel the recipes to determine the optimal item cost, and acquisition method.
        try:
            if time: cost = (MAX_COST, "Purchase")  # TODO - Get time-based instance
            else: cost = (MAX_COST, "Purchase")  # TODO - Get most recent
        except DatabaseError: cost = (MAX_COST, "Purchase")

        if self.merchant_price <= cost[0]: cost = (self.merchant_price, "Merchant")

        for recipe in Recipe.by_item_id(self.itmID):
            try:
                # Sum all the components needed after multiplying them by the amount needed for crafting.
                subcost = sum([Item.by_item_id(y[0]).get_optimals(time)[0] * y[1] for y in recipe.compnonents])
                if subcost < cost[0]: cost = (subcost, recipe)
            except MalformedItemError as e:
                print(e)

        self.optimal_price, self.optimal_recipe = cost
        return cost

    def get_price(self):
        if not self.optimal_price: self.get_optimals()
        return self.optimal_price

    def set_craftable(self):
        self.craftable = len(self.db_link.conn.execute(IS_CRAFTABLE_QUERY, (self.itmID,)).fetchall()) > 0

    def save_item_to_db(self):
        """
        Saves item to database, or skips it if already present.
        :return: '.' or ','. '.' indicates the item was added, ',' indicates it was already there.
        """
        if not self.db_link.conn.execute(ITEM_IN_DATABSE, (self.itmID,)).fetchall():
            self.db_link.conn.execute(SAVE_ITEM_QUERY, (self.itmID, self.name, self.icon, self.sellable, self.craftable))
            self.db_link.conn.commit()
            return "."
        else:
            return ","

    @classmethod
    def from_web(cls, s):
        """
        Initialises the object from the API response
        """
        itmID, name, icon, sellable = s.get('id'), s.get('name'), s.get('icon'), 'NoSell' not in s.get('flags')

        if (name is None) or (icon is None):
            if (name is None) and (icon is None):
                raise MalformedItemError("Name and icon are 'None' for item with ID {}".format(itmID))
            if name is None:
                raise MalformedItemError("Name is 'None' for item with ID {}".format(itmID))
            else:
                raise MalformedItemError("Icon is 'None' for item with ID {}".format(itmID))
        return cls(itmID, name, icon, sellable, None)

    @classmethod
    def by_item_id(cls, itmID):
        """
        :param itmID: The item ID
        :return: Item object
        """
        db_link = DB.DatabaseLink()
        try: item = db_link.conn.execute(ITEM_IN_DATABSE, (itmID,)).fetchall()[0]
        except IndexError: raise MalformedItemError("Item {} not found in database.".format(itmID))
        return cls(item[0], item[1], item[2], item[3], item[4])


if __name__ == '__main__':
    i = Item.by_item_id(71334)
    print(i)
