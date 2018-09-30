class MalformedRecipeError(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)


SAVE_RECIPE_QUERY = "INSERT INTO Recipes VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
CRAFTING_CLASSES = ['Artificer', 'Armorsmith', 'Chef', 'Huntsman', 'Jeweler', 'Leatherworker', 'Tailor', 'Weaponsmith', 'Scribe']


class Recipe:

    def __init__(self, recID, itmID, count, craft_time, components,
                 artificer, armorsmith, chef, huntsman, jeweler, leatherworker, tailor, weaponsmith, scribe):
        self.recID = recID
        self.itmID = itmID
        self.count = count
        self.craft_time = craft_time
        self.component = components
        self.by_artificer = artificer
        self.by_armorsmith = armorsmith
        self.by_chef = chef
        self.by_huntsman = huntsman
        self.by_jeweler = jeweler
        self.by_leatherworker = leatherworker
        self.by_tailor = tailor
        self.by_weaponsmith = weaponsmith
        self.by_scribe = scribe


    @classmethod
    def from_web(cls, recID, itmID, count, craft_time, classes, components):
        cls(recID, itmID, count, craft_time, components, [x in classes for x in CRAFTING_CLASSES])
        #{'itmID': s['output_item_id'], 'count': s['output_item_count'], 'craft_time': s['time_to_craft_ms'],
        # 'crafter_class': s['disciplines'], 'components': s['ingredients']}