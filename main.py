import requests
import configparser


# Setup the config parser, and read the needed values from the file
config = configparser.ConfigParser()
config.read('config.ini')
CreatorToken = config['Patreon']['CreatorToken']
CampaignID = config['Patreon']['CampaignID']
SaveFile = config['General']['SaveFile']

# Initialize a global dictionary to use for lookup from ID
all_tiers = {}


def get_patrons():
    access_url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{CampaignID}/members?include=currently_entitled_tiers&fields%5Bmember%5D=full_name&fields%5Btier%5D=title"
    PatreonResponse = requests.get(access_url, headers={"Authorization": f"Bearer {CreatorToken}"})
    return PatreonResponse.json()


def setup_tiers():
    # This URL is used to get only the tiers, but also includes patrons as well.
    # No identifying information is included, except for a unique ID for each member.
    access_url = f"https://www.patreon.com/api/oauth2/v2/campaigns/{CampaignID}/members?include=currently_entitled_tiers&fields%5Btier%5D=title"
    # Make the request to the API
    PatreonResponse = requests.get(access_url, headers={"Authorization": f"Bearer {CreatorToken}"})

    # Populate the global dictionary with the tier ID as the key, and the tier name as the value
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
        # Loop through the patrons, writing the data to the savefile
        for patron in all_patrons['data']:
            f.write(patron['attributes']['full_name'] + ":" + get_tier_from_id(patron['relationships']['currently_entitled_tiers']['data'][0]['id']))
    print("Done!")