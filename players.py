import efuncs
import states
import magic
import random
import weapons
import items
## PLAYER / CHARACTER ##
class Character():
    name = ''
    weapon = ''
    currenthealth = 0
    maxhealth = 0
    attack = 0
    baseattack = 0
    defense = 0
    magic = 0
    basemagic = 0
    spells = []
    mp = 0
    currentmp = 0
    resistance = 0
    speed = 0
    lvl = 0
    xp = 0
    tnl = 0
    state = ''
    armor = {}
    bag = []
    credits = 0
    spells_to_learn = []
    def __init__(self, name, weapon, currenthealth, maxhealth, attack, baseattack, defense, magic, basemagic, spells, mp, currentmp, resistance, speed, lvl, xp, tnl, state, armor, bag, credits, spells_to_learn):
        self.name = name
        self.weapon = weapon
        self.currenthealth = currenthealth
        self.maxhealth = maxhealth
        self.attack = attack
        self.baseattack = baseattack
        self.defense = defense
        #add basedefense for armor 
        self.magic = magic
        self.basemagic = basemagic
        self.spells = spells
        self.mp = mp
        self.currentmp = currentmp
        self.resistance = resistance
        self.speed = speed
        self.lvl = lvl
        self.xp = xp
        self.tnl = tnl
        self.state = state
        self.armor = armor 
        self.bag = bag
        self.credits = credits
        self.spells_to_learn = spells_to_learn
    def print_stats(self):
        print(f"""
{self.name.title()}'s stats are as follows: 
Weapon: {self.weapon.name} 
Current HP: {str(self.currenthealth)} 
Max HP: {str(self.maxhealth)} 
ATK: {str(self.attack)} 
Base ATK: {str(self.baseattack)} 
DEF: {str(self.defense)} 
MAG: {str(self.magic)} 
Base MAG: {str(self.basemagic)}
Spells: [{efuncs.list_print(self.spells)}]
MP: {str(self.mp)} 
Current MP: {str(self.currentmp)}
RES: {str(self.resistance)} 
SPD: {str(self.speed)} 
LVL: {str(self.lvl)} 
XP: {str(self.xp)} 
To next level: {str(self.tnl)}
Bag: [{efuncs.list_print(self.bag)}]
Credits: {str(self.credits)}
""")
    def use_magic(self, target, spell):
        print()
        if spell not in self.spells:
            print(f"{self.name.title()} does not know that spell.")
        else:
            if isinstance(spell, magic.Heal):
                print(f"{self.name.title()} used {spell.name}!")
                if (target.currenthealth + spell.heals) > (target.maxhealth):
                    target.currenthealth = target.maxhealth
                else: 
                    target.currenthealth += spell.heals
                print(f"{target.name.title()}\'s health is now {target.currenthealth}!")
                self.currentmp -= spell.cost
            elif isinstance(spell, magic.Buff):
                increased_by = spell.atkadd
                spell.value_buffer = target.attack
                target.attack += increased_by
                print(f"{target.name.title()}\'s ATK is now {str(target.attack)} for {str(spell.duration)} turns.")
                self.currentmp -= spell.cost
            elif isinstance(spell, magic.Boost_Magic):
                print(f"{self.name} used {spell.name}! {spell.attr_to_boost.title()} + {spell.boost_amt} for {spell.duration} turns.")
                self.currentmp -= spell.cost                
                target.adjust_val(spell.attr_to_boost, spell.boost_amt, spell.duration)
            elif isinstance(spell, magic.attack_spell):
                print(f"{self.name.title()} used {spell.name}!")
                self.magic += spell.damage
                if spell.kind == "P":
                    defense_type = target.defense
                elif spell.kind == "M":
                    defense_type = target.resistance
                spell_damage = (self.magic - defense_type) 
                if spell_damage <= 0:
                    spell_damage = 1
                spell_damage = int(round(spell_damage))
                target.currenthealth -= spell_damage
                print(f"{target.name.title()} took {str(spell_damage)} damage. Their health is now {str(target.currenthealth)}")
                self.magic = self.basemagic + self.weapon.mag
                self.currentmp -= spell.cost
                affliction_yes = random.randint(0, 10)
                if affliction_yes == 8:
                    if spell.affliction == states.fire:
                        states.set_player_state(target, states.fire)
                    elif spell.affliction == states.frozen:
                        states.set_player_state(target, states.frozen)
    def view_spells(self):
        print()
        spelldictionary = efuncs.make_temp_dictionary(self.spells)
        while True:
            try:
                print("Get more info on which spell?")
                print(efuncs.pretty_print(self.spells))  
                detail = int(input(">\t"))             
                spellarg = spelldictionary[detail]
                efuncs.detailed_spell_view(spellarg)
                break    
            except (ValueError, TypeError, IndexError):
                print("Invalid choice.")
                continue
    def player_attack(self, enemy):
        damage = (self.attack - enemy.defense) 
        if damage <= 0:
            damage = 1
        enemy.currenthealth -= damage
        print(f"{self.name.title()} attacks {enemy.name.title()} for {damage} damage!\n{enemy.name.title()}'s health is now {enemy.currenthealth}.")
        if (self.speed - enemy.speed) >= 5:
            print(f"Speed supremacy! {self.name.title()} gets another, weaker hit in!")
            weak_damage = int(round(damage / 2))
            enemy.currenthealth -= weak_damage
            print(f"{enemy.name.title()}\'s health is now {enemy.currenthealth}.")
    def equip_weapon(self, weapon):
        current_weapon = self.weapon
        if weapon.name == 'Athena\'s Kiss':
            print(f"{self.name} equips {weapon.name}. They feel their MAG strengthen.")
            self.basemagic += 5
        if weapon.name == 'Draco\'s Polearm':
            print(f"{self.name} equips {weapon.name}. They feel their feet lighten.")
            self.speed += 5
        if weapon.name == 'Lightning Sword':
            print(f"{self.name} equips {weapon.name}. They feel their skin strengthen.")
            self.defense += 3
        if weapon.name == 'Lightning Axe':
            print(f"{self.name} equips {weapon.name}. They feel like they can deliver stronger blows to the enemy.")
            self.baseattack += 3
        names_vals = {'Athena\'s Kiss': (self.basemagic, 5), 'Draco\'s Polearm': (self.speed, 5), 'Lightning Sword': (self.defense, 3), 'Lightning Axe': (self.baseattack, 3)}
        if current_weapon.name in names_vals.keys():
            resetattr = names_vals[current_weapon.name][0]
            resetamt = names_vals[current_weapon.name][1]
            resetattr -= resetamt
            print(f"{self.name} unequipped {current_weapon.name}. They lost its positive effects.")
        self.weapon = weapon
        self.attack = (self.baseattack + weapon.atk)
        self.magic = (self.basemagic + weapon.mag)
        if self == protag:
            print(f"{self.name} now has an attack of {str(self.attack)} and a magic of {str(self.magic)}. They equipped {self.weapon.name}.")
    def unequip_weapon(self):
        self.attack = self.baseattack
        self.mag = self.basemagic
        print(f"{self.name} now has an attack of {str(self.attack)} and a magic of {str(self.magic)}. They unequipped {self.weapon}.")
        self.weapon = 'Fisticuffs'
    def use_item(self, target, item):
        if item not in self.bag:
            print(f"{self.name} does not have that item in their bag.")
        else:
            if isinstance(item, items.Health_Potion):
                if (item.increase_amt + target.currenthealth) >= target.maxhealth:
                    target.currenthealth = target.maxhealth
                else:
                    target.currenthealth += item.increase_amt
                print(f"{self.name} used {item.name}!\n{target.name}'s HP is now {target.currenthealth}.")
            if isinstance(item, items.Ether):
                if (item.increase_amt + target.currentmp) >= target.mp:
                    target.currentmp = target.mp 
                else:
                    target.currentmp += item.increase_amt
                print(f"{self.name} used {item.name}!\nTarget MP is now {target.currentmp}.")
            self.bag.remove(item)
    def adjust_val(self, attr, amt, duration, spell):
        before_adjust = getattr(self, attr)
        spell.value_buffer = before_adjust
        setattr(self, attr, (before_adjust + amt))
        #Adjust_val takes in a str and val and increments the attr by the val
    def xpcheck(self):
        if self.xp - self.tnl >= 0:
            startlvl = self.lvl
            while (self.xp - self.tnl) >= 0:
                self.lvl += 1
                extraxp = (self.xp - self.tnl)
                self.tnl = round((self.tnl + (self.tnl / 2)))                
                self.currenthealth += 8
                self.maxhealth += 8
                self.baseattack += 5
                self.defense += 5
                self.basemagic += 5
                self.mp += 5
                self.currentmp += 5
                self.resistance += 5
                self.speed += 5
                self.xp = extraxp
                self.attack = (self.baseattack + self.weapon.atk)
                self.magic = (self.basemagic + self.weapon.mag)
            print(f"{self.name.title()} gained {self.lvl - startlvl} level(s)!")
            self.print_stats()
        else: 
            needed = (self.tnl - self.xp)
            print(f"{self.name} needs {str(needed)} more XP to level up.\n")
    def detail_str(self): 
        detail = f"{self.name} (HP: {self.currenthealth} / {self.maxhealth}, ATK: {self.attack}, MAG: {self.magic}, DEF: {self.defense}, RES: {self.resistance}, SPD: {self.speed})"
        return detail

