import states
class Heal():
    name = ''
    cost = 0
    heals = 0
    level = 0
    def __init__(self, name, cost, heals, level):
        self.name = name
        self.cost = cost
        self.heals = heals
        self.level = level
    def detail_str(self):
        detail = f"{self.name} (Heals: {self.heals}, Cost: {self.cost})"
        return detail
class Buff():
    name = ''
    cost = 0
    atkadd = 0
    duration = 0
    level = 0
    value_buffer = 0
    def __init__(self, name, cost, atkadd, duration, level, value_buffer):
        self.name = name
        self.cost = cost
        self.atkadd = atkadd
        self.duration = duration
        self.level = level
        self.value_buffer = value_buffer
    def detail_str(self):
        detail = f"{self.name} (Cost: {self.cost}, Attack Boost: {self.atkadd}, Duration: {self.duration})"
        return detail
class Boost_Magic():
    name = ''
    cost = 0
    attr_to_boost = ''
    boost_amt = 0
    duration = 0
    level = 0
    value_buffer = 0
    def __init__(self, name, cost, attr_to_boost, boost_amt, duration, level, value_buffer):
        self.name = name
        self.cost = cost
        self.attr_to_boost = attr_to_boost
        self.boost_amt = boost_amt
        self.duration = duration
        self.level 
        self.value_buffer = value_buffer
    def detail_str(self):
        detail = f"Name: {self.name} (Cost: {self.cost}, Attribute Boosted: {self.attr_to_boost}, Boost Amount: {self.boost_amt}, Duration: {self.duration})"
        return detail

healI = Heal('Heal I', 5, 50, 0)
healII = Heal('Heal II', 7, 80, 3)
healIII = Heal('Heal III', 10, 120, 5)
healIV = Heal('Heal IV', 13, 175, 7)
healV = Heal('Heal V', 17, 250, 10)

heal_spells = [healI, healII, healIII, healIV, healV] ##

buffI = Buff('Buff I', 7, 5, 2, 2, 0)
buffII = Buff('Buff II', 9, 10, 5, 7, 0)
buffIII = Buff('Buff III', 11, 16, 6, 11, 0)

buff_spells = [buffI, buffII, buffIII] ## 

quickenI = Boost_Magic('Quicken I', 5, 'speed', 5, 3, 2, 0)
quickenII = Boost_Magic('Quicken II', 8, 'speed', 15, 4, 10, 0)
quickenIII = Boost_Magic('Quicken III', 10, 'speed', 30, 5, 17, 0)

boost_spells = [quickenI, quickenII, quickenIII] ##

class attack_spell():
    name = ''
    damage = 0
    cost = 0
    kind = ''
    affliction = ''
    level = 0
    aoe = False
    def __init__(self, name, damage, cost, kind, affliction, level, aoe):
        self.name = name
        self.damage = damage  
        self.cost = cost
        self.kind = kind
        self.affliction = affliction 
        self.level = level
        self.aoe = aoe
    def detail_str(self):
        detail = f"{self.name} (Damage: {self.damage}, Cost: {self.cost}, Kind: {self.kind}, Affliction: {self.affliction.name})"
        return detail

raze1 = attack_spell('Raze I', 15, 7, 'P', states.normal, 5, False)
raze2 = attack_spell('Raze II', 30, 15, 'P', states.normal, 8, False)

scorched_earth = attack_spell('Scorched Earth', 50, 20, 'P', states.fire, 20, False) # sakura final

earth_spells = [raze1, raze2, scorched_earth] ##

fireball = attack_spell('Fireball', 10, 5, 'M', states.fire, 5, False)
fireball2 = attack_spell('Fireball II', 15, 8, 'M', states.fire, 7, False)
grand_fireball = attack_spell('Grand Fireball', 35, 15, 'M', states.fire, 15, False)

napalm = attack_spell("Napalm", 45, 20, 'P', states.fire, 17, False) # kurita final

fire_spells = [fireball, fireball2, grand_fireball, napalm] ##

