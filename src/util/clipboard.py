import pyperclip

class Clipboard:
  latestValue = ""

  def __init__(self):
    self.latestValue = ""

  def saveToClipboard(self, text):
    pyperclip.copy(text)

  def readClipboard(self, forceUpdate=False):
    if forceUpdate:
      self.latestValue = pyperclip.paste()
      return self.latestValue
    return pyperclip.paste()

  def isClipboardUpdated(self):
    currentValue = self.readClipboard()
    if currentValue != self.latestValue:
      self.latestValue = currentValue
      return True
    return False

  def isSpotifyLink(self, forceUpdate=False):
    clipboard = self.readClipboard(forceUpdate)
    return clipboard.startswith("https://open.spotify.com/track/")