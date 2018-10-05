class MalformedRecipeError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


SAVE_RECIPE_QUERY = "INSERT INTO Recipes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
CRAFTING_CLASSES = ('Artificer', 'Armorsmith', 'Chef', 'Huntsman', 'Jeweler', 'Leatherworker', 'Tailor', 'Weaponsmith', 'Scribe')


class Recipe:

    def __init__(self, recID, itmID, count, craft_time, components, crafters):
        self.recID = recID
        self.itmID = itmID
        self.count = count
        self.craft_time = craft_time
        self.component = components
        self.crafters = crafters
        self.by_artificer = self.crafters[0]
        self.by_armorsmith = self.crafters[1]
        self.by_chef = self.crafters[2]
        self.by_huntsman = self.crafters[3]
        self.by_jeweler = self.crafters[4]
        self.by_leatherworker = self.crafters[5]
        self.by_tailor = self.crafters[6]
        self.by_weaponsmith = self.crafters[7]
        self.by_scribe = self.crafters[8]


    def save_item_to_db(self, db_link):
        ## TODO -
        db_link.conn.execute(SAVE_RECIPE_QUERY, ("//TODO",))
        db_link.conn.commit()

    @classmethod
    def from_web(cls, recID, itmID, count, craft_time, classes, components):
        # if 'upgrade_id' in recipe: raise MalformedRecipeError
        cls(recID, itmID, count, craft_time, components, (x in classes for x in CRAFTING_CLASSES))

        #{'itmID': s['output_item_id'], 'count': s['output_item_count'], 'craft_time': s['time_to_craft_ms'],
        # 'crafter_class': s['disciplines'], 'components': s['ingredients']}