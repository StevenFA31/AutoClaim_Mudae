import discum
import json
import time
import requests
from datetime import datetime, timedelta
from discum.utils.slash import SlashCommander
import logging
import re

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_path_exists(jsonCard):
    try:
        emoji_name = jsonCard[0]['components'][0]['components'][0]["emoji"]["name"]
        logging.info("Emoji name found: %s", emoji_name)
        return True
    except (KeyError, IndexError) as e:
        logging.error("Path does not exist: %s", e)
        return False

def simpleRoll(config):

    botID = '432610292342587392' 
    auth = {'authorization': config['token']}
    bot = discum.Client(token=config['token'], log=False)
    url = f'https://discord.com/api/v8/channels/{config["channelId"]}/messages'

    logging.info("Rolling for server %s in channel -> %s", config["serverName"], config["channelName"])

    i = 1
    y = 0
    claimed = '❤️'
    unclaimed = '🤍'
    kakera = '💎'
    wish = '☀️'
    rollCommand = SlashCommander(bot.getSlashCommands(botID).json()).get([config['rollCommand']])
    continueRolling = True
    cards = []

    while continueRolling == True or y < 4:
        try:
            bot.triggerSlashCommand(botID, config["channelId"], config["serverId"], data=rollCommand)
            time.sleep(1.8)
            r = requests.get(url, headers=auth)
            time.sleep(0.8)
            jsonCard = json.loads(r.text)
        except (requests.RequestException, json.JSONDecodeError) as e:
            logging.error("Error in API request or JSON decoding: %s", e)
            continue

        if len(jsonCard[0]['content']) != 0:
            y += 1  
            continueRolling = False
            continue

        idMessage = jsonCard[0]["id"]

        try:
            cardName = jsonCard[0]['embeds'][0]['author']['name']
            cardSeries = jsonCard[0]['embeds'][0]['description'].replace('\n', '**').split('**')[0]
            cardPower = int((jsonCard[0]['embeds'][0]['description']).split('**')[1])
            claim = 'footer' in jsonCard[0]['embeds'][0]
        except (IndexError, KeyError):
            logging.error("Error parsing card data: %s", e)
            cardName = 'null'
            cardSeries = 'null'
            cardPower = 0
            claim = False
        except ValueError:
            cardPower = 0

        cards.append({
            'name': cardName,
            'series': cardSeries,
            'power': cardPower,
            'claim': claim,
            'idMessage': idMessage

        })

        # Initialize the variable for checking if the wished user is mentioned

        is_wished_user = False

        # Check if 'mentions' key exists and is not empty
        if 'mentions' in jsonCard[0] and jsonCard[0]['mentions']:
            # Check each mention for the wished username
            for mention in jsonCard[0]['mentions']:
                if mention["id"] == config["userId"]:
                    is_wished_user = True
                    break

        # Check content and conditions
        is_wished = "Wished by" in jsonCard[0]['content']
        is_user_mentioned = config["userId"] in jsonCard[0]['content']
        is_footer_missing_or_icon_url_missing = ('footer' not in jsonCard[0].get('embeds', [{}])[0] or
                                                'icon_url' not in jsonCard[0].get('embeds', [{}])[0].get('footer', {}))

        if (is_wished and is_wished_user and is_user_mentioned) or is_footer_missing_or_icon_url_missing:
            if (is_wished and is_wished_user and is_user_mentioned):
                logging.info("%d - %s ---- %d - %s - %s", i, wish, cardPower, cardName, cardSeries)
                print("Ooh it's your wished card !")
            else:
                logging.info("%d - %s ---- %d - %s - %s", i, unclaimed,cardPower, cardName, cardSeries)
            if cardPower >= config["claimCriteria"]["minKakeraPoints"] or cardSeries in config['desiredSeries']:
                logging.info("Trying to claim %s", cardName)
                r= requests.put(f'https://discord.com/api/v8/channels/{config["channelId"]}/messages/{idMessage}/reactions/❤️/%40me',headers=auth)
                time.sleep(1.8)
                x= requests.get(f'https://discord.com/api/v9/channels/{config["channelId"]}/messages',headers=auth)
                time.sleep(1)
                if config["claimedCardText"] in x.json()[0]["content"]:
                    logging.warning("%s IS NOW YOUR PROPERTY !", cardName)
                if config["noClaimCardAvailableText"] in x.json()[0]["content"]:
                    logging.warning("No claim available ... Trying to use reset claim (RT) ...")
                    requests.post(url=url , headers = auth, data = {'content' : '$rt'})
                    time.sleep(1.8)
                    x= requests.get(f'https://discord.com/api/v9/channels/{config["channelId"]}/messages',headers=auth)
                    time.sleep(1)
                    if "reactions" in x.json()[0]:
                        if x.json()[0]["reactions"] and "✅" in x.json()[0]["reactions"][0]["emoji"]["name"]:
                            logging.critical("ATTENTION. Reset claim used.")
                            r= requests.put(f'https://discord.com/api/v8/channels/{config["channelId"]}/messages/{idMessage}/reactions/😀/%40me',headers=auth)
                            time.sleep(1)
                            x= requests.get(f'https://discord.com/api/v9/channels/{config["channelId"]}/messages',headers=auth)
                            time.sleep(1)
                            if config["claimedCardText"] in x.json()[0]["content"]:
                                logging.warning("%s IS NOW YOUR PROPERTY !", cardName)
                            else:
                                logging.error("There was a problem AFTER the reset claim. Continue rolling ...") 
                    else:
                        logging.warning("You don't have reset claim. %s is not claimed.", cardName)

        else: 
                logging.info("%d - %s ---- %d - %s - %s", i, claimed,cardPower, cardName, cardSeries)

        try:
            cardsKakera = jsonCard[0]['components'][0]['components'][0]['emoji']['name']
            if cardsKakera in config['desiredKakeras']:
                y -= 1 
                logging.info('%s - %s - Trying to react to %s of %s', kakera, kakera, cardsKakera, cardName)
                bot.click(jsonCard[0]['author']["id"], channelID=jsonCard[0]["channel_id"], guildID=config["serverId"], messageID=jsonCard[0]["id"], messageFlags=jsonCard[0]['flags'], data={'component_type': 2, 'custom_id': jsonCard[0]['components'][0]['components'][0]['custom_id']})
                time.sleep(1)
                x= requests.get(f'https://discord.com/api/v9/channels/{config["channelId"]}/messages',headers=auth)
                time.sleep(1)
                if cardsKakera in x.json()[0]["content"]:
                    logging.warning('%s - %s - React to %s of %s successful !', kakera, kakera, cardsKakera, cardName)
                elif config["noReactKakeraAvailableText"] in x.json()[0]["content"]:
                    logging.warning("No kakera reaction available ... Trying to use daily kakera (DK) ...")
                    requests.post(url=url , headers = auth, data = {'content' : '$dk'})
                    time.sleep(1)
                    x= requests.get(f'https://discord.com/api/v9/channels/{config["channelId"]}/messages',headers=auth)
                    time.sleep(1)
                    if config["useDailyKakeraText"] in x.json()[0]["content"]:
                            logging.critical("ATTENTION. Daily kakera used.")
                            bot.click(jsonCard[0]['author']["id"], channelID=jsonCard[0]["channel_id"], guildID=config["serverId"], messageID=jsonCard[0]["id"], messageFlags=jsonCard[0]['flags'], data={'component_type': 2, 'custom_id': jsonCard[0]['components'][0]['components'][0]['custom_id']})
                            time.sleep(1)
                            x= requests.get(f'https://discord.com/api/v9/channels/{config["channelId"]}/messages',headers=auth)
                            time.sleep(1)
                            if cardsKakera in x.json()[0]["content"]:
                                logging.warning('%s - %s - React to %s of %s was successful !', kakera, kakera, cardsKakera, cardName)
                            else:
                                logging.error("There was a problem AFTER the daily kakera. Continue rolling ...") 
                    elif config["noDailyKakeraAvailableText"] in x.json()[0]["content"]:
                        logging.info("No daily kakera available ... ")
                        logging.warning('React to %s of %s has failed ...', kakera, kakera, cardsKakera, cardName)
                        logging.info("Continue rolling ... ")
                    else:
                        logging.error("There was a problem with daily kakera. Continue rolling ...")
                else:
                    logging.error("There was a problem with react kakera. Continue rolling ...")
                
        except IndexError:
            cardsKakera = 'null'
        i += 1
    print('Rolling ended')
 
    requests.post(url=url , headers = auth, data = {'content' : '$tu'})
    time.sleep(1.8)
    tu=requests.get(f'https://discord.com/api/v9/channels/{config["channelId"]}/messages',headers=auth)

    def parse_remaining_time(content):
        # Check for claim availability and time remaining
        can_claim_en = re.search(r'you __can__ claim right now!', content)
        if can_claim_en:
            # Look for remaining time when claim is available
            time_match = re.search(r'The next claim reset is in \*\*(\d+)\*\* min', content)
            if not time_match:
                time_match = re.search(r'The next claim reset is in \*\*(\d+)h (\d+)\*\* min', content)

            if time_match:
                if len(time_match.groups()) == 1:
                    return True, int(time_match.group(1))  # Claim available, return remaining minutes
                elif len(time_match.groups()) == 2:
                    return True, int(time_match.group(1)) * 60 + int(time_match.group(2))  # Claim available, return total minutes
        
                
            # Look for remaining time when claim is not available, Patterns for non-availability
        no_claim_en = re.search(r'you can\'t claim for another \*\*(\d+)\*\* min', content)
        if no_claim_en:
            return False, int(no_claim_en.group(1))  # Claim not available, return remaining minutes
        
        no_claim_en_hours = re.search(r'you can\'t claim for another \*\*(\d+)h (\d+)\*\* min', content)
        if no_claim_en_hours:
            return False, int(no_claim_en_hours.group(1)) * 60 + int(no_claim_en_hours.group(2))  # Claim not available, return total minutes
        
        return None, None

    content = tu.json()[0]['content']
    time.sleep(1)
    can_claim, remaining_minutes = parse_remaining_time(content)

    if can_claim is not None:
        # Determine if within last hour
        if can_claim and remaining_minutes <= 60:
            logging.info('Within the last hour before reset and no claims made. Running best_card functionality...')
            best_card = None

            for card in cards:
                if not card['claim']:
                    if best_card is None or card['power'] > best_card['power']:
                        best_card = card

            if best_card:
                logging.info("Trying to claim best card %s with %d kakera points", best_card['name'], best_card['power'])
                try:
                    react = requests.put(f'https://discord.com/api/v8/channels/{config["channelId"]}/messages/{best_card["idMessage"]}/reactions/🐿️/%40me', headers=auth)
                    react.raise_for_status()
                    z= requests.get(f'https://discord.com/api/v9/channels/{config["channelId"]}/messages',headers=auth)
                    z.raise_for_status()
                    if "are now married" or "sormais raciste" or "are now of the right political persuasion" in z.json()[0]["content"]:
                        logging.warning("%s IS NOW YOUR PROPERTY !", best_card['name'])

                except requests.RequestException as e:
                    logging.error("Error in claim request: %s", e)
        elif can_claim:
            print(f'Claim is available but not within the last hour. Time remaining before reset: {remaining_minutes} minutes')
        else:
            print(f'Claim is not available. Time remaining before reset: {remaining_minutes} minutes')
    else:
        logging.error('Unable to parse claim status or time from the content.')

    if config["pokeRoll"] and "p is available!" in tu.json()[0]["content"]:
        logging.warning('Trying to roll Pokeslot ...')
        try:
            requests.post(url=url , headers = auth, data = {'content' : '$p'})
            time.sleep(1)
            pokemon= requests.get(f'https://discord.com/api/v9/channels/{config["channelId"]}/messages',headers=auth)
            time.sleep(1)
            if "Congratulations, you won an uncommon nothing." in pokemon.json()[0]["content"]:
                logging.warning('Congratulation ! You won 0 pokemon.')
            if "You won" in pokemon.json()[0]["content"]:
                logging.warning('Congratulation ! You won 1 Common pokemon.')
            if "That's better: you got an uncommon" in pokemon.json()[0]["content"]:
                logging.warning('Congratulation ! You won 1 Uncommon pokemon.')
            if "Oh, it's rare: you just won" in pokemon.json()[0]["content"]:
                logging.warning('Congratulation ! You won 1 Rare pokemon.')
            if "Very impressive!!! You got" in pokemon.json()[0]["content"]:
                logging.warning('Congratulation ! You won 1 Very Rare pokemon.')
            if "Congrats, you just won... " in pokemon.json()[0]["content"]:
                logging.warning('Congratulation ! You won 1 Legendary pokemon.')
            if "You just obtained a" in pokemon.json()[0]["content"]:
                logging.warning('Congratulation ! You won 1 Ultra Beast pokemon.')
            if "ERROR 4761" in pokemon.json()[0]["content"]:
                logging.warning('Congratulation ! You won 1 Paradox pokemon.')
            if "Ces couleurs semblent inhabituelles..." in pokemon.json()[0]["content"]:
                logging.warning("There is a Shiny in your pokemon")

        except requests.RequestException as e:
            logging.error("Error in Pokeslot roll request: %s", e)
    
    if "You may vote right now!" in tu.json()[0]["content"] or "Vous pouvez voter" in tu.json()[0]["content"]:
        logging.warning("YOUR VOTE IS AVAILABLE!")
        
    if "daily is available!" in tu.json()[0]["content"] or "daily est disponible !" in tu.json()[0]["content"]:
        logging.warning("YOUR DAILY IS AVAILABLE! Try to claim ...")
        requests.post(url=url , headers = auth, data = {'content' : '$daily'})
        time.sleep(1)
        daily= requests.get(f'https://discord.com/api/v9/channels/{config["channelId"]}/messages',headers=auth)
        time.sleep(1)
        if '✅' in daily.json()[0]["reactions"][0]["emoji"]["name"]:
            logging.warning("DAILY CLAIMED SUCCESSFULLY!")

    print("\n")