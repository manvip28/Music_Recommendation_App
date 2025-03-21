# AI Music Recommendation App

## Overview

The AI Music Recommendation App is a Streamlit-based web application that suggests new songs to users based on their favorite Spotify playlists. By analyzing the audio features of the tracks in a given playlist, the app recommends songs with similar characteristics, helping users discover new music tailored to their tastes.

## Features

- **Playlist Analysis**: Input a Spotify playlist URL to analyze its tracks.
- **Song Recommendations**: Receive song suggestions based on the analyzed playlist.
- **Direct Links**: Access Spotify search results for recommended songs directly from the app.

## Dataset

The app utilizes the "Spotify 1.2M+ Songs" dataset, which contains audio features for over 1.2 million songs obtained through the Spotify API. This dataset is essential for the recommendation system to function effectively.

**Download the dataset**:

1. Visit the dataset page on Kaggle: [Spotify 1.2M+ Songs](https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs/data)
2. Log in to your Kaggle account.
3. Click on the "Download" button to obtain the dataset files.

## Installation

To set up the AI Music Recommendation App on your local machine, follow these steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/manvip28/Music_Recommendation_App.git
   cd Music_Recommendation_App
   ```

2. **Set up a virtual environment** (optional):

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download and prepare the dataset**:

   - After downloading the dataset from Kaggle, extract the contents.
   - Place the `tracks_features.csv` file in the appropriate directory or update the data loading path in the code to point to its location.

5. **Run the application**:

   ```bash
   streamlit run app.py
   ```

   This command will launch the app in your default web browser.

## Usage

1. **Enter a Spotify Playlist URL**: Paste the URL of your Spotify playlist into the input field on the app's interface.
2. **Get Recommendations**: Click on the "Get Recommendations" button to analyze the playlist and receive song suggestions.
3. **Explore Recommendations**: View the list of recommended songs, complete with titles, artists, durations, and direct links to Spotify search results.

## Contributing

Contributions to the AI Music Recommendation App are welcome. If you have ideas for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgments

- The [Spotify 1.2M+ Songs](https://www.kaggle.com/datasets/rodolfofigueroa/spotify-12m-songs/data) dataset by [Rodolfo Figueroa](https://www.kaggle.com/rodolfofigueroa).
- The [Streamlit](https://streamlit.io/) community for providing an intuitive framework for building interactive web applications.

