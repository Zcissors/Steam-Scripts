import os
import json
import requests


#   Open https://store.steampowered.com/pointssummary/ajaxgetasyncconfig
#   Copy the value of webapi_token
def get_api_key():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            api_key = config.get('key')
            if api_key:
                return api_key
            else:
                print("API key not found in config.json.")
                return None
    except FileNotFoundError:
        print("config.json not found. Current working directory:", os.getcwd())
        return None
    except Exception as e:
        print("Error reading config.json:", e)
        return None
    

def steamid64_to_vanity_url(steamid64, api_key):
    base_url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    params = {
        'key': api_key,
        'steamids': steamid64
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        players = data.get('response', {}).get('players', [])

        if players:
            profile_url = players[0].get('profileurl', '')
            
            # Check if the profile URL contains a custom vanity URL
            if "/id/" in profile_url:
                # Extract the part after "/id/"
                vanity_url_part = profile_url.split("/id/")[-1]
                return vanity_url_part
            else:
                # If no custom vanity URL, return the whole profile URL
                return profile_url
        else:
            print(f"Failed to convert SteamID64 to vanity URL. Response: {data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to convert SteamID64 to vanity URL. Error: {e}")
        print(f"Response content: {response.content.decode('utf-8')}")
        return None

def vanity_url_to_steamid64(vanity_url, api_key):
    custom_url = vanity_url.rstrip('/').rsplit('/', 1)[-1]
    url = "https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/"
    params = {
        'key': api_key,
        'vanityurl': custom_url
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if data.get('response', {}).get('success') == 1:
            steamid64 = data.get('response', {}).get('steamid', '')
            return steamid64
        else:
            print(f"Failed to convert vanity URL to SteamID64. {data.get('response', {}).get('message')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to convert vanity URL to SteamID64. Error: {e}")
        return None

def get_friends_list(api_key, steamid64):
    base_url = "https://api.steampowered.com/ISteamUser/GetFriendList/v1/"
    params = {
        'key': api_key,
        'steamid': steamid64
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        friends = data.get('friendslist', {}).get('friends', [])
        return friends
    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve friend list for {steamid64}. Error: {e}")
        return None

def save_to_file(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)

def main():
    try:
        # Get the API key from config.json
        api_key = get_api_key()

        if api_key:
            # Get the SteamID64 or vanity URL from the user
            input_identifier = input("Enter SteamID64 or vanity URL: ")

            # Convert SteamID64 to vanity URL if needed
            if input_identifier.isdigit():
                vanity_url = steamid64_to_vanity_url(input_identifier, api_key)
                if vanity_url:
                    print(f"Vanity URL: {vanity_url}")
                    input_identifier = vanity_url
                else:
                    print("Exiting...")
                    exit()

            # If the input is not a SteamID64, attempt to convert vanity URL to SteamID64
            if not input_identifier.isdigit():
                steamid64 = vanity_url_to_steamid64(input_identifier, api_key)
                if steamid64:
                    print(f"SteamID64: {steamid64}")
                    input_identifier = steamid64
                else:
                    print("Exiting...")
                    exit()

            # Call the function to get the friends list
            friends_list = get_friends_list(api_key, input_identifier)

            if friends_list:
                # Create a Profiles directory if it doesn't exist
                profiles_dir = 'Profiles'
                os.makedirs(profiles_dir, exist_ok=True)

                # Save the friend list to a file in Profiles directory
                profile_filename = os.path.join(profiles_dir, f'{input_identifier}.json')
                save_to_file(profile_filename, friends_list)

                
                print(f"Number of friends: {len(friends_list)}")
                print(f"Friend list saved to {profile_filename}.")
            else:
                print("Exiting...")

    except KeyboardInterrupt:
        print("\nKeyboard interrupt. Exiting...")

if __name__ == "__main__":
    main()
