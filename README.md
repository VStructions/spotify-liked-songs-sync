# spotify-liked-songs-sync
The simplest way to get a Spotify access token and sync your Liked Songs library.

* Creates a TXT file with artist, song and album names.
* Creates a second TXT file that keeps an archive of all deleted songs (between syncs). If songs get reliked, they will be removed from the archive (Useful for accidental dislikes).


# Requires
* Client ID and Secret of [Spotify App](https://developer.spotify.com/dashboard/) for token generation


# Usage
* Paste your client ID, Secret and scope in the script files (variables at the top)
* Follow [getSpotifyTokenAuthCodeFlow()](https://github.com/VStructions/spotify-liked-songs-sync/blob/main/getSpotifyTokens.py#L30) function's instructions (from [getSpotifyTokens](https://github.com/VStructions/spotify-liked-songs-sync/blob/main/getSpotifyTokens.py)) to generate a refresh token
* Paste the refresh token at it's designated variable in [SpotifyLikedSongsSync](https://github.com/VStructions/spotify-liked-songs-sync/blob/main/SpotifyLikedSongsSync.py)
* Run [SpotifyLikedSongsSync](https://github.com/VStructions/spotify-liked-songs-sync/blob/main/SpotifyLikedSongsSync.py) whenever you want to sync your Liked Songs library!
* The liked songs TXT file will appear in the same directory
* The deleted songs TXT file will appear when the first deletion is detected


# Warning
* The TXT files should be managed by the script, manual changes could create issues
* If you want to maintain the deleted songs archive functionality, don't move the TXT files (if you do, update the paths in the script)
