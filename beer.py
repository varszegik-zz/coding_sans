from operator import attrgetter


class Beer:
    def __init__(self, beertype, name, id_, price, alcohol, ingredients, iscan):
        self.beertype = beertype
        self.name = name
        self.id = id_
        self.price = int(price)
        self.alcohol = alcohol
        self.ingredients = []
        for ing in ingredients:
            self.ingredients.append(Ingredient(ing['id'], ing['ratio'], ing['name']))
        self.isCan = iscan
        self.water = self.water_percentage()

    def contains_ingredient(self, _ingredient):
        """
        This function returns whether the Beer contains the ingredient in param1
       :param _ingredient:
       :return: True if it contains the ingredient in param1, false otherwise
       :rtype:
       """
        for ingredient in self.ingredients:
            if ingredient.name == _ingredient:
                return True
        return False

    def water_percentage(self):
        """
        This function returns the water percentage of the beer,
        which is the sum of all ingredient's percentage subtracted from 1.00
        :return: The percentage of water in the Beer
        """
        water = 1.00
        for ingredient in self.ingredients:
            water -= ingredient.ratio
        return water


class Ingredient:
    def __init__(self, id, ratio, name):
        self.id = id
        self.ratio = float(ratio)
        self.name = name


class Brand:
    def __init__(self, brand, beer):
        self.brand = brand
        self.beers = [beer]
        self.avg_price = None

    def __getstate__(self):
        """
        This function deletes the attribute avg_price from serialization as it might not be initialized
        :return: Returns a copy of itself, without the attribute avg_price
        """
        state = self.__dict__.copy()
        del state['avg_price']
        return state

    def __eq__(self, _brand):
        return self.brand == _brand

    def append(self, _beer):
        self.beers.append(_beer)

    def filter_by_type(self, beertype):
        """
        This function selects all beers that are the type given in param beertype
        :param beertype: Beer type to be searched
        :return: Array of beers in the brand which are the type given in param beertype
        """
        data = []
        for beer in self.beers:
            if beer.beertype == beertype:
                data.append(beer)
        return data

    def average(self):
        """
        Calculates the average price in this brand, if not already calculated. Prices are provided /liter
        :return: The average price of the brand's beers.
        """
        if self.avg_price is None:
            price = 0
            for beer in self.beers:
                price += beer.price
            self.avg_price = price / len(self.beers)
        return self.avg_price

    def lack_of_ingredient(self, _ingredient):
        """
        Returns an array of beers of this brand which does not contain the ingredient given in the parameter.
        :param _ingredient: This is the ingredient the beers should not contain
        :return: An array of beers which are lack of the ingredient in parameter _ingredient
        """
        data = []
        for beer in self.beers:
            if not beer.contains_ingredient(_ingredient):
                data.append(beer)
        return data


class Inventory:
    def __init__(self):
        self.brands = []

    def add_if_exists(self, _beer, _brand):
        """
        The function appends the given beer in param _beer to the brand given in param _brand, if it exists.
        :param _beer: The beer object to be added
        :param _brand: The name of the brand
        :return: Returns True if addition was successful, False otherwise
        """
        for br in self.brands:
            if br == _brand:
                br.append(_beer)
                return True
        return False

    def push(self, _beer, _brand):
        """
        Checks if the given brand exists, and adds to it if it does.
        If it doesn't, then it creates a new brand and adds the beer to it.
        :param _beer: The beer to be added
        :param _brand: The beer's brand
        """
        if not self.add_if_exists(_beer, _brand):
            self.brands.append(Brand(_brand, _beer))

    def search_by_type(self, beertype):
        """
        Returns an array of beers of any brand which are a type of param beertype.
        :param beertype: The type to be searched
        :return: The array of beers that are the type of beertype
        """
        data = []
        for brand in self.brands:
            data = data + brand.filter_by_type(beertype)
        return data

    def cheapest_brand(self):
        """
        Returns the brand's name with the cheapest average price
        :return: The name of the brand which have the lowest average price
        """
        return min(self.brands, key=Brand.average).brand

    def lack_of_ingredient(self, _ingredient):
        """
        Returns an array of beers of any brand which lack the ingredient given in _ingredient
        :param _ingredient: The ingredient that the beers must not contain
        :return: The array of beers
        """
        data = []
        for brand in self.brands:
            data = data + brand.lack_of_ingredient(_ingredient)
        return data

    def create_water_list(self):
        """
        Creates a list of beers in desceding order by water percentage
        :return:
        :rtype:
        """
        data = []
        for brand in self.brands:
            data += brand.beers
        return sorted(data, key=attrgetter('water'), reverse=True)