party = []
partynames = []
def add_to_party(char):
    global party
    global partynames
    party.append(char)
    partynames.append(char.name)
    print(f"{char.name} has joined the party.")
def assign_party_leader():
    if len(party) <= 1:
        print("No one else is in contention for party leader.")
    else:
        while True: 
            try:
                desired = int(input(f"\nMake who the party leader?\n{efuncs.pretty_print(party)}\n>\t"))
                desired -= 1
                replacementidx = party.index(party[desired])
                temp = party[0]
                party[0] = 'temp'
                party[0] = party[replacementidx]
                party[replacementidx] = temp
                print(f"{party[0].name} is now the party leader.")
                break
            except ValueError:
                print("Not an option.")
                continue
            except IndexError:
                print("Index error")
                continue
    return party

#Characters
#name, weapon, currenthealth, maxhealth, attack, baseattack, defense, magic, basemagic, spells, mp, currentmp, resistance, speed, lvl, xp, tnl, state, armor, bag, credits, spells_to_learn
protag = Character('protag', weapons.fisticuffs, 140, 140, 15, 15, 15, 15, 15, [magic.healI, magic.fireball, magic.raze1], 45,  45, 15, 10, 1, 0, 50, states.normal, {}, [items.health_potion2], 0, [magic.healII, magic.buffII, magic.raze2, magic.fireball2, magic.luminaire, magic.healIV])

