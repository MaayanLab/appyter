from appyter.ext import fsspec
from appyter.ext.urllib import join_url


def s3_to_url(s3_uri):
  import urllib.parse
  uri = urllib.parse.urlparse(s3_uri)
  q = dict(urllib.parse.parse_qsl(uri.query))
  return urllib.parse.urlparse(f"{'https' if q.get('use_ssl') else 'http'}://{uri.hostname}:{uri.port or (443 if q.get('use_ssl') else 80)}/{uri.path}")

def serve(app_path, **kwargs):
  import os
  import sys
  import logging
  logger = logging.getLogger(__name__)
  from subprocess import Popen
  from appyter.context import get_env, get_jinja2_env, find_blueprints, get_appyter_directory
  config = get_env(**kwargs)
  logger.info(kwargs)
  env = get_jinja2_env(config=config)
  with fsspec.url_to_chroot_fs('tmpfs://') as tmp_fs:
    logger.info(f"Working directory {tmp_fs.path()}")
    #
    logger.info(f"Pre-rendering pages...")
    with fsspec.open(join_url(config['CWD'], config['IPYNB']), 'r') as fr:
      from appyter.parse.nb import nb_from_ipynb_io
      nbtemplate = nb_from_ipynb_io(fr)
    with tmp_fs.open('index.html', 'w') as fw:
      from appyter.render.form import render_form_from_nbtemplate
      fw.write(render_form_from_nbtemplate(env, nbtemplate))
    with tmp_fs.open('index.json', 'w') as fw:
      import json
      from appyter.render.nbinspect import render_nbtemplate_json_from_nbtemplate
      json.dump(render_nbtemplate_json_from_nbtemplate(env, nbtemplate), fw)
    with tmp_fs.open('landing.html', 'w') as fw:
      env.get_template('landing.j2').stream(
        _nb=os.path.basename(config['IPYNB']),
      ).dump(fw)
    #
    logger.info(f"Generating production config...")
    with tmp_fs.open('supervisord.conf', 'w') as fw:
      env.get_template('production/supervisord.conf.j2').stream(_tmp_fs=tmp_fs, sys=sys, str=str).dump(fw)
    with tmp_fs.open('nginx.conf', 'w') as fw:
      env.get_template('production/nginx.conf.j2').stream(
        _tmp_fs=tmp_fs, os=os,
        s3_to_url=s3_to_url,
        get_appyter_directory=get_appyter_directory,
        find_blueprints=find_blueprints,
      ).dump(fw)
    logger.info(f"Starting production instance at http://{config['HOST']}:{config['PORT']}{config['PREFIX']} ...")
    with Popen(['supervisord', '-n', '-c', tmp_fs.path('supervisord.conf')]) as proc:
      try:
        sys.exit(proc.wait())
      except KeyboardInterrupt:
        proc.terminate()
        sys.exit(proc.wait())
