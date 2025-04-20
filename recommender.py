from model import df, X_scaled, annoy_index
from collections import defaultdict
import pandas as pd


def recommend_song_annoy(song_data, top_n=5):
    # Extract song title properly
    if isinstance(song_data, dict):
        song_title = song_data.get('title', song_data.get('name', ''))
    else:
        song_title = str(song_data)
    
    # Debug output to see what's being searched
    print(f"Searching for song: '{song_title}'")
    
    # Clean the title for better matching
    clean_title = song_title.lower().strip()
    
    # Check if song exists in database
    valid_df = df.dropna(subset=['name'])
    
    # Try exact match first (case insensitive)
    indices = valid_df.index[valid_df['name'].str.lower().str.strip() == clean_title].tolist()
    
    if not indices:
        # Log this for debugging
        print(f"No exact match found for '{clean_title}'")
        
        # Try partial match with some guards
        try:
            partial_matches = valid_df[valid_df['name'].str.lower().str.contains(clean_title, regex=False, na=False)]
            if not partial_matches.empty:
                print(f"Found {len(partial_matches)} partial matches")
                indices = [partial_matches.index[0]]
            else:
                print(f"No partial matches found for '{clean_title}'")
                return []
        except Exception as e:
            print(f"Error in partial matching: {e}")
            return []
    
    if indices:
        idx = indices[0]
        try:
            # Get recommendations
            nearest_indices = annoy_index.get_nns_by_item(idx, top_n + 1)
            # Remove the original song
            nearest_indices = [i for i in nearest_indices if i != idx][:top_n]
            
            # Return recommended songs
            return df.iloc[nearest_indices][['name', 'artists', 'duration_ms']].to_dict(orient='records')
        except Exception as e:
            print(f"Error finding recommendations: {e}")
            return []
    
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
    matched_count = 0
    
    for i, song in enumerate(song_list):
        print(f"Song {i+1}/{len(song_list)}: {song.get('title', str(song))}")
        recommendations = recommend_song_annoy(song, top_n=20)
        
        if recommendations:
            matched_count += 1
            all_recommendations.append(recommendations)
    
    print(f"Successfully matched {matched_count}/{len(song_list)} songs")
    
    if matched_count == 0:
        return ["No matching songs found in the database."]
    
    # Get common recommendations or prioritized list
    final_recommendations = common_songs_priority(*all_recommendations)
    
    if not final_recommendations:
        return ["No recommendations found."]
    
    print(f"Final recommendation count: {len(final_recommendations)}")
    return final_recommendations
