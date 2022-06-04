# spotify2youtube (s2yt)
When copying a Spotify URL, automatically generate a matching YouTube URL.

## Setup
1. Download and extract the source code zip from [the releases page](https://github.com/Logey/s2yt/releases/latest).
2. `pip install -r requirements.txt`
3. Create a `src/secrets.py` file - based on the `src/secrets.example.py` file - and fill in your Spotify client key and secret.
4. `python src/main.py`
5. Any Spotify links you copy will automatically have a matching YouTube URL show in the terminal and a notification will appear which you can copy the song ID or song URL from.