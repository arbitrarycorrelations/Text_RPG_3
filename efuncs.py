import players
import arena
import shop 
import magic
import items
import operator
import save 

class string_exception(Exception): pass

def home():
    while True:
        try:
            switch = int(input("\nParty has returned home. What do you want to do?\n1: View spell info\n2: View entity stats\n3: Recruit characters\n4: Learn a spell\n5: Change party leader\n6: Save the game\n7: Back to navigation\n>\t"))
            if switch == 1:
                party_temp = make_temp_dictionary(players.party)
                entity = int(input(f"\nView whose spells?\n{pretty_print(players.party)}\n>\t"))
                party_temp[entity].view_spells()
            elif switch == 2: 
                party_temp = make_temp_dictionary(players.party)
                if len(players.bosses_defeated) >= 3: bosslist = players.superbosses
                else: bosslist = players.bosses
                boss_temp = make_temp_dictionary(bosslist)
                enemy_temp = make_temp_dictionary(players.enemies)
                entity_type = int(input(f"\nEntity type:\n1: Players\n2: Enemies\n3: Bosses\n>\t"))
                if entity_type not in {1,2,3}:
                    print("Oops, that isn't an option.")
                    continue
                elif entity_type == 1:
                    player_choice = int(input(f"\nView whose stats?\n{pretty_print(players.party)}\n>\t"))
                    party_temp[player_choice].print_stats()
                elif entity_type == 2:
                    enemy_choice = int(input(f"\nView whose stats?\n{pretty_print(players.enemies)}\n>\t"))
                    enemy_temp[enemy_choice].print_enemy_stats()
                elif entity_type == 3:
                    boss_choice = int(input(f"\nView whose stats?\n{pretty_print(bosslist)}\n>\t"))
                    boss_temp[boss_choice].print_boss_stats()
            elif switch == 3:
                recruit_check()
            elif switch == 4:
                party_temp = make_temp_dictionary(players.party)
                entity_choice = int(input(f"\nWho will learn a spell?\n{pretty_print(players.party)}\n>\t"))
                learn_spell(party_temp[entity_choice])         
            elif switch == 5:
                if len(players.party) < 2:
                    print("The party only has one member.")
                else:
                    while True:
                        try:
                            temp_party_dict = make_temp_dictionary(players.party)
                            new_leader = int(input(f"Assign which character as the leader?\n{pretty_print(players.party)}\n>\t"))
                            replacementidx = players.party.index(temp_party_dict[new_leader])
                            current_leader = players.party[0]
                            players.party[0] = 'temp value'
                            players.party[0] = players.party[replacementidx]
                            players.party[replacementidx] = current_leader
                            print(f"The party now looks like this: {list_print(players.party)}")
                            break
                        except (ValueError, KeyError):
                            print("Invalid choice.")
                            continue 
            elif switch == 6:
                save.save(players.party)
                continue
            elif switch == 7:
                nav()
            else:
                print("Invalid choice.")
                continue
        except (ValueError, KeyError):
            print("Not a valid choice.")
            continue

def exit():
    while True:
        qyn = input("Quit the game? (Y/N) \n>\t")
        if qyn.capitalize() in ['Y']:
            save.save(players.party)
            print("Thanks for playing!")
            quit()
        else:
            nav()

def rules():
    while True: 
        rules_advance = False
        rulesYN = input("\nView the rules?\n1: Yes\n2: No\n>\t")
        try:
            rulesYN = int(rulesYN)
            if rulesYN not in {1,2}: raise ValueError
        except ValueError:
            print("Not a choice.")
            continue
        if rulesYN == 1: rules_advance = True
        elif rulesYN == 2: nav()
        if rules_advance == True:
            print(f"""
The rules of the game are as follows:
Combat is turn-based. During a combat cycle, you can attack, use a spell, use an item, or concede. 

✦Stat Breakdown✦

⋆Current Health: The health that an entity has at that moment.
⋆Max Health: The maximum health that an entity can have.
⋆Attack: Base attack + weapon attack. This is how powerful an entity's physical attacks are.
⋆Defense: Guards against physical attacks or physical spells.
⋆Magic: Base magic + weapon magic. This is how powerful an entity's attack spells are.
⋆Resistance: Guards against magic spells.
⋆MP: The capacity an entity has for spellcasting.
⋆Speed: How fast an entity is. If an entity's speed is 5 or higher than their opponent's, the entity will attack again.

✦Spell Attributes✦

⋆Name: The spell's name.
⋆Damage: How much damage the spell will do.
⋆Cost: How much MP the spell costs to use.
⋆Kind: The type of defense the spell is measured against (Defense or Resistance)\n[M: Magic -- Against RES \\\ P: Physical -- Against DEF].
⋆Affliction: The state that the spell has a chance to set.

✦Basic Game Info✦

After defeating all three bosses (Magus, Erika, and Zombor), the player unlocks the ability to fight superbosses. These are difficult, endgame bosses that should be fought at a high level. If you defeat all three superbosses, you win the game.
""")
            nav()
def nav():
    places = {1: arena.arena, 2: shop.shop, 3: home, 4: rules, 5: exit}
    while True:
        try:
            desired_place = int(input("\nWhere would you like to go?\n1. Arena\n2. Shop\n3. Home\n4. View Rules\n5. Quit Game\n>\t"))
            places[desired_place]()
        except (ValueError, IndexError): 
            print("Not a choice.")
            continue 

