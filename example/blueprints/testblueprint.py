from flask import Blueprint

testblueprint = Blueprint('testblueprint', __name__)

@testblueprint.route('/')
def testroute():
  return 'Test Blueprint!'