kurita = Character('Kurita', weapons.fisticuffs, 210, 210, 40, 40, 35, 45, 45, [magic.healI, magic.buffI, magic.fireball], 85, 85, 45, 45, 5, 0, 75, states.normal, {}, [], 0, [magic.fireball2, magic.grand_fireball, magic.healIII, magic.healIV, magic.buffIII, magic.napalm])

ralf = Character('Ralf', weapons.fisticuffs, 300, 300, 65, 65, 40, 20, 20, [], 30, 30, 40, 50, 7, 0, 125, states.normal, {}, [], 0, [magic.healII, magic.icecicle_spear, magic.glacier])

sakura = Character('Sakura', weapons.fisticuffs, 250, 250, 20, 20, 25, 60, 60, [magic.healII, magic.buffII, magic.fireball2, magic.raze1, magic.icecicle_spear2, magic.zapzap], 120, 120, 45, 20, 9, 0, 250, states.normal, {}, [], 0, [magic.healIV, magic.healV, magic.raze2, magic.scorched_earth])

all_characters = [protag, kurita, ralf, sakura]
recruitable_chars = [kurita, ralf, sakura]

starting_weapons = [weapons.baseSword, weapons.poleArm, weapons.handAxe, weapons.wand]

def assign_weapon(sw):
    swd = efuncs.make_temp_dictionary(sw)
    while True:
        wp = input(f"\nWhat weapon would you like to wield?\n{efuncs.pretty_print(sw)}\nI: View weapon details\n>\t")
        try:
            if wp in {'i', 'I'}:
                wpdetail = int(input(f"\nView details for what weapon?\n1:\tSword\n2:\tPolearm\n3:\tAxe\n4:\tWand\n>\t"))
                efuncs.weapon_detail(swd[wpdetail])
                continue
            else:
                wp = int(wp)
                protag.equip_weapon(swd[wp])
                break
        except (ValueError, IndexError, KeyError):
            print("That's not an option.")
            continue

