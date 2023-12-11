import requests
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
CreatorToken = config['Patreon']['CreatorToken']
CampaignID = config['Patreon']['CampaignID']
SaveFile = config['General']['SaveFile']

all_tiers = {}


def get_patrons():
    access_url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{CampaignID}/members?include=currently_entitled_tiers&fields[member]=full_name&fields[tier]=title"
    PatreonResponse = requests.get(access_url, headers={"Authorization": f"Bearer {CreatorToken}"})
    return PatreonResponse.json()


def setup_tiers():
    access_url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{CampaignID}/members?include=currently_entitled_tiers&fields[tier]=title"
    PatreonResponse = requests.get(access_url, headers={"Authorization": f"Bearer {CreatorToken}"})
    # print(PatreonResponse.json())

    for tier in PatreonResponse.json()['included']:
        all_tiers[tier['id']] = tier['attributes']['title']


def get_tier_from_id(tier_id):
    return all_tiers[tier_id]


if __name__ == '__main__':
    print("Caching tiers...")
    setup_tiers()
    print("Done!")
    print("Retrieving patrons...")
    all_patrons = get_patrons()
    print("Done!")
    # print(all_patrons)
    print("Creating list...")
    with open(SaveFile, 'a') as f:
        for patron in all_patrons['data']:
            f.write(patron['attributes']['full_name'] + ":" + get_tier_from_id(patron['relationships']['currently_entitled_tiers']['data'][0]['id']))
    print("Done!")