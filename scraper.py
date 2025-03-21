import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def get_playlist_tracks(playlist_url):
    try:
        # Set up authentication with Spotify API
        client_id = st.secrets["SPOTIFY_CLIENT_ID"]
        client_secret = st.secrets["SPOTIFY_CLIENT_SECRET"]
        
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id, 
            client_secret=client_secret
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        
        # Extract playlist ID from URL
        if "playlist/" in playlist_url:
            playlist_id = playlist_url.split("playlist/")[1].split("?")[0]
        else:
            return ["Invalid playlist URL. Please use a Spotify playlist URL."]
        
        # Get playlist tracks
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']
        
        # Get all tracks if there are more than the initial batch
        while results['next']:
            results = sp.next(results)
            tracks.extend(results['items'])
        
        # Extract track names, artists, and durations
        songs = []
        for track in tracks:
            track_info = track['track']
            if track_info:  # Some tracks might be None
                song_name = track_info['name']
                artists = [artist['name'] for artist in track_info['artists']]
                artist_str = ", ".join(artists)
                # Duration comes in milliseconds
                duration_ms = track_info['duration_ms']
                
                songs.append({
                    "title": song_name,
                    "artist": artist_str,
                    "duration_ms": duration_ms,
                    "duration": format_duration(duration_ms)
                })

        return songs
    
    except Exception as e:
        return [f"Error: {str(e)}"]

def format_duration(duration_ms):
    """
    Format duration from milliseconds to mm:ss format
    """
    try:
        duration_sec = int(duration_ms) // 1000
        minutes = duration_sec // 60
        seconds = duration_sec % 60
        return f"{minutes}:{seconds:02d}"
    except (ValueError, TypeError):
        return "Unknown Duration"