## BOSS / ENEMY ##

class Boss():
    name = ''
    weapon = ''
    currenthealth = 0
    maxhealth = 0
    attack = 0
    baseattack = 0
    defense = 0
    magic = 0
    basemagic = 0
    spells = []
    mp = 0
    currentmp = 0
    resistance = 0
    speed = 0
    state = ''
    def __init__(self, name, weapon, currenthealth, maxhealth, attack, baseattack, defense, magic, basemagic, spells, mp, currentmp, resistance, speed, state):
        self.name = name
        self.weapon = weapon
        self.currenthealth = currenthealth
        self.maxhealth = maxhealth
        self.attack = attack
        self.baseattack = baseattack
        self.defense = defense
        self.magic = magic
        self.basemagic = basemagic
        self.spells = spells
        self.mp = mp
        self.currentmp = currentmp
        self.resistance = resistance
        self.speed = speed
        self.state = state 
    def print_boss_stats(self):
        print(f"""
{self.name}\'s stats are as follows: 
Weapon: {self.weapon.name} 
Current HP: {str(self.currenthealth)} 
Max HP: {str(self.maxhealth)} 
ATK: {str(self.attack)} 
Base ATK: {str(self.baseattack)} 
DEF: {str(self.defense)} 
MAG: {str(self.magic)} 
Base MAG: {str(self.basemagic)} 
Spells: [{efuncs.list_print(self.spells)}]
MP: {str(self.mp)} 
Current MP: {str(self.currentmp)}
RES: {str(self.resistance)} 
SPD: {str(self.speed)} 
        """)
    def equip_boss_weapon(self, weapon):
        if weapon.elemental_affinity == 'S':
            self.basemagic += 5
        if weapon == weapons.throwing_knives: 
            self.speed += 5
        if weapon == weapons.club:
            self.baseattack += 3
        self.weapon = weapon 
        self.attack = (self.baseattack + weapon.atk)
        self.magic = (self.basemagic + weapon.mag)
    def enemy_use_magic(self, target, spell):
        print()
        if spell not in self.spells: 
            print(f"{self.name.title()} tried to use a spell that they don\'t know.")
        else: 
            if isinstance(spell, magic.Heal):
                print(f"{self.name.title()} used {spell.name.title()}!")
                if (self.currenthealth + spell.heals) > (self.maxhealth):
                    self.currenthealth = self.maxhealth
                else: 
                    self.currenthealth += spell.heals
                print(f"{self.name.title()}\'s HP is now {self.currenthealth}!")
                self.currentmp -= spell.cost
            elif isinstance(spell, magic.Buff):
                print(f"{self.name.title()} used {spell.name.title()}!")
                spell.value_buffer = self.attack
                self.attack += spell.atkadd
                print(f"{self.name.title()}\'s ATK is now {self.attack}!")
                self.currentmp -= spell.cost
            elif isinstance(spell, magic.attack_spell):
                print(f"{self.name.title()} used {spell.name}!")
                self.magic += spell.damage
                if spell.aoe == True:
                    for player in party:    
                        if spell.kind == "P":
                            defense_type = player.defense
                        elif spell.kind == "M":
                            defense_type = player.resistance
                        spell_damage = (self.magic - defense_type)
                        if spell_damage <= 0:
                            spell_damage = 1 
                        spell_damage = int(round(spell_damage))               
                        player.currenthealth -= spell_damage
                        print(f"{player.name.title()} took {str(spell_damage)} damage. Their health is now {str(player.currenthealth)}")
                else:
                    if spell.kind == "P":
                        defense_type = target.defense
                    elif spell.kind == "M":
                        defense_type = target.resistance
                    spell_damage = (self.magic - defense_type)
                    if spell_damage <= 0:
                        spell_damage = 1 
                    spell_damage = int(round(spell_damage))
                    target.currenthealth -= spell_damage
                    print(f"{target.name.title()} took {str(spell_damage)} damage. Their health is now {str(target.currenthealth)}")   
                self.magic = self.basemagic + self.weapon.mag
                self.currentmp -= spell.cost
                affliction_yes = random.randint(0, 10)
                if affliction_yes == 8:
                    if spell.affliction == states.fire:
                        states.set_player_state(target, states.fire)
                    elif spell.affliction == states.frozen:
                        states.set_player_state(target, states.frozen)
            elif isinstance(spell, magic.Boost_Magic): 
                print(f"{self.name} used {spell.name}! {spell.attr_to_boost.title()} + {spell.boost_amt} for {spell.duration} turns.")
                self.currentmp -= spell.cost     
                self.adjust_val(spell.attr_to_boost, spell.boost_amt, spell.duration, spell)               
    def enemy_attack(self, enemy):
        print()
        damage = (self.attack - enemy.defense) 
        if damage <= 0:
            damage = 1
        enemy.currenthealth -= damage
        print(f"{self.name.title()} attacks {enemy.name.title()} for {damage} damage!\n{enemy.name.title()}'s health is now {enemy.currenthealth}.")
        if (self.speed - enemy.speed) >= 5:
            print(f"Speed supremacy! {self.name.title()} gets another, weaker hit in!")
            weak_damage = int(round(damage / 2))
            enemy.currenthealth -= weak_damage
            print(f"{enemy.name.title()}\'s health is now {enemy.currenthealth}.")
    def adjust_val(self, attr, amt, duration, spell):
        before_adjust = getattr(self, attr)
        spell.value_buffer = before_adjust
        setattr(self, attr, (before_adjust + amt))
    def detail_str(self): 
        detail = f"{self.name} (HP: {self.currenthealth} / {self.maxhealth}, ATK: {self.attack}, MAG: {self.magic}, DEF: {self.defense}, RES: {self.resistance}, SPD: {self.speed})"
        return detail

