import json
import jsonpickle
from beer import Beer, Inventory

inv = Inventory()


def json_serialize(_filename, _object):
    with open('data/'+_filename+'.json', 'w', encoding='utf-8') as output:
        json.dump(json.loads(jsonpickle.encode(_object, unpicklable=False)), output, indent=4, ensure_ascii=False)


with open('data/beers.json', encoding='utf-8') as beers_json:
    data = json.load(beers_json)
    for b in data:
        inv.push(Beer(b['type'], b['name'], b['id'], b['price'], b['alcohol'], b['ingredients'], b['isCan']), b['brand'])


feladat1 = inv
feladat2 = inv.search_by_type("Búza")
feladat3 = inv.cheapest_brand()
feladat4 = inv.lack_of_ingredient("búza")
feladat5 = inv.create_water_list()

json_serialize('feladat1', feladat1)
json_serialize('feladat2', feladat2)
json_serialize('feladat3', feladat3)
json_serialize('feladat4', feladat4)
json_serialize('feladat5', feladat5)