import shelve
from box import Box
import box
import time
from colorama import Fore, init
init(autoreset=True)

width_index = 5
width_brawler = 8
width_gamemode = 13
width_powerplay = 35
player_name = ''

name_lookup = {
   'soloShowdown': 'Solo Showdown',
   'duoShowdown' : 'Duo Showdown',
   'brawlBall' : 'Brawl Ball',
   'gemGrab': 'Gem Grab',
   'heist': 'Heist',
   'siege': 'Siege',
   'bounty': 'Bounty',
   'bigGame': 'Big Game',
   'roboRumble':'Robo Rumble',
   'bossFight':'Boss Fight',
   'hotZone':'Hot Zone'
}
soloPP = {
   1:38,
   2:34,
   3:30,
   4:26,
   5:22,
   6:18,
   7:14,
   8:10,
   9:6,
   10:2
}

duoPP = {
   1:34,
   2:26,
   3:18,
   4:10,
   5:2
}

def is_powerplay(battle):
   try:
      if battle.battle.mode == 'soloShowdown':
         if soloPP[battle.battle.rank] == battle.battle.trophyChange:
            return True
         else: return False
      elif battle.battle.mode == 'duoShowdown':
         if duoPP[battle.battle.rank] == battle.battle.trophyChange:
            return True
         else: return False
      else:
         if battle.battle.trophyChange > 8:
            return True
         else:
            if battle.battle.result == 'defeat' and battle.battle.trophyChange > 0:
               return True
            else: return False
   except box.exceptions.BoxKeyError:
      pass

def calculate_trophyChange(battles, num):
    total_change = 0
    for i in range(num):
      try:
         total_change += battles[i].battle.trophyChange
      except box.exceptions.BoxKeyError:
        print('error')
        pass
      except:
         print("You screwed something up son!")
    return total_change

def get_brawler_played(battle, player_tag): 
   player_tag = '#'+player_tag.upper()
   global player_name
   if battle.mode in set([ 'bigGame','roboRumble']):
      return None
   elif battle.mode == 'soloShowdown':
        for i in range (10):
           if battle.players[i].tag == player_tag:
              if player_name == '':
                player_name = battle.players[i].name
              return battle.players[i].brawler
   elif battle.mode == 'duoShowdown':
      for i in range (5):
         for j in range(2):
           if battle.teams[i][j].tag == player_tag:
              if player_name == '':
                player_name = battle.teams[i][j].name
              return battle.teams[i][j].brawler
   else: 
      for i in range(2):
         for j in range(3):
            if battle.teams[i][j].tag == player_tag:
               if player_name == '':
                player_name = battle.teams[i][j].name
               return battle.teams[i][j].brawler



def sign(value): return ('-','+')[value >= 0]

def colourise(value):
    if value in set(['+', 'victory']):
        return Fore.GREEN
    elif value in set(['-','defeat']):
        return Fore.RED
    else:
        return Fore.WHITE

