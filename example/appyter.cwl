{
  "cwlVersion": "v1.2",
  "class": "CommandLineTool",
  "id": "appyter-example",
  "baseCommand": [
    "python3",
    "-u",
    "-m",
    "appyter",
    "commandify",
    "/app/example.ipynb",
    "run"
  ],
  "hints": [
    {
      "class": "DockerRequirement",
      "dockerPull": "maayanlab/appyter-example:0.0.0-0.19.0-rc.13"
    }
  ],
  "label": "My Example Appyter",
  "doc": "An awesome appyter that I created.",
  "s:version": "0.0.0-0.19.0-rc.13",
  "s:author": "Daniel J. B. Clarke",
  "s:license": "CC-BY-NC-SA-4.0",
  "s:codeRepository": "https://github.com/MaayanLab/appyter-catalog",
  "s:keywords": [
    "example"
  ],
  "inputs": [
    {
      "id": "title",
      "inputBinding": {
        "prefix": "--title=",
        "separate": false,
        "shellQuote": true
      },
      "type": "string?",
      "label": "Title",
      "default": "My Title"
    },
    {
      "id": "number_1",
      "inputBinding": {
        "prefix": "--number_1=",
        "separate": false,
        "shellQuote": true
      },
      "type": "int",
      "label": "First Number",
      "default": 11
    },
    {
      "id": "number_2",
      "inputBinding": {
        "prefix": "--number_2=",
        "separate": false,
        "shellQuote": true
      },
      "type": "int",
      "label": "Second Number",
      "default": 5
    },
    {
      "id": "operator",
      "inputBinding": {
        "prefix": "--operator=",
        "separate": false,
        "shellQuote": true
      },
      "type": [
        "null",
        {
          "type": "enum",
          "symbols": [
            "add",
            "subtract",
            "multiply",
            "divide",
            "power"
          ]
        }
      ],
      "label": "Operator",
      "default": "add"
    },
    {
      "id": "file",
      "inputBinding": {
        "prefix": "--file=",
        "separate": false,
        "shellQuote": true
      },
      "type": "File?",
      "label": "File Upload Test",
      "doc": "File Upload Test",
      "default": {
        "class": "File",
        "path": "/static/test.js",
        "name": "/static/test.js"
      }
    },
    {
      "id": "test-multi-choice",
      "inputBinding": {
        "prefix": "--test-multi-choice=",
        "separate": false,
        "shellQuote": true
      },
      "type": "string?",
      "label": "Test",
      "doc": "test",
      "default": "[\"a\", \"c\"]"
    },
    {
      "id": "test-multi-checkbox",
      "inputBinding": {
        "prefix": "--test-multi-checkbox=",
        "separate": false,
        "shellQuote": true
      },
      "type": "string?",
      "label": "Test",
      "doc": "test multi checkboxes",
      "default": "[\"a\", \"c\"]"
    },
    {
      "id": "test-textlistfield",
      "inputBinding": {
        "prefix": "--test-textlistfield=",
        "separate": false,
        "shellQuote": true
      },
      "type": "string?",
      "label": "TextListField",
      "default": "hello\nworld"
    },
    {
      "id": "s",
      "inputBinding": {
        "prefix": "-s",
        "separate": true,
        "shellQuote": true
      },
      "type": "string?",
      "label": "Location to send realtime update stream"
    },
    {
      "id": "w",
      "inputBinding": {
        "prefix": "-w",
        "separate": true,
        "shellQuote": true
      },
      "type": "string",
      "default": "output",
      "label": "Work directory (all files are collected/output here)"
    }
  ],
  "outputs": [
    {
      "id": "report",
      "type": "Directory",
      "outputBinding": {
        "glob": "$(inputs.w)"
      }
    }
  ],
  "s:programmingLanguage": "Python",
  "$namespaces": {
    "s": "https://schema.org"
  },
  "$schemas": [
    "https://schema.org/version/latest/schemaorg-current-http.rdf"
  ]
}
