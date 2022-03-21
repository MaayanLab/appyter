def ensure_drs(url):
  ''' Coerces url into a DRS either by locating the DRS or falling back to a appyter-hosted DRS server.
  '''
  from appyter.ext.fsspec.core import url_to_fs_ex
  fs, fo = url_to_fs_ex(url)
  try:
    # Some providers, namely SBFS, provide DRS endpoints already
    return fs.get_drs(fo)
  except AttributeError:
    pass
  # Here we'll point to a drs service we manage which decodes
  #  a HS256 encoded JWT which represents our serialized storage provider.
  #  The recipient of this id will be `appyter.render.flask_app.drs`
  import re, json
  from jwcrypto import jwk, jwe
  from appyter.context import get_env
  env = get_env()
  key = jwk.JWK.from_json(json.dumps({ 'kty': 'oct', 'k': env['SECRET_KEY'] }))
  jwetoken = jwe.JWE(
    json.dumps(dict(fs=json.loads(fs.to_json()), fo=fo)).encode(),
    json.dumps({ 'alg': 'A256KW', 'enc': 'A256CBC-HS512' }),
  )
  jwetoken.add_recipient(key)
  drs_id = jwetoken.serialize(compact=True)
  return f"{re.sub(r'^https?://', 'drs://', env['PUBLIC_URL'])}/{drs_id}"
