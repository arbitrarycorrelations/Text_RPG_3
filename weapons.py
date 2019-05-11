class Weapon():
    name = ''
    tier = ''
    atk = 0
    mag = 0
    elemental_affinity = ''
    cost = 0
    description = ''
    def __init__(self, name, tier, atk, mag, elemental_affinity, cost, description):
        self.name = name
        self.tier = tier
        self.atk = atk
        self.mag = mag
        self.elemental_affinity = elemental_affinity
        self.cost = cost
        self.description = description
    def change_affinity(self):
        while True:
            affinities = ['I', 'L', 'G', 'F']
            affinities_long = ['Ice', 'Lightning', 'Ground', 'Fire']
            print("Change affinity to what?")
            desired_affinity = input(" 1: Ice\n 2: Lightning\n 3: Ground\n 4: Fire\n > ")
            try:
                desired_affinity = int(desired_affinity)
            except ValueError:
                print(f"Choose 1, 2, 3, or 4, not {desired_affinity}")
                print()
                continue
            try:
                self.elemental_affinity = affinities[desired_affinity-1]
                print(f"{self.name} now has an affinity for {affinities_long[desired_affinity-1]}")
                print(self.elemental_affinity)
            except IndexError:
                print(f"Choose 1, 2, 3, or 4, not {str(desired_affinity)}") 
                print()  
                continue 
    
fisticuffs = Weapon('Fisticuffs', 'F', 0, 0, 'None', 0, 'Fists and feet. Not very powerful.')
## Player ##
baseSword = Weapon('Iron Sword', 'D', 20, 5, 'None', 0, 'A makeshift sword good in a pinch.')
swordII = Weapon('Silver Sword', 'B', 35, 10, 'None', 1200, 'A sword used by knights.')
lightningSword = Weapon('Lightning Sword', 'A', 40, 40, 'L', 3000, 'A legendary sword forged from lightning. Boosts DEF by 3.')

swords = [baseSword, swordII, lightningSword]

handAxe = Weapon('Hand Axe', 'C', 25, 0, 'None', 0, 'A lumberjack\'s axe.')
handAxeII = Weapon('Silver Hand Axe', 'A', 45, 18,'None', 1100, 'A battle axe popular with fiends and brigands.')
lightningAxe = Weapon('Lightning Axe', 'A', 25, 40, 'L', 2920, 'An axe forged from lightning. Boosts ATK by 3.')

axes = [handAxe, handAxeII, lightningAxe]

poleArm = Weapon('Iron Polearm', 'D', 15, 15, 'G', 0, 'A simple spear.')
poleArmII = Weapon('Silver Polearm', 'B', 30, 25, 'G', 1750, 'A polearm used by the Royal Guard.')
poleArmIII = Weapon('Draco\'s Polearm', 'A', 45, 45, 'G', 3050, 'A legendary polearm used by the Greek monarch Draco. Boosts SPD by 5.')

polearms = [poleArm, poleArmII, poleArmIII]

wand = Weapon('Wooden Wand', 'D', 10, 25, 'F', 0, "A makeshift wand constructed from a branch.")
wandII = Weapon('Iron Wand', 'B', 10, 40, 'F', 1850, 'An iron wand used by mages in the Royal Army.')
wandIII = Weapon('Athena\'s Kiss', 'A', 20, 50, 'F', 5200, 'The wand used by the legendary goddess Athena. Boosts MAG by 5.')

wands = [wand, wandII, wandIII]

all_weapons = [swords, axes, polearms, wands]

## Boss ##

#Zombor
club = Weapon('Cast Iron Club', 'A', 55, 0, 'G', 0, 'A heaping hunk of iron used to bash those who defy its wielder.')

#Erika
throwing_knives = Weapon('Masamune\'s Tantō', 'A', 40, 10, 'S', 0, 'Throwing daggers made by Japan\'s legendary swordsmith Gorō Masamune.')
#Erika II  
zanmato = Weapon("Zanmato", 'S', 50, 20, 'S', 0, "A katana forged from demonic ore. Erika's final weapon.")

#Magus 
moonfall_scythe = Weapon("Moonfall Scythe", 'A', 25, 30, 'S', 0, 'A famous scythe wielded by a shadowy dark mage.')
#Magus II  
dreamreaper = Weapon("Dreamreaper", 'S', 35, 50, 'S', 0, "A scythe seething with shadow magic. Magus's final weapon.")

#Queen Zeal
suzaku = Weapon("Suzaku", 'S', 50, 50, 'S', 0, "A sword imbued with holy power.")

## Enemy ## 
rocks = Weapon("Rocks", "D", 10, 0, '', 0, "Some rocks, I guess.")

weathered_sword = Weapon('Weathered Sword', 'C', 15, 10, '', 0, 'An old-timey sword that was once quite powerful.')

glaive = Weapon("Glaive", "C", 18, 0, '', 0, "A basic wartime glaive held by the soldier who fell alongside it.")
hammer = Weapon("Double-Handed Hammer", 'B', 20, 15, 'G', 0, "A formidable hammer that is so heavy it requires two hands to hold.")

brass_knuckles = Weapon("Brass Knuckles", 'B', 25, 17, "", 0, "Spiked brass knuckles capable of devastating punches.")
tree_trunk = Weapon("Tree Trunk", "A", 30, 18, 'G', 0, "A tree trunk ripped out of the ground by a huge beast.")

claws = Weapon("Dactyl Claws", "D", 10, 0, '', 0, "The fierce claws of a Dactyl.")

bongo = Weapon("Big Bongo", "C", 12, 2, '', 0, "The bongo drum of a gluttonous drummer.")

imbued_wand = Weapon("Imbued Wand", 'D', 5, 10, '', 0, "A wand imbued with magical strength.")

calmcaster = Weapon("Calmcaster", "C", 10, 15, '', 0, "A soothing wand favored by mages.")

backstabber = Weapon("Backstabber", "A", 14, 16, 'G', 0, "A dagger / wand combo popular with the conniving.")

warped_wand = Weapon("Warped Wand", "A", 12, 24, '', 0, "A possessed wand capable of enslaving its wielder.")

dream_devourer = Weapon("Dream Devourer", "S", 15, 30, 'S', 0, "A wand that draws power from its owner's dreams.")