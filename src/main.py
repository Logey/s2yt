import time
from youtubesearchpython import VideosSearch
from util.score import getVideoScore

from util.spotify import spotify
from util.clipboard import Clipboard
from util.video import viewsInt
from util.score import updateScoresForViews
from util.notifications import notify

from config import CLIPBOARD_CHECK_FREQUENCY, IGNORED_TERMS, MAX_SEARCH_RESULTS

# main code
if __name__ == "__main__":
  # constantly check for clipboard updates
  clipboard = Clipboard()
  while True:
    if clipboard.isClipboardUpdated() and clipboard.isSpotifyLink():
      # get spotify track from clipboard
      spotifyTrack = clipboard.readClipboard()
      track = spotify.track(spotifyTrack)

      # search youtube for videos
      searchQuery = "%s - %s" % (track["artists"][0]["name"], track["name"])
      videosSearch = VideosSearch(searchQuery, limit=MAX_SEARCH_RESULTS)
      videos = videosSearch.result()["result"]

      # init list for scored videos
      scoredVideos = []

      # loop through videos
      for vid in videos:
        # check if video title contains ignored term
        shouldIgnore = False
        titleLower = vid["title"].lower()
        searchQueryLower = searchQuery.lower()
        for term in IGNORED_TERMS:
          term = term.lower()
          if term in titleLower and term not in searchQueryLower:
            shouldIgnore = True
            break

        if shouldIgnore: continue

        # score video
        scoredVideos.append({
          "id": vid["id"],
          "url": "https://youtube.com/watch?v=" + vid["id"],
          "title": vid["title"],
          "views": viewsInt(vid["viewCount"]["text"]),
          "score": getVideoScore(searchQuery, track, vid)
        })

      # add more score based on views
      updateScoresForViews(scoredVideos)

      # get highest score video
      # highestID = highestScore = None
      highest = None
      for vid in scoredVideos:
        if highest == None or vid["score"] > highest["score"]:
          highest = vid

      # print(json.dumps(scoredVideos, indent=2))
      print(highest)
      notify(highest["id"], track["name"], highest["title"])

    # sleep for user-specified time between clipboard checks
    time.sleep(CLIPBOARD_CHECK_FREQUENCY)