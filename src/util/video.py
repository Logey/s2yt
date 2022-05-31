def videoLengthToMS(length):
  try:
    lengthSplit = length.split(":")
    h = m = s = ms = 0

    if len(lengthSplit) == 2:
      m = int(lengthSplit[0])
      s = int(lengthSplit[1])
    elif len(lengthSplit) == 3:
      h = int(lengthSplit[0])
      m = int(lengthSplit[1])
      s = int(lengthSplit[2])

    if s > 0: ms += s*1000
    if m > 0: ms += m*60*1000
    if h > 0: ms += h*60*60*1000
  except:
    ms = 0

  return ms

def viewsInt(viewsText):
  try:
    viewsTextSplit = viewsText.split(" view")
    views = int(viewsTextSplit[0].replace(",", ""))
  except:
    views = 0
  return views