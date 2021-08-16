''' ```eval_rst
This module contains :class:`appyter.fields.Field`, the base class for all fields
defined in :mod:`appyter.profiles.default.fields`.
``` '''

import os
import re
import json
from copy import copy
from flask import Markup
from appyter.context import get_jinja2_env

class PartialField:
  ''' Partial instantiation of a field
  Replaces a decorator so that we can still identify it as
   a callable which will produce a field.
  '''
  def __init__(self, field, **kwargs):
    self._field = field
    self._kwargs = kwargs

  def __call__(self, name=None, value=None, **kwargs):
    kwargs = dict(self._kwargs, **kwargs)
    value = kwargs.pop('context').get(name)
    return self._field(name=name, value=value, **kwargs)

def build_fields(fields, context={}, env=None):
  ''' INTERNAL: Build a dictionary of Field instances
  '''
  return {
    field_name: PartialField(field, context=context, _env=env)
    for field_name, field in fields.items()
  }

class FieldConstraintException(Exception):
  def __init__(self, field, field_name, value, message=None):
    self.field = field
    self.field_name = field_name
    self.value = value
    if message is None: message = "{}[{}]: {} does not satisfy constraints".format(field, field_name, repr(value))
    self.message = message
    super().__init__(message)
  
  def as_dict(self):
    return dict(
      field=self.field,
      field_name=self.field_name,
      value=self.value,
      message=self.message,
    )

class Field(dict):
  ''' Base field for which all fields derive
  ```eval_rst
  Base class for all Field objects representing a value that will later be provided via a front-end form.
  See :mod:`appyter.profiles.default.fields` for the actual fields.
  ``` '''
  def __init__(self,
      name=None,
      label=None,
      description=None,
      choices=[],
      required=False,
      default=None,
      value=None,
      section=None,
      _env=None,
      **kwargs):
    '''
    :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
    :param label: (str) A human readable label for the field for the HTML form
    :param description: (Optional[str]) A long human readable description for the field for the HTML form
    :param choices: (Optional[Union[List[str], Set[str], Dict[str, str]]]) A set of choices that are available for this field or lookup table mapping from choice label to resulting value
    :param required: (Optional[bool]) Whether or not this field is required (defaults to false)
    :param default: (Any) A default value as an example and for use during prototyping
    :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
    :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
    :param \**kwargs: Additional keyword arguments used by other fields
    '''
    super().__init__(
      field=self.field,
      args=dict(
        name=name,
        label=label,
        description=description,
        choices=choices,
        required=required,
        default=default,
        value=value if value is not None else default,
        section=section,
        **kwargs,
      )
    )
    assert name is not None, "Name should be defined and unique"
    self._env = _env
  
  @property
  def args(self):
    ''' Get the raw args, the values used to initialize this field
    '''
    return self['args']

  def constraint(self):
    ''' Return true if the received args.value satisfies constraints.
    Should be overridden by subclasses.
    '''
    return (self.raw_value is None and not self.args.get('required')) or (self.raw_value in self.choices)

  def render(self, **kwargs):
    ''' Return a rendered version of the field (form)

    :param \**kwargs: The instance values of the form e.g. `Field.render(**field.args)`
    '''
    return Markup(
      self._env.get_template(
        self.template
      ).render(dict(**kwargs, this=self))
    )

  @property
  def field(self):
    ''' Field name
    '''
    return self.__class__.__name__

  @property
  def template(self):
    ''' Template to use for rendering field
    '''
    return '/'.join(['fields', self.field + '.j2'])

  @property
  def js_url(self):
    ''' Template to use for rendering field
    '''
    from appyter.profiles.default.filters.url_for import url_for
    return url_for('static', filename='js/fields/' + self.field + '.js')

  @property
  def choices(self):
    ''' Potential values to choose from
    '''
    return self.args['choices']

  @property
  def raw_value(self):
    ''' (UNSAFE) Raw value of the field
    '''
    return self.args['value']

  @property
  def value(self):
    ''' (SEMI-SAFE) Effective raw value of the field when parsed and constraints are asserted.
    When instantiating code, you should use safe_value.
    '''
    choices = self.choices
    if self.raw_value is None:
      if not self.args.get('required'):
        return None
      else:
        raise FieldConstraintException(
          field=self.field,
          field_name=self.args['name'],
          value=self.raw_value,
          message='{}[{}] is required'.format(self.field, self.args['name']),
        )
    elif type(choices) == dict:
      if self.raw_value in choices:
        return choices[self.raw_value]
      else:
        raise FieldConstraintException(
          field=self.field,
          field_name=self.args['name'],
          value=self.raw_value,
        )
    elif not self.constraint():
      raise FieldConstraintException(
        field=self.field,
        field_name=self.args['name'],
        value=self.raw_value,
      )
    else:
      return self.raw_value

  @property
  def safe_value(self):
    ''' (SAFE) Effective safe value for use in code, we use `repr` to escape values as necessary
    '''
    return repr(self.value)

  @property
  def render_value(self):
    ''' (SAFE) Effective safe value ready to be displayed, specifically for Markdown output.
    '''
    return Markup(self.value)

  def __str__(self):
    ''' (SAFE) The default str(Field) is just safe_value
    '''
    return self.safe_value
