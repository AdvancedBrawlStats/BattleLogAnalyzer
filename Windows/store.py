import brawlstats
import asyncio
import box
import shelve
import time
import dotenv
from colorama import Fore

token = dotenv.load_dotenv("TOKEN")

def battle_logs_dict(client, player_tag):
    battle_log_list = []
    battles = client.get_battle_logs(player_tag)
    for battle in battles:
        if not battle.battle.mode in set(['roboRumble']):
            battle_log_list.append(battle.to_dict())
    return battle_log_list


if __name__ == "__main__":

    player_tag = '202JCYQQQ' #Enter your player tag here without the #

    client = brawlstats.OfficialAPI(token)

    player_name = client.get_player(player_tag).name
    update_time = time.ctime()
    list_of_battles = battle_logs_dict(client, player_tag)
    
    with shelve.open(player_tag) as db:
        for battle in list_of_battles:
            db[battle["battleTime"]] = battle
    with open('last_updated','w') as update_log:
        update_log.write(update_time)

    print(f'Time: {update_time} | Player: {player_name}')

    
