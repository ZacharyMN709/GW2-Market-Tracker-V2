class MalformedItemError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


SAVE_ITEM_QUERY = "INSERT INTO Items VALUES (?, ?, ?, ?, ?);"
IS_CRAFTABLE_QUERY = "SELECT recID FROM Recipes WHERE itmID = ?"


class Item:

    def __init__(self, itmID, name, icon, sellable, craftable):
        self.itmID = itmID
        self.name = name
        self.icon = icon
        self.sellable = sellable
        self.craftable = craftable

    def set_craftable(self, db_link):
        self.craftable = len(db_link.conn.execute(IS_CRAFTABLE_QUERY, (self.itmID,)).fetchall()) > 0

    def save_item_to_db(self, db_link):
        db_link.conn.execute(SAVE_ITEM_QUERY, (self.itmID, self.name, self.icon, self.sellable, self.craftable))
        db_link.conn.commit()

    @classmethod
    def from_web(cls, itmID, name, icon, sellable):
        if (name is None) or (icon is None):
            if (name is None) and (icon is None):
                raise MalformedItemError("Name and icon are 'None' for item with ID {}".format(itmID))
            if name is None:
                raise MalformedItemError("Name is 'None' for item with ID {}".format(itmID))
            else:
                raise MalformedItemError("Icon is 'None' for item with ID {}".format(itmID))
        return cls(itmID, name, icon, sellable, None)
