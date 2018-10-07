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
    return s['id'], [(x['unit_price'], x['quantity']) for x in s['buys']], [(x['unit_price'], x['quantity']) for x in s['sells']]


if __name__ == '__main__':
    s = API.getPrices(71334)
    print(s)
    print(parse_prices(s))

    s = API.getListings(71334)
    print(s)
    print(parse_listings(s))
