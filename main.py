import players
import weapons 
import efuncs
import time
import save 
import os

class LoadGame(Exception): pass

def startup():
    while True:
        try:
            landing = input("Welcome to TRPGIII!\nN:\tNew Game\nL:\tLoad Existing Game\n>\t").capitalize()
            if landing not in {'N', 'L'}:
                print("Invalid option.\n")
                continue
            elif landing == 'N':
                while True:
                    if os.stat('save.json').st_size > 0 and open('save.json').read() != "Placeholder text":
                        overwrite = input("There is an existing save game. Would you like to overwrite it? (Y/N)\n>\t")
                        if overwrite.capitalize() not in {'Y', 'N'}: print("Invalid option.") ; continue
                        elif overwrite.capitalize() == 'Y': fresh_start()
                        else: raise LoadGame
                    else: fresh_start()  
            elif landing == 'L': raise LoadGame
        except LoadGame:
            if open('save.json').read() == "Placeholder text":
                print("No saves found. Starting a new game instead...")
                fresh_start()
            else:
                save.load()
                cycle_start_key = 'l'
                cycle_start(cycle_start_key)
                    
def fresh_start():
    print("\nStarted a new game.")
    pname = input("What's your name? \n>\t")
    pname = pname.title()
    players.protag.name = pname
    cycle_start_key = 'n'
    cycle_start(cycle_start_key)

def cycle_start(key):
    if key.capitalize() != 'L':
        #Ally weapons assignment for new games
        players.assign_weapon(players.starting_weapons)
        print("\nSetting up objects...")
        players.kurita.equip_weapon(weapons.poleArm)
        players.ralf.equip_weapon(weapons.handAxe)
        players.sakura.equip_weapon(weapons.wand)
        #Party is already set for loaded games
        players.add_to_party(players.protag)
        #players.add_to_party(players.kurita)
        #players.add_to_party(players.ralf)
        #players.add_to_party(players.sakura)
        save.save(players.party)
    #Boss weapon assignment
    players.magus.equip_boss_weapon(weapons.moonfall_scythe)
    players.erika.equip_boss_weapon(weapons.throwing_knives)
    players.zombor.equip_boss_weapon(weapons.club)
    players.magus_2.equip_boss_weapon(weapons.dreamreaper)
    players.erika_2.equip_boss_weapon(weapons.zanmato)
    players.queen_zeal.equip_boss_weapon(weapons.suzaku)
    #Enemy weapon assignment
    players.goblin.equip_enemy_weapon(weapons.rocks)
    players.gogoblin.equip_enemy_weapon(weapons.weathered_sword)
    players.skelly.equip_enemy_weapon(weapons.glaive)
    players.bigskelly.equip_enemy_weapon(weapons.hammer)
    players.cyclops.equip_enemy_weapon(weapons.brass_knuckles)
    players.redcyclops.equip_enemy_weapon(weapons.tree_trunk)
    players.dactyl.equip_enemy_weapon(weapons.claws)
    players.bongo_nongo.equip_enemy_weapon(weapons.bongo)
    players.practicioner.equip_enemy_weapon(weapons.imbued_wand)
    players.black_mage.equip_enemy_weapon(weapons.calmcaster)
    players.rogue.equip_enemy_weapon(weapons.backstabber)
    players.shadow_mage.equip_enemy_weapon(weapons.warped_wand)
    players.acolyte_of_magus.equip_enemy_weapon(weapons.dream_devourer)
    time.sleep(1)
    print("\nDone.")
    players.protag.print_stats()
    #Done setting up objects -- goes to navigation menu 
    efuncs.nav()

startup()