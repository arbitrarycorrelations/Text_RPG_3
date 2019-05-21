import players
import items
import weapons 
import efuncs 

class RangeError(Exception): pass
class StringError(Exception): pass

def shop():
    while True: 
        switch = input(f"\nWelcome to the shop. What would you like to browse? The party has {players.protag.credits} CR.\n1: Weapons\n2: Items\nE: Exit the shop\n>\t")
        try:
            if switch in {'e', 'E'}:
                raise StringError
            else: 
                switch = int(switch)
            if switch not in {1,2}: 
                raise RangeError
            elif switch == 1: 
                dol = {1: weapons.swords, 2: weapons.axes, 3: weapons.polearms, 4: weapons.wands}
                browse_detail = int(input("\nBrowse what type of weapon?\n1: Swords\n2: Axes\n3: Polearms\n4: Wands\nD: Don't browse\n>\t"))
                if browse_detail not in range(1,5):
                    raise RangeError
                else: 
                    spec_d = efuncs.make_temp_dictionary(dol[browse_detail])
                    indiv_weapon = int(input(f"\nWhich weapon are you interested in? \n{efuncs.pretty_print(dol[browse_detail])}\nD:\tDon't browse\n>\t"))
                    if indiv_weapon not in range(1,4):
                        raise RangeError
                    else:
                        efuncs.weapon_detail(spec_d[indiv_weapon])
                        buy = input("Wanna buy it? (Y/N)\n>\t")
                        if buy not in {'y', 'Y', 'n', 'N'}:
                            raise ValueError
                        elif buy.upper() == 'Y':
                            purchase_w(spec_d[indiv_weapon])
                        elif buy.upper() == 'N':
                            break
            elif switch == 2:
                dol = {1: items.potions, 2: items.ethers}
                browse_detail = int(input("\nBrowse what type of items?\n1: Health Potions\n2: Ethers\nD: Don't browse\n>\t"))
                if browse_detail not in {1,2}:
                    raise RangeError
                else: 
                    spec_d = efuncs.make_temp_dictionary(dol[browse_detail])
                    indiv_item = int(input(f"\nWhich item are you interested in?\n{efuncs.pretty_print(dol[browse_detail])}\nD:\tDon't browse\n>\t"))
                    if indiv_item not in range(1,4):
                        raise RangeError   
                    else: 
                        efuncs.item_detail(spec_d[indiv_item])
                        buy = input("Wanna buy it? (Y/N) \n>\t")
                        if buy.upper() not in {'Y', 'N'}:
                            print("Not an option.")
                            continue
                        elif buy.upper() in {'N'}:
                            shop()
                        else:
                            quant = int(input("How many do you want?\n>\t"))
                    if quant == 0:
                        raise RangeError
                    else:
                        desired_item = spec_d[indiv_item]
                        purchase_i(desired_item, quant)            
        except ValueError:
            continue
        except StringError:
            efuncs.nav()
        except RangeError:
            print("That isn't in the range.")
            continue 
        except KeyError:
            print("KeyError")
            continue
                
def purchase_w(weapon): 
    while True:
        try:
            if players.protag.credits < weapon.cost: 
                print("Oops, you can't afford that.")
                shop() 
            else: 
                chars_d = efuncs.make_temp_dictionary(players.party)
                char = input(f"\nWho will wield the {weapon.name}?\n{efuncs.pretty_print(players.party)}\nS: View player stats\nD: Don't buy\n>\t")
                char = int(char)
                chars_d[char].equip_weapon(weapon)
                players.protag.credits -= weapon.cost 
                print(f"Party has {players.protag.credits} credits left.")
                shop()
        except ValueError:
            try:
                if char.capitalize() not in {'S', 'D'}: print("That option doesn't exist.") ; continue
                else:
                    if char.capitalize() == 'S': 
                        stat_view = int(input(f"\nView whose stats?\n{efuncs.pretty_print(players.party)}\n>\t"))
                        chars_d[stat_view].print_stats()
                    elif char.capitalize() == 'D':
                        shop()
            except ValueError:
                print("Invalid input.")
                continue
        except KeyError:
            print("\nThat isn't an option.")
            continue

def purchase_i(item, quantity):
    while True:
        try:
            if players.protag.credits < (item.cost * quantity): 
                print("Oops, you can't afford that.")
                shop() 
            else: 
                chars_d = efuncs.make_temp_dictionary(players.party)
                char = int(input(f"\nWho will hold the item(s)?\n{efuncs.pretty_print(players.party)}\n>\t"))
                for val in range(0, quantity):
                    chars_d[char].bag.append(item)
                players.protag.credits -= (item.cost * quantity) 
                print(f"Party has {players.protag.credits} credits left.")
                shop()
        except (ValueError, KeyError):
            print("\nThat isn't an option.")
            continue    