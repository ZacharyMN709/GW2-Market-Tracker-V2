import src.API_Link as API
import src.Parser as Parser
from Objects.Item import Item
from Objects.Recipe import Recipe

#######################
### Struct Trawlers ###
#######################

def TrawlRecipeByOutput(ids, prt=True):
    d = dict()
    out, s, = API.searchRecipeByOutput(ids)

    if out == "?":
        out, d = Parser.parse_recipes_from_item(s)
    if (prt): print(out, end="")
    return out, d


def TrawlCraftingTree(ids, tree=False):
    print("Trawling Recipes and Items...")

    def getDynamData(ids, tree, spaces=0):
        new_items = dict()
        new_recipes = dict()
        final_out = []
        item_out, l = API.get_item(ids)
        new_items[ids] = l
        out, d = TrawlRecipe(ids, prt=False)
        if (d): new_recipes[ids] = d
        for y in d:
            for z in d.get(y):
                o, n, i = getDynamData(z[0], tree, spaces + 2)
                if n: new_recipes.update(n)
                if i: new_items.update(i)
                final_out += o

        fout = str(ids) + "- " + out + " " + item_out
        if (tree):
            if (spaces >= 2):
                print(" " * (spaces - 2) + "v-" + fout)
            else:
                print(fout)
        else:
            if ("O" in out or "U" in out):
                print(".", end="")
            else:
                print("!", end="")
        final_out.append(fout)
        return final_out, new_recipes, new_items

    def CharCheck(s):
        c1, c2 = s[-1], s[-5]
        error = (c1 in "D12!?") or (c1 in "D12!?")
        return error

    f_out, recipes, items = getDynamData(ids, tree=tree)
    f_out.sort(reverse=True)
    count = 0
    out = "O"
    print()
    for x in f_out:
        count += 1
        if (CharCheck(x)): out = "!"
        space = "   "
        if (not tree):
            LinePrint(str(x), count)

    print()
    return out, recipes, items
#############################################
