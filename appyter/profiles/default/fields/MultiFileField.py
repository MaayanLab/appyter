from appyter.profiles.default.fields.FileField import FileField

class MultiFileField(FileField):
  def __init__(self, multiple=True, **kwargs):
    super().__init__(multiple=multiple, **kwargs)
