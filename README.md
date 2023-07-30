# Spotify to YouTube Playlist Generator

## Introduction

This Python script allows you to generate a YouTube playlist containing music videos of songs from a Spotify playlist. The script uses the Spotify and YouTube APIs for retrieving track data and searching for music videos on YouTube.

### Security Disclaimer

⚠️ **Security Notice:** This code does not include encryption for sensitive credential information. The Spotify Client ID, Client Secret, YouTube API Key, and other sensitive data are stored in plain text in the `.env` file. When using this code or forking the repository, exercise caution and ensure that you protect your sensitive data properly.

Always follow best practices when handling sensitive information. Do not share your credentials publicly or commit them to version control. Use appropriate encryption techniques and secure storage methods for handling sensitive data in production environments.

Please be responsible with your credentials and follow good security practices to keep your data safe.

### Limitations

Please note the following limitations of the current implementation:

1. **Long Spotify Playlists:** The script may not work efficiently for very long Spotify playlists, as it relies on querying the Spotify API for each track individually and adding each track to a Youtube playlist individually. Spotify and Youtube APIs have rate and usage limitations that could affect the performance for large playlists.

2. **Unfunded Developer Accounts:** If you are using an unfunded Spotify and/or Youtube developer account, you might encounter rate/ usage limitations and restrictions on certain API endpoints, which could impact the functionality of the script. I maxed out my daily Youtube quota 3 times while writing this code.

### Future Improvements

In the future, I plan to enhance the code to address these limitations and improve the overall user experience. One potential improvement is to implement progress tracking and allow the script to build the YouTube playlist over multiple days, accommodating the quota limitations enforced by YouTube's API.

Feel free to contribute to the project and suggest additional improvements!

## Getting Started

### Prerequisites

Before running the script, make sure you have the following:

- Python 3.x installed on your system
- A Spotify Developer Account to obtain the Spotify Client ID and Client Secret
- A Google Developer Account to set up OAuth 2.0 for YouTube and get the YouTube API Key

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/spotify-to-youtube-playlist.git
```

2. Change to the project directory:
```bash
cd spotify-to-youtube-playlist
```

3. Create a virtual environment (optional, but recommended):
```bash
python3 -m venv venv
```

4. Activate the virtual environment:

- **For macOS/Linux:**

```bash
source venv/bin/activate
```

- **For Windows:**
```bash
venv\Scripts\activate
```

5. Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Setup

#### Obtaining Spotify Client ID and Client Secret

To use the Spotify API, you'll need a Client ID and Client Secret. Here's how to obtain them:

1. Visit the Spotify Developer Dashboard: https://developer.spotify.com/dashboard/applications
2. Log in with your Spotify account (or create one if you don't have it).
3. Click "Create an App" and follow the instructions to create a new Spotify App.
4. Once the app is created, you'll find the Client ID and Client Secret on the App's dashboard.

#### Obtaining YouTube API Key

To use the YouTube API, you'll need an API Key. Here's how to obtain it:

1. Go to the Google Developer Console: https://console.developers.google.com/
2. Create a new project or select an existing one.
3. Click "Enable APIs and Services" and search for "YouTube Data API v3."
4. Enable the API and create credentials for your project.
5. Once the credentials are created, you'll find the API Key under "Credentials."

#### Setting Up OAuth 2.0 for YouTube

In order to access private YouTube playlists and perform write operations (creating playlists), you'll need to set up OAuth 2.0:

1. In the Google Developer Console, navigate to the "Credentials" section.
2. Click "Create Credentials" > "OAuth client ID."
3. Select "Desktop app" as the application type.
4. Save the generated client secrets JSON file as "client_secrets.json" in the project directory.

#### Creating the .env File

Create a file named `.env` in the project directory and add the following lines:

```plaintext
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
YOUTUBE_API_KEY=your_youtube_api_key
```

Replace `your_spotify_client_id`, `your_spotify_client_secret`, and `your_youtube_api_key` with the credentials you obtained in the previous steps.

### Usage

Run the script and provide the Spotify playlist URL when prompted:

```bash
python main.py
```
The script will generate a YouTube playlist with music videos of the songs from the Spotify playlist.

### Suggested Uses and Spin-Off Projects

The original intent of this project was to create a way to share your favorite Spotify playlists with older relatives who are perplexed by or too stubborn to create or login to a Spotify account. They'll enjoy listening to the music videos on YouTube without the hassle of signing up for a new platform. (You're welcome, mom!)

This turned out to be a really fun and fast project that touches on some key programming concepts in a non-threatening way. In fact, I kind of feel like it would have been a great homework assignment in high school or college. In that spirit, I've left a couple of exercises for the reader, if you'd like to play around with the code: 

1. **Mashup Machine:** Tweak the search parameters to make a list of something other than music videos. Make a playlist of movie clips, TikTok compilations, or even cooking videos that are (however loosely) based on Spotify playlists.

2. **Instant Karaoke Night:** Tweak the search parameters to find lyrics videos and turn your Spotify playlist into a Youtube karaoke party playlist!

2. **Kpop Bootcamp Generator:** Tweak the search parameters to find dance tutorial videos for your favorite Kpop Spotify playlist so you can learn all the moves of your favorite idol.





