import base64

def atob(s):
  return base64.b64decode(s.encode()).decode()