icecicle_spear = attack_spell("Icecicle Spear", 10, 7, "M", states.frozen, 5, False)
icecicle_spear2 = attack_spell("Icecicle Spear II", 15, 12, "M", states.frozen, 7, False)
iceberg = attack_spell("Iceberg", 40, 20, 'P', states.frozen, 15, False)

glacier = attack_spell("Glacier", 60, 20, 'P', states.frozen, 18, False) # ralf final

ice_spells = [icecicle_spear, icecicle_spear2, iceberg, glacier] ##

zipzip = attack_spell("Zip", 12, 8, 'M', states.electrified, 7, False)
zapzap = attack_spell("Zap", 20, 10, 'M', states.electrified, 9, False)
lightning = attack_spell("Lightning", 32, 20, 'M', states.electrified, 13, False) 

gigavolt_blast = attack_spell("Gigavolt Blast", 52, 27, 'M', states.electrified, 20, False) 

luminaire = attack_spell("Luminaire", 65, 23, 'M', states.normal, 24, False) # protag final

electric_spells = [zipzip, zapzap, lightning, gigavolt_blast, luminaire] ##

all_spells = [heal_spells, buff_spells, boost_spells, earth_spells, fire_spells, ice_spells, electric_spells] ##

#Enemy-specific spells 

ground_fault = attack_spell("Ground Fault", 10, 5, 'M', states.normal, 0, False)
sigil_of_fire = attack_spell("Sigil of Fire", 12, 7, 'M', states.fire, 0, False)
sigil_of_earth = attack_spell("Sigil of Earth", 15, 8, 'P', states.normal, 0, False)
sigil_of_ice = attack_spell("Sigil of Ice", 16, 9, 'M', states.frozen, 0, False)
sigil_of_darkness = attack_spell("Sigil of Darkness", 22, 17, 'M', states.normal, 0, True)
viscious_incantation = attack_spell("Viscious Incantation", 25, 19, 'M', states.normal, 0, True)
dreadful_hymn = attack_spell("Dreadful Hymn", 24, 12, 'M', states.normal, 0, True)
reality_inversion = attack_spell("Reality Inversion", 30, 8, 'M', states.normal, 0, True)

magical_protection = Boost_Magic("Magical Protection", 7, 'resistance', 7, 3, 0, 0)
ominous_wind = Boost_Magic("Ominous Wind", 10, 'speed', 10, 5, 0, 0)

#Boss-specific spells 

#Magus
barrier = Boost_Magic('Barrier', 10, 'resistance', 20, 4, 0, 0)
dark_mist = attack_spell('Dark Mist', 15, 8, 'M', states.normal, 0, False)
dark_matter = attack_spell("Dark Matter", 30, 8, 'M', states.normal, 0, True)
#Magus II
barrier2 = Boost_Magic('Barrier II', 7, 'resistance', 50, 7, 0, 0)
shadow_scythe = attack_spell('Shadow Scythe', 45, 8, 'M', states.normal, 0, False)
eternal_darkness = attack_spell("Eternal Darkness", 60, 8, 'M', states.normal, 0, True)

#Erika
rainbow_storm = attack_spell("Rainbow Storm", 15, 7, 'M', states.normal, 0, False)
wind_waltz = attack_spell("Wind Waltz", 20, 11, 'P', states.normal, 0, False)
#Erika II  
rainbow_hurricane = attack_spell('Rainbow Hurricane', 35, 12, 'M', states.normal, 0, True)
tornado_tango = Boost_Magic('Tornado Tango', 10, 'speed', 40, 6, 0, 0)

#Zombor
flame_strike = attack_spell("Flame Strike", 10, 5, 'P', states.fire, 0, False)
annihilation_ray = attack_spell("Annihilation Ray", 20, 7, 'M', states.electrified, 0, False)

#Zeal 
starburst = attack_spell("Starburst", 60, 12, "M", states.normal, 0, True)
gears_of_darkness = attack_spell("Gears of Darkness", 30, 6, "M", states.electrified, 0, True)
evil_within = attack_spell("Evil Within", 44, 9, 'M', states.normal, 0, False)