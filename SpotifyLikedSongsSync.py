import requests
import requests_oauthlib
import base64

import os

#### Insecure storage of Tokens ####

# Spotify App's:
clID         = "Your client ID here"
clS          = "Your client Secret here"
# For this program to work, the token scope must include "playlist-read-private user-library-read"
refreshToken = "Your Refresh Token here"

#### Insecure storage of Tokens ####

api_url               = "https://api.spotify.com/v1/"
token_url             = "https://accounts.spotify.com/api/token"
liked_songs           = "me/tracks"
liked_songs_file      = "liked_songs_list.txt" # Contains the Spotify list as is 
liked_songs_diff_file = "liked_songs_diff_list.txt" # Contains any songs that used to exist (deleted) in older versions of liked_songs_file

def refreshSpotifyAccessToken(): # Get a new Access Token using the Refresh Token

    base64_id_secret = base64.urlsafe_b64encode(f"{clID}:{clS}".encode()).decode()

    headers = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64_id_secret}"
    }

    data = {
        "grant_type" : "refresh_token",
        "refresh_token": refreshToken
    }

    access_token_request = requests.post(token_url, data=data, headers=headers)

    if access_token_request.status_code != 200:
        return None
    
    return access_token_request.json()['access_token']


def main():

    # Get token (This program is planned to run once in a while. For frequent usage,
    # there would be an access token expiration check instead of a new token request everytime)
    token = refreshSpotifyAccessToken()

    if token == None:
        print("Could not refresh access token for Spotify, if you don't have a refresh token make one using the other app")
        return

    # Make OAuth2 session
    client = requests_oauthlib.OAuth2Session(client_id=clID, token={"access_token": token})

    # Get the total amount of songs (, by asking for one, 0 not allowed)  
    response = client.get(f"{api_url}{liked_songs}", params={"offset": "0", "limit":"1"})
    
    if response.status_code != 200:
        print("Could not get total amount of songs in playlist\n")
        print(response.text)
        return
    
    total_amount = int(response.json()['total'])


    song_list = []
    limit     = 50  # Max 50
    offset    = 0

    # For the whole length of the playlist, get songs at max rate of 50 (limited)
    while offset <= total_amount:

        response = client.get(f"{api_url}{liked_songs}", params={"offset": str(offset), "limit":str(limit)})

        if response.status_code != 200:
            print("Could not get song names from playlist\n")
            print(response.text)
            return
        
        songs = response.json()['items']

        for song in songs:
            # All details are in the track dictionary
            track = song['track']
            #                        Create the comma separated artist list                    Song name          Song album
            song_list.append(f"{', '.join([artist['name'] for artist in track['artists']])} - {track['name']} -- {track['album']['name']}".encode('utf-8'))

        offset += limit

    # Remove the songs, from diff, that returned to song list
    if os.path.exists(liked_songs_diff_file):
        
        diff_list = []

        with open(liked_songs_diff_file, mode='rb') as file:
            for line in file:
                utf8_line = line.replace(b"\n", b"") # New line doesn't exist in downloaded list and shouldn't exist at all anyway
                
                # Append only if it doesn't exist in the new list, means that it will remain in the diff file
                if utf8_line not in song_list:
                    diff_list.append(utf8_line)

        with open(liked_songs_diff_file, mode='wb') as file:
            file.write(b'\n'.join(diff_list))

    # Move deleted songs to diff
    if os.path.exists(liked_songs_file):
        
        new_diff_list = []

        with open(liked_songs_file, mode='rb') as file:
            for line in file:
                utf8_line = line.replace(b"\n", b"")
            
                if utf8_line not in song_list:
                    new_diff_list.append(utf8_line)
        
        if len(new_diff_list) != 0:
            with open(liked_songs_diff_file, mode='ab') as file:
                if file.tell() != 0: # If file isn't new
                    file.write(b'\n')
                
                file.write(b'\n'.join(new_diff_list))


    # Save new list to file
    with open(liked_songs_file, mode='wb') as file:
        file.write(b'\n'.join(song_list))

    list_dir = os.path.dirname(liked_songs_file)
    print(f"Done! Check: {'Working directory' if list_dir == '' else list_dir}")

    return 0


if __name__ == '__main__':

    main()
