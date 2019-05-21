import players
import random
import efuncs
import time
import magic
import items
import states 

class string_exception(Exception): pass 
class range_error(Exception): pass
class EnemyAttack(Exception): pass

def arena():
    fighter_index = 0
    turns = 0
    cycle_complete = False
    dead_players = []
    while True:
        battle_choice = input("\nWelcome to the arena. would you like to battle? (Y/N)\n>\t").upper()
        if battle_choice in ['Y', 'N']:
            if battle_choice == 'Y':
                advance = True
                break
            elif battle_choice == 'N':
                advance = False
                efuncs.nav()
        else:
            advance = False
            print("Not an option.")
            continue
    while advance == True:
        try:
            boss_or_enemy = int(input("\nFight an enemy or a boss?\n1: Enemy\n2: Boss\n>\t"))
        except ValueError:
            print("\nThat isn't an option.")
            continue
        if boss_or_enemy not in [1, 2]:
            print("\nThat isn't an option.")
            continue
        elif boss_or_enemy == 1:
            while True:
                #Fights enemies
                enemy_dict = efuncs.make_temp_dictionary(players.enemies)
                opponent = input(f"\nFight which enemy?\n{efuncs.pretty_print(players.enemies)}\nS: View Enemy Stats\nD: Don't fight an enemy\n>\t")
                try:  
                    if opponent in {'s', 'S', 'd', 'D'}: raise string_exception
                    opponent = int(opponent)
                    active_opponent = enemy_dict[opponent]
                    break
                except (KeyError, ValueError):
                    print("Invalid choice.")
                    continue
                except string_exception:
                    if opponent in {'s', 'S'}: 
                        try:
                            view_stats = int(input(f"\nView the stats of which enemy?\n{efuncs.pretty_print(players.enemies)}\n>\t"))
                            enemy_dict[view_stats].print_enemy_stats()
                        except (ValueError, KeyError):
                            print("Not an option.")
                            continue
                    elif opponent in {'d', 'D'}:
                        arena()
                    else:
                        print("Not an option.")
                        continue
        elif boss_or_enemy  == 2:
            while True:
                #Fights boss/superboss
                if len(players.superbosses_defeated) >= 3:
                    efuncs.win(players.superbosses_defeated)
                elif len(players.bosses_defeated) >= 3:
                    boss_list = players.superbosses
                    print("Party will fight superbosses.")
                else: boss_list = players.bosses
                boss_dict = efuncs.make_temp_dictionary(boss_list)
                opponent = input(f"\nFight which boss?\n{efuncs.pretty_print(boss_list)}\nS: View Boss Stats\nD: Don't fight a boss\n>\t")
                try:
                    if opponent in {'s', 'S', 'd', 'D'}: raise string_exception
                    opponent = int(opponent)
                    active_opponent = boss_dict[opponent]
                    break
                except (KeyError, ValueError):
                    print("Invalid choice.")
                    continue 
                except string_exception:
                    if opponent in {'s', 'S'}: 
                        try:
                            view_stats = int(input(f"\nView the stats of which boss?\n{efuncs.pretty_print(boss_list)}\n>\t"))
                            boss_dict[view_stats].print_enemy_stats()
                        except (ValueError, KeyError):
                            print("Not an option.")
                            continue
                    elif opponent in {'d', 'D'}:
                        arena()
                    else:
                        print("Not an option.")
                        continue
        print("\n--COMBAT START--")
        while True:
            looprun = False
            totalhealth = 0
            if active_opponent.currenthealth <= 0: #Opponent death
                time.sleep(.7)
                print(f"\nYou win! You defeated {active_opponent.name} in {str(turns)} turns!\n")
                if isinstance(active_opponent, players.Enemy) == True:
                    players.protag.credits += active_opponent.bounty
                    print(f"{players.protag.name} now has {players.protag.credits} credits.\n")
                    for player in players.party:
                        for player in dead_players: players.party.append(player)
                        player.xp += (turns * 15) + active_opponent.xpbounty                        
                        if player.state != states.normal: 
                            player.state.turns_active = (player.state.duration + 1)
                            states.check_duration(player)
                        player.currenthealth = player.maxhealth
                        player.currentmp = player.mp
                        player.xpcheck()
                    efuncs.reset()
                    if active_opponent.state != states.normal: 
                        active_opponent.state.turns_active = (active_opponent.state.duration + 1)
                        states.check_duration(active_opponent)
                    efuncs.recruit_check()
                    efuncs.nav()
                else: 
                    if active_opponent in players.bosses: xp_coeff = 50
                    elif active_opponent in players.superbosses: xp_coeff = 100
                    for player in players.party:
                        for player in dead_players:
                            players.party.append(player)
                        player.xp += (turns * xp_coeff)
                        player.currenthealth = player.maxhealth
                        player.currentmp = player.mp
                        if player.state != states.normal: 
                            player.state.turns_active = (player.state.duration + 1)
                            states.check_duration(player)
                        player.xpcheck()
                    efuncs.reset()
                    if active_opponent.state != states.normal: 
                        active_opponent.state.turns_active = (active_opponent.state.duration + 1)
                        states.check_duration(active_opponent)
                    if active_opponent not in (players.bosses_defeated + players.superbosses_defeated):
                        if active_opponent in players.superbosses:
                            players.superbosses_defeated.append(active_opponent)
                        else:
                            players.bosses_defeated.append(active_opponent)
                    efuncs.recruit_check()
                    efuncs.nav()
            for player in players.party:
                if player.currenthealth <= 0:
                    dead_players.append(player)
                    print(f"{player.name} died!")
                    players.party.remove(player)
            if len(players.party) <= 0:
                for player in dead_players:
                    players.party.append(player)
                print(f"You lost! CR -50!\nYou gained no experience.")
                for player in players.party:
                    player.currenthealth = player.maxhealth
                    player.currentmp = player.mp
                    player.xpcheck()
                efuncs.reset()
                players.protag.credits -= 50
                efuncs.nav()
            try:
                if cycle_complete == True:
                    raise EnemyAttack
                current_fighter = players.party[fighter_index]
                action = int(input(f"\nWhat will {current_fighter.name} do?\n1: Attack\n2: Use magic\n3: Bag\n4: Concede\n>\t"))
                if action not in range(1,5):
                    raise range_error
            except (ValueError, range_error):
                print("Invalid choice.")
                continue
            except IndexError:
                cycle_complete = False
                fighter_index = 0
                continue
            except EnemyAttack: 
                #Enemy attack 
                chosen_enemy_target = players.party[random.randint(0, (len(players.party)-1))]
                will_use_magic = random.randint(6,10)
                if will_use_magic in {8,9,10} and len(active_opponent.spells) != 0:
                    opponent_heal_spells = []
                    opponent_other_spells = []
                    for item in active_opponent.spells:
                        if isinstance(item, (magic.attack_spell, magic.Buff, magic.Boost_Magic)): opponent_other_spells.append(item)
                        elif isinstance(item, magic.Heal): opponent_heal_spells.append(item)
                    if active_opponent.currenthealth <= (active_opponent.maxhealth * .40):
                        spell_to_use = random.choice(opponent_heal_spells)
                        active_opponent.enemy_use_magic('', spell_to_use)
                    else:
                        spell_to_use = random.choice(opponent_other_spells)
                        active_opponent.enemy_use_magic(chosen_enemy_target, spell_to_use)
                    """
                    for iteration, item in enumerate(active_opponent.spells):
                        if isinstance(item, magic.Heal):
                            healindex = iteration
                            spell_to_use = active_opponent.spells[healindex]   
                    if active_opponent.currenthealth <= (active_opponent.currenthealth * .40):
                        active_opponent.enemy_use_magic('', spell_to_use)
                    elif len(active_opponent.spells) != 0:
                        if (active_opponent.spells[:healindex] + active_opponent.spells[healindex+1:]) == []:
                            active_opponent.enemy_attack(chosen_enemy_target)
                        else:
                            spell_to_use = random.choice((active_opponent.spells[:healindex] + active_opponent.spells[healindex+1:]))
                            active_opponent.enemy_use_magic(chosen_enemy_target, spell_to_use)"""
                else:
                    active_opponent.enemy_attack(chosen_enemy_target)
                cycle_complete = False
                continue
            while True:
                if looprun == True:
                    break
                if current_fighter.state != states.normal:
                    player.state.turns_active += 1
                    states.check_duration(current_fighter)
                turns += 1
                if action == 1:
                    print()
                    current_fighter.player_attack(active_opponent)
                    fighter_index += 1
                    cycle_complete = True
                    looprun = True
                elif action == 2:
                    print()
                    while True:
                        if looprun == True:
                            break
                        try:
                            spell_choice = input(f"Use which spell? {current_fighter.name} has {current_fighter.currentmp} MP.\n{efuncs.detail_print(current_fighter.spells)}\nD: Don't use a spell\n>\t")
                            if spell_choice in {'d', 'D'}:
                                raise string_exception
                            else:
                                spell_choice = int(spell_choice)
                        except ValueError:
                            print("Not an option.")
                            continue
                        except string_exception:
                            if spell_choice in {'d', 'D'}:
                                looprun = True
                                break
                        try:
                            temp_spell_dictionary = efuncs.make_temp_dictionary(current_fighter.spells)
                            spell = temp_spell_dictionary[spell_choice]
                            if isinstance(spell, (magic.Boost_Magic, magic.Heal, magic.Buff)) == True:
                                if len(players.party) > 1:
                                    spelltarg = int(input(f"\nUse spell on:\n{efuncs.detail_print(players.party)}\n>\t"))
                                    fighters = efuncs.make_temp_dictionary(players.party)
                                    if current_fighter.currentmp - spell.cost < 0:
                                        print(f"\n{current_fighter.name} doesn't have enough MP to use that spell.\n")
                                        continue
                                    else:
                                        current_fighter.use_magic(fighters[spelltarg], spell) 
                                        cycle_complete = True
                                        looprun = True
                                        fighter_index += 1
                                        break
                                else: 
                                    if current_fighter.currentmp - spell.cost < 0:
                                        print(f"\n{current_fighter.name} doesn't have enough MP to use that spell.\n")
                                        continue
                                    else:
                                        current_fighter.use_magic(current_fighter, spell)
                                        cycle_complete = True
                                        looprun = True
                                        fighter_index += 1                         
                                        break    
                            elif isinstance(spell, magic.attack_spell) == True:
                                if current_fighter.currentmp - spell.cost < 0:
                                    print(f"\n{current_fighter.name} doesn't have enough MP to use that spell.\n")
                                    continue
                                else:
                                    current_fighter.use_magic(active_opponent, spell)
                                    cycle_complete = True
                                    looprun = True
                                    fighter_index += 1
                                    break
                        except (IndexError, ValueError, KeyError):
                            print("Invalid choice.")
                            continue
                elif action == 3:
                    while True:
                        if looprun == True: 
                            break
                        try:
                            item_choice = input(f"\nUse which item?\n{efuncs.detail_print(current_fighter.bag)}\nD: Don't use an item\n>\t")
                            if item_choice in {'d', 'D'}:
                                raise string_exception
                            else:
                                item_choice = int(item_choice)
                                temp_item_dictionary = efuncs.make_temp_dictionary(current_fighter.bag)
                                temp_party_dictionary = efuncs.make_temp_dictionary(players.party)
                                target_choice = int(input(f"\nOn who?\n{efuncs.pretty_print(players.party)}\n>\t"))
                                target = temp_party_dictionary[target_choice]
                                item = temp_item_dictionary[item_choice]
                                current_fighter.use_item(target, item)
                                looprun = True
                                cycle_complete = True
                                fighter_index += 1
                                break
                        except (ValueError, IndexError, KeyError):
                            print("Invalid choice.")
                            continue
                        except string_exception:    
                            looprun = True
                            break
                elif action == 4:
                    if players.protag.credits < 50:
                        print("\nYou can't pay the concede fee!")
                        looprun = True
                        break
                    else:
                        print(f"The party ran away and dropped 50 CR!")
                        players.protag.credits -= 50
                        efuncs.nav()
            