import contextlib
import typing as t

@contextlib.asynccontextmanager
async def adhoc_ssl_context(
  cn: t.Optional[str] = None,
  protocol: t.Optional[int] = None,
):
  '''
  From https://github.com/pallets/werkzeug/blob/main/src/werkzeug/serving.py
  Produces an adhoc SSL cert and returns an SSL context for https in development.
  '''
  import os
  import ssl
  import tempfile
  from datetime import datetime as dt
  from datetime import timedelta, timezone

  from cryptography import x509
  from cryptography.hazmat.backends import default_backend
  from cryptography.hazmat.primitives import hashes, serialization
  from cryptography.hazmat.primitives.asymmetric import rsa
  from cryptography.x509.oid import NameOID
  backend = default_backend()
  pkey = rsa.generate_private_key(
    public_exponent=65537, key_size=2048, backend=backend
  )
  if cn is None: cn = '*'
  subject = x509.Name([
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Dummy Certificate"),
    x509.NameAttribute(NameOID.COMMON_NAME, cn),
  ])
  backend = default_backend()
  cert = (
      x509.CertificateBuilder()
      .subject_name(subject)
      .issuer_name(subject)
      .public_key(pkey.public_key())
      .serial_number(x509.random_serial_number())
      .not_valid_before(dt.now(timezone.utc))
      .not_valid_after(dt.now(timezone.utc) + timedelta(days=365))
      .add_extension(x509.ExtendedKeyUsage([x509.OID_SERVER_AUTH]), critical=False)
      .add_extension(x509.SubjectAlternativeName([x509.DNSName(cn)]), critical=False)
      .sign(pkey, hashes.SHA256(), backend)
  )
  cert_handle, cert_file = tempfile.mkstemp()
  pkey_handle, pkey_file = tempfile.mkstemp()
  os.write(cert_handle, cert.public_bytes(serialization.Encoding.PEM))
  os.write(
      pkey_handle,
      pkey.private_bytes(
          encoding=serialization.Encoding.PEM,
          format=serialization.PrivateFormat.TraditionalOpenSSL,
          encryption_algorithm=serialization.NoEncryption(),
      ),
  )

  os.close(cert_handle)
  os.close(pkey_handle)

  if protocol is None:
      protocol = ssl.PROTOCOL_TLS_SERVER
  
  ctx = ssl.SSLContext(protocol)
  ctx.load_cert_chain(cert_file, pkey_file)

  try:
    yield ctx
  finally:
    os.remove(pkey_file)
    os.remove(cert_file)
