# ignore videos including these strings (not case sensitive)
# if the song or artist name includes this string, it will not be ignored
EXCLUSIONS = [
  # no lyrics / instrumental version
  "karaoke", "instrumental", "acoustic",

  # unintended remixes
  "nightcore", "remix", "bootleg",

  # fan-edits / filters
  "8d audio", "bass boost",

  # censored versions
  "clean",

  # covers
  "cover",

  # live / concert recordings
  "live", "concert", "austin city limits"
]

# maximum distance to accept if the song name is not found in the video title
# used for typos - higher numbers are less strict
MAX_DISTANCE = 11