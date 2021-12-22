
class Gens:
    def __init__(self, name, _id, price, info):
        self.name = name
        self.id = _id
        self.price = price
        self.info = info
        self.amount = 0

    def edit(self, name=None, price=None, info=None):
        if name is not None:
            self.name = name
        if price is not None:
            self.price = price
        if info is not None:
            self.info = info

    def sell(self, amount):
        self.amount -= amount

    def buy(self, amount):
        self.amount += amount


class Core:
    def __init__(self):
        self.genses = []
        self.last_gens_id = 0
        self.total_sell = 0

    def add_gens(self, name, price, info):
        self.last_gens_id += 1
        new_gens = Gens(name, self.last_gens_id, price, info)
        self.genses.append(new_gens)

    def get_gens(self):
        return self.genses

    def sell(self, _id, amount):
        for gens in self.genses:
            if gens.id == _id:
                gens.sell(amount)
                self.total_sell += gens.price * amount
