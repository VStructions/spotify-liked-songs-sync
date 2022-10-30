from   urllib.parse      import urlencode, urlparse, parse_qs
import requests
import oauthlib.oauth2
import requests_oauthlib
import webbrowser
import base64

# Spotify App's:
clID  = "Your client ID here"
clS   = "Your client Secret here"
scope = "https://developer.spotify.com/documentation/general/guides/authorization/scopes/" # Select scope!

token_url    = "https://accounts.spotify.com/api/token"
auth_url     = "https://accounts.spotify.com/authorize?"
redirect_uri = "http://127.0.0.1:5000/callback"

def getSpotifyTokenClientCredFlow(): # Client Credentials Flow (Doesn't allow user content/playback interaction)
    
    client = oauthlib.oauth2.BackendApplicationClient(client_id=clID)

    oauth = requests_oauthlib.OAuth2Session(client=client, scope=scope)

    try:
        token = oauth.fetch_token(token_url=token_url, client_secret=clS)
    except:
        token = None

    return token
	
def getSpotifyTokenAuthCodeFlow(): # Authorization Code Flow (Allows all)
    
    auth_code_params = {
        "response_type":"code",
        "client_id":clID,
        "scope":scope,
        "redirect_uri":redirect_uri
    }

    # While I could have setup a listener, this is simpler
    input("Press enter to open the Spotify authorization screen. When you click \"Agree\" return to this window for more instructions.\n")

    webbrowser.open_new(f"{auth_url}{urlencode(auth_code_params)}")

    auth_code = input("You should be redirected to the set URI. Copy the whole URL from the browser's URL bar and paste it here: ")

    auth_code = parse_qs(urlparse(auth_code).query)['code'][0] # Get code from URL

    print(f"Temporary code: {auth_code}")

    base64_client_secret = base64.urlsafe_b64encode(f"{clID}:{clS}".encode()).decode()

    headers = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "Authorization": f"Basic {base64_client_secret}"
    }

    data = {
        "grant_type" : "authorization_code",
        "code": auth_code,
        "redirect_uri": redirect_uri
    }

    access_token_request = requests.post(token_url, data=data, headers=headers)

    if access_token_request.status_code != 200:
        return None
    
    print("Generated tokens:\n")
    
    return access_token_request.json()


def main():

    # Select a flow
    #print(getSpotifyTokenClientCredFlow())
    #print(getSpotifyTokenAuthCodeFlow())

    return 0



if __name__ == '__main__':

    main()
