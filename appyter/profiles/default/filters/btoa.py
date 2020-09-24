import base64

def btoa(s):
  return base64.b64encode(s.encode()).decode()
