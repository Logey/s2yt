# ignore videos including these strings (not case sensitive)
# if the song or artist name includes this string, it will not be ignored
EXCLUSIONS = ["karaoke", "nightcore", "live", "remix", "8d audio", "clean", "bootleg"]

# maximum distance to accept if the song name is not found in the video title
# used for typos - higher numbers are less strict
MAX_DISTANCE = 11