# completely skip videos including these terms (case INsensitive)
# if the song or artist name includes this string, it will not be ignored
IGNORED_TERMS = [
  # unwanted remixes
  "nightcore",

  # cartoon / anime episodes
  "episode",

  # top 10 videos
  "top 10"
]

# number of milliseconds for the notification to stay in windows action center
ACTION_CENTER_MS = 1800000 # 30 mins

# max notifications to keep in memory
MAX_NOTIFICATIONS = 10

# how frequent, in seconds, to check the clipboard for a new spotify link
CLIPBOARD_CHECK_FREQUENCY = 0.1

# max videos to search on youtube
MAX_SEARCH_RESULTS = 15

# points to reward for video title being the exact song name
TITLE_IS_SONG_NAME_POINTS = 100

# points to reward for video title containing the song name
TITLE_CONTAINS_SONG_NAME_POINTS = 50

# points to reward for video title being exact "artist - song" name
TITLE_IS_TRACK_NAME_POINTS = 120

# if the video title is "song name - artist"
TITLE_IS_TRACK_BACKWARDS_POINTS = 100

# how many points to reward certain search terms (case INsensitive)
# the video with the highest points is chosen
TERMS_POINTS_POSITIVE = {
  "official audio": 100,
  "audio": 90,
  "official lyric": 80,
  "lyric": 70,
  "legendado": 65, # spanish lyric video
  "official music video": 60,
  "music video": 50,
  "explicit": 10 # uncensored
}

# deduct points if these terms are found in the video title
TERMS_POINTS_NEGATIVE = {
  "remix": 50,
  "cover": 40,
  "live": 40,
  "guitar": 20,
  "parody": 10,
  ",": 8
}

# how many points to deduct per 1 distance
DISTANCE_DEDUCT = 5

# how many milliseconds difference to deduct 1 point
MS_DEDUCT = 2500

# should it take views into account?
SHOULD_SCORE_FOR_VIEWS = False

# how much should view count affect scores?
VIEW_WEIGHT = 2

# how many points to reward if the artist name is in the channel name
ARTIST_IN_CHANNEL_NAME_POINTS = 10