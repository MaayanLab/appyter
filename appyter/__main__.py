if __name__ == '__main__':
  # load dotenv if present
  from dotenv import load_dotenv
  load_dotenv()
  # 
  from appyter.cli import cli
  from appyter.render.flask_app import app
  cli()
