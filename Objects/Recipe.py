import src.Database_Link as DB

class MalformedRecipeError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


SAVE_RECIPE_QUERY = "INSERT INTO Recipes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
RECIPE_IN_DATABSE = "SELECT * FROM Recipes WHERE recID = ?"
CRAFTING_CLASSES = ('Artificer', 'Armorsmith', 'Chef', 'Huntsman', 'Jeweler', 'Leatherworker', 'Tailor', 'Weaponsmith', 'Scribe')


class Recipe:

    def __init__(self, recID, itmID, count, craft_time, components, crafters):
        self.recID = recID
        self.itmID = itmID
        self.count = count
        self.craft_time = craft_time
        self.components = components
        self.crafters = tuple(crafters)
        self.by_artificer = self.crafters[0]
        self.by_armorsmith = self.crafters[1]
        self.by_chef = self.crafters[2]
        self.by_huntsman = self.crafters[3]
        self.by_jeweler = self.crafters[4]
        self.by_leatherworker = self.crafters[5]
        self.by_tailor = self.crafters[6]
        self.by_weaponsmith = self.crafters[7]
        self.by_scribe = self.crafters[8]
        self.db_link = DB.DatabaseLink()

        """
        self.recID, self.itmID, self.count, self.craft_time, self.component, self.crafters,
        self.by_artificer, self.by_armorsmith, self.by_chef, self.by_huntsman, self.by_jeweler,
        self.by_leatherworker,self.by_tailor, self.by_weaponsmith, self.by_scribe
        """

    def __str__(self):
        return "Recipe ID: {}\n" \
               "Item ID and Count: {}, {}\n" \
               "Craft Time: {}\n" \
               "Components: {}\n" \
               "Crafter List: {}\n".format(
                self.recID,
                self.itmID, self.count,
                self.craft_time,
                self.components,
                self.crafters
        )

    def save_recipe_to_db(self):
        """
        Saves recipe to database, or skips it if already present.
        :return: '.' or ','. '.' indicates the recipe was added, ',' indicates it was already there.
        """
        if not self.db_link.conn.execute(RECIPE_IN_DATABSE, (self.recID,)).fetchall():
            tup = (self.recID, self.itmID, self.count, str(self.components), self.craft_time,
                   self.by_artificer, self.by_armorsmith, self.by_chef, self.by_huntsman, self.by_jeweler,
                   self.by_leatherworker, self.by_tailor, self.by_weaponsmith, self.by_scribe)
            self.db_link.conn.execute(SAVE_RECIPE_QUERY, tup)
            self.db_link.conn.commit()
            return "."
        else:
            ## TODO - Update if recipe already in DB
            return ","

    @classmethod
    def from_web(cls, s):
        """
        Initialises the object from the API response
        """
        recID, itmID, count, craft_time = s.get('id'), s.get('output_item_id'), s.get('output_item_count'), s.get('time_to_craft_ms')
        components = s.get('ingredients')
        crafters = [(x in s.get('disciplines')) for x in CRAFTING_CLASSES]

        if 'upgrade_id' in s: raise MalformedRecipeError("Guild Items not handled. Recipe ID: {}".format(recID))
        return cls(recID, itmID, count, craft_time, components, crafters)

    @classmethod
    def from_rec_table(cls, recID):
        db_link = DB.DatabaseLink()
        recipe = db_link.conn.execute(RECIPE_IN_DATABSE, (recID,)).fetchall()[0]
        return cls(recipe[0], recipe[1], recipe[2], recipe[3], recipe[4], recipe[5:])


if __name__ == '__main__':
    r = Recipe.from_rec_table(10122)
    print(r)
