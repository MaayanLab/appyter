def main():
  import os
  import appyter.ext.multiprocessing
  # load dotenv if present
  os.environ['PYTHONUTF8'] = '1'
  from dotenv import load_dotenv
  load_dotenv()
  # load everything permitting injection to cli
  from pathlib import Path
  from appyter.ext.importlib import importdir
  importdir(Path(__file__).parent, __package__, globals())
  # grab cli
  from appyter.cli import cli
  cli()

if __name__ == '__main__':
  main()
