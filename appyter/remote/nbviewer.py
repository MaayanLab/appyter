import sys
import json
import tempfile
from subprocess import Popen, PIPE

from appyter.context import get_env, get_jinja2_env
from appyter.render.nbviewer import render_nb_from_stream

def jupyter_inline_evaluate(url, context):
  def stream_generator():
      with tempfile.NamedTemporaryFile('w') as tmp:
          tmp.close()
          with open(tmp.name, 'w') as fw:
              json.dump(context, fw)

          with Popen([
              sys.executable,
              '-u',
              '-m', 'appyter',
              'remote', 'nbevaluate',
              f"--context={tmp.name}",
              url,
          ], stdout=PIPE, stderr=PIPE) as proc:
              packet = proc.stderr.readline()
              while packet:
                  yield packet.decode()
                  packet = proc.stderr.readline()

  env = get_jinja2_env(get_env(**dict(ipynb='app.ipynb'))) 
  render_nb_from_stream(env, stream_generator())
