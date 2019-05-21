import json 
import players
import efuncs
import magic
import weapons
import items
import time 

def save(party):
    print("\nSaving...")
    save = {}
    for character in party:
        if character == players.protag: header = 'protag'
        else: header = character.name
        save["{}".format(header)] = []
        save["{}".format(header)].append({
            'name' : character.name,
            'weapon': character.weapon.name,
            'currenthealth': character.currenthealth,
            'maxhealth': character.maxhealth,
            'attack'  : character.attack,
            'baseattack'  : character.baseattack,
            'defense': character.defense,
            'magic'  : character.magic,
            'basemagic'  : character.basemagic,
            'spells'  : [x.name for x in character.spells],
            'mp'  : character.mp,
            'currentmp'  : character.currentmp,
            'resistance'  : character.resistance,
            'speed'  : character.speed,
            'lvl'  : character.lvl,
            'xp'  : character.xp,
            'tnl'  : character.tnl,
            'state'  : character.state.name,
            'armor'  : character.armor,
            'bag'  : [x.name for x in character.bag],
            'credits'  : character.credits,
            'spells_to_learn'  : [x.name for x in character.spells_to_learn]
        })
    save["Party"] = ["protag"] + [x.name for x in players.party if x != players.protag]  
    save["Recruitable Characters"] = [x.name for x in players.recruitable_chars]
    save["Bosses Defeated"] = [x.name for x in players.bosses_defeated]
    save["Superbosses Defeated"] = [x.name for x in players.superbosses_defeated]
    with open('save.json', 'w') as save_file:
        json.dump(save, save_file)
    time.sleep(.5)
    print("Saved.")

def load():
    with open('save.json', 'r') as save_file:
        save_obj = json.load(save_file)
    save_str = json.dumps(save_obj)
    save_db = json.loads(save_str)
    #Loading party members
    char_objs = []
    for character in save_db["Recruitable Characters"]:
        for charo in players.all_characters:
            if character == charo.name:
                char_objs.append(charo)
    players.recruitable_chars = char_objs
    party_objs = []
    for character in save_db["Party"]:
        for char_obj in players.all_characters:
            if character == char_obj.name:
                party_objs.append(char_obj)
    players.party = party_objs
    #Loading individual player data
    for char in players.party:
        for key, value in save_db["{}".format(char.name)][0].items():
            if type(value) not in {list, str}:
                setattr(char, key, value)
            elif key == "weapon":
                for weapon_group in weapons.all_weapons:
                    for weapon in weapon_group:
                        if save_db["{}".format(char.name)][0]["weapon"] == weapon.name:
                            setattr(char, 'weapon', weapon)
            elif key == "spells":
                spell_objs = []
                for spell in save_db["{}".format(char.name)][0]["spells"]: 
                    for spell_group in magic.all_spells:
                        for item in spell_group:
                            if spell == item.name:
                                spell_objs.append(item)
                setattr(char, 'spells', spell_objs)
            elif key == "spells_to_learn":
                spell_objs = []
                for spell in save_db["{}".format(char.name)][0]["spells_to_learn"]: 
                    for spell_group in magic.all_spells:
                        for item in spell_group:
                            if spell == item.name:
                                spell_objs.append(item)
                setattr(char, 'spells_to_learn', spell_objs)
            elif key == "bag":
                bag_objs = []
                for item_name in save_db["{}".format(char.name)][0]['bag']:
                    for item in items.all_items:
                        if item_name == item.name:
                            bag_objs.append(item)
                setattr(char, 'bag', bag_objs)
    players.protag.name = save_db['protag'][0]["name"]
    print(f"\nLoaded party: {efuncs.list_print(players.party)}")
    print("Loaded character data.")
    #Loading bosses and superbosses that have been defeated
    boss_objs = []
    for boss in save_db["Bosses Defeated"]: 
        for bosso in players.bosses:
            if boss == bosso.name:
                boss_objs.append(bosso)
    players.bosses_defeated = boss_objs
    superboss_objs = []
    for superboss in save_db["Superbosses Defeated"]: 
        for superbosso in players.superbosses:
            if superboss == superbosso.name:
                superboss_objs.append(superbosso)
    players.superbosses_defeated = superboss_objs
    print("Loaded bosses defeated and superbosses defeated.")        

