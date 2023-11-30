import requests
from bs4 import BeautifulSoup
import re

def get_friends_list(username):
    # Steam Community URL for the user's friends list
    url = f'https://steamcommunity.com/id/{username}/friends/'

    # Send an HTTP GET request to the user's friends list page
    response = requests.get(url)

    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the friends list from the HTML
        friends = []
        friend_elements = soup.select('.selectable_overlay')

        for friend_element in friend_elements:
            # Extract the SteamID from the href attribute
            href = friend_element.get('href', '')
            
            # Match either /id/ or /profiles/ followed by the SteamID
            steamid_match = re.search(r'/(id|profiles)/([^/]+)', href)
            
            if steamid_match:
                friend_steamid = steamid_match.group(2)
                friends.append({'steamid': friend_steamid})

        return friends

    else:
        print(f"Failed to retrieve friends list. Status code: {response.status_code}")
        return None

if __name__ == "__main__":
    # Get the Steam username from the user
    steam_username = input("Enter the Steam username: ")

    # Call the function to get the friends list
    friends_list = get_friends_list(steam_username)

    if friends_list:
        print("\nFriends List:")
        for friend in friends_list:
            print(f"{friend['steamid']}")

        # Print the number of friends
        print(f"Number of friends: {len(friends_list)}")
    else:
        print("Exiting...")
