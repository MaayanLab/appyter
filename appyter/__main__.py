def main():
  # load dotenv if present
  from dotenv import load_dotenv
  load_dotenv()
  # TODO: introspect to get this
  from appyter.cli import cli
  import appyter.profiles
  import appyter.render.flask_app.app
  import appyter.render.nbexecutor
  cli()

if __name__ == '__main__':
  main()
