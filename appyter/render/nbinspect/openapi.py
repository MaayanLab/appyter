from appyter.render.nbinspect.jsonschema import render_jsonschema_from_nbtemplate

def render_openapi_from_nbtemplate(env, nb):
  ''' Render a openapi representing the relevant Fields throughout the notebook.
  TODO: outputs
  TODO: appyter.json metadata
  '''
  schema = {
    'openapi': '3.1.0',
    'info': {
      # TODO
      'version': '1.0.0',
      'title': 'Appyter API',
      'description': 'An API for interfacing with the Appyter.',
      # termsOfService:
      'contact': {
        'name': "Ma'ayan Lab",
        # 'email': '',
        'url': 'https://maayanlab.cloud/',
      },
      'license': {
        'name': 'CC-BY-NC-SA',
        'url': 'https://github.com/MaayanLab/appyter/blob/main/LICENSE',
      },
    },
    'servers': [
      { 'url': '/' },
    ],
    'paths': {
      '/': {
        'get': {
          'description': 'Get information about this appyter',
          'operationId': 'appyter_inspect',
          'responses': {
            '200': {
              'description': 'Appyter instance',
              'content': {
                'application/vnd.jupyter': {
                  # 'description': 'Appyter notebook',
                  'schema': {
                    '$ref': '#/components/schemas/AppyterIPYNB',
                  },
                },
                'application/json': {
                  # 'description': 'Appyter nbinspect',
                  'schema': {
                    '$ref': '#/components/schemas/AppyterNBInspect',
                  },
                },
                'text/html': {
                  # 'description': 'Appyter form',
                  'schema': {
                    'type': 'string',
                  },
                },
              },
            },
          },
        },
        'post': {
          'description': 'Executes the appyter',
          'operationId': 'appyter_execute',
          'requestBody': {
            'required': True,
            'content': {
              'multipart/form-data': {
                'schema': render_jsonschema_from_nbtemplate(env, nb),
              },
            },
          },
          'responses': {
            '200': {
              'description': 'Appyter results',
              'content': {
                'application/json': {
                  'schema': {
                    'type': 'object',
                    'properties': {
                      'session_id': {
                        'type': 'string',
                        'description': 'A unique identifier for this appyter invokation',
                      },
                    },
                  },
                },
              },
            },
            '406': {
              'description': 'Not acceptable error, field(s) did not satisfy constraint(s)',
              'content': {
                'application/json': {
                  'schema': {
                    '$ref': '#/components/schemas/Error',
                  },
                },
              },
            },
          },
        },
      },
      '/{session_id}/': {
        'get': {
          'description': 'Fetch or interact with an appyter instance',
          'operationId': 'appyter_instance_fetch',
          'parameters': [
            {
              'in': 'path',
              'name': 'session_id',
              'schema': {
                'type': 'string'
              },
              'required': True,
              'description': 'Session identifier',
            },
          ],
          'responses': {
            '200': {
              'description': 'Appyter instance',
              'content': {
                'application/vnd.jupyter': {
                  # 'description': 'Appyter instance',
                  'schema': {
                    "$ref": "#/components/schemas/AppyterInstanceIPYNB",
                  },
                },
                'application/json': {
                  # 'description': 'Appyter instance',
                  'schema': {
                    "$ref": "#/components/schemas/AppyterInstanceIPYNB",
                  },
                },
                'text/html': {
                  # 'description': 'Interactive appyter instance viewer',
                  'schema': {
                    'type': 'string',
                  },
                },
              },
            },
            '404': {
              'description': 'Appyter instance not found',
            },
          },
        },
      },
    },
    'components': {
      'schemas': {
        'AppyterNBInspect': {
          'description': 'Appyter field extracts',
          'type': 'array',
          'items': {
            'type': 'object',
            'properties': {
              'field': {
                'type': 'string',
              },
              'args': {
                'description': 'Field-specific arguments',
                'type': 'object',
                'properties': {
                  'name': {
                    'description': 'The unique name of this field',
                    'type': 'string',
                  },
                  'label': {
                    'description': 'A human readable label for the field',
                    'type': 'string',
                  },
                  'description': {
                    'description': 'A human readable description for the field',
                    'type': 'string',
                  },
                  'choices': {
                    'description': 'A list or lookup dictionary of possible choices',
                    'oneOf': [
                      {'type': 'array', 'items': { '$ref': '#/components/schemas/Any' }},
                      {'type': 'object', 'additionalProperties': { '$ref': '#/components/schemas/Any' }},
                    ]
                  },
                  'required': {
                    'description': 'Whether or not this field is required',
                    'type': 'boolean',
                    'default': False,
                  },
                  'default': {
                    'description': 'The value used if not provided',
                    '$ref': '#/components/schemas/Any',
                  },
                },
                'required': ['name'],
                'additionalProperties': True,
              },
            },
          },
        },
        'AppyterIPYNB': {
          'description': 'Appyter IPython Notebook format',
          'type': 'object',
          'properties': {
            'metadata': {
              'description': 'Jupyter notebook metadata',
              'type': 'object',
              'properties': {
                'appyter': {
                  'description': 'Appyter specific metadata',
                  'type': 'object',
                  'properties': {
                    'info': {
                      '$ref': 'https://raw.githubusercontent.com/MaayanLab/appyter-catalog/master/schema/appyter-validator.json',
                    },
                  },
                },
              },
            },
          },
        },
        'AppyterInstanceIPYNB': {
          'description': 'Appyter Instance IPython Notebook format',
          'type': 'object',
          'properties': {
            'metadata': {
              'description': 'Jupyter notebook metadata',
              'type': 'object',
              'properties': {
                'appyter': {
                  'description': 'Appyter specific metadata',
                  'type': 'object',
                  'properties': {
                    'info': {
                      '$ref': 'https://raw.githubusercontent.com/MaayanLab/appyter-catalog/master/schema/appyter-validator.json',
                    },
                    'nbconstruct': {
                      'type': 'object',
                      'properties': {
                        'filename': {
                          'type': 'string',
                        },
                        'files': {
                          'description': 'File name to source mapping used during nbconstruct',
                          'type': 'object',
                          'additionalProperties': {
                            'type': 'string',
                          },
                        },
                        'version': {
                          'description': 'Version of appyter used for nbconstruct',
                          'type': 'string',
                        },
                      },
                    },
                    'nbexecute': {
                      'type': 'object',
                      'properties': {
                        'started': {
                          'description': 'Server time when nbexecute was started',
                          'type': 'string',
                          'format': 'date-time',
                        },
                        'completed': {
                          'description': 'Server time when nbexecute completed',
                          'type': 'string',
                          'format': 'date-time',
                        },
                        'files': {
                          'description': 'File name to source mapping present after nbexecute',
                          'type': 'object',
                          'additionalProperties': {
                            'type': 'string',
                          },
                        },
                        'version': {
                          'description': 'Version of appyter used for nbexecute',
                          'type': 'string',
                        },
                      },
                    },
                  },
                },
              },
              'additionalProperties': True,
            },
          },
          'additionalProperties': True,
        },
        'Error': {
          'type': 'object',
          'properties': {
            'error': {
              'type': 'object',
              'properties': {
                'cls': {
                  'type': 'string',
                  'description': 'Specific type of error',
                },
                'message': {
                  'type': 'string',
                  'description': 'Human readable indication of what went wrong',
                },
              },
            },
          },
          'additionalProperties': True,
          'required': ['cls'],
        },
        'Any': {
          'oneOf': [
            {'type': 'null'},
            {'type': 'string'},
            {'type': 'number'},
            {'type': 'integer'},
            {'type': 'boolean'},
            {'type': 'array', 'items': { '$ref': '#/components/schemas/Any' } },
            {'type': 'object', 'additionalProperties': { '$ref': '#/components/schemas/Any' } },
          ],
        },
      },
    },
  }
  return schema