def battle_log(data, player_tag, display=True):
    if display==True:
        print(f'{"Num.":^{width_index}}|{"Game Mode":^{width_gamemode+1}}|{"Brawler":^{width_brawler+9}}|{"Outcome":^{20}}\n{"-"*60}')
    brawler_trophy_change = {}
    if player_tag[0] == '#':
        player_tag = player_tag[1:]
    listofkeys = list(data.keys())
    listofkeys.sort()
    trophy_change = 0
    index = 1
    

    for key in listofkeys:
        battle = Box(data[key])
        powerPlay = is_powerplay(battle)
        brawler = get_brawler_played(battle.battle,player_tag)
        if battle.battle.mode in set(['bigGame','roboRumble']):
            pass
        elif battle.battle.mode in set([ 'soloShowdown','duoShowdown']): 
            if battle.battle.type == 'ranked' and brawler != None:
                if powerPlay:
                    pptext = f'Power Play ({brawler.trophies})'
                    brawler_details = f'{Fore.MAGENTA}{brawler.name:>{width_brawler}}\n{pptext:>{width_powerplay}}'
                else:
                    brawler_details = f'{Fore.LIGHTBLUE_EX}{brawler.name:>{width_brawler}} ({brawler.trophies})'
            elif brawler != None:
                brawler_details = f'{Fore.WHITE}{brawler.name:>{width_brawler}} (Fri)'  
            try:
                if display==True:
                    print(f'{index:>{width_index}}. {Fore.GREEN}{name_lookup[battle.battle.mode]:>{width_gamemode}} {brawler_details} ->{Fore.YELLOW} Rank: {battle.battle.rank} {colourise(sign(battle.battle.trophyChange))}({sign(battle.battle.trophyChange)}{abs(battle.battle.trophyChange)})')
                trophy_change += battle.battle.trophyChange
                if powerPlay:
                    if 'POWER-PLAY Points' in brawler_trophy_change:
                        brawler_trophy_change['POWER-PLAY Points']+=battle.battle.trophyChange
                    else:
                        brawler_trophy_change['POWER-PLAY Points']=battle.battle.trophyChange
                else:
                    if brawler.name in brawler_trophy_change:
                        brawler_trophy_change[brawler.name]+=battle.battle.trophyChange
                    else:
                        brawler_trophy_change[brawler.name]=battle.battle.trophyChange
                
            except box.exceptions.BoxError:
                if display==True:
                    print(f'{index:>{width_index}}. {Fore.GREEN}{name_lookup[battle.battle.mode]:>{width_gamemode}} {brawler_details} ->{Fore.YELLOW} Rank: {battle.battle.rank}')

        else:
            if battle.battle.type == 'ranked' and brawler != None:
                if powerPlay:
                    pptext = f'Power Play ({brawler.trophies})'
                    brawler_details = f'{Fore.MAGENTA}{brawler.name:>{width_brawler}}\n{pptext:>{width_powerplay}}'
                else:
                    brawler_details = f'{Fore.LIGHTBLUE_EX}{brawler.name:>{width_brawler}} ({brawler.trophies})'
            elif brawler != None:
                  brawler_details = f'{Fore.WHITE}{brawler.name:>{width_brawler}} (Fri)' 
            try:
                if display==True:
                    print(f'{index:>{width_index}}. {Fore.CYAN}{name_lookup[battle.battle.mode]:>{width_gamemode}} {brawler_details} ->{Fore.YELLOW} Result: {colourise(battle.battle.result)}{battle.battle.result} {colourise(sign(battle.battle.trophyChange))}({sign(battle.battle.trophyChange)}{abs(battle.battle.trophyChange)})')
                trophy_change += battle.battle.trophyChange
                if powerPlay:
                    if 'POWER-PLAY Points' in brawler_trophy_change:
                        brawler_trophy_change['POWER-PLAY Points']+=battle.battle.trophyChange
                    else:
                        brawler_trophy_change['POWER-PLAY Points']=battle.battle.trophyChange
                else:
                    if brawler.name in brawler_trophy_change:
                        brawler_trophy_change[brawler.name]+=battle.battle.trophyChange
                    else:
                        brawler_trophy_change[brawler.name]=battle.battle.trophyChange
            except box.exceptions.BoxKeyError:
                if display==True:
                    print(f'{index:>{width_index}}. {Fore.CYAN}{name_lookup[battle.battle.mode]:>{width_gamemode}} {brawler_details} ->{Fore.YELLOW} Result: {colourise(battle.battle.result)}{battle.battle.result}{Fore.RESET}')
        index += 1
    brawler_trophy_changes = ''
    for key, value in brawler_trophy_change.items():
        brawler_trophy_changes += f'{key:<{17}} : {colourise(sign(value))}{sign(value)}{abs(value):>{4}}{Fore.RESET} \n'
    if 'POWER-PLAY Points' in brawler_trophy_change:
            deduct_from_total = brawler_trophy_change['POWER-PLAY Points']
    else: deduct_from_total = 0
    print('='*60)
    print(f'{player_name:^60}')
    print('='*60)
    print(f'For {len(listofkeys)} games, total Trophy change was {colourise(sign(trophy_change))}{sign(trophy_change)}{abs(trophy_change-deduct_from_total)}{Fore.RESET}\n{"-"*50}\n{brawler_trophy_changes} {Fore.RESET}')




if __name__ == "__main__":
    #Enter your player tag here as used when saved
    player_tag = '202JCYQQQ' 
    data = shelve.open(player_tag)
    battle_log(data, player_tag)
    print('~'*60)