from math import floor
import re
import Levenshtein as lev

from util.video import videoLengthToMS

from config import (MS_DEDUCT, TERMS_POINTS_NEGATIVE, TITLE_CONTAINS_SONG_NAME_POINTS, TITLE_IS_TRACK_BACKWARDS_POINTS,
  TITLE_IS_TRACK_NAME_POINTS, TITLE_IS_SONG_NAME_POINTS, TERMS_POINTS_POSITIVE, DISTANCE_DEDUCT,
  ARTIST_IN_CHANNEL_NAME_POINTS, VIEW_WEIGHT)

def getBarebones(text):
  return re.sub(r"[^.a-zA-Z\d]", "", text)

def getDistance(text1, text2, barebones=True):
  if barebones:
    text1 = getBarebones(text1)
    text2 = getBarebones(text2)
  return lev.distance(text1, text2)

def getVideoScore(searchQuery, track, video):
  score = 0

  # check if video title is exact match for song name
  bbSongName = getBarebones(track["name"].lower())
  bbVideoTitle = getBarebones(video["title"].lower())
  if bbSongName == bbVideoTitle:
    score = TITLE_IS_SONG_NAME_POINTS

  # check if video title is exact match for "artist - song name"
  bbSearchQuery = getBarebones(searchQuery.lower())
  if bbSearchQuery == bbVideoTitle and score < TITLE_IS_TRACK_NAME_POINTS:
    score = TITLE_IS_TRACK_NAME_POINTS

  # check for "track - artist"
  bbBackwards = getBarebones(track["name"].lower() + track["artists"][0]["name"].lower())
  if bbBackwards == bbVideoTitle and score < TITLE_IS_TRACK_BACKWARDS_POINTS:
    score = TITLE_IS_TRACK_BACKWARDS_POINTS

  # if not exact match, check preferred terms and distance
  if score == 0:
    # set base score based on preferred terms
    for term, points in TERMS_POINTS_POSITIVE.items():
      term = term.lower()
      if term in video["title"].lower() and term not in searchQuery:
        if points > score:
          score = points

    # deduct points if unwanted terms found
    for term, points in TERMS_POINTS_NEGATIVE.items():
      term = term.lower()
      if term in video["title"].lower() and term not in searchQuery:
        score -= points

    # add points if video title contains song name
    if bbSongName in bbVideoTitle:
      score += TITLE_CONTAINS_SONG_NAME_POINTS

    # deduct points based on distance
    distanceSQ = getDistance(bbSearchQuery, bbVideoTitle, False)
    distanceN = getDistance(bbSongName, bbVideoTitle, False)
    distance = min([distanceSQ, distanceN])

    score -= floor(distance * DISTANCE_DEDUCT)

  # deduct points based on duration difference
  trackDur = int(track["duration_ms"])
  vidDur = videoLengthToMS(video["duration"])
  diff = abs(trackDur - vidDur)
  score -= floor(diff / MS_DEDUCT)

  # add points if artist in channel name
  bbArtist = getBarebones(track["artists"][0]["name"].lower())
  bbChannel = getBarebones(video["channel"]["name"].lower())
  if bbArtist in bbChannel:
    score += ARTIST_IN_CHANNEL_NAME_POINTS

  return score

def updateScoresForViews(videos):
  def getViews(video):
    return video["views"]

  sortedVideos = sorted(videos, key=getViews, reverse=True)

  videoCount = 0
  for video in sortedVideos:
    video["score"] += (len(sortedVideos) - videoCount) * VIEW_WEIGHT
    videoCount += 1