from model import df, X_scaled, annoy_index
from collections import defaultdict
import pandas as pd

def recommend_song_annoy(song_title, top_n=5):
    # Extract just the song title if in "Song Name - Artist" format
    if isinstance(song_title, dict):
        song_title = song_title.get('name', '')


    if " - " in song_title:
        song_title = song_title.split(" - ")[0].strip()
    
    # Ensure the 'name' column has no NaN values
    valid_df = df.dropna(subset=['name'])
    
    # Try to find a match in the dataset
    indices = valid_df.index[valid_df['name'].str.lower() == song_title.lower()].tolist()
    if not indices:
        # If no exact match, try partial match
        try:
            indices = valid_df.index[valid_df['name'].str.lower().str.contains(song_title.lower(), regex=False)].tolist()
        except Exception:
            indices = []
        
        if not indices:
            return []
    
    idx = indices[0]
    try:
        nearest_indices = annoy_index.get_nns_by_item(idx, top_n + 1)
        nearest_indices = [i for i in nearest_indices if i != idx][:top_n]
        
        # Return song title, artist(s), and duration
        return df.iloc[nearest_indices][['name', 'artists', 'duration_ms']].to_dict(orient='records')
    except Exception as e:
        print(f"Error finding recommendations: {e}")
        return []

def common_songs_priority(*lists):
    if not lists or all(len(lst) == 0 for lst in lists):
        return []
        
    song_counts = defaultdict(int)
    song_positions = {}
    song_details = {}

    # Track song counts and details
    for i, song_list in enumerate(lists):
        for song in song_list:
            song_key = (song['name'], song['artists'], song['duration_ms'])
            song_counts[song_key] += 1
            song_details[song_key] = song
            if song_key not in song_positions:
                song_positions[song_key] = i
    
    # Sort based on frequency and position
    recommended_songs = sorted(
        song_details.values(),
        key=lambda song: (-song_counts[(song['name'], song['artists'], song['duration_ms'])], 
                           song_positions.get((song['name'], song['artists'], song['duration_ms']), 999))
    )
    
    return recommended_songs[:10]  # Return top 10 recommendations

def recommend_playlist_songs(song_list):
    if not song_list:
        return ["No songs to recommend."]
    
    print(f"Processing {len(song_list)} songs")
    
    # Get recommendations for each song
    all_recommendations = []
    for song in song_list:  
        recommendations = recommend_song_annoy(song, top_n=20)
        if recommendations:
            all_recommendations.append(recommendations)
    
    if not all_recommendations:
        return ["No matching songs found in the database."]
    
    # Get common recommendations or prioritized list
    final_recommendations = common_songs_priority(*all_recommendations)
    
    if not final_recommendations:
        return ["No recommendations found."]
    
    return final_recommendations
