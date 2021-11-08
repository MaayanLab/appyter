import logging
logger = logging.getLogger(__name__)

def url_to_chroot_fs(url, pathmap=None, cached=False, appyter=None, **kwargs):
  ''' Like url_to_fs but supporting our extensions, namely:
  chroot   filesystem path is treated as the root
  pathmap  overlay other fsspec-compatible paths
  appyter  create a pathmap from an appyter ipynb
  cached   cache read/writes
  '''
  from fsspec.core import url_to_fs, split_protocol
  from appyter.ext.fsspec.parse import parse_file_uri_qs
  url, qs = parse_file_uri_qs(url)
  protocol, path = split_protocol(url)
  protocol = protocol or 'file'
  full_url = protocol + '://' + path
  # add protocol options to inner protocol
  if protocol not in kwargs: kwargs[protocol] = {}
  kwargs[protocol].update(qs)
  # ensure auto_mkdir is enabled
  if protocol == 'file':
    if 'auto_mkdir' not in kwargs[protocol]: kwargs[protocol]['auto_mkdir'] = True
  # add chroot
  full_url = 'chroot::' + full_url
  fs, _ = url_to_fs(full_url, **kwargs)
  # apply pathmap as needed
  if pathmap:
    from appyter.ext.fsspec.chroot import ChrootFileSystem
    from appyter.ext.fsspec.mapperfs import MapperFileSystem
    from appyter.ext.fsspec.overlayfs import OverlayFileSystem
    fs = ChrootFileSystem(
      fs=OverlayFileSystem(
        lower_fs=MapperFileSystem(pathmap=pathmap),
        upper_fs=fs,
      )
    )
  elif appyter:
    from appyter import __version__
    from appyter.ext.urllib import join_slash
    from appyter.parse.nb import nb_from_ipynb_io
    from appyter.ext.fsspec.chroot import ChrootFileSystem
    from appyter.ext.fsspec.mapperfs import MapperFileSystem
    from appyter.ext.fsspec.overlayfs import OverlayFileSystem
    url, qs = parse_file_uri_qs(appyter)
    _fs, path = url_to_fs(url, **qs)
    parent, _filename = path.rsplit('/', maxsplit=1)
    # load notebook
    with _fs.open(path, 'rb') as fr:
      nb = nb_from_ipynb_io(fr)
    # grab relevant files from metadata
    metadata = nb.get('metadata', {}).get('appyter', {})
    nbconstruct = metadata.get('nbconstruct', {})
    nbconstruct_version = nbconstruct.get('version', 'unknown')
    if nbconstruct_version and nbconstruct_version == __version__:
      pass
    else:
      logger.warning(f"This appyter was not created with this version, instance version was {nbconstruct_version} and our version is {__version__}. Proceed with caution")
    #
    if 'nbexecute' not in metadata:
      logger.warning('This appyter instance has not been executed, no results will be available')
    elif 'started' in metadata['nbexecute'] and 'completed' not in metadata['nbexecute']:
      logger.warning('This appyter is not finished running, no results will be available')
    elif 'started' in metadata['nbexecute'] and 'completed' in metadata['nbexecute']:
      logger.info(f"Appyter ran from {metadata['nbexecute']['started']} to {metadata['nbexecute']['completed']}")
    else:
      logger.warning('This appyter seems old, this may not work properly, please contact us and we can update it')
    #
    filename = nbconstruct.get('filename', 'appyter.ipynb')
    files = { filename: appyter }
    # input files are fully resolvable
    files.update(nbconstruct.get('files', {}))
    # output files are relative to notebook
    files.update({
      k: join_slash(parent, v)
      for k, v in metadata.get('nbexecute', {}).get('files', {}).items()
    })
    # prepare pathmaped filesystem overlayed on target_fs
    fs = ChrootFileSystem(
      fs=OverlayFileSystem(
        lower_fs=MapperFileSystem(pathmap=files),
        upper_fs=fs,
      ),
    )
  if cached:
    from appyter.ext.fsspec.writecache import WriteCacheFileSystem
    fs = WriteCacheFileSystem(fs=fs)
  return fs
