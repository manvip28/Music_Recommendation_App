import streamlit as st
from scraper import get_playlist_tracks
from recommender import recommend_playlist_songs
import urllib.parse
import re

def format_duration(duration_ms):
    try:
        minutes = int(duration_ms) // 60000
        seconds = (int(duration_ms) // 1000) % 60
        return f"{minutes}:{seconds:02d}"
    except (ValueError, TypeError):
        return "Unknown Duration"

def clean_artist_name(artist_data):
    if not artist_data:
        return "Unknown Artist"
        
    if isinstance(artist_data, str) and re.search(r'\[.*,.*\'.*\'.*,.*\]', artist_data):
        chars = re.findall(r"'(.)'", artist_data)
        if chars:
            return ''.join(chars)

    if isinstance(artist_data, str) and artist_data.startswith('[') and artist_data.endswith(']'):
        try:
            cleaned = artist_data.replace("'", '"')
            artists = re.findall(r'"([^"]+)"', cleaned)
            if artists:
                return ', '.join(artists)
        except Exception:
            pass
    
    if isinstance(artist_data, list):
        return ', '.join([str(a) for a in artist_data if a])
        
    return str(artist_data)

st.set_page_config(
    page_title="AI Music Recommender",
    page_icon="🎵",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background-color: #121212;
        color: #FFFFFF;
        font-family: 'Montserrat', sans-serif;
    }
    
    .main-title {
        color: #1DB954;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        
    }

    .subtitle {
        font-size: 1.4rem;
        text-align: center;
        background: linear-gradient(90deg, #1DB954, #1ED760);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 600;
        margin-bottom: 30px;
    }

    .header, .row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 15px;
        border-radius: 8px;
    }
    
    .header {
        background-color: #1e1e1e;
        font-weight: bold;
        border-bottom: 2px solid #1DB954;
        margin-bottom: 5px;
    }
    
    .row {
        background-color: #181818;
        margin-bottom: 5px;
        border-left: 3px solid transparent;
        transition: all 0.2s ease;
    }
    
    .row:hover {
        background-color: #242424;
        border-left: 3px solid #1DB954;
        transform: translateX(5px);
    }

    .title { flex: 2; }
    .singer { flex: 1.5; color: #bbbbbb; }
    .duration { flex: 0.5; text-align: right; }

    .play-button {
        margin-left: 15px;
        color: #1DB954;
        text-decoration: none;
        font-size: 1rem;
        background-color: rgba(29, 185, 84, 0.2);
        padding: 5px 10px;
        border-radius: 50px;
    }
    
    .play-button:hover {
        background-color: rgba(29, 185, 84, 0.4);
        transform: scale(1.05);
    }
            
    .spotify-icon {
        width: 20px;
        height: 20px;
        margin-left: 10px;
    }

    /* Style for the expander header */
    div[role="button"][data-testid="stExpanderToggle"] {
        color: #1DB954 !important; /* Spotify Green */
        font-weight: bold;
    } 
            
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title"> ♬ AI Song Recommender</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover new music based on your favorite Spotify playlists</p>', unsafe_allow_html=True)

# Split into two columns
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Enter your playlist")
    playlist_url = st.text_input("Spotify playlist URL:")

    get_recs_button = st.button("Get Recommendations")
    
    if st.button("Use Sample Playlist"):
        playlist_url = "https://open.spotify.com/playlist/493ACcNpvy0uqfDRqzeXLy"
        st.session_state.playlist_url = playlist_url
    
    
    st.markdown('<div class="section-header">How it works</div>', unsafe_allow_html=True)
    st.info("""
    1. Enter a Spotify playlist URL above.
    2. Our AI analyzes the songs' audio features.
    3. The system finds songs with similar characteristics.
    4. Listen to previews directly in the app!
    """)

# Display on the right side
with col2:
    if get_recs_button or ('playlist_url' in st.session_state and playlist_url):
        if playlist_url:
            with st.spinner("Analyzing your playlist..."):
                songs = get_playlist_tracks(playlist_url)

                if not songs or not isinstance(songs, list):
                    st.error("Failed to retrieve songs. Please check the URL or try again.")
                else:
                    st.markdown(f'<div class="success-message">Found {len(songs)} songs in the playlist!</div>', unsafe_allow_html=True)

                    with st.expander("View Playlist Songs"):
                        st.markdown('<div class="header"><div class="title">Title</div><div class="singer">Singer(s)</div><div class="duration">Duration</div></div>', unsafe_allow_html=True)
                        for i, song in enumerate(songs):
                            if isinstance(song, dict):
                                song_name = song.get('title', 'Unknown Song')
                                artist_name = song.get('artist', 'Unknown Artist')
                                duration = song.get('duration', 'Unknown Duration')
                            else:
                                song_data = str(song).split('|')
                                song_name = song_data[0] if len(song_data) > 0 else "Unknown Song"
                                artist_name = song_data[1] if len(song_data) > 1 else "Unknown Artist"
                                duration = format_duration(song_data[2]) if len(song_data) > 2 else "Unknown Duration"
                            
                            st.markdown(f'<div class="row"><div class="title">{song_name}</div><div class="singer">{artist_name}</div><div class="duration">{duration}</div></div>', unsafe_allow_html=True)

                    with st.spinner("Finding recommendations..."):
                        recommendations = recommend_playlist_songs(songs)

                        if isinstance(recommendations, list) and recommendations:
                            st.markdown('<div class="section-header">🎧 Recommended Songs</div>', unsafe_allow_html=True)

                            st.markdown('<div class="header"><div class="title">Title</div><div class="singer">Singer(s)</div><div class="duration">Duration</div></div>', unsafe_allow_html=True)

                            for rec in recommendations:
                                song_name = rec.get('name', rec.get('title', 'Unknown Song'))
                                artists_data = rec.get('artists', rec.get('artist', 'Unknown Artist'))
                                artist_name = clean_artist_name(artists_data)
                                duration = format_duration(rec.get('duration_ms', 'Unknown Duration'))
                                spotify_search_url = f"https://open.spotify.com/search/{urllib.parse.quote(song_name)}"
                                
                                st.markdown(f"""
                                    <div class="row">
                                        <div class="title">{song_name}</div>
                                        <div class="singer">{artist_name}</div>
                                        <div class="duration">{duration}
                                            <a href="{spotify_search_url}" target="_blank">
                                            <img src="https://upload.wikimedia.org/wikipedia/commons/8/84/Spotify_icon.svg" alt="Play" class="spotify-icon"/>
                                            </a>
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                        else:
                            st.error("No recommendations available. Please check your playlist.")
