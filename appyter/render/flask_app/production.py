import fsspec
from appyter.ext.urllib import join_url
from appyter.ext.tempfile import tempdir

def serve(app_path, **kwargs):
  import os
  import sys
  import logging
  logger = logging.getLogger(__name__)
  from subprocess import Popen
  from appyter.context import get_env, get_jinja2_env, find_blueprints, get_appyter_directory
  config = get_env(**kwargs, mode='prerender')
  logger.info(kwargs)
  env = get_jinja2_env(config=config)
  exit_code = 1
  with tempdir() as tmp_dir:
    logger.info(f"Working directory {tmp_dir}")
    #
    logger.info(f"Pre-rendering pages...")
    with fsspec.open(join_url(config['CWD'], config['IPYNB']), 'r') as fr:
      from appyter.parse.nb import nb_from_ipynb_io
      nbtemplate = nb_from_ipynb_io(fr)
    with (tmp_dir/'index.html').open('w') as fw:
      from appyter.render.form import render_form_from_nbtemplate
      fw.write(render_form_from_nbtemplate(env, nbtemplate))
    with (tmp_dir/'index.json').open('w') as fw:
      import json
      from appyter.render.nbinspect.nbtemplate_json import render_nbtemplate_json_from_nbtemplate
      json.dump(render_nbtemplate_json_from_nbtemplate(env, nbtemplate), fw)
    with (tmp_dir/'landing.html').open('w') as fw:
      env.get_template('landing.j2').stream(
        _nb=os.path.basename(config['IPYNB']),
      ).dump(fw)
    #
    logger.info(f"Generating production config...")
    with (tmp_dir/'supervisord.conf').open('w') as fw:
      env.get_template('production/supervisord.conf.j2').stream(_tmp_dir=tmp_dir, sys=sys, str=str).dump(fw)
    with (tmp_dir/'nginx.conf').open('w') as fw:
      env.get_template('production/nginx.conf.j2').stream(
        _tmp_dir=tmp_dir, os=os, str=str,
        get_appyter_directory=get_appyter_directory,
        find_blueprints=find_blueprints,
      ).dump(fw)
    logger.info(f"Starting production instance at http://{config['HOST']}:{config['PORT']}{config['PREFIX']}/ ...")
    with Popen(['supervisord', '-n', '-c', str(tmp_dir/'supervisord.conf')]) as proc:
      try:
        exit_code = proc.wait()
      except KeyboardInterrupt:
        proc.terminate()
        exit_code = proc.wait()
  #
  return exit_code
