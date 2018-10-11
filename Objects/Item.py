import src.Database_Link as DB


class MalformedItemError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


SAVE_ITEM_QUERY = "INSERT INTO Items VALUES (?, ?, ?, ?, ?);"
IS_CRAFTABLE_QUERY = "SELECT recID FROM Recipes WHERE itmID = ?"
ITEM_IN_DATABSE = "SELECT * FROM Items WHERE itmID = ?"


class Item:

    def __init__(self, itmID, name, icon, sellable, craftable):
        self.itmID = itmID
        self.name = name
        self.icon = icon
        self.sellable = sellable
        self.craftable = craftable
        self.db_link = DB.DatabaseLink()

    def __str__(self):
        return "ItemID: {}"\
               "Name: {}"\
               "Sellable: {}"\
               "Craftable: {}"\
               "Icon: {}".format(
                self.itmID,
                self.name,
                "True" if self.sellable else "False",
                "True" if self.craftable else "False",
                self.icon
        )

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
        item = db_link.conn.execute(ITEM_IN_DATABSE, (itmID,)).fetchall()[0]
        return cls(item[0], item[1], item[2], item[3], item[4])


if __name__ == '__main__':
    i = Item.by_item_id(71334)
    print(i)