## Bosses ## 
#name, weapon, currenthealth, maxhealth, attack, baseattack, defense, magic, basemagic, spells, mp, currentmp, resistance, speed, state

magus = Boss('Magus', weapons.fisticuffs, 360, 360, 25, 25, 40, 40, 40, [magic.healIII, magic.barrier, magic.dark_matter, magic.dark_mist], 150, 150, 50, 40, states.normal)

erika = Boss('Erika', weapons.fisticuffs, 290, 290, 25, 20, 45, 15, 15, [magic.healII, magic.buffII, magic.rainbow_storm, magic.wind_waltz], 80, 80, 45, 35, states.normal)

zombor = Boss('Zombor', weapons.fisticuffs, 375, 375, 30, 30, 70, 10, 10, [magic.healII, magic.flame_strike, magic.annihilation_ray], 65, 65, 70, 10, states.normal)

queen_zeal = Boss('Queen Zeal', weapons.fisticuffs, 500, 500, 45, 45, 65, 45, 45, [magic.healIII, magic.gears_of_darkness, magic.starburst, magic.evil_within, magic.reality_inversion], 160, 160, 65, 40, states.normal)

magus_2 = Boss('Magus II', weapons.fisticuffs, 525, 525, 30, 30, 55, 55, 55, [magic.healV, magic.barrier2, magic.dark_matter, magic.eternal_darkness, magic.shadow_scythe], 250, 250, 75, 30, states.normal)

erika_2 = Boss("Erika II", weapons.fisticuffs, 450, 450, 40, 40, 75, 30, 30, [magic.healIV, magic.buffIII, magic.rainbow_hurricane, magic.tornado_tango], 155, 155, 60, 60, states.normal)

bosses = [magus, erika, zombor]
superbosses = [magus_2, erika_2, queen_zeal]
bosses_defeated = []
superbosses_defeated = []

## Enemies ##

