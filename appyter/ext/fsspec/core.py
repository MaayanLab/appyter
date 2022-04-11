import logging
logger = logging.getLogger(__name__)

def url_to_fs_ex(url, **kwargs):
  ''' Like url_to_fs but get opts from fragment_qs
  '''
  from appyter.ext.urllib import URI
  from fsspec.core import url_to_fs
  uri_parsed = URI(url)
  opts = dict(kwargs, **uri_parsed.fragment_query_ex)
  fs, fspath = url_to_fs(str(uri_parsed.with_fragment(None)), **opts)
  return fs, fspath

def url_to_chroot_fs(url, pathmap=None, cached=False, appyter=None, **kwargs):
  ''' Like url_to_fs but supporting our extensions, namely:
  chroot   filesystem path is treated as the root
  pathmap  overlay other fsspec-compatible paths
  appyter  create a pathmap from an appyter ipynb
  cached   cache read/writes
  '''
  from appyter.ext.fsspec.chroot import ChrootFileSystem
  fs, fs_path = url_to_fs_ex(url, **kwargs)
  # add chroot
  fs = ChrootFileSystem(fs=fs, fo=fs_path)
  # apply pathmap as needed
  if pathmap:
    from appyter.ext.fsspec.mapperfs import MapperFileSystem
    from appyter.ext.fsspec.overlayfs import OverlayFileSystem
    fs = ChrootFileSystem(
      fs=OverlayFileSystem(
        lower_fs=MapperFileSystem(pathmap=pathmap),
        upper_fs=fs,
      )
    )
  elif appyter:
    import urllib.request
    from appyter import __version__
    from appyter.ext.urllib import join_slash
    from appyter.parse.nb import nb_from_ipynb_io
    from appyter.ext.fsspec.mapperfs import MapperFileSystem
    from appyter.ext.fsspec.overlayfs import OverlayFileSystem
    # load notebook
    req = urllib.request.Request(appyter, headers={'Accept': 'application/vnd.jupyter'})
    with urllib.request.urlopen(req) as fr:
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
    files = { filename: filename }
    files.update(nbconstruct.get('files', {}))
    files.update(metadata.get('nbexecute', {}).get('files', {}))
    pathmap = {
      filename: path if '://' in path else join_slash(appyter, path)
      for filename, path in files.items()
    }
    # prepare pathmaped filesystem overlayed on target_fs
    fs = ChrootFileSystem(
      fs=OverlayFileSystem(
        lower_fs=MapperFileSystem(pathmap=pathmap),
        upper_fs=fs,
      ),
    )
  if cached:
    from appyter.ext.fsspec.writecache import WriteCacheFileSystem
    fs = WriteCacheFileSystem(fs=fs)
  return fs
