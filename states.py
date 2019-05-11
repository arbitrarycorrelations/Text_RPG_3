class currentattack(object): pass 
class speed(object): pass

class State():
    name = ''
    attr = ''
    debuff = 0
    buff = 0
    duration = 0
    turns_active = 0
    def __init__(self, name, attr, debuff, buff, duration, turns_active):
        self.name = name
        self.attr = attr
        self.debuff = debuff
        self.buff = buff
        self.duration = duration
        self.turns_active = turns_active

def set_player_state(player, state):
    player.state = state
    if player.state != normal:
        print(f"{player.name.title()} is {player.state.name}. {state.attr.title()} -{str(state.debuff)} for {str(state.duration)} turns.")
        pattr = getattr(player, state.attr)
        nv = (pattr - state.debuff)
        setattr(player, state.attr, nv)
        player.state.turns_active += 1
    
def check_duration(player):
    if player.state.name != "Normal":
        if player.state.turns_active >= player.state.duration:
            pattr = getattr(player, player.state.attr)
            nv = (pattr + player.state.debuff)
            setattr(player, player.state.attr, nv)
            pattr = getattr(player, player.state.attr)
            print(f"{player.name}'s '{player.state.name}' has ended. Their {player.state.attr} is {pattr} again.")
            set_player_state(player, normal)
        else:
            print(f"{player.name}'s {player.state.name} debuff will last for {(player.duration - player.state.state.turns_active)}")
    else:
        print(f"{player.name.title()} is doing just fine.")

#States
#name, attr, debuff, buff, duration, turns_active
fire = State('On fire', 'attack', 4, 0, 4, 3)
frozen = State('Frozen', 'speed', '!mov', 0, 2, 0)
electrified = State('Electrified', 'speed', 5, 0, 3, 0)
normal = State('Normal', '', 0, 0, 0, 0) 
