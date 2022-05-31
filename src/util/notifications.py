import zroya
import webbrowser

from util.clipboard import Clipboard

from config import ACTION_CENTER_MS, MAX_NOTIFICATIONS

# initialise zroya
status = zroya.init(
  app_name="s2yt",
  company_name="s2yt",
  product_name="s2yt",
  sub_product="s2yt",
  version="s2yt"
)

# create zroya template
template = zroya.Template(zroya.TemplateType.ImageAndText4)

# time in ms until notification is removed from windows action center
# does not affect length that the notification is displayed for
template.setExpiration(ACTION_CENTER_MS)

# add actions to template
songIDIndex = template.addAction("Copy ID")
songURLIndex = template.addAction("Open URL")
songName = template.addAction("Copy Track")

# create notifications list
notifications = []

def action(notificationID, actionIndex):
  clipboard = Clipboard()

  # get song id for matching notification id
  notification = None
  for notif in notifications:
    if notif["notificationID"] == notificationID:
      notification = notif
      break

  # unable to find matching notification
  if notification == None: return

  if actionIndex == 0: # song ID
    return clipboard.saveToClipboard(notification["songID"])
  if actionIndex == 1: # song url
    # return clipboard.saveToClipboard("https://youtube.com/watch?v=%s" % notification["songID"])
    browser = webbrowser.get()
    browser.open_new_tab("https://youtube.com/watch?v=%s" % notification["songID"])
  if actionIndex == 2: # song name
    return clipboard.saveToClipboard(notification["fullName"])

def notify(songID, fullName, videoTitle):
  # set notification text
  template.setFirstLine(fullName)
  template.setSecondLine(videoTitle)

  # remove oldest notification if above limit
  if len(notifications) > MAX_NOTIFICATIONS:
    notifications.pop(0)

  # display notification
  notificationID = zroya.show(template, on_action=action)

  # save notification details
  notifications.append({
    "notificationID": notificationID,
    "songID": songID,
    "fullName": fullName
  })