def list_print(listattr):
    blocks = ''
    for item in listattr:
        blocks = blocks + "{.name}, "
    blocks = blocks.strip(", ")
    blocks = blocks.format(*listattr)
    return blocks

def pretty_print(listattr):
    ppstr = ''
    for iteration, item in enumerate(listattr):
        ppstr = ppstr + str(iteration+1) + ": {.name}\n" 
    ppstr = ppstr.format(*listattr)
    return ppstr

def make_temp_dictionary(listattr):
    dictattr = {}
    for iteration, item in enumerate(listattr):
        dictattr[iteration+1] = item
    return dictattr

def recruit(player):
    if player in players.party:
        nav()
    else:
        while True:
            try:
                accept_deny = int(input(f"{player.name} would like to join your party.\n1: Accept\n2: Deny\n>\t"))
                if accept_deny not in {1,2}: raise ValueError
                elif accept_deny == 1: 
                    players.add_to_party(player)
                    player.print_stats()
                    players.recruitable_chars.remove(player)
                    nav()
                elif accept_deny == 2:
                    print("Oh, okay.")
                    nav()
            except ValueError:
                print("Not an option.")
                continue

def recruit_check():
    if players.recruitable_chars == []:
        print("No one to recruit.")
    else:
        for character in players.recruitable_chars:
            if players.protag.lvl >= character.lvl:
                recruit(character)
        print("No one to recruit.")
        
def detailed_spell_view(spell):
    print()
    if isinstance(spell, magic.attack_spell):
        print(f"Name: {spell.name}\nDamage: {spell.damage}\nCost: {spell.cost}\nKind: {spell.kind}\nAffliction: {spell.affliction.name}")
    elif isinstance(spell, magic.Heal):
        print(f"Name: {spell.name}\nCost: {spell.cost}\nHeals: {spell.heals}")
    elif isinstance(spell, magic.Buff):
        print(f"Name: {spell.name}\nCost: {spell.cost}\nAttack Boost: {spell.atkadd}\nDuration: {spell.duration}")
    elif isinstance(spell, magic.Boost_Magic):
        print(f"Name: {spell.name}\nCost: {spell.cost}\nAttribute Boosted: {spell.attr_to_boost}\nBoost Amount: {spell.boost_amt}\nDuration: {spell.duration}")
    print()

def item_detail(item):
    if isinstance(item, items.Health_Potion):
        print(f"\nName: {item.name}\nHeals: {item.increase_amt}\nShop Cost: {item.cost}\n")
    elif isinstance(item, items.Ether):
        print(f"\nName: {item.name}\nMP Restored: {item.increase_amt}\nCost: {item.cost}\n")

def weapon_detail(weapon):
    print(f"\n{weapon.name}:\nTier:\t{weapon.tier}\nAffinity:\t{weapon.elemental_affinity}\nATK:\t{weapon.atk}\nMAG:\t{weapon.mag}\nCost:\t{weapon.cost}\n{weapon.description}\n")
    
def learn_spell(player):
    filtered_stl = []
    keyf = operator.attrgetter('level')
    player.spells_to_learn.sort(key = keyf, reverse = False)
    for spell in player.spells_to_learn:
        if player.lvl >= spell.level:
            filtered_stl.append(spell)
    if filtered_stl != []:
        spells_temp = make_temp_dictionary(filtered_stl)
        while True:
            try:
                spell_choice = input(f"\nWhich spell should {player.name} learn?\n{pretty_print(filtered_stl)}\nI: View spell info\nD: Don't learn a spell\n>\t")
                if spell_choice in {'i', 'I', 'd', 'D'}:
                    raise string_exception
                else:
                    spell_choice = int(spell_choice)
                learn = spells_temp[spell_choice] 
                if learn.level > player.lvl:
                    print(f"\n{player.name} is not able to learn that spell yet. They need to be level {learn.level}")
                    continue
                elif learn.level <= player.lvl:
                    player.spells.append(learn)
                    player.spells_to_learn.remove(learn)
                    print(f"{player.name} learned {learn.name}!")
                    home()
            except KeyError:
                print("Oops, not an option.")
                continue
            except ValueError:
                print("Invalid choice.")
                continue
            except string_exception:
                if spell_choice in {'i', 'I'}:
                    spell_detail = int(input(f"\nView which spell's details?\n{pretty_print(filtered_stl)}\n>\t"))
                    if spell_detail not in spells_temp.keys():
                        print("\nNot an option.")
                        continue 
                    else:
                        detailed_spell_view(spells_temp[spell_detail])
                elif spell_choice in {'d', 'D'}:
                    home()
    else: 
        print(f"\n{player.name} can't learn any spells right now.")

def reset():
    for enemy in players.enemies:
        enemy.currenthealth = enemy.maxhealth
        enemy.currentmp = enemy.mp 
    for boss in players.bosses: 
        boss.currenthealth = boss.maxhealth
        boss.currentmp = boss.mp
    for superboss in players.superbosses:
        superboss.currenthealth = superboss.maxhealth
        superboss.currentmp = superboss.mp

def win(bosses):
    print(f"You've beaten all the superbosses, {players.protag.name}! You win!")
    print("Thanks so much for playing!")
    quit()

    