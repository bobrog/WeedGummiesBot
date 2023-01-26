#!/usr/bin/env python3

import os
import gspread
import configargparse
import json
import logging
import datetime
import spotipy
import pprint
import time
import pandas as pd
from spotipy.oauth2 import SpotifyOAuth

artist_cache = {}
album_cache = {}
def playlist_data_dump(pid, pdate):
    track_rows = []

    playlist = sp.playlist(playlist_id=pid)
    playlist_date = pdate

    pid_tracks = playlist['tracks']['items']
    genres = []
    for track in pid_tracks:
        artist = artist_cache.get(track['track']['artists'][0]['id'],
                                  sp.artist(artist_id=track['track']['artists'][0]['id']))
        artist_cache.update({track['track']['artists'][0]['id'] : artist})

        album = album_cache.get(track['track']['album']['id'],
                                sp.album(album_id=track['track']['album']['id']))
        album_cache.update({track['track']['album']['id'] : album})

        genre = artist['genres'][0] if len(artist['genres']) > 0 else ""

        track_rows.append([
            playlist_date,
            playlist['id'],
            playlist['name'],
            track['track']['id'],
            track['track']['name'],
            artist['name'],
            album['name'],
            album['release_date'][0:4],
            track['added_by']['id'],
            int(track['track']['duration_ms']) / 1000,
            genre
        ])

    return track_rows


if __name__ == "__main__":
    # setup/process args
    parser = configargparse.ArgParser()
    parser.add("--config-file", is_config_file=True,
               help="config file path")
    parser.add("--gsheet-creds", env_var="GSHEET_CREDS",
               help="Google API Service account key JSON string")
    parser.add("--gsheet-key", env_var="GSHEET_KEY")
    parser.add("--log-level", env_var="LOG_LEVEL", default="INFO")
    parser.add("--spotify-client-id", env_var="SPOTIFY_CLIENT_ID")
    parser.add("--spotify-client-secret", env_var="SPOTIFY_CLIENT_SECRET")
    parser.add("--spotify-client-token", env_var="SPOTIFY_CLIENT_TOKEN")
    parser.add("--spotify-cache-path", env_var="SPOTIFY_CACHE_PATH",
               default=".env/spotify")
    parser.add("--spotify-scope", env_var="SPOTIFY_SCOPE",
               default=" ".join([
                   "playlist-modify-private",
                   "playlist-read-collaborative",
                   "playlist-modify-public"
               ]))

    opts = parser.parse_args()

    # init logs
    logger_level = getattr(logging, opts.log_level.upper())
    logger_format = "%(asctime)s %(name)-20s %(levelname)-8s %(message)s"
    logging.basicConfig(level=logger_level,
                        format=logger_format)

    # init gspread
    gauth_key = json.loads(opts.gsheet_creds)
    gauth = gspread.service_account_from_dict(gauth_key)
    gsheet = gauth.open_by_key(opts.gsheet_key)

    # init spotify
    if opts.spotify_client_token:
        with open(opts.spotify_cache_path, mode="w+") as f:
            f.write(opts.spotify_client_token)

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=opts.spotify_client_id,
        client_secret=opts.spotify_client_secret,
        redirect_uri="http://127.0.0.1:8080",
        open_browser=False,
        scope=opts.spotify_scope,
        cache_path=opts.spotify_cache_path))

    logging.info("spotify username {}".format(
        sp.current_user().get("display_name")))

    tracks = []
    for l in gsheet.worksheet('Playlists').get_all_values()[1:]:
        logging.info("{} {}".format(l[0], l[3]))
        t = playlist_data_dump(l[3], l[0])
        tracks = tracks + t

    df_t = pd.DataFrame(tracks, columns=['p_date', 'p_id', 'p_name', 'id',
                                         'name', 'artist_name', 'album_name', 'release_year', 'added_by', 'duration_s', 'genre'])

    # workaround for sporadic client resets
    try:
        gsheet.client.login()
    except:
        pass

    gsheet.worksheet('gds_tracks').clear()
    gsheet.worksheet('gds_tracks').update(
        [df_t.columns.tolist()] + df_t.values.tolist())
