def serve(app_path, **kwargs):
  import os
  import appyter
  from aiohttp_devtools.logs import setup_logging
  from aiohttp_devtools.runserver import runserver, run_app
  setup_logging(True)
  run_app(*runserver(
    # the path of appyter's install location
    python_path=os.path.dirname(appyter.__path__[0]),
    # the path to this particular file
    app_path=app_path,
    # server configuration
    host=kwargs.get('host'),
    main_port=kwargs.get('port'),
    # watch cwd, we serve static files a different way
    static_path=kwargs.get('cwd'),
    static_url='/_static/',
  ))
