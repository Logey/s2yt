import time, pyperclip, spotipy, re
import Levenshtein as lev
from youtubesearchpython import VideosSearch
from spotipy.oauth2 import SpotifyClientCredentials

from secrets import CLIENT_ID, CLIENT_SECRET
from config import EXCLUSIONS, MAX_DISTANCE

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

latestValue = ""

def ytDurationToMS(duration):
  durationSplit = duration.split(":")
  h = m = s = ms = 0
  if (len(durationSplit) == 2):
    m = int(durationSplit[0])
    s = int(durationSplit[1])
  elif len(durationSplit) == 3:
    h = int(durationSplit[0])
    m = int(durationSplit[1])
    s = int(durationSplit[2])

  if s > 0: ms += s*1000
  if m > 0: ms += m*60*1000
  if h > 0: ms += h*60*60*1000

  return ms

def barebones(string):
  return re.sub(r"[^.a-zA-Z\d]", "", string)

def similarityScore(string1, string2):
  string1 = barebones(string1.lower())
  string2 = barebones(string2.lower())
  return lev.distance(string1, string2)

# watch clipboard for changes
while True:
  currentValue = pyperclip.paste()
  if currentValue != latestValue: # found clipboard change
    latestValue = currentValue
    # check if spotify link
    if currentValue.startswith("https://open.spotify.com/track/"):
      closest = {
        "name": None,
        "id": None,
        "url": None,
        "msDiff": None,
        "distance": None
      }
      def updateClosest(name, id, ms, distance):
        closest["name"] = name
        closest["id"] = id
        closest["url"] = "https://youtube.com/watch?v=%s" % id
        closest["msDiff"] = ms
        closest["distance"] = distance

      track = spotify.track(currentValue)
      duration = int(track["duration_ms"])
      trackName = track["name"]
      artist = track["artists"][0]["name"]
      fullSong = "%s - %s" % (artist, trackName)

      def getClosest(searchQuery, songName):
        videosSearch = VideosSearch(searchQuery)
        videos = videosSearch.result()["result"]

        for video in videos:
          skipVideo = False
          vTitle = video["title"]

          # skip videos where title contains excluded phrase,
          # unless the excluded phrase is part of the song title / artist name
          for exclusion in EXCLUSIONS:
            exclusion = exclusion.lower()
            vTitleLower = vTitle.lower()
            if (exclusion in vTitleLower and exclusion not in searchQuery.lower()):
              skipVideo = True
              break

          # skip videos that surpass the max distance defined in the config
          distance = similarityScore(songName, vTitle)
          distance1 = similarityScore(searchQuery, vTitle)
          if distance1 < distance:
            distance = distance1

          bbSongName = barebones(songName.lower())
          bbVTitle = barebones(vTitle.lower())
          if bbSongName not in bbVTitle and distance > MAX_DISTANCE:
            skipVideo = True

          # skip video if failed any of the above checks
          if skipVideo: continue

          vDuration = int(ytDurationToMS(video["duration"]))
          msDiff = abs(duration - vDuration)
          if closest["id"] == None or msDiff < closest["msDiff"]:
            updateClosest(vTitle, video["id"], msDiff, distance)

      getClosest(fullSong, trackName)

      # if nothing found, search everything before brackets
      if closest["id"] == None and "(" in fullSong:
        fullSongBeforeBracket = fullSong.split("(")[0]
        trackNameBeforeBracket = trackName.split("(")[0]
        getClosest(fullSongBeforeBracket, trackNameBeforeBracket)

      print(closest)

  time.sleep(0.1)