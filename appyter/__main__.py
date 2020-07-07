def main():
  # load dotenv if present
  from dotenv import load_dotenv
  load_dotenv()
  # load everything permitting injection to cli
  import os
  from appyter.util import importdir
  importdir(os.path.join(os.path.dirname(__file__)), __package__, globals())
  # grab cli
  from appyter.cli import cli
  cli()

if __name__ == '__main__':
  main()