class Enemy():
    name = ''
    weapon = ''
    currenthealth = 0
    maxhealth = 0
    attack = 0
    baseattack = 0
    defense = 0
    magic = 0
    basemagic = 0
    spells = []
    mp = 0
    currentmp = 0
    resistance = 0
    speed = 0
    state = ''
    bounty = 0
    xpbounty = 0
    def __init__(self, name, weapon, currenthealth, maxhealth, attack, baseattack, defense, magic, basemagic, spells, mp, currentmp, resistance, speed, state, bounty, xpbounty): 
        self.name = name
        self.weapon = weapon
        self.currenthealth = currenthealth
        self.maxhealth = maxhealth
        self.attack = attack
        self.baseattack = baseattack
        self.defense = defense
        self.magic = magic
        self.basemagic = basemagic
        self.spells = spells
        self.mp = mp
        self.currentmp = currentmp
        self.resistance = resistance
        self.speed = speed
        self.state = state 
        self.bounty = bounty
        self.xpbounty = xpbounty
    def print_enemy_stats(self):
        print(f"""
{self.name.title()}\'s stats are as follows: 
Weapon: {self.weapon.name} 
Current HP: {str(self.currenthealth)} 
Max HP: {str(self.maxhealth)} 
ATK: {str(self.attack)} 
Base ATK: {str(self.baseattack)} 
DEF: {str(self.defense)} 
MAG: {str(self.magic)} 
Base MAG: {str(self.basemagic)} 
Spells: [{efuncs.list_print(self.spells)}]
MP: {str(self.mp)} 
Current MP: {str(self.currentmp)}
RES: {str(self.resistance)} 
SPD: {str(self.speed)}
Bounty: {str(self.bounty)} CR
XP Bounty: {str(self.xpbounty)} XP
        """)      
    def equip_enemy_weapon(self, weapon):
        if weapon.elemental_affinity == 'S':
            self.basemagic += 5
        if weapon == weapons.throwing_knives: 
            self.speed += 5
        if weapon == weapons.club:
            self.baseattack += 3
        self.weapon = weapon
        self.attack = (self.baseattack + weapon.atk)
        self.magic = (self.basemagic + weapon.mag)
    def enemy_use_magic(self, target, spell):
        print()
        if spell not in self.spells: 
            print(f"{self.name.title()} tried to use a spell that they don\'t know.")
        else: 
            if isinstance(spell, magic.Heal):
                print(f"{self.name.title()} used {spell.name}!")
                if (self.currenthealth + spell.heals) > (self.maxhealth):
                    self.currenthealth = self.maxhealth
                else: 
                    self.currenthealth += spell.heals
                print(f"{self.name.title()}\'s HP is now {self.currenthealth}!")
                self.currentmp -= spell.cost
            elif isinstance(spell, magic.Buff):
                print(f"{self.name} used {spell.name}!")
                spell.value_buffer = self.attack
                self.attack += spell.atkadd
                print(f"{self.name.title()}\'s ATK is now {self.attack}!")
                self.currentmp -= spell.cost
            elif isinstance(spell, magic.attack_spell):
                print(f"{self.name.title()} used {spell.name}!")
                self.magic += spell.damage
                if spell.aoe == True:
                    for player in party:    
                        if spell.kind == "P":
                            defense_type = player.defense
                        elif spell.kind == "M":
                            defense_type = player.resistance
                        spell_damage = (self.magic - defense_type)
                        if spell_damage <= 0:
                            spell_damage = 1 
                        spell_damage = int(round(spell_damage))               
                        player.currenthealth -= spell_damage
                        print(f"{player.name.title()} took {str(spell_damage)} damage. Their health is now {str(player.currenthealth)}")
                else:
                    if spell.kind == "P":
                        defense_type = target.defense
                    elif spell.kind == "M":
                        defense_type = target.resistance
                    spell_damage = (self.magic - defense_type)
                    if spell_damage <= 0:
                        spell_damage = 1 
                    spell_damage = int(round(spell_damage))
                    target.currenthealth -= spell_damage
                    print(f"{target.name.title()} took {str(spell_damage)} damage. Their health is now {str(target.currenthealth)}")  
                self.magic = self.basemagic + self.weapon.mag
                self.currentmp -= spell.cost
                affliction_yes = random.randint(0, 10)
                if affliction_yes == 8:
                    if spell.affliction == states.fire:
                        states.set_player_state(target, states.fire)
                    elif spell.affliction == states.frozen:
                        states.set_player_state(target, states.frozen) 
            elif isinstance(spell, magic.Boost_Magic):
                print(f"{self.name} used {spell.name}! {spell.attr_to_boost.title()} + {spell.boost_amt} for {spell.duration} turns.")
                self.currentmp -= spell.cost
                self.adjust_val(spell.attr_to_boost, spell.boost_amt, spell.duration, spell)    
    def enemy_attack(self, enemy):
        print()
        damage = (self.attack - enemy.defense)
        if damage <= 0:
            damage = 1
        enemy.currenthealth -= damage
        print(f"{self.name.title()} attacks {enemy.name.title()} for {damage} damage!\n{enemy.name.title()}'s health is now {enemy.currenthealth}.")
        if (self.speed - enemy.speed) >= 5:
            print(f"Speed supremacy! {self.name.title()} gets another, weaker hit in!")
            weak_damage = int(round(damage / 2))
            enemy.currenthealth -= weak_damage
            print(f"{enemy.name.title()}\'s health is now {enemy.currenthealth}.")
    def adjust_val(self, attr, amt, duration, spell):
        before_adjust = getattr(self, attr)
        spell.value_buffer = before_adjust
        setattr(self, attr, (before_adjust + amt))
    def detail_str(self): 
        detail = f"{self.name} (HP: {self.currenthealth} / {self.maxhealth}, ATK: {self.attack}, MAG: {self.magic}, DEF: {self.defense}, RES: {self.resistance}, SPD: {self.speed})"
        return detail

