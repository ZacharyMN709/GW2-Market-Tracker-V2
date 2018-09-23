import src.API_Link as API

'''
## TODO - Implement current crafted market price when pandas is added
def GetCraftPrice(ids, time):
    cost = 999999999
    if ids in recipes:
        d = recipes.get(ids)
        for x in d:
            subcost = 0
            for y in d.get(x):
                subcost += GetCraftPrice(y[0], time) * y[1]
            if (cost > subcost): cost = subcost
        buy = 1000000  ##data[ids][time][2]
        if buy:
            if (cost > buy): cost = buy
    else:
        cost = 1000000  ##data[ids][time][2]
    if ids in merchant:
        if (cost > merchant.get(ids)): cost = merchant.get(ids)
    return cost


def GetDamaskPrice(time):
    cloth = GetCraftPrice(46741, time)
    square = GetCraftPrice(46739, time)
    cost = cloth + square
    ##    buy = data[ids][time][2]
    ##    if buy:
    ##         if(cost > data[ids][time][2]): cost = data[ids][time][2]
    return cost, cloth, square
'''


def parse_recipes_from_item(s):
    """
    :param s: A list of recipe ids, which is the output of searching recipes by output
    :return: The dictionary of recipes for an item.
    """

    out = dict()
    for x in s:
        out[x] = parse_recipe(API.getRecipe(x)[1])
    return out


def parse_recipe(s):
    """
    :param s: API Recipe JSON Object
    :return: The dictionary of relevant recipe data
    """

    out = {'itmID': s['output_item_id'], 'count': s['output_item_count'], 'craft_time': s['time_to_craft_ms'],
           'crafter_class': s['disciplines'], 'components': s['ingredients']}
    return out


def parse_item(s):
    """
    :param s: API Item JSON Object
    :return: Tuple containing: (Item Name, Item Icon Link, Sellable)
    """
    out = (s.get('name'), s.get('icon'), 'NoSell' not in s.get('flags'))
    return out


def parse_prices(s):
    """
    :param s: API Prices JSON Object
    :return: Tuple containing: (Item ID, Buy Prc., Quy Qty., Sell Prc., Sell Qty.)
    """
    vals = (s['id'], s['buys']['unit_price'], s['buys']['quantity'], s['sells']['unit_price'], s['sells']['quantity'])
    return vals


def parse_listings(s):
    """
    :param s: API Listings JSON Object
    :return: Tuple containing: (Item ID, (Buy Tuple), (Sell Tuple))
    The Buy and Sell tuples have (Prc., Qty.) pairs as entries.
    """
    return s['id'], ((x['unit_price'], x['quantity']) for x in s['buys']), ((x['unit_price'], x['quantity']) for x in s['sells'])

