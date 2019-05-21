class Health_Potion():
    name = ''
    increase_amt = 0
    cost = 0
    def __init__(self, name, increase_amt, cost):
        self.name = name
        self.increase_amt = increase_amt
        self.cost = cost
    def detail_str(self):
        detail = f"{self.name} (Heals: {self.increase_amt})"
        return detail
    
health_potion = Health_Potion('Small Health Potion', 20, 50)
health_potion2 = Health_Potion("Medium Health Potion", 50, 75)
health_potion3 = Health_Potion("Large Health Potion", 75, 100)

potions = [health_potion, health_potion2, health_potion3]

class Ether():
    name = ''
    increase_amt = 0
    cost = 0
    def __init__(self, name, increase_amt, cost):
        self.name = name
        self.increase_amt = increase_amt
        self.cost = cost
    def detail_str(self):
        detail = f"{self.name} (Heals: {self.increase_amt})"
        return detail

ether = Ether("Small Ether", 15, 100)
ether2 = Ether("Medium Ether", 20, 150)
ether3 = Ether("Large Ether", 40, 350)

ethers = [ether, ether2, ether3]

all_items = potions + ethers