#name, weapon, currenthealth, maxhealth, attack, baseattack, defense, magic, basemagic, spells, mp, currentmp, resistance, speed, state, bounty, xpbounty

#Physical enemies
goblin = Enemy('Goblin', weapons.fisticuffs, 50, 50, 10, 10, 20, 0, 0, [], 0, 0, 0, 5, states.normal, 115, 25)
gogoblin = Enemy('Gogoblin', weapons.fisticuffs, 75, 75, 15, 15, 20, 0, 0, [], 0, 0, 5, 10, states.normal, 230, 75)

skelly = Enemy('Skelly', weapons.fisticuffs, 60, 60, 20, 20, 40, 0, 0, [], 0, 0, 0, 10, states.normal, 485, 185)
bigskelly = Enemy('Big Skelly', weapons.fisticuffs, 120, 120, 25, 25, 45, 0, 0, [], 0, 0, 15, 15, states.normal, 550, 365)

cyclops = Enemy('Cyclops', weapons.fisticuffs, 150, 150, 30, 30, 30, 10, 10, [], 0, 0, 35, 10, states.normal, 720, 425)
redcyclops = Enemy('Red Cyclops', weapons.fisticuffs, 175, 175, 30, 30, 35, 0, 0, [], 0, 0, 30, 15, states.normal, 825, 475)

dactyl = Enemy('Dactyl', weapons.fisticuffs, 90, 90, 10, 10, 10, 0, 0, [], 0, 0, 10, 20, states.normal, 500, 125) 

bongo_nongo = Enemy("Bongo Nongo", weapons.fisticuffs, 200, 200, 30, 30, 50, 5, 5, [magic.healII], 55, 55, 50, 5, states.normal, 1000, 500)

#Magic enemies 

practicioner = Enemy('Practicioner', weapons.fisticuffs, 125, 125, 20, 20, 15, 30, 30, [magic.healII, magic.buffII, magic.fireball, magic.icecicle_spear, magic.zipzip], 55, 55, 20, 20, states.normal, 330, 220)

black_mage = Enemy("Black Mage", weapons.fisticuffs, 130, 130, 20, 20, 25, 40, 40, [magic.healIII, magic.ominous_wind, magic.fireball, magic.ground_fault, magic.sigil_of_fire], 80, 80, 45, 40, states.normal, 750, 440)

rogue = Enemy('Rogue', weapons.fisticuffs, 150, 150, 34, 34, 25, 36, 36, [magic.healII, magic.icecicle_spear, magic.zapzap], 70, 70, 30, 75, states.normal, 2675, 560)

shadow_mage = Enemy("Shadow Mage", weapons.fisticuffs, 185, 185, 30, 30, 30, 45, 45, [magic.healIII, magic.sigil_of_darkness, magic.magical_protection, magic.ominous_wind, magic.sigil_of_fire, magic.sigil_of_earth], 80, 80, 40, 50, states.normal, 1000, 650)

acolyte_of_magus = Enemy("Acolyte of Magus", weapons.fisticuffs, 200, 200, 37, 37, 40, 55, 55, [magic.healIV, magic.ominous_wind, magic.reality_inversion, magic.dreadful_hymn, magic.sigil_of_darkness], 110, 110, 50, 50, states.normal, 1250, 1000)

enemies = [goblin, gogoblin, skelly, bigskelly, cyclops, redcyclops, dactyl, bongo_nongo, practicioner, black_mage, rogue, shadow_mage, acolyte_of_magus]