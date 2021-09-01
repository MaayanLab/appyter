# {{ cookiecutter.project_name }}

{{ cookiecutter.project_description }}

## Launching the appyter
```bash
appyter --profile=biojupies {{ cookiecutter.project_slug }}.ipynb
```

As long as the terminal is open, the appyter should be available at https://localhost:5000/

## Developing the appyter
The appyter can be developed with any jupyter notebook compatible editor.
```bash
jupyter {{ cookiecutter.project_slug }}.ipynb